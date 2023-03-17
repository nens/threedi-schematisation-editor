# Copyright (C) 2023 by Lutra Consulting
import os
import shutil
import sys
from collections import OrderedDict
from enum import Enum
from itertools import groupby
from operator import attrgetter
from typing import Union
from uuid import uuid4

from qgis.core import (
    QgsBilinearRasterResampler,
    QgsCoordinateTransform,
    QgsDataSourceUri,
    QgsEditorWidgetSetup,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsHillshadeRenderer,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsMapLayer,
    QgsPointLocator,
    QgsProject,
    QgsRasterLayer,
    QgsRasterMinMaxOrigin,
    QgsValueMapFieldFormatter,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QObject, QSettings, QVariant
from qgis.PyQt.QtGui import QDoubleValidator, QPainter
from qgis.PyQt.QtWidgets import QFileDialog, QItemDelegate, QLineEdit
from qgis.utils import plugins, qgsfunction

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en

field_types_mapping = {
    bool: QVariant.Bool,
    int: QVariant.Int,
    float: QVariant.Double,
    str: QVariant.String,
}


def backup_sqlite(filename):
    """Make a backup of the sqlite database."""
    backup_folder = os.path.join(os.path.dirname(os.path.dirname(filename)), "_backup")
    os.makedirs(backup_folder, exist_ok=True)
    prefix = str(uuid4())[:8]
    backup_sqlite_path = os.path.join(backup_folder, f"{prefix}_{os.path.basename(filename)}")
    shutil.copyfile(filename, backup_sqlite_path)
    return backup_sqlite_path


def cast_if_bool(value):
    """Function for changing True/False from GeoPackage layers to 0/1 integers used in Spatialite layers."""
    if value is True:
        return 1
    elif value is False:
        return 0
    else:
        return value


def vector_layer_factory(annotated_model_cls, epsg=4326):
    """Function that creates memory layer based on annotated data model class."""
    fields = []
    geometry_type = annotated_model_cls.__geometrytype__.value
    layer_name = annotated_model_cls.__tablename__
    uri = f"{geometry_type}?crs=EPSG:{epsg}"
    layer = QgsVectorLayer(uri, layer_name, "memory")
    for field_name, field_type in annotated_model_cls.__annotations__.items():
        if is_optional(field_type):
            field_type = optional_type(field_type)
        if issubclass(field_type, Enum):
            field_type = enum_type(field_type)
        try:
            field_variant = field_types_mapping[field_type]
        except KeyError:
            raise NotImplementedError(f"Unsupported field type: {field_type}")
        field = QgsField(field_name, field_variant)
        fields.append(field)
    layer_dt = layer.dataProvider()
    layer_dt.addAttributes(fields)
    layer.updateFields()
    return layer


def is_optional(field_type):
    """Checking if field type is an Optional."""
    try:
        field_args = field_type.__args__
        field_origin = field_type.__origin__
    except AttributeError:
        return False
    if field_origin is Union:
        real_field_type, default = field_args
        none_type = type(None)
        if real_field_type is not none_type and default is none_type:
            return True
    return False


def optional_type(optional_field_type):
    """Getting real type of Optional field type."""
    field_type = next(iter(optional_field_type.__args__))
    return field_type


def enum_type(enum_field_type):
    """Getting real type of Enum field type."""
    field_type = type(next(iter(enum_field_type[i].value for i in enum_field_type.__members__)))
    return field_type


def layer_to_gpkg(layer, gpkg_filename, overwrite=False, driver_name="GPKG"):
    """Function which saves memory layer into GeoPackage file."""
    transform_context = QgsProject.instance().transformContext()
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.actionOnExistingFile = (
        QgsVectorFileWriter.CreateOrOverwriteLayer if overwrite is False else QgsVectorFileWriter.CreateOrOverwriteFile
    )
    fields = layer.fields()
    valid_indexes = [fields.lookupField(fname) for fname in fields.names() if fname != "fid"]
    options.attributes = valid_indexes
    options.driverName = driver_name
    options.layerName = layer.name()
    writer, error = QgsVectorFileWriter.writeAsVectorFormatV2(layer, gpkg_filename, transform_context, options)
    return writer, error


def gpkg_layer(gpkg_path, table_name, layer_name=None):
    """Creating vector layer out of GeoPackage source."""
    uri = f"{gpkg_path}|layername={table_name}"
    layer_name = table_name if layer_name is None else layer_name
    vlayer = QgsVectorLayer(uri, layer_name, "ogr")
    return vlayer


def sqlite_layer(sqlite_path, table_name, layer_name=None, geom_column="the_geom", schema=""):
    """Creating vector layer out of Spatialite source."""
    uri = QgsDataSourceUri()
    uri.setDatabase(sqlite_path)
    uri.setDataSource(schema, table_name, geom_column)
    layer_name = table_name if layer_name is None else layer_name
    vlayer = QgsVectorLayer(uri.uri(), layer_name, "spatialite")
    return vlayer


def create_empty_model(export_sqlite_path):
    """Copying Spatialite database template with 3Di model data structure."""
    empty_sqlite = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "empty.sqlite")
    shutil.copy(empty_sqlite, export_sqlite_path)


