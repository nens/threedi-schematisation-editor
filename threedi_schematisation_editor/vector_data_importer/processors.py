import warnings
from abc import ABC
from collections import defaultdict
from functools import cached_property
from typing import Optional

from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsSpatialIndex,
    QgsVectorLayer,
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
from threedi_schematisation_editor.warnings import ProcessorWarning


class Processor:
    def process_feature(self, src_feat: QgsFeature) -> dict[str, list[QgsFeature]]:
        raise NotImplementedError

    def process_features(
        self, external_features: list[QgsFeature]
    ) -> dict[str, list[QgsFeature]]:
        new_features = defaultdict(list)
        for external_src_feat in external_features:
            for name, features in self.process_feature(external_src_feat).items():
                new_features[name] += features
        return new_features


class SpatialProcessor(Processor):
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


class CrossSectionDataProcessor(Processor):
    target_models: list[type] = [
        dm.Pipe,
        dm.Culvert,
        dm.Orifice,
        dm.Weir,
        dm.CrossSectionLocation,
    ]

    def __init__(
        self,
        target_fields_config,
        target_match_config,
        target_layers,
    ):
        self.target_fields_config = target_fields_config
        self.target_match_config = target_match_config
        self.target_layer_map = {
            CrossSectionDataProcessor.get_unified_object_type_str(
                target_layer.name()
            ): target_layer
            for target_layer in target_layers
        }
        self.source_feat_map = {}

    def process_feature(self, src_feat: QgsFeature) -> dict[str, list[QgsFeature]]:
        # retrieve target feature, model class and layer
        target_feat = self.source_feat_map[src_feat]
        target_model_cls = self.get_target_model_cls(src_feat)
        target_layer = self.get_target_layer(target_model_cls)
        # updata attributes
        update_attributes(
            self.target_fields_config,
            target_model_cls,
            src_feat,
            target_feat,
        )
        # add cross section table manually because this is not in self.target_fields_config
        if "cross_section_table" in src_feat.fields().names():
            target_feat["cross_section_table"] = src_feat["cross_section_table"]
        target_layer.updateFeature(target_feat)
        return {}

    def process_features(
        self, external_features: QgsFeature
    ) -> dict[str, list[QgsFeature]]:
        # match imported features to features in the schematisation
        self.build_target_map(external_features)
        # group features with the same target and that can be grouped
        grouped_features = self.group_features()
        # convert grouped features into a single feature that can be processed
        external_features = [
            self.get_feat_from_group(feat_group) for feat_group in grouped_features
        ]
        return super().process_features(external_features)

    def build_target_map(self, features):
        for src_feat in features:
            target_model_cls = self.get_target_model_cls(src_feat)
            if not target_model_cls:
                continue
            target_layer = self.get_target_layer(target_model_cls)
            if not target_layer:
                continue
            target_feat = self.find_target_object(
                src_feat,
                target_layer,
                self.target_match_config.get("target_object_id"),
                self.target_match_config.get("target_object_code"),
            )
            self.source_feat_map[src_feat] = target_feat

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
    def get_cross_section_table_column(feature_group, column_name, field_config):
        column = [
            get_field_config_value(field_config[column_name], feat)
            for feat in feature_group
        ]
        if any(val == NULL for val in column):
            null_idx = [
                feat.id()
                for idx, feat in enumerate(feature_group)
                if column[idx] == NULL
            ]
            warnings.warn(
                f"Cannot cross-section table because {column_name} is NULL for features: {null_idx}",
                ProcessorWarning,
            )
            return []
        return column

    @staticmethod
    def get_cross_section_table(
        feature_group: list[QgsFeature],
        cross_section_shape: CrossSectionShape,
        order_by_config: dict,
        field_config,
    ) -> Optional[str]:
        # Build cross section table for a group of features
        if not cross_section_shape.is_tabulated:
            return None
        col_left = []
        col_right = []
        if cross_section_shape in [
            CrossSectionShape.TABULATED_RECTANGLE,
            CrossSectionShape.TABULATED_TRAPEZIUM,
        ]:
            # collect height, width pairs
            col_left = CrossSectionDataProcessor.get_cross_section_table_column(
                feature_group, "cross_section_height", field_config
            )
            col_right = CrossSectionDataProcessor.get_cross_section_table_column(
                feature_group, "cross_section_width", field_config
            )
        elif cross_section_shape == CrossSectionShape.TABULATED_YZ:
            #  collect y, z pairs
            col_left = CrossSectionDataProcessor.get_cross_section_table_column(
                feature_group, "cross_section_y", field_config
            )
            col_right = CrossSectionDataProcessor.get_cross_section_table_column(
                feature_group, "cross_section_z", field_config
            )
        if not col_right or not col_left:
            return ""
        # Retrieve order values from data
        order_by_vals = [
            get_field_config_value(order_by_config, feat) for feat in feature_group
        ]
        # Use default when any value in order_by_vals is NULL
        # this happens when AUTO is selected or when the parsing for another method is unsuccessful
        if NULL in order_by_vals:
            order_by_vals = col_left
        sorted_indices = sorted(
            range(len(order_by_vals)), key=lambda i: order_by_vals[i]
        )
        table = [(col_left[i], col_right[i]) for i in sorted_indices]
        return "\n".join(f"{pair[0]},{pair[1]}" for pair in table)

    @staticmethod
    def organize_group(
        group: list[QgsFeature], shape_config_field: dict
    ) -> Optional[list[QgsFeature]]:
        cross_section_shape_values = [
            get_field_config_value(shape_config_field, feat) for feat in group
        ]
        # check if all shapes in a group are the same
        # warn if not, but continue
        if not all(
            shape_value == cross_section_shape_values[0]
            for shape_value in cross_section_shape_values
        ):
            warnings.warn(
                f"Not all features in group have the same cross section shape; grouped ids: {[feat.id() for feat in group]}",
                ProcessorWarning,
            )
        # find the first item with a tabulated shape
        # if no such item exists, warn and abort grouping
        tabulated_shapes = [
            shape.value for shape in CrossSectionShape if shape.is_tabulated
        ]
        first_valid_idx = next(
            (
                idx
                for idx, shape_value in enumerate(cross_section_shape_values)
                if shape_value in tabulated_shapes
            ),
            None,
        )
        if first_valid_idx is None:
            warnings.warn(
                f"No feature in this group has a tabulated cross-section shape; grouped ids: {[feat.id() for feat in group]}",
                ProcessorWarning,
            )
            return
        # Reorder group so that group[first_valid_idx] is the first item
        group.insert(0, group.pop(first_valid_idx))
        return group

    def group_features(self) -> list[list[QgsFeature]]:
        # Group features based on group by value.
        grouped_features = []
        # map each target feature the its associated source features
        target_map = defaultdict(list)
        for src_feat, tgt_feat in self.source_feat_map.items():
            target_map[tgt_feat].append(src_feat)
        for tgt_feat, provisional_group in target_map.items():
            # skip grouping for single features
            if len(provisional_group) == 1:
                grouped_features.append(provisional_group)
                continue
            # organize features that match to the same object
            group = CrossSectionDataProcessor.organize_group(
                provisional_group, self.target_fields_config["cross_section_shape"]
            )
            # in case the cross section shape does not support grouping, just add features one by one
            # and add ids to grouped_ids to prevent revisiting those features
            if not group:
                for feat in provisional_group:
                    grouped_features.append([feat])
                continue
            # add group, with supported shape, as list of features
            grouped_features.append(group)
        return grouped_features

    def get_feat_from_group(self, group: list[QgsFeature]) -> Optional[QgsFeature]:
        # Combine group of feature in a single feature that is used for processing
        if len(group) == 0:
            return
        if len(group) == 1:
            return group[0]
        feature = group[0]
        cross_section_shape = CrossSectionShape(
            get_field_config_value(
                self.target_fields_config["cross_section_shape"], feature
            )
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
                group,
                cross_section_shape,
                self.target_match_config.get("order_by"),
                self.target_fields_config,
            )
        )
        self.source_feat_map[new_feat] = self.source_feat_map[feature]
        return new_feat

    @staticmethod
    def find_target_object(
        src_feat: QgsFeature,
        target_layer: QgsVectorLayer,
        target_object_id_config: dict,
        target_object_code_config: dict,
    ) -> Optional[QgsFeature]:
        target_feat = None
        if target_object_id_config:
            target_id = get_field_config_value(target_object_id_config, src_feat)
            if target_id:
                target_feat = next(
                    (
                        feature
                        for feature in target_layer.getFeatures()
                        if feature["id"] == target_id
                    ),
                    None,
                )
        if not target_feat and target_object_code_config:
            target_code = get_field_config_value(target_object_code_config, src_feat)
            if target_code:
                target_feat = next(
                    (
                        feature
                        for feature in target_layer.getFeatures()
                        if feature["code"] == target_code
                    ),
                    None,
                )
        if not target_feat:
            warnings.warn(
                f'Could not find target object for feature "{src_feat["id"]}"',
                ProcessorWarning,
            )
        return target_feat

    def get_target_model_cls(self, src_feat: QgsFeature) -> Optional[type]:
        target_object_config = self.target_match_config.get("target_object_type")
        if not target_object_config:
            return
        src_object_type = get_field_config_value(target_object_config, src_feat)
        # Make sure src_object_type = NULL warns
        if not src_object_type:
            warnings.warn(
                f"Could not find value for target_object_type for feature {src_feat['id']}",
                ProcessorWarning,
            )
            return
        src_object_type_str = CrossSectionDataProcessor.get_unified_object_type_str(
            src_object_type
        )
        target_model_cls = self.object_type_map.get(src_object_type_str, None)
        if not target_model_cls:
            warnings.warn(
                f"Could not find target model for object type {src_object_type} for feature {src_feat['id']}",
                ProcessorWarning,
            )
        return target_model_cls

    def get_target_layer(self, target_model_cls) -> Optional[QgsVectorLayer]:
        return self.target_layer_map.get(
            CrossSectionDataProcessor.get_unified_object_type_str(
                target_model_cls.__layername__
            ),
            None,
        )


