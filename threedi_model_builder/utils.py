# Copyright (C) 2022 by Lutra Consulting
import os
import sys
import shutil
import sqlite3
import threedi_model_builder.data_models as dm
from enum import Enum
from typing import Union
from collections import OrderedDict
from qgis.PyQt.QtCore import QSettings, QVariant
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsMapLayer,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsField,
    QgsGeometry,
    QgsCoordinateTransform,
    QgsVectorFileWriter,
    QgsPointLocator,
)
from qgis.utils import plugins

field_types_mapping = {
    bool: QVariant.Bool,
    int: QVariant.Int,
    float: QVariant.Double,
    str: QVariant.String,
}


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
    """Getting real type of an Optional field type."""
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


def set_initial_layer_configuration(layer):
    """Set initial vector layer configuration that should be set within currently active style."""
    attr_table_config = layer.attributeTableConfig()
    columns = attr_table_config.columns()
    for column in columns:
        if column.name == "fid":
            column.hidden = True
            break
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
        plugin = plugins["threedi_model_builder"]
    except AttributeError:
        return
    plugin.layer_manager.populate_edit_form(dialog, layer, feature)


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


def create_3di_views(sqlite_filepath):
    """Create views in 3Di model sqlite database."""
    connection = sqlite3.connect(sqlite_filepath)
    qry = """
    CREATE VIEW IF NOT EXISTS v2_manhole_view
    AS SELECT manh.rowid AS ROWID, node.id AS node_id, manh.bottom_level
    AS manh_bottom_level, manh.surface_level AS manh_surface_level,
    manh.display_name AS manh_display_name, manh.shape AS manh_shape,
    manh.width AS manh_width, manh.length AS manh_length,
    manh.manhole_indicator AS manh_manhole_indicator, manh.calculation_type
    AS manh_calculation_type, manh.drain_level AS manh_drain_level,
    manh.zoom_category AS manh_zoom_category, node.initial_waterlevel AS
    node_initial_waterlevel, manh.id AS manh_id, manh.connection_node_id  AS
    manh_connection_node_id, node.storage_area AS node_storage_area,
    manh.code AS manh_code, node.code AS node_code, node.the_geom,
    node.the_geom_linestring AS node_the_geom_linestring,
    manh.sediment_level AS manh_sediment_level
    FROM v2_manhole manh, v2_connection_nodes node
    WHERE manh.connection_node_id = node.id;

    DELETE FROM views_geometry_columns
    WHERE view_name = 'v2_manhole_view';

    INSERT INTO views_geometry_columns (view_name, view_geometry,
    view_rowid, f_table_name, f_geometry_column)
    VALUES('v2_manhole_view', 'the_geom', 'ROWID',
    'v2_connection_nodes', 'the_geom');

    CREATE VIEW IF NOT EXISTS v2_pumpstation_point_view
    AS SELECT a.ROWID AS ROWID, a.id AS pump_id, a.display_name, a.code,
    a.classification, a.sewerage, a.start_level, a.lower_stop_level,
    a.upper_stop_level, a.capacity, a.zoom_category,
    a.connection_node_start_id, a.connection_node_end_id, a.type,
    b.id AS connection_node_id, b.storage_area, b.the_geom
    FROM v2_pumpstation a
    JOIN v2_connection_nodes b
    ON a.connection_node_start_id = b.id;

    DELETE FROM views_geometry_columns
    WHERE view_name = 'v2_pumpstation_point_view';

    INSERT INTO views_geometry_columns (view_name, view_geometry,
    view_rowid, f_table_name, f_geometry_column)
    VALUES('v2_pumpstation_point_view', 'the_geom',
    'connection_node_start_id', 'v2_connection_nodes', 'the_geom');

    CREATE VIEW IF NOT EXISTS v2_1d_lateral_view
    AS SELECT a.ROWID AS ROWID, a.id AS id,
    a.connection_node_id AS connection_node_id,
    a.timeseries AS timeseries, b.the_geom
    FROM v2_1d_lateral a
    JOIN v2_connection_nodes b ON a.connection_node_id = b.id;

    DELETE FROM views_geometry_columns
    WHERE view_name = 'v2_1d_lateral_view';

    INSERT INTO views_geometry_columns (view_name, view_geometry,
    view_rowid, f_table_name, f_geometry_column)
    VALUES('v2_1d_lateral_view', 'the_geom', 'connection_node_id',
    'v2_connection_nodes', 'the_geom');

    CREATE VIEW IF NOT EXISTS v2_1d_boundary_conditions_view
    AS SELECT a.ROWID AS ROWID, a.id AS id,
    a.connection_node_id AS connection_node_id,
    a.boundary_type AS boundary_type, a.timeseries AS timeseries,
    b.the_geom
    FROM v2_1d_boundary_conditions a
    JOIN v2_connection_nodes b ON a.connection_node_id = b.id;

    DELETE FROM views_geometry_columns
    WHERE view_name = 'v2_1d_boundary_conditions_view';

    INSERT INTO views_geometry_columns (view_name, view_geometry,
    view_rowid, f_table_name, f_geometry_column)
    VALUES('v2_1d_boundary_conditions_view', 'the_geom',
    'connection_node_id', 'v2_connection_nodes', 'the_geom');

    CREATE VIEW IF NOT EXISTS v2_cross_section_location_view
    AS SELECT loc.ROWID as ROWID, loc.id as loc_id, loc.code as loc_code,
    loc.reference_level as loc_reference_level,
    loc.bank_level as loc_bank_level, loc.friction_type as
    loc_friction_type, loc.friction_value as loc_friction_value,
    loc.definition_id as loc_definition_id, loc.channel_id as
    loc_channel_id, loc.the_geom as the_geom, def.id as def_id,
    def.shape as def_shape, def.width as def_width, def.code as
    def_code, def.height as def_height
    FROM v2_cross_section_location loc, v2_cross_section_definition def
    WHERE loc.definition_id = def.id;

    DELETE FROM views_geometry_columns
    WHERE view_name = 'v2_cross_section_location_view';

    INSERT INTO views_geometry_columns (view_name, view_geometry,
    view_rowid, f_table_name, f_geometry_column)
    VALUES('v2_cross_section_location_view', 'the_geom',
    'ROWID', 'v2_cross_section_location', 'the_geom');
    """
    c = connection.cursor()
    c.executescript(qry)
    connection.commit()
    connection.close()


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


def add_gpkg_connection(gpkg_path, iface=None):
    """Write GeoPackage connection into the settings."""
    connection_name = os.path.basename(gpkg_path)
    gpkg_path = gpkg_path.replace("\\", "/")
    settings = QSettings()
    settings.setValue(f"providers/ogr/GPKG/connections/{connection_name}/path", gpkg_path)
    if iface is not None:
        iface.mainWindow().connectionsChanged.emit()