def get_qml_style_path(style_name, *subfolders):
    """Getting QML styles path."""
    qml_filename = f"{style_name}.qml"
    filepath = os.path.join(os.path.dirname(__file__), "styles", *subfolders, qml_filename)
    if os.path.isfile(filepath):
        return filepath
    return None


def get_multiple_qml_style_paths(styles_folder_name, *subfolders):
    """Getting QML styles paths within given styles folder."""
    styles_folder_path = os.path.join(os.path.dirname(__file__), "styles", *subfolders, styles_folder_name)
    if os.path.exists(styles_folder_path):
        qml_paths = [os.path.join(styles_folder_path, q) for q in os.listdir(styles_folder_path) if q.endswith(".qml")]
    else:
        qml_paths = []
    return qml_paths


def get_form_ui_path(table_name):
    """Getting UI form path for a given table name."""
    ui_filename = f"{table_name}.ui"
    filepath = os.path.join(os.path.dirname(__file__), "forms", "ui", ui_filename)
    if os.path.isfile(filepath):
        return filepath
    return None


def create_tree_group(name, insert_at_top=False, root=None):
    """Creating layer tree group with given name."""
    root = QgsProject.instance().layerTreeRoot() if root is None else root
    grp = QgsLayerTreeGroup(name)
    root.insertChildNode(0 if insert_at_top else -1, grp)
    return grp


def get_tree_group(name):
    """Getting layer tree group with given name."""
    root = QgsProject.instance().layerTreeRoot()
    grp = root.findGroup(name)
    return grp


def add_layer_to_group(name, layer, bottom=False, cached_groups=None):
    """Adding layer to the specific group."""
    project = QgsProject.instance()
    grp = cached_groups.get(name, None) if cached_groups else project.layerTreeRoot().findGroup(name)
    if not grp:
        return
    project.addMapLayer(layer, False)
    grp.insertChildNode(-1 if bottom else 0, QgsLayerTreeLayer(layer))


def remove_layer(layer):
    """Removing layer from the map canvas."""
    QgsProject.instance().removeMapLayer(layer)


def remove_group_with_children(name):
    """Removing group with all layers from the map canvas."""
    project = QgsProject.instance()
    root = project.layerTreeRoot()
    group = root.findGroup(name)
    if group is not None:
        group.removeAllChildren()
        root.removeChildNode(group)


def get_filepath(parent, extension_filter=None, extension=None, save=True, dialog_title=None):
    """Opening dialog to get a filepath."""
    if extension_filter is None:
        extension_filter = "All Files (*.*)"

    if dialog_title is None:
        dialog_title = "Choose file"

    starting_dir = QSettings().value("threedi_mb/last_folder", os.path.expanduser("~"), type=str)
    if save is True:
        file_name, __ = QFileDialog.getSaveFileName(parent, dialog_title, starting_dir, extension_filter)
    else:
        file_name, __ = QFileDialog.getOpenFileName(parent, dialog_title, starting_dir, extension_filter)
    if len(file_name) == 0:
        return None

    if extension:
        if not file_name.endswith(extension):
            file_name += extension

    QSettings().setValue("threedi_mb/last_folder", os.path.dirname(file_name))
    return file_name


