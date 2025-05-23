# Copyright (C) 2025 by Lutra Consulting
from operator import itemgetter

from qgis.core import (
    QgsFeature,
    QgsFeatureRequest,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)

from qgis.PyQt.QtCore import QCoreApplication

import json
from pathlib import Path

from threedi_schematisation_editor.enumerators import SewerageType
from threedi_schematisation_editor.utils import get_feature_by_id, get_next_feature_id, spatial_index
from threedi_schematisation_editor.data_models import SurfaceParameters


class LinkToConnectionNodesAlgorithm(QgsProcessingAlgorithm):
    """Base algorithm for linking surface or DWF polygons to connection nodes."""

    POLYGON_LAYER = "POLYGON_LAYER"
    SELECTED_POLYGONS = "SELECTED_POLYGONS"
    MAP_LAYER = "MAP_LAYER"
    PIPE_LAYER = "PIPE_LAYER"
    SELECTED_PIPES = "SELECTED_PIPES"
    NODE_LAYER = "NODE_LAYER"
    SEWERAGE_TYPES = "SEWERAGE_TYPES"
    STORMWATER_SEWER_PREFERENCE = "STORMWATER_SEWER_PREFERENCE"
    SANITARY_SEWER_PREFERENCE = "SANITARY_SEWER_PREFERENCE"
    SEARCH_DISTANCE = "SEARCH_DISTANCE"

    def parameter_names(self):
        # Not implemented as proper abstractmethod because QgsProcessingAlgorithm already has a metaclass
        # and setting ABCMeta as metaclass creates complicated problems
        return NotImplementedError("Subclasses must implement this method")

    def default_values(self):
        # Not implemented as proper abstractmethod because QgsProcessingAlgorithm already has a metaclass
        # and setting ABCMeta as metaclass creates complicated problems
        return NotImplementedError("Subclasses must implement this method")

    def polygon_id_field(self):
        # Not implemented as proper abstractmethod because QgsProcessingAlgorithm already has a metaclass
        # and setting ABCMeta as metaclass creates complicated problems
        return NotImplementedError("Subclasses must implement this method")

    def group(self):
        return "Inflow"

    def groupId(self):
        return "0d"

    def shortHelpString(self):
        return (
            f"""
            <p>Connect {self.parameter_names[self.POLYGON_LAYER]} features to the sewer system by creating {self.default_values[self.MAP_LAYER]} features. The new features are added to the {self.parameter_names[self.MAP_LAYER]} directly.</p>
            <p>For each {self.parameter_names[self.POLYGON_LAYER]} feature, the nearest pipe is found; it is mapped to the nearest of this pipe's connection nodes.</p>
            <p>In some cases, you may want to prefer e.g. stormwater drains or sanitary sewers over combined sewers. This can be done by setting the stormwater sewer preference to a value greater than zero.</p>
            <h3>Parameters</h3>
            <h4>{self.parameter_names[self.POLYGON_LAYER]}</h4>
            <p>{self.parameter_names[self.POLYGON_LAYER]} that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>{self.parameter_names[self.MAP_LAYER]}</h4>
            <p>{self.parameter_names[self.MAP_LAYER]} that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Pipe layer</h4>
            <p>Pipe layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Connection node layer</h4>
            <p>Connection node layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Sewerage types</h4>
            <p>Only pipes of the selected sewerage types will be used in the algorithm</p>
            <h4>Stormwater sewer preference</h4>
            <p>This value (in meters) will be subtracted from the distance between the {self.default_values[self.POLYGON_LAYER]} and the stormwater drain. For example: there is a combined sewer within 10 meters from the {self.default_values[self.POLYGON_LAYER]}, and a stormwater drain within 11 meters; if the stormwater sewer preference is 2 m, the algorithm will use 11 - 2 = 9 m as distance to the stormwater sewer, so the {self.default_values[self.POLYGON_LAYER]} will be mapped to one of the stormwater drain's connection nodes, instead of to the combined sewer's connection nodes.</p>
            <h4>Sanitary sewer preference</h4>
            <p>This value (in meters) will be subtracted from the distance between the {self.default_values[self.POLYGON_LAYER]} and the sanitary sewer. See 'stormwater sewer preference' for further explanation.</p>
            <h4>Search distance</h4>
            <p>Only pipes within search distance (m) from the surface will be used in the algorithm.</p>
            """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.POLYGON_LAYER,
                self.parameter_names[self.POLYGON_LAYER],
                [QgsProcessing.TypeVectorPolygon],
                defaultValue=self.default_values[self.POLYGON_LAYER],
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_POLYGONS,
                self.parameter_names[self.SELECTED_POLYGONS],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.MAP_LAYER,
                self.parameter_names[self.MAP_LAYER],
                [QgsProcessing.TypeVectorLine],
                defaultValue=self.default_values[self.MAP_LAYER],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PIPE_LAYER,
                "Pipe layer",
                [QgsProcessing.TypeVectorLine],
                defaultValue="Pipe",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_PIPES,
                "Selected pipes only",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NODE_LAYER,
                "Connection node layer",
                [QgsProcessing.TypeVectorPoint],
                defaultValue="Connection node",
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEWERAGE_TYPES,
                "Sewerage types",
                allowMultiple=True,
                options=[e.name for e in SewerageType],
                defaultValue=self.default_values[self.SEWERAGE_TYPES],
            )
        )
        storm_pref = QgsProcessingParameterNumber(
            self.STORMWATER_SEWER_PREFERENCE,
            "Stormwater sewer preference [m]",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0,
        )
        storm_pref.setMinimum(0.0)
        storm_pref.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(storm_pref)
        sanitary_pref = QgsProcessingParameterNumber(
            self.SANITARY_SEWER_PREFERENCE,
            "Sanitary sewer preference [m]",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=0.0,
        )
        sanitary_pref.setMinimum(0.0)
        sanitary_pref.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(sanitary_pref)
        search_distance = QgsProcessingParameterNumber(
            self.SEARCH_DISTANCE,
            "Search distance",
            type=QgsProcessingParameterNumber.Double,
            defaultValue=10.0,
        )
        search_distance.setMinimum(0.01)
        search_distance.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(search_distance)

    def processAlgorithm(self, parameters, context, feedback):
        surface_lyr = self.parameterAsLayer(parameters, self.POLYGON_LAYER, context)
        if surface_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.POLYGON_LAYER))
        surface_map_lyr = self.parameterAsLayer(parameters, self.MAP_LAYER, context)
        if surface_map_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.MAP_LAYER))
        selected_surfaces = self.parameterAsBool(parameters, self.SELECTED_POLYGONS, context)
        pipe_lyr = self.parameterAsLayer(parameters, self.PIPE_LAYER, context)
        if pipe_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PIPE_LAYER))
        selected_pipes = self.parameterAsBool(parameters, self.SELECTED_PIPES, context)
        node_lyr = self.parameterAsLayer(parameters, self.NODE_LAYER, context)
        if node_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.NODE_LAYER))
        sewerage_types = self.parameterAsEnums(parameters, self.SEWERAGE_TYPES, context)
        if sewerage_types is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SEWERAGE_TYPES))
        storm_pref = self.parameterAsDouble(parameters, self.STORMWATER_SEWER_PREFERENCE, context)
        if storm_pref is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.STORMWATER_SEWER_PREFERENCE))
        sanitary_pref = self.parameterAsDouble(parameters, self.SANITARY_SEWER_PREFERENCE, context)
        if sanitary_pref is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SANITARY_SEWER_PREFERENCE))
        search_distance = self.parameterAsDouble(parameters, self.SEARCH_DISTANCE, context)
        if search_distance is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SEARCH_DISTANCE))
        surface_to_pipes_distances = {}
        pipe_iterator = pipe_lyr.selectedFeatures() if selected_pipes else pipe_lyr.getFeatures()
        pipe_filter_request = QgsFeatureRequest(
            [feat.id() for feat in pipe_iterator if feat["sewerage_type"] in sewerage_types]
        )
        pipe_features, pipe_index = spatial_index(pipe_lyr, pipe_filter_request)
        feedback.setProgress(0)
        number_of_surfaces = surface_lyr.selectedFeatureCount() if selected_surfaces else surface_lyr.featureCount()
        number_of_steps = number_of_surfaces * 2
        step = 1
        for surface_feat in surface_lyr.selectedFeatures() if selected_surfaces else surface_lyr.getFeatures():
            if feedback.isCanceled():
                return {}
            surface_fid = surface_feat.id()
            surface_to_pipes_distances[surface_fid] = []
            surface_geom = surface_feat.geometry()
            if surface_geom.isNull():
                feedback.setProgress(100 * step / number_of_steps)
                step += 1
                continue
            surface_buffer = surface_geom.buffer(search_distance, 5)
            for pipe_id in pipe_index.intersects(surface_buffer.boundingBox()):
                pipe_feat = pipe_features[pipe_id]
                pipe_sewerage_type = pipe_feat["sewerage_type"]
                pipe_geometry = pipe_feat.geometry()
                surface_pipe_distance = surface_geom.distance(pipe_geometry)
                if surface_pipe_distance > search_distance:
                    continue
                if pipe_sewerage_type == SewerageType.STORM_DRAIN.value:
                    surface_pipe_distance -= storm_pref
                elif pipe_sewerage_type == SewerageType.SANITARY_SEWER.value:
                    surface_pipe_distance -= sanitary_pref
                surface_to_pipes_distances[surface_fid].append((pipe_feat.id(), surface_pipe_distance))
            feedback.setProgress(100 * step / number_of_steps)
            step += 1
        surface_map_feats = []
        surface_map_fields = surface_map_lyr.fields()
        next_surface_map_id = get_next_feature_id(surface_map_lyr)
        for surface_id, surface_pipes in surface_to_pipes_distances.items():
            if feedback.isCanceled():
                return {}
            if not surface_pipes:
                feedback.setProgress(100 * step / number_of_steps)
                step += 1
                continue
            surface_pipes.sort(key=itemgetter(1))
            surface_feat = surface_lyr.getFeature(surface_id)
            surface_geom = surface_feat.geometry()
            pipe_id, surface_pipe_distance = surface_pipes[0]
            pipe_feat = pipe_features[pipe_id]
            surface_centroid = surface_geom.pointOnSurface()
            start_node_id = pipe_feat["connection_node_id_start"]
            end_node_id = pipe_feat["connection_node_id_end"]
            start_node = get_feature_by_id(node_lyr, start_node_id)
            end_node = get_feature_by_id(node_lyr, end_node_id)
            start_node_geom = start_node.geometry()
            end_node_geom = end_node.geometry()
            surface_start_node_distance = surface_geom.distance(start_node_geom)
            surface_end_node_distance = surface_geom.distance(end_node_geom)
            if surface_start_node_distance < surface_end_node_distance:
                surface_node_id = start_node_id
                node_geom = start_node_geom
            else:
                surface_node_id = end_node_id
                node_geom = end_node_geom
            surface_map_feat = QgsFeature(surface_map_fields)
            surface_map_feat["id"] = next_surface_map_id
            surface_map_feat[self.polygon_id_field] = surface_feat["id"]
            surface_map_feat["connection_node_id"] = surface_node_id
            surface_map_feat["percentage"] = 100.0
            surface_map_geom = QgsGeometry.fromPolylineXY([surface_centroid.asPoint(), node_geom.asPoint()])
            surface_map_feat.setGeometry(surface_map_geom)
            surface_map_feats.append(surface_map_feat)
            next_surface_map_id += 1
            feedback.setProgress(100 * step / number_of_steps)
            step += 1
        if feedback.isCanceled():
            return {}
        if surface_map_feats:
            surface_map_lyr.startEditing()
            surface_map_lyr.addFeatures(surface_map_feats)
        feedback.setProgress(100)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}


