import os
import sys
import shutil
import threedi_model_builder.data_models as dm
from enum import Enum
from collections import OrderedDict
from qgis.PyQt.QtCore import QSettings, QVariant
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import (
    QgsDataSourceUri,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsField,
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
    """We need to change True/False from GeoPackage layers to 0/1 integers used in Spatialite layers."""
    if value is True:
        return 1
    elif value is False:
        return 0
    else:
        return value


def vector_layer_factory(annotated_model_cls, epsg=4326):
    fields = []
    geometry_type = annotated_model_cls.__geometrytype__.value
    layer_name = annotated_model_cls.__tablename__
    uri = f"{geometry_type}?crs=EPSG:{epsg}"
    layer = QgsVectorLayer(uri, layer_name, "memory")
    for field_name, field_type in annotated_model_cls.__annotations__.items():
        if issubclass(field_type, Enum):
            field_type = type(next(iter(field_type[i].value for i in field_type.__members__)))
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


def layer_to_gpkg(layer, gpkg_filename, overwrite=False, driver_name="GPKG"):
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
    return writer


def gpkg_layer(gpkg_path, table_name, layer_name=None):
    uri = f"{gpkg_path}|layername={table_name}"
    layer_name = table_name if layer_name is None else layer_name
    vlayer = QgsVectorLayer(uri, layer_name, "ogr")
    return vlayer


def sqlite_layer(sqlite_path, table_name, layer_name=None, geom_column="the_geom", schema=""):
    uri = QgsDataSourceUri()
    uri.setDatabase(sqlite_path)
    uri.setDataSource(schema, table_name, geom_column)
    layer_name = table_name if layer_name is None else layer_name
    vlayer = QgsVectorLayer(uri.uri(), layer_name, "spatialite")
    return vlayer


def create_empty_model(export_sqlite_path):
    empty_sqlite = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "empty.sqlite")
    shutil.copy(empty_sqlite, export_sqlite_path)


def get_qml_style_path(style_name, *subfolders):
    qml_filename = f"{style_name}.qml"
    filepath = os.path.join(os.path.dirname(__file__), "styles", *subfolders, qml_filename)
    if os.path.isfile(filepath):
        return filepath
    return None


def get_form_ui_path(table_name):
    ui_filename = f"{table_name}.ui"
    filepath = os.path.join(os.path.dirname(__file__), "forms", "ui", ui_filename)
    if os.path.isfile(filepath):
        return filepath
    return None


def get_tree_group(name, create=True, insert_at_top=False):
    root = QgsProject.instance().layerTreeRoot()
    grp = root.findGroup(name)
    if not grp and create:
        grp = QgsLayerTreeGroup(name)
        root.insertChildNode(0 if insert_at_top else -1, grp)
    return grp


def add_layer_to_group(name, layer, bottom=False):
    grp = QgsProject.instance().layerTreeRoot().findGroup(name)
    if not grp:
        return
    QgsProject.instance().addMapLayer(layer, False)
    grp.insertChildNode(-1 if bottom else 0, QgsLayerTreeLayer(layer))


def remove_layer(layer):
    QgsProject.instance().removeMapLayer(layer)


def remove_group_with_children(name):
    root = QgsProject.instance().layerTreeRoot()
    group = root.findGroup(name)
    if group is not None:
        for child in group.children():
            QgsProject.instance().removeMapLayer(child.layerId())
        root.removeChildNode(group)


def get_filepath(parent, filter=None, extension=None, save=True, dialog_title=None):
    if filter is None:
        filter = "All Files (*.*)"

    if dialog_title is None:
        dialog_title = "Choose file"

    starting_dir = QSettings().value("threedi_mb/last_folder", os.path.expanduser("~"), type=str)
    if save is True:
        file_name, __ = QFileDialog.getSaveFileName(parent, dialog_title, starting_dir, filter)
    else:
        file_name, __ = QFileDialog.getOpenFileName(parent, dialog_title, starting_dir, filter)
    if len(file_name) == 0:
        return None

    if extension:
        if not file_name.endswith(extension):
            file_name += extension

    QSettings().setValue("threedi_mb/last_folder", os.path.dirname(file_name))
    return file_name


def load_user_layers(gpkg_path):
    groups = OrderedDict()
    groups["1D"] = dm.MODEL_1D_ELEMENTS
    groups["2D"] = dm.MODEL_2D_ELEMENTS
    groups["Inflow"] = dm.INFLOW_ELEMENTS
    groups["Settings"] = dm.SETTINGS_ELEMENTS
    for group_name, group_models in groups.items():
        get_tree_group(group_name)
        for model_cls in group_models:
            vlayer = gpkg_layer(gpkg_path, model_cls.__tablename__, model_cls.__layername__)
            qml_path = get_qml_style_path(model_cls.__tablename__)
            if qml_path is not None:
                vlayer.loadNamedStyle(qml_path)
            add_layer_to_group(group_name, vlayer, bottom=True)
    load_model_raster_layers(gpkg_path)


def load_model_raster_layers(gpkg_path):
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
    signal.connect(slot)


def disconnect_signal(signal, slot):
    try:
        signal.disconnect(slot)
    except TypeError:
        pass


def find_point_node(point, node_layer, locator=None):
    if not locator:
        locator = QgsPointLocator(node_layer)
    connection_node_feat = None
    match = locator.nearestVertex(point, tolerance=0.0)
    match_layer = match.layer()
    if match_layer:
        node_fid = match.featureId()
        connection_node_feat = match_layer.getFeature(node_fid)
    return connection_node_feat


def find_linestring_nodes(linestring, node_layer, locator=None):
    if not locator:
        locator = QgsPointLocator(node_layer)
    connection_node_start_feat = None
    connection_node_end_feat = None
    start_point, end_point = linestring[0], linestring[-1]
    start_match = locator.nearestVertex(start_point, tolerance=0.0)
    end_match = locator.nearestVertex(end_point, tolerance=0.0)
    start_match_layer = start_match.layer()
    end_match_layer = end_match.layer()
    if start_match_layer:
        start_node_fid = start_match.featureId()
        connection_node_start_feat = start_match_layer.getFeature(start_node_fid)
    if end_match_layer:
        end_node_fid = end_match.featureId()
        connection_node_end_feat = end_match_layer.getFeature(end_node_fid)
    return connection_node_start_feat, connection_node_end_feat


def count_vertices(geometry):
    c = sum(1 for _ in geometry.vertices())
    return c


def get_qgis(qgis_build_path="C:/OSGeo4W64/apps/qgis", qgis_proj_path="C:/OSGeo4W64/share/proj"):
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
