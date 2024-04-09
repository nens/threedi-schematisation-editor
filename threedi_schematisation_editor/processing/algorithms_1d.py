# Copyright (C) 2023 by Lutra Consulting
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
        return self.tr(
        """
        <p>Calculate manhole bottom level from the invert levels of pipes or culverts.</p>
        <p>For each manhole, the algorithm determines which sides of which pipes (or culverts) are connected to it, and what is the invert level at that side. It than takes the lowest of these invert levels as bottom level for the manhole.</p>
        <h3>Parameters</h3>
        <h4>Manhole layer</h4>
        <p>Manhole layer that is added to the project with the 3Di Schematisation Editor.</p>
        <p>If "Selected manholes only" is checked, only the selected manholes will be used in the algorithm.</p>
        <h4>Pipe layer</h4>
        <p>Pipe or Culvert layer that is added to the project with the 3Di Schematisation Editor.</p>
        <p>If "Selected pipes only" is checked, only the selected pipes will be used in the algorithm.</p>
        <h4>Overwrite existing bottom levels</h4>
        <p>If checked, bottom levels will be recalculated for manholes that already have a bottom level filled in</p> 
        <h4>Do not raise existing bottom levels</h4>
        <p>This is only relevant if "Overwrite existing bottom levels" is checked.</p>
        <p>If checked, bottom levels will only be updated for manholes where the calculated value is lower than the existing value.</p>
        """)

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
        feedback.setProgress(0)
        num_pipes = pipe_lyr.selectedFeatureCount() if selected_pipes else pipe_lyr.featureCount()
        processed_pipes = 0
        for pipe_feat in pipe_lyr.selectedFeatures() if selected_pipes else pipe_lyr.getFeatures():
            pipe_start_node_id = pipe_feat["connection_node_start_id"]
            pipe_end_node_id = pipe_feat["connection_node_end_id"]
            invert_level_start_point = pipe_feat["invert_level_start_point"]
            invert_level_end_point = pipe_feat["invert_level_end_point"]
            if invert_level_start_point != NULL:
                node_adjacent_invert_levels[pipe_start_node_id].add(invert_level_start_point)
            if invert_level_end_point != NULL:
                node_adjacent_invert_levels[pipe_end_node_id].add(invert_level_end_point)
            processed_pipes += 1
            feedback.setProgress(100/3 * processed_pipes / num_pipes)
            if feedback.isCanceled():
                return {}
        bottom_level_changes = {}
        num_manholes = manhole_lyr.selectedFeatureCount() if selected_manholes else manhole_lyr.featureCount()
        processed_manholes = 0
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
            processed_manholes += 1
            feedback.setProgress(100/3 + 100/3 * processed_manholes / num_manholes)
            if feedback.isCanceled():
                return {}
        if bottom_level_changes:
            bottom_level_field_idx = manhole_lyr.fields().lookupField("bottom_level")
            manhole_lyr.startEditing()
            for i, (manhole_fid, bottom_level) in enumerate(bottom_level_changes.items()):
                if feedback.isCanceled():
                    return {}
                manhole_lyr.changeAttributeValue(manhole_fid, bottom_level_field_idx, bottom_level)
                feedback.setProgress(200/3 + 100/3 * (i + 1) / len(bottom_level_changes))
                if feedback.isCanceled():
                    return {}
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
