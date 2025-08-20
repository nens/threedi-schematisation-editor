import warnings
from _operator import attrgetter, itemgetter
from collections import defaultdict
from dataclasses import dataclass

from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    get_features_by_expression,
    get_next_feature_id,
    gpkg_layer,
    spatial_index,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_INTERSECTION_BUFFER_SEGMENTS,
    FeatureManager,
    get_float_value_from_feature,
    update_attributes,
)
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning


@dataclass
class LinearIntegratorStructureData:
    conduit_id: int
    feature: QgsFeature
    m: float
    length: float


class LinearIntegrator:
    """Integrate linear structures onto a conduit (channel or pipe)"""

    def __init__(
        self,
        conduit_layer,
        target_model_cls,
        target_layer,
        target_manager,
        node_layer,
        node_manager,
        fields_configurations,
        conversion_settings,
        cross_section_layer,
        external_source,
        target_gpkg,
        conduit_model_cls,
    ):
        self.external_source = external_source
        self.conduit_model_cls = conduit_model_cls
        self.target_model_cls = target_model_cls
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings
        # set schematisation layer to add - if any are missing retrieve them from the gpkg
        self.integrate_layer = (
            conduit_layer
            if conduit_layer
            else gpkg_layer(target_gpkg, self.conduit_model_cls.__tablename__)
        )
        self.target_layer = (
            target_layer
            if target_layer
            else gpkg_layer(target_gpkg, self.target_model_cls.__tablename__)
        )
        self.node_layer = (
            node_layer
            if node_layer
            else gpkg_layer(target_gpkg, dm.ConnectionNode.__tablename__)
        )
        self.cross_section_layer = (
            cross_section_layer
            if cross_section_layer
            else gpkg_layer(target_gpkg, dm.CrossSectionLocation.__tablename__)
        )
        # feature managers that handle id's for added features
        # for target features and nodes a manager can be supplied such that they match the associated importer
        self.target_manager = (
            target_manager if target_manager else FeatureManager(self.target_model_cls)
        )
        self.node_manager = (
            node_manager if node_manager else FeatureManager(dm.ConnectionNode)
        )
        self.integrate_manager = FeatureManager(
            get_next_feature_id(self.integrate_layer)
        )
        self.cross_section_manager = FeatureManager(
            get_next_feature_id(self.cross_section_layer)
        )
        # initialize mappings and indices
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    @classmethod
    def from_importer(cls, integrate_layer, cross_section_layer, importer):
        """extract data from importer to created matching integrator"""
        return cls(
            integrate_layer,
            importer.target_model_cls,
            importer.target_layer,
            importer.processor.target_manager,
            importer.node_layer,
            importer.processor.node_manager,
            importer.fields_configurations,
            importer.conversion_settings,
            cross_section_layer,
            importer.external_source,
            importer.target_gpkg,
        )

    @staticmethod
    def get_substring_geometry(curve, start_distance, end_distance, simplify=False):
        curve_substring = curve.curveSubstring(start_distance, end_distance)
        substring_geometry = QgsGeometry(curve_substring)
        if simplify:
            substring_polyline = substring_geometry.asPolyline()
            substring_geometry = QgsGeometry.fromPolylineXY(
                [substring_polyline[0], substring_polyline[-1]]
            )
        return substring_geometry

    def setup_fields_map(self):
        """Setup input layer fields map."""
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        for layer in [
            self.target_layer,
            self.node_layer,
            self.integrate_layer,
            self.cross_section_layer,
        ]:
            layer_name = layer.name()
            layer_fields = layer.fields()
            self.layer_fields_mapping[layer_name] = layer_fields
            self.layer_field_names_mapping[layer_name] = [
                field.name() for field in layer_fields.toList()
            ]

    def setup_spatial_indexes(self):
        """Setup input layer spatial indexes."""
        self.spatial_indexes_map = {}
        self.spatial_indexes_map["source"] = spatial_index(self.external_source)
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
    def get_conduit_structure_from_line(
        structure_feat, conduit_feat, snapping_distance
    ):
        conduit_geometry = conduit_feat.geometry()
        structure_geom = structure_feat.geometry()
        poly_line = structure_geom.asPolyline()
        start_geom = QgsGeometry.fromPointXY(poly_line[0])
        end_geom = QgsGeometry.fromPointXY(poly_line[-1])
        start_buffer = start_geom.buffer(
            snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
        )
        end_buffer = end_geom.buffer(
            snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
        )
        if not all(
            [
                start_buffer.intersects(conduit_geometry),
                end_buffer.intersects(conduit_geometry),
            ]
        ):
            return
        intersection_m = conduit_geometry.lineLocatePoint(structure_geom.centroid())
        structure_length = structure_geom.length()
        return LinearIntegratorStructureData(
            conduit_feat["id"], structure_feat, intersection_m, structure_length
        )

    @staticmethod
    def get_conduit_structure_from_point(
        structure_feat,
        conduit_feat,
        snapping_distance,
        length_source_field,
        length_fallback_value,
    ):
        structure_geom = structure_feat.geometry()
        conduit_geometry = conduit_feat.geometry()
        structure_buffer = structure_geom.buffer(
            snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
        )
        if not structure_buffer.intersects(conduit_geometry):
            return
        intersection_m = conduit_geometry.lineLocatePoint(structure_geom)
        structure_length = get_float_value_from_feature(
            structure_feat, length_source_field, length_fallback_value
        )
        return LinearIntegratorStructureData(
            conduit_feat["id"], structure_feat, intersection_m, structure_length
        )

    def get_conduit_structures_data(self, conduit_feat, selected_ids=None):
        """Extract and calculate channel structures data."""
        conduit_structures = []
        processed_structure_ids = set()
        if selected_ids is None:
            selected_ids = set()
        conduit_geometry = conduit_feat.geometry()
        structure_features_map, structure_index = self.spatial_indexes_map["source"]
        structure_fids = structure_index.intersects(conduit_geometry.boundingBox())
        for structure_fid in structure_fids:
            if structure_fid in processed_structure_ids:
                continue
            if selected_ids and structure_fid not in selected_ids:
                continue
            structure_feat = structure_features_map[structure_fid]
            if (
                structure_feat.geometry().type()
                == QgsWkbTypes.GeometryType.LineGeometry
            ):
                conduit_structure = LinearIntegrator.get_conduit_structure_from_line(
                    structure_feat,
                    conduit_feat,
                    self.conversion_settings.snapping_distance,
                )
            elif (
                structure_feat.geometry().type()
                == QgsWkbTypes.GeometryType.PointGeometry
            ):
                conduit_structure = LinearIntegrator.get_conduit_structure_from_point(
                    structure_feat,
                    conduit_feat,
                    self.conversion_settings.snapping_distance,
                    self.conversion_settings.length_source_field,
                    self.conversion_settings.length_fallback_value,
                )
            else:
                continue
            if conduit_structure is not None:
                conduit_structures.append(conduit_structure)
                processed_structure_ids.add(structure_fid)
        conduit_structures.sort(key=attrgetter("m"))
        return conduit_structures, processed_structure_ids

    def add_node(self, point, node_layer_fields, node_attributes):
        node_feat = self.node_manager.create_new(
            QgsGeometry.fromPointXY(point), node_layer_fields, node_attributes
        )
        self.node_by_location[point] = node_feat["id"]
        return node_feat

    def update_feature_endpoints(self, dst_feature, **template_node_attributes):
        """Update feature endpoint references."""
        new_nodes = []
        conduit_polyline = dst_feature.geometry().asPolyline()
        start_node_point, end_node_point = conduit_polyline[0], conduit_polyline[-1]
        node_layer_fields = self.layer_fields_mapping[self.node_layer.name()]
        for point in [start_node_point, end_node_point]:
            if point not in self.node_by_location:
                node_feat = self.add_node(
                    point, node_layer_fields, template_node_attributes
                )
                new_nodes.append(node_feat)
        dst_feature["connection_node_id_start"] = self.node_by_location[
            start_node_point
        ]
        dst_feature["connection_node_id_end"] = self.node_by_location[end_node_point]
        return new_nodes

    @staticmethod
    def substring_feature(
        curve, start_distance, end_distance, fields, simplify=False, **attributes
    ):
        """Extract part of the curve as a new structure feature."""
        substring_feat = QgsFeature(fields)
        substring_feat.setGeometry(
            LinearIntegrator.get_substring_geometry(
                curve, start_distance, end_distance, simplify
            )
        )
        for field_name, field_value in attributes.items():
            substring_feat[field_name] = field_value
        return substring_feat

    @staticmethod
    def fix_structure_placement(
        conduit_structures, conduit_geom, minimum_conduit_length
    ):
        # fix any gaps on the left side of the structures
        conduit_structures = LinearIntegrator.fix_structure_placement_lhs(
            conduit_structures, conduit_geom.length(), minimum_conduit_length
        )
        conduit_structures = LinearIntegrator.fix_structure_placement_rhs(
            conduit_structures, conduit_geom.length(), minimum_conduit_length
        )
        conduit_structures = LinearIntegrator.fix_structure_placement_overlap_at_end(
            conduit_structures, conduit_geom.length()
        )
        return conduit_structures

    def place_structures_on_conduit(
        self, conduit_structures, conduit_feat, simplify_structure_geometry
    ):
        conduit_geom = conduit_feat.geometry()
        added_features = []
        for i, cs in enumerate(conduit_structures):
            substring_geom = LinearIntegrator.get_substring_geometry(
                conduit_geom.constGet(),
                cs.m - cs.length * 0.5,
                cs.m + cs.length * 0.5,
                simplify_structure_geometry,
            )
            substring_feat = self.target_manager.create_new(
                substring_geom, self.layer_fields_mapping[self.target_layer.name()]
            )
            update_attributes(
                self.fields_configurations[self.target_model_cls],
                self.target_model_cls,
                cs.feature,
                substring_feat,
            )
            added_features.append(substring_feat)
        return added_features

    @staticmethod
    def fix_structure_placement_lhs(
        conduit_structures, conduit_length, minimum_conduit_length
    ):
        conduit_structures = sorted(conduit_structures, key=lambda x: x.m)
        for i, cs in enumerate(conduit_structures):
            prev_end = (
                0
                if i == 0
                else conduit_structures[i - 1].m
                + 0.5 * conduit_structures[i - 1].length
            )
            end_left = cs.m - 0.5 * cs.length
            # move structure if distance is too small
            # except when the structure extends over the end of the conduit
            if (
                end_left - prev_end
            ) < minimum_conduit_length and prev_end + cs.length <= conduit_length:
                cs.m = prev_end + 0.5 * cs.length
        return conduit_structures

    @staticmethod
    def fix_structure_placement_rhs(
        conduit_structures, conduit_length, minimum_conduit_length
    ):
        conduit_structures = sorted(conduit_structures, key=lambda x: x.m)
        last_struct = conduit_structures[-1]
        end_right = last_struct.m + 0.5 * last_struct.length
        if conduit_length - end_right < minimum_conduit_length:
            prev_right = (
                conduit_structures[-2].m + 0.5 * conduit_structures[-2].length
                if len(conduit_structures) > 1
                else 0
            )
            # move if the remaining space is sufficient
            if (
                conduit_length - last_struct.length
            ) - prev_right >= minimum_conduit_length:
                last_struct.m = conduit_length - 0.5 * last_struct.length
            # resize if remaining space does not allow move
            elif (conduit_length - prev_right) > 0:
                last_struct.length = conduit_length - prev_right
                last_struct.m = prev_right + 0.5 * last_struct.length
        return conduit_structures

    @staticmethod
    def fix_structure_placement_overlap_at_end(conduit_structures, conduit_length):
        # handle edge case where multiple structures end at the conduit end
        idx_at_right_end = [
            i
            for i, cs in enumerate(conduit_structures)
            if (cs.m + 0.5 * cs.length) == conduit_length
        ]
        if len(idx_at_right_end) > 1:
            for i in idx_at_right_end[:-1]:
                cs_i = conduit_structures[i]
                cs_next = conduit_structures[i + 1]
                if cs_i.m == cs_next.m and cs_i.length == cs_next.length:
                    continue
                left_i = cs_i.m - 0.5 * cs_i.length
                new_right = cs_next.m - 0.5 * cs_next.length
                cs_i.length = new_right - left_i
                cs_i.m = new_right - 0.5 * cs_i.length
        return conduit_structures

    @staticmethod
    def get_conduit_cuts(conduit_structures, conduit_length):
        # left hand side of structure
        lefts = [cs.m - 0.5 * cs.length for cs in conduit_structures] + [conduit_length]
        # right hand side of previous structure
        rights = [0] + [cs.m + 0.5 * cs.length for cs in conduit_structures]
        gaps = [left - right for left, right in zip(lefts, rights)]
        # return conduit ends for gaps > 0
        return [(rights[i], lefts[i]) for (i, l) in enumerate(gaps) if l > 0]

    def cut_conduit(self, conduit_feat, conduit_structures):
        added_conduits = []
        conduit_geom = conduit_feat.geometry()
        conduit_fields = self.layer_fields_mapping[self.integrate_layer.name()]
        conduit_attributes = {
            field_name: conduit_feat[field_name]
            for field_name in self.layer_field_names_mapping[
                self.integrate_layer.name()
            ]
        }
        conduit_cuts = LinearIntegrator.get_conduit_cuts(
            conduit_structures, conduit_geom.length()
        )
        if len(conduit_cuts) > 0:
            self.integrate_layer.deleteFeature(conduit_feat.id())
        for i, (left, right) in enumerate(conduit_cuts):
            substring_feat = LinearIntegrator.substring_feature(
                conduit_geom.constGet(),
                left,
                right,
                conduit_fields,
                False,
                **conduit_attributes,
            )
            self.integrate_manager.add_feature(substring_feat, set_id=(i > 0))
            added_conduits.append(substring_feat)
        return added_conduits

    def integrate_structure_features(self, conduit_feat, conduit_structures):
        """Integrate structures with a channel network."""
        added_features = defaultdict(list)
        conduit_geom = conduit_feat.geometry()
        total_length = sum(
            conduit_structure.length for conduit_structure in conduit_structures
        )
        if conduit_geom.length() < total_length:
            id_str = ", ".join(
                str(conduit_structure.feature.id())
                for conduit_structure in conduit_structures
            )
            message = (
                f"Cannot integrate {self.target_model_cls.__tablename__}s with total length {total_length:.2f} "
                f"into {self.conduit_model_cls.__tablename__} {conduit_feat['id']} with length {conduit_geom.length():.2f}. "
                f"Primary keys {self.target_model_cls.__tablename__}s: {id_str}"
            )
            warnings.warn(f"{message}", StructuresIntegratorWarning)
            return added_features

        simplify_structure_geometry = self.target_model_cls != dm.Culvert

        # Collect structures correctly placed along the conduit
        conduit_structures = LinearIntegrator.fix_structure_placement(
            conduit_structures,
            conduit_geom,
            self.conversion_settings.minimum_channel_length,
        )
        added_features[self.target_layer.name()] = self.place_structures_on_conduit(
            conduit_structures, conduit_feat, simplify_structure_geometry
        )

        # Remove parts of the conduit that overlap with new structures
        added_features[self.integrate_layer.name()] = self.cut_conduit(
            conduit_feat, conduit_structures
        )

        # update connection nodes for modified featurees
        # Get attributes of the first node to use for newly added nodes
        first_node_feat = next(
            get_features_by_expression(
                self.node_layer,
                f'"id" = {conduit_feat["connection_node_id_start"]}',
            )
        )
        node_attributes = {
            field_name: first_node_feat[field_name]
            for field_name in self.layer_field_names_mapping[self.node_layer.name()]
        }
        for substring_feat in (
            added_features[self.target_layer.name()]
            + added_features[self.integrate_layer.name()]
        ):
            added_features[self.node_layer.name()] += self.update_feature_endpoints(
                substring_feat, **node_attributes
            )

        return added_features

    def integrate_features(self, input_feature_ids):
        """Method responsible for the importing/integrating structures from the external feature source."""
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        for conduit_feature in self.integrate_layer.getFeatures():
            conduit_structures, processed_structures_fids = (
                self.get_conduit_structures_data(conduit_feature, input_feature_ids)
            )
            if not conduit_structures:
                continue
            added_features = self.integrate_structure_features(
                conduit_feature, conduit_structures
            )
            added_features[self.cross_section_layer.name()] = (
                self.update_channel_cross_section_references(
                    added_features[self.integrate_layer.name()], conduit_feature["id"]
                )
            )
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= processed_structures_fids
        visited_channel_ids = [
            channel["id"] for channel in features_to_add[self.integrate_layer.name()]
        ]
        self.cross_section_layer.deleteFeatures(
            self.get_hanging_cross_sections(visited_channel_ids)
        )
        return features_to_add, list(all_processed_structure_ids)