def enum_to_editor_widget_setup(enum, optional=False, enum_name_format_fn=None):
    """Creating QgsEditorWidgetSetup out of the Enum object."""
    if enum_name_format_fn is None:

        def enum_name_format_fn(entry_name):
            return entry_name

    value_map = [{enum_name_format_fn(entry.name): entry.value} for entry in enum]
    if optional:
        null_value = QgsValueMapFieldFormatter.NULL_VALUE
        value_map.insert(0, {"": null_value})
    ews = QgsEditorWidgetSetup("ValueMap", {"map": value_map})
    return ews


def set_initial_layer_configuration(layer, model_cls):
    """Set initial vector layer configuration that should be set within currently active style."""
    attr_table_config = layer.attributeTableConfig()
    fields = layer.dataProvider().fields()
    columns = attr_table_config.columns()

    def enum_entry_name_format(entry_name):
        if entry_name != "YZ":
            formatted_entry_name = entry_name.capitalize().replace("_", " ")
        else:
            formatted_entry_name = entry_name
        return formatted_entry_name

    for column in columns:
        column_name = column.name
        if column_name == "fid":
            column.hidden = True
            continue
        try:
            field_type = model_cls.__annotations__[column_name]
            if is_optional(field_type):
                field_type = optional_type(field_type)
                optional = True
            else:
                optional = False
            if issubclass(field_type, Enum):
                field_idx = fields.lookupField(column_name)
                ews = enum_to_editor_widget_setup(field_type, optional, enum_name_format_fn=enum_entry_name_format)
                layer.setEditorWidgetSetup(field_idx, ews)
        except KeyError:
            continue
    attr_table_config.setColumns(columns)
    layer.setAttributeTableConfig(attr_table_config)
    layer.setFlags(QgsMapLayer.Searchable | QgsMapLayer.Identifiable)


def set_field_default_value(vector_layer, field_name, expression, apply_on_update=False):
    """Set default value expression for field under the given index."""
    field_index = vector_layer.fields().lookupField(field_name)
    default_value_definition = vector_layer.defaultValueDefinition(field_index)
    default_value_definition.setExpression(expression)
    default_value_definition.setApplyOnUpdate(apply_on_update)
    vector_layer.setDefaultValueDefinition(field_index, default_value_definition)


def load_user_layers(gpkg_path):
    """Loading grouped User Layers from GeoPackage into map canvas."""
    groups = OrderedDict()
    groups["1D"] = dm.MODEL_1D_ELEMENTS
    groups["2D"] = dm.MODEL_2D_ELEMENTS
    groups["Inflow"] = dm.INFLOW_ELEMENTS
    groups["Settings"] = dm.SETTINGS_ELEMENTS
    default_style_name = "default"
    for group_name, group_models in groups.items():
        get_tree_group(group_name)
        for model_cls in group_models:
            layer = gpkg_layer(gpkg_path, model_cls.__tablename__, model_cls.__layername__)
            fields_indexes = list(range(len(layer.fields())))
            form_ui_path = get_form_ui_path(model_cls.__tablename__)
            qml_paths = get_multiple_qml_style_paths(model_cls.__tablename__, "vector")
            qml_names = [os.path.basename(qml_path).split(".")[0] for qml_path in qml_paths]
            try:
                default_idx = qml_names.index(default_style_name)
                qml_paths.append(qml_paths.pop(default_idx))
                qml_names.append(qml_names.pop(default_idx))
            except ValueError:
                # There is no default.qml style defined for the model layer
                pass
            style_manager = layer.styleManager()
            for style_name, qml_path in zip(qml_names, qml_paths):
                layer.loadNamedStyle(qml_path)
                style_manager.addStyleFromLayer(style_name)
            all_styles = style_manager.styles()
            default_widgets_setup = [(idx, layer.editorWidgetSetup(idx)) for idx in fields_indexes]
            default_edit_form_config = layer.editFormConfig()
            if form_ui_path:
                default_edit_form_config.setUiForm(form_ui_path)
            else:
                id_increment_expression = "if (maximum(id) is null, 1, maximum(id) + 1)"
                set_field_default_value(layer, "id", id_increment_expression)
            for style in all_styles:
                style_manager.setCurrentStyle(style)
                layer.setEditFormConfig(default_edit_form_config)
                for field_idx, field_widget_setup in default_widgets_setup:
                    layer.setEditorWidgetSetup(field_idx, field_widget_setup)
            style_manager.setCurrentStyle(default_style_name)
            add_layer_to_group(group_name, layer, bottom=True)
    load_model_raster_layers(gpkg_path)


