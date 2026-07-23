from dataclasses import dataclass

import mock
import pytest
import shapely
from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
    QgsCoordinateReferenceSystem,
    QgsCurvePolygon,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsLineString,
    QgsPoint,
    QgsPointLocator,
    QgsPointXY,
    QgsPolygon,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)
from shapely.testing import assert_geometries_equal

from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureIDInvalid,
    FeatureManager,
    build_feature_mapping,
    get_field_config_value,
    get_float_value_from_feature,
    get_point_locator,
    get_src_geometry,
    resolve_id,
    update_attributes,
)
from threedi_schematisation_editor.warnings import (
    FeaturesImporterWarning,
    GeometryImporterWarning,
)


@pytest.fixture
def node_fields():
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("foo", QVariant.String))
    return fields


@pytest.fixture
def node_point():
    return QgsPointXY(1.0, 2.0)


@pytest.fixture
def node_geom(node_point):
    return QgsGeometry.fromPointXY(node_point)


@pytest.mark.parametrize("next_id", [1, 100])
def test_feature_manager_increment_id(next_id, node_geom, node_fields):
    manager = FeatureManager(auto_id=True, next_id=next_id)
    assert manager.next_id == next_id
    node_feat = manager.create_new(node_geom, node_fields)
    assert node_feat["id"] == next_id
    assert manager.next_id == next_id + 1


def test_feature_manager_not_set_id(node_geom, node_fields):
    manager = FeatureManager(next_id=1)
    node_feat = manager.create_new(node_geom, node_fields, set_id=False)
    assert node_feat["id"] is None
    assert manager.next_id == 1


def test_feature_manager_create_new(node_geom, node_fields):
    manager = FeatureManager()
    node_feat = manager.create_new(node_geom, node_fields)
    assert node_feat.geometry().asWkt() == node_geom.asWkt()


def test_feature_manager_create_new_with_attributes(node_geom, node_fields):
    manager = FeatureManager()
    node_feat = manager.create_new(node_geom, node_fields, attributes={"foo": "bar"})
    assert node_feat["foo"] == "bar"


@pytest.mark.parametrize("auto_id, kwargs", [(True, {"explicit_id": 42}), (False, {})])
def test_feature_manager_auto_id_clash(node_geom, node_fields, auto_id, kwargs):
    manager = FeatureManager(auto_id=auto_id)
    with pytest.raises(ValueError):
        manager.create_new(node_geom, node_fields, **kwargs)


def test_feature_manager_explicit_id(node_geom, node_fields):
    """explicit_id sets the ID and does not advance next_id."""
    manager = FeatureManager(auto_id=False)
    node_feat = manager.create_new(node_geom, node_fields, explicit_id=42)
    assert node_feat["id"] == 42
    assert manager.next_id == 1  # next_id must not advance
    assert 42 in manager.used_ids


@pytest.mark.parametrize(
    "auto_id, explicit_id, existing_ids, conflict, expected_id",
    [
        (False, 42, {1, 2, 3}, False, 42),
        (False, 5, {5, 10}, True, None),
        (True, None, {1, 2, 3}, False, 1),
    ],
)
def test_feature_manager_explicit_id(
    node_geom, node_fields, auto_id, explicit_id, existing_ids, conflict, expected_id
):
    manager = FeatureManager(auto_id=auto_id, existing_ids=existing_ids)
    if conflict:
        with pytest.warns(FeaturesImporterWarning):
            result = manager.create_new(node_geom, node_fields, explicit_id=explicit_id)
        assert result is None
    else:
        result = manager.create_new(node_geom, node_fields, explicit_id=explicit_id)
        assert result["id"] == expected_id


@dataclass
class TestModel:
    id: int
    missing_field: str


@pytest.mark.parametrize(
    "fields_config,explicit_id_valid",
    [
        ({"id": {"method": ColumnImportMethod.AUTO.value}}, False),
        ({}, False),
        (
            {
                "id": {
                    "method": ColumnImportMethod.ATTRIBUTE.value,
                    "source_attribute": "id",
                }
            },
            True,
        ),
    ],
)
def test_resolve_id(fields_config, explicit_id_valid):
    id_val = 5
    src_feat = create_feature_with_fields("id")
    src_feat.setAttribute("id", id_val)
    explicit_id = resolve_id(fields_config, src_feat)
    if explicit_id_valid:
        assert explicit_id == id_val
    else:
        assert explicit_id is None


