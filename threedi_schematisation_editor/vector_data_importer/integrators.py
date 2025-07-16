import warnings
from _operator import attrgetter, itemgetter
from collections import namedtuple, defaultdict

from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.utils import (
    update_attributes,
    FeatureManager,
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_INTERSECTION_BUFFER_SEGMENTS,
    get_value_from_feature
)
from threedi_schematisation_editor.utils import (
    gpkg_layer,
    get_next_feature_id,
    spatial_index,
    get_features_by_expression,
)
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning


class LinearIntegrator:
    """ Integrate linear structures onto a channel or similar """
    # shorthand with channel_structure properties
    integrate_structure_data = namedtuple("integrate_structure_data", ["channel_id", "feature", "m", "length"])

    def __init__(self, integrate_model_cls, integrate_layer,
                 target_model_cls, target_layer, target_manager,
                 node_layer, node_manager,
                 fields_configurations, conversion_settings,
                 cross_section_layer, external_source,
                 target_gpkg):
        self.external_source = external_source
        self.integrate_model_cls = integrate_model_cls
        self.target_model_cls = target_model_cls
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings
        # set schematisation layer to add - if any are missing retrieve them from the gpkg
        self.integrate_layer = integrate_layer if integrate_layer else gpkg_layer(target_gpkg, self.integrate_model_cls.__tablename__)
        self.target_layer = target_layer if target_layer else gpkg_layer(target_gpkg, self.target_model_cls.__tablename__)
        self.node_layer = node_layer if node_layer else gpkg_layer(target_gpkg, dm.ConnectionNode.__tablename__)
        self.cross_section_layer = cross_section_layer if cross_section_layer else gpkg_layer(target_gpkg, dm.CrossSectionLocation.__tablename__)
        # feature managers that handle id's for added features
        # for target features and nodes a manager can be supplied such that they match the associated importer
        self.target_manager = target_manager if target_manager else FeatureManager(self.target_model_cls)
        self.node_manager = node_manager if node_manager else FeatureManager(dm.ConnectionNode)
        self.integrate_manager = FeatureManager(get_next_feature_id(self.integrate_layer))
        self.cross_section_manager = FeatureManager(get_next_feature_id(self.cross_section_layer))
        # initialize mappings and indices
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    @classmethod
    def from_importer(cls, integrate_model_cls, integrate_layer, cross_section_layer, importer):
        """ extract data from importer to created matching integrator """
        return cls(integrate_model_cls=integrate_model_cls,
                   integrate_layer=integrate_layer,
                   target_model_cls=importer.target_model_cls,
                   target_layer=importer.target_layer,
                   target_manager=importer.processor.target_manager,
                   node_layer=importer.node_layer,
                   node_manager=importer.processor.node_manager,
                   fields_configurations=importer.fields_configurations,
                   conversion_settings=importer.conversion_settings,
                   cross_section_layer=cross_section_layer,
                   external_source=importer.external_source,
                   target_gpkg=importer.target_gpkg)

    @classmethod
    def get_substring_geometry(cls, curve, start_distance, end_distance, simplify=False):
        curve_substring = curve.curveSubstring(start_distance, end_distance)
        substring_geometry = QgsGeometry(curve_substring)
        if simplify:
            substring_polyline = substring_geometry.asPolyline()
            substring_geometry = QgsGeometry.fromPolylineXY([substring_polyline[0], substring_polyline[-1]])
        return substring_geometry

    def setup_fields_map(self):
        """Setup input layer fields map."""
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        for layer in [self.target_layer, self.node_layer, self.integrate_layer, self.cross_section_layer]:
            layer_name = layer.name()
            layer_fields = layer.fields()
            self.layer_fields_mapping[layer_name] = layer_fields
            self.layer_field_names_mapping[layer_name] = [field.name() for field in layer_fields.toList()]

    def setup_spatial_indexes(self):
        """Setup input layer spatial indexes."""
        self.spatial_indexes_map = {}
        self.spatial_indexes_map['source'] = spatial_index(self.external_source)
        for layer in [self.node_layer, self.cross_section_layer]:
            layer_name = layer.name()
            self.spatial_indexes_map[layer_name] = spatial_index(layer)

    def setup_node_by_location(self):
        """Setup nodes by location."""
        self.node_by_location = {}
        for node_feat in self.node_layer.getFeatures():
            node_geom = node_feat.geometry()
            node_point = node_geom.asPoint()
            self.node_by_location[node_point] = node_feat["id"]

    @staticmethod
    def get_channel_structure_from_line(structure_feat, channel_feat, snapping_distance):
        channel_geometry = channel_feat.geometry()
        structure_geom = structure_feat.geometry()
        poly_line = structure_geom.asPolyline()
        start_point = poly_line[0]
        end_point = poly_line[-1]
        start_geom, end_geom = QgsGeometry.fromPointXY(start_point), QgsGeometry.fromPointXY(end_point)
        start_buffer = start_geom.buffer(snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
        end_buffer = end_geom.buffer(snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
        if all([start_buffer.intersects(channel_geometry), end_buffer.intersects(channel_geometry)]):
            return
        intersection_m = channel_geometry.lineLocatePoint(structure_geom.centroid())
        structure_length = structure_geom.length()
        return LinearIntegrator.integrate_structure_data(
            channel_feat["id"],
            structure_feat,
            intersection_m,
            structure_length)

    @staticmethod
    def get_channel_structure_from_point(structure_feat, channel_feat, snapping_distance,
                                         length_source_field, length_fallback_value):
        structure_geom = structure_feat.geometry()
        channel_geometry = channel_feat.geometry()
        structure_buffer = structure_geom.buffer(snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
        if not structure_buffer.intersects(channel_geometry):
            return
        intersection_m = channel_geometry.lineLocatePoint(structure_geom)
        structure_length = get_value_from_feature(structure_feat, length_source_field, length_fallback_value)
        return LinearIntegrator.integrate_structure_data(
            channel_feat["id"],
            structure_feat,
            intersection_m,
            structure_length)

    def get_channel_structures_data(self, channel_feat, selected_ids=None):
        """Extract and calculate channel structures data."""
        channel_structures = []
        processed_structure_ids = set()
        if selected_ids is None:
            selected_ids = set()
        channel_geometry = channel_feat.geometry()
        structure_features_map, structure_index = self.spatial_indexes_map['source']
        structure_fids = structure_index.intersects(channel_geometry.boundingBox())
        for structure_fid in structure_fids:
            if structure_fid in processed_structure_ids:
                continue
            if selected_ids and structure_fid not in selected_ids:
                continue
            structure_feat = structure_features_map[structure_fid]
            if structure_feat.geometry().type() == QgsWkbTypes.GeometryType.LineGeometry:
                channel_structure = LinearIntegrator.get_channel_structure_from_line(
                    structure_feat,
                    channel_feat,
                    self.conversion_settings.snapping_distance
                )
            elif structure_feat.geometry().type() == QgsWkbTypes.GeometryType.PointGeometry:
                channel_structure = LinearIntegrator.get_channel_structure_from_point(
                    structure_feat,
                    channel_feat,
                    self.conversion_settings.snapping_distance,
                    self.conversion_settings.length_source_field,
                    self.conversion_settings.length_fallback_value)
            else:
                continue
            channel_structures.append(channel_structure)
            processed_structure_ids.add(structure_fid)
        channel_structures.sort(key=attrgetter("m"))
        return channel_structures, processed_structure_ids

    def add_node(self, point, node_layer_fields, node_attributes):
        node_feat = self.node_manager.create_new(QgsGeometry.fromPointXY(point),
                                                 node_layer_fields,
                                                 node_attributes)
        self.node_by_location[point] = node_feat["id"]
        return node_feat

    def update_feature_endpoints(self, dst_feature, **template_node_attributes):
        """Update feature endpoint references."""
        new_nodes = []
        channel_polyline = dst_feature.geometry().asPolyline()
        start_node_point, end_node_point = channel_polyline[0], channel_polyline[-1]
        node_layer_fields = self.layer_fields_mapping[self.node_layer.name()]
        for point in [start_node_point, end_node_point]:
            if point not in self.node_by_location:
                node_feat = self.add_node(point, node_layer_fields, template_node_attributes)
                new_nodes.append(node_feat)
        dst_feature["connection_node_id_start"] =  self.node_by_location[start_node_point]
        dst_feature["connection_node_id_end"] = self.node_by_location[end_node_point]
        return new_nodes

    @staticmethod
    def get_cross_sections_for_channel(channel_feat, cross_section_fids, cross_section_location_features_map):
        cross_sections_for_channel = []
        for cross_section_fid in cross_section_fids:
            cross_section_feat = cross_section_location_features_map[cross_section_fid]
            buffer = cross_section_feat.geometry().buffer(
                DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
            )
            if channel_feat.geometry().intersects(buffer):
                cross_sections_for_channel.append(cross_section_fid)
        return cross_sections_for_channel

    @staticmethod
    def get_closest_cross_section_location(channel_feat, cross_section_layer, source_channel_cross_section_locations):
        channel_geometry = channel_feat.geometry()
        src_channel_cross_section_ids = [str(id) for id in source_channel_cross_section_locations]
        if src_channel_cross_section_ids:
            id_str = ",".join(src_channel_cross_section_ids)
            distance_map = [
                (cross_section_feat, channel_geometry.distance(cross_section_feat.geometry()))
                for cross_section_feat in get_features_by_expression(
                    cross_section_layer, f'"id" in ({id_str})', with_geometry=True
                )
            ]
            distance_map.sort(key=itemgetter(1))
            closest_cross_section_copy = QgsFeature(distance_map[0][0])
            return closest_cross_section_copy

    def update_channel_cross_section_references(self, new_channels, original_channel_id):
        """Update channel cross-section references."""
        source_channel_cross_section_locations = [xs["id"] for xs in
                                       get_features_by_expression(self.cross_section_layer,
                                                                  f'"channel_id" = {original_channel_id}')]
        cross_section_location_features_map, cross_section_location_index = self.spatial_indexes_map[self.cross_section_layer.name()]
        channel_id_idx = self.layer_fields_mapping[self.cross_section_layer.name()].lookupField("channel_id")
        cross_section_location_copies = []
        for channel_feat in new_channels:
            channel_geom = channel_feat.geometry()
            cross_section_fids = cross_section_location_index.intersects(channel_geom.boundingBox())
            # Find any nearby cross sections and associate those to this channel
            cross_sections_for_channel = LinearIntegrator.get_cross_sections_for_channel(channel_feat,
                                                                                         cross_section_fids,
                                                                                         cross_section_location_features_map)
            for cross_section_fid in cross_sections_for_channel:
                self.cross_section_layer.changeAttributeValue(cross_section_fid, channel_id_idx, channel_feat["id"])
            # If no nearby cross sections were found, find the closest cross section create a copy of that one
            if len(cross_sections_for_channel) == 0:
                closest_cross_section_copy = self.get_closest_cross_section_location(channel_feat,
                                                                                     self.cross_section_layer,
                                                                                     source_channel_cross_section_locations)
                if closest_cross_section_copy:
                    self.cross_section_manager.add_feature(closest_cross_section_copy,
                                                           geom=channel_geom.interpolate(channel_geom.length() * 0.5))

                    closest_cross_section_copy["channel_id"] = channel_feat["id"]
                    self.cross_section_layer.addFeatures([closest_cross_section_copy])
                    cross_section_location_copies.append(closest_cross_section_copy)
        return cross_section_location_copies


    @staticmethod
    def is_hanging_cross_section(cross_section_feat, channel_feats, channel_fids):
        """Get cross-sections that are not aligned with any channel."""
        xs_buffer = cross_section_feat.geometry().buffer(DEFAULT_INTERSECTION_BUFFER,
                                                         DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
        # only check channels that were visited
        if len(channel_fids) > 0:
            for channel_fid in channel_fids:
                if xs_buffer.intersects(channel_feats[channel_fid].geometry()):
                    return True
        return False


    def get_hanging_cross_sections(self, visited_channel_ids):
        """Remove cross-sections not aligned with the channels."""
        hanging_cross_section_ids = []
        channel_feats, channels_spatial_index = spatial_index(self.integrate_layer)
        for cross_section_feat in self.cross_section_layer.getFeatures():
            buffer = cross_section_feat.geometry().buffer(DEFAULT_INTERSECTION_BUFFER,
                                                          DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
            channel_fids = channels_spatial_index.intersects(buffer.boundingBox())
            # only consider channels that were visited
            channel_fids = list(set(channel_fids).intersection(visited_channel_ids))
            if len(channel_fids) == 0:
                continue
            is_hanging = LinearIntegrator.is_hanging_cross_section(cross_section_feat, channel_feats, channel_fids)
            if is_hanging:
                hanging_cross_section_ids.append(cross_section_feat.id())
        return hanging_cross_section_ids


    @staticmethod
    def substring_feature(curve, start_distance, end_distance, fields, simplify=False, **attributes):
        """Extract part of the curve as a new structure feature."""
        substring_feat = QgsFeature(fields)
        substring_feat.setGeometry(LinearIntegrator.get_substring_geometry(curve, start_distance, end_distance, simplify))
        for field_name, field_value in attributes.items():
            substring_feat[field_name] = field_value
        return substring_feat

    def integrate_structure_features(self, channel_feat, channel_structures):
        """Integrate structures with a channel network."""
        added_features = defaultdict(list)
        channel_geom = channel_feat.geometry()
        total_length = sum(channel_structure.length for channel_structure in channel_structures)
        if channel_geom.length() < total_length:
            id_str = ', '.join(str(channel_structure.feature.id()) for channel_structure in channel_structures)
            message = (f'Cannot integrate {self.target_model_cls.__tablename__}s with total length {total_length:.2f} '
                       f'into channel {channel_feat["id"]} with length {channel_geom.length():.2f}. '
                       f'Primary keys {self.target_model_cls.__tablename__}s: {id_str}')
            warnings.warn(f"{message}", StructuresIntegratorWarning)
            return added_features
        channel_fields = self.layer_fields_mapping[self.integrate_layer.name()]
        channel_attributes = {field_name: channel_feat[field_name] for field_name in self.layer_field_names_mapping[self.integrate_layer.name()]}
        first_node_feat = next(get_features_by_expression(self.node_layer,
                                                          f'"id" = {channel_attributes["connection_node_id_start"]}'))
        node_attributes = {field_name: first_node_feat[field_name] for field_name in self.layer_field_names_mapping[self.node_layer.name()]}
        simplify_structure_geometry = self.target_model_cls != dm.Culvert
        previous_structure_end = 0
        for i, channel_structure in enumerate(sorted(channel_structures, key=lambda x: x.m)):
            new_nodes = []
            channel_structure_m = channel_structure.m
            half_length = channel_structure.length * 0.5
            # when structures overlap, move them to the end of the previous structure
            if channel_structure_m - half_length < previous_structure_end:
                channel_structure_m = previous_structure_end + half_length
            start_distance = channel_structure_m - half_length
            end_distance = channel_structure_m + half_length
            # Setup structure feature
            substring_geom = LinearIntegrator.get_substring_geometry(channel_geom.constGet(), start_distance, end_distance, simplify_structure_geometry)
            substring_feat = self.target_manager.create_new(substring_geom,
                                                            self.layer_fields_mapping[self.target_layer.name()])
            update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, channel_structure.feature, substring_feat)
            added_features[self.target_layer.name()].append(substring_feat)
            added_features[self.node_layer.name()] += self.update_feature_endpoints(substring_feat, **node_attributes)
            # Setup channel leftover feature
            if start_distance > previous_structure_end:
                before_substring_feat = self.substring_feature(
                    channel_geom.constGet(), previous_structure_end, start_distance, channel_fields, False, **channel_attributes
                )
                self.integrate_manager.add_feature(before_substring_feat, set_id=(i>0))
                added_features[self.integrate_layer.name()].append(before_substring_feat)
                added_features[self.node_layer.name()] += self.update_feature_endpoints(before_substring_feat, **node_attributes)
            previous_structure_end = end_distance
            if new_nodes:
                update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_structure_feat, *new_nodes)
        # Setup last channel leftover feature
        last_substring_end = channel_geom.length()
        if last_substring_end - previous_structure_end > 0:
            last_substring_feat = self.substring_feature(
                channel_geom.constGet(), previous_structure_end, last_substring_end, channel_fields, False, **channel_attributes
            )
            self.integrate_manager.add_feature(last_substring_feat)
            added_features[self.node_layer.name()] += self.update_feature_endpoints(last_substring_feat, **node_attributes)
            added_features[self.integrate_layer.name()].append(last_substring_feat)
        return added_features

    def integrate_features(self, input_feature_ids):
        """Method responsible for the importing/integrating structures from the external feature source."""
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        channels_replaced = []
        for channel_feature in self.integrate_layer.getFeatures():
            channel_structures, processed_structures_fids = self.get_channel_structures_data(channel_feature, input_feature_ids)
            if not channel_structures:
                continue
            added_features = self.integrate_structure_features(channel_feature, channel_structures)
            added_features[self.cross_section_layer.name()] = self.update_channel_cross_section_references(
                added_features[self.integrate_layer.name()], channel_feature["id"])
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= processed_structures_fids
            channels_replaced.append(channel_feature["id"])
        self.integrate_layer.startEditing()
        for ch_id in channels_replaced:
            self.integrate_layer.deleteFeature(ch_id)
        self.cross_section_layer.startEditing()
        visited_channel_ids = [channel["id"] for channel in features_to_add[self.integrate_layer.name()]]
        self.cross_section_layer.deleteFeatures(self.get_hanging_cross_sections(visited_channel_ids))
        return features_to_add, list(all_processed_structure_ids)

