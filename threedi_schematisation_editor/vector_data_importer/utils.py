import warnings
from enum import Enum
from threading import Event
from typing import Optional

from qgis.core import (
    NULL,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsFeatureRequest,
    QgsGeometry,
    QgsPointLocator,
    QgsPointXY,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.gui import QgisInterface

from threedi_schematisation_editor.utils import TypeConversionError, convert_to_type
from threedi_schematisation_editor.warnings import (
    FeaturesImporterWarning,
    GeometryImporterWarning,
)

DEFAULT_INTERSECTION_BUFFER = 1
DEFAULT_INTERSECTION_BUFFER_SEGMENTS = 5
DEFAULT_MINIMUM_CHANNEL_LENGTH = 5


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


def build_feature_mapping(features, field_config_dict):
    """Build a {value: feature} mapping from a feature iterable using a FieldMapConfig dict.

    Supports ATTRIBUTE (including value_map) and EXPRESSION methods.
    Returns an empty dict on missing or unsupported config.
    Features resolving to None or NULL are skipped.
    Non-unique values are ambiguous and are excluded from the mapping.
    """
    mapping = {}
    if not field_config_dict:
        return mapping
    method = field_config_dict.get("method")
    if method == ColumnImportMethod.EXPRESSION.value:
        expression = QgsExpression(
            field_config_dict.get(ColumnImportMethod.EXPRESSION.value)
        )
        if not expression.isValid():
            return mapping
    elif method != ColumnImportMethod.ATTRIBUTE.value:
        return mapping
    uniques = set()
    for feature in features:
        value = get_field_config_value(field_config_dict, feature)
        if value is None or value == NULL:
            continue
        # only add unique values, and remove ambiguous matches
        if value not in uniques:
            mapping[value] = feature
            uniques.add(value)
        elif value in mapping:
            mapping.pop(value)
    return mapping


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


class ColumnImportMethod(str, Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    EXPRESSION = "expression"
    IGNORE = "ignore"

    def __str__(self):
        return self.name.capitalize()

    @staticmethod
    def all() -> list["ColumnImportMethod"]:
        return [item for item in ColumnImportMethod]


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


class CancellationToken:
    def __init__(self):
        self._event = Event()
        self._interrupted = False

    @property
    def is_cancelled(self):
        return self._event.is_set()

    @property
    def was_interrupted(self):
        return self._interrupted

    def interrupt(self):
        """Called when actually breaking from processing"""
        self._interrupted = True

    def cancel(self):
        self._event.set()

    def reset(self):
        self._event.clear()


def get_point_locator(
    layer: QgsVectorLayer, context: Optional[QgisInterface] = None
) -> QgsPointLocator:
    project = context.project() if context else QgsProject.instance()
    return QgsPointLocator(layer, layer.crs(), project.transformContext())


def compute_selected_ids(layer, source_settings):
    """Return the list of feature IDs to import given source selection and filter expression.

    Returns None when neither selected-only nor an expression is configured,
    meaning the importer should process all features.

    Cases:
    1. use_selected=False, no expression  -> None (all features)
    2. use_selected=True,  no expression  -> list of selected feature IDs
    3. use_selected=False, expression set -> list of IDs matching expression
    4. use_selected=True,  expression set -> selected IDs filtered by expression
    """
    use_selected = source_settings.use_selected_features
    expression_str = source_settings.include_expression

    if use_selected:
        candidate_ids = list(layer.selectedFeatureIds())
    else:
        candidate_ids = None  # all features

    if not expression_str:
        return candidate_ids

    expression = QgsExpression(expression_str)

    if expression.hasParserError():
        warnings.warn(
            f"Filter expression has a syntax error ({expression.parserErrorString()}) "
            f"— expression ignored, all candidate features will be imported",
            FeaturesImporterWarning,
        )
        return candidate_ids

    field_names = {f.name() for f in layer.fields()}
    unknown = expression.referencedColumns() - field_names - {"*"}
    if unknown:
        warnings.warn(
            f"Filter expression references fields not found in the layer: "
            f"{sorted(unknown)} — expression ignored, all candidate features will be imported",
            FeaturesImporterWarning,
        )
        return candidate_ids

    context = QgsExpressionContext()
    if candidate_ids is not None:
        request = layer.getFeatures(QgsFeatureRequest().setFilterFids(candidate_ids))
    else:
        request = layer.getFeatures()
    result = []
    for feat in request:
        context.setFeature(feat)
        try:
            if expression.evaluate(context):
                result.append(feat.id())
        except Exception as e:
            warnings.warn(
                f"Filter expression evaluation failed for feature {feat.id()}: {e} "
                f"— feature skipped",
                FeaturesImporterWarning,
            )
    return result


def get_substring_geometry(curve, start_distance, end_distance, simplify=False):
    """Extract a substring of a curve as a QgsGeometry.

    If simplify is True, reduces the result to a 2-point line (first and last vertex).
    """
    curve_substring = curve.curveSubstring(start_distance, end_distance)
    substring_geometry = QgsGeometry(curve_substring)
    if simplify:
        substring_polyline = substring_geometry.asPolyline()
        substring_geometry = QgsGeometry.fromPolylineXY(
            [substring_polyline[0], substring_polyline[-1]]
        )
    return substring_geometry


def update_conduit_endpoints(feature, node_by_location, node_layer_fields, node_attributes, node_manager) -> list:
    """Assign connection_node_id_start/_end for a cut conduit segment; create missing nodes."""
    new_nodes = []
    conduit_polyline = feature.geometry().asPolyline()
    start_node_point, end_node_point = conduit_polyline[0], conduit_polyline[-1]
    for point in [start_node_point, end_node_point]:
        if point not in node_by_location:
            node_feat = node_manager.create_new(
                QgsGeometry.fromPointXY(point), node_layer_fields, node_attributes
            )
            node_by_location[point] = node_feat["id"]
            new_nodes.append(node_feat)
    feature["connection_node_id_start"] = node_by_location[start_node_point]
    feature["connection_node_id_end"] = node_by_location[end_node_point]
    return new_nodes
