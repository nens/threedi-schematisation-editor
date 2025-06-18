# Copyright (C) 2025 by Lutra Consulting
import json

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFile,
    QgsProcessingParameterFeatureSource,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.custom_tools.importers import (
    ConnectionNodesImporter,
    CulvertsImporter,
    CulvertsIntegrator,
    OrificesImporter,
    OrificesIntegrator,
    PipesImporter,
    WeirsImporter,
    WeirsIntegrator,
)


class BaseImporter(QgsProcessingAlgorithm):
    """Base class for all importers."""

    SOURCE_LAYER = "SOURCE_LAYER"
    IMPORT_CONFIG = "IMPORT_CONFIG"
    TARGET_GPKG = "TARGET_GPKG"
    FEATURE_TYPE = ""  # To be overridden by subclasses

    def createInstance(self):
        return self.__class__()

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def group(self):
        return self.tr("Conversion")

    def groupId(self):
        return "conversion"

    def name(self):
        return f"threedi_import_{self.FEATURE_TYPE}s"

    def displayName(self):
        return self.tr(f"Import {self.get_feature_repr()}s")

    def shortHelpString(self):
        return self.tr(f"""Import {self.get_feature_repr()}s from the external source layer.""")

    def get_feature_repr(self):
        return self.FEATURE_TYPE.replace('_',' ')

    def initAlgorithm(self, config=None):
        source_layer = QgsProcessingParameterFeatureSource(
            self.SOURCE_LAYER,
            self.tr(f"Source {self.get_feature_repr()} layer"),
            self.get_source_layer_types(),
        )
        self.addParameter(source_layer)
        import_config_file = QgsProcessingParameterFile(
            self.IMPORT_CONFIG,
            self.tr(f"{self.get_feature_repr().title()} import configuration file"),
            extension="json",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(import_config_file)
        target_gpkg = QgsProcessingParameterFile(
            self.TARGET_GPKG,
            self.tr("Target schematisation database"),
            extension="gpkg",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(target_gpkg)

    def get_source_layer_types(self):
        # Default is both line and point, overridden in connection nodes
        return [QgsProcessing.TypeVectorLine, QgsProcessing.TypeVectorPoint]

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}

    def create_importer(self, source_layer, target_gpkg, import_config):
        """Create the appropriate importer instance."""
        raise NotImplementedError("Subclasses must implement create_importer()")

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

        importer = self.create_importer(source_layer, target_gpkg, import_config)

        # Use the right import method based on the importer type
        if hasattr(importer, 'import_features'):
            importer.import_features(context=context)
        else:
            importer.import_structures(context=context)

        importer.commit_pending_changes()
        return {}


class SimpleImporter(BaseImporter):
    IMPORTER_CLASS = None  # To be overridden by subclasses

    def create_importer(self, source_layer, target_gpkg, import_config):
        return self.IMPORTER_CLASS(source_layer, target_gpkg, import_config)


class ImportConnectionNodes(SimpleImporter):
    """Import connection nodes."""
    IMPORTER_CLASS = ConnectionNodesImporter
    FEATURE_TYPE = "connection_node"  # To be overridden by subclasses

    def get_source_layer_types(self):
        return [QgsProcessing.TypeVectorPoint]


class ImportPipes(SimpleImporter):
    """Import pipes."""
    IMPORTER_CLASS = PipesImporter
    FEATURE_TYPE = "pipe"  # To be overridden by subclasses


class StructureImporter(BaseImporter):
    """Base class for importing different feature types."""
    IMPORTER_CLASS = None  # To be overridden by subclasses
    INTEGRATOR_CLASS = None  # To be overridden by subclasses

    def create_importer(self, source_layer, target_gpkg, import_config):
        conversion_settings = import_config["conversion_settings"]
        edit_channels = conversion_settings.get("edit_channels", False)

        if edit_channels:
            return self.INTEGRATOR_CLASS(source_layer, target_gpkg, import_config)
        else:
            return self.IMPORTER_CLASS(source_layer, target_gpkg, import_config)


class ImportCulverts(StructureImporter):
    """Import culverts."""
    FEATURE_TYPE = "culvert"
    IMPORTER_CLASS = CulvertsImporter
    INTEGRATOR_CLASS = CulvertsIntegrator


class ImportOrifices(StructureImporter):
    """Import orifices."""
    FEATURE_TYPE = "orifice"
    IMPORTER_CLASS = OrificesImporter
    INTEGRATOR_CLASS = OrificesIntegrator


class ImportWeirs(StructureImporter):
    """Import weirs."""
    FEATURE_TYPE = "weir"
    IMPORTER_CLASS = WeirsImporter
    INTEGRATOR_CLASS = WeirsIntegrator