class LinkSurfacesWithConnectionNodes(LinkToConnectionNodesAlgorithm):
    """Link surfaces to connection nodes."""

    @property
    def parameter_names(self):
        return {
            LinkToConnectionNodesAlgorithm.POLYGON_LAYER: "Surface layer",
            LinkToConnectionNodesAlgorithm.SELECTED_POLYGONS: "Selected surfaces only",
            LinkToConnectionNodesAlgorithm.MAP_LAYER: "Surface map layer"
        }

    @property
    def default_values(self):
        return {
            LinkToConnectionNodesAlgorithm.POLYGON_LAYER: "Surface",
            LinkToConnectionNodesAlgorithm.MAP_LAYER: "Surface map",
            LinkToConnectionNodesAlgorithm.SEWERAGE_TYPES: [
                SewerageType.COMBINED_SEWER.value,
                SewerageType.STORM_DRAIN.value
            ]
        }

    @property
    def polygon_id_field(self):
        return "surface_id"

    def createInstance(self):
        return LinkSurfacesWithConnectionNodes()

    def name(self):
        return "threedi_map_surfaces_to_connection_nodes"

    def displayName(self):
        return "Map surfaces to connection nodes"


class LinkDWFWithConnectionNodes(LinkToConnectionNodesAlgorithm):
    """Link dry weather flow polygons to connection nodes."""

    @property
    def parameter_names(self):
        return {
            LinkToConnectionNodesAlgorithm.POLYGON_LAYER: "Dry weather flow layer",
            LinkToConnectionNodesAlgorithm.SELECTED_POLYGONS: "Selected DWF polygons only",
            LinkToConnectionNodesAlgorithm.MAP_LAYER: "Dry weather flow map layer"
        }

    @property
    def default_values(self):
        return {
            LinkToConnectionNodesAlgorithm.POLYGON_LAYER: "Dry weather flow",
            LinkToConnectionNodesAlgorithm.MAP_LAYER: "Dry weather flow map",
            LinkToConnectionNodesAlgorithm.SEWERAGE_TYPES: [
                SewerageType.COMBINED_SEWER.value,
                SewerageType.SANITARY_SEWER.value
            ]
        }

    @property
    def polygon_id_field(self):
        return "dry_weather_flow_id"

    def createInstance(self):
        return LinkDWFWithConnectionNodes()

    def name(self):
        return "threedi_map_dwf_to_connection_nodes"

    def displayName(self):
        return "Map dry weather flow to connection nodes"


