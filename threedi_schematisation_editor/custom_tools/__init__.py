# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict, namedtuple
from enum import Enum
from itertools import chain
from operator import attrgetter

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
    enum_entry_name_format,
    find_line_endpoints_nodes,
    find_point_nodes,
    get_features_by_expression,
    get_next_feature_id,
    gpkg_layer,
    is_optional,
    optional_type,
    spatial_index,
)


class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    EXPRESSION = "expression"
    IGNORE = "ignore"

    def __str__(self):
        return self.name.capitalize()


class StructuresImportConfig:
    """Structures import tool configuration class."""

    FIELD_NAME_COLUMN_IDX = 0
    METHOD_COLUMN_IDX = 1
    SOURCE_ATTRIBUTE_COLUMN_IDX = 2
    VALUE_MAP_COLUMN_IDX = 3
    DEFAULT_VALUE_COLUMN_IDX = 4
    EXPRESSION_COLUMN_IDX = 5

    def __init__(self, structures_model_cls):
        self.structures_model_cls = structures_model_cls
        self.nodes_model_cls = dm.ConnectionNode
        self.related_models_classes = set()

    def add_related_model_class(self, model_cls):
        self.related_models_classes.add(model_cls)

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
        expression_context = QgsExpressionContext()
        expression_context.setFeature(source_feat)
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
                elif method == ColumnImportMethod.EXPRESSION:
                    expression_str = field_config["expression"]
                    expression = QgsExpression(expression_str)
                    new_feat[field_name] = expression.evaluate(expression_context)
                elif method == ColumnImportMethod.DEFAULT:
                    default_value = field_config["default_value"]
                    new_feat[field_name] = default_value
                else:
                    new_feat[field_name] = NULL

    @staticmethod
    def process_commit_errors(layer):
        commit_errors = layer.commitErrors()
        commit_errors_message = "\n".join(commit_errors)
        return commit_errors_message

    def new_structure_geometry(self, src_structure_feat):
        """Create new structure geometry based on the source structure feature."""
        raise NotImplementedError("Function called from the abstract class.")

    def process_structure_feature(self, *args, **kwargs):
        """Process source structure feature."""
        raise NotImplementedError("Function called from the abstract class.")

    def process_structure_features(self, *args, **kwargs):
        """Process source structure features."""
        raise NotImplementedError("Function called from the abstract class.")

    def import_structures(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        raise NotImplementedError("Function called from the abstract class.")


class WeldingFeaturesImporter(AbstractFeaturesImporter):
    INTERSECTION_BUFFER = 0.1
    INTERSECTION_BUFFER_SEGMENTS = 5
    DEFAULT_STRUCTURE_LENGTH = 10.0
    STRUCTURE_LENGTH_FIELD = "length"
    COMMIT_IMMEDIATELY = False

    def __init__(self, *args):
        super().__init__(*args)
        self.manhole_layer = None
        self.channel_layer = None
        self.cross_section_location_layer = None
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        self.spatial_indexes_map = {}
        self.node_by_location = {}
        self.next_node_id = 0
        self.features_to_add = defaultdict(list)
        self.channel_structure_cls = namedtuple("channel_structure", ["channel_id", "feature", "m", "length"])

    def setup_target_layers(
        self,
        structure_model_cls,
        structure_layer=None,
        node_layer=None,
        manhole_layer=None,
        channel_layer=None,
        cross_section_location_layer=None,
    ):
        super().setup_target_layers(structure_model_cls, structure_layer, node_layer)
        self.manhole_layer = (
            gpkg_layer(self.target_gpkg, dm.Manhole.__tablename__) if manhole_layer is None else manhole_layer
        )
        self.channel_layer = (
            gpkg_layer(self.target_gpkg, dm.Channel.__tablename__) if channel_layer is None else channel_layer
        )
        self.cross_section_location_layer = (
            gpkg_layer(self.target_gpkg, dm.CrossSectionLocation.__tablename__)
            if cross_section_location_layer is None
            else cross_section_location_layer
        )
        self.fields_configurations[dm.Manhole] = self.import_settings.get("manhole_fields", {})
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    def setup_fields_map(self):
        self.layer_fields_mapping.clear()
        for layer in [self.structure_layer, self.node_layer, self.channel_layer, self.cross_section_location_layer]:
            layer_name = layer.name()
            layer_fields = layer.fields()
            self.layer_fields_mapping[layer_name] = layer_fields
            self.layer_field_names_mapping[layer_name] = [field.name() for field in layer_fields.toList()]

    def setup_spatial_indexes(self):
        self.spatial_indexes_map.clear()
        for layer in [self.external_source, self.node_layer, self.cross_section_location_layer]:
            self.spatial_indexes_map[layer.name()] = spatial_index(layer)

    def setup_node_by_location(self):
        self.node_by_location.clear()
        for node_feat in self.node_layer.getFeatures():
            node_geom = node_feat.geometry()
            node_point = node_geom.asPoint()
            self.node_by_location[node_point] = node_feat["id"]
        self.next_node_id = get_next_feature_id(self.node_layer)

    def get_channel_structures_data(self, channel_feat):
        channel_structures = []
        channel_id = channel_feat["id"]
        channel_geometry = channel_feat.geometry()
        structure_layer_name = self.structure_layer.name()
        structure_features_map, structure_index = self.spatial_indexes_map[structure_layer_name]
        structure_fids = structure_index.intersects(channel_geometry.boundingBox())
        for structure_fid in structure_fids:
            structure_feat = structure_features_map[structure_fid]
            structure_geom = structure_feat.geometry()
            structure_geom_type = structure_geom.type()
            if structure_geom_type == QgsWkbTypes.GeometryType.LineGeometry:
                start_point, end_point = structure_geom.asPolyline()
                start_geom, end_geom = QgsGeometry.fromPointXY(start_point), QgsGeometry.fromPointXY(end_point)
                start_buffer = start_geom.buffer(self.INTERSECTION_BUFFER, self.INTERSECTION_BUFFER_SEGMENTS)
                end_buffer = end_geom.buffer(self.INTERSECTION_BUFFER, self.INTERSECTION_BUFFER_SEGMENTS)
                intersection_m = channel_geometry.lineLocatePoint(structure_geom.centroid())
                structure_length = structure_geom.length()
                if not all([start_buffer.intersects(channel_geometry), end_buffer.intersects(channel_geometry)]):
                    continue
            elif structure_geom_type == QgsWkbTypes.GeometryType.PointGeometry:
                structure_buffer = structure_geom.buffer(self.INTERSECTION_BUFFER, self.INTERSECTION_BUFFER_SEGMENTS)
                if not structure_buffer.intersects(channel_geometry):
                    continue
                intersection_m = channel_geometry.lineLocatePoint(structure_geom)
                structure_length = getattr(structure_feat, self.STRUCTURE_LENGTH_FIELD, self.DEFAULT_STRUCTURE_LENGTH)
            else:
                continue
            channel_structure = self.channel_structure_cls(channel_id, structure_feat, intersection_m, structure_length)
            channel_structures.append(channel_structure)
        channel_structures.sort(key=attrgetter("m"))
        return channel_structures

    def update_feature_endpoints(self, dst_feature, **template_node_attributes):
        added_nodes = []
        linear_geom = dst_feature.geometry()
        channel_polyline = linear_geom.asPolyline()
        start_node_point, end_node_point = channel_polyline[0], channel_polyline[-1]
        node_layer_name = self.node_layer.name()
        try:
            start_node_id = self.node_by_location[start_node_point]
        except KeyError:
            start_node_id = self.next_node_id
            start_node_feat = QgsFeature(self.layer_fields_mapping[node_layer_name])
            start_node = QgsGeometry.fromPointXY(start_node_point)
            start_node_feat.setGeometry(start_node)
            for field_name, field_value in template_node_attributes.items():
                start_node_feat[field_name] = field_value
            start_node_feat["fid"] = start_node_id
            start_node_feat["id"] = start_node_id
            self.next_node_id += 1
            self.node_by_location[start_node_point] = start_node_id
            self.features_to_add[node_layer_name].append(start_node_feat)
            added_nodes.append(start_node_feat)
        try:
            end_node_id = self.node_by_location[end_node_point]
        except KeyError:
            end_node_id = self.next_node_id
            end_node_feat = QgsFeature(self.layer_fields_mapping[node_layer_name])
            end_node = QgsGeometry.fromPointXY(end_node_point)
            end_node_feat.setGeometry(end_node)
            for field_name, field_value in template_node_attributes.items():
                end_node_feat[field_name] = field_value
            end_node_feat["fid"] = end_node_id
            end_node_feat["id"] = end_node_id
            self.next_node_id += 1
            self.node_by_location[end_node_point] = end_node_id
            self.features_to_add[node_layer_name].append(end_node_feat)
            added_nodes.append(end_node_feat)
        dst_feature["connection_node_start_id"] = start_node_id
        dst_feature["connection_node_end_id"] = end_node_id
        return added_nodes

    def update_channel_cross_section_references(self, channels):
        xs_location_layer_name = self.cross_section_location_layer.name()
        xs_location_features_map, xs_location_index = self.spatial_indexes_map[xs_location_layer_name]
        xs_fields = self.layer_fields_mapping[xs_location_layer_name]
        channel_id_idx = xs_fields.lookupField("channel_id")
        for channel_feat in channels:
            channel_id = channel_feat["id"]
            channel_code = channel_feat["code"]
            channel_geometry = channel_feat.geometry()
            xs_fids = xs_location_index.intersects(channel_geometry.boundingBox())
            for xs_fid in xs_fids:
                xs_feat = xs_location_features_map[xs_fid]
                xs_code = xs_feat["code"]
                if not xs_code.startswith(channel_code):
                    continue
                xs_geom = xs_feat.geometry()
                xs_buffer = xs_geom.buffer(self.INTERSECTION_BUFFER, self.INTERSECTION_BUFFER_SEGMENTS)
                if channel_geometry.intersects(xs_buffer):
                    self.cross_section_location_layer.changeAttributeValue(xs_fid, channel_id_idx, channel_id)

    @staticmethod
    def substring_feature(curve, start_distance, end_distance, fields, simplify=False, **attributes):
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

    def process_structure_features(self, channel_feat, channel_structures):
        channel_layer_name = self.channel_layer.name()
        channel_fields = self.layer_fields_mapping[channel_layer_name]
        channel_field_names = self.layer_field_names_mapping[channel_layer_name]
        channel_attributes = {field_name: channel_feat[field_name] for field_name in channel_field_names}
        del channel_attributes["fid"]
        channel_geom = channel_feat.geometry()
        channel_polyline = channel_geom.asPolyline()
        first_point = channel_polyline[0]
        first_node_id = self.node_by_location[first_point]
        first_node_feat = next(get_features_by_expression(self.node_layer, f'"id" = {first_node_id}'))
        node_field_names = self.layer_field_names_mapping[self.node_layer.name()]
        node_attributes = {field_name: first_node_feat[field_name] for field_name in node_field_names}
        channel_curve = channel_geom.constGet()
        before_substring_start, before_substring_end = 0, 0
        simplify_structure_geometry = self.structure_model_cls != dm.Culvert
        structure_fields = self.layer_fields_mapping[self.structure_model_cls.__layername__]
        structure_field_names = self.layer_field_names_mapping[self.structure_model_cls.__layername__]
        for channel_structure in channel_structures:
            added_nodes = []
            src_structure_feat = channel_structure.feature
            structure_feat = QgsFeature(structure_fields)
            # Update with values from the widgets.
            self.update_attributes(self.structure_model_cls, src_structure_feat, structure_feat)
            structure_attributes = {field_name: structure_feat[field_name] for field_name in structure_field_names}
            del structure_attributes["fid"]
            structure_length = channel_structure.length
            half_length = structure_length * 0.5
            structure_m = channel_structure.m
            start_distance = structure_m - half_length
            end_distance = structure_m + half_length
            # Setup structure feature
            substring_feat = self.substring_feature(
                channel_curve,
                start_distance,
                end_distance,
                structure_fields,
                simplify_structure_geometry,
                **structure_attributes,
            )
            added_nodes += self.update_feature_endpoints(substring_feat, **node_attributes)
            self.features_to_add[self.structure_model_cls.__layername__].append(substring_feat)
            # Setup channel leftover feature
            before_substring_end = start_distance
            before_substring_feat = self.substring_feature(
                channel_curve, before_substring_start, before_substring_end, channel_fields, False, **channel_attributes
            )
            added_nodes += self.update_feature_endpoints(before_substring_feat, **node_attributes)
            self.features_to_add[channel_layer_name].append(before_substring_feat)
            before_substring_start = end_distance
            if added_nodes:
                self.update_attributes(dm.ConnectionNode, src_structure_feat, *added_nodes)
        # Setup last channel leftover feature
        last_substring_end = channel_geom.length()
        if last_substring_end - before_substring_start > 0:
            last_substring_feat = self.substring_feature(
                channel_curve, before_substring_start, last_substring_end, channel_fields, False, **channel_attributes
            )
            self.update_feature_endpoints(last_substring_feat, **node_attributes)
            self.features_to_add[channel_layer_name].append(last_substring_feat)

    def import_structures(self, context=None, selected_ids=None):
        processed_structure_ids = set()
        for channel_feature in self.channel_layer.getFeatures():
            channel_structures, processed_channel_structures_ids = self.get_channel_structures_data(channel_feature)
            self.process_structure_features(channel_feature, channel_structures)
            processed_structure_ids |= processed_channel_structures_ids
        # Process nodes
        self.node_layer.startEditing()
        self.node_layer.addFeatures(self.features_to_add[self.node_layer.name()])
        if self.COMMIT_IMMEDIATELY:
            success = self.node_layer.commitChanges()
            if not success:
                return self.process_commit_errors(self.node_layer)
        # Process channels
        next_channel_id = get_next_feature_id(self.channel_layer)
        self.channel_layer.startEditing()
        visited_channel_ids = set()
        channels_to_add = []
        for channel_feat in self.features_to_add[self.channel_layer.name()]:
            channel_id = channel_feat["id"]
            if channel_id not in visited_channel_ids:
                source_channel_feat = next(get_features_by_expression(self.channel_layer, f'"id" = {channel_id}'))
                self.channel_layer.deleteFeature(source_channel_feat.id())
                visited_channel_ids.add(channel_id)
                channel_feat["fid"] = source_channel_feat["fid"]
                channel_feat["id"] = source_channel_feat["id"]
            else:
                channel_feat["fid"] = next_channel_id
                channel_feat["id"] = next_channel_id
                next_channel_id += 1
            channels_to_add.append(channel_feat)
        self.channel_layer.addFeatures(channels_to_add)
        if self.COMMIT_IMMEDIATELY:
            success = self.channel_layer.commitChanges()
            if not success:
                return self.process_commit_errors(self.channel_layer)
        # Update cross-section location features
        self.cross_section_location_layer.startEditing()
        self.update_channel_cross_section_references(channels_to_add)
        if self.COMMIT_IMMEDIATELY:
            success = self.cross_section_location_layer.commitChanges()
            if not success:
                return self.process_commit_errors(self.cross_section_location_layer)
        # Process structures
        structures_to_add = []
        for structure_id, structure_feat in enumerate(
            self.features_to_add[self.structure_model_cls.__layername__], start=1
        ):
            structure_feat["fid"] = structure_id
            structure_feat["id"] = structure_id
            structures_to_add.append(structure_feat)
        self.structure_layer.startEditing()
        self.structure_layer.addFeatures(structures_to_add)
        if self.COMMIT_IMMEDIATELY:
            success = self.structure_layer.commitChanges()
            if not success:
                return self.process_commit_errors(self.structure_layer)
        return ""


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
