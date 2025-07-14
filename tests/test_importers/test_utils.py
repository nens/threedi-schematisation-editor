import pytest
from dataclasses import dataclass

from PyQt5.QtCore import QVariant

from qgis.core import (
    QgsFeature,
    QgsExpression,
    QgsExpressionContext,
    NULL,
    QgsFields,
    QgsField,
    QgsGeometry,
    QgsWkbTypes,
    QgsPointXY,
)

from threedi_schematisation_editor.custom_tools.utils import update_attributes, FeatureManager, get_substring_geometry, \
    ColumnImportMethod


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


@pytest.mark.parametrize('next_id', [1, 100])
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


@pytest.mark.parametrize('field_config,source_val,new_val,expected_val',
                         [
                             ({'method': ColumnImportMethod.AUTO.value}, 1, 2, 2),
                             ({
                                  'method': ColumnImportMethod.ATTRIBUTE.value,
                                  'source_attribute': 'id'
                              }, 1, 2, 1),
                             ({'method': ColumnImportMethod.ATTRIBUTE.value,
                               'source_attribute': 'foo',
                               'default_value': 42}, 1, 2, 42),
                             ({'method': ColumnImportMethod.ATTRIBUTE.value,
                               'source_attribute': 'id',
                               'value_map': {'1': 100, '2': 200}}, 1, 2, 100),
                             ({'method': ColumnImportMethod.DEFAULT.value, 'default_value': 42}, 1, 2, 42),
                             ({'method': ColumnImportMethod.EXPRESSION.value, 'expression': '10 + 10'}, 1, 2, 20),
                         ])
def test_update_attributes(field_config, source_val, new_val, expected_val):
    fields_config = {'id': field_config}
    source_feat = create_feature_with_fields('id', 'foo')
    source_feat.setAttribute('id', source_val)
    new_feat = create_feature_with_fields('id')
    new_feat.setAttribute('id', new_val)
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat['id'] == expected_val


def test_update_attributes_missing_field():
    """Test update_attributes with a field missing from the config."""
    # Setup
    fields_config = {}
    source_feat = create_feature_with_fields('id')
    source_feat.setAttribute('id', 1)
    new_feat = create_feature_with_fields('missing_field')
    new_feat.setAttribute('missing_field', 'original_value')
    update_attributes(fields_config, TestModel, source_feat, new_feat)
    assert new_feat['missing_field'] == 'original_value'


def test_update_attributes_type_conversion_error():
    fields_config = {
        'id': {
            'method': ColumnImportMethod.DEFAULT.value,
            'default_value': 'no_an_int'
        }
    }
    source_feat = create_feature_with_fields('id')
    source_feat.setAttribute('id', 1)

    new_feat = create_feature_with_fields('id')
    new_feat.setAttribute('id', 1)

    # Execute
    with pytest.warns(UserWarning):
        update_attributes(fields_config, TestModel, source_feat, new_feat)

    # Assert
    assert new_feat['id'] == NULL


@pytest.mark.parametrize('simplify', [True, False])
def test_get_substring_geometry_argument_processing(simplify):
    """Test that get_substring_geometry processes the simplify argument correctly."""
    # Create a simple line geometry for testing
    line_geom = QgsGeometry.fromPolylineXY([
        QgsPointXY(0, 0),
        QgsPointXY(50, 0),
        QgsPointXY(100, 0)
    ])

    # Get the underlying curve object
    curve = line_geom.constGet()

    # Test parameters
    start_distance = 25.0
    end_distance = 75.0

    # Call the function with simplify=False
    result = get_substring_geometry(curve, start_distance, end_distance, simplify=simplify)

    # Verify that both calls return a QgsGeometry object
    assert isinstance(result, QgsGeometry)

    if simplify:
        assert len(result.asPolyline()) == 2
    else:
        assert len(result.asPolyline()) >= 2

    assert result.length() == end_distance - start_distance


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


@pytest.mark.parametrize('next_id', [1, 100])
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