# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict

from qgis.core import (
    NULL,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterVectorLayer,
    QgsProject,
)
from qgis.PyQt.QtCore import QCoreApplication


class BottomLevelCalculator(QgsProcessingAlgorithm):
    """Calculate manhole bottom level from pipes."""

    MANHOLE_LAYER = "MANHOLE_LAYER"
    SELECTED_MANHOLES = "SELECTED_MANHOLES"
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
        return self.tr("""Calculate manhole bottom level from pipes.""")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.MANHOLE_LAYER,
                self.tr("Manhole layer"),
                [QgsProcessing.TypeVectorPoint],
                defaultValue="Manhole",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED_MANHOLES,
                self.tr("Selected manholes only"),
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
        manhole_lyr = self.parameterAsLayer(parameters, self.MANHOLE_LAYER, context)
        if manhole_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.MANHOLE_LAYER))
        selected_manholes = self.parameterAsBool(parameters, self.SELECTED_MANHOLES, context)
        pipe_lyr = self.parameterAsLayer(parameters, self.PIPE_LAYER, context)
        if pipe_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PIPE_LAYER))
        selected_pipes = self.parameterAsBool(parameters, self.SELECTED_PIPES, context)
        overwrite_levels = self.parameterAsBool(parameters, self.OVERWRITE_LEVELS, context)
        do_not_raise_levels = self.parameterAsBool(parameters, self.DO_NOT_RAISE_LEVELS, context)
        node_adjacent_invert_levels = defaultdict(set)
        for pipe_feat in pipe_lyr.selectedFeatures() if selected_pipes else pipe_lyr.getFeatures():
            pipe_start_node_id = pipe_feat["connection_node_start_id"]
            pipe_end_node_id = pipe_feat["connection_node_end_id"]
            invert_level_start_point = pipe_feat["invert_level_start_point"]
            invert_level_end_point = pipe_feat["invert_level_end_point"]
            if invert_level_start_point != NULL:
                node_adjacent_invert_levels[pipe_start_node_id].add(invert_level_start_point)
            if invert_level_end_point != NULL:
                node_adjacent_invert_levels[pipe_end_node_id].add(invert_level_end_point)
        bottom_level_changes = {}
        for manhole_feat in manhole_lyr.selectedFeatures() if selected_manholes else manhole_lyr.getFeatures():
            manhole_fid = manhole_feat.id()
            node_id = manhole_feat["connection_node_id"]
            if not node_id:
                continue
            bottom_level = manhole_feat["bottom_level"]
            if bottom_level != NULL and not overwrite_levels:
                continue
            invert_levels = node_adjacent_invert_levels[node_id]
            if not invert_levels:
                continue
            min_invert_level = min(invert_levels)
            if bottom_level != NULL:
                if min_invert_level > bottom_level and do_not_raise_levels:
                    continue
            bottom_level_changes[manhole_fid] = min_invert_level
        if bottom_level_changes:
            bottom_level_field_idx = manhole_lyr.fields().lookupField("bottom_level")
            manhole_lyr.startEditing()
            for manhole_fid, bottom_level in bottom_level_changes.items():
                manhole_lyr.changeAttributeValue(manhole_fid, bottom_level_field_idx, bottom_level)
            success = manhole_lyr.commitChanges()
            if not success:
                commit_errors = manhole_lyr.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)
        return {}

    def postProcessAlgorithm(self, context, feedback):
        for layer in QgsProject.instance().mapLayers().values():
            layer.triggerRepaint()
        return {}
