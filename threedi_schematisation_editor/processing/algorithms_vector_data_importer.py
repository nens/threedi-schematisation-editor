# Copyright (C) 2025 by Nelen & Schuurmans
import json

from pydantic import ValidationError
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingOutputFile,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QCoreApplication

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.importers import (
    ChannelsImporter,
    ConnectionNodesImporter,
    CrossSectionDataImporter,
    CrossSectionLocationImporter,
    CulvertsImporter,
    OrificesImporter,
    PipesImporter,
    SurfaceImporter,
    WeirsImporter,
)
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ImportSettings,
    IntegrationMode,
    validate_field_map,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    compute_selected_ids,
)


def load_import_settings(file_path, model_cls, connection_node_model_cls=None):
    """Load and fully validate import settings from a JSON file.

    Handles JSON parse errors, ImportSettings validation, and field map
    validation against the target model class and (optionally) the connection
    node model class.
    Raises QgsProcessingException on any failure.
    """
    try:
        with open(file_path) as f:
            import_settings_dict = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise QgsProcessingException(
            f"Could not read import config {file_path}: {e}"
        ) from e

    try:
        import_config = ImportSettings(**import_settings_dict)
    except ValidationError as e:
        raise QgsProcessingException(f"Invalid import settings: {e}") from e

    if model_cls is not None:
        try:
            validate_field_map(import_config.fields, model_cls)
        except ValidationError as e:
            raise QgsProcessingException(f"Invalid field map (fields): {e}") from e

    if connection_node_model_cls is not None:
        try:
            validate_field_map(
                import_config.connection_node_fields, connection_node_model_cls
            )
        except ValidationError as e:
            raise QgsProcessingException(
                f"Invalid field map (connection_node_fields): {e}"
            ) from e

    return import_config


class BaseImporter(QgsProcessingAlgorithm):
    """Base class for all importers."""

    SOURCE_LAYER = "SOURCE_LAYER"
    IMPORT_CONFIG = "IMPORT_CONFIG"
    TARGET_GPKG = "TARGET_GPKG"
    FEATURE_TYPE = ""  # To be overridden by subclasses
    TARGET_MODEL_CLS = None  # Override in subclasses that have a single target model
    CONNECTION_NODE_MODEL_CLS = (
        None  # Override in subclasses that validate connection_node_fields
    )

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

        # Hidden file output. Not shown in UI, but available in processing model builder
        self.addOutput(
            QgsProcessingOutputFile(self.TARGET_GPKG, "Target schematisation database")
        )

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

        import_config = load_import_settings(
            import_config_file, self.TARGET_MODEL_CLS, self.CONNECTION_NODE_MODEL_CLS
        )

        importer = self.create_importer(source_layer, target_gpkg, import_config)

        # The source_layer from the UI takes priority over any layer name in the config.
        # include_expression from the config is applied against the UI-selected layer.
        selected_ids = compute_selected_ids(source_layer, import_config.source)
        importer.import_features(context=context, selected_ids=selected_ids)
        importer.commit_pending_changes()
        return {self.TARGET_GPKG: target_gpkg}


class SimpleImporter(BaseImporter):
    IMPORTER_CLASS = None  # To be overridden by subclasses

    def create_importer(self, source_layer, target_gpkg, import_config):
        return self.IMPORTER_CLASS(source_layer, target_gpkg, import_config)


class ImportConnectionNodes(SimpleImporter):
    """Import connection nodes."""

    IMPORTER_CLASS = ConnectionNodesImporter
    FEATURE_TYPE = "connection_node"
    TARGET_MODEL_CLS = dm.ConnectionNode

    def get_source_layer_types(self):
        return [QgsProcessing.TypeVectorPoint]


class ImportPipes(SimpleImporter):
    """Import pipes."""

    IMPORTER_CLASS = PipesImporter
    FEATURE_TYPE = "pipe"
    TARGET_MODEL_CLS = dm.Pipe


class ImportChannels(SimpleImporter):
    """Import channels."""

    IMPORTER_CLASS = ChannelsImporter
    FEATURE_TYPE = "channel"
    TARGET_MODEL_CLS = dm.Channel


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
    TARGET_MODEL_CLS = dm.Culvert
    CONNECTION_NODE_MODEL_CLS = dm.ConnectionNode


class ImportOrifices(StructureImporter):
    """Import orifices."""

    FEATURE_TYPE = "orifice"
    IMPORTER_CLASS = OrificesImporter
    INTEGRATOR_CLASS = OrificesImporter
    TARGET_MODEL_CLS = dm.Orifice
    CONNECTION_NODE_MODEL_CLS = dm.ConnectionNode


class ImportWeirs(StructureImporter):
    """Import weirs."""

    FEATURE_TYPE = "weir"
    IMPORTER_CLASS = WeirsImporter
    INTEGRATOR_CLASS = WeirsImporter
    TARGET_MODEL_CLS = dm.Weir
    CONNECTION_NODE_MODEL_CLS = dm.ConnectionNode


class ImportCrossSectionLocation(SimpleImporter):
    IMPORTER_CLASS = CrossSectionLocationImporter
    FEATURE_TYPE = "cross_section_location"
    TARGET_MODEL_CLS = dm.CrossSectionLocation

    def get_source_layer_types(self):
        return [
            QgsProcessing.TypeVectorPoint,
            QgsProcessing.TypeVectorLine,
            QgsProcessing.TypeVector,
        ]


class ImportCrossSectionData(SimpleImporter):
    IMPORTER_CLASS = CrossSectionDataImporter
    FEATURE_TYPE = "cross_section_data"
    # TARGET_MODEL_CLS is intentionally not set: CrossSectionData is a virtual
    # import-only class with no single target model.

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


class ImportSurfaces(SimpleImporter):
    IMPORTER_CLASS = SurfaceImporter
    FEATURE_TYPE = "surface"
    TARGET_MODEL_CLS = dm.Surface

    def get_source_layer_types(self):
        return [QgsProcessing.TypeVectorPolygon]
