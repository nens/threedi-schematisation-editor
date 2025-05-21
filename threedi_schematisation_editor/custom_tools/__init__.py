# Copyright (C) 2025 by Lutra Consulting
import warnings

from collections import defaultdict, namedtuple
from enum import Enum
from functools import cached_property
from itertools import chain
from operator import attrgetter, itemgetter

from qgis.core import (
    NULL,
    QgsCoordinateTransform,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsGeometry,
    QgsPointLocator,
    QgsProject,
    QgsWkbTypes,
)


from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import (
    convert_to_type,
    enum_entry_name_format,
    find_line_endpoints_nodes,
    find_point_nodes,
    get_features_by_expression,
    get_next_feature_id,
    gpkg_layer,
    is_optional,
    optional_type,
    spatial_index,
    TypeConversionError
)

from threedi_schematisation_editor.warnings import FeaturesImporterWarning, StructuresIntegratorWarning


class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    EXPRESSION = "expression"
    IGNORE = "ignore"

    def __str__(self):
        return self.name.capitalize()


class FeaturesImportConfig:
    """Features import tool configuration class."""

    FIELD_NAME_COLUMN_IDX = 0
    METHOD_COLUMN_IDX = 1
    SOURCE_ATTRIBUTE_COLUMN_IDX = 2
    VALUE_MAP_COLUMN_IDX = 3
    DEFAULT_VALUE_COLUMN_IDX = 4
    EXPRESSION_COLUMN_IDX = 5

    def __init__(self, import_model_cls):
        self.import_model_cls = import_model_cls

    @property
    def config_header(self):
        header = ["Field name", "Method", "Source attribute", "Value map", "Default value", "Expression"]
        return header

    @property
    def config_keys(self):
        header = ["method", "source_attribute", "value_map", "default_value", "expression"]
        return header

    @property
    def models_fields_iterator(self):
        fields_iterator = ((k, self.import_model_cls) for k in self.import_model_cls.__annotations__.keys())
        return fields_iterator

    @property
    def field_methods_mapping(self):
        methods_mapping = defaultdict(dict)
        auto_fields = {"id"}
        auto_attribute_fields = {"connection_node_id", "connection_node_id_start", "connection_node_id_end"}
        for field_name, model_cls in self.models_fields_iterator:
            if field_name in auto_fields:
                methods_mapping[model_cls][field_name] = [ColumnImportMethod.AUTO]
            elif field_name in auto_attribute_fields:
                methods_mapping[model_cls][field_name] = [
                    ColumnImportMethod.AUTO,
                    ColumnImportMethod.ATTRIBUTE,
                    ColumnImportMethod.EXPRESSION,
                ]
            else:
                methods_mapping[model_cls][field_name] = [
                    ColumnImportMethod.ATTRIBUTE,
                    ColumnImportMethod.DEFAULT,
                    ColumnImportMethod.EXPRESSION,
                    ColumnImportMethod.IGNORE,
                ]
        return methods_mapping

    def data_model_widgets(self):
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
                    elif column_idx == self.EXPRESSION_COLUMN_IDX:
                        widget = QgsFieldExpressionWidget()
                    else:
                        if column_idx == self.DEFAULT_VALUE_COLUMN_IDX and (
                            issubclass(field_type, Enum) or field_type == bool
                        ):
                            widget = QComboBox()
                            items = (
                                [["False", False], ["True", True]]
                                if field_type == bool
                                else [["NULL", "NULL"]] + [[enum_entry_name_format(e), e.value] for e in field_type]
                            )
                            for item_str, item_data in items:
                                widget.addItem(item_str, item_data)
                        else:
                            widget = QLineEdit()
                    widgets_to_add[model_cls][row_idx, column_idx] = widget
                row_idx += 1
        return widgets_to_add


class StructuresImportConfig(FeaturesImportConfig):
    """Structures import tool configuration class."""

    def __init__(self, import_model_cls):
        super().__init__(import_model_cls)
        self.nodes_model_cls = dm.ConnectionNode
        self.related_models_classes = set()

    def add_related_model_class(self, model_cls):
        self.related_models_classes.add(model_cls)

    @property
    def models_fields_iterator(self):
        structure_fields = ((k, self.import_model_cls) for k in self.import_model_cls.__annotations__.keys())
        node_fields = ((k, self.nodes_model_cls) for k in self.nodes_model_cls.__annotations__.keys())
        related_models_fields = (
            (k, model_cls) for model_cls in self.related_models_classes for k in model_cls.__annotations__.keys()
        )
        fields_iterator = chain(structure_fields, node_fields, related_models_fields)
        return fields_iterator


