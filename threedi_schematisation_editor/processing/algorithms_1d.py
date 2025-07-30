# Copyright (C) 2025 by Lutra Consulting
from collections import defaultdict

from qgis.core import (
    NULL,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication


class BottomLevelCalculator(QgsProcessingAlgorithm):
    """Calculate connection node manhole bottom level from pipes."""

    CONNECTION_NODE_LAYER = "CONNECTION_NODE_LAYER"
    SELECTED_CONNECTION_NODES = "SELECTED_CONNECTION_NODES"
    PIPE_LAYER = "PIPE_LAYER"
    SELECTED_PIPES = "SELECTED_PIPES"
    OVERWRITE_LEVELS = "OVERWRITE_LEVELS"
    DO_NOT_RAISE_LEVELS = "DO_NOT_RAISE_LEVELS"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return BottomLevelCalculator()

    def name(self):
        return "threedi_bottom_level_calculator"

    def displayName(self):
        return self.tr("Manhole bottom level from pipes")

    def group(self):
        return self.tr("1D")

    def groupId(self):
        return "1d"

    def shortHelpString(self):
        return self.tr(
            """
        <p>Calculate connection node manhole bottom level from the invert levels of pipes or culverts.</p>
        <p>For each connection node manhole, the algorithm determines which sides of which pipes (or culverts) are connected to it, and what the invert level is at that side. It than takes the lowest of these invert levels as bottom level for the manhole.</p>
        <h3>Parameters</h3>
        <h4>Connection node layer</h4>
        <p>Connection node layer that is added to the project with the 3Di Schematisation Editor.</p>
        <p>If "Selected connection nodes only" is checked, only the selected manholes will be used in the algorithm.</p>
        <h4>Pipe layer</h4>
        <p>Pipe or Culvert layer that is added to the project with the 3Di Schematisation Editor.</p>
        <p>If "Selected pipes only" is checked, only the selected pipes will be used in the algorithm.</p>
        <h4>Overwrite existing bottom levels</h4>
        <p>If checked, bottom levels will be recalculated for manholes that already have a bottom level filled in.</p> 
        <h4>Do not raise existing bottom levels</h4>
        <p>This is only relevant if "Overwrite existing bottom levels" is checked.</p>
        <p>If checked, bottom levels will only be updated for manholes where the calculated value is lower than the existing value.</p>
        """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.CONNECTION_NODE_LAYER,
                self.tr("Connection node layer"),
                [QgsProcessing.TypeVectorPoint],
                defaultValue="Connection node",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_CONNECTION_NODES,
                self.tr("Selected connection node manholes only"),
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
            QgsProcessingParameterBoolean(
                self.OVERWRITE_LEVELS,
                self.tr("Overwrite existing bottom levels"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.DO_NOT_RAISE_LEVELS,
                self.tr("Do not raise existing bottom levels"),
                defaultValue=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        connection_node_lyr = self.parameterAsLayer(
            parameters, self.CONNECTION_NODE_LAYER, context
        )
        if connection_node_lyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.CONNECTION_NODE_LAYER)
            )
        selected_manhole_nodes = self.parameterAsBool(
            parameters, self.SELECTED_CONNECTION_NODES, context
        )
        pipe_lyr = self.parameterAsLayer(parameters, self.PIPE_LAYER, context)
        if pipe_lyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.PIPE_LAYER)
            )
        selected_pipes = self.parameterAsBool(parameters, self.SELECTED_PIPES, context)
        overwrite_levels = self.parameterAsBool(
            parameters, self.OVERWRITE_LEVELS, context
        )
        do_not_raise_levels = self.parameterAsBool(
            parameters, self.DO_NOT_RAISE_LEVELS, context
        )
        node_adjacent_invert_levels = defaultdict(set)
        feedback.setProgress(0)
        num_pipes = (
            pipe_lyr.selectedFeatureCount()
            if selected_pipes
            else pipe_lyr.featureCount()
        )
        processed_pipes = 0
        for pipe_feat in (
            pipe_lyr.selectedFeatures() if selected_pipes else pipe_lyr.getFeatures()
        ):
            pipe_start_node_id = pipe_feat["connection_node_id_start"]
            pipe_end_node_id = pipe_feat["connection_node_id_end"]
            invert_level_start = pipe_feat["invert_level_start"]
            invert_level_end = pipe_feat["invert_level_end"]
            if invert_level_start != NULL:
                node_adjacent_invert_levels[pipe_start_node_id].add(invert_level_start)
            if invert_level_end != NULL:
                node_adjacent_invert_levels[pipe_end_node_id].add(invert_level_end)
            processed_pipes += 1
            feedback.setProgress(100 / 3 * processed_pipes / num_pipes)
            if feedback.isCanceled():
                return {}
        bottom_level_changes = {}
        num_manhole_nodes = (
            connection_node_lyr.selectedFeatureCount()
            if selected_manhole_nodes
            else connection_node_lyr.featureCount()
        )
        processed_nodes = 0
        for node_feat in (
            connection_node_lyr.selectedFeatures()
            if selected_manhole_nodes
            else connection_node_lyr.getFeatures()
        ):
            node_fid = node_feat.id()
            node_id = node_feat["id"]
            if not node_id:
                continue
            bottom_level = node_feat["bottom_level"]
            if bottom_level != NULL and not overwrite_levels:
                continue
            invert_levels = node_adjacent_invert_levels[node_id]
            if not invert_levels:
                continue
            min_invert_level = min(invert_levels)
            if bottom_level != NULL:
                if min_invert_level > bottom_level and do_not_raise_levels:
                    continue
            bottom_level_changes[node_fid] = min_invert_level
            processed_nodes += 1
            feedback.setProgress(
                100 / 3 + 100 / 3 * processed_nodes / num_manhole_nodes
            )
            if feedback.isCanceled():
                return {}
        if bottom_level_changes:
            bottom_level_field_idx = connection_node_lyr.fields().lookupField(
                "bottom_level"
            )
            connection_node_lyr.startEditing()
            for i, (node_fid, bottom_level) in enumerate(bottom_level_changes.items()):
                if feedback.isCanceled():
                    return {}
                connection_node_lyr.changeAttributeValue(
                    node_fid, bottom_level_field_idx, bottom_level
                )
                feedback.setProgress(
                    200 / 3 + 100 / 3 * (i + 1) / len(bottom_level_changes)
                )
                if feedback.isCanceled():
                    return {}
            success = connection_node_lyr.commitChanges()
            if not success:
                commit_errors = connection_node_lyr.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}
