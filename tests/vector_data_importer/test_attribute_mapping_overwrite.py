from unittest.mock import MagicMock

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer import settings_models as sm
from threedi_schematisation_editor.vector_data_importer.integrators import (
    LinearIntegrator,
    LinearIntegratorStructureData,
)
from threedi_schematisation_editor.vector_data_importer.processors import LineProcessor
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureManager,
)


@pytest.fixture
def node_layer_with_nodes():
    """Create a memory layer with nodes A (id=100) and B (id=200) at known locations."""
    layer = QgsVectorLayer("Point?crs=EPSG:4326", "Connection node", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("id", QVariant.Int)])
    layer.updateFields()

    node_a = QgsFeature(layer.fields())
    node_a.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(5, 5)))
    node_a.setAttribute("id", 100)

    node_b = QgsFeature(layer.fields())
    node_b.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 50)))
    node_b.setAttribute("id", 200)

    provider.addFeatures([node_a, node_b])
    layer.updateExtents()
    return layer


class TestLineProcessorAttributeMappingOverwrite:
    """Tests that attribute mapping for connection_node_id_start/end is preserved
    when the user explicitly maps these fields.

    Scenario:
    - Source feature has connection_node_id_start=100 (node A) and
      connection_node_id_end=200 (node B) via attribute mapping
    - Spatial snapping finds nodes C (id=42) and D (id=43) at the geometry endpoints
    - Expected: attribute-mapped values (100, 200) should be preserved
    - Actual (bug): snapping overwrites with (42, 43)
    """

    @pytest.fixture
    def source_line_feature_with_node_ids(self):
        """Source feature with connection_node_id_start/end attributes set."""
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id_start", QVariant.Int))
        fields.append(QgsField("connection_node_id_end", QVariant.Int))
        feature = QgsFeature(fields)
        feature.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(10, 20), QgsPointXY(30, 40)])
        )
        feature.setAttribute("id", 1)
        feature.setAttribute("connection_node_id_start", 100)  # Node A
        feature.setAttribute("connection_node_id_end", 200)  # Node B
        return feature

    @pytest.fixture
    def import_settings_with_node_mapping(self):
        """Import settings that map connection_node_id_start/end from source attributes."""
        return sm.ImportSettings(
            fields={
                "id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO),
                "connection_node_id_start": sm.FieldMapConfig(
                    method=ColumnImportMethod.ATTRIBUTE,
                    source_attribute="connection_node_id_start",
                ),
                "connection_node_id_end": sm.FieldMapConfig(
                    method=ColumnImportMethod.ATTRIBUTE,
                    source_attribute="connection_node_id_end",
                ),
            },
            connection_node_fields={
                "id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO),
            },
        )

    @pytest.fixture
    def target_fields(self):
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id_start", QVariant.Int))
        fields.append(QgsField("connection_node_id_end", QVariant.Int))
        return fields

    def test_process_feature_preserves_attribute_mapped_node_ids(
        self,
        source_line_feature_with_node_ids,
        target_fields,
        import_settings_with_node_mapping,
        node_layer_with_nodes,
    ):
        """When connection_node_id_start/end are explicitly attribute-mapped,
        process_feature should preserve those values and snap geometry to the
        referenced nodes.
        """
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "weirs"

        processor = LineProcessor(
            target_layer,
            dm.Weir,
            node_layer_with_nodes,
            import_settings_with_node_mapping,
        )

        # Mock get_node (should NOT be called when attribute mapping is used)
        processor.get_node = MagicMock(
            side_effect=AssertionError(
                "get_node should not be called for mapped fields"
            )
        )

        result = processor.process_feature(source_line_feature_with_node_ids)
        new_weir = result["weirs"][0]

        # Attribute mapping should preserve node IDs A=100, B=200
        assert new_weir["connection_node_id_start"] == 100, (
            f"Expected attribute-mapped node A (100), got {new_weir['connection_node_id_start']}. "
            "Spatial snapping overwrote the attribute-mapped connection_node_id_start."
        )
        assert new_weir["connection_node_id_end"] == 200, (
            f"Expected attribute-mapped node B (200), got {new_weir['connection_node_id_end']}. "
            "Spatial snapping overwrote the attribute-mapped connection_node_id_end."
        )

        # Geometry should be snapped to nodes A (5,5) and B (50,50)
        polyline = new_weir.geometry().asPolyline()
        assert polyline[0] == QgsPointXY(5, 5), (
            f"Geometry start should be snapped to node A at (5,5), got {polyline[0]}"
        )
        assert polyline[-1] == QgsPointXY(50, 50), (
            f"Geometry end should be snapped to node B at (50,50), got {polyline[-1]}"
        )


