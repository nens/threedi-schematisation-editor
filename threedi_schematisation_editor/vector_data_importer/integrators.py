import warnings
from _operator import attrgetter, itemgetter
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Type

from qgis.core import NULL, QgsFeature, QgsGeometry, QgsWkbTypes

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    get_feature_by_id,
    get_features_by_expression,
    get_next_feature_id,
    gpkg_layer,
    spatial_index,
)
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    IntegrationMode,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_INTERSECTION_BUFFER_SEGMENTS,
    CancellationToken,
    FeatureManager,
    get_field_config_value,
    get_src_geometry,
    get_substring_geometry,
    update_attributes,
)
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning


@dataclass
class LinearIntegratorStructureData:
    conduit_id: int
    feature: QgsFeature
    m: float
    length: float


class StructurePlacementStrategy:
    """Base class for structure-type-specific placement behaviour."""

    def get_structure_data(self, structure_feat, conduit_feat) -> LinearIntegratorStructureData:
        """Compute position (m) and length for structure on conduit."""
        raise NotImplementedError

    def place_structure(
        self, conduit_geom, structure_data, target_fields, target_manager, fields_configurations, target_model_cls
    ) -> QgsFeature:
        """Create structure feature with correct geometry."""
        raise NotImplementedError

    def update_structure_nodes(
        self, feature, node_by_location, node_layer_fields, node_attributes, node_manager
    ) -> list:
        """Assign connection node(s) and create new nodes if needed."""
        raise NotImplementedError


class LineStructurePlacement(StructurePlacementStrategy):
    """Strategy for line-target structures (Weir, Orifice, Culvert)."""

    def __init__(self, length_config, simplify_geometry):
        self.length_config = length_config
        self.simplify_geometry = simplify_geometry

    def get_structure_data(self, structure_feat, conduit_feat) -> LinearIntegratorStructureData:
        conduit_geometry = conduit_feat.geometry()
        structure_geom = structure_feat.geometry()
        if structure_geom.type() == QgsWkbTypes.GeometryType.LineGeometry:
            intersection_m = conduit_geometry.lineLocatePoint(structure_geom.centroid())
            structure_length = structure_geom.length()
        else:
            intersection_m = conduit_geometry.lineLocatePoint(structure_geom)
            structure_length = get_field_config_value(self.length_config, structure_feat)
        return LinearIntegratorStructureData(
            conduit_feat["id"], structure_feat, intersection_m, structure_length
        )

    def place_structure(
        self, conduit_geom, structure_data, target_fields, target_manager, fields_configurations, target_model_cls
    ) -> QgsFeature:
        cs = structure_data
        substring_geom = get_substring_geometry(
            conduit_geom.constGet(),
            cs.m - cs.length * 0.5,
            cs.m + cs.length * 0.5,
            self.simplify_geometry,
        )
        substring_feat = target_manager.create_new(substring_geom, target_fields)
        update_attributes(fields_configurations, target_model_cls, cs.feature, substring_feat)
        return substring_feat

    def update_structure_nodes(
        self, feature, node_by_location, node_layer_fields, node_attributes, node_manager
    ) -> list:
        new_nodes = []
        conduit_polyline = feature.geometry().asPolyline()
        start_node_point, end_node_point = conduit_polyline[0], conduit_polyline[-1]
        for point in [start_node_point, end_node_point]:
            if point not in node_by_location:
                node_feat = node_manager.create_new(
                    QgsGeometry.fromPointXY(point), node_layer_fields, node_attributes
                )
                node_by_location[point] = node_feat["id"]
                new_nodes.append(node_feat)
        feature["connection_node_id_start"] = node_by_location[start_node_point]
        feature["connection_node_id_end"] = node_by_location[end_node_point]
        return new_nodes


