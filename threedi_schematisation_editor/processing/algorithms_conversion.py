# Copyright (C) 2023 by Lutra Consulting
import json

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.custom_tools import import_culverts


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
        with open(import_config_file) as import_config_json:
            import_config = json.loads(import_config_json.read())
        import_culverts(source_layer, target_gpkg, import_config, context)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}