class AbstractFeaturesImporter:
    """Base class for the importing features from the external data source."""

    def __init__(self, external_source, target_gpkg, import_settings):
        self.external_source = external_source
        self.target_gpkg = target_gpkg
        self.import_settings = import_settings
        self.target_model_cls = None
        self.target_layer = None
        self.target_layer_name = None
        self.fields_configurations = {}

    @cached_property
    def external_source_name(self):
        try:
            layer_name = self.external_source.name()
        except AttributeError:
            layer_name = self.external_source.sourceName()
        return layer_name

    def setup_target_layers(self, target_model_cls, target_layer=None):
        self.target_model_cls = target_model_cls
        self.target_layer = (
            gpkg_layer(self.target_gpkg, target_model_cls.__tablename__) if target_layer is None else target_layer
        )
        self.target_layer_name = self.target_layer.name()
        self.fields_configurations = {target_model_cls: self.import_settings.get("fields", {})}

    def update_attributes(self, model_cls, source_feat, *new_features):
        fields_config = self.fields_configurations[model_cls]
        expression_context = QgsExpressionContext()
        expression_context.setFeature(source_feat)
        type_annotations = model_cls.__annotations__
        for new_feat in new_features:
            for field_name, field_type in type_annotations.items():
                try:
                    field_config = fields_config[field_name]
                except KeyError:
                    continue
                method = ColumnImportMethod(field_config["method"])
                if method == ColumnImportMethod.AUTO:
                    continue
                field_value = NULL
                if method == ColumnImportMethod.ATTRIBUTE:
                    src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
                    src_value = source_feat[src_field_name]
                    value_map = field_config.get("value_map", {})
                    field_value = value_map.get(src_value, src_value)
                    if field_value == NULL:
                        field_value = field_config.get("default_value", NULL)
                elif method == ColumnImportMethod.EXPRESSION:
                    expression_str = field_config["expression"]
                    expression = QgsExpression(expression_str)
                    field_value = expression.evaluate(expression_context)
                elif method == ColumnImportMethod.DEFAULT:
                    field_value = field_config["default_value"]
                try:
                    new_feat[field_name] = convert_to_type(field_value, field_type)
                except TypeConversionError as e:
                    new_feat[field_name] = NULL
                    feat_id = new_feat["id"]
                    message = f"Attribute {field_name} of feature with id {feat_id} in layer {self.target_layer_name} was not filled in"
                    warnings.warn(f"{message}. {e}", FeaturesImporterWarning)

    @staticmethod
    def process_commit_errors(layer):
        commit_errors = layer.commitErrors()
        commit_errors_message = "\n".join(commit_errors)
        return commit_errors_message

    def commit_pending_changes(self):
        for layer in self.modifiable_layers:
            if layer.isModified():
                layer.commitChanges()

    @property
    def modifiable_layers(self):
        """Return a list of the layers that can be modified."""
        return [self.target_layer]

    @staticmethod
    def new_point_geometry(src_feat):
        """Create a new point feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_point = src_geometry.asPoint()
        dst_point = src_point
        dst_geometry = QgsGeometry.fromPointXY(dst_point)
        return dst_geometry

    @staticmethod
    def new_polyline_geometry(src_feat):
        """Create a new polyline feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_polyline = src_geometry.asPolyline()
        dst_polyline = src_polyline
        dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        return dst_geometry

    @staticmethod
    def new_polygon_geometry(src_feat):
        """Create a new polygon feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_polygon = src_geometry.asPolygon()
        dst_polygon = src_polygon
        dst_geometry = QgsGeometry.fromPolygonXY(dst_polygon)
        return dst_geometry


class AbstractStructuresImporter(AbstractFeaturesImporter):
    """Base class for the importing structure features from the external data source."""

    DEFAULT_INTERSECTION_BUFFER = 1
    DEFAULT_INTERSECTION_BUFFER_SEGMENTS = 5

    def __init__(self, external_source, target_gpkg, import_settings):
        super().__init__(external_source, target_gpkg, import_settings)
        self.node_layer = None
        self.conversion_settings_cls = namedtuple(
            "conversion_settings",
            [
                "use_snapping",
                "snapping_distance",
                "create_connection_nodes",
                "length_source_field",
                "length_fallback_value",
                "azimuth_source_field",
                "azimuth_fallback_value",
                "edit_channels",
            ],
        )

    @cached_property
    def conversion_settings(self):
        conversion_config = self.import_settings["conversion_settings"]
        use_snapping = conversion_config.get("use_snapping", False)
        if use_snapping:
            snapping_distance = conversion_config.get("snapping_distance")
        else:
            snapping_distance = self.DEFAULT_INTERSECTION_BUFFER
        create_connection_nodes = conversion_config.get("create_connection_nodes", False)
        length_source_field = conversion_config.get("length_source_field", None)
        length_fallback_value = conversion_config.get("length_fallback_value", 10.0)
        azimuth_source_field = conversion_config.get("azimuth_source_field", None)
        azimuth_fallback_value = conversion_config.get("azimuth_fallback_value", 90.0)
        edit_channels = conversion_config.get("edit_channels", False)
        cs = self.conversion_settings_cls(
            use_snapping,
            snapping_distance,
            create_connection_nodes,
            length_source_field,
            length_fallback_value,
            azimuth_source_field,
            azimuth_fallback_value,
            edit_channels,
        )
        return cs

    def setup_target_layers(self, target_model_cls, target_layer=None, node_layer=None):
        self.target_model_cls = target_model_cls
        self.target_layer = (
            gpkg_layer(self.target_gpkg, target_model_cls.__tablename__) if target_layer is None else target_layer
        )
        self.target_layer_name = self.target_layer.name()
        self.node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__) if node_layer is None else node_layer
        )
        self.fields_configurations = {
            target_model_cls: self.import_settings.get("fields", {}),
            dm.ConnectionNode: self.import_settings.get("connection_node_fields", {}),
        }

    @property
    def modifiable_layers(self):
        """Return a list of the layers that can be modified."""
        return [self.target_layer, self.node_layer]

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        raise NotImplementedError("Function called from the abstract class.")

    def process_structure_feature(self, *args, **kwargs):
        """Process source structure feature."""
        raise NotImplementedError("Function called from the abstract class.")

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        raise NotImplementedError("Function called from the abstract class.")


class PointStructuresImporter(AbstractStructuresImporter):
    """Point structures importer class."""

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        return self.new_point_geometry(src_structure_feat)

    def process_structure_feature(
        self,
        src_feat,
        structure_fields,
        next_structure_id,
        node_fields,
        next_connection_node_id,
        locator,
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
        if self.conversion_settings.use_snapping:
            node_feat = find_point_nodes(
                point, self.node_layer, self.conversion_settings.snapping_distance, False, locator
            )
            if node_feat:
                node_point = node_feat.geometry().asPoint()
                new_geom = QgsGeometry.fromPointXY(node_point)
                new_structure_feat["connection_node_id"] = node_feat["id"]
            else:
                if self.conversion_settings.create_connection_nodes:
                    node_point = point
                    new_node_feat = QgsFeature(node_fields)
                    new_node_feat.setGeometry(QgsGeometry.fromPointXY(node_point))
                    new_node_feat["id"] = next_connection_node_id
                    new_structure_feat["connection_node_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes.append(new_node_feat)
        else:
            if self.conversion_settings.create_connection_nodes:
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
        structure_fields = self.target_layer.fields()
        node_fields = self.node_layer.fields()
        project = context.project() if context else QgsProject.instance()
        src_crs = self.external_source.sourceCrs()
        dst_crs = self.target_layer.crs()
        transform_ctx = project.transformContext()
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
        next_structure_id = get_next_feature_id(self.target_layer)
        next_connection_node_id = get_next_feature_id(self.node_layer)
        locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
        new_structures = []
        self.node_layer.startEditing()
        self.target_layer.startEditing()
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
                transformation,
            )
            new_structure_geom = new_structure_feat.geometry()
            if find_point_nodes(new_structure_geom.asPoint(), self.target_layer) is not None:
                continue
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, external_src_feat, *new_nodes)
                self.node_layer.addFeatures(new_nodes)
                locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            self.update_attributes(self.target_model_cls, external_src_feat, new_structure_feat)
            next_structure_id += 1
            new_structures.append(new_structure_feat)
        self.target_layer.addFeatures(new_structures)


class LinearStructuresImporter(AbstractStructuresImporter):
    """Linear structures importer class."""

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = QgsGeometry(src_structure_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        geometry_type = src_geometry.type()
        if geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
            src_polyline = src_geometry.asPolyline()
            dst_polyline = src_polyline if self.target_model_cls == dm.Culvert else [src_polyline[0], src_polyline[-1]]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        elif geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
            start_point = src_geometry.asPoint()
            length = (
                src_structure_feat[self.conversion_settings.length_source_field]
                if self.conversion_settings.length_source_field
                else self.conversion_settings.length_fallback_value
            )
            azimuth = (
                src_structure_feat[self.conversion_settings.azimuth_source_field]
                if self.conversion_settings.azimuth_source_field
                else self.conversion_settings.azimuth_fallback_value
            )
            end_point = start_point.project(length, azimuth)
            dst_polyline = [start_point, end_point]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        else:
            raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")
        return dst_geometry

    def process_structure_feature(
        self,
        src_feat,
        structure_fields,
        next_structure_id,
        node_fields,
        next_connection_node_id,
        locator,
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
        if self.conversion_settings.use_snapping:
            node_start_feat, node_end_feat = find_line_endpoints_nodes(
                polyline, locator, self.conversion_settings.snapping_distance
            )
            if node_start_feat:
                node_start_point = node_start_feat.geometry().asPoint()
                polyline[0] = node_start_point
                new_geom = QgsGeometry.fromPolylineXY(polyline)
                node_start_id = node_start_feat["id"]
                new_structure_feat["connection_node_id_start"] = node_start_id
            else:
                if self.conversion_settings.create_connection_nodes:
                    new_start_node_feat = QgsFeature(node_fields)
                    node_start_point = polyline[0]
                    new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                    new_node_start_id = next_connection_node_id
                    new_start_node_feat["id"] = new_node_start_id
                    new_structure_feat["connection_node_id_start"] = new_node_start_id
                    next_connection_node_id += 1
                    new_nodes.append(new_start_node_feat)
            if node_end_feat:
                node_end_point = node_end_feat.geometry().asPoint()
                polyline[-1] = node_end_point
                new_geom = QgsGeometry.fromPolylineXY(polyline)
                node_end_id = node_end_feat["id"]
                new_structure_feat["connection_node_id_end"] = node_end_id
            else:
                if self.conversion_settings.create_connection_nodes:
                    new_end_node_feat = QgsFeature(node_fields)
                    node_end_point = polyline[-1]
                    new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                    new_node_end_id = next_connection_node_id
                    new_end_node_feat["id"] = new_node_end_id
                    new_structure_feat["connection_node_id_end"] = new_node_end_id
                    next_connection_node_id += 1
                    new_nodes.append(new_end_node_feat)
        else:
            if self.conversion_settings.create_connection_nodes:
                new_start_node_feat = QgsFeature(node_fields)
                node_start_point = polyline[0]
                new_start_node_feat.setGeometry(QgsGeometry.fromPointXY(node_start_point))
                new_start_node_id = next_connection_node_id
                new_start_node_feat["id"] = new_start_node_id
                new_structure_feat["connection_node_id_start"] = new_start_node_id
                next_connection_node_id += 1
                new_end_node_feat = QgsFeature(node_fields)
                node_end_point = polyline[-1]
                new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                new_end_node_id = next_connection_node_id
                new_end_node_feat["id"] = new_end_node_id
                new_structure_feat["connection_node_id_end"] = new_end_node_id
                next_connection_node_id += 1
                new_nodes += [new_start_node_feat, new_end_node_feat]
        new_structure_feat.setGeometry(new_geom)
        return new_structure_feat, new_nodes, next_connection_node_id

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        structure_fields = self.target_layer.fields()
        node_fields = self.node_layer.fields()
        project = context.project() if context else QgsProject.instance()
        src_crs = self.external_source.sourceCrs()
        dst_crs = self.target_layer.crs()
        transform_ctx = project.transformContext()
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
        next_structure_id = get_next_feature_id(self.target_layer)
        next_connection_node_id = get_next_feature_id(self.node_layer)
        locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
        new_structures, external_source_structures = [], []
        self.node_layer.startEditing()
        self.target_layer.startEditing()
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
                transformation,
            )
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, external_src_feat, *new_nodes)
                self.node_layer.addFeatures(new_nodes)
                locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            self.update_attributes(self.target_model_cls, external_src_feat, new_structure_feat)
            next_structure_id += 1
            new_structures.append(new_structure_feat)
            external_source_structures.append(external_src_feat)
        self.target_layer.addFeatures(new_structures)


class StructuresIntegrator(LinearStructuresImporter):
    """External structures integrator class."""

    def __init__(self, *args):
        super().__init__(*args)
        self.channel_layer = None
        self.cross_section_location_layer = None
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        self.spatial_indexes_map = {}
        self.node_by_location = {}
        self.next_node_id = 0
        self.features_to_add = defaultdict(list)
        self.channel_structure_cls = namedtuple("channel_structure", ["channel_id", "feature", "m", "length"])

    @property
    def modifiable_layers(self):
        """Return a list of the layers that can be modified."""
        return super().modifiable_layers + [self.channel_layer, self.cross_section_location_layer]

    def setup_target_layers(
        self,
        target_model_cls,
        target_layer=None,
        node_layer=None,
        channel_layer=None,
        cross_section_location_layer=None,
    ):
        """Setup target layers with fields configuration."""
        super().setup_target_layers(target_model_cls, target_layer, node_layer)
        self.channel_layer = (
            gpkg_layer(self.target_gpkg, dm.Channel.__tablename__) if channel_layer is None else channel_layer
        )
        self.cross_section_location_layer = (
            gpkg_layer(self.target_gpkg, dm.CrossSectionLocation.__tablename__)
            if cross_section_location_layer is None
            else cross_section_location_layer
        )
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    def setup_fields_map(self):
        """Setup input layer fields map."""
        self.layer_fields_mapping.clear()
        for layer in [self.target_layer, self.node_layer, self.channel_layer, self.cross_section_location_layer]:
            layer_name = layer.name()
            layer_fields = layer.fields()
            self.layer_fields_mapping[layer_name] = layer_fields
            self.layer_field_names_mapping[layer_name] = [field.name() for field in layer_fields.toList()]

    def setup_spatial_indexes(self):
        """Setup input layer spatial indexes."""
        self.spatial_indexes_map.clear()
        self.spatial_indexes_map[self.external_source_name] = spatial_index(self.external_source)
        for layer in [self.node_layer, self.cross_section_location_layer]:
            layer_name = layer.name()
            self.spatial_indexes_map[layer_name] = spatial_index(layer)

    def setup_node_by_location(self):
        """Setup nodes by location."""
        self.node_by_location.clear()
        for node_feat in self.node_layer.getFeatures():
            node_geom = node_feat.geometry()
            node_point = node_geom.asPoint()
            self.node_by_location[node_point] = node_feat["id"]
        self.next_node_id = get_next_feature_id(self.node_layer)

    def get_channel_structures_data(self, channel_feat, selected_ids=None):
        """Extract and calculate channel structures data."""
        channel_structures = []
        processed_structure_ids = set()
        if selected_ids is None:
            selected_ids = set()
        channel_id = channel_feat["id"]
        channel_geometry = channel_feat.geometry()
        structure_features_map, structure_index = self.spatial_indexes_map[self.external_source_name]
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
                    self.conversion_settings.snapping_distance, self.DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                end_buffer = end_geom.buffer(
                    self.conversion_settings.snapping_distance, self.DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                intersection_m = channel_geometry.lineLocatePoint(structure_geom.centroid())
                structure_length = structure_geom.length()
                if not all([start_buffer.intersects(channel_geometry), end_buffer.intersects(channel_geometry)]):
                    continue
            elif structure_geom_type == QgsWkbTypes.GeometryType.PointGeometry:
                structure_buffer = structure_geom.buffer(
                    self.conversion_settings.snapping_distance, self.DEFAULT_INTERSECTION_BUFFER_SEGMENTS
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
        try:
            start_node_id = self.node_by_location[start_node_point]
        except KeyError:
            start_node_id = self.next_node_id
            start_node_feat = QgsFeature(node_layer_fields)
            start_node = QgsGeometry.fromPointXY(start_node_point)
            start_node_feat.setGeometry(start_node)
            for field_name, field_value in template_node_attributes.items():
                start_node_feat[field_name] = field_value
            start_node_feat["id"] = start_node_id
            self.next_node_id += 1
            self.node_by_location[start_node_point] = start_node_id
            self.features_to_add[node_layer_name].append(start_node_feat)
            new_nodes.append(start_node_feat)
        try:
            end_node_id = self.node_by_location[end_node_point]
        except KeyError:
            end_node_id = self.next_node_id
            end_node_feat = QgsFeature(node_layer_fields)
            end_node = QgsGeometry.fromPointXY(end_node_point)
            end_node_feat.setGeometry(end_node)
            for field_name, field_value in template_node_attributes.items():
                end_node_feat[field_name] = field_value
            end_node_feat["id"] = end_node_id
            self.next_node_id += 1
            self.node_by_location[end_node_point] = end_node_id
            self.features_to_add[node_layer_name].append(end_node_feat)
            new_nodes.append(end_node_feat)
        dst_feature["connection_node_id_start"] = start_node_id
        dst_feature["connection_node_id_end"] = end_node_id
        return new_nodes

    def update_channel_cross_section_references(self, new_channels, source_channel_xs_locations):
        """Update channel cross-section references."""
        xs_location_layer_name = self.cross_section_location_layer.name()
        xs_location_features_map, xs_location_index = self.spatial_indexes_map[xs_location_layer_name]
        xs_fields = self.layer_fields_mapping[xs_location_layer_name]
        channel_id_idx = xs_fields.lookupField("channel_id")
        next_cross_section_location_id = get_next_feature_id(self.cross_section_location_layer)
        cross_section_location_copies = []
        for src_channel_id, channels in new_channels.items():
            for channel_feat in channels:
                channel_xs_count = 0
                channel_id = channel_feat["id"]
                channel_geometry = channel_feat.geometry()
                channel_geometry_middle = channel_geometry.interpolate(channel_geometry.length() * 0.5)
                xs_fids = xs_location_index.intersects(channel_geometry.boundingBox())
                for xs_fid in xs_fids:
                    xs_feat = xs_location_features_map[xs_fid]
                    xs_geom = xs_feat.geometry()
                    xs_buffer = xs_geom.buffer(
                        self.DEFAULT_INTERSECTION_BUFFER, self.DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                    )
                    if channel_geometry.intersects(xs_buffer):
                        self.cross_section_location_layer.changeAttributeValue(xs_fid, channel_id_idx, channel_id)
                        channel_xs_count += 1
                if channel_xs_count == 0:
                    src_channel_xs_ids = [str(xs_id) for xs_id in source_channel_xs_locations[src_channel_id]]
                    if src_channel_xs_ids:
                        xs_ids_str = ",".join(src_channel_xs_ids)
                        xs_distance_map = [
                            (xs_feat, channel_geometry.distance(xs_feat.geometry()))
                            for xs_feat in get_features_by_expression(
                                self.cross_section_location_layer, f'"id" in ({xs_ids_str})', with_geometry=True
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
            self.cross_section_location_layer.addFeatures(cross_section_location_copies)

    def remove_hanging_cross_sections(self):
        """Remove cross-sections not aligned with the channels."""
        xs_leftovers = []
        channel_feats, channels_spatial_index = spatial_index(self.channel_layer)
        for xs_feat in self.cross_section_location_layer.getFeatures():
            xs_geom = xs_feat.geometry()
            xs_buffer = xs_geom.buffer(self.DEFAULT_INTERSECTION_BUFFER, self.DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
            channel_fids = channels_spatial_index.intersects(xs_buffer.boundingBox())
            xs_intersects = False
            for channel_fid in channel_fids:
                channel_feat = channel_feats[channel_fid]
                if xs_buffer.intersects(channel_feat.geometry()):
                    xs_intersects = True
                    break
            if not xs_intersects:
                xs_leftovers.append(xs_feat.id())
        if xs_leftovers:
            self.cross_section_location_layer.deleteFeatures(xs_leftovers)

    @staticmethod
    def substring_feature(curve, start_distance, end_distance, fields, simplify=False, **attributes):
        """Extract part of the curve as a new structure feature."""
        curve_substring = curve.curveSubstring(start_distance, end_distance)
        substring_feat = QgsFeature(fields)
        substring_geometry = QgsGeometry(curve_substring)
        if simplify:
            substring_polyline = substring_geometry.asPolyline()
            substring_geometry = QgsGeometry.fromPolylineXY([substring_polyline[0], substring_polyline[-1]])
        substring_feat.setGeometry(substring_geometry)
        for field_name, field_value in attributes.items():
            substring_feat[field_name] = field_value
        return substring_feat

    def integrate_structure_features(self, channel_feat, channel_structures):
        """Integrate structures with a channel network."""
        channel_layer_name = self.channel_layer.name()
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
        structure_fields = self.layer_fields_mapping[self.target_layer_name]
        structure_field_names = self.layer_field_names_mapping[self.target_layer_name]
        total_length = sum(channel_structure.length for channel_structure in channel_structures)
        if channel_geom.length() < total_length:
            id_str = ', '.join(str(channel_structure.feature.id()) for channel_structure in channel_structures)
            message = (f'Cannot integrate {self.target_model_cls.__tablename__}s with total length {total_length:.2f} '
                       f'into channel {channel_feat["id"]} with length {channel_geom.length():.2f}. '
                       f'Primary keys {self.target_model_cls.__tablename__}s: {id_str}')
            warnings.warn(f"{message}", StructuresIntegratorWarning)
            return
        for channel_structure in sorted(channel_structures, key=lambda x: x.m):
            new_nodes = []
            src_structure_feat = channel_structure.feature
            structure_feat = QgsFeature(structure_fields)
            # Update with values from the widgets.
            self.update_attributes(self.target_model_cls, src_structure_feat, structure_feat)
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
            substring_feat = self.substring_feature(
                channel_curve,
                start_distance,
                end_distance,
                structure_fields,
                simplify_structure_geometry,
                **structure_attributes,
            )
            new_nodes += self.update_feature_endpoints(substring_feat, **node_attributes)
            self.features_to_add[self.target_layer_name].append(substring_feat)
            # Setup channel leftover feature
            if start_distance > previous_structure_end:
                before_substring_feat = self.substring_feature(
                    channel_curve, previous_structure_end, start_distance, channel_fields, False, **channel_attributes
                )
                new_nodes += self.update_feature_endpoints(before_substring_feat, **node_attributes)
                self.features_to_add[channel_layer_name].append(before_substring_feat)
            previous_structure_end = end_distance
            if new_nodes:
                self.update_attributes(dm.ConnectionNode, src_structure_feat, *new_nodes)
        # Setup last channel leftover feature
        last_substring_end = channel_geom.length()
        if last_substring_end - previous_structure_end > 0:
            last_substring_feat = self.substring_feature(
                channel_curve, previous_structure_end, last_substring_end, channel_fields, False, **channel_attributes
            )
            self.update_feature_endpoints(last_substring_feat, **node_attributes)
            self.features_to_add[channel_layer_name].append(last_substring_feat)

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing/integrating structures from the external feature source."""
        all_processed_structure_ids = set()
        source_channel_xs_locations = defaultdict(set)
        input_feature_ids = (
            {feat.id() for feat in self.external_source.getFeatures()} if not selected_ids else set(selected_ids)
        )
        for channel_feature in self.channel_layer.getFeatures():
            channel_structures, processed_structures_fids = self.get_channel_structures_data(
                channel_feature, selected_ids
            )
            ch_id = channel_feature["id"]
            source_channel_xs_locations[ch_id] |= {
                xs["id"]
                for xs in get_features_by_expression(self.cross_section_location_layer, f'"channel_id" = {ch_id}')
            }
            if channel_structures:
                self.integrate_structure_features(channel_feature, channel_structures)
                all_processed_structure_ids |= processed_structures_fids
        # Process nodes
        self.node_layer.startEditing()
        self.node_layer.addFeatures(self.features_to_add[self.node_layer.name()])
        # Process channels
        next_channel_id = get_next_feature_id(self.channel_layer)
        self.channel_layer.startEditing()
        visited_channel_ids = set()
        channels_to_add = defaultdict(list)
        for channel_feat in self.features_to_add[self.channel_layer.name()]:
            channel_id = channel_feat["id"]
            if channel_id not in visited_channel_ids:
                source_channel_feat = next(get_features_by_expression(self.channel_layer, f'"id" = {channel_id}'))
                self.channel_layer.deleteFeature(source_channel_feat.id())
                visited_channel_ids.add(channel_id)
                channel_feat["id"] = source_channel_feat["id"]
            else:
                channel_feat["id"] = next_channel_id
                next_channel_id += 1
            channels_to_add[channel_id].append(channel_feat)
        self.channel_layer.addFeatures(list(chain.from_iterable(channels_to_add.values())))
        # Update cross-section location features
        self.cross_section_location_layer.startEditing()
        self.update_channel_cross_section_references(channels_to_add, source_channel_xs_locations)
        self.remove_hanging_cross_sections()
        # Process structures
        structures_to_add = []
        next_feature_id = get_next_feature_id(self.target_layer)
        for structure_feat in self.features_to_add[self.target_layer_name]:
            structure_feat["id"] = next_feature_id
            structures_to_add.append(structure_feat)
            next_feature_id += 1
        self.target_layer.startEditing()
        self.target_layer.addFeatures(structures_to_add)
        # Fallback import for disconnected structures.
        disconnected_structure_ids = list(input_feature_ids.difference(all_processed_structure_ids))
        if disconnected_structure_ids:
            disconnected_structures_to_add, external_source_structures = [], []
            structure_fields = self.layer_fields_mapping[self.target_layer_name]
            node_fields = self.layer_fields_mapping[self.node_layer.name()]
            project = context.project() if context else QgsProject.instance()
            src_crs = self.external_source.sourceCrs()
            dst_crs = self.target_layer.crs()
            transform_ctx = project.transformContext()
            transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
            next_structure_id = get_next_feature_id(self.target_layer)
            next_connection_node_id = get_next_feature_id(self.node_layer)
            locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
            for disconnected_structure in self.external_source.getFeatures(disconnected_structure_ids):
                new_structure_feat, new_nodes, next_connection_node_id = self.process_structure_feature(
                    disconnected_structure,
                    structure_fields,
                    next_structure_id,
                    node_fields,
                    next_connection_node_id,
                    locator,
                    transformation,
                )
                if new_nodes:
                    self.update_attributes(dm.ConnectionNode, disconnected_structure, *new_nodes)
                    self.node_layer.addFeatures(new_nodes)
                    locator = QgsPointLocator(self.node_layer, dst_crs, transform_ctx)
                self.update_attributes(self.target_model_cls, disconnected_structure, new_structure_feat)
                next_structure_id += 1
                disconnected_structures_to_add.append(new_structure_feat)
                external_source_structures.append(disconnected_structure)
            self.target_layer.addFeatures(disconnected_structures_to_add)


