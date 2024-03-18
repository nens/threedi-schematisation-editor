# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict
from operator import itemgetter

from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterEnum,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.enumerators import SewerageType
from threedi_schematisation_editor.utils import get_feature_by_id, get_next_feature_id


class LinkSurfacesWithNodes(QgsProcessingAlgorithm):
    """Link (impervious) surfaces to connection nodes."""

    SURFACE_LAYER = "SURFACE_LAYER"
    SURFACE_MAP_LAYER = "SURFACE_MAP_LAYER"
    PIPE_LAYER = "PIPE_LAYER"
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
        return "threedi_link_surfaces_with_nodes"

    def displayName(self):
        return self.tr("Link surfaces with nodes")

    def group(self):
        return self.tr("0D")

    def groupId(self):
        return "0d"

    def shortHelpString(self):
        return self.tr("""Link (impervious) surfaces to connection nodes.""")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SURFACE_LAYER,
                self.tr("(Impervious) surface layer"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="Surface",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SURFACE_MAP_LAYER,
                self.tr("(Impervious) surface map layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="Surface map",
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
                defaultValue=SewerageType.COMBINED_SEWER.name,
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
        pipe_lyr = self.parameterAsLayer(parameters, self.PIPE_LAYER, context)
        if pipe_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PIPE_LAYER))
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
        surface_to_pipes_distances = defaultdict(list)
        pipe_features = [feat for feat in pipe_lyr.getFeatures() if feat["sewerage_type"] in sewerage_types]
        for surface_feat in surface_lyr.getFeatures():
            surface_fid = surface_feat.id()
            surface_geom = surface_feat.geometry()
            for pipe_feat in pipe_features:
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
        surface_map_feats = []
        surface_map_fields = surface_map_lyr.fields()
        next_surface_map_id = get_next_feature_id(surface_map_lyr)
        for surface_id, surface_pipes in surface_to_pipes_distances.items():
            surface_pipes.sort(key=itemgetter(1))
            surface_feat = surface_lyr.getFeature(surface_id)
            surface_geom = surface_feat.geometry()
            surface_centroid = surface_geom.centroid()
            pipe_id, surface_pipe_distance = surface_pipes[0]
            pipe_feat = pipe_lyr.getFeature(pipe_id)
            start_node_id = pipe_feat["connection_node_start_id"]
            end_node_id = pipe_feat["connection_node_end_id"]
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
            surface_map_geom = QgsGeometry.fromPolylineXY([surface_centroid.asPoint(), node_geom.asPoint()])
            surface_map_feat.setGeometry(surface_map_geom)
            surface_map_feat["id"] = next_surface_map_id
            surface_map_feat["surface_id"] = surface_feat["id"]
            surface_map_feat["connection_node_id"] = surface_node_id
            surface_map_feat["percentage"] = 100.0
            surface_map_feats.append(surface_map_feat)
            next_surface_map_id += 1
        if surface_map_feats:
            surface_map_lyr.startEditing()
            surface_map_lyr.addFeatures(surface_map_feats)
            success = surface_map_lyr.commitChanges()
            if not success:
                commit_errors = surface_map_lyr.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}