def load_model_raster_layers(gpkg_path):
    """Loading raster layers related with 3Di model."""
    gpkg_dir = os.path.dirname(gpkg_path)
    group_name = "Model rasters"
    get_tree_group(group_name)
    for settings_cls in dm.SETTINGS_ELEMENTS:
        if settings_cls.RELATED_RASTERS is None:
            continue
        settings_layer = gpkg_layer(gpkg_path, settings_cls.__tablename__)
        try:
            feat = next(settings_layer.getFeatures())
        except StopIteration:
            continue
        for raster_file_field, raster_layer_name in settings_cls.RELATED_RASTERS:
            relative_path = feat[raster_file_field]
            if not relative_path:
                continue
            raster_filepath = os.path.normpath(os.path.join(gpkg_dir, relative_path))
            if not os.path.isfile(raster_filepath):
                continue
            rlayer = QgsRasterLayer(raster_filepath, raster_layer_name)
            qml_path = get_qml_style_path(raster_file_field, "raster")
            if qml_path is not None:
                rlayer.loadNamedStyle(qml_path)
            add_layer_to_group(group_name, rlayer, bottom=True)


def remove_user_layers():
    """Removing all 3Di model User Layers and rasters from the map canvas."""
    groups = ["1D", "2D", "Inflow", "Settings", "Model rasters"]
    for group_name in groups:
        remove_group_with_children(group_name)


def open_edit_form(dialog, layer, feature):
    """Open location custom feature edit form."""
    try:
        plugin = plugins["threedi_schematisation_editor"]
    except AttributeError:
        return
    plugin.layer_manager.populate_edit_form(dialog, layer, feature)


def cross_section_table_values(cross_section_table):
    """Get height and width values."""
    height_list, width_list = [], []
    for row in cross_section_table.split("\n"):
        height_str, width_str = row.split(",")
        height = float(height_str)
        width = float(width_str)
        height_list.append(height)
        width_list.append(width)
    return height_list, width_list


@qgsfunction(args="auto", group="3Di")
def cross_section_max_height(feature, parent):
    """Get max height value."""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.TABLE_SHAPES:
        return feature["cross_section_height"]
    table = feature["cross_section_table"]
    height_list, width_list = cross_section_table_values(table)
    return max(height_list)


@qgsfunction(args="auto", group="3Di")
def cross_section_max_width(feature, parent):
    """Get max width value."""
    shape_value = feature["cross_section_shape"]
    if shape_value not in dm.TABLE_SHAPES:
        return feature["cross_section_width"]
    table = feature["cross_section_table"]
    height_list, width_list = cross_section_table_values(table)
    return max(width_list)


@qgsfunction(args="auto", group="3Di")
def cross_section_label(feature, parent):
    """Create label with max height and max width out of cross-section table values."""
    label = ""
    shape_value = feature["cross_section_shape"]
    if not shape_value:
        return label
    shape_name = en.CrossSectionShape(shape_value).name.replace("_", " ")
    if shape_value != en.CrossSectionShape.YZ.value:
        shape_name = shape_name.capitalize()
    shape_value_and_name = f"{shape_value}: {shape_name}\n"
    label += shape_value_and_name
    width = feature["cross_section_width"]
    height = feature["cross_section_height"]
    if shape_value == en.CrossSectionShape.CLOSED_RECTANGLE.value:
        label += f"w: {width:.2f}"
    elif shape_value == en.CrossSectionShape.OPEN_RECTANGLE.value:
        label += f"w: {width:.2f}\nh: {height:.2f}"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width:.2f}"
    elif shape_value in {en.CrossSectionShape.EGG.value, en.CrossSectionShape.INVERTED_EGG.value}:
        label += f"w: {width:.2f}\nh: {width*1.5:.2f}"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table)
        max_height = max(height_list)
        max_width = max(width_list)
        label += f"w: {max_width:.2f}\nh: {max_height:.2f}"
    return label