@pytest.mark.parametrize(
    "fields_config",
    [
        {
            "id": {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                "source_attribute": "id",
            }
        },
        {"id": {"method": ColumnImportMethod.DEFAULT.value, "default_value": "foo"}},
    ],
)
def test_resolve_id_invalid(fields_config):
    src_feat = create_feature_with_fields("id")
    src_feat.setAttribute("id", "foo")
    with pytest.raises(FeatureIDInvalid):
        resolve_id(fields_config, src_feat)


def create_feature_with_fields(*field_names):
    """Helper function to create a feature with the specified fields."""
    fields = QgsFields()
    for field_name in field_names:
        fields.append(QgsField(field_name, 10))  # 10 is the type code for string
    feature = QgsFeature(fields)
    return feature


@pytest.mark.parametrize(
    "field_config,source_val,new_val,expected_val",
    [
        ({"method": ColumnImportMethod.AUTO.value}, 1, 2, 2),
        ({"method": ColumnImportMethod.DEFAULT.value, "default_value": 42}, 1, 2, 2),
    ],
)
def test_update_attributes(field_config, source_val, new_val, expected_val):
    """id field is always skipped by update_attributes regardless of method."""
    fields_config = {"id": field_config}
    source_feat = create_feature_with_fields("id", "foo")
    source_feat.setAttribute("id", source_val)
    new_feat = create_feature_with_fields("id")
    new_feat.setAttribute("id", new_val)
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat["id"] == expected_val


@pytest.mark.parametrize(
    "field_config,source_val,expected_val",
    [
        ({"method": ColumnImportMethod.AUTO.value}, 1, NULL),
        (
            {"method": ColumnImportMethod.ATTRIBUTE.value, "source_attribute": "id"},
            1,
            1,
        ),
        (
            {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                "source_attribute": "foo",
                "default_value": 42,
            },
            1,
            42,
        ),
        (
            {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                "source_attribute": "id",
                "value_map": {"1": 100, "2": 200},
            },
            1,
            100,
        ),
        ({"method": ColumnImportMethod.DEFAULT.value, "default_value": 42}, 1, 42),
        (
            {"method": ColumnImportMethod.EXPRESSION.value, "expression": "10 + 10"},
            1,
            20,
        ),
    ],
)
def test_get_field_config_value(field_config, source_val, expected_val):
    fields_config = {"id": field_config}
    source_feat = create_feature_with_fields("id", "foo")
    source_feat.setAttribute("id", source_val)
    assert get_field_config_value(fields_config["id"], source_feat) == expected_val


def test_get_field_config_value_invalid_field_name():
    fields_config = {
        "id": {
            "method": ColumnImportMethod.ATTRIBUTE.value,
            ColumnImportMethod.ATTRIBUTE.value: "bar",
        }
    }
    source_feat = create_feature_with_fields("id", "foo")
    assert get_field_config_value(fields_config["id"], source_feat) == NULL


def test_update_attributes_missing_field():
    """Test update_attributes with a field missing from the config."""
    # Setup
    fields_config = {}
    source_feat = create_feature_with_fields("id")
    source_feat.setAttribute("id", 1)
    new_feat = create_feature_with_fields("missing_field")
    new_feat.setAttribute("missing_field", "original_value")
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat["missing_field"] == "original_value"


def test_update_attributes_id_always_skipped():
    """id field is always skipped by update_attributes, even with a type conversion error."""
    fields_config = {
        "id": {
            "method": ColumnImportMethod.DEFAULT.value,
            "default_value": "not_an_int",
        }
    }
    source_feat = create_feature_with_fields("id")
    source_feat.setAttribute("id", 1)

    new_feat = create_feature_with_fields("id")
    new_feat.setAttribute("id", 1)

    # No warning, no change — id is handled before create_new, never via update_attributes
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat["id"] == 1


@pytest.fixture
def node_fields():
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("foo", QVariant.String))
    return fields


@pytest.fixture
def node_point():
    return QgsPointXY(1.0, 2.0)


@pytest.fixture
def node_geom(node_point):
    return QgsGeometry.fromPointXY(node_point)


def test_feature_manager_create_new(node_geom, node_fields):
    manager = FeatureManager()
    node_feat = manager.create_new(node_geom, node_fields)
    assert node_feat.geometry().asWkt() == node_geom.asWkt()


def test_feature_manager_create_new_with_attributes(node_geom, node_fields):
    manager = FeatureManager()
    node_feat = manager.create_new(node_geom, node_fields, attributes={"foo": "bar"})
    assert node_feat["foo"] == "bar"


@pytest.mark.parametrize(
    "value, expected_value",
    [
        (1, 1),
        ("1", 1),
        ("foo", 0),
        (NULL, 0),
    ],
)
def test_get_value_from_feature_with_field(value, expected_value):
    feat = {"foo": value}
    assert get_float_value_from_feature(feat, "foo", 0) == expected_value