class TestIntegrationAttributeMappingOverwrite:
    """Tests that attribute mapping for connection_node_id_start/end is preserved
    during structure integration.

    Scenario:
    - A weir is integrated onto a channel
    - Attribute mapping sets connection_node_id_start=100 (A) and
      connection_node_id_end=200 (B)
    - Integration creates/finds nodes C and D at the structure's geometry endpoints
    - Expected: attribute-mapped values (100, 200) should be preserved
    - Actual (bug): update_feature_endpoints overwrites with C/D node IDs
    """

    def test_integrate_structure_preserves_attribute_mapped_node_ids(
        self, node_layer_with_nodes
    ):
        """When connection_node_id_start/end are explicitly attribute-mapped,
        _snap_geometry_to_mapped_nodes should preserve those values and snap
        geometry to the referenced nodes.
        """
        # Set up fields
        weir_fields = QgsFields()
        weir_fields.append(QgsField("id", QVariant.Int))
        weir_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        weir_fields.append(QgsField("connection_node_id_end", QVariant.Int))

        node_fields = QgsFields()
        node_fields.append(QgsField("id", QVariant.Int))

        # Create a channel from (0,0) to (100,0)
        channel_fields = QgsFields()
        channel_fields.append(QgsField("id", QVariant.Int))
        channel_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        channel_fields.append(QgsField("connection_node_id_end", QVariant.Int))

        channel_feat = QgsFeature(channel_fields)
        channel_feat.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
        )
        channel_feat.setAttribute("id", 1)
        channel_feat.setAttribute("connection_node_id_start", 1)
        channel_feat.setAttribute("connection_node_id_end", 2)

        # Create source weir feature with attribute-mapped node IDs A=100, B=200
        src_weir_fields = QgsFields()
        src_weir_fields.append(QgsField("id", QVariant.Int))
        src_weir_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        src_weir_fields.append(QgsField("connection_node_id_end", QVariant.Int))
        src_weir_fields.append(QgsField("length", QVariant.Double))

        src_weir = QgsFeature(src_weir_fields)
        src_weir.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 0)))
        src_weir.setAttribute("id", 10)
        src_weir.setAttribute("connection_node_id_start", 100)  # Node A
        src_weir.setAttribute("connection_node_id_end", 200)  # Node B
        src_weir.setAttribute("length", 10.0)

        conduit_structure = LinearIntegratorStructureData(
            conduit_id=1,
            feature=src_weir,
            m=50.0,
            length=10.0,
        )

        # Set up the integrator with mocks
        integrator = MagicMock(spec=LinearIntegrator)
        integrator.target_model_cls = dm.Weir
        integrator.conduit_model_cls = dm.Channel
        integrator.minimum_conduit_length = 1.0
        integrator.node_by_location = {
            QgsPointXY(0, 0): 1,
            QgsPointXY(100, 0): 2,
        }

        # Set up field configurations with attribute mapping for connection node IDs
        integrator.fields_configurations = {
            "id": {"method": "auto"},
            "connection_node_id_start": {
                "method": "source_attribute",
                "source_attribute": "connection_node_id_start",
            },
            "connection_node_id_end": {
                "method": "source_attribute",
                "source_attribute": "connection_node_id_end",
            },
        }

        # Set up layer fields mapping
        integrator.layer_fields_mapping = {
            "Weir": weir_fields,
            "Connection node": node_fields,
        }
        integrator.layer_field_names_mapping = {
            "Connection node": ["id"],
        }

        # Set up managers
        integrator.target_manager = FeatureManager(next_id=10)
        integrator.node_manager = FeatureManager(next_id=50)

        # Set up layers
        integrator.target_layer = MagicMock()
        integrator.target_layer.name.return_value = "Weir"
        integrator.integrate_layer = MagicMock()
        integrator.integrate_layer.name.return_value = "Channel"
        integrator.node_layer = node_layer_with_nodes

        # Call place_structures_on_conduit (which calls update_attributes)
        placed_features = LinearIntegrator.place_structures_on_conduit(
            integrator,
            [conduit_structure],
            channel_feat,
            simplify_structure_geometry=True,
        )

        assert len(placed_features) == 1
        weir_feat = placed_features[0]

        # After place_structures_on_conduit, attribute mapping should have set A=100, B=200
        assert weir_feat["connection_node_id_start"] == 100
        assert weir_feat["connection_node_id_end"] == 200

        # Now call _snap_geometry_to_mapped_nodes (the fix)
        new_nodes = LinearIntegrator._snap_geometry_to_mapped_nodes(
            integrator, weir_feat, True, True, {}
        )

        # Connection node IDs should STILL be 100 and 200
        assert weir_feat["connection_node_id_start"] == 100, (
            f"Expected attribute-mapped node A (100), got {weir_feat['connection_node_id_start']}. "
            "Integration overwrote the attribute-mapped connection_node_id_start."
        )
        assert weir_feat["connection_node_id_end"] == 200, (
            f"Expected attribute-mapped node B (200), got {weir_feat['connection_node_id_end']}. "
            "Integration overwrote the attribute-mapped connection_node_id_end."
        )

        # Geometry should be snapped to nodes A (5,5) and B (50,50)
        polyline = weir_feat.geometry().asPolyline()
        assert polyline[0] == QgsPointXY(5, 5), (
            f"Geometry start should be snapped to node A at (5,5), got {polyline[0]}"
        )
        assert polyline[-1] == QgsPointXY(50, 50), (
            f"Geometry end should be snapped to node B at (50,50), got {polyline[-1]}"
        )
