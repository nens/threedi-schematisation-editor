# Copyright (C) 2025 by Lutra Consulting
from pathlib import Path

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputFile,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsVectorLayer,
)


class ExtractLayerByNameAlgorithm(QgsProcessingAlgorithm):
    """
    Extract a layer by name from a GeoPackage
    """

    INPUT_GPKG = "INPUT_GPKG"
    LAYER_NAME = "LAYER_NAME"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config=None):
        # GeoPackage input (file)
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_GPKG, description="Source geopackage", extension="gpkg"
            )
        )

        # Layer name input (string)
        self.addParameter(
            QgsProcessingParameterString(self.LAYER_NAME, description="Layer name")
        )

        # Define output layer
        self.addOutput(
            QgsProcessingOutputVectorLayer(self.OUTPUT, description="Extracted layer")
        )

    def processAlgorithm(self, parameters, context, feedback):
        gpkg = self.parameterAsFile(parameters, self.INPUT_GPKG, context)
        layer_name = self.parameterAsString(parameters, self.LAYER_NAME, context)

        uri = f"{gpkg}|layername={layer_name}"
        layer = QgsVectorLayer(uri, layer_name, "ogr")

        if not layer.isValid():
            raise QgsProcessingException(f"Layer '{layer_name}' not found in {gpkg}")

        # return as output
        return {self.OUTPUT: layer.source()}

    def name(self):
        return "extract_layer_by_name"

    def displayName(self):
        return "Extract layer by name"

    def shortHelpString(self):
        return """
            Utility algorithm to select a layer from an input geopackage file. 
            Useful when automating importer workflows in the Processing Model Builder.
            """

    def group(self):
        return "Import utilities"

    def groupId(self):
        return "import_utils"

    def createInstance(self):
        return ExtractLayerByNameAlgorithm()


class GetConfigFileAlgorithm(QgsProcessingAlgorithm):
    CONFIG_DIR = "CONFIG_DIR"
    BASE_NAME = "BASE_NAME"
    OUTPUT_JSON = "OUTPUT_JSON"

    def initAlgorithm(self, config=None):
        # Directory containing config JSONs
        self.addParameter(
            QgsProcessingParameterFile(
                self.CONFIG_DIR,
                description="Directory containing config JSON files",
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        # Base name for the config file (without .json)
        self.addParameter(
            QgsProcessingParameterString(
                self.BASE_NAME,
                description="Config file base name (without .json, e.g. 'channels')",
            )
        )

        # Output JSON file path
        self.addOutput(
            QgsProcessingOutputFile(self.OUTPUT_JSON, description="Config JSON file")
        )

    def processAlgorithm(self, parameters, context, feedback):
        config_dir = Path(self.parameterAsFile(parameters, self.CONFIG_DIR, context))
        base_name = self.parameterAsString(parameters, self.BASE_NAME, context).strip()

        # Build expected file path
        json_file = config_dir / f"{base_name}.json"

        if not json_file.exists():
            raise QgsProcessingException(f"Config file not found: {json_file}")

        return {self.OUTPUT_JSON: str(json_file)}

    def name(self):
        return "get_config_file"

    def displayName(self):
        return "Get config file from directory"

    def shortHelpString(self):
        return """
            Utility algorithm to select a vector data importer configuration file (.json) from a directory. 
            Useful when automating importer workflows in the Processing Model Builder.
            """

    def group(self):
        return "Import utilities"

    def groupId(self):
        return "import_utils"

    def createInstance(self):
        return GetConfigFileAlgorithm()
