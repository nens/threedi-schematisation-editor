# Copyright (C) 2023 by Lutra Consulting
import json
from enum import Enum

from qgis.core import (
    NULL,
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsPointLocator,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import find_line_endpoints_nodes, get_next_feature_id, gpkg_layer


class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    IGNORE = "ignore"


class ImportCulverts(QgsProcessingAlgorithm):
    """Import culverts."""

    SOURCE_LAYER = "SOURCE_LAYER"
    IMPORT_CONFIG = "IMPORT_CONFIG"
    TARGET_GPKG = "TARGET_GPKG"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ImportCulverts()

    def name(self):
        return "threedi_import_culverts"

    def displayName(self):
        return self.tr("Import culverts")

    def group(self):
        return self.tr("Conversion")

    def groupId(self):
        return "conversion"

    def shortHelpString(self):
        return self.tr("""Import culverts from external source layer.""")

    def initAlgorithm(self, config=None):
        source_layer = QgsProcessingParameterFeatureSource(
            self.SOURCE_LAYER,
            self.tr("Source culvert layer"),
            [QgsProcessing.TypeVectorLine],
        )
        self.addParameter(source_layer)
        import_config_file = QgsProcessingParameterFile(
            self.IMPORT_CONFIG,
            self.tr("Culvert import configuration file"),
            extension="json",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(import_config_file)
        target_gpkg = QgsProcessingParameterFile(
            self.TARGET_GPKG,
            self.tr("Target Schematisation Editor GeoPackage file"),
            extension="gpkg",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(target_gpkg)

    def processAlgorithm(self, parameters, context, feedback):
        source_layer = self.parameterAsSource(parameters, self.SOURCE_LAYER, context)
        if source_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SOURCE_LAYER))
        import_config_file = self.parameterAsFile(parameters, self.IMPORT_CONFIG, context)
        if import_config_file is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.IMPORT_CONFIG))
        target_gpkg = self.parameterAsFile(parameters, self.TARGET_GPKG, context)
        if target_gpkg is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.TARGET_GPKG))
        culvert_layer = gpkg_layer(target_gpkg, dm.Culvert.__tablename__)
        if not culvert_layer.isValid():
            raise QgsProcessingException(self.invalidSourceError(parameters, self.TARGET_GPKG))
        with open(import_config_file) as import_config_json:
            import_config = json.loads(import_config_json.read())
        node_layer = gpkg_layer(target_gpkg, dm.ConnectionNode.__tablename__)
        conversion_settings = import_config["conversion_settings"]
        use_snapping = conversion_settings.get("use_snapping", False)
        snapping_distance = conversion_settings.get("snapping_distance", 0.1)
        fields_config = import_config["fields"]
        culvert_fields = culvert_layer.fields()
        node_fields = node_layer.fields()
        project = context.project()
        src_crs = source_layer.sourceCrs()
        dst_crs = culvert_layer.crs()
        transform_ctx = project.transformContext()
        transformation = QgsCoordinateTransform(src_crs, dst_crs, transform_ctx) if src_crs != dst_crs else None
        next_culvert_id = get_next_feature_id(culvert_layer)
        next_connection_node_id = get_next_feature_id(node_layer)
        locator = QgsPointLocator(node_layer, dst_crs, transform_ctx)
        new_culverts = []
        node_layer.startEditing()
        culvert_layer.startEditing()
        for src_feat in source_layer.getFeatures():
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
                    node_end_point = polyline[-1]
                    new_end_node_feat = QgsFeature(node_fields)
                    new_end_node_feat.setGeometry(QgsGeometry.fromPointXY(node_end_point))
                    new_end_node_feat["id"] = next_connection_node_id
                    new_culvert_feat["connection_node_end_id"] = next_connection_node_id
                    next_connection_node_id += 1
                    new_nodes.append(new_end_node_feat)
            else:
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
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}
