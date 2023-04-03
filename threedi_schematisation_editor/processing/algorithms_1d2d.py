# Copyright (C) 2023 by Lutra Consulting
from qgis.core import (
    Qgis,
    QgsExpression,
    QgsFeature,
    QgsFeatureRequest,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.enumerators import CalculationType
from threedi_schematisation_editor.utils import get_features_by_expression, get_next_feature_id


class GenerateExchangeLines(QgsProcessingAlgorithm):
    """Generate channels exchange lines."""

    INPUT_CHANNELS = "INPUT_CHANNELS"
    OFFSET_DISTANCE = "OFFSET_DISTANCE"
    EXCHANGE_LINES = "EXCHANGE_LINES"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return GenerateExchangeLines()

    def name(self):
        return "threedi_generate_exchange_lines"

    def displayName(self):
        return self.tr("Generate exchange lines")

    def group(self):
        return self.tr("1D2D")

    def groupId(self):
        return "1d2d"

    def shortHelpString(self):
        return self.tr(
            """
            <p>This processing algorithm generates exchange lines for (a selection of) channels. The resulting exchange line's geometry is a copy of the input channel's geometry, at user specified distance from that channel (the GIS term for this is 'offset curve'). The resulting exchange lines is added to the exchange line layer, and the attribute 'channel_id' refers to the channel it was derived from.</p>
            <h3>Parameters</h3>
            <h4>Input channel layer</h4>
            <p>Usually this is the Channel layer that is added to the project with the 3Di Schematisation Editor. Technically, any layer with a line geometry and the fields 'id' and 'calculation_type' can be used as input.</p>
            <h4>Distance</h4>
            <p>Offset distance in meters. A positive value will place the output exchange line to the left of the line, negative values will place it to the right.</p>
            <h4>Exchange lines layer</h4>
            <p>The layer to which the results are written. Usually this is the 'Exchange line' layer that is added to the project with the 3Di Schematisation Editor. Technically, any layer with a line geometry and the field 'channel_id' can be used.</p>
            """
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CHANNELS,
                self.tr("Input channel layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="Channel",
            )
        )

        offset_param = QgsProcessingParameterNumber(self.OFFSET_DISTANCE, self.tr("Distance (m)"), type=1)
        offset_param.setMetadata({"widget_wrapper": {"decimals": 3}})
        self.addParameter(offset_param)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.EXCHANGE_LINES,
                self.tr("Exchange lines layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="Exchange line",
            )
        )

    def checkParameterValues(self, parameters, context):
        success, msg = super().checkParameterValues(parameters, context)
        if success:
            invalid_parameters_messages = []
            channels = self.parameterAsSource(parameters, self.INPUT_CHANNELS, context)
            required_channel_fields = {"id", "calculation_type"}
            channels_field_names = {f.name() for f in channels.fields()}
            if not required_channel_fields.issubset(channels_field_names):
                invalid_parameters_messages.append(
                    "Channel layer is missing required fields ('id' and/or 'calculation_type')"
                )
            offset_distance = self.parameterAsDouble(parameters, self.OFFSET_DISTANCE, context)
            if offset_distance == 0:
                invalid_parameters_messages.append("Offset distance cannot be 0")
            exchange_lines_lyr = self.parameterAsLayer(parameters, self.EXCHANGE_LINES, context)
            exchange_lines_names = {f.name() for f in exchange_lines_lyr.fields()}
            if "channel_id" not in exchange_lines_names:
                invalid_parameters_messages.append("Exchange line layer is missing required 'channel_id' field")
            if invalid_parameters_messages:
                success = False
                msg = "\n".join(invalid_parameters_messages)
        return success, msg

    def processAlgorithm(self, parameters, context, feedback):
        channels = self.parameterAsSource(parameters, self.INPUT_CHANNELS, context)
        if channels is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_CHANNELS))
        offset_distance = self.parameterAsDouble(parameters, self.OFFSET_DISTANCE, context)
        if offset_distance is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OFFSET_DISTANCE))
        exchange_lines_lyr = self.parameterAsLayer(parameters, self.EXCHANGE_LINES, context)
        if exchange_lines_lyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.EXCHANGE_LINES))
        exchange_line_feats = []
        exchange_lines_fields = exchange_lines_lyr.fields()
        current_exchange_line_id = get_next_feature_id(exchange_lines_lyr)
        calculation_type_max_exchange_lines = {
            CalculationType.ISOLATED.value: 0,
            CalculationType.EMBEDDED.value: 0,
            CalculationType.CONNECTED.value: 1,
            CalculationType.DOUBLE_CONNECTED.value: 2,
        }
        error_template = (
            "Error: channel {} with calculation type {} ({}) already has a maximum of {} exchange lines. "
            "Change the calculation type or remove exchange lines for this channel and try again."
        )
        for channel_feat in channels.getFeatures():
            channel_fid = channel_feat.id()
            channel_id = channel_feat["id"]
            if not channel_id:
                feedback.reportError(f"Error: invalid channel ID. Processing feature with FID {channel_fid} skipped.")
                continue
            calculation_type = channel_feat["calculation_type"]
            if calculation_type not in calculation_type_max_exchange_lines:
                feedback.reportError(
                    f"Error: invalid channel calculation type. Processing feature with FID {channel_fid} skipped."
                )
                continue
            calculation_type_name = CalculationType(calculation_type).name
            channel_expression_text = f'"channel_id" = {channel_id}'
            channel_exchange_lines = list(get_features_by_expression(exchange_lines_lyr, channel_expression_text))
            calc_type_limit = calculation_type_max_exchange_lines[calculation_type]
            if len(channel_exchange_lines) >= calc_type_limit:
                error_msg = error_template.format(channel_id, calculation_type, calculation_type_name, calc_type_limit)
                feedback.reportError(error_msg)
                continue
            channel_geom = channel_feat.geometry()
            offset_geom = channel_geom.offsetCurve(offset_distance, 8, Qgis.JoinStyle.Bevel, 0.0)
            new_exchange_line = QgsFeature(exchange_lines_fields)
            new_exchange_line["id"] = current_exchange_line_id
            new_exchange_line["channel_id"] = channel_feat["id"]
            new_exchange_line.setGeometry(offset_geom)
            exchange_line_feats.append(new_exchange_line)
            current_exchange_line_id += 1
        if exchange_line_feats:
            exchange_lines_lyr.startEditing()
            exchange_lines_lyr.addFeatures(exchange_line_feats)
            success = exchange_lines_lyr.commitChanges()
            if not success:
                commit_errors = exchange_lines_lyr.commitErrors()
                commit_errors_message = "\n".join(commit_errors)
                feedback.reportError(commit_errors_message)
        return {}
