# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict
from enum import Enum
from itertools import chain

from qgis.core import NULL, QgsCoordinateTransform, QgsFeature, QgsGeometry, QgsPointLocator, QgsProject
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    enum_entry_name_format,
    find_line_endpoints_nodes,
    find_point_nodes,
    get_features_by_expression,
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
        self.nodes_model_cls = dm.ConnectionNode
        self.related_models_classes = set()

    def add_related_model_class(self, model_cls):
        self.related_models_classes.add(model_cls)

    @property
    def config_header(self):
        header = ["Field name", "Method", "Source attribute", "Value map", "Default value"]
        return header

    @property
    def config_keys(self):
        header = ["method", "source_attribute", "value_map", "default_value"]
        return header

    @property
    def models_fields_iterator(self):
        structure_fields = ((k, self.structures_model_cls) for k in self.structures_model_cls.__annotations__.keys())
        node_fields = ((k, self.nodes_model_cls) for k in self.nodes_model_cls.__annotations__.keys())
        related_models_fields = (
            (k, model_cls) for model_cls in self.related_models_classes for k in model_cls.__annotations__.keys()
        )
        fields_iterator = chain(structure_fields, node_fields, related_models_fields)
        return fields_iterator

    @property
    def field_methods_mapping(self):
        methods_mapping = defaultdict(dict)
        auto_fields = {"id"}
        auto_attribute_fields = {"connection_node_id", "connection_node_start_id", "connection_node_end_id"}
        for field_name, model_cls in self.models_fields_iterator:
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
            model_obsolete_fields = model_cls.obsolete_fields()
            model_fields_display_names = model_cls.fields_display_names()
            row_idx = 0
            for field_name, field_methods in field_methods_mapping.items():
                if field_name in model_obsolete_fields:
                    continue
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
                row_idx += 1
        return widgets_to_add


class AbstractFeaturesImporter:
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
        self.structure_model_cls = structure_model_cls
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
        raise NotImplementedError("Function called from the abstract class.")

    def process_structure_feature(self, *args, **kwargs):
        """Process source structure feature."""
        raise NotImplementedError("Function called from the abstract class.")

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        raise NotImplementedError("Function called from the abstract class.")