@pytest.mark.parametrize("field", ["", None])
def test_get_value_from_feature_no_field(field):
    feat = {"foo": 1}
    assert get_float_value_from_feature(feat, "", 0) == 0


def test_get_value_from_feature_field_not_present():
    feat = {"bar": 1}
    assert get_float_value_from_feature(feat, "foo", 0) == 0


class TestGetSrcGeometry:
    @pytest.mark.parametrize(
        "geom",
        [
            QgsGeometry.fromPointXY(QgsPointXY(10, 20)),
            QgsGeometry.fromPolygonXY(
                [[QgsPointXY(10, 20), QgsPointXY(100, 40), QgsPointXY(10, 20)]]
            ),
            QgsGeometry.fromPolylineXY([QgsPointXY(10, 20), QgsPointXY(100, 40)]),
        ],
    )
    def test_unchanged(self, geom):
        feature = QgsFeature()
        feature.setGeometry(geom)
        feat_geom = get_src_geometry(feature)

        assert_geometries_equal(
            shapely.wkt.loads(geom.asWkt()), shapely.wkt.loads(feat_geom.asWkt())
        )

    @pytest.mark.parametrize(
        "geom",
        [
            QgsGeometry.fromMultiPointXY([QgsPointXY(10, 20), QgsPointXY(100, 40)]),
            QgsGeometry.fromPointXY(QgsPointXY(10, 20)),
        ],
    )
    def test_multipart(self, geom):
        feature = QgsFeature()
        feature.setGeometry(geom)
        feat_geom = get_src_geometry(feature)
        assert not feat_geom.isMultipart()
        assert feat_geom.asPoint() == QgsPointXY(10, 20)

    @pytest.mark.parametrize(
        "geom",
        [
            QgsGeometry.fromPointXY(QgsPointXY(0, 0)),
            QgsGeometry.fromPoint(QgsPoint(0, 0, 10, 10)),
        ],
    )
    def test_not_flat_point(self, geom):
        feature = QgsFeature()
        feature.setGeometry(geom)
        feat_geom = get_src_geometry(feature)
        assert feat_geom.wkbType() == QgsWkbTypes.Point
        assert feat_geom.asPoint() == QgsPointXY(0, 0)

    @pytest.mark.parametrize(
        "geom",
        [
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(10, 10)]),
            QgsGeometry.fromPolyline([QgsPoint(0, 0, 5, 5), QgsPoint(10, 10, 5, 50)]),
        ],
    )
    def test_not_flat_line(self, geom):
        feature = QgsFeature()
        feature.setGeometry(geom)
        feat_geom = get_src_geometry(feature)
        assert feat_geom.wkbType() == QgsWkbTypes.LineString
        assert feat_geom.asPolyline() == [QgsPointXY(0, 0), QgsPointXY(10, 10)]

    @pytest.mark.parametrize(
        "line_geom",
        [
            QgsLineString([QgsPointXY(0, 0), QgsPointXY(10, 10), QgsPointXY(0, 0)]),
            QgsLineString(
                [QgsPoint(0, 0, 5, 5), QgsPoint(10, 10, 5, 50), QgsPoint(0, 0, 5, 5)]
            ),
        ],
    )
    def test_not_flat_polygon(self, line_geom):
        # create polygon geometry
        polygon = QgsPolygon()
        polygon.setExteriorRing(line_geom)
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry(polygon))
        feat_geom = get_src_geometry(feature)
        assert feat_geom.wkbType() == QgsWkbTypes.Polygon
        assert feat_geom.asPolygon() == [
            [QgsPointXY(0, 0), QgsPointXY(10, 10), QgsPointXY(0, 0)]
        ]

    def test_curved(self):
        line_geom = QgsLineString(
            [QgsPointXY(0, 0), QgsPointXY(10, 10), QgsPointXY(0, 0)]
        )
        curve = QgsCurvePolygon()
        curve.setExteriorRing(line_geom)
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry(curve))
        feat_geom = get_src_geometry(feature)
        assert feat_geom.wkbType() == QgsWkbTypes.Polygon
        assert feat_geom.asPolygon() == [
            [QgsPointXY(0, 0), QgsPointXY(10, 10), QgsPointXY(0, 0)]
        ]

    def test_warnings_no_geometry(self):
        feature = QgsFeature()
        with pytest.warns(GeometryImporterWarning):
            get_src_geometry(feature)

    def test_warnings_no_geometry_none_ok(self):
        feature = QgsFeature()
        with pytest.warns(None) as record:
            get_src_geometry(feature, none_ok=True)

    def test_warnings_unsupported_type(self):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry())
        with pytest.warns(GeometryImporterWarning):
            get_src_geometry(feature, none_ok=True)

    def test_warnings_cannot_convert(self):
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry())
        with mock.patch.object(
            QgsGeometry, "coerceToType", side_effect=Exception("Mock conversion error")
        ):
            with pytest.warns(GeometryImporterWarning):
                get_src_geometry(feature, none_ok=True)