class AddNWRWSurfaceParameters(QgsProcessingAlgorithm):
    """
    Add NWRW surface parameters to a surface parameter layer.
    """

    SURFACE_PARAMETERS = 'SURFACE_PARAMETERS_LAYER'

    def tr(self, string):
        """Returns a translatable string"""
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AddNWRWSurfaceParameters()

    def name(self):
        return 'threedi_add_nwrw_surface_parameters'

    def displayName(self):
        return self.tr('Add NWRW surface parameters')

    def group(self):
        return self.tr("Inflow")

    def groupId(self):
        return "0d"

    def shortHelpString(self):
        return  f"""
            <p>Add surface parameters from the Dutch NWRW inflow model to a schematisation.</p>
            <h3>Parameters</h3>
            <h4>Target surface parameters layer</h4>
            <p>Surface parameters layer of the 3Di schematisation that you want to add NWRW surface parameters to. Add it to your project to be able to select it.</p>
            """

    def initAlgorithm(self, config=None):
        """Define input and output parameters."""
        self.addParameter(
            QgsProcessingParameterMapLayer(
                self.SURFACE_PARAMETERS,
                'Target surface parameters layer',
                defaultValue='Surface parameters'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Process the algorithm.
        """
        # Get the target layer
        target_layer = self.parameterAsVectorLayer(parameters, self.SURFACE_PARAMETERS, context)
        if not target_layer:
            raise QgsProcessingException(f"Target layer {target_layer.name()} is not found")
            return {}

        # Check if the target layer exists and has the required fields
        if not target_layer.isValid():
            raise QgsProcessingException(f"Target layer {target_layer.name()} is not valid")
            return {}

        required_fields = [field for field in SurfaceParameters.__annotations__.keys()]
        layer_fields = [field.name() for field in target_layer.fields()]
        if set(required_fields) - set(layer_fields):
            raise QgsProcessingException(f"Target layer {target_layer.name()} does not contain the expected fields")

        # Load the surface parameters from the JSON file
        # No error handling because the json is not supplied by the user
        json_path = Path(__file__).parent.absolute() / 'data' / 'nwrw_surface_parameters.json'
        feedback.pushInfo(f"load {str(json_path)}")
        with json_path.open('r', encoding='utf-8') as f:
            nwrw_parameters = json.load(f)

        # Get the existing IDs from the target layer
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        existing_ids = set(
            [feature['id'] for feature in target_layer.getFeatures(request) if 'id' in feature.fields().names()])

        # Start editing the target layer
        target_layer.startEditing()

        try:
            # Process each parameter from the JSON file
            for param in nwrw_parameters:
                if param['id'] in existing_ids:
                    feedback.pushInfo(f"Skipped adding NWRW surface parameter {param['id']}, because id already exists")
                    continue
                feature = QgsFeature(target_layer.fields())
                for field_name, value in param.items():
                    feature[field_name] = value
                target_layer.addFeature(feature)
                feedback.pushInfo(f"Added NWRW surface parameter {param['id']}")
            # Commit the changes
            target_layer.commitChanges()
            feedback.pushInfo(f"Added NWRW surface parameters")
        except Exception as e:
            target_layer.rollBack()
            # manual raise is needed to ensure the processing fails when there is no output
            raise QgsProcessingException(f"Error adding NWRW surface parameters to layer {target_layer.name()}")

        return {}
