# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict
from enum import Enum
from functools import cached_property
from itertools import chain

from qgis.core import NULL, QgsCoordinateTransform, QgsFeature, QgsGeometry, QgsPointLocator, QgsProject
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton

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


class StructuresImportConfig:
    """Structures import tool configuration class."""

    FIELD_NAME_COLUMN_IDX = 0
    METHOD_COLUMN_IDX = 1
    SOURCE_ATTRIBUTE_COLUMN_IDX = 2
    VALUE_MAP_COLUMN_IDX = 3
    DEFAULT_VALUE_COLUMN_IDX = 4

    def __init__(self, structures_model_cls):
        self.structures_model_cls = structures_model_cls
        self.nodes_cls = dm.ConnectionNode

    @property
    def config_header(self):
        header = ["Field name", "Method", "Source attribute", "Value map", "Default value"]
        return header

    @property
    def config_keys(self):
        header = ["method", "source_attribute", "value_map", "default_value"]
        return header

    @cached_property
    def field_methods_mapping(self):
        methods_mapping = defaultdict(dict)
        auto_fields = {"id"}
        auto_attribute_fields = {"connection_node_start_id", "connection_node_end_id"}
        culvert_fields = ((k, self.structures_model_cls) for k in self.structures_model_cls.__annotations__.keys())
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

    def structure_widgets(self):
        widgets_to_add = defaultdict(dict)
        combobox_column_indexes = {self.METHOD_COLUMN_IDX, self.SOURCE_ATTRIBUTE_COLUMN_IDX}
        for model_cls, field_methods_mapping in self.field_methods_mapping.items():
            model_fields_display_names = model_cls.fields_display_names()
            for row_idx, (field_name, field_methods) in enumerate(field_methods_mapping.items()):
                field_type = model_cls.__annotations__[field_name]
                if is_optional(field_type):
                    field_type = optional_type(field_type)
                for column_idx, column_name in enumerate(self.config_header):
                    if column_idx == self.FIELD_NAME_COLUMN_IDX:
                        field_display_name = model_fields_display_names[field_name]
                        label_text = f"{field_display_name}\t"
                        widget = QLabel(label_text)
                    elif column_idx in combobox_column_indexes:
                        widget = QComboBox()
                        if column_idx == self.METHOD_COLUMN_IDX:
                            for method in field_methods:
                                widget.addItem(method.name.capitalize(), method.value)
                    elif column_idx == self.VALUE_MAP_COLUMN_IDX:
                        widget = QPushButton("Set...")
                        widget.value_map = {}
                    else:
                        if column_idx == self.DEFAULT_VALUE_COLUMN_IDX and (
                            issubclass(field_type, Enum) or field_type == bool
                        ):
                            widget = QComboBox()
                            items = (
                                [["False", False], ["True", True]]
                                if field_type == bool
                                else [["NULL", "NULL"]]
                                + [[enum_entry_name_format(e.name), e.value] for e in field_type]
                            )
                            for item_str, item_data in items:
                                widget.addItem(item_str, item_data)
                        else:
                            widget = QLineEdit()
                    widgets_to_add[model_cls][row_idx, column_idx] = widget
        return widgets_to_add