@pytest.mark.parametrize("use_context", [True, False])
def test_get_point_locator(use_context):
    layer = QgsVectorLayer("Point?crs=EPSG:28992", "test", "memory")
    if use_context:
        context = mock.Mock()
        project = QgsProject.instance()  # Use real project instance
        context.project.return_value = project
    else:
        context = None
    locator = get_point_locator(layer, context)
    assert isinstance(locator, QgsPointLocator)
    assert locator.destinationCrs().authid() == "EPSG:28992"
    if use_context:
        assert context.project.call_count == 1


# ---------------------------------------------------------------------------
# compute_selected_ids
# ---------------------------------------------------------------------------

from threedi_schematisation_editor.vector_data_importer.settings_models import (
    SourceSettings,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    compute_selected_ids,
)


def _make_layer_with_values(values):
    """Return a memory layer with a single integer 'value' field and one feature per entry."""
    layer = QgsVectorLayer("NoGeometry", "test", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("value", QVariant.Int)])
    layer.updateFields()
    features = []
    for v in values:
        feat = QgsFeature(layer.fields())
        feat.setAttribute("value", v)
        features.append(feat)
    provider.addFeatures(features)
    return layer


@pytest.mark.parametrize(
    "selected_indices, expression, expected_indices",
    [
        # Case 1: no selection, no expression -> None (all features)
        ([], None, None),
        # Case 2: selected only, no expression -> selected IDs
        ([0, 1], None, [0, 1]),
        # Case 3: no selection, expression -> filtered by expression
        ([], '"value" > 2', [2, 3, 4]),
        # Case 4: selected + expression -> expression applied on selection only
        ([0, 2, 4], '"value" > 2', [2, 4]),
        # Expression that matches nothing
        ([], '"value" > 99', []),
        # Expression that matches all
        ([], '"value" >= 1', [0, 1, 2, 3, 4]),
    ],
)
def test_compute_selected_ids(selected_indices, expression, expected_indices):
    layer = _make_layer_with_values([1, 2, 3, 4, 5])
    all_ids = [feat.id() for feat in layer.getFeatures()]

    if len(selected_indices) > 0:
        layer.selectByIds([all_ids[i] for i in selected_indices])

    settings = SourceSettings(
        use_selected_features=len(selected_indices) > 0,
        include_expression=expression,
    )

    result = compute_selected_ids(layer, settings)

    if expected_indices is None:
        assert result is None
    else:
        expected_ids = [all_ids[i] for i in expected_indices]
        assert sorted(result) == sorted(expected_ids)


def test_compute_selected_ids_invalid_expression_warns_and_returns_candidates():
    layer = _make_layer_with_values([1, 2, 3])
    all_ids = [feat.id() for feat in layer.getFeatures()]
    layer.selectByIds([all_ids[0]])
    settings = SourceSettings(
        use_selected_features=True, include_expression="((invalid(("
    )
    import warnings as stdlib_warnings

    from threedi_schematisation_editor.warnings import FeaturesImporterWarning

    with stdlib_warnings.catch_warnings(record=True) as caught:
        stdlib_warnings.simplefilter("always")
        result = compute_selected_ids(layer, settings)
    assert sorted(result) == [all_ids[0]]  # falls back to candidate_ids
    assert any(issubclass(w.category, FeaturesImporterWarning) for w in caught)


def test_compute_selected_ids_unknown_field_warns_and_returns_candidates():
    layer = _make_layer_with_values([1, 2, 3])
    all_ids = [feat.id() for feat in layer.getFeatures()]
    settings = SourceSettings(include_expression='"nonexistent" > 1')
    import warnings as stdlib_warnings

    from threedi_schematisation_editor.warnings import FeaturesImporterWarning

    with stdlib_warnings.catch_warnings(record=True) as caught:
        stdlib_warnings.simplefilter("always")
        result = compute_selected_ids(layer, settings)
    assert result is None  # falls back to candidate_ids (None = all)
    assert any(issubclass(w.category, FeaturesImporterWarning) for w in caught)