@qgsfunction(args="auto", group="3Di")
def diameter_label(feature, parent):
    """Create label with diameter value."""
    label = ""
    shape_value = feature["cross_section_shape"]
    if not shape_value:
        return label
    width = feature["cross_section_width"]
    height = feature["cross_section_height"]
    if shape_value in {en.CrossSectionShape.OPEN_RECTANGLE.value, en.CrossSectionShape.CLOSED_RECTANGLE.value}:
        label += f"rect {width*1000:.0f}x{height*1000:.0f}"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width*1000:.0f}"
    elif shape_value == en.CrossSectionShape.EGG.value:
        label += f"egg {width*1000:.0f}/{width * 1000 * 1.5:.3f}"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table)
        max_height = max(height_list)
        max_width = max(width_list)
        label += "tab " if shape_value != en.CrossSectionShape.YZ.value else "yz "
        label += f"{max_width*1000:.0f}/{max_height*1000:.0f}"
    return label


@qgsfunction(args="auto", group="3Di")
def width_label(feature, parent):
    """Create label with width value."""
    label = ""
    shape_value = feature["cross_section_shape"]
    if not shape_value:
        return label
    width = feature["cross_section_width"]
    if shape_value in {en.CrossSectionShape.OPEN_RECTANGLE.value, en.CrossSectionShape.CLOSED_RECTANGLE.value}:
        label += f"w: {width:.2f} (rect)"
    elif shape_value == en.CrossSectionShape.CIRCLE.value:
        label += f"Ø{width:.2f}"
    elif shape_value in {en.CrossSectionShape.EGG.value, en.CrossSectionShape.INVERTED_EGG.value}:
        label += f"w: {width:.2f} (egg)"
    elif shape_value in dm.TABLE_SHAPES:
        table = feature["cross_section_table"]
        height_list, width_list = cross_section_table_values(table)
        max_width = max(width_list)
        label += f"w: {max_width:.2f} "
        label += "(tab)" if shape_value != en.CrossSectionShape.YZ.value else "(yz)"
    return label


def connect_signal(signal, slot):
    """Connecting signal with slot."""
    signal.connect(slot)


def disconnect_signal(signal, slot):
    """Disconnecting signal with slot."""
    try:
        signal.disconnect(slot)
    except TypeError:
        pass


def find_point_nodes(point, node_layer, tolerance=0.0000001, allow_multiple=False, locator=None):
    """Function that finds features from given layer that are located within tolerance distance from given point."""
    project = QgsProject.instance()
    src_crs = node_layer.sourceCrs()
    dst_crs = project.crs()
    transform_ctx = project.transformContext()
    if not locator:
        locator = QgsPointLocator(node_layer, dst_crs, transform_ctx)
    node_feats = []
    node_feat = None
    if src_crs != dst_crs:
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx)
        point_geom = QgsGeometry.fromPointXY(point)
        point_geom.transform(transformation)
        point = point_geom.asPoint()
    matches = locator.verticesInRect(point, tolerance)
    for match in matches:
        match_layer = match.layer()
        if match_layer:
            node_fid = match.featureId()
            node_feat = match_layer.getFeature(node_fid)
            node_feats.append(node_feat)
    return node_feats if allow_multiple else node_feat


def find_linestring_nodes(linestring, node_layer, tolerance=0.0000001, allow_multiple=False, locator=None):
    """
    Function that finds features from given layer that are located within tolerance distance from linestring endpoints.
    """
    project = QgsProject.instance()
    src_crs = node_layer.sourceCrs()
    dst_crs = project.crs()
    transform_ctx = project.transformContext()
    if not locator:
        locator = QgsPointLocator(node_layer, dst_crs, transform_ctx)
    feats_at_start, feats_at_end = [], []
    node_start_feat, node_end_feat = None, None
    start_point, end_point = linestring[0], linestring[-1]
    if src_crs != dst_crs:
        start_geom = QgsGeometry.fromPointXY(start_point)
        end_geom = QgsGeometry.fromPointXY(end_point)
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx)
        start_geom.transform(transformation)
        end_geom.transform(transformation)
        start_point = start_geom.asPoint()
        end_point = end_geom.asPoint()
    start_matches = locator.verticesInRect(start_point, tolerance)
    end_matches = locator.verticesInRect(end_point, tolerance)
    for start_match in start_matches:
        start_match_layer = start_match.layer()
        if start_match_layer:
            node_start_fid = start_match.featureId()
            node_start_feat = start_match_layer.getFeature(node_start_fid)
            feats_at_start.append(node_start_feat)
    for end_match in end_matches:
        end_match_layer = end_match.layer()
        if end_match_layer:
            node_end_fid = end_match.featureId()
            node_end_feat = end_match_layer.getFeature(node_end_fid)
            feats_at_end.append(node_end_feat)
    if allow_multiple:
        return feats_at_start, feats_at_end
    else:
        return node_start_feat, node_end_feat


