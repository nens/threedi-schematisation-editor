# Copyright (C) 2023 by Lutra Consulting
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
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.enumerators import SewerageType
from threedi_schematisation_editor.utils import get_feature_by_id, get_next_feature_id, spatial_index


class LinkSurfacesWithNodes(QgsProcessingAlgorithm):
    """Link (impervious) surfaces to connection nodes."""

    SURFACE_LAYER = "SURFACE_LAYER"
    SELECTED_SURFACES = "SELECTED_SURFACES"
    SURFACE_MAP_LAYER = "SURFACE_MAP_LAYER"
    PIPE_LAYER = "PIPE_LAYER"
    SELECTED_PIPES = "SELECTED_PIPES"
    NODE_LAYER = "NODE_LAYER"
    SEWERAGE_TYPES = "SEWERAGE_TYPES"
    STORMWATER_SEWER_PREFERENCE = "STORMWATER_SEWER_PREFERENCE"
    SANITARY_SEWER_PREFERENCE = "SANITARY_SEWER_PREFERENCE"
    SEARCH_DISTANCE = "SEARCH_DISTANCE"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return LinkSurfacesWithNodes()

    def name(self):
        return "threedi_map_surfaces_to_connection_nodes"

    def displayName(self):
        return self.tr("Map (impervious) surfaces to connection nodes")

    def group(self):
        return self.tr("Inflow")

    def groupId(self):
        return "0d"

    def shortHelpString(self):
        return self.tr(
            """
            <p>Connect (impervious) surfaces to the sewer system by creating (impervious) surface map features. The new features are added to the (impervious) surface layer directly.</p>
            <p>For each (impervious) surface, the nearest pipe is found; the surface is mapped to the the nearest of this pipe's connection nodes.</p>
            <p>In some cases, you may want to prefer e.g. stormwater drains over combined sewers. This can be done by setting the stormwater sewer preference to a value greater than zero.</p>
            <h3>Parameters</h3>
            <h4>(Impervious) surface layer</h4>
            <p>Surface or Impervious surface layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>(Impervious) surface map layer</h4>
            <p>Surface map or Impervious surface map layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Pipe layer</h4>
            <p>Pipe layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Connection node layer</h4>
            <p>Connection node layer that is added to the project with the 3Di Schematisation Editor.</p>
            <h4>Sewerage types</h4>
            <p>Only pipes of the selected sewerage types will be used in the algorithm</p>
            <h4>Stormwater sewer preference</h4>
            <p>This value (in meters) will be subtracted from the distance between the (impervious) surface and the stormwater drain. For example: there is a combined sewer within 10 meters from the (impervious) surface, and a stormwater drain within 11 meters; if the stormwater sewer preference is 2 m, the algorithm will use 11 - 2 = 9 m as distance to the stormwater sewer, so the (impervious) surface will be mapped to one of the stormwater drain's connection nodes, instead of to the combined sewer's connection nodes.</p>
            <h4>Sanitary sewer preference</h4>
            <p>This value (in meters) will be subtracted from the distance between the (impervious) surface and the sanitary sewer. See 'stormwater sewer preference' for further explanation.</p>
            <h4>Search distance</h4>
            <p>Only pipes within search distance (m) from the (impervious) surface will be used in the algorithm.</p>
            """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SURFACE_LAYER,
                self.tr("(Impervious) surface layer"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="Impervious Surface",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_SURFACES,
                self.tr("Selected (impervious) surfaces only"),
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SURFACE_MAP_LAYER,
                self.tr("(Impervious) surface map layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="Impervious surface map",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PIPE_LAYER,
                self.tr("Pipe layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="Pipe",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_PIPES,
                self.tr("Selected pipes only"),
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NODE_LAYER,
                self.tr("Connection node layer"),
                [QgsProcessing.TypeVectorPoint],
                defaultValue="Connection Node",
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SEWERAGE_TYPES,
                self.tr("Sewerage types"),
                allowMultiple=True,
                options=[e.name for e in SewerageType],
                defaultValue=[SewerageType.COMBINED_SEWER.value, SewerageType.STORM_DRAIN.value],
            )
        )
        storm_pref = QgsProcessingParameterNumber(
            self.STORMWATER_SEWER_PREFERENCE, self.tr("Stormwater sewer preference [m]"), type=1, defaultValue=0.0
        )
        storm_pref.setMinimum(0.0)
        storm_pref.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(storm_pref)
        sanitary_pref = QgsProcessingParameterNumber(
            self.SANITARY_SEWER_PREFERENCE, self.tr("Sanitary sewer preference [m]"), type=1, defaultValue=0.0
        )
        sanitary_pref.setMinimum(0.0)
        sanitary_pref.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(sanitary_pref)
        search_distance = QgsProcessingParameterNumber(
            self.SEARCH_DISTANCE, self.tr("Search distance"), type=1, defaultValue=10.0
        )
        search_distance.setMinimum(0.01)
        search_distance.setMetadata({"widget_wrapper": {"decimals": 2}})
        self.addParameter(search_distance)

    def processAlgorithm(self, parameters, context, feedback):
        surface_lyr = self.parameterAsLayer(parameters, self.SURFACE_LAYER, context)
        if surface_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SURFACE_LAYER))
        surface_map_lyr = self.parameterAsLayer(parameters, self.SURFACE_MAP_LAYER, context)
        if surface_map_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SURFACE_MAP_LAYER))
        selected_surfaces = self.parameterAsBool(parameters, self.SELECTED_SURFACES, context)
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
        surface_map_field_names = {fld.name() for fld in surface_map_fields}
        next_surface_map_id = get_next_feature_id(surface_map_lyr)
        surface_id_field = "surface_id" if "surface_id" in surface_map_field_names else "dry_weather_flow_id"
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
            surface_centroid = surface_geom.centroid()
            pipe_id, surface_pipe_distance = surface_pipes[0]
            pipe_feat = pipe_features[pipe_id]
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
            surface_map_feat[surface_id_field] = surface_feat["id"]
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
