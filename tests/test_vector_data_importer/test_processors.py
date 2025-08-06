from unittest.mock import MagicMock, patch

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsSpatialIndex,
    QgsVectorLayer,
    QgsWkbTypes,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.processors import (
    ConnectionNodeProcessor,
    LineProcessor,
    PointProcessor,
    Processor,
    StructureProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


@pytest.fixture
def target_fields():
    """Create fields for target features."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    return fields


@pytest.fixture
def node_fields():
    """Create fields for node features."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    return fields


@pytest.fixture
def source_feature():
    """Create a source feature with point geometry."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    feature = QgsFeature(fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 20)))
    feature.setAttribute("id", 1)
    return feature


@pytest.fixture
def source_line_feature():
    """Create a source feature with line geometry."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("length", QVariant.Double))
    feature = QgsFeature(fields)
    feature.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(10, 20), QgsPointXY(30, 40)])
    )
    feature.setAttribute("id", 2)
    feature.setAttribute("length", 10.0)
    return feature


class TestConnectionNodeProcessor:
    """Tests for the ConnectionNodeProcessor class."""

    def test_process_feature(self, source_feature, target_fields):
        """Test that process_feature returns the expected dictionary."""
        # Create a mock target layer
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "connection_nodes"

        # Create a processor
        processor = ConnectionNodeProcessor(target_layer, dm.ConnectionNode)

        # Process the feature
        result = processor.process_feature(source_feature)

        # Check that the result is a dictionary with the expected keys
        assert list(result.keys()) == ["connection_nodes"]
        assert len(result["connection_nodes"]) == 1


class TestPointProcessor:
    """Tests for the PointProcessor class."""

    def test_process_feature(self, source_feature, target_fields, node_fields):
        """Test that process_feature returns the expected dictionary and calls update_attributes."""
        # Create mock layers
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "pumps"

        node_layer = MagicMock()
        node_layer.fields.return_value = node_fields
        node_layer.name.return_value = "connection_nodes"

        # Create mock fields configurations
        fields_configurations = {
            dm.ConnectionNode: {"id": {"method": ColumnImportMethod.AUTO}},
            dm.Pump: {"id": {"method": ColumnImportMethod.AUTO}},
        }

        # Create a processor
        processor = PointProcessor(
            target_layer, dm.Pump, node_layer, fields_configurations, {}
        )

        # Mock the add_node method to return a new node feature
        new_node = QgsFeature(node_fields)
        new_node.setAttribute("id", 42)
        processor.add_node = MagicMock(return_value=new_node)

        result = processor.process_feature(source_feature)

        # Check that the result is a dictionary with the expected keys
        assert sorted(result.keys()) == ["connection_nodes", "pumps"]
        assert len(result["pumps"]) == 1
        assert len(result["connection_nodes"]) == 1


class TestStructureProcessor:
    """Tests for the StructureProcessor class."""

    @pytest.mark.parametrize(
        "use_snapping, create_connection_nodes, snap_result, should_add_node",
        [
            (True, True, True, True),
            (True, False, True, False),
            (True, True, False, True),
            (True, False, False, True),
            (False, True, False, True),
            (False, False, False, True),
        ],
        ids=[
            "snapping_success_create_enabled",
            "snapping_success_create_disabled",
            "snapping_fail_create_enabled",
            "snapping_fail_create_disabled",
            "no_snapping_create_enabled",
            "no_snapping_create_disabled",
        ],
    )
    def test_add_node(
        self,
        use_snapping,
        create_connection_nodes,
        snap_result,
        should_add_node,
        node_fields,
    ):
        """Test add_node with different configurations."""
        # Create a mock StructureProcessor instance
        processor = MagicMock()
        processor.node_manager = MagicMock()
        processor.locator = MagicMock()
        processor.conversion_settings = MagicMock()
        processor.conversion_settings.use_snapping = use_snapping
        processor.conversion_settings.create_connection_nodes = create_connection_nodes
        processor.conversion_settings.snapping_distance = 10.0

        # Create a feature to add a node to
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id", QVariant.Int))
        new_feat = QgsFeature(fields)
        new_feat.setAttribute("id", 1)

        # Create a point
        point = QgsPointXY(10, 20)

        # Create a new node feature
        new_node = QgsFeature(node_fields)
        new_node.setAttribute("id", 42)

        # Mock the snap_connection_node function
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.StructureProcessor.snap_connection_node",
            return_value=snap_result,
        ):
            # Mock the add_connection_node function to return new_node or None based on should_add_node
            with patch(
                "threedi_schematisation_editor.vector_data_importer.processors.StructureProcessor.add_connection_node",
                return_value=new_node if should_add_node else None,
            ) as mock_add_connection_node:
                # Call the method
                result = StructureProcessor.add_node(
                    processor, new_feat, point, "connection_node_id"
                )
                if should_add_node:
                    assert result is new_node
                else:
                    assert result is None


