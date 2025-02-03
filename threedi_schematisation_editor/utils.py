# Copyright (C) 2025 by Lutra Consulting
import os
import shutil
import sys
from enum import Enum
from itertools import groupby
from operator import attrgetter, itemgetter
from typing import Union
from uuid import uuid4

from qgis.core import (
    NULL,
    QgsBilinearRasterResampler,
    QgsCoordinateTransform,
    QgsEditorWidgetSetup,
    QgsExpression,
    QgsFeature,
    QgsFeatureRequest,
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
    QgsSettings,
    QgsSpatialIndex,
    QgsValueMapFieldFormatter,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QObject, QVariant
from qgis.PyQt.QtGui import QDoubleValidator, QPainter
from qgis.PyQt.QtWidgets import QFileDialog, QItemDelegate, QLineEdit
from qgis.utils import plugins

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en

NULL_STR = "NULL"
QUOTED_NULL = '"NULL"'
REQUIRED_VALUE_STYLESHEET = "background-color: rgb(255, 224, 178);"

field_types_mapping = {
    bool: QVariant.Bool,
    int: QVariant.Int,
    float: QVariant.Double,
    str: QVariant.String,
}


def backup_schematisation_file(filename):
    """Make a backup of the schematisation file."""
    backup_folder = os.path.join(os.path.dirname(os.path.dirname(filename)), "_backup")
    os.makedirs(backup_folder, exist_ok=True)
    prefix = str(uuid4())[:8]
    backup_file_path = os.path.join(backup_folder, f"{prefix}_{os.path.basename(filename)}")
    shutil.copyfile(filename, backup_file_path)
    return backup_file_path


def vector_layer_factory(annotated_model_cls, epsg=4326):
    """Function that creates memory layer based on annotated data model class."""
    fields = []
    geometry_type = annotated_model_cls.__geometrytype__.value
    layer_name = annotated_model_cls.__tablename__
    uri = f"{geometry_type}?crs=EPSG:{epsg}"
    layer = QgsVectorLayer(uri, layer_name, "memory")
    for field_name, field_type in annotated_model_cls.__annotations__.items():
        field_type = core_field_type(field_type)
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


def core_field_type(field_type):
    """Return a core field type of the field type."""
    real_field_type = field_type
    if is_optional(real_field_type):
        real_field_type = optional_type(real_field_type)
    if issubclass(real_field_type, Enum):
        real_field_type = enum_type(real_field_type)
    return real_field_type


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
    valid_indexes = [fields.lookupField(fname) for fname in fields.names()]
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
        qml_paths = [
            os.path.normpath(os.path.join(styles_folder_path, q))
            for q in os.listdir(styles_folder_path)
            if q.endswith(".qml")
        ]
    else:
        qml_paths = []
    return qml_paths


def get_form_ui_path(table_name):
    """Getting UI form path for a given table name."""
    ui_filename = f"{table_name}.ui"
    filepath = os.path.normpath(os.path.join(os.path.dirname(__file__), "forms", "ui", ui_filename))
    if os.path.isfile(filepath):
        return filepath
    return None


def get_icon_path(icon_filename, root_dir=None):
    """Getting icon path for a given icon file."""
    icon_filepath = os.path.join(os.path.dirname(__file__) if root_dir is None else root_dir, "icons", icon_filename)
    return icon_filepath


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


def get_filepath(
    parent,
    extension_filter=None,
    extension=None,
    save=True,
    dialog_title=None,
    default_settings_entry="threedi/last_schematisation_folder",
):
    """Opening dialog to get a filepath."""
    if extension_filter is None:
        extension_filter = "All Files (*.*)"
    if dialog_title is None:
        dialog_title = "Save to file" if save else "Choose file"
    starting_dir = QgsSettings().value(default_settings_entry, os.path.expanduser("~"), type=str)
    if save is True:
        file_name, __ = QFileDialog.getSaveFileName(parent, dialog_title, starting_dir, extension_filter)
    else:
        file_name, __ = QFileDialog.getOpenFileName(parent, dialog_title, starting_dir, extension_filter)
    if len(file_name) == 0:
        return None
    if extension:
        if not file_name.endswith(extension):
            file_name += extension
    return file_name


def dataclass_field_to_widget_setup(model_cls_field_type, optional=False, **config_overrides):
    """Create QgsEditorWidgetSetup out of the dataclass field type."""
    if model_cls_field_type is bool:
        config_type = "CheckBox"
        config_map = {"AllowNull": optional}
    elif model_cls_field_type is int:
        config_type = "TextEdit"
        config_map = {"AllowNull": optional}
    elif model_cls_field_type is float:
        config_type = "Range"
        config_map = {
            "AllowNull": optional,
            "Max": 10**15,
            "Min": -(10**15),
            "Precision": 3,
            "Step": 1.0,
            "Style": "SpinBox",
        }
    elif model_cls_field_type is str:
        config_type = "TextEdit"
        config_map = {"AllowNull": optional}
    else:
        return None
    config_map.update(config_overrides)
    ews = QgsEditorWidgetSetup(config_type, config_map)
    return ews


def enum_to_editor_widget_setup(enum, optional=False, enum_name_format_fn=None):
    """Create QgsEditorWidgetSetup out of the Enum object."""
    if enum_name_format_fn is None:

        def enum_name_format_fn(entry_name):
            return entry_name

    value_map = [{f"{enum_name_format_fn(entry.name)}": entry.value} for entry in enum]
    if optional:
        null_value = QgsValueMapFieldFormatter.NULL_VALUE
        value_map.insert(0, {"": null_value})
    ews = QgsEditorWidgetSetup("ValueMap", {"map": value_map})
    return ews


def enum_entry_name_format(entry_name):
    if entry_name not in ["YZ", "HPE", "HDPE", "PVC"]:
        formatted_entry_name = entry_name.capitalize().replace("_", " ")
    else:
        formatted_entry_name = entry_name
    return formatted_entry_name


def set_initial_layer_configuration(layer, model_cls):
    """Set initial vector layer configuration that should be set within currently active style."""
    attr_table_config = layer.attributeTableConfig()
    fields = layer.dataProvider().fields()
    columns = attr_table_config.columns()
    model_hidden_fields = model_cls.hidden_fields()
    for column in columns:
        column_name = column.name
        if column_name in model_hidden_fields:
            column.hidden = True
            continue
        try:
            field_type = model_cls.__annotations__[column_name]
            if is_optional(field_type):
                field_type = optional_type(field_type)
                optional = True
            else:
                optional = False
            field_idx = fields.lookupField(column_name)
            if issubclass(field_type, Enum):
                ews = enum_to_editor_widget_setup(field_type, optional, enum_name_format_fn=enum_entry_name_format)
            else:
                if column_name.startswith("hydraulic_conductivity"):
                    ews = dataclass_field_to_widget_setup(field_type, optional=True, Min=0)
                else:
                    ews = dataclass_field_to_widget_setup(field_type)
            if ews is not None:
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


def remove_user_layers():
    """Removing all 3Di model User Layers and rasters from the map canvas."""
    groups = [
        "1D",
        "1D2D",
        "2D",
        "Laterals & 0D inflow",
        "Structure control",
        "Hydrological processes",
        "Settings",
        "Rasters",
    ]
    for group_name in groups:
        remove_group_with_children(group_name)


def open_edit_form(dialog, layer, feature):
    """Open location custom feature edit form."""
    try:
        plugin = plugins["threedi_schematisation_editor"]
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


def find_line_endpoints_nodes(linestring, locator, tolerance=0.1):
    """
    Find features from given locator layer which are in the tolerance distance from the linestring endpoints.
    """
    node_start_feat, node_end_feat = None, None
    start_point, end_point = linestring[0], linestring[-1]
    start_match = locator.nearestVertex(start_point, tolerance)
    end_match = locator.nearestVertex(end_point, tolerance)
    start_match_layer = start_match.layer()
    if start_match_layer:
        node_start_fid = start_match.featureId()
        node_start_feat = start_match_layer.getFeature(node_start_fid)
    end_match_layer = end_match.layer()
    if end_match_layer:
        node_end_fid = end_match.featureId()
        node_end_feat = end_match_layer.getFeature(node_end_fid)
    return node_start_feat, node_end_feat


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
    settings = QgsSettings()
    option = settings.value("/qgis/enableMacros", type=str)
    return option


def get_next_feature_id(layer):
    """Return first available ID within layer features."""
    id_idx = layer.fields().indexFromName("id")
    # Ensure the id attribute is unique
    try:
        next_id = max(layer.uniqueValues(id_idx)) + 1
    except (TypeError, ValueError):
        # this is the first feature
        next_id = 1
    return next_id


def get_features_by_expression(layer, expression_text, with_geometry=False):
    """Return iterator of the layer features matching to the given expression."""
    expression = QgsExpression(expression_text)
    request = QgsFeatureRequest(expression)
    if not with_geometry:
        request.setFlags(QgsFeatureRequest.NoGeometry)
    feat_iterator = layer.getFeatures(request)
    return feat_iterator


def get_feature_by_id(layer, object_id, id_field="id"):
    """Return layer feature with the given id."""
    feat = None
    if object_id not in (None, NULL):
        expression = QgsExpression(f'"{id_field}" = {object_id}')
        request = QgsFeatureRequest(expression)
        feats = layer.getFeatures(request)
        try:
            feat = next(feats)
        except StopIteration:
            pass
    return feat


def add_settings_entry(gpkg_path, **initial_fields_values):
    """Adding initial settings entry with defined fields values."""
    settings_layer = gpkg_layer(gpkg_path, dm.ModelSettings.__tablename__)
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
    settings = QgsSettings()
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
    settings = QgsSettings()
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


def migrate_schematisation_schema(schematisation_filepath):
    migration_succeed = False
    try:
        from threedi_schema import ThreediDatabase, errors

        backup_filepath = backup_schematisation_file(schematisation_filepath)
        threedi_db = ThreediDatabase(schematisation_filepath)
        threedi_db.schema.upgrade(backup=False)
        shutil.rmtree(os.path.dirname(backup_filepath))
        migration_succeed = True
        migration_feedback_msg = "Migration succeed."
    except ImportError:
        migration_feedback_msg = "Missing threedi-schema library (or its dependencies). Schema migration failed."
    except errors.UpgradeFailedError:
        migration_feedback_msg = (
            "The schematisation database schema cannot be migrated to the current version. "
            "Please contact the service desk for assistance."
        )
    except Exception as e:
        migration_feedback_msg = f"{e}"
    return migration_succeed, migration_feedback_msg


def bypass_max_path_limit(path, is_file=False):
    """Check and modify path to bypass Windows MAX_PATH limitation."""
    dir_max_path = 248
    file_max_path = 260
    unc_prefix = "\\\\?\\"
    path_str = str(path)
    if path_str.startswith(unc_prefix):
        valid_path = path_str
    else:
        if is_file:
            if len(path_str) >= file_max_path:
                valid_path = f"{unc_prefix}{path_str}"
            else:
                valid_path = path_str
        else:
            if len(path_str) > dir_max_path:
                valid_path = f"{unc_prefix}{path_str}"
            else:
                valid_path = path_str
    return valid_path


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


def spatial_index(layer, request=None):
    """Creating spatial index over layer features."""
    features = {}
    index = QgsSpatialIndex()
    for feat in layer.getFeatures() if request is None else layer.getFeatures(request):
        feat_copy = QgsFeature(feat)
        features[feat.id()] = feat_copy
        index.insertFeature(feat_copy)
    return features, index


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
    cross_section_table_widget_copy = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_table_copy")
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
        cross_section_table_widget_copy,
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
        if cross_section_shape in dm.NON_TABLE_SHAPES:
            cross_section_width_widget.setEnabled(True)
            cross_section_width_clear_widget.setEnabled(True)
            cross_section_width_label_widget.setEnabled(True)
            cross_section_table_widget.setDisabled(True)
            cross_section_table_widget_add.setDisabled(True)
            cross_section_table_widget_paste.setDisabled(True)
            cross_section_table_widget_delete.setDisabled(True)
            cross_section_table_widget_copy.setDisabled(True)
            cross_section_table_label_widget.setDisabled(True)
            if cross_section_shape in {
                en.CrossSectionShape.CLOSED_RECTANGLE.value,
            }:
                cross_section_height_widget.setEnabled(True)
                cross_section_height_clear_widget.setEnabled(True)
                cross_section_height_label_widget.setEnabled(True)
        elif cross_section_shape in dm.TABLE_SHAPES:
            cross_section_width_widget.setDisabled(True)
            cross_section_width_clear_widget.setDisabled(True)
            cross_section_width_label_widget.setDisabled(True)
            cross_section_table_widget.setEnabled(True)
            cross_section_table_widget_add.setEnabled(True)
            cross_section_table_widget_paste.setEnabled(True)
            cross_section_table_widget_delete.setEnabled(True)
            cross_section_table_widget_copy.setEnabled(True)
            cross_section_table_label_widget.setEnabled(True)
        else:
            pass


def setup_friction_and_vegetation_widgets(custom_form, cross_section_shape_widget, friction_widget, prefix=""):
    """Adjust friction and vegetation characteristic widgets availability based on the selected shape type."""
    friction_value_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}friction_value_label")
    friction_value_widget = custom_form.dialog.findChild(QObject, f"{prefix}friction_value")
    friction_value_clear_widget = custom_form.dialog.findChild(QObject, f"{prefix}friction_value_clear")
    cross_section_friction_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_friction_label")
    cross_section_friction_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_friction_widget")
    cross_section_friction_clear = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_friction_clear")
    cross_section_friction_copy = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_friction_copy")
    vegetation_stem_density_label_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_stem_density_label"
    )
    vegetation_stem_density_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_stem_density")
    vegetation_stem_density_clear_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_stem_density_clear"
    )
    vegetation_stem_diameter_label_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_stem_diameter_label"
    )
    vegetation_stem_diameter_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_stem_diameter")
    vegetation_stem_diameter_clear_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_stem_diameter_clear"
    )
    vegetation_height_label_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_height_label")
    vegetation_height_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_height")
    vegetation_height_clear_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_height_clear")
    vegetation_drag_coefficient_label_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_drag_coefficient_label"
    )
    vegetation_drag_coefficient_widget = custom_form.dialog.findChild(QObject, f"{prefix}vegetation_drag_coefficient")
    vegetation_drag_coefficient_clear_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}vegetation_drag_coefficient_clear"
    )
    cross_section_vegetation_label_widget = custom_form.dialog.findChild(
        QObject, f"{prefix}cross_section_vegetation_label"
    )
    cross_section_vegetation_widget = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_vegetation_widget")
    cross_section_vegetation_clear = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_vegetation_clear")
    cross_section_vegetation_copy = custom_form.dialog.findChild(QObject, f"{prefix}cross_section_vegetation_copy")
    single_friction_widgets = [friction_value_label_widget, friction_value_widget, friction_value_clear_widget]
    multi_friction_widgets = [
        cross_section_friction_label_widget,
        cross_section_friction_widget,
        cross_section_friction_clear,
        cross_section_friction_copy,
    ]
    single_vege_widgets = [
        vegetation_stem_density_label_widget,
        vegetation_stem_density_widget,
        vegetation_stem_density_clear_widget,
        vegetation_stem_diameter_label_widget,
        vegetation_stem_diameter_widget,
        vegetation_stem_diameter_clear_widget,
        vegetation_height_label_widget,
        vegetation_height_widget,
        vegetation_height_clear_widget,
        vegetation_drag_coefficient_label_widget,
        vegetation_drag_coefficient_widget,
        vegetation_drag_coefficient_clear_widget,
    ]
    multi_vege_widgets = [
        cross_section_vegetation_label_widget,
        cross_section_vegetation_widget,
        cross_section_vegetation_clear,
        cross_section_vegetation_copy,
    ]
    all_related_widgets = single_friction_widgets + multi_friction_widgets + single_vege_widgets + multi_vege_widgets
    for related_widget in all_related_widgets:
        related_widget.setDisabled(True)
    cross_section_shape = custom_form.get_widget_value(cross_section_shape_widget)
    friction_value = custom_form.get_widget_value(friction_widget)
    custom_form.update_cross_section_table_header("cross_section_friction_values")
    custom_form.update_cross_section_table_header("cross_section_vegetation_table")
    if not custom_form.layer.isEditable():
        return
    if cross_section_shape == en.CrossSectionShape.YZ.value:
        if friction_value == en.FrictionTypeExtended.CHEZY.value:
            related_widgets = single_friction_widgets + single_vege_widgets
        elif friction_value == en.FrictionTypeExtended.MANNING.value:
            related_widgets = single_friction_widgets
        elif friction_value == en.FrictionTypeExtended.CHEZY_WITH_CONVEYANCE.value:
            related_widgets = (
                single_friction_widgets + multi_friction_widgets + single_vege_widgets + multi_vege_widgets
            )
        elif friction_value == en.FrictionTypeExtended.MANNING_WITH_CONVEYANCE.value:
            related_widgets = single_friction_widgets + multi_friction_widgets
        else:
            related_widgets = []
    elif cross_section_shape in {
        en.CrossSectionShape.TABULATED_RECTANGLE.value,
        en.CrossSectionShape.TABULATED_TRAPEZIUM.value,
    }:
        if friction_value == en.FrictionTypeExtended.CHEZY.value:
            related_widgets = single_friction_widgets
        elif friction_value == en.FrictionTypeExtended.MANNING.value:
            related_widgets = single_friction_widgets
        elif friction_value == en.FrictionTypeExtended.CHEZY_WITH_CONVEYANCE.value:
            related_widgets = single_friction_widgets + single_vege_widgets
        elif friction_value == en.FrictionTypeExtended.MANNING_WITH_CONVEYANCE.value:
            related_widgets = single_friction_widgets
        else:
            related_widgets = []
    else:
        related_widgets = single_friction_widgets
    for related_widget in related_widgets:
        related_widget.setEnabled(True)