def find_point_polygons(point, polygon_layer, allow_multiple=False, locator=None):
    """Function that finds features from given polygon layer that contains given point."""
    project = QgsProject.instance()
    src_crs = polygon_layer.sourceCrs()
    dst_crs = project.crs()
    transform_ctx = project.transformContext()
    if not locator:
        locator = QgsPointLocator(polygon_layer, dst_crs, transform_ctx)
    polygon_feats = []
    polygon_feat = None
    if src_crs != dst_crs:
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx)
        point_geom = QgsGeometry.fromPointXY(point)
        point_geom.transform(transformation)
        point = point_geom.asPoint()
    matches = locator.pointInPolygon(point)
    for match in matches:
        match_layer = match.layer()
        if match_layer:
            polygon_fid = match.featureId()
            polygon_feat = match_layer.getFeature(polygon_fid)
            polygon_feats.append(polygon_feat)
    return polygon_feats if allow_multiple else polygon_feat


def find_point_polyline(point, polyline_layer, tolerance=0.0000001, locator=None):
    """Function that finds feature from given polyline layer that intersects with given point."""
    project = QgsProject.instance()
    src_crs = polyline_layer.sourceCrs()
    dst_crs = project.crs()
    transform_ctx = project.transformContext()
    if not locator:
        locator = QgsPointLocator(polyline_layer, dst_crs, transform_ctx)
    polyline_feat = None
    if src_crs != dst_crs:
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx)
        point_geom = QgsGeometry.fromPointXY(point)
        point_geom.transform(transformation)
        point = point_geom.asPoint()
    match = locator.nearestEdge(point, tolerance)
    match_layer = match.layer()
    if match_layer:
        polyline_fid = match.featureId()
        polyline_feat = match_layer.getFeature(polyline_fid)
    return polyline_feat


def count_vertices(geometry):
    """Returning number of vertices within geometry."""
    c = sum(1 for _ in geometry.vertices())
    return c


def check_enable_macros_option():
    """Check if macros are enabled."""
    settings = QSettings()
    option = settings.value("/qgis/enableMacros", type=str)
    return option


def get_next_feature_id(layer):
    """Return first available ID within layer features."""
    id_idx = layer.fields().indexFromName("id")
    # Ensure the id attribute is unique
    try:
        next_id = max(layer.uniqueValues(id_idx)) + 1
    except ValueError:
        # this is the first feature
        next_id = 1
    return next_id


def add_settings_entry(gpkg_path, **initial_fields_values):
    """Adding initial settings entry with defined fields values."""
    settings_layer = gpkg_layer(gpkg_path, dm.GlobalSettings.__tablename__)
    if settings_layer.featureCount() == 0:
        settings_fields = settings_layer.fields()
        settings_feat = QgsFeature(settings_fields)
        for field, value in initial_fields_values.items():
            settings_feat[field] = value
        settings_layer.startEditing()
        settings_layer.addFeature(settings_feat)
        settings_layer.commitChanges()


def get_qgis(qgis_build_path="C:/OSGeo4W64/apps/qgis-ltr", qgis_proj_path="C:/OSGeo4W64/share/proj"):
    """Initializing QGIS instance for running standalone scripts tha are using QGIS API."""
    qgis_python_path = os.path.join(qgis_build_path, "python")
    qgis_plugins_path = os.path.join(qgis_python_path, "plugins")

    os.putenv("QGIS_PREFIX_PATH", qgis_build_path)
    os.putenv("QGIS_DEBUG", "-1")
    os.putenv("PROJ_LIB", qgis_proj_path)

    sys.path.insert(0, qgis_python_path)
    sys.path.insert(1, qgis_plugins_path)

    from qgis.core import QgsApplication

    qgis_app = QgsApplication([b"test"], False)
    qgis_app.initQgis()
    return qgis_app


