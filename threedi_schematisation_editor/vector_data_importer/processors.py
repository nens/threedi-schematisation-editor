from abc import ABC
from functools import cached_property

from qgis.core import (
    NULL,
    QgsExpression,
    QgsExpressionContext,
    QgsFeatureRequest,
    QgsGeometry,
    QgsSpatialIndex,
    QgsWkbTypes,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    find_connection_node,
    get_next_feature_id,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureManager,
    get_float_value_from_feature,
    update_attributes,
)


class Processor(ABC):
    def __init__(self, target_layer, target_model_cls):
        self.target_fields = target_layer.fields()
        self.target_name = target_layer.name()
        self.target_manager = FeatureManager(get_next_feature_id(target_layer))
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
