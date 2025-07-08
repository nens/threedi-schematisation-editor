import warnings

from qgis.core import (
    NULL,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsGeometry,
)

from threedi_schematisation_editor.custom_tools.import_config import ColumnImportMethod
from threedi_schematisation_editor.utils import convert_to_type, TypeConversionError
from threedi_schematisation_editor.warnings import FeaturesImporterWarning

DEFAULT_INTERSECTION_BUFFER = 1
DEFAULT_INTERSECTION_BUFFER_SEGMENTS = 5

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
            method = ColumnImportMethod(field_config["method"])
            if method == ColumnImportMethod.AUTO:
                continue
            field_value = NULL
            if method == ColumnImportMethod.ATTRIBUTE:
                src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
                src_value = source_feat[src_field_name]
                value_map = field_config.get("value_map", {})
                # Prevent type mismatches in keys by casting keys to strings to match those the dict in src_value['value_map'] which is also forced to be strings
                field_value = value_map.get(str(src_value), src_value)
                if field_value == NULL:
                    field_value = field_config.get("default_value", NULL)
            elif method == ColumnImportMethod.EXPRESSION:
                expression_str = field_config["expression"]
                expression = QgsExpression(expression_str)
                field_value = expression.evaluate(expression_context)
            elif method == ColumnImportMethod.DEFAULT:
                field_value = field_config["default_value"]
            try:
                new_feat[field_name] = convert_to_type(field_value, field_type)
            except TypeConversionError as e:
                new_feat[field_name] = NULL
                feat_id = new_feat["id"]
                message = f"Attribute {field_name} of feature with id {feat_id} was not filled in"
                warnings.warn(f"{message}. {e}", FeaturesImporterWarning)


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
        self.integrate = conversion_config.get("edit_channels", False)
        self.use_snapping = conversion_config.get("use_snapping", False)
        if self.use_snapping:
            self.snapping_distance = conversion_config.get("snapping_distance")
        else:
            self.snapping_distance = DEFAULT_INTERSECTION_BUFFER
        self.create_connection_nodes = conversion_config.get("create_connection_nodes", False)
        self.length_source_field = conversion_config.get("length_source_field", None)
        self.length_fallback_value = conversion_config.get("length_fallback_value", 10.0)
        self.azimuth_source_field = conversion_config.get("azimuth_source_field", None)
        self.azimuth_fallback_value = conversion_config.get("azimuth_fallback_value", 90.0)
        self.edit_channels = conversion_config.get("edit_channels", False)


def get_substring_geometry(curve, start_distance, end_distance, simplify=False):
    curve_substring = curve.curveSubstring(start_distance, end_distance)
    substring_geometry = QgsGeometry(curve_substring)
    if simplify:
        substring_polyline = substring_geometry.asPolyline()
        substring_geometry = QgsGeometry.fromPolylineXY([substring_polyline[0], substring_polyline[-1]])
    return substring_geometry