def setup_cross_section_definition_widgets(custom_form, shape_widget, friction_widget, prefix=""):
    """Setup cross section definition dependent widgets."""
    if shape_widget is not None:
        setup_cross_section_widgets(custom_form, shape_widget, prefix)
    if custom_form.MODEL in [dm.CrossSectionLocation, dm.Channel]:
        setup_friction_and_vegetation_widgets(custom_form, shape_widget, friction_widget, prefix)


class NumericItemDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator(editor)
        validator.setBottom(0)
        validator.setDecimals(3)
        validator.setNotation(QDoubleValidator.StandardNotation)
        editor.setValidator(validator)
        return editor


def get_plugin_instance(plugin_name="threedi_schematisation_editor"):
    """Return given plugin name instance."""
    try:
        plugin_instance = plugins[plugin_name]
    except AttributeError:
        plugin_instance = None
    return plugin_instance


def extract_multiple_substrings(linestring_geometry, *start_end_distances):
    """
    Cut out line segments between given start and end distances along the line and return them with a line leftovers.
    """
    curve = linestring_geometry.constGet()
    start_end_distances.sort(key=itemgetter(0))
    substring_geometries, linestring_parts_left = [], []
    before_substring_start, before_substring_end = 0, 0
    for start_distance, end_distance in start_end_distances:
        curve_substring = curve.curveSubstring(start_distance, end_distance)
        substring_geometry = QgsGeometry(curve_substring)
        substring_geometries.append(substring_geometry)
        before_substring_end = start_distance
        before_substring_curve = curve.curveSubstring(before_substring_start, before_substring_end)
        before_substring_geometry = QgsGeometry(before_substring_curve)
        before_substring_start = end_distance
        linestring_parts_left.append(before_substring_geometry)
    last_substring_curve = curve.curveSubstring(before_substring_start, linestring_geometry.length())
    last_substring_geometry = QgsGeometry(last_substring_curve)
    linestring_parts_left.append(last_substring_geometry)
    return substring_geometries, linestring_parts_left


def extract_substring(linestring_geometry, start_distance, end_distance):
    """Cut out line segment between given start and end distance along the line and return it with a line leftovers."""
    curve = linestring_geometry.constGet()
    curve_substring = curve.curveSubstring(start_distance, end_distance)
    before_start_substring = curve.curveSubstring(0, start_distance)
    after_end_substring = curve.curveSubstring(end_distance, linestring_geometry.length())
    substring_geometry = QgsGeometry(curve_substring)
    before_start_geometry = QgsGeometry(before_start_substring)
    after_end_geometry = QgsGeometry(after_end_substring)
    return substring_geometry, before_start_geometry, after_end_geometry