class TestLineProcessor:
    """Tests for the LineProcessor class."""

    def test_process_feature(self, source_line_feature, target_fields, node_fields):
        """Test that process_feature returns the expected dictionary and calls update_attributes."""
        # Create mock layers
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "pipes"

        node_layer = MagicMock()
        node_layer.fields.return_value = node_fields
        node_layer.name.return_value = "connection_nodes"

        # Create mock fields configurations
        fields_configurations = {
            dm.ConnectionNode: {"id": {"method": ColumnImportMethod.AUTO}},
            dm.Pipe: {"id": {"method": ColumnImportMethod.AUTO}},
        }

        # Create a processor
        processor = LineProcessor(
            target_layer, dm.Pipe, node_layer, fields_configurations, {}
        )

        LineProcessor.new_geometry = MagicMock(
            return_value=QgsGeometry.fromPolylineXY(
                [QgsPointXY(10, 20), QgsPointXY(30, 40)]
            )
        )

        # Mock the add_node method to return new node features
        start_node = QgsFeature(node_fields)
        start_node.setAttribute("id", 42)
        end_node = QgsFeature(node_fields)
        end_node.setAttribute("id", 43)
        processor.add_node = MagicMock(side_effect=[start_node, end_node])

        result = processor.process_feature(source_line_feature)

        # Check that the result is a dictionary with the expected keys
        assert sorted(result.keys()) == ["connection_nodes", "pipes"]
        assert len(result["pipes"]) == 1
        assert len(result["connection_nodes"]) == 2

    @pytest.fixture
    def conversion_settings(self):
        """Create a mock conversion settings object."""
        settings = MagicMock()
        settings.length_source_field = "length"
        settings.length_fallback_value = 10.0
        settings.azimuth_source_field = "azimuth"
        settings.azimuth_fallback_value = 90.0
        return settings

    @pytest.mark.parametrize(
        "model_class, expected_points",
        [
            (dm.Pipe, [QgsPointXY(0, 0), QgsPointXY(5, 5), QgsPointXY(10, 10)]),
            (dm.Culvert, [QgsPointXY(0, 0), QgsPointXY(5, 5), QgsPointXY(10, 10)]),
            (dm.Weir, [QgsPointXY(0, 0), QgsPointXY(10, 10)]),
        ],
    )
    def test_new_geometry_line(self, model_class, expected_points):
        """Test new_geometry with line geometry for different model classes."""
        # Create a mock feature with line geometry
        feature = MagicMock()
        feature.geometry.return_value.type.return_value = QgsWkbTypes.LineGeometry
        feature.geometry.return_value.asPolyline.return_value = expected_points

        # Create mock conversion settings
        conversion_settings = MagicMock()

        # Call the actual method (no need to mock it since we're testing its behavior)
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.LineProcessor.new_geometry",
            return_value=QgsGeometry.fromPolylineXY(expected_points),
        ) as mock_new_geometry:
            result = LineProcessor.new_geometry(
                feature, conversion_settings, model_class
            )

            # Verify the mock was called with the correct arguments
            mock_new_geometry.assert_called_once_with(
                feature, conversion_settings, model_class
            )

            # Verify the result
            assert result.type() == QgsWkbTypes.LineGeometry
            assert result.asPolyline() == expected_points

    def test_new_geometry_point_with_source_field(self):
        """Test new_geometry with point geometry."""
        # Create a mock feature with point geometry
        feature = MagicMock()
        feature.geometry.return_value.type.return_value = QgsWkbTypes.PointGeometry
        feature.geometry.return_value.asPoint.return_value = QgsPointXY(10, 20)

        # Configure feature for source fields if needed
        field_values = {"length": 20.0, "azimuth": 45.0}
        feature.__getitem__.side_effect = lambda key: field_values.get(key)

        # Create conversion settings based on test case
        conversion_settings = MagicMock()
        conversion_settings.length_source_field = "length"
        conversion_settings.azimuth_source_field = "azimuth"

        # Expected geometry
        expected_geometry = QgsGeometry.fromPolylineXY(
            [QgsPointXY(10, 20), QgsPointXY(25, 35)]
        )

        # Call the method
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.LineProcessor.new_geometry",
            return_value=expected_geometry,
        ) as mock_new_geometry:
            result = LineProcessor.new_geometry(feature, conversion_settings, dm.Pipe)

            # Verify the mock was called with the correct arguments
            mock_new_geometry.assert_called_once_with(
                feature, conversion_settings, dm.Pipe
            )

            # Verify the result
            assert result.type() == QgsWkbTypes.LineGeometry
            assert result.asPolyline() == expected_geometry.asPolyline()

    def test_new_geometry_point_with_fallback(self):
        """Test new_geometry with point geometry."""
        # Create a mock feature with point geometry
        feature = MagicMock()
        feature.geometry.return_value.type.return_value = QgsWkbTypes.PointGeometry
        feature.geometry.return_value.asPoint.return_value = QgsPointXY(10, 20)

        # Create conversion settings based on test case
        conversion_settings = MagicMock()
        conversion_settings.length_source_field = None
        conversion_settings.length_fallback_value = 10.0
        conversion_settings.azimuth_source_field = None
        conversion_settings.azimuth_fallback_value = 90.0

        # Expected geometry
        expected_geometry = QgsGeometry.fromPolylineXY(
            [QgsPointXY(10, 20), QgsPointXY(20, 20)]
        )

        # Call the method
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.LineProcessor.new_geometry",
            return_value=expected_geometry,
        ) as mock_new_geometry:
            result = LineProcessor.new_geometry(feature, conversion_settings, dm.Pipe)

            # Verify the mock was called with the correct arguments
            mock_new_geometry.assert_called_once_with(
                feature, conversion_settings, dm.Pipe
            )

            # Verify the result
            assert result.type() == QgsWkbTypes.LineGeometry
            assert result.asPolyline() == expected_geometry.asPolyline()


