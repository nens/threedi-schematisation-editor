import pytest
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFields, QgsField
from PyQt5.QtCore import QVariant
from threedi_schematisation_editor.custom_tools.importers import ConnectionNodeManager


@pytest.fixture
def node_fields():
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    return fields


@pytest.fixture
def node_point():
    return QgsPointXY(1.0, 2.0)


@pytest.fixture
def node_geom(node_point):
    return QgsGeometry.fromPointXY(node_point)


@pytest.mark.parametrize('next_connection_node_id', [1, 100])
def test_connection_node_manager_increment_id(next_connection_node_id, node_geom, node_fields):
    manager = ConnectionNodeManager(next_connection_node_id)
    assert manager.next_connection_node_id == next_connection_node_id
    node_feat = manager.create_node(node_geom, node_fields)
    assert node_feat["id"] == next_connection_node_id
    assert manager.next_connection_node_id == next_connection_node_id + 1


def test_connection_node_manager_add_node(node_geom, node_fields):
    manager = ConnectionNodeManager()
    node_feat = manager.create_node(node_geom, node_fields)
    assert node_feat.geometry().asWkt() == node_geom.asWkt()


def test_connection_node_manager_add_node_from_point(node_point, node_fields):
    manager = ConnectionNodeManager()
    node_feat = manager.create_node_for_point(node_point, node_fields)
    assert node_feat.geometry().asPoint() == node_point
