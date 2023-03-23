# Copyright (C) 2023 by Lutra Consulting
from qgis.core import (
    Qgis,
    QgsFeature,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication

from threedi_schematisation_editor.utils import get_next_feature_id


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
        return self.tr("Generate exchange lines from channel geometries")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CHANNELS, self.tr("Input Channel layer"), [QgsProcessing.TypeVectorLine]
            )
        )

        offset_param = QgsProcessingParameterNumber(self.OFFSET_DISTANCE, self.tr("Distance (m)"), type=1)
        offset_param.setMetadata({"widget_wrapper": {"decimals": 3}})
        self.addParameter(offset_param)
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.EXCHANGE_LINES, self.tr("Exchange lines layer"), [QgsProcessing.TypeVectorLine]
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        channels = self.parameterAsSource(parameters, self.INPUT_CHANNELS, context)
        if channels is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_CHANNELS))
        offset_distance = self.parameterAsDouble(parameters, self.OFFSET_DISTANCE, context)
        if offset_distance is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.OFFSET_DISTANCE))
        exchange_lines_lyr = self.parameterAsLayer(parameters, self.EXCHANGE_LINES, context)
        if exchange_lines_lyr is None or "channel_id" not in {f.name() for f in exchange_lines_lyr.fields()}:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.EXCHANGE_LINES))
        exchange_line_feats = []
        exchange_lines_fields = exchange_lines_lyr.fields()
        current_exchange_line_id = get_next_feature_id(exchange_lines_lyr)
        for channel_feat in channels.getFeatures():
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
            exchange_lines_lyr.commitChanges()
        return {}
