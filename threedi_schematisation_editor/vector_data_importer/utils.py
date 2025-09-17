import warnings
from enum import Enum

from qgis.core import (
    NULL,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
)

from threedi_schematisation_editor.utils import TypeConversionError, convert_to_type
from threedi_schematisation_editor.warnings import (
    FeaturesImporterWarning,
    GeometryImporterWarning,
)

DEFAULT_INTERSECTION_BUFFER = 1
DEFAULT_INTERSECTION_BUFFER_SEGMENTS = 5
DEFAULT_MINIMUM_CHANNEL_LENGTH = 5

from qgis.core import Qgis, QgsMessageLog


def get_field_config_value(field_config, source_feat, expression_context=None):
    method = ColumnImportMethod(field_config["method"])
    field_value = NULL
    if method == ColumnImportMethod.ATTRIBUTE:
        src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
        try:
            src_value = source_feat[src_field_name]
        except KeyError:
            src_value = NULL
        value_map = field_config.get("value_map", {})
        # Prevent type mismatches in keys by casting keys to strings to match those the dict in src_value['value_map'] which is also forced to be strings
        field_value = value_map.get(str(src_value), src_value)
        if field_value == NULL:
            field_value = field_config.get("default_value", NULL)
    elif method == ColumnImportMethod.EXPRESSION:
        if expression_context is None:
            expression_context = QgsExpressionContext()
            expression_context.setFeature(source_feat)
        expression_str = field_config["expression"]
        expression = QgsExpression(expression_str)
        field_value = expression.evaluate(expression_context)
    elif method == ColumnImportMethod.DEFAULT:
        field_value = field_config["default_value"]
    return field_value


def update_attributes(fields_config, model_cls, source_feat, *new_features):
    expression_context = QgsExpressionContext()
    expression_context.setFeature(source_feat)
    type_annotations = model_cls.__annotations__
    for new_feat in new_features:
        for field_name, field_type in type_annotations.items():
            try:
                field_config = fields_config[field_name]
            except KeyError:
                continue
            QgsMessageLog.logMessage(f"set field {field_name}", "Warning", Qgis.Warning)
            if ColumnImportMethod(field_config["method"]) == ColumnImportMethod.AUTO:
                continue
            field_value = get_field_config_value(
                field_config, source_feat, expression_context=expression_context
            )
            try:
                new_feat[field_name] = convert_to_type(field_value, field_type)
            except TypeConversionError as e:
                new_feat[field_name] = NULL
                feat_id = new_feat["id"]
                message = f"Attribute {field_name} of feature with id {feat_id} was not filled in"
                warnings.warn(f"{message}. {e}", FeaturesImporterWarning)


def get_float_value_from_feature(feature, field_name, fallback_value):
    if field_name:
        try:
            feature[field_name]
        except KeyError:
            return fallback_value
        if feature[field_name] != NULL:
            try:
                return convert_to_type(feature[field_name], float)
            except TypeConversionError:
                return fallback_value
    return fallback_value


class FeatureManager:
    def __init__(self, next_id=1):
        self.next_id = next_id

    def create_new(self, geom, fields, attributes=None, set_id=True):
        new_feat = QgsFeature(fields)
        self.add_feature(new_feat, geom, attributes, set_id)
        return new_feat

    def add_feature(self, new_feat, geom=None, attributes=None, set_id=True):
        if geom:
            new_feat.setGeometry(geom)
        if attributes:
            for field_name, field_value in attributes.items():
                new_feat[field_name] = field_value
        if set_id:
            new_feat["id"] = self.next_id
            self.next_id += 1


class ConversionSettings:
    def __init__(self, conversion_config):
        self.integrate_pipes = conversion_config.get("edit_pipes", False)
        self.integrate_channels = conversion_config.get("edit_channels", False)
        self.use_snapping = conversion_config.get("use_snapping", False)
        if self.use_snapping:
            self.snapping_distance = conversion_config.get("snapping_distance")
        else:
            self.snapping_distance = DEFAULT_INTERSECTION_BUFFER
        self.minimum_channel_length = conversion_config.get(
            "minimum_channel_length", DEFAULT_MINIMUM_CHANNEL_LENGTH
        )
        self.create_connection_nodes = conversion_config.get(
            "create_connection_nodes", False
        )
        self.length_source_field = conversion_config.get("length_source_field", None)
        self.length_fallback_value = conversion_config.get(
            "length_fallback_value", 10.0
        )
        self.azimuth_source_field = conversion_config.get("azimuth_source_field", None)
        self.azimuth_fallback_value = conversion_config.get(
            "azimuth_fallback_value", 90.0
        )
        self.edit_channels = conversion_config.get("edit_channels", False)
        self.join_field_src = conversion_config.get("join_field_src", None)
        self.join_field_tgt = conversion_config.get("join_field_tgt", None)
        self.group_by_field = conversion_config.get("group_by", None)
        self.order_by_field = conversion_config.get("order_by", None)


class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    EXPRESSION = "expression"
    IGNORE = "ignore"

    def __str__(self):
        return self.name.capitalize()


def get_src_geometry(feature: QgsFeature, none_ok=False) -> QgsGeometry:
    # convert source geometry to type that can be processed
    # when the geometry cannot be handled None is returned and warnings/errors are raised upstream
    warning_base = f"Source geometry of feature with id {feature.id()}"
    geom = feature.geometry()
    if geom is None:
        if not none_ok:
            warnings.warn(f"{warning_base} is None", GeometryImporterWarning)
        return None
    if geom.type() not in [
        QgsWkbTypes.GeometryType.Point,
        QgsWkbTypes.GeometryType.Line,
        QgsWkbTypes.GeometryType.Polygon,
    ]:
        warnings.warn(
            f"{warning_base} has unsupported geometry type", GeometryImporterWarning
        )
        return None
    # the desired geometry type is linear (not curved), single (not multi-part) and flat (no z- or m-coordinates) and
    desired_type = QgsWkbTypes.linearType(
        QgsWkbTypes.singleType(QgsWkbTypes.flatType(geom.wkbType()))
    )
    # convert the source geometry to the desired type
    try:
        return geom.coerceToType(desired_type)[0]
    except Exception:
        warnings.warn(
            f"{warning_base} cannot be converted to desired geometry type",
            GeometryImporterWarning,
        )
        return None
