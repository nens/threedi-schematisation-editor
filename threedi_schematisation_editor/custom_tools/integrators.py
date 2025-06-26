import warnings
from _operator import attrgetter, itemgetter
from collections import namedtuple, defaultdict

from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.custom_tools.utils import update_attributes, FeatureManager, \
    DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
from threedi_schematisation_editor.utils import gpkg_layer, get_next_feature_id, spatial_index, \
    get_features_by_expression
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning


class LinearIntegrator:
    """ Integrate linear structures onto a channel or similar """
    # shorthand with channel_structure properties
    channel_structure_cls = namedtuple("channel_structure", ["channel_id", "feature", "m", "length"])

    def __init__(self, integrate_model_cls, integrate_layer,
                 target_model_cls, target_layer, target_manager,
                 node_layer, node_manager,
                 fields_configurations, conversion_settings,
                 cross_section_layer, external_source,
                 target_gpkg):
        # TODO: add tests
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

    def get_channel_structures_data(self, channel_feat, selected_ids=None):
        """Extract and calculate channel structures data."""
        channel_structures = []
        processed_structure_ids = set()
        if selected_ids is None:
            selected_ids = set()
        channel_id = channel_feat["id"]
        channel_geometry = channel_feat.geometry()
        structure_features_map, structure_index = self.spatial_indexes_map['source']
        structure_fids = structure_index.intersects(channel_geometry.boundingBox())
        for structure_fid in structure_fids:
            if structure_fid in processed_structure_ids:
                continue
            if selected_ids and structure_fid not in selected_ids:
                continue
            structure_feat = structure_features_map[structure_fid]
            structure_geom = structure_feat.geometry()
            structure_geom_type = structure_geom.type()
            if structure_geom_type == QgsWkbTypes.GeometryType.LineGeometry:
                poly_line = structure_geom.asPolyline()
                start_point = poly_line[0]
                end_point = poly_line[-1]
                start_geom, end_geom = QgsGeometry.fromPointXY(start_point), QgsGeometry.fromPointXY(end_point)
                start_buffer = start_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                end_buffer = end_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                intersection_m = channel_geometry.lineLocatePoint(structure_geom.centroid())
                structure_length = structure_geom.length()
                if not all([start_buffer.intersects(channel_geometry), end_buffer.intersects(channel_geometry)]):
                    continue
            elif structure_geom_type == QgsWkbTypes.GeometryType.PointGeometry:
                structure_buffer = structure_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                if not structure_buffer.intersects(channel_geometry):
                    continue
                intersection_m = channel_geometry.lineLocatePoint(structure_geom)
                structure_length = (
                    structure_feat[self.conversion_settings.length_source_field]
                    if self.conversion_settings.length_source_field
                    else self.conversion_settings.length_fallback_value
                )
            else:
                continue
            channel_structure = self.channel_structure_cls(channel_id, structure_feat, intersection_m, structure_length)
            channel_structures.append(channel_structure)
            processed_structure_ids.add(structure_fid)
        channel_structures.sort(key=attrgetter("m"))
        return channel_structures, processed_structure_ids

    def update_feature_endpoints(self, dst_feature, **template_node_attributes):
        """Update feature endpoint references."""
        new_nodes = []
        linear_geom = dst_feature.geometry()
        channel_polyline = linear_geom.asPolyline()
        start_node_point, end_node_point = channel_polyline[0], channel_polyline[-1]
        node_layer_name = self.node_layer.name()
        node_layer_fields = self.layer_fields_mapping[node_layer_name]
        # TODO: remove duplicate code
        try:
            start_node_id = self.node_by_location[start_node_point]
        except KeyError:
            start_node_feat = self.node_manager.create_new(QgsGeometry.fromPointXY(start_node_point), node_layer_fields)
            start_node_id = start_node_feat["id"]
            for field_name, field_value in template_node_attributes.items():
                if field_name == "id":
                    continue
                start_node_feat[field_name] = field_value
            self.node_by_location[start_node_point] = start_node_id
            new_nodes.append(start_node_feat)
        try:
            end_node_id = self.node_by_location[end_node_point]
        except KeyError:
            end_node_feat = self.node_manager.create_new(QgsGeometry.fromPointXY(end_node_point), node_layer_fields)
            end_node_id = end_node_feat["id"]
            for field_name, field_value in template_node_attributes.items():
                if field_name == "id":
                    continue
                end_node_feat[field_name] = field_value
            self.node_by_location[end_node_point] = end_node_id
            new_nodes.append(end_node_feat)
        dst_feature["connection_node_id_start"] = start_node_id
        dst_feature["connection_node_id_end"] = end_node_id
        return new_nodes

    def update_channel_cross_section_references(self, new_channels, source_channel_xs_locations):
        """Update channel cross-section references."""
        xs_location_features_map, xs_location_index = self.spatial_indexes_map[self.cross_section_layer.name()]
        xs_fields = self.layer_fields_mapping[self.cross_section_layer.name()]
        channel_id_idx = xs_fields.lookupField("channel_id")
        next_cross_section_location_id = get_next_feature_id(self.cross_section_layer)
        cross_section_location_copies = []
        for channel_feat in new_channels:
            channel_xs_count = 0
            channel_id = channel_feat["id"]
            channel_geometry = channel_feat.geometry()
            channel_geometry_middle = channel_geometry.interpolate(channel_geometry.length() * 0.5)
            xs_fids = xs_location_index.intersects(channel_geometry.boundingBox())
            for xs_fid in xs_fids:
                xs_feat = xs_location_features_map[xs_fid]
                xs_geom = xs_feat.geometry()
                xs_buffer = xs_geom.buffer(
                    DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                if channel_geometry.intersects(xs_buffer):
                    self.cross_section_layer.changeAttributeValue(xs_fid, channel_id_idx, channel_id)
                    channel_xs_count += 1
            if channel_xs_count == 0:
                src_channel_xs_ids = [str(xs_id) for xs_id in source_channel_xs_locations]
                if src_channel_xs_ids:
                    xs_ids_str = ",".join(src_channel_xs_ids)
                    xs_distance_map = [
                        (xs_feat, channel_geometry.distance(xs_feat.geometry()))
                        for xs_feat in get_features_by_expression(
                            self.cross_section_layer, f'"id" in ({xs_ids_str})', with_geometry=True
                        )
                    ]
                    xs_distance_map.sort(key=itemgetter(1))
                    closest_xs_feat_copy = QgsFeature(xs_distance_map[0][0])
                    closest_xs_feat_copy.setGeometry(channel_geometry_middle)
                    closest_xs_feat_copy["channel_id"] = channel_id
                    closest_xs_feat_copy["id"] = next_cross_section_location_id
                    next_cross_section_location_id += 1
                    cross_section_location_copies.append(closest_xs_feat_copy)
        if cross_section_location_copies:
            self.cross_section_layer.addFeatures(cross_section_location_copies)

    def remove_hanging_cross_sections(self, visited_channel_ids):
        """Remove cross-sections not aligned with the channels."""
        xs_leftovers = []
        channel_feats, channels_spatial_index = spatial_index(self.integrate_layer)
        for xs_feat in self.cross_section_layer.getFeatures():
            xs_geom = xs_feat.geometry()
            xs_buffer = xs_geom.buffer(DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
            channel_fids = channels_spatial_index.intersects(xs_buffer.boundingBox())
            # only modify channels that were visited
            channel_fids = list(set(channel_fids).intersection(visited_channel_ids))
            if len(channel_fids) == 0:
                continue
            xs_intersects = False
            for channel_fid in channel_fids:
                channel_feat = channel_feats[channel_fid]
                if xs_buffer.intersects(channel_feat.geometry()):
                    xs_intersects = True
                    break
            if not xs_intersects:
                xs_leftovers.append(xs_feat.id())
        if xs_leftovers:
            self.cross_section_layer.deleteFeatures(xs_leftovers)

    @staticmethod
    def substring_feature(curve, start_distance, end_distance, fields, simplify=False, **attributes):
        """Extract part of the curve as a new structure feature."""
        substring_feat = QgsFeature(fields)
        substring_feat.setGeometry(get_substring_geometry(curve, start_distance, end_distance, simplify))
        for field_name, field_value in attributes.items():
            substring_feat[field_name] = field_value
        return substring_feat

    def integrate_structure_features(self, channel_feat, channel_structures):
        """Integrate structures with a channel network."""
        channel_layer_name = self.integrate_layer.name()
        channel_fields = self.layer_fields_mapping[channel_layer_name]
        channel_field_names = self.layer_field_names_mapping[channel_layer_name]
        channel_attributes = {field_name: channel_feat[field_name] for field_name in channel_field_names}
        channel_geom = channel_feat.geometry()
        first_node_id = channel_attributes['connection_node_id_start']
        first_node_feat = next(get_features_by_expression(self.node_layer, f'"id" = {first_node_id}'))
        node_field_names = self.layer_field_names_mapping[self.node_layer.name()]
        node_attributes = {field_name: first_node_feat[field_name] for field_name in node_field_names}
        channel_curve = channel_geom.constGet()
        previous_structure_end = 0
        simplify_structure_geometry = self.target_model_cls != dm.Culvert
        structure_fields = self.layer_fields_mapping[self.target_layer.name()]
        structure_field_names = self.layer_field_names_mapping[self.target_layer.name()]
        total_length = sum(channel_structure.length for channel_structure in channel_structures)
        added_features = defaultdict(list)
        if channel_geom.length() < total_length:
            id_str = ', '.join(str(channel_structure.feature.id()) for channel_structure in channel_structures)
            message = (f'Cannot integrate {self.target_model_cls.__tablename__}s with total length {total_length:.2f} '
                       f'into channel {channel_feat["id"]} with length {channel_geom.length():.2f}. '
                       f'Primary keys {self.target_model_cls.__tablename__}s: {id_str}')
            warnings.warn(f"{message}", StructuresIntegratorWarning)
            return
        next_channel_id = get_next_feature_id(self.integrate_layer)
        for i, channel_structure in enumerate(sorted(channel_structures, key=lambda x: x.m)):
            new_nodes = []
            src_structure_feat = channel_structure.feature
            structure_feat = QgsFeature(structure_fields)
            # Update with values from the widgets.
            update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_structure_feat, structure_feat)
            structure_attributes = {field_name: structure_feat[field_name] for field_name in structure_field_names}
            structure_length = channel_structure.length
            channel_structure_m = channel_structure.m
            half_length = structure_length * 0.5
            # when structures overlap, move them to the end of the previous structure
            if channel_structure_m - half_length < previous_structure_end:
                channel_structure_m = previous_structure_end + half_length
            start_distance = channel_structure_m - half_length
            end_distance = channel_structure_m + half_length
            # Setup structure feature
            substring_geom = get_substring_geometry(channel_curve, start_distance, end_distance, simplify_structure_geometry)
            substring_feat = self.target_manager.create_new(substring_geom, structure_fields, structure_attributes)
            added_features[self.node_layer.name()] += self.update_feature_endpoints(substring_feat, **node_attributes)
            added_features[self.target_layer.name()].append(substring_feat)
            # Setup channel leftover feature
            # todo: is this check necessary?
            if start_distance > previous_structure_end:
                before_substring_feat = self.substring_feature(
                    channel_curve, previous_structure_end, start_distance, channel_fields, False, **channel_attributes
                )
                added_features[self.node_layer.name()] += self.update_feature_endpoints(before_substring_feat, **node_attributes)
                if i > 0:
                    before_substring_feat["id"] = next_channel_id
                    next_channel_id += 1
                added_features[channel_layer_name].append(before_substring_feat)
            previous_structure_end = end_distance
            if new_nodes:
                update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_structure_feat, *new_nodes)
        # Setup last channel leftover feature
        last_substring_end = channel_geom.length()
        if last_substring_end - previous_structure_end > 0:
            last_substring_feat = self.substring_feature(
                channel_curve, previous_structure_end, last_substring_end, channel_fields, False, **channel_attributes
            )
            added_features[self.node_layer.name()] += self.update_feature_endpoints(last_substring_feat, **node_attributes)
            last_substring_feat["id"] = next_channel_id
            added_features[channel_layer_name].append(last_substring_feat)
        return added_features

    def integrate_features(self, input_feature_ids, selected_ids):
        """Method responsible for the importing/integrating structures from the external feature source."""
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        channels_replaced = []
        for channel_feature in self.integrate_layer.getFeatures():
            channel_structures, processed_structures_fids = self.get_channel_structures_data(
                channel_feature, selected_ids
            )
            ch_id = channel_feature["id"]
            source_channel_xs_locations = [xs["id"] for xs in get_features_by_expression(self.cross_section_layer, f'"channel_id" = {ch_id}')]
            if channel_structures:
                added_features = self.integrate_structure_features(channel_feature, channel_structures)
                self.update_channel_cross_section_references(added_features[self.integrate_layer.name()], source_channel_xs_locations)
                for key in added_features:
                    features_to_add[key] += added_features[key]
                all_processed_structure_ids |= processed_structures_fids
                channels_replaced.append(ch_id)
        self.integrate_layer.startEditing()
        for ch_id in channels_replaced:
            self.integrate_layer.deleteFeature(ch_id)
        return features_to_add, list(all_processed_structure_ids)


def get_substring_geometry(curve, start_distance, end_distance, simplify=False):
    curve_substring = curve.curveSubstring(start_distance, end_distance)
    substring_geometry = QgsGeometry(curve_substring)
    if simplify:
        substring_polyline = substring_geometry.asPolyline()
        substring_geometry = QgsGeometry.fromPolylineXY([substring_polyline[0], substring_polyline[-1]])
    return substring_geometry
