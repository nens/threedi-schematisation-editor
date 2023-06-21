# Copyright (C) 2023 by Lutra Consulting
import json
from collections import defaultdict

from qgis.core import (
    QgsFeature,
    QgsGeometry,
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
    extract_substring,
    get_features_by_expression,
    get_next_feature_id,
    gpkg_layer,
    spatial_index,
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

        node_fields = node_layer.fields()
        cross_section_location_fields = cross_section_location_layer.fields()
        channel_fields = channel_layer.fields()
        weir_fields = weir_layer.fields()
        culvert_fields = culvert_layer.fields()
        orifice_fields = orifice_layer.fields()

        point_weir_layer = gpkg_layer(structures_gpkg_filepath, dm.Weir.__tablename__)
        point_culvert_layer = gpkg_layer(structures_gpkg_filepath, dm.Culvert.__tablename__)
        point_orifice_layer = gpkg_layer(structures_gpkg_filepath, dm.Orifice.__tablename__)
        structure_point_layers = [point_weir_layer, point_culvert_layer, point_orifice_layer]

        target_structures_mapping = {
            "weir": (weir_layer, weir_fields),
            "culvert": (culvert_layer, culvert_fields),
            "orifice": (orifice_layer, orifice_fields),
        }

        channels_index, channels_feat_map = spatial_index(channel_layer)
        branch_erased_geometries = defaultdict(list)
        channels_extra_node_ids = {}
        next_node_id = get_next_feature_id(node_layer)
        visited_channels = set()  # TODO: Change it to support multiple structures within single channel
        for structure_layer in structure_point_layers:
            structures_to_add = []
            structure_layer_name = structure_layer.name()
            structure_id = get_next_feature_id(structure_layer)
            target_layer, target_fields = target_structures_mapping[structure_layer_name]
            for structure_feat in structure_layer.getFeatures():
                structure_geometry = structure_feat.geometry()
                channel_fids = channels_index.intersects(structure_geometry.boundingBox())
                if not channel_fids:
                    continue
                structure_buffer = structure_geometry.buffer(0.1, 5)
                structure_length = getattr(structure_feat, "length", default_structure_length)
                half_structure_length = structure_length * 0.5
                structure_attributes = structure_feat.attributes()
                for channel_fid in channel_fids:
                    channel_feat = channels_feat_map[channel_fid]
                    channel_geometry = channel_feat.geometry()
                    if not channel_geometry.intersects(structure_buffer) or channel_fid in visited_channels:
                        continue
                    intersection_m = channel_geometry.lineLocatePoint(structure_geometry)
                    start_structure_m = intersection_m - half_structure_length
                    end_structure_m = intersection_m + half_structure_length
                    structure_line, before_structure_line, after_structure_line = extract_substring(
                        channel_geometry, start_structure_m, end_structure_m
                    )
                    new_node_end_id = next_node_id
                    next_node_id += 1
                    new_node_start_id = next_node_id
                    next_node_id += 1
                    channels_extra_node_ids[channel_fid] = (new_node_end_id, new_node_start_id)
                    structure_points = structure_line.asPolyline()
                    start_cut_point, end_cut_point = structure_points[0], structure_points[-1]
                    if structure_layer_name == "culvert":
                        structure_geometry = structure_line
                        structure_attributes.pop()
                    else:
                        structure_geometry = QgsGeometry.fromPolylineXY([start_cut_point, end_cut_point])
                    linear_structure_feat = QgsFeature(target_fields)
                    structure_attributes[0] = structure_id
                    linear_structure_feat.setAttributes(structure_attributes)
                    linear_structure_feat["connection_node_start_id"] = new_node_end_id
                    linear_structure_feat["connection_node_end_id"] = new_node_start_id
                    linear_structure_feat.setGeometry(structure_geometry)
                    structures_to_add.append(linear_structure_feat)
                    structure_id += 1
                    branch_erased_geometries[channel_fid] += [before_structure_line, after_structure_line]
                    visited_channels.add(channel_fid)
            target_layer.startEditing()
            target_layer.addFeatures(structures_to_add)
            success = target_layer.commitChanges()
            if not success:
                commit_errors = target_layer.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)

        cross_section_location_index, cross_section_location_feat_map = spatial_index(cross_section_location_layer)
        next_channel_id = get_next_feature_id(channel_layer)
        node_layer.startEditing()
        cross_section_location_layer.startEditing()
        channel_layer.startEditing()
        node_end_id_idx = channel_fields.lookupField("connection_node_end_id")
        channel_id_idx = cross_section_location_fields.lookupField("channel_id")
        new_channels, new_nodes = [], []
        for channel_fid, channel_geometries in branch_erased_geometries.items():
            structure_start_node_id, structure_end_node_id = channels_extra_node_ids[channel_fid]
            main_geom, new_channel_geom = channel_geometries
            channel_feat = channels_feat_map[channel_fid]
            # Get and update channel connection node end attributes
            connection_node_end_id = channel_feat["connection_node_end_id"]
            connection_node_end_feat = next(
                get_features_by_expression(node_layer, f'"id" = {connection_node_end_id}', True)
            )
            connection_node_end_attrs = connection_node_end_feat.attributes()
            connection_node_end_attrs[:2] = [structure_start_node_id, structure_start_node_id]
            # Get and update channel connection node start attributes
            connection_node_start_id = channel_feat["connection_node_start_id"]
            connection_node_start_feat = next(
                get_features_by_expression(node_layer, f'"id" = {connection_node_start_id}', True)
            )
            connection_node_start_attrs = connection_node_start_feat.attributes()
            connection_node_start_attrs[:2] = [structure_end_node_id, structure_end_node_id]

            channel_attributes = channel_feat.attributes()
            # Edit and add extra channels and nodes
            new_channel = QgsFeature(channel_fields)
            main_polyline = main_geom.asPolyline()
            new_connection_node_end_geom = QgsGeometry.fromPointXY(main_polyline[-1])
            new_connection_node_end_feat = QgsFeature(node_fields)
            new_connection_node_end_feat.setAttributes(connection_node_end_attrs)
            new_connection_node_end_feat.setGeometry(new_connection_node_end_geom)
            new_channel_polyline = new_channel_geom.asPolyline()
            new_connection_node_start_geom = QgsGeometry.fromPointXY(new_channel_polyline[0])
            new_connection_node_start_feat = QgsFeature(node_fields)
            new_connection_node_start_feat.setAttributes(connection_node_start_attrs)
            new_connection_node_start_feat.setGeometry(new_connection_node_start_geom)
            channel_attributes[:2] = [next_channel_id, next_channel_id]
            new_channel.setAttributes(channel_attributes)
            new_channel["connection_node_start_id"] = connection_node_start_attrs[0]
            new_channel.setGeometry(new_channel_geom)
            xs_fids = cross_section_location_index.intersects(new_channel_geom.boundingBox())
            for xs_fid in xs_fids:
                xs_feat = cross_section_location_feat_map[xs_fid]
                xs_geom = xs_feat.geometry()
                xs_buffer = xs_geom.buffer(0.1, 5)
                if new_channel_geom.intersects(xs_buffer):
                    cross_section_location_layer.changeAttributeValue(xs_fid, channel_id_idx, next_channel_id)
            next_channel_id += 1
            channel_layer.changeGeometry(channel_fid, main_geom)
            channel_layer.changeAttributeValue(channel_fid, node_end_id_idx, connection_node_end_attrs[0])
            new_channels.append(new_channel)
            new_nodes += [new_connection_node_end_feat, new_connection_node_start_feat]
        node_layer.addFeatures(new_nodes)
        channel_layer.addFeatures(new_channels)
        for layer in [node_layer, channel_layer, cross_section_location_layer]:
            success = layer.commitChanges()
            if not success:
                commit_errors = layer.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)
        return {}
