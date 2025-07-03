import pytest
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFields, QgsField
from PyQt5.QtCore import QVariant
from threedi_schematisation_editor.custom_tools.utils import FeatureManager


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