class ConversionError(Exception):
    pass


def is_gpkg_connection_exists(gpkg_path):
    """Check if GeoPackage connection exists in settings."""
    gpkg_path = gpkg_path.replace("\\", "/")
    settings = QSettings()
    settings.beginGroup("providers/ogr/GPKG/connections")
    for connection in settings.allKeys():
        connection_path = settings.value(connection, type=str)
        connection_path = connection_path.replace("\\", "/")
        if connection_path == gpkg_path:
            return True
    return False


def can_write_in_dir(path_to_test):
    """Try to write and remove an empty text file into given location."""
    try:
        test_filename = f"{uuid4()}.txt"
        test_file_path = os.path.join(path_to_test, test_filename)
        with open(test_file_path, "w") as test_file:
            test_file.write("")
        os.remove(test_file_path)
        return True
    except (PermissionError, OSError):
        return False


def add_gpkg_connection(gpkg_path, iface=None):
    """Write GeoPackage connection into the settings."""
    connection_name = os.path.basename(gpkg_path)
    gpkg_path = gpkg_path.replace("\\", "/")
    settings = QSettings()
    settings.setValue(f"providers/ogr/GPKG/connections/{connection_name}/path", gpkg_path)
    if iface is not None:
        iface.mainWindow().connectionsChanged.emit()


def hillshade_layer(raster_filepath, layer_name="Hillshade", band=1, light_azimuth=315, light_altitude=45, opacity=0.5):
    """Initialize raster layer with hilshade rendering."""
    hillshade_raster_layer = QgsRasterLayer(raster_filepath, layer_name)
    renderer = QgsHillshadeRenderer(hillshade_raster_layer.dataProvider(), band, light_azimuth, light_altitude)
    renderer.setOpacity(opacity)
    hillshade_raster_layer.setRenderer(renderer)
    hillshade_raster_layer.setBlendMode(QPainter.CompositionMode_Multiply)
    hillshade_raster_layer.resampleFilter().setZoomedInResampler(QgsBilinearRasterResampler())
    return hillshade_raster_layer


def modify_raster_style(raster_layer, limits=QgsRasterMinMaxOrigin.MinMax, extent=QgsRasterMinMaxOrigin.UpdatedCanvas):
    """Improve predefined raster styling."""
    renderer = raster_layer.renderer().clone()
    min_max_origin = renderer.minMaxOrigin()
    min_max_origin.setLimits(limits)
    min_max_origin.setExtent(extent)
    renderer.setMinMaxOrigin(min_max_origin)
    raster_layer.setRenderer(renderer)


def migrate_spatialite_schema(sqlite_filepath):
    migration_succeed = False
    try:
        from threedi_schema import ThreediDatabase, errors

        threedi_db = ThreediDatabase(sqlite_filepath)
        schema = threedi_db.schema
        backup_filepath = backup_sqlite(sqlite_filepath)
        schema.upgrade(backup=False, upgrade_spatialite_version=True)
        schema.set_spatial_indexes()
        shutil.rmtree(os.path.dirname(backup_filepath))
        migration_succeed = True
        migration_feedback_msg = "Migration succeed."
    except ImportError:
        migration_feedback_msg = "Missing threedi-schema library. Schema migration failed."
    except errors.UpgradeFailedError:
        migration_feedback_msg = (
            "There are errors in the spatialite. Please re-open this file in QGIS 3.16, run the threedi-schema and "
            "fix error messages. Then attempt to upgrade again. For questions please contact the servicedesk."
        )
    except Exception as e:
        migration_feedback_msg = f"{e}"
    return migration_succeed, migration_feedback_msg


