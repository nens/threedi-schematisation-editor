import pytest
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFields, QgsField
from PyQt5.QtCore import QVariant
from threedi_schematisation_editor.custom_tools.importers import ConnectionNodeManager


@pytest.mark.parametrize('next_connection_node_id', [1, 100])
def test_connection_node_manager_add_point(next_connection_node_id):
    manager = ConnectionNodeManager(next_connection_node_id)
    assert manager.next_connection_node_id == next_connection_node_id
    point = QgsPointXY(1.0, 2.0)
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    node_feat = manager.create_node_for_point(point, fields)
    assert node_feat.geometry().asPoint() == point
    assert node_feat["id"] == next_connection_node_id
    assert manager.next_connection_node_id == next_connection_node_id + 1
