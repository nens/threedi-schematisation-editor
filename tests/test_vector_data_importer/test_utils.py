from dataclasses import dataclass

import mock
import pytest
import shapely
from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
    QgsCurvePolygon,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsLineString,
    QgsPoint,
    QgsPointXY,
    QgsPolygon,
    QgsWkbTypes,
)
from shapely.testing import assert_geometries_equal

from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureManager,
    get_float_value_from_feature,
    get_src_geometry,
    update_attributes,
)
from threedi_schematisation_editor.warnings import GeometryImporterWarning


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
    manager = FeatureManager(next_id)
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


@dataclass
class TestModel:
    id: int
    missing_field: str


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
        (
            {"method": ColumnImportMethod.ATTRIBUTE.value, "source_attribute": "id"},
            1,
            2,
            1,
        ),
        (
            {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                "source_attribute": "foo",
                "default_value": 42,
            },
            1,
            2,
            42,
        ),
        (
            {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                "source_attribute": "id",
                "value_map": {"1": 100, "2": 200},
            },
            1,
            2,
            100,
        ),
        ({"method": ColumnImportMethod.DEFAULT.value, "default_value": 42}, 1, 2, 42),
        (
            {"method": ColumnImportMethod.EXPRESSION.value, "expression": "10 + 10"},
            1,
            2,
            20,
        ),
    ],
)
def test_update_attributes(field_config, source_val, new_val, expected_val):
    fields_config = {"id": field_config}
    source_feat = create_feature_with_fields("id", "foo")
    source_feat.setAttribute("id", source_val)
    new_feat = create_feature_with_fields("id")
    new_feat.setAttribute("id", new_val)
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat["id"] == expected_val


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


def test_update_attributes_type_conversion_error():
    fields_config = {
        "id": {"method": ColumnImportMethod.DEFAULT.value, "default_value": "no_an_int"}
    }
    source_feat = create_feature_with_fields("id")
    source_feat.setAttribute("id", 1)

    new_feat = create_feature_with_fields("id")
    new_feat.setAttribute("id", 1)

    # Execute
    with pytest.warns(UserWarning):
        update_attributes(fields_config, TestModel, source_feat, new_feat)

    # Assert
    assert new_feat["id"] == NULL


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
    manager = FeatureManager(next_id)
    assert manager.next_id == next_id
    node_feat = manager.create_new(node_geom, node_fields)
    assert node_feat["id"] == next_id
    assert manager.next_id == next_id + 1


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
