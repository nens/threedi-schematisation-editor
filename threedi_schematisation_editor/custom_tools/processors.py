from abc import ABC

from qgis.core import QgsGeometry, QgsWkbTypes


from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.custom_tools.utils import update_attributes, FeatureManager
from threedi_schematisation_editor.utils import find_connection_node
from threedi_schematisation_editor.utils import get_next_feature_id


class Processor(ABC):
    def __init__(self, target_layer, target_model_cls):
        self.target_fields = target_layer.fields()
        self.target_name = target_layer.name()
        self.target_manager = FeatureManager(get_next_feature_id(target_layer))
        self.target_model_cls = target_model_cls
        self.transformation = None
        self.locator = None

    @classmethod
    def snap_connection_node(cls, feat, point, snapping_distance, locator, connection_id_name):
        node = find_connection_node(point, locator, snapping_distance)
        if node:
            feat.setGeometry(QgsGeometry.fromPointXY(node.geometry().asPoint()))
            feat[connection_id_name] = node["id"]
            return True
        else:
            return False

    @classmethod
    def add_connection_node(cls, feat, geom, node_manager, connection_id_name, node_fields):
        new_node_feat = node_manager.create_new(QgsGeometry.fromPointXY(geom), node_fields)
        feat[connection_id_name] = new_node_feat["id"]
        return new_node_feat

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


class ConnectionNodeProcessor(Processor):

    def process_feature(self, src_feat):
        """Process source point into connection node feature."""
        new_geom = ConnectionNodeProcessor.create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        return {self.target_name : [self.target_manager.create_new(new_geom, self.target_fields)]}


class StructureProcessor(Processor, ABC):
    def __init__(self, target_layer, target_model_cls, node_layer, fields_configurations, conversion_settings):
        super().__init__(target_layer, target_model_cls)
        self.node_fields = node_layer.fields()
        self.node_name = node_layer.name()
        self.node_manager = FeatureManager(get_next_feature_id(node_layer))
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings

    def add_node(self, new_feat, point, name):
        snapped = False
        if self.conversion_settings.use_snapping:
            snapped = StructureProcessor.snap_connection_node(new_feat, point, self.conversion_settings.snapping_distance, self.locator,
                                           name)
        if not snapped or self.conversion_settings.create_connection_nodes:
            return StructureProcessor.add_connection_node(new_feat, point, self.node_manager, name, self.node_fields)


class PointProcessor(StructureProcessor):

    def process_feature(self, src_feat):
        """Process source point structure feature."""
        new_nodes = []
        new_geom = PointProcessor.create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        point = new_geom.asPoint()
        new_node = self.add_node(new_feat, point, "connection_node_id")
        if new_node:
            new_nodes.append(new_node)
        update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_feat,
                          *new_nodes)
        update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_feat,
                          new_feat)
        return {self.target_name : [new_feat], self.node_name : new_nodes}


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
            dst_polyline = src_polyline if (target_model_cls == dm.Culvert or target_model_cls == dm.Pipe) else [src_polyline[0], src_polyline[-1]]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        elif geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
            start_point = src_geometry.asPoint()
            length = (
                src_feat[conversion_settings.length_source_field]
                if conversion_settings.length_source_field
                else conversion_settings.length_fallback_value
            )
            azimuth = (
                src_feat[conversion_settings.azimuth_source_field]
                if conversion_settings.azimuth_source_field
                else conversion_settings.azimuth_fallback_value
            )
            end_point = start_point.project(length, azimuth)
            dst_polyline = [start_point, end_point]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        else:
            raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")
        return dst_geometry

    def process_feature(self, src_feat):
        """Process source linear structure feature."""
        new_nodes = []
        new_geom = LineProcessor.new_geometry(src_feat, self.conversion_settings, self.target_model_cls)
        if self.transformation:
            new_geom.transform(transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        polyline = new_feat.geometry().asPolyline()
        for (idx, name) in [(0, 'connection_node_id_start'), (1, 'connection_node_id_end')]:
            new_node = self.add_node(new_feat, polyline[idx], name)
            if new_node:
                new_nodes.append(new_node)
        update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_feat,
                          new_feat)
        update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_feat,
                          *new_nodes)
        return {self.target_name : [new_feat], self.node_name : new_nodes}

