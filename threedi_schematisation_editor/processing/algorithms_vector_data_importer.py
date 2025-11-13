# Copyright (C) 2025 by Lutra Consulting
import json

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.vector_data_importer.importers import (
    ChannelsImporter,
    ConnectionNodesImporter,
    CrossSectionDataImporter,
    CrossSectionLocationImporter,
    CulvertsImporter,
    OrificesImporter,
    PipesImporter,
    WeirsImporter,
)
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ImportSettings,
    IntegrationMode,
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
        return self.tr("Import")

    def groupId(self):
        return "import"

    def name(self):
        return f"threedi_import_{self.FEATURE_TYPE}s"

    def displayName(self):
        return self.tr(f"Import {self.get_feature_repr()}s")

    def shortHelpString(self):
        return self.tr(
            f"""Import {self.get_feature_repr()}s from the external source layer."""
        )

    def get_feature_repr(self):
        return self.FEATURE_TYPE.replace("_", " ")

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
        # Try to load input as vector layer
        source_layer = self.parameterAsVectorLayer(parameters, "INPUT", context)
        # If that doesn't work, do some dirty magic to make a vector layer
        if not source_layer:
            source = self.parameterAsSource(parameters, self.SOURCE_LAYER, context)
            feedback.pushInfo(
                "Using self.parameterAsSource() method to load the source layer as no source layer was directly available."
            )
            source_layer = QgsVectorLayer(
                f"{QgsWkbTypes.displayString(source.wkbType())}?crs={source.sourceCrs().authid()}",
                "temp_layer",
                "memory",
            )
            # Set up the fields
            provider = source_layer.dataProvider()
            provider.addAttributes(source.fields().toList())
            source_layer.updateFields()

            # Add features
            features = list(source.getFeatures())
            provider.addFeatures(features)

        if source_layer is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.SOURCE_LAYER)
            )
        import_config_file = self.parameterAsFile(
            parameters, self.IMPORT_CONFIG, context
        )
        if import_config_file is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.IMPORT_CONFIG)
            )
        target_gpkg = self.parameterAsFile(parameters, self.TARGET_GPKG, context)
        if target_gpkg is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.TARGET_GPKG)
            )

        with open(import_config_file) as import_config_json:
            import_settings_dict = json.loads(import_config_json.read())
        import_config = ImportSettings(**import_settings_dict)

        importer = self.create_importer(source_layer, target_gpkg, import_config)

        # Use the right import method based on the importer type
        importer.import_features(context=context)
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
    FEATURE_TYPE = "pipe"


class ImportChannels(SimpleImporter):
    """Import channels."""

    IMPORTER_CLASS = ChannelsImporter
    FEATURE_TYPE = "channel"


class StructureImporter(BaseImporter):
    """Base class for importing different feature types."""

    IMPORTER_CLASS = None  # To be overridden by subclasses
    INTEGRATOR_CLASS = None  # To be overridden by subclasses

    def create_importer(self, source_layer, target_gpkg, import_config):
        integration_mode = import_config.integration.integration_mode
        if integration_mode == IntegrationMode.NONE:
            return self.IMPORTER_CLASS(source_layer, target_gpkg, import_config)
        else:
            return self.INTEGRATOR_CLASS(source_layer, target_gpkg, import_config)


class ImportCulverts(StructureImporter):
    """Import culverts."""

    FEATURE_TYPE = "culvert"
    IMPORTER_CLASS = CulvertsImporter
    INTEGRATOR_CLASS = CulvertsImporter


class ImportOrifices(StructureImporter):
    """Import orifices."""

    FEATURE_TYPE = "orifice"
    IMPORTER_CLASS = OrificesImporter
    INTEGRATOR_CLASS = OrificesImporter


class ImportWeirs(StructureImporter):
    """Import weirs."""

    FEATURE_TYPE = "weir"
    IMPORTER_CLASS = WeirsImporter
    INTEGRATOR_CLASS = WeirsImporter


class ImportCrossSectionLocation(SimpleImporter):
    IMPORTER_CLASS = CrossSectionLocationImporter
    FEATURE_TYPE = "cross_section_location"

    def get_source_layer_types(self):
        return [
            QgsProcessing.TypeVectorPoint,
            QgsProcessing.TypeVectorLine,
            QgsProcessing.TypeVector,
        ]


class ImportCrossSectionData(SimpleImporter):
    IMPORTER_CLASS = CrossSectionDataImporter
    FEATURE_TYPE = "cross_section_data"

    def get_source_layer_types(self):
        return [
            QgsProcessing.TypeVectorPoint,
            QgsProcessing.TypeVectorLine,
            QgsProcessing.TypeVector,
        ]

    def name(self):
        return f"threedi_import_{self.FEATURE_TYPE}"

    def displayName(self):
        return self.tr(f"Import {self.get_feature_repr()}")

    def shortHelpString(self):
        return self.tr(
            f"""Import {self.get_feature_repr()} from the external source layer."""
        )
