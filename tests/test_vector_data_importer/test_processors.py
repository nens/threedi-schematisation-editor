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

import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.processors import (
    ConnectionNodeProcessor,
    LineProcessor,
    PointProcessor,
    SpatialProcessor,
    StructureProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    get_src_geometry,
)


@pytest.fixture
def target_fields():
    """Create fields for target features."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("connection_node_id", QVariant.Int))
    fields.append(QgsField("connection_node_id_start", QVariant.Int))
    fields.append(QgsField("connection_node_id_end", QVariant.Int))
    return fields


@pytest.fixture
def node_fields():
    """Create fields for node features."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    return fields


@pytest.fixture(scope="function")
def source_feature():
    """Create a source feature with point geometry."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    feature = QgsFeature(fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 20)))
    feature.setAttribute("id", 1)
    return feature


@pytest.fixture(scope="function")
def source_line_feature():
    """Create a source feature with line geometry."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("length", QVariant.Double))
    fields.append(QgsField("connection_node_id_start", QVariant.Int))
    fields.append(QgsField("connection_node_id_end", QVariant.Int))
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
        processor = ConnectionNodeProcessor(
            target_layer,
            dm.ConnectionNode,
            import_settings=sm.ConversionSettingsModel(),
        )

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
        import_settings = sm.ConversionSettingsModel(
            fields={"id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO)},
            connection_node_fields={
                "id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO)
            },
        )

        # Create a processor
        processor = PointProcessor(target_layer, dm.Pump, node_layer, import_settings)

        # Mock the add_node method to return a new node feature
        new_node = QgsFeature(node_fields)
        new_node.setAttribute("id", 42)
        new_node.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(11, 21)))
        processor.get_node = MagicMock(return_value=(new_node, True))

        result = processor.process_feature(source_feature)

        # Check that the result is a dictionary with the expected keys
        assert sorted(result.keys()) == ["pumps"]
        assert len(result["pumps"]) == 1
        new_pump = result["pumps"][0]
        assert new_pump["connection_node_id"] == 42
        assert new_pump.geometry().asPoint() == QgsPointXY(11, 21)


class TestStructureProcessor:
    """Tests for the StructureProcessor class."""

    @pytest.mark.parametrize(
        "use_snapping, create_connection_nodes, snap_result, should_return_node",
        [
            (True, True, True, True),
            (True, False, True, True),
            (True, True, False, True),
            (True, False, False, False),
            (False, True, False, True),
            (False, False, False, False),
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
        should_return_node,
        node_fields,
    ):
        """Test add_node with different configurations."""
        # Create a mock StructureProcessor instance
        processor = MagicMock()
        processor.node_manager = MagicMock()
        processor.locator = MagicMock()
        processor.connection_nodes_settings = MagicMock()
        processor.connection_nodes_settings = sm.ConnectionNodeSettingsModel(
            snap=use_snapping,
            create_nodes=create_connection_nodes,
            snap_distance=10.0,
        )
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
            "threedi_schematisation_editor.vector_data_importer.processors.find_connection_node",
            return_value=new_node if snap_result else None,
        ) as mock_find:
            node, snapped = StructureProcessor.get_node(processor, point)
            assert (node is None) == (not should_return_node)


