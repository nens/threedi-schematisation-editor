# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict
from enum import Enum
from functools import cached_property
from itertools import chain

from qgis.core import NULL, QgsCoordinateTransform, QgsFeature, QgsGeometry, QgsPointLocator, QgsProject
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QLineEdit

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    enum_entry_name_format,
    find_line_endpoints_nodes,
    get_next_feature_id,
    gpkg_layer,
    is_optional,
    optional_type,
)


class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    IGNORE = "ignore"


class CulvertImportSettings:
    def __init__(self):
        self.culvert_cls = dm.Culvert
        self.nodes_cls = dm.ConnectionNode

    @property
    def config_header(self):
        header = ["Field name", "Method", "Source attribute", "Value map", "Default value"]
        return header

    @cached_property
    def field_methods_mapping(self):
        methods_mapping = defaultdict(dict)
        auto_fields = {"id"}
        auto_attribute_fields = {"connection_node_start_id", "connection_node_end_id"}
        culvert_fields = ((k, self.culvert_cls) for k in self.culvert_cls.__annotations__.keys())
        node_fields = ((k, self.nodes_cls) for k in self.nodes_cls.__annotations__.keys())
        for field_name, model_cls in chain(culvert_fields, node_fields):
            if field_name in auto_fields:
                methods_mapping[model_cls][field_name] = [ColumnImportMethod.AUTO]
            elif field_name in auto_attribute_fields:
                methods_mapping[model_cls][field_name] = [ColumnImportMethod.AUTO, ColumnImportMethod.ATTRIBUTE]
            else:
                methods_mapping[model_cls][field_name] = [
                    ColumnImportMethod.ATTRIBUTE,
                    ColumnImportMethod.DEFAULT,
                    ColumnImportMethod.IGNORE,
                ]
        return methods_mapping

    def culvert_widgets(self):
        widgets_to_add = defaultdict(dict)
        for model_cls, field_methods_mapping in self.field_methods_mapping.items():
            model_fields_display_names = model_cls.fields_display_names()
            for row_idx, (field_name, field_methods) in enumerate(field_methods_mapping.items()):
                field_type = model_cls.__annotations__[field_name]
                if is_optional(field_type):
                    field_type = optional_type(field_type)
                for column_idx, column_name in enumerate(self.config_header):
                    if column_idx == 0:
                        widget = QLabel(model_fields_display_names[field_name])
                    elif column_idx == 1:
                        widget = QComboBox()
                        widget.addItems([method.value for method in field_methods])
                    else:
                        if issubclass(field_type, Enum) and column_name == "Default value":
                            widget = QComboBox()
                            widget.addItems([""] + [enum_entry_name_format(e.name) for e in field_type])
                        else:
                            widget = QLineEdit()
                    widgets_to_add[model_cls][row_idx, column_idx] = widget
        return widgets_to_add


def import_culverts(source_culvert_layer, target_gpkg, import_config, context=None):
    conversion_settings = import_config["conversion_settings"]
    use_snapping = conversion_settings.get("use_snapping", False)
    snapping_distance = conversion_settings.get("snapping_distance", 0.1)
    create_connection_nodes = conversion_settings.get("create_connection_nodes", False)
    fields_config = import_config["fields"]
    culvert_layer = gpkg_layer(target_gpkg, dm.Culvert.__tablename__)
    node_layer = gpkg_layer(target_gpkg, dm.ConnectionNode.__tablename__)
    culvert_fields = culvert_layer.fields()
    node_fields = node_layer.fields()
    project = context.project() if context else QgsProject.instance()
    src_crs = source_culvert_layer.sourceCrs()
    dst_crs = culvert_layer.crs()
    transform_ctx = project.transformContext()
    transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
    next_culvert_id = get_next_feature_id(culvert_layer)
    next_connection_node_id = get_next_feature_id(node_layer)
    locator = QgsPointLocator(node_layer, dst_crs, transform_ctx)
    new_culverts = []
    node_layer.startEditing()
    culvert_layer.startEditing()
    for src_feat in source_culvert_layer.getFeatures():
        new_nodes = []
        new_culvert_feat = QgsFeature(culvert_fields)
        new_culvert_feat["id"] = next_culvert_id
        new_geom = QgsGeometry.fromPolylineXY(src_feat.geometry().asPolyline())
        if transformation:
            new_geom.transform(transformation)
        polyline = new_geom.asPolyline()
        if use_snapping:
            node_start_feat, node_end_feat = find_line_endpoints_nodes(polyline, locator, snapping_distance)
            if node_start_feat:
                node_start_point = node_start_feat.geometry().asPoint()
                polyline[0] = node_start_point
                new_culvert_feat["connection_node_start_id"] = node_start_feat["id"]
                new_geom = QgsGeometry.fromPolylineXY(polyline)
            else:
                if create_connection_nodes:
                    node_start_point = polyline[0]
                    new_start_node_feat = QgsFeature(node_fields)
                    new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                    new_start_node_feat["id"] = next_connection_node_id
                    new_culvert_feat["connection_node_start_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes.append(new_start_node_feat)
            if node_end_feat:
                node_end_point = node_end_feat.geometry().asPoint()
                polyline[-1] = node_end_point
                new_culvert_feat["connection_node_end_id"] = node_end_feat["id"]
                new_geom = QgsGeometry.fromPolylineXY(polyline)
            else:
                if create_connection_nodes:
                    node_end_point = polyline[-1]
                    new_end_node_feat = QgsFeature(node_fields)
                    new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                    new_end_node_feat["id"] = next_connection_node_id
                    new_culvert_feat["connection_node_end_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes.append(new_end_node_feat)
        else:
            if create_connection_nodes:
                node_start_point = polyline[0]
                new_start_node_feat = QgsFeature(node_fields)
                new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                new_start_node_feat["id"] = next_connection_node_id
                new_culvert_feat["connection_node_start_id"] = next_connection_node_id
                next_connection_node_id += 1
                node_end_point = polyline[-1]
                new_end_node_feat = QgsFeature(node_fields)
                new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                new_end_node_feat["id"] = next_connection_node_id
                new_culvert_feat["connection_node_end_id"] = next_connection_node_id
                next_connection_node_id += 1
                new_nodes += [new_start_node_feat, new_end_node_feat]
        if new_nodes:
            node_layer.addFeatures(new_nodes)
            locator = QgsPointLocator(node_layer, dst_crs, transform_ctx)
        new_culvert_feat.setGeometry(new_geom)
        fields_to_process = [
            field_name
            for field_name in dm.Culvert.__annotations__.keys()
            if field_name != "id" and not field_name.startswith("connection_node_")
        ]
        for field_name in fields_to_process:
            try:
                field_config = fields_config[field_name]
            except KeyError:
                continue
            method = ColumnImportMethod(field_config["method"])
            if method == ColumnImportMethod.ATTRIBUTE:
                src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
                src_value = src_feat[src_field_name]
                try:
                    value_map = field_config["value_map"]
                    field_value = value_map[src_value]
                except KeyError:
                    field_value = src_value
                if field_value == NULL:
                    field_value = field_config.get("default_value", NULL)
                new_culvert_feat[field_name] = field_value
            elif method == ColumnImportMethod.DEFAULT:
                default_value = field_config["default_value"]
                new_culvert_feat[field_name] = default_value
            else:
                new_culvert_feat[field_name] = NULL
        next_culvert_id += 1
        new_culverts.append(new_culvert_feat)
    node_layer.commitChanges()
    culvert_layer.addFeatures(new_culverts)
    culvert_layer.commitChanges()