class LinearIntegrator:
    """Integrate linear structures onto a conduit (channel or pipe)"""

    _cancellation_token = CancellationToken()

    def __init__(
        self,
        conduit_layer,
        target_model_cls,
        target_layer,
        target_manager,
        node_layer,
        node_manager,
        import_settings,
        external_source,
        target_gpkg,
        conduit_model_cls,
        strategy,
    ):
        self.external_source = external_source
        self.conduit_model_cls = conduit_model_cls
        self.strategy = strategy
        self.target_model_cls = target_model_cls
        self.fields_configurations = import_settings.fields
        self.point_to_line_settings = import_settings.point_to_line_conversion
        self.snapping_distance = import_settings.integration.snap_distance
        self.minimum_conduit_length = import_settings.integration.min_length
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
        # initialize mappings and indices
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    @staticmethod
    def get_integrator(
        integrate_layer, cross_section_layer, importer
    ) -> Optional["LinearIntegrator"]:
        integration_mode = importer.import_settings.integration.integration_mode
        if integration_mode == IntegrationMode.CHANNELS:
            return ChannelIntegrator.from_importer(
                integrate_layer, cross_section_layer, importer
            )
        elif (
            integration_mode == IntegrationMode.PIPES
            and importer.target_model_cls
            in [
                dm.Weir,
                dm.Orifice,
            ]
        ):
            return PipeIntegrator.from_importer(integrate_layer, importer)

    @property
    def map_layers(self):
        return [self.target_layer, self.node_layer, self.integrate_layer]

    @property
    def spatial_layers(self):
        return [self.node_layer]

    @property
    def modifiable_layers(self):
        return [self.integrate_layer]

    def setup_fields_map(self):
        """Setup input layer fields map."""
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        for layer in self.map_layers:
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
        for layer in self.spatial_layers:
            layer_name = layer.name()
            self.spatial_indexes_map[layer_name] = spatial_index(layer)

    def set_transformed_spatial_index(self, transform):
        # update spatial index for source when source has a transformation
        # this is not done at initialization because the transform is aware of the context
        self.spatial_indexes_map["source"] = spatial_index(
            self.external_source, transform=transform
        )

    def setup_node_by_location(self):
        """Setup nodes by location."""
        self.node_by_location = {}
        for node_feat in self.node_layer.getFeatures():
            node_geom = node_feat.geometry()
            node_point = node_geom.asPoint()
            self.node_by_location[node_point] = node_feat["id"]

    def get_conduit_matches(self, selected_ids=None) -> list:
        """Return matched (conduit, [structures]) pairs for integration.

        Structures that snap to more than one conduit are excluded and reported
        via a single StructuresIntegratorWarning.
        """
        if selected_ids is None:
            selected_ids = set()
        structure_features_map, structure_index = self.spatial_indexes_map["source"]
        # structure_fid -> set of conduit fids it snaps to
        structure_conduit_map = defaultdict(set)
        # conduit fid -> (conduit_feat, list of matching structure_feats)
        conduit_matches = {}
        for conduit_feat in self.integrate_layer.getFeatures():
            conduit_geom = conduit_feat.geometry()
            bbox = conduit_geom.boundingBox()
            bbox.grow(self.snapping_distance)
            structure_fids = structure_index.intersects(bbox)
            for structure_fid in structure_fids:
                if selected_ids and structure_fid not in selected_ids:
                    continue
                structure_feat = structure_features_map[structure_fid]
                geom_type = structure_feat.geometry().type()
                if geom_type == QgsWkbTypes.GeometryType.LineGeometry:
                    poly_line = structure_feat.geometry().asPolyline()
                    start_buf = QgsGeometry.fromPointXY(poly_line[0]).buffer(
                        self.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                    )
                    end_buf = QgsGeometry.fromPointXY(poly_line[-1]).buffer(
                        self.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                    )
                    snaps = start_buf.intersects(conduit_geom) and end_buf.intersects(
                        conduit_geom
                    )
                elif geom_type == QgsWkbTypes.GeometryType.PointGeometry:
                    buf = structure_feat.geometry().buffer(
                        self.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                    )
                    snaps = buf.intersects(conduit_geom)
                else:
                    continue
                if snaps:
                    structure_conduit_map[structure_fid].add(conduit_feat["id"])
                    if conduit_feat["id"] not in conduit_matches:
                        conduit_matches[conduit_feat["id"]] = (conduit_feat, [])
                    conduit_matches[conduit_feat["id"]][1].append(structure_feat)
        multi = {
            fid
            for fid, conduit_fids in structure_conduit_map.items()
            if len(conduit_fids) > 1
        }
        if multi:
            lines = [
                f"  - structure fid {fid} matches conduits "
                f"{sorted(structure_conduit_map[fid])}"
                for fid in multi
            ]
            warnings.warn(
                f"Skipped {len(multi)} structure(s) within snapping distance of "
                f"multiple conduits:\n" + "\n".join(lines),
                StructuresIntegratorWarning,
            )
        return [
            (conduit_feat, [s for s in structures if s.id() not in multi])
            for conduit_feat, structures in conduit_matches.values()
            if any(s.id() not in multi for s in structures)
        ]

    def add_node(self, point, node_layer_fields, node_attributes):
        node_feat = self.node_manager.create_new(
            QgsGeometry.fromPointXY(point), node_layer_fields, node_attributes
        )
        self.node_by_location[point] = node_feat["id"]
        return node_feat

    @staticmethod
    def substring_feature(
        curve, start_distance, end_distance, fields, simplify=False, **attributes
    ):
        """Extract part of the curve as a new structure feature."""
        substring_feat = QgsFeature(fields)
        substring_feat.setGeometry(
            get_substring_geometry(
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

    def integrate_structure_features(
        self, conduit_feat, conduit_geom, conduit_structures
    ):
        """Integrate structures with a channel network."""
        added_features = defaultdict(list)
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

        # Collect structures correctly placed along the conduit
        conduit_structures = LinearIntegrator.fix_structure_placement(
            conduit_structures,
            conduit_geom,
            self.minimum_conduit_length,
        )

        target_fields = self.layer_fields_mapping[self.target_layer.name()]
        for cs in conduit_structures:
            added_features[self.target_layer.name()].append(
                self.strategy.place_structure(
                    conduit_geom,
                    cs,
                    target_fields,
                    self.target_manager,
                    self.fields_configurations,
                    self.target_model_cls,
                )
            )

        # Remove parts of the conduit that overlap with new structures
        added_features[self.integrate_layer.name()] = self.cut_conduit(
            conduit_feat, conduit_structures
        )

        # update connection nodes for modified features
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

        for substring_feat in added_features[self.target_layer.name()]:
            added_features[self.node_layer.name()] += self.update_feature_endpoints(
                substring_feat, node_attributes, respect_mapped_node_ids=True
            )

        # Conduit segments always need endpoint updates (they don't have attribute mapping)
        node_layer_fields = self.layer_fields_mapping[self.node_layer.name()]
        for substring_feat in added_features[self.integrate_layer.name()]:
            added_features[self.node_layer.name()] += self.strategy.update_structure_nodes(
                substring_feat,
                self.node_by_location,
                node_layer_fields,
                node_attributes,
                self.node_manager,
            )

        return added_features

    def update_feature_endpoints(
        self, feat, template_node_attributes, respect_mapped_node_ids=False
    ):
        """Snap geometry endpoints to attribute-mapped nodes, create nodes for non-mapped endpoints."""
        new_nodes = []
        polyline = feat.geometry().asPolyline()
        node_layer_fields = self.layer_fields_mapping[self.node_layer.name()]

        for idx, field_name in [
            (0, "connection_node_id_start"),
            (-1, "connection_node_id_end"),
        ]:
            node_id = feat[field_name]
            if node_id is not None and node_id is not NULL and respect_mapped_node_ids:
                node_feat = get_feature_by_id(self.node_layer, node_id)
                if node_feat is not None:
                    polyline[idx] = node_feat.geometry().asPoint()
                    feat.setGeometry(QgsGeometry.fromPolylineXY(polyline))
            else:
                # Non-mapped: create/find node at geometry endpoint (existing behavior)
                point = polyline[idx]
                if point not in self.node_by_location:
                    node_feat = self.add_node(
                        point, node_layer_fields, template_node_attributes
                    )
                    new_nodes.append(node_feat)
                feat[field_name] = self.node_by_location[point]

        return new_nodes


class PipeIntegrator(LinearIntegrator):
    def __init__(self, *args):
        super().__init__(*args, conduit_model_cls=dm.Pipe)

    @classmethod
    def from_importer(cls, integrate_layer, importer):
        """extract data from importer to created matching integrator"""
        strategy = LineStructurePlacement(
            importer.import_settings.point_to_line_conversion.length,
            importer.target_model_cls != dm.Culvert,
        )
        return cls(
            integrate_layer,
            importer.target_model_cls,
            importer.target_layer,
            importer.processor.target_manager,
            importer.node_layer,
            importer.processor.node_manager,
            importer.import_settings,
            importer.external_source,
            importer.target_gpkg,
            strategy,
        )

    def integrate_features(self, input_feature_ids, progress_callback: callable = None):
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        for conduit_feature, structure_feats in self.get_conduit_matches(
            input_feature_ids
        ):
            if self._cancellation_token.is_cancelled:
                self._cancellation_token.interrupt()
                break
            if progress_callback:
                progress_callback(add=1)
            conduit_geom = get_src_geometry(conduit_feature)
            if conduit_geom is None:
                continue
            conduit_structures = sorted(
                (self.strategy.get_structure_data(s, conduit_feature) for s in structure_feats),
                key=attrgetter("m"),
            )
            if not conduit_structures:
                continue
            added_features = self.integrate_structure_features(
                conduit_feature, conduit_geom, conduit_structures
            )
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= {s.id() for s in structure_feats}
        return features_to_add, list(all_processed_structure_ids)


class ChannelIntegrator(LinearIntegrator):
    def __init__(
        self,
        conduit_layer,
        target_model_cls,
        target_layer,
        target_manager,
        node_layer,
        node_manager,
        import_settings,
        external_source,
        target_gpkg,
        cross_section_layer,
        strategy,
    ):
        self.cross_section_layer = cross_section_layer or gpkg_layer(
            target_gpkg, dm.CrossSectionLocation.__tablename__
        )
        self.cross_section_manager = FeatureManager(
            get_next_feature_id(self.cross_section_layer)
        )
        super().__init__(
            conduit_layer,
            target_model_cls,
            target_layer,
            target_manager,
            node_layer,
            node_manager,
            import_settings,
            external_source,
            target_gpkg,
            conduit_model_cls=dm.Channel,
            strategy=strategy,
        )

    @classmethod
    def from_importer(cls, integrate_layer, cross_section_layer, importer):
        """extract data from importer to created matching integrator"""
        strategy = LineStructurePlacement(
            importer.import_settings.point_to_line_conversion.length,
            importer.target_model_cls != dm.Culvert,
        )
        return cls(
            integrate_layer,
            importer.target_model_cls,
            importer.target_layer,
            importer.processor.target_manager,
            importer.node_layer,
            importer.processor.node_manager,
            importer.import_settings,
            importer.external_source,
            importer.target_gpkg,
            cross_section_layer,
            strategy,
        )

    @property
    def modifiable_layers(self):
        return super().modifiable_layers + [self.cross_section_layer]

    @property
    def map_layers(self):
        return super().map_layers + [self.cross_section_layer]

    @property
    def spatial_layers(self):
        return super().spatial_layers + [self.cross_section_layer]

    def integrate_features(self, input_feature_ids, progress_callback: callable = None):
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        for conduit_feature, structure_feats in self.get_conduit_matches(
            input_feature_ids
        ):
            if self._cancellation_token.is_cancelled:
                self._cancellation_token.interrupt()
                break
            if progress_callback:
                progress_callback(add=1)
            conduit_geom = get_src_geometry(conduit_feature)
            if conduit_geom is None:
                continue
            conduit_structures = sorted(
                (self.strategy.get_structure_data(s, conduit_feature) for s in structure_feats),
                key=attrgetter("m"),
            )
            if not conduit_structures:
                continue
            added_features = self.integrate_structure_features(
                conduit_feature, conduit_geom, conduit_structures
            )
            added_features[self.cross_section_layer.name()] = (
                self.update_channel_cross_section_references(
                    added_features[self.integrate_layer.name()], conduit_feature["id"]
                )
            )
            for key in added_features:
                features_to_add[key] += added_features[key]
            all_processed_structure_ids |= {s.id() for s in structure_feats}
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