class PipeIntegrator(LinearIntegrator):
    def __init__(self, *args):
        super().__init__(*args, conduit_model_cls=dm.Pipe)

    def integrate_features(self, input_feature_ids):
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        for conduit_feature in self.integrate_layer.getFeatures():
            conduit_structures, processed_structures_fids = (
                self.get_conduit_structures_data(conduit_feature, input_feature_ids)
            )
            if not conduit_structures:
                continue
            added_features = self.integrate_structure_features(
                conduit_feature, conduit_structures
            )
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= processed_structures_fids
        return features_to_add, list(all_processed_structure_ids)


class ChannelIntegrator(LinearIntegrator):
    def __init__(self, *args):
        super().__init__(*args, conduit_model_cls=dm.Channel)

    def integrate_features(self, input_feature_ids):
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        for conduit_feature in self.integrate_layer.getFeatures():
            conduit_structures, processed_structures_fids = (
                self.get_conduit_structures_data(conduit_feature, input_feature_ids)
            )
            if not conduit_structures:
                continue
            added_features = self.integrate_structure_features(
                conduit_feature, conduit_structures
            )
            added_features[self.cross_section_layer.name()] = (
                self.update_channel_cross_section_references(
                    added_features[self.integrate_layer.name()], conduit_feature["id"]
                )
            )
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= processed_structures_fids
        visited_channel_ids = [
            channel["id"] for channel in features_to_add[self.integrate_layer.name()]
        ]
        self.cross_section_layer.deleteFeatures(
            self.get_hanging_cross_sections(visited_channel_ids)
        )
        return features_to_add, list(all_processed_structure_ids)

    @staticmethod
    def get_cross_sections_for_channel(
        channel_feat, cross_section_fids, cross_section_location_features_map
    ):
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
    def get_closest_cross_section_location(
        channel_feat, cross_section_layer, source_channel_cross_section_locations
    ):
        channel_geometry = channel_feat.geometry()
        src_channel_cross_section_ids = [
            str(id) for id in source_channel_cross_section_locations
        ]
        if src_channel_cross_section_ids:
            id_str = ",".join(src_channel_cross_section_ids)
            distance_map = [
                (
                    cross_section_feat,
                    channel_geometry.distance(cross_section_feat.geometry()),
                )
                for cross_section_feat in get_features_by_expression(
                    cross_section_layer, f'"id" in ({id_str})', with_geometry=True
                )
            ]
            distance_map.sort(key=itemgetter(1))
            closest_cross_section_copy = QgsFeature(distance_map[0][0])
            return closest_cross_section_copy

    def update_channel_cross_section_references(
        self, new_channels, original_channel_id
    ):
        """Update channel cross-section references."""
        source_channel_cross_section_locations = [
            xs["id"]
            for xs in get_features_by_expression(
                self.cross_section_layer, f'"channel_id" = {original_channel_id}'
            )
        ]
        cross_section_location_features_map, cross_section_location_index = (
            self.spatial_indexes_map[self.cross_section_layer.name()]
        )
        channel_id_idx = self.layer_fields_mapping[
            self.cross_section_layer.name()
        ].lookupField("channel_id")
        cross_section_location_copies = []
        for channel_feat in new_channels:
            channel_geom = channel_feat.geometry()
            cross_section_fids = cross_section_location_index.intersects(
                channel_geom.boundingBox()
            )
            # Find any nearby cross sections and associate those to this channel
            cross_sections_for_channel = (
                ChannelIntegrator.get_cross_sections_for_channel(
                    channel_feat,
                    cross_section_fids,
                    cross_section_location_features_map,
                )
            )
            for cross_section_fid in cross_sections_for_channel:
                self.cross_section_layer.changeAttributeValue(
                    cross_section_fid, channel_id_idx, channel_feat["id"]
                )
            # If no nearby cross sections were found, find the closest cross section create a copy of that one
            if len(cross_sections_for_channel) == 0:
                closest_cross_section_copy = self.get_closest_cross_section_location(
                    channel_feat,
                    self.cross_section_layer,
                    source_channel_cross_section_locations,
                )
                if closest_cross_section_copy:
                    self.cross_section_manager.add_feature(
                        closest_cross_section_copy,
                        geom=channel_geom.interpolate(channel_geom.length() * 0.5),
                    )
                    closest_cross_section_copy["channel_id"] = channel_feat["id"]
                    cross_section_location_copies.append(closest_cross_section_copy)
        return cross_section_location_copies

    @staticmethod
    def is_hanging_cross_section(cross_section_feat, channel_feats, channel_fids):
        """Get cross-sections that are not aligned with any channel."""
        xs_buffer = cross_section_feat.geometry().buffer(
            DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
        )
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
            buffer = cross_section_feat.geometry().buffer(
                DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
            )
            channel_fids = channels_spatial_index.intersects(buffer.boundingBox())
            # only consider channels that were visited
            channel_fids = list(set(channel_fids).intersection(visited_channel_ids))
            if len(channel_fids) == 0:
                continue
            is_hanging = ChannelIntegrator.is_hanging_cross_section(
                cross_section_feat, channel_feats, channel_fids
            )
            if is_hanging:
                hanging_cross_section_ids.append(cross_section_feat.id())
        return hanging_cross_section_ids