class PointFeaturesImporter(AbstractFeaturesImporter):
    """Point features importer class."""

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = QgsGeometry(src_structure_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_point = src_geometry.asPoint()
        dst_point = src_point
        dst_geometry = QgsGeometry.fromPointXY(dst_point)
        return dst_geometry

    def process_structure_feature(
        self,
        src_feat,
        structure_fields,
        next_structure_id,
        node_fields,
        next_connection_node_id,
        locator,
        use_snapping,
        snapping_distance,
        create_connection_nodes=False,
        transformation=None,
    ):
        """Process source point structure feature."""
        new_nodes = []
        new_structure_feat = QgsFeature(structure_fields)
        new_structure_feat["id"] = next_structure_id
        new_geom = self.new_structure_geometry(src_feat)
        if transformation:
            new_geom.transform(transformation)
        point = new_geom.asPoint()
        if use_snapping:
            node_feat = find_point_nodes(point, self.node_layer, snapping_distance, False, locator)
            if node_feat:
                node_point = node_feat.geometry().asPoint()
                new_geom = QgsGeometry.fromPointXY(node_point)
                new_structure_feat["connection_node_id"] = node_feat["id"]
            else:
                if create_connection_nodes:
                    node_point = point
                    new_node_feat = QgsFeature(node_fields)
                    new_node_feat.setGeometry(QgsGeometry.fromPointXY(node_point))
                    new_node_feat["id"] = next_connection_node_id
                    new_structure_feat["connection_node_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes.append(new_node_feat)
        else:
            if create_connection_nodes:
                node_point = point
                new_node_feat = QgsFeature(node_fields)
                new_node_feat.setGeometry(QgsGeometry.fromPointXY(node_point))
                new_node_feat["id"] = next_connection_node_id
                new_structure_feat["connection_node_id"] = next_connection_node_id
                next_connection_node_id += 1
                new_nodes.append(new_node_feat)
        new_structure_feat.setGeometry(new_geom)
        return new_structure_feat, new_nodes, next_connection_node_id

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
        features_iterator = (
            self.external_source.getFeatures(selected_ids) if selected_ids else self.external_source.getFeatures()
        )
        for external_src_feat in features_iterator:
            new_structure_feat, new_nodes, next_connection_node_id = self.process_structure_feature(
                external_src_feat,
                structure_fields,
                next_structure_id,
                node_fields,
                next_connection_node_id,
                locator,
                use_snapping,
                snapping_distance,
                create_connection_nodes,
                transformation,
            )
            new_structure_geom = new_structure_feat.geometry()
            if find_point_nodes(new_structure_geom.asPoint(), self.structure_layer) is not None:
                continue
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, external_src_feat, *new_nodes)
                self.node_layer.addFeatures(new_nodes)
                locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            self.update_attributes(self.structure_model_cls, external_src_feat, new_structure_feat)
            next_structure_id += 1
            new_structures.append(new_structure_feat)
        self.structure_layer.addFeatures(new_structures)


class LinearFeaturesImporter(AbstractFeaturesImporter):
    """Linear features importer class."""

    def __init__(self, *args):
        super().__init__(*args)
        self.manhole_layer = None

    def setup_target_layers(self, structure_model_cls, structure_layer=None, node_layer=None, manhole_layer=None):
        """Setup target layers with fields configuration."""
        super().setup_target_layers(structure_model_cls, structure_layer, node_layer)
        self.manhole_layer = (
            gpkg_layer(self.target_gpkg, dm.Manhole.__tablename__) if manhole_layer is None else manhole_layer
        )
        self.fields_configurations[dm.Manhole] = self.import_settings.get("manhole_fields", {})

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = QgsGeometry(src_structure_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_polyline = src_geometry.asPolyline()
        dst_polyline = src_polyline if self.structure_model_cls == dm.Culvert else [src_polyline[0], src_polyline[-1]]
        dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        return dst_geometry

    def process_structure_feature(
        self,
        src_feat,
        structure_fields,
        next_structure_id,
        node_fields,
        next_connection_node_id,
        locator,
        use_snapping,
        snapping_distance,
        create_connection_nodes=False,
        transformation=None,
    ):
        """Process source linear structure feature."""
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
                new_geom = QgsGeometry.fromPolylineXY(polyline)
                node_start_id = node_start_feat["id"]
                new_structure_feat["connection_node_start_id"] = node_start_id
            else:
                if create_connection_nodes:
                    new_start_node_feat = QgsFeature(node_fields)
                    node_start_point = polyline[0]
                    new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                    new_node_start_id = next_connection_node_id
                    new_start_node_feat["id"] = new_node_start_id
                    new_structure_feat["connection_node_start_id"] = new_node_start_id
                    next_connection_node_id += 1
                    new_nodes.append(new_start_node_feat)
            if node_end_feat:
                node_end_point = node_end_feat.geometry().asPoint()
                polyline[-1] = node_end_point
                new_geom = QgsGeometry.fromPolylineXY(polyline)
                node_end_id = node_end_feat["id"]
                new_structure_feat["connection_node_end_id"] = node_end_id
            else:
                if create_connection_nodes:
                    new_end_node_feat = QgsFeature(node_fields)
                    node_end_point = polyline[-1]
                    new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                    new_node_end_id = next_connection_node_id
                    new_end_node_feat["id"] = new_node_end_id
                    new_structure_feat["connection_node_end_id"] = new_node_end_id
                    next_connection_node_id += 1
                    new_nodes.append(new_end_node_feat)
        else:
            if create_connection_nodes:
                new_start_node_feat = QgsFeature(node_fields)
                node_start_point = polyline[0]
                new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                new_start_node_id = next_connection_node_id
                new_start_node_feat["id"] = new_start_node_id
                new_structure_feat["connection_node_start_id"] = new_start_node_id
                next_connection_node_id += 1
                new_end_node_feat = QgsFeature(node_fields)
                node_end_point = polyline[-1]
                new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                new_end_node_id = next_connection_node_id
                new_end_node_feat["id"] = new_end_node_id
                new_structure_feat["connection_node_end_id"] = new_end_node_id
                next_connection_node_id += 1
                new_nodes += [new_start_node_feat, new_end_node_feat]
        new_structure_feat.setGeometry(new_geom)
        return new_structure_feat, new_nodes, next_connection_node_id

    def manholes_for_structures(self, external_source_features, new_structure_features):
        """Create manholes for the structures."""
        manhole_fields = self.manhole_layer.fields()
        next_manhole_id = get_next_feature_id(self.manhole_layer)
        manholes_at_nodes = {manhole_feat["connection_node_id"] for manhole_feat in self.manhole_layer.getFeatures()}
        new_manholes = []
        for external_src_feat, structure_feat in zip(external_source_features, new_structure_features):
            start_node_id = structure_feat["connection_node_start_id"]
            end_node_id = structure_feat["connection_node_end_id"]
            if start_node_id not in manholes_at_nodes:
                start_manhole_feat = QgsFeature(manhole_fields)
                start_node = next(get_features_by_expression(self.node_layer, f'"id" = {start_node_id}', True))
                start_node_point = start_node.geometry().asPoint()
                start_manhole_feat.setGeometry(QgsGeometry.fromPointXY(start_node_point))
                start_manhole_feat["id"] = next_manhole_id
                start_manhole_feat["connection_node_id"] = start_node_id
                self.update_attributes(dm.Manhole, external_src_feat, start_manhole_feat)
                new_manholes.append(start_manhole_feat)
                manholes_at_nodes.add(start_node_id)
                next_manhole_id += 1
            if end_node_id not in manholes_at_nodes:
                end_manhole_feat = QgsFeature(manhole_fields)
                end_node = next(get_features_by_expression(self.node_layer, f'"id" = {end_node_id}', True))
                end_node_point = end_node.geometry().asPoint()
                end_manhole_feat.setGeometry(QgsGeometry.fromPointXY(end_node_point))
                end_manhole_feat["id"] = next_manhole_id
                end_manhole_feat["connection_node_id"] = end_node_id
                self.update_attributes(dm.Manhole, external_src_feat, end_manhole_feat)
                new_manholes.append(end_manhole_feat)
                manholes_at_nodes.add(end_node_id)
                next_manhole_id += 1
        return new_manholes

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        conversion_settings = self.import_settings["conversion_settings"]
        use_snapping = conversion_settings.get("use_snapping", False)
        snapping_distance = conversion_settings.get("snapping_distance", 0.1)
        create_connection_nodes = conversion_settings.get("create_connection_nodes", False)
        create_manholes = conversion_settings.get("create_manholes", False)
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
        new_structures, external_source_structures = [], []
        self.node_layer.startEditing()
        self.structure_layer.startEditing()
        features_iterator = (
            self.external_source.getFeatures(selected_ids) if selected_ids else self.external_source.getFeatures()
        )
        for external_src_feat in features_iterator:
            new_structure_feat, new_nodes, next_connection_node_id = self.process_structure_feature(
                external_src_feat,
                structure_fields,
                next_structure_id,
                node_fields,
                next_connection_node_id,
                locator,
                use_snapping,
                snapping_distance,
                create_connection_nodes,
                transformation,
            )
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, external_src_feat, *new_nodes)
                self.node_layer.addFeatures(new_nodes)
                locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            self.update_attributes(self.structure_model_cls, external_src_feat, new_structure_feat)
            next_structure_id += 1
            new_structures.append(new_structure_feat)
            external_source_structures.append(external_src_feat)
        if create_manholes:
            self.manhole_layer.startEditing()
            new_manholes = self.manholes_for_structures(external_source_structures, new_structures)
            self.manhole_layer.addFeatures(new_manholes)
        self.structure_layer.addFeatures(new_structures)


class CulvertsImporter(LinearFeaturesImporter):
    """Class with methods responsible for the importing culverts from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None, manhole_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Culvert, structure_layer, node_layer, manhole_layer)


class OrificesImporter(LinearFeaturesImporter):
    """Class with methods responsible for the importing orifices from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None, manhole_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Orifice, structure_layer, node_layer, manhole_layer)


class WeirsImporter(LinearFeaturesImporter):
    """Class with methods responsible for the importing weirs from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None, manhole_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Weir, structure_layer, node_layer, manhole_layer)


class PipesImporter(LinearFeaturesImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None, manhole_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Pipe, structure_layer, node_layer, manhole_layer)


class ManholesImporter(PointFeaturesImporter):
    """Class with methods responsible for the importing manholes from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Manhole, structure_layer, node_layer)