class CulvertsImporter(LinearStructuresImporter):
    """Class with methods responsible for the importing culverts from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Culvert, structure_layer, node_layer)


class CulvertsIntegrator(StructuresIntegrator):
    """Class with methods responsible for the integrating culverts from the external data source."""

    def __init__(
        self,
        *args,
        structure_layer=None,
        node_layer=None,
        channel_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(*args)
        self.setup_target_layers(dm.Culvert, structure_layer, node_layer, channel_layer, cross_section_location_layer)


class OrificesImporter(LinearStructuresImporter):
    """Class with methods responsible for the importing orifices from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Orifice, structure_layer, node_layer)


class OrificesIntegrator(StructuresIntegrator):
    """Class with methods responsible for the integrating orifices from the external data source."""

    def __init__(
        self,
        *args,
        structure_layer=None,
        node_layer=None,
        channel_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(*args)
        self.setup_target_layers(dm.Orifice, structure_layer, node_layer, channel_layer, cross_section_location_layer)


class WeirsImporter(LinearStructuresImporter):
    """Class with methods responsible for the importing weirs from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Weir, structure_layer, node_layer)


class WeirsIntegrator(StructuresIntegrator):
    """Class with methods responsible for the integrating weirs from the external data source."""

    def __init__(
        self,
        *args,
        structure_layer=None,
        node_layer=None,
        channel_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(*args)
        self.setup_target_layers(dm.Weir, structure_layer, node_layer, channel_layer, cross_section_location_layer)


class PipesImporter(LinearStructuresImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.Pipe, structure_layer, node_layer)


class ConnectionNodesImporter(AbstractFeaturesImporter):
    """Connection nodes importer class."""

    def __init__(self, *args, target_layer=None):
        super().__init__(*args)
        self.setup_target_layers(dm.ConnectionNode, target_layer)

    def process_feature(self, src_feat, target_fields, next_connection_node_id, transformation=None):
        """Process source point into connection node feature."""
        new_node_feat = QgsFeature(target_fields)
        new_node_feat["id"] = next_connection_node_id
        new_geom = self.new_point_geometry(src_feat)
        if transformation:
            new_geom.transform(transformation)
        new_node_feat.setGeometry(new_geom)
        return new_node_feat

    def import_features(self, context=None, selected_ids=None):
        """Method responsible for the importing connection nodes from the external feature source."""
        target_fields = self.target_layer.fields()
        project = context.project() if context else QgsProject.instance()
        src_crs = self.external_source.sourceCrs()
        dst_crs = self.target_layer.crs()
        transform_ctx = project.transformContext()
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
        next_feature_id = get_next_feature_id(self.target_layer)
        new_feats = []
        self.target_layer.startEditing()
        features_iterator = (
            self.external_source.getFeatures(selected_ids) if selected_ids else self.external_source.getFeatures()
        )
        for external_src_feat in features_iterator:
            new_feat = self.process_feature(
                external_src_feat,
                target_fields,
                next_feature_id,
                transformation,
            )
            self.update_attributes(self.target_model_cls, external_src_feat, new_feat)
            next_feature_id += 1
            new_feats.append(new_feat)
        self.target_layer.addFeatures(new_feats)
