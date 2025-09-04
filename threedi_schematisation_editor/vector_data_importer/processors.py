from abc import ABC
from collections import defaultdict
from functools import cached_property
from typing import Optional

from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsSpatialIndex,
    QgsWkbTypes,
)
from threedi_schema.domain.constants import CrossSectionShape

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    find_connection_node,
    get_next_feature_id,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureManager,
    get_field_config_value,
    get_float_value_from_feature,
    update_attributes,
)


class Processor(ABC):
    def __init__(self, target_layer, target_model_cls):
        self.target_fields = target_layer.fields() if target_layer else []
        self.target_name = target_layer.name() if target_layer else None
        self.target_manager = (
            FeatureManager(get_next_feature_id(target_layer)) if target_layer else None
        )
        self.target_model_cls = target_model_cls
        self.transformation = None
        self.node_locator = None

    @classmethod
    def snap_connection_node(
        cls, feat, point, snapping_distance, locator, connection_id_name
    ):
        node = find_connection_node(point, locator, snapping_distance)
        if node:
            feat.setGeometry(QgsGeometry.fromPointXY(node.geometry().asPoint()))
            feat[connection_id_name] = node["id"]
            return True
        else:
            return False

    @classmethod
    def create_new_point_geometry(cls, src_feat):
        """Create a new point feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_point = src_geometry.asPoint()
        dst_point = src_point
        dst_geometry = QgsGeometry.fromPointXY(dst_point)
        return dst_geometry

    def process_feature(self, src_feat):
        raise NotImplementedError

    def process_features(self, external_features):
        new_features = defaultdict(list)
        for external_src_feat in external_features:
            for name, features in self.process_feature(external_src_feat).items():
                new_features[name] += features
        return new_features


class CrossSectionDataProcessor:
    # TODO: consider relation with Processor - split in attribute and layer processer?
    target_models: list[type] = [
        dm.Pipe,
        dm.Culvert,
        dm.Orifice,
        dm.Weir,
        dm.CrossSectionLocation,
    ]

    def __init__(self, conversion_settings, target_fields_config, target_layers):
        self.target_fields_config = target_fields_config
        self.conversion_settings = conversion_settings
        self.target_layer_map = {
            target_layer.name(): target_layer for target_layer in target_layers
        }

    @property
    def object_type_map(self) -> dict[str, type]:
        return {
            **{
                CrossSectionDataProcessor.get_unified_object_type_str(
                    model_cls.__tablename__
                ): model_cls
                for model_cls in self.target_models
            },
            **{
                CrossSectionDataProcessor.get_unified_object_type_str(
                    model_cls.__layername__
                ): model_cls
                for model_cls in self.target_models
            },
        }

    @staticmethod
    def get_unified_object_type_str(object_type_str: str) -> str:
        return (
            object_type_str.lower().replace("-", "").replace("_", "").replace(" ", "")
        )

    @staticmethod
    def get_cross_section_table(
        feature_group: list[QgsFeature],
        cross_section_shape: CrossSectionShape,
        order_by: str,
        field_config,
    ) -> Optional[str]:
        # Build cross section table for a group of features
        if not cross_section_shape.is_tabulated:
            return None
        # Sort the feature group based on the 'order_by' field
        feature_group.sort(key=lambda feat: feat[order_by])
        table = []
        if cross_section_shape in [
            CrossSectionShape.TABULATED_RECTANGLE,
            CrossSectionShape.TABULATED_TRAPEZIUM,
        ]:
            # CSV-style table of height, width pairs
            heights = [
                get_field_config_value(field_config["cross_section_height"], feat)
                for feat in feature_group
            ]
            widths = [
                get_field_config_value(field_config["cross_section_width"], feat)
                for feat in feature_group
            ]
            table = list(zip(heights, widths))
        elif cross_section_shape == CrossSectionShape.TABULATED_YZ:
            # CSV-style table of y, z pairs
            y = [
                get_field_config_value(field_config["cross_section_y"], feat)
                for feat in feature_group
            ]
            z = [
                get_field_config_value(field_config["cross_section_z"], feat)
                for feat in feature_group
            ]
            table = list(zip(y, z))
        return "\n".join(f"{pair[0]},{pair[1]}" for pair in table)

    @staticmethod
    def group_features(
        external_features: list[QgsFeature], group_by: str, target_fields_config
    ) -> list[list[QgsFeature]]:
        # Group features based on group by value.
        grouped_features = []
        grouped_ids = []
        for feature in external_features:
            if feature.id() in grouped_ids:
                continue
            group_by_val = feature[group_by]
            if not group_by_val:
                grouped_features.append([feature])
                continue
            try:
                cross_section_shape = CrossSectionShape(
                    get_field_config_value(
                        target_fields_config["cross_section_shape"], feature
                    )
                )
            except ValueError:
                # rows without valid cross section shapes cannot be grouped
                grouped_features.append([feature])
                continue
            if not cross_section_shape.is_tabulated:
                # rows that doe not represent a tabulated shape cannot be grouped
                grouped_features.append([feature])
            else:
                group = [
                    feat for feat in external_features if feat[group_by] == group_by_val
                ]
                grouped_ids += [feat.id() for feat in group]
                grouped_features.append(group)
        return grouped_features

    @staticmethod
    def get_feat_from_group(
        group: list[QgsFeature], order_by: str, target_fields_config
    ) -> Optional[QgsFeature]:
        # Combine group of feature in a single feature that is used for processing
        if len(group) == 0:
            return
        if len(group) == 1:
            return group[0]
        feature = group[0]
        cross_section_shape = CrossSectionShape(
            get_field_config_value(target_fields_config["cross_section_shape"], feature)
        )
        # copy first feature and ensure cross_section_table field exists
        new_feat = QgsFeature()
        new_fields = QgsFields(feature.fields())
        if "cross_section_table" not in feature.fields().names():
            new_fields.append(QgsField("cross_section_table", QVariant.String))
        new_feat.setFields(new_fields)
        # Copy all existing attributes from the original feature
        for field_name in feature.fields().names():
            new_feat[field_name] = feature[field_name]
        new_feat["cross_section_table"] = (
            CrossSectionDataProcessor.get_cross_section_table(
                group, cross_section_shape, order_by, target_fields_config
            )
        )
        return new_feat

    @staticmethod
    def find_target_object(
        src_feat, target_layer, target_object_id_field, target_object_code_field
    ) -> Optional[QgsFeature]:
        target_feat = None
        if target_object_id_field:
            target_id = src_feat[target_object_id_field]
            if target_id:
                target_feat = next(
                    (
                        feature
                        for feature in target_layer.getFeatures()
                        if feature["id"] == target_id
                    ),
                    None,
                )
        if not target_feat and target_object_code_field:
            target_code = src_feat[target_object_code_field]
            if target_code:
                # TODO: consider multiple matches??
                target_feat = next(
                    (
                        feature
                        for feature in target_layer.getFeatures()
                        if feature["code"] == target_code
                    ),
                    None,
                )
        return target_feat

    def get_target_model_cls(self, src_feat):
        src_object_type = src_feat[self.conversion_settings.target_object_type_field]
        if src_object_type:
            return self.object_type_map.get(
                CrossSectionDataProcessor.get_unified_object_type_str(src_object_type),
                None,
            )

    def get_target_layer(self, target_model_cls):
        return self.target_layer_map.get(target_model_cls.__layername__, None)

    def process_feature(self, src_feat):
        target_model_cls = self.get_target_model_cls(src_feat)
        if not target_model_cls:
            return
        target_layer = self.get_target_layer(target_model_cls)
        if not target_layer:
            return
        target_feat = self.find_target_object(
            src_feat,
            target_layer,
            self.conversion_settings.target_object_id_field,
            self.conversion_settings.target_object_code_field,
        )
        if not target_feat:
            return
        update_attributes(
            self.target_fields_config,
            target_model_cls,
            src_feat,
            target_feat,
        )
        if "cross_section_table" in src_feat.fields().names():
            target_feat["cross_section_table"] = src_feat["cross_section_table"]
        target_layer.updateFeature(target_feat)

    def process_features(self, external_features):
        grouped_features = self.group_features(
            external_features,
            self.conversion_settings.group_by_field,
            self.target_fields_config,
        )
        external_features = [
            CrossSectionDataProcessor.get_feat_from_group(
                feat_group,
                self.conversion_settings.order_by_field,
                self.target_fields_config,
            )
            for feat_group in grouped_features
        ]
        for external_src_feat in external_features:
            self.process_feature(external_src_feat)
        return {}


class CrossSectionLocationProcessor(Processor):
    def __init__(
        self,
        target_layer,
        target_model_cls,
        channel_layer,
        conversion_settings,
        target_fields_config,
    ):
        super().__init__(target_layer, target_model_cls)
        self.channel_layer = channel_layer
        self.channel_spatial_index = QgsSpatialIndex(channel_layer)
        self.conversion_settings = conversion_settings
        self.target_fields_config = target_fields_config

    @cached_property
    def channel_mapping(self):
        if self.conversion_settings.join_field_tgt in ["id", "code"]:
            return {
                feature[self.conversion_settings.join_field_tgt]: feature
                for feature in self.channel_layer.getFeatures()
            }
        else:
            return {}

    @cached_property
    def join_field_src(self):
        if self.conversion_settings.join_field_src in self.target_fields.names():
            return self.conversion_settings.join_field_src
        else:
            return None

    def get_matching_channel(self, feat, geom):
        # note that feat.geometry() is not used because geom may be transformed
        channel_match = None
        if geom.isEmpty():
            if (
                self.conversion_settings.join_field_src is not None
                and feat[self.conversion_settings.join_field_src] is not None
            ):
                channel_match = self.channel_mapping.get(
                    feat[self.conversion_settings.join_field_src]
                )
        else:
            geometry_type = geom.type()
            if geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
                closest_feature_id = self.channel_spatial_index.nearestNeighbor(
                    geom.asPoint(), 1, self.conversion_settings.snapping_distance
                )
                if len(closest_feature_id) > 0:
                    channel_match = next(
                        f
                        for f in self.channel_layer.getFeatures(
                            QgsFeatureRequest(closest_feature_id[0])
                        )
                    )
                else:
                    channel_match = None

            elif geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
                matching_channels = [
                    channel
                    for channel in self.channel_layer.getFeatures()
                    if channel.geometry().intersects(geom)
                ]
                if len(matching_channels) != 1:
                    return None
                channel_match = matching_channels[0]
            else:
                raise NotImplementedError(
                    f"Unsupported geometry type: '{geometry_type}'"
                )
        if channel_match:
            return channel_match["id"]

    @staticmethod
    def get_new_geom(src_geom, ref_channel):
        channel_geom = ref_channel.geometry() if ref_channel else None
        geometry_type = src_geom.type()
        if src_geom.isEmpty():
            # return center of matching channel
            if ref_channel is not None:
                return channel_geom.interpolate(channel_geom.length() / 2)
        elif geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
            # return nearest point on matched channel if there is a channel match
            if ref_channel is not None:
                return channel_geom.nearestPoint(src_geom)
            # otherwise return point
            else:
                return src_geom
        elif geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
            # return intersection between channel and line if there is a channel match
            if ref_channel:
                return src_geom.intersection(channel_geom)
            # otherwise return center of the line
            else:
                return src_geom.interpolate(src_geom.length() / 2)
        else:
            raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")

    def process_feature(self, src_feat):
        src_geom = QgsGeometry(src_feat.geometry())
        if self.transformation:
            src_geom.transform(self.transformation)
        channel_id = self.get_matching_channel(src_feat, src_geom)
        ref_channel = next(
            (
                channel
                for channel in self.channel_layer.getFeatures()
                if channel.id() == channel_id
            ),
            None,
        )
        new_geom = CrossSectionLocationProcessor.get_new_geom(src_geom, ref_channel)
        if new_geom is None:
            return {self.target_name: []}
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        update_attributes(
            self.target_fields_config,
            self.target_model_cls,
            src_feat,
            new_feat,
        )
        if channel_id is not None:
            new_feat["channel_id"] = channel_id
        return {self.target_name: [new_feat]}


class ConnectionNodeProcessor(Processor):
    def __init__(
        self,
        target_layer,
        target_model_cls,
        fields_configuration,
    ):
        super().__init__(target_layer, target_model_cls)
        self.fields_configuration = fields_configuration

    def process_feature(self, src_feat):
        """Process source point into connection node feature."""
        new_geom = ConnectionNodeProcessor.create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        update_attributes(
            self.fields_configuration,
            dm.ConnectionNode,
            src_feat,
            new_feat,
        )
        return {self.target_name: [new_feat]}


class StructureProcessor(Processor, ABC):
    def __init__(
        self,
        target_layer,
        target_model_cls,
        node_layer,
        fields_configurations,
        conversion_settings,
    ):
        super().__init__(target_layer, target_model_cls)
        self.node_fields = node_layer.fields()
        self.node_name = node_layer.name()
        self.node_layer = node_layer
        self.node_manager = FeatureManager(get_next_feature_id(node_layer))
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings

    def get_node(self, point):
        snapped = False
        node = None
        if self.conversion_settings.use_snapping:
            node = find_connection_node(
                point, self.node_locator, self.conversion_settings.snapping_distance
            )
            snapped = node is not None
        if self.conversion_settings.create_connection_nodes and (
            not snapped or not self.conversion_settings.use_snapping
        ):
            node = self.node_manager.create_new(
                QgsGeometry.fromPointXY(point), self.node_fields
            )
        return node, snapped


class PointProcessor(StructureProcessor):
    def update_connection_nodes(self, new_feat):
        node, snapped = self.get_node(new_feat.geometry().asPoint())
        new_nodes = []
        if node:
            new_feat["connection_node_id"] = node["id"]
            if snapped:
                new_feat.setGeometry(QgsGeometry.fromPointXY(node.geometry().asPoint()))
            if not snapped:
                self.node_layer.addFeature(node)
                new_nodes.append(node)
        return new_nodes

    def process_feature(self, src_feat):
        """Process source point structure feature."""
        new_nodes = []
        new_geom = PointProcessor.create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        update_attributes(
            self.fields_configurations[dm.ConnectionNode],
            dm.ConnectionNode,
            src_feat,
            *new_nodes,
        )
        new_nodes = self.update_connection_nodes(new_feat)
        update_attributes(
            self.fields_configurations[self.target_model_cls],
            self.target_model_cls,
            src_feat,
            new_feat,
        )
        return {self.target_name: [new_feat]}


class LineProcessor(StructureProcessor):
    @staticmethod
    def new_geometry(src_feat, conversion_settings, target_model_cls):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        geometry_type = src_geometry.type()
        if geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
            src_polyline = src_geometry.asPolyline()
            dst_polyline = (
                src_polyline
                if target_model_cls in [dm.Culvert, dm.Pipe, dm.Channel]
                else [src_polyline[0], src_polyline[-1]]
            )
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        elif geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
            start_point = src_geometry.asPoint()
            length = get_float_value_from_feature(
                src_feat,
                conversion_settings.length_source_field,
                conversion_settings.length_fallback_value,
            )
            azimuth = get_float_value_from_feature(
                src_feat,
                conversion_settings.azimuth_source_field,
                conversion_settings.azimuth_fallback_value,
            )
            end_point = start_point.project(length, azimuth)
            dst_polyline = [start_point, end_point]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        else:
            raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")
        return dst_geometry

    def update_connection_nodes(self, new_feat):
        new_nodes = []
        polyline = new_feat.geometry().asPolyline()
        for idx, name in [
            (0, "connection_node_id_start"),
            (-1, "connection_node_id_end"),
        ]:
            node, snapped = self.get_node(polyline[idx])
            if node:
                new_feat[name] = node["id"]
                if snapped:
                    polyline[idx] = node.geometry().asPoint()
                    new_feat.setGeometry(QgsGeometry.fromPolylineXY(polyline))
                if not snapped:
                    self.node_layer.addFeature(node)
                    new_nodes.append(node)
        return new_nodes

    def process_feature(self, src_feat):
        """Process source linear structure feature."""
        new_geom = LineProcessor.new_geometry(
            src_feat, self.conversion_settings, self.target_model_cls
        )
        if self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        update_attributes(
            self.fields_configurations[self.target_model_cls],
            self.target_model_cls,
            src_feat,
            new_feat,
        )
        new_nodes = self.update_connection_nodes(new_feat)
        update_attributes(
            self.fields_configurations[dm.ConnectionNode],
            dm.ConnectionNode,
            src_feat,
            *new_nodes,
        )
        return {self.target_name: [new_feat]}