def validation_errors_summary(validation_errors):
    """Create validation summary message grouped by the data model class."""
    summary_per_model = []
    for model_cls, errors in groupby(validation_errors, attrgetter("data_model_cls")):
        errors_fids = sorted(ve.source_id for ve in errors)
        errors_fids_str = ", ".join(str(ve) for ve in errors_fids)
        summary_per_model.append(f"{model_cls.__layername__}: {errors_fids_str}")
    summary_per_model.sort()
    summary_message = "\n".join(summary_per_model)
    return summary_message


class FormCustomizations:
    """Methods container for the forms widgets extra customizations."""

    @staticmethod
    def cross_section_table_placeholder_text(widget):
        placeholder_text = (
            "Format this input as a CSV-style table of height, width pairs.\n\n"
            "Example:\n\n"
            "0.0, 0.5\n"
            "0.5, 1.2\n"
            "2.3, 3.2\n"
            "4.4, 5.0"
        )
        widget.setPlaceholderText(placeholder_text)


def setup_cross_section_widgets(custom_form, cross_section_shape_widget, prefix=""):
    """Adjust cross-section characteristic widgets availability based on the selected shape type."""
    cross_section_width_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_width")
    cross_section_width_clear_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_width_clear")
    cross_section_width_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_width_label")
    cross_section_height_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_height")
    cross_section_height_clear_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_height_clear")
    cross_section_height_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_height_label")
    cross_section_table_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_widget")
    cross_section_table_widget_add = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_add")
    cross_section_table_widget_paste = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_paste")
    cross_section_table_widget_delete = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_delete")
    cross_section_table_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_label")
    all_related_widgets = [
        cross_section_width_widget,
        cross_section_width_clear_widget,
        cross_section_width_label_widget,
        cross_section_height_widget,
        cross_section_height_clear_widget,
        cross_section_height_label_widget,
        cross_section_table_widget,
        cross_section_table_widget_add,
        cross_section_table_widget_paste,
        cross_section_table_widget_delete,
        cross_section_table_label_widget,
    ]
    for related_widget in all_related_widgets:
        related_widget.setDisabled(True)
    cross_section_shape = custom_form.get_widget_value(cross_section_shape_widget)
    custom_form.update_cross_section_table_header()
    if cross_section_shape == en.CrossSectionShape.CIRCLE.value:
        cross_section_width_label_widget.setText("Diameter [m]")
    else:
        cross_section_width_label_widget.setText("Width [m]")
    if custom_form.layer.isEditable():
        if cross_section_shape in {
            en.CrossSectionShape.CLOSED_RECTANGLE.value,
            en.CrossSectionShape.OPEN_RECTANGLE.value,
            en.CrossSectionShape.CIRCLE.value,
            en.CrossSectionShape.EGG.value,
            en.CrossSectionShape.INVERTED_EGG.value,
        }:
            cross_section_width_widget.setEnabled(True)
            cross_section_width_clear_widget.setEnabled(True)
            cross_section_width_label_widget.setEnabled(True)
            cross_section_table_widget.setDisabled(True)
            cross_section_table_widget_add.setDisabled(True)
            cross_section_table_widget_paste.setDisabled(True)
            cross_section_table_widget_delete.setDisabled(True)
            cross_section_table_label_widget.setDisabled(True)
            if cross_section_shape in {
                en.CrossSectionShape.CLOSED_RECTANGLE.value,
            }:
                cross_section_height_widget.setEnabled(True)
                cross_section_height_clear_widget.setEnabled(True)
                cross_section_height_label_widget.setEnabled(True)
        elif cross_section_shape in {
            en.CrossSectionShape.TABULATED_RECTANGLE.value,
            en.CrossSectionShape.TABULATED_TRAPEZIUM.value,
            en.CrossSectionShape.YZ.value,
        }:
            cross_section_width_widget.setDisabled(True)
            cross_section_width_clear_widget.setDisabled(True)
            cross_section_width_label_widget.setDisabled(True)
            cross_section_table_widget.setEnabled(True)
            cross_section_table_widget_add.setEnabled(True)
            cross_section_table_widget_paste.setEnabled(True)
            cross_section_table_widget_delete.setEnabled(True)
            cross_section_table_label_widget.setEnabled(True)
        else:
            pass


class NumericItemDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(editor)
        validator.setBottom(0)
        validator.setDecimals(3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        editor.setValidator(validator)
        return editor