class TestLineProcessor:
    """Tests for the LineProcessor class."""

    @pytest.fixture
    def import_settings(self):
        return sm.ConversionSettingsModel(
            fields={"id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO)},
            connection_node_fields={
                "id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO)
            },
        )

    def test_update_connection_nodes(
        self, source_line_feature, target_fields, node_fields, import_settings
    ):
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "pipes"
        node_layer = MagicMock()
        node_layer.fields.return_value = node_fields
        node_layer.name.return_value = "connection_nodes"
        processor = LineProcessor(target_layer, dm.Pipe, node_layer, import_settings)
        # Mock the get_node method to return new node features
        start_node = QgsFeature(node_fields)
        start_node.setAttribute("id", 42)
        start_node.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(11, 21)))
        end_node = QgsFeature(node_fields)
        end_node.setAttribute("id", 43)
        end_node.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(30, 40)))
        processor.get_node = MagicMock(
            side_effect=[(start_node, True), (end_node, False)]
        )
        # Run update_connection_nodes and check results
        new_nodes = processor.update_connection_nodes(source_line_feature)
        assert source_line_feature["connection_node_id_start"] == 42
        assert source_line_feature["connection_node_id_end"] == 43
        assert source_line_feature.geometry().asPolyline() == [
            QgsPointXY(11, 21),
            QgsPointXY(30, 40),
        ]
        assert new_nodes[0] == end_node

    def test_process_feature(
        self, source_line_feature, target_fields, node_fields, import_settings
    ):
        target_layer = MagicMock()
        target_layer.fields.return_value = target_fields
        target_layer.name.return_value = "pipes"
        node_layer = MagicMock()
        node_layer.fields.return_value = node_fields
        node_layer.name.return_value = "connection_nodes"
        processor = LineProcessor(target_layer, dm.Pipe, node_layer, import_settings)
        processor.update_connection_nodes = MagicMock(return_value=[])
        # Run process_feature and check results
        result = processor.process_feature(source_line_feature)
        assert sorted(result.keys()) == ["pipes"]
        assert len(result["pipes"]) == 1

    @pytest.fixture
    def point_to_line_conversion_settings(self):
        return sm.PointToLineSettingsModel(
            length=sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE,
                source_attribute="length",
                default_value=20,
            ),
            azimuth=sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE,
                source_attribute="azimuth",
                default_value=0,
            ),
        )

    @pytest.mark.parametrize(
        "line",
        [
            [[QgsPointXY(10, 20), QgsPointXY(10, 40)]],
            [
                [QgsPointXY(10, 20), QgsPointXY(10, 40)],
                [QgsPointXY(100, 20), QgsPointXY(100, 40)],
            ],
        ],
    )
    def test_new_geometry_multi_geom_line(
        self, source_feature, line, point_to_line_conversion_settings
    ):
        source_feature.setGeometry(QgsGeometry.fromMultiPolylineXY(line))
        result = LineProcessor.new_geometry(
            source_feature,
            get_src_geometry(source_feature),
            point_to_line_conversion_settings,
            dm.Weir,
        )
        assert not result.isMultipart()
        assert result.asPolyline() == [QgsPointXY(10, 20), QgsPointXY(10, 40)]

    @pytest.mark.parametrize(
        "point", [[QgsPointXY(10, 20), QgsPointXY(100, 40)], [QgsPointXY(10, 20)]]
    )
    def test_new_geometry_multi_geom_point(
        self, source_feature, point_to_line_conversion_settings, point
    ):
        source_feature.setGeometry(QgsGeometry.fromMultiPointXY(point))
        result = LineProcessor.new_geometry(
            source_feature,
            get_src_geometry(source_feature),
            point_to_line_conversion_settings,
            dm.Weir,
        )
        assert not result.isMultipart()
        assert result.asPolyline() == [QgsPointXY(10, 20), QgsPointXY(10, 40)]

    @pytest.mark.parametrize("model_class", [dm.Pipe, dm.Culvert, dm.Channel])
    def test_new_geometry_full_line(
        self, source_feature, point_to_line_conversion_settings, model_class
    ):
        # Set geometry of source_feature
        line = QgsGeometry.fromPolylineXY(
            [QgsPointXY(0, 0), QgsPointXY(5, 5), QgsPointXY(10, 10)]
        )
        source_feature.setGeometry(line)
        # Retrieve geometry
        result = LineProcessor.new_geometry(
            source_feature, line, point_to_line_conversion_settings, model_class
        )
        # Verify that the full line is returned
        assert result.asPolyline() == line.asPolyline()
        assert result.type() == QgsWkbTypes.LineGeometry

    def test_new_geometry_simplified_line(
        self, source_feature, point_to_line_conversion_settings
    ):
        # Set geometry of source_feature
        line = QgsGeometry.fromPolylineXY(
            [QgsPointXY(0, 0), QgsPointXY(5, 5), QgsPointXY(10, 10)]
        )
        source_feature.setGeometry(line)
        # Retrieve geometry
        result = LineProcessor.new_geometry(
            source_feature, line, point_to_line_conversion_settings, dm.Weir
        )
        # Verify that only the start and end point are returned
        assert result.asPolyline() == [line.asPolyline()[0], line.asPolyline()[-1]]
        assert result.type() == QgsWkbTypes.LineGeometry

    @pytest.mark.parametrize(
        "feature_fields, expected_points",
        [
            ({}, [QgsPointXY(10, 20), QgsPointXY(10, 40)]),
            (
                {"length": 20.0, "azimuth": 90.0},
                [QgsPointXY(10, 20), QgsPointXY(30, 20)],
            ),
        ],
    )
    def test_new_geometry_point(
        self, point_to_line_conversion_settings, feature_fields, expected_points
    ):
        # Create feature with point geometry and specified fields
        fields = QgsFields()
        for field_name in feature_fields:
            fields.append(QgsField(field_name, QVariant.Double))
        feature = QgsFeature(fields)
        geom = QgsGeometry.fromPointXY(QgsPointXY(10, 20))
        feature.setGeometry(geom)
        for field_name, field_value in feature_fields.items():
            feature.setAttribute(field_name, field_value)
        # Retrieve geometry and verify results
        result = LineProcessor.new_geometry(
            feature, geom, point_to_line_conversion_settings, dm.Weir
        )
        assert result.type() == QgsWkbTypes.LineGeometry
        assert result.asPolyline() == expected_points


class TestUtilityFunctions:
    """Tests for utility functions in the processors module."""

    def test_create_new_point_geometry(self):
        """Test that create_new_point_geometry returns a point geometry."""
        geom = QgsGeometry.fromPointXY(QgsPointXY(10, 20))
        result = SpatialProcessor.create_new_point_geometry(geom)
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
            result = SpatialProcessor.snap_connection_node(
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
            result = SpatialProcessor.snap_connection_node(
                feat, QgsPointXY(10, 20), 10.0, locator, "connection_node_id"
            )

            # Check that the result is False
            assert result is False