class CrossSectionLocationProcessor(SpatialProcessor):
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
        if (
            self.conversion_settings.join_field_tgt.get("method")
            == ColumnImportMethod.ATTRIBUTE.value
        ):
            col = self.conversion_settings.join_field_tgt.get(
                ColumnImportMethod.ATTRIBUTE.value
            )
            if col:
                return {
                    feature[col]: feature
                    for feature in self.channel_layer.getFeatures()
                }
        elif (
            self.conversion_settings.join_field_tgt.get("method")
            == ColumnImportMethod.EXPRESSION.value
        ):
            expression_str = self.conversion_settings.join_field_tgt.get(
                ColumnImportMethod.EXPRESSION.value
            )
            expression = QgsExpression(expression_str)
            if expression.isValid():
                context = QgsExpressionContext()
                expr_map = {}
                for feature in self.channel_layer.getFeatures():
                    context.setFeature(feature)
                    expr_map[expression.evaluate(context)] = feature
                return expr_map
        return {}

    @cached_property
    def join_field_src(self):
        if self.conversion_settings.join_field_src in self.target_fields.names():
            return self.conversion_settings.join_field_src
        else:
            return None

    def get_join_feat_src_value(self, feat):
        if self.conversion_settings.join_field_src is None:
            return
        if (
            self.conversion_settings.join_field_src.get("method")
            == ColumnImportMethod.ATTRIBUTE.value
        ):
            field = self.conversion_settings.join_field_src.get(
                ColumnImportMethod.ATTRIBUTE.value
            )
            if field in feat.fields().names():
                return feat[field]
        elif (
            self.conversion_settings.join_field_src.get("method")
            == ColumnImportMethod.EXPRESSION.value
        ):
            expression_str = self.conversion_settings.join_field_src.get(
                ColumnImportMethod.EXPRESSION.value
            )
            expression = QgsExpression(expression_str)
            context = QgsExpressionContext()
            context.setFeature(feat)
            return expression.evaluate(context)

    def get_matching_channel(self, feat, geom):
        # note that feat.geometry() is not used because geom may be transformed
        # First match based on join settings, if no join settings are present channel_match will be None
        feat_val = self.get_join_feat_src_value(feat)
        channel_match = self.channel_mapping.get(feat_val)
        # If no match on join setings was made, match based on geometry
        if not channel_match and not geom.isEmpty():
            if geom.type() not in [
                QgsWkbTypes.GeometryType.LineGeometry,
                QgsWkbTypes.GeometryType.PointGeometry,
            ]:
                raise NotImplementedError(f"Unsupported geometry type: '{geom.type()}'")
            if geom.type() == QgsWkbTypes.GeometryType.LineGeometry:
                matching_channels = [
                    channel
                    for channel in self.channel_layer.getFeatures()
                    if channel.geometry().intersects(geom)
                ]
                if len(matching_channels) == 0:
                    return None
                elif len(matching_channels) == 1:
                    channel_match = matching_channels[0]
                else:
                    # in case of multiple matches, perform match based on midpoint
                    geom = geom.interpolate(geom.length() / 2)
            if geom.type() == QgsWkbTypes.GeometryType.PointGeometry:
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


class ConnectionNodeProcessor(SpatialProcessor):
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


class StructureProcessor(SpatialProcessor, ABC):
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
