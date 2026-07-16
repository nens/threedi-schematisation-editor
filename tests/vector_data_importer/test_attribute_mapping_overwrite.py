from unittest.mock import MagicMock

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import QgsFeature, QgsField, QgsFields, QgsGeometry, QgsPointXY

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer import settings_models as sm
from threedi_schematisation_editor.vector_data_importer.integrators import (
    LinearIntegrator,
    LinearIntegratorStructureData,
)
from threedi_schematisation_editor.vector_data_importer.processors import LineProcessor
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


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

    @pytest.fixture
    def node_fields(self):
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        return fields

    def test_process_feature_preserves_attribute_mapped_node_ids(
        self,
        source_line_feature_with_node_ids,
        target_fields,
        node_fields,
        import_settings_with_node_mapping,
    ):
        """When connection_node_id_start/end are explicitly attribute-mapped,
        process_feature should preserve those values instead of overwriting
        them with spatially snapped node IDs.

        This test currently FAILS, demonstrating the bug.
        """
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "weirs"
        node_layer = MagicMock()
        node_layer.fields.return_value = node_fields
        node_layer.name.return_value = "connection_nodes"

        processor = LineProcessor(
            target_layer,
            dm.Weir,
            node_layer,
            import_settings_with_node_mapping,
        )

        # Spatially snapped nodes C (id=42) and D (id=43)
        snapped_start_node = QgsFeature(node_fields)
        snapped_start_node.setAttribute("id", 42)
        snapped_start_node.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(11, 21)))
        snapped_end_node = QgsFeature(node_fields)
        snapped_end_node.setAttribute("id", 43)
        snapped_end_node.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(31, 41)))
        processor.get_node = MagicMock(
            side_effect=[
                (snapped_start_node, True),
                (snapped_end_node, True),
            ]
        )

        result = processor.process_feature(source_line_feature_with_node_ids)
        new_weir = result["weirs"][0]

        # Attribute mapping set these to 100 (A) and 200 (B).
        # Snapping found nodes 42 (C) and 43 (D).
        # The attribute-mapped values should be preserved.
        assert new_weir["connection_node_id_start"] == 100, (
            f"Expected attribute-mapped node A (100), got {new_weir['connection_node_id_start']}. "
            "Spatial snapping overwrote the attribute-mapped connection_node_id_start."
        )
        assert new_weir["connection_node_id_end"] == 200, (
            f"Expected attribute-mapped node B (200), got {new_weir['connection_node_id_end']}. "
            "Spatial snapping overwrote the attribute-mapped connection_node_id_end."
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

    def test_integrate_structure_preserves_attribute_mapped_node_ids(self):
        """When connection_node_id_start/end are explicitly attribute-mapped,
        integrate_structure_features should preserve those values.

        This test currently FAILS, demonstrating the bug.
        """
        from threedi_schematisation_editor import data_models as dm
        from threedi_schematisation_editor.vector_data_importer.utils import (
            ColumnImportMethod,
            FeatureManager,
        )

        # Set up fields
        channel_fields = QgsFields()
        channel_fields.append(QgsField("id", QVariant.Int))
        channel_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        channel_fields.append(QgsField("connection_node_id_end", QVariant.Int))

        weir_fields = QgsFields()
        weir_fields.append(QgsField("id", QVariant.Int))
        weir_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        weir_fields.append(QgsField("connection_node_id_end", QVariant.Int))

        node_fields = QgsFields()
        node_fields.append(QgsField("id", QVariant.Int))

        # Create a channel from (0,0) to (100,0) with existing nodes 1 and 2
        channel_feat = QgsFeature(channel_fields)
        channel_feat.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
        )
        channel_feat.setAttribute("id", 1)
        channel_feat.setAttribute("connection_node_id_start", 1)
        channel_feat.setAttribute("connection_node_id_end", 2)

        # Create existing nodes at channel endpoints
        node_1 = QgsFeature(node_fields)
        node_1.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(0, 0)))
        node_1.setAttribute("id", 1)

        node_2 = QgsFeature(node_fields)
        node_2.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(100, 0)))
        node_2.setAttribute("id", 2)

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

        # Create a conduit structure data for the weir at m=50 with length=10
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
        integrator.node_layer = MagicMock()
        integrator.node_layer.name.return_value = "Connection node"

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
        assert weir_feat["connection_node_id_start"] == 100, (
            "Attribute mapping should set connection_node_id_start to 100 (node A)"
        )
        assert weir_feat["connection_node_id_end"] == 200, (
            "Attribute mapping should set connection_node_id_end to 200 (node B)"
        )

        # Now simulate what integrate_structure_features does next:
        # It calls update_feature_endpoints which creates/finds nodes at the
        # structure's geometry endpoints and overwrites connection_node_id_start/end.
        # The weir geometry after placement is a substring of the channel at m=45..55.
        weir_polyline = weir_feat.geometry().asPolyline()
        start_point = weir_polyline[0]
        end_point = weir_polyline[-1]

        # These points are NOT in node_by_location yet, so update_feature_endpoints
        # will create new nodes (C and D) via add_node.
        # Set up add_node to create nodes with IDs 50 and 51 and update node_by_location.
        node_id_counter = [50]

        def mock_add_node(point, fields, attributes):
            node_feat = QgsFeature(node_fields)
            node_feat.setGeometry(QgsGeometry.fromPointXY(point))
            node_feat.setAttribute("id", node_id_counter[0])
            integrator.node_by_location[point] = node_id_counter[0]
            node_id_counter[0] += 1
            return node_feat

        integrator.add_node = mock_add_node

        new_nodes = LinearIntegrator.update_feature_endpoints(integrator, weir_feat)

        # After update_feature_endpoints, the values should STILL be A=100, B=200
        # (attribute mapping should take priority over spatial snapping)
        # This assertion currently FAILS - demonstrating the bug
        assert weir_feat["connection_node_id_start"] == 100, (
            f"Expected attribute-mapped node A (100), got {weir_feat['connection_node_id_start']}. "
            "update_feature_endpoints overwrote the attribute-mapped connection_node_id_start."
        )
        assert weir_feat["connection_node_id_end"] == 200, (
            f"Expected attribute-mapped node B (200), got {weir_feat['connection_node_id_end']}. "
            "update_feature_endpoints overwrote the attribute-mapped connection_node_id_end."
        )