class ExternalFeaturesImporter:
    """Base class for the importing features from the external data source."""

    def __init__(self, external_source, target_gpkg, import_settings):
        self.external_source = external_source
        self.target_gpkg = target_gpkg
        self.import_settings = import_settings
        self.structure_model_cls = None
        self.structure_layer = None
        self.node_layer = None
        self.fields_configurations = {}

    def setup_target_layers(self, structure_model_cls, structure_layer=None, node_layer=None):
        self.structure_layer = (
            gpkg_layer(self.target_gpkg, structure_model_cls.__tablename__)
            if structure_layer is None
            else structure_layer
        )
        self.node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__) if node_layer is None else node_layer
        )
        self.fields_configurations = {
            structure_model_cls: self.import_settings.get("fields", {}),
            dm.ConnectionNode: self.import_settings.get("connection_node_fields", {}),
        }
        self.structure_model_cls = structure_model_cls

    def update_attributes(self, model_cls, source_feat, *new_features):
        fields_config = self.fields_configurations[model_cls]
        for new_feat in new_features:
            for field_name in model_cls.__annotations__.keys():
                try:
                    field_config = fields_config[field_name]
                except KeyError:
                    continue
                method = ColumnImportMethod(field_config["method"])
                if method == ColumnImportMethod.AUTO:
                    continue
                elif method == ColumnImportMethod.ATTRIBUTE:
                    src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
                    src_value = source_feat[src_field_name]
                    try:
                        value_map = field_config["value_map"]
                        field_value = value_map[src_value]
                    except KeyError:
                        field_value = src_value
                    if field_value == NULL:
                        field_value = field_config.get("default_value", NULL)
                    new_feat[field_name] = field_value
                elif method == ColumnImportMethod.DEFAULT:
                    default_value = field_config["default_value"]
                    new_feat[field_name] = default_value
                else:
                    new_feat[field_name] = NULL

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = src_structure_feat.geometry()
        src_polyline = src_geometry.asPolyline()
        dst_polyline = src_polyline if self.structure_model_cls == dm.Culvert else [src_polyline[0], src_polyline[-1]]
        dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        return dst_geometry

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        conversion_settings = self.import_settings["conversion_settings"]
        use_snapping = conversion_settings.get("use_snapping", False)
        snapping_distance = conversion_settings.get("snapping_distance", 0.1)
        create_connection_nodes = conversion_settings.get("create_connection_nodes", False)
        structure_fields = self.structure_layer.fields()
        node_fields = self.node_layer.fields()
        project = context.project() if context else QgsProject.instance()
        src_crs = self.external_source.sourceCrs()
        dst_crs = self.structure_layer.crs()
        transform_ctx = project.transformContext()
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
        next_structure_id = get_next_feature_id(self.structure_layer)
        next_connection_node_id = get_next_feature_id(self.node_layer)
        locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
        new_structures = []
        self.node_layer.startEditing()
        self.structure_layer.startEditing()
        for src_feat in (
            self.external_source.getFeatures(selected_ids) if selected_ids else self.external_source.getFeatures()
        ):
            new_nodes = []
            new_structure_feat = QgsFeature(structure_fields)
            new_structure_feat["id"] = next_structure_id
            new_geom = self.new_structure_geometry(src_feat)
            if transformation:
                new_geom.transform(transformation)
            polyline = new_geom.asPolyline()
            if use_snapping:
                node_start_feat, node_end_feat = find_line_endpoints_nodes(polyline, locator, snapping_distance)
                if node_start_feat:
                    node_start_point = node_start_feat.geometry().asPoint()
                    polyline[0] = node_start_point
                    new_structure_feat["connection_node_start_id"] = node_start_feat["id"]
                    new_geom = QgsGeometry.fromPolylineXY(polyline)
                else:
                    if create_connection_nodes:
                        node_start_point = polyline[0]
                        new_start_node_feat = QgsFeature(node_fields)
                        new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                        new_start_node_feat["id"] = next_connection_node_id

                        new_structure_feat["connection_node_start_id"] = next_connection_node_id
                        next_connection_node_id += 1
                        new_nodes.append(new_start_node_feat)
                if node_end_feat:
                    node_end_point = node_end_feat.geometry().asPoint()
                    polyline[-1] = node_end_point
                    new_structure_feat["connection_node_end_id"] = node_end_feat["id"]
                    new_geom = QgsGeometry.fromPolylineXY(polyline)
                else:
                    if create_connection_nodes:
                        node_end_point = polyline[-1]
                        new_end_node_feat = QgsFeature(node_fields)
                        new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                        new_end_node_feat["id"] = next_connection_node_id
                        new_structure_feat["connection_node_end_id"] = next_connection_node_id
                        next_connection_node_id += 1
                        new_nodes.append(new_end_node_feat)
            else:
                if create_connection_nodes:
                    node_start_point = polyline[0]
                    new_start_node_feat = QgsFeature(node_fields)
                    new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                    new_start_node_feat["id"] = next_connection_node_id
                    new_structure_feat["connection_node_start_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    node_end_point = polyline[-1]
                    new_end_node_feat = QgsFeature(node_fields)
                    new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                    new_end_node_feat["id"] = next_connection_node_id
                    new_structure_feat["connection_node_end_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes += [new_start_node_feat, new_end_node_feat]
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, src_feat, *new_nodes)
                self.node_layer.addFeatures(new_nodes)
                locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            new_structure_feat.setGeometry(new_geom)
            self.update_attributes(self.structure_model_cls, src_feat, new_structure_feat)
            next_structure_id += 1
            new_structures.append(new_structure_feat)
        commit_errors = []
        success = self.node_layer.commitChanges()
        if not success:
            commit_errors += self.node_layer.commitErrors()
        self.structure_layer.addFeatures(new_structures)
        success = self.structure_layer.commitChanges()
        if not success:
            commit_errors += self.structure_layer.commitErrors()
        return success, commit_errors


class CulvertsImporter(ExternalFeaturesImporter):
    """Class with methods responsible for the importing culverts from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Culvert, structure_layer, node_layer)


class OrificesImporter(ExternalFeaturesImporter):
    """Class with methods responsible for the importing orifices from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Orifice, structure_layer, node_layer)


class WeirsImporter(ExternalFeaturesImporter):
    """Class with methods responsible for the importing weirs from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Weir, structure_layer, node_layer)
