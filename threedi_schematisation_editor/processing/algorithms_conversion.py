# Copyright (C) 2023 by Lutra Consulting
import json

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterNumber,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication
from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.custom_tools import CulvertsImporter
from threedi_schematisation_editor.mike.mike_model_converter import MIKEConverter
from threedi_schematisation_editor.utils import (
    PointStructuresWelder,
    gpkg_layer,
)


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
        culverts_importer = CulvertsImporter(source_layer, target_gpkg, import_config)
        success, commit_errors = culverts_importer.import_culverts(context=context)
        if not success:
            commit_errors_message = "\n".join(commit_errors)
            feedback.reportError(commit_errors_message)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}


class ImportFromMike11(QgsProcessingAlgorithm):
    INPUT_SIM11 = "INPUT_SIM11"
    OUTPUT_GPKG = "OUTPUT_GPKG"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ImportFromMike11()

    def name(self):
        return "threedi_import_from_mike11"

    def displayName(self):
        return self.tr("Import data from MIKE11 model")

    def shortHelpString(self):
        return self.tr("""Import MIKE11 model data into 3Di schematisation structure.""")

    def group(self):
        return self.tr("Conversion")

    def groupId(self):
        return "conversion"

    def initAlgorithm(self, config=None):
        sim11_filepath = QgsProcessingParameterFile(
            self.INPUT_SIM11,
            self.tr("Mike11 simulation file"),
            extension="sim11",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(sim11_filepath)
        output_gpkg_filepath = QgsProcessingParameterFileDestination(
            self.OUTPUT_GPKG,
            self.tr("Target Schematisation Editor GeoPackage file"),
            fileFilter="*.gpkg",
        )
        self.addParameter(output_gpkg_filepath)

    def processAlgorithm(self, parameters, context, feedback):
        sim11_filepath = self.parameterAsFile(parameters, self.INPUT_SIM11, context)
        if sim11_filepath is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_SIM11))
        output_gpkg_filepath = self.parameterAsFileOutput(parameters, self.OUTPUT_GPKG, context)
        if output_gpkg_filepath is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OUTPUT_GPKG))
        mc = MIKEConverter(sim11_filepath, output_gpkg_filepath)
        mc.mike2threedi()
        feedback.pushInfo("Mike11 data import finished!")
        return {}


class StructuresLineation(QgsProcessingAlgorithm):
    SCHEMATISATION_GPKG = "SCHEMATISATION_GPKG"
    STRUCTURES_GPKG = "STRUCTURES_GPKG"
    STRUCTURE_LENGTH = "STRUCTURE_LENGTH"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return StructuresLineation()

    def name(self):
        return "threedi_import_point_structures"

    def displayName(self):
        return self.tr("Import point structures")

    def shortHelpString(self):
        return self.tr("""Import point structures and convert them into 3Di compliant linestring structures.""")

    def group(self):
        return self.tr("Conversion")

    def groupId(self):
        return "conversion"

    def initAlgorithm(self, config=None):
        schematisation_gpkg_filepath = QgsProcessingParameterFile(
            self.SCHEMATISATION_GPKG,
            self.tr("3Di schematisation Geopackage file"),
            extension="gpkg",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(schematisation_gpkg_filepath)
        structures_gpkg_filepath = QgsProcessingParameterFile(
            self.STRUCTURES_GPKG,
            self.tr("Point structures Geopackage file"),
            extension="gpkg",
            behavior=QgsProcessingParameterFile.File,
        )
        self.addParameter(structures_gpkg_filepath)
        structure_length = QgsProcessingParameterNumber(
            self.STRUCTURE_LENGTH, self.tr("Structure inline length (m)"), type=1, defaultValue=10.0
        )
        structure_length.setMetadata({"widget_wrapper": {"decimals": 2}})
        structure_length.setMinimum(0.0)
        self.addParameter(structure_length)

    def processAlgorithm(self, parameters, context, feedback):
        schematisation_gpkg_filepath = self.parameterAsFile(parameters, self.SCHEMATISATION_GPKG, context)
        if schematisation_gpkg_filepath is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SCHEMATISATION_GPKG))
        structures_gpkg_filepath = self.parameterAsFile(parameters, self.STRUCTURES_GPKG, context)
        if structures_gpkg_filepath is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.STRUCTURES_GPKG))
        default_structure_length = self.parameterAsDouble(parameters, self.STRUCTURE_LENGTH, context)
        if default_structure_length is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.STRUCTURE_LENGTH))

        node_layer = gpkg_layer(schematisation_gpkg_filepath, dm.ConnectionNode.__tablename__)
        channel_layer = gpkg_layer(schematisation_gpkg_filepath, dm.Channel.__tablename__)
        cross_section_location_layer = gpkg_layer(schematisation_gpkg_filepath, dm.CrossSectionLocation.__tablename__)
        weir_layer = gpkg_layer(schematisation_gpkg_filepath, dm.Weir.__tablename__)
        culvert_layer = gpkg_layer(schematisation_gpkg_filepath, dm.Culvert.__tablename__)
        orifice_layer = gpkg_layer(schematisation_gpkg_filepath, dm.Orifice.__tablename__)

        point_weir_layer = gpkg_layer(structures_gpkg_filepath, dm.Weir.__tablename__)
        point_culvert_layer = gpkg_layer(structures_gpkg_filepath, dm.Culvert.__tablename__)
        point_orifice_layer = gpkg_layer(structures_gpkg_filepath, dm.Orifice.__tablename__)

        welder = PointStructuresWelder(
            node_layer,
            channel_layer,
            cross_section_location_layer,
            culvert_layer,
            orifice_layer,
            weir_layer,
            point_culvert_layer,
            point_orifice_layer,
            point_weir_layer,
        )
        commit_errors_message = welder.integrate_structures_with_network()
        if commit_errors_message:
            feedback.reportError(commit_errors_message)
        return {}