@pytest.fixture
def simple_layer():
    layer = QgsVectorLayer("NoGeometry", "test", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("code", QVariant.String)])
    layer.updateFields()
    f1 = QgsFeature(layer.fields())
    f2 = QgsFeature(layer.fields())
    f1.setAttribute("code", "abc")
    f2.setAttribute("code", "xyz")
    provider.addFeatures([f1, f2])
    return layer


@pytest.mark.parametrize(
    "config, values, expected_keys",
    [
        [
            {"method": "source_attribute", "source_attribute": "code"},
            ["abc", "xyz"],
            ["abc", "xyz"],
        ],
        [
            {"method": "expression", "expression": '"code"'},
            ["abc", "xyz"],
            ["abc", "xyz"],
        ],
        [{"method": "source_attribute", "source_attribute": "bar"}, ["abc", "xyz"], []],
        [{}, ["abc", "xyz"], []],
        [{"method": "auto"}, ["abc", "xyz"], []],
        [{"method": "expression", "expression": '"code(('}, ["abc", "xyz"], []],
        [
            {"method": "source_attribute", "source_attribute": "code"},
            ["abc", "abc", "abc"],
            [],
        ],
    ],
)
def test_build_feature_mapping(config, values, expected_keys):
    layer = QgsVectorLayer("NoGeometry", "test", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("code", QVariant.String)])
    layer.updateFields()
    for value in values:
        f = QgsFeature(layer.fields())
        f.setAttribute("code", value)
        provider.addFeatures([f])
    result = build_feature_mapping(layer.getFeatures(), config)
    assert set(result.keys()) == set(expected_keys)
    for feature in layer.getFeatures():
        if feature["code"] in expected_keys:
            assert result[feature["code"]] == feature


@pytest.mark.parametrize("simplify", [True, False])
def test_get_substring_geometry(simplify):
    """get_substring_geometry returns a QgsGeometry; simplify reduces it to 2 vertices."""
    from threedi_schematisation_editor.vector_data_importer.utils import (
        get_substring_geometry,
    )

    line_geom = QgsGeometry.fromPolylineXY(
        [QgsPointXY(0, 0), QgsPointXY(50, 0), QgsPointXY(100, 0)]
    )
    curve = line_geom.constGet()
    result = get_substring_geometry(curve, 25.0, 75.0, simplify=simplify)

    assert isinstance(result, QgsGeometry)
    assert result.length() == pytest.approx(50.0)
    if simplify:
        assert len(result.asPolyline()) == 2
    else:
        assert len(result.asPolyline()) >= 2


@pytest.mark.parametrize("initial_nodes", [["start"], [], ["start", "end"]])
def test_update_conduit_endpoints(initial_nodes):
    """update_conduit_endpoints assigns connection_node_id_start/_end; creates missing nodes."""
    from unittest.mock import MagicMock

    from threedi_schematisation_editor.vector_data_importer.utils import (
        update_conduit_endpoints,
    )

    points = {"start": (QgsPointXY(0, 0), 101), "end": (QgsPointXY(100, 0), 102)}
    start_point = QgsPointXY(0, 0)
    end_point = QgsPointXY(100, 0)
    node_by_location = {points[name][0]: points[name][1] for name in initial_nodes}

    node_layer_fields = QgsFields()
    node_layer_fields.append(QgsField("id", QVariant.Int))

    features_to_add = []
    for name, (pt, node_id) in points.items():
        if name not in initial_nodes:
            feat = QgsFeature(node_layer_fields)
            feat.setGeometry(QgsGeometry.fromPointXY(pt))
            feat["id"] = node_id
            features_to_add.append(feat)
    mock_features = features_to_add.copy()

    node_manager = MagicMock()

    def mock_create_new(geom, fields, attributes):
        feat = mock_features.pop(0)
        node_by_location[geom.asPoint()] = feat["id"]
        return feat

    node_manager.create_new.side_effect = mock_create_new

    conduit_fields = QgsFields()
    conduit_fields.append(QgsField("id", QVariant.Int))
    conduit_fields.append(QgsField("connection_node_id_start", QVariant.Int))
    conduit_fields.append(QgsField("connection_node_id_end", QVariant.Int))
    feature = QgsFeature(conduit_fields)
    feature.setGeometry(QgsGeometry.fromPolylineXY([start_point, end_point]))

    result = update_conduit_endpoints(
        feature,
        node_by_location,
        node_layer_fields,
        {"name": "Test Node"},
        node_manager,
    )

    assert result == features_to_add
    assert node_by_location[start_point] == 101
    assert node_by_location[end_point] == 102
    assert feature["connection_node_id_start"] == 101
    assert feature["connection_node_id_end"] == 102