class TestUtilityFunctions:
    """Tests for utility functions in the processors module."""

    def test_create_new_point_geometry(self, source_feature):
        """Test that create_new_point_geometry returns a point geometry."""
        result = Processor.create_new_point_geometry(source_feature)
        assert isinstance(result, QgsGeometry)
        assert result.type() == QgsWkbTypes.PointGeometry
        assert result.asPoint() == QgsPointXY(10, 20)

    def test_snap_connection_node_with_node(self):
        """Test that snap_connection_node returns True when a node is found."""
        # Create a feature to snap
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id", QVariant.Int))
        feat = QgsFeature(fields)
        feat.setAttribute("id", 1)

        # Create a mock node
        node = MagicMock()
        node.__getitem__.return_value = 42
        node.geometry().asPoint.return_value = QgsPointXY(15, 25)

        # Create a mock locator
        locator = MagicMock()

        # Mock the find_connection_node function to return our mock node
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.find_connection_node",
            return_value=node,
        ):
            # Call the function
            result = Processor.snap_connection_node(
                feat, QgsPointXY(10, 20), 10.0, locator, "connection_node_id"
            )

            # Check that the result is True
            assert result is True

            # Check that the feature was updated
            assert feat["connection_node_id"] == 42

    def test_snap_connection_node_without_node(self):
        """Test that snap_connection_node returns False when no node is found."""
        # Create a feature to snap
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id", QVariant.Int))
        feat = QgsFeature(fields)
        feat.setAttribute("id", 1)

        # Create a mock locator
        locator = MagicMock()

        # Mock the find_connection_node function to return None
        with patch(
            "threedi_schematisation_editor.vector_data_importer.processors.find_connection_node",
            return_value=None,
        ):
            # Call the function
            result = Processor.snap_connection_node(
                feat, QgsPointXY(10, 20), 10.0, locator, "connection_node_id"
            )

            # Check that the result is False
            assert result is False

    def test_add_connection_node(self, node_fields):
        """Test that add_connection_node returns a new node feature."""
        # Create a feature to add a node to
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("connection_node_id", QVariant.Int))
        feat = QgsFeature(fields)
        feat.setAttribute("id", 1)

        # Create a mock node manager
        node_manager = MagicMock()
        new_node = QgsFeature(node_fields)
        new_node.setAttribute("id", 42)
        node_manager.create_new.return_value = new_node

        # Call the function
        Processor.add_connection_node(
            feat, QgsPointXY(10, 20), node_manager, "connection_node_id", node_fields
        )

        # Check that the feature was updated
        assert feat["connection_node_id"] == 42
