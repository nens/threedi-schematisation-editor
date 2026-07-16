from unittest.mock import MagicMock, patch

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsSpatialIndex,
)

from threedi_schematisation_editor.vector_data_importer import settings_models as sm
from threedi_schematisation_editor.vector_data_importer.integrators import (
    ChannelIntegrator,
    LinearIntegrator,
    LinearIntegratorStructureData,
)
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning


@pytest.fixture
def channel_fields():
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    return fields


@pytest.fixture
def structure_fields():
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("length", QVariant.Double))
    return fields


@pytest.fixture
def channel_feature(channel_fields):
    """Create a simple channel feature with a straight line geometry."""
    feature = QgsFeature(channel_fields)
    feature.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
    )
    feature.setAttribute("id", 1)
    return feature


@pytest.fixture
def line_structure_feature_no_intersection(structure_fields):
    """Create a line structure feature perpendicular to the channel."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(50, -10), QgsPointXY(50, 10)])
    )
    feature.setAttribute("id", 2)
    return feature


@pytest.fixture
def line_structure_feature(structure_fields):
    """Create a line structure feature that intersects the channel at both ends."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(25, 0), QgsPointXY(75, 0)])
    )
    feature.setAttribute("id", 3)
    return feature


@pytest.fixture
def point_structure_feature(structure_fields):
    """Create a point structure feature near the channel."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 1)))
    feature.setAttribute("id", 4)
    feature.setAttribute("length", 10.0)
    return feature


@pytest.fixture
def point_structure_feature_far(structure_fields):
    """Create a point structure feature far from the channel."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 20)))
    feature.setAttribute("id", 5)
    feature.setAttribute("length", 10.0)
    return feature


@pytest.fixture
def cross_section_fields():
    """Create fields for cross section features."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("channel_id", QVariant.Int))
    return fields


@pytest.fixture
def cross_section_feature_near(cross_section_fields):
    """Create a cross section feature near the channel."""
    feature = QgsFeature(cross_section_fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(25, 1)))
    feature.setAttribute("id", 10)
    feature.setAttribute("channel_id", 1)
    return feature


@pytest.fixture
def cross_section_feature_middle(cross_section_fields):
    """Create a cross section feature in the middle of the channel."""
    feature = QgsFeature(cross_section_fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 0)))
    feature.setAttribute("id", 11)
    feature.setAttribute("channel_id", 1)
    return feature


@pytest.fixture
def cross_section_feature_far(cross_section_fields):
    """Create a cross section feature far from the channel."""
    feature = QgsFeature(cross_section_fields)
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(75, 10)))
    feature.setAttribute("id", 12)
    feature.setAttribute("channel_id", 1)
    return feature


@pytest.fixture
def cross_section_feature_same_distance(cross_section_fields):
    """Create a cross section feature with the same distance to the channel as the middle feature."""
    feature = QgsFeature(cross_section_fields)
    # Same distance to the channel as the middle feature (50, 0), but at a different position
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 0)))
    feature.setAttribute("id", 13)
    feature.setAttribute("channel_id", 1)
    return feature


@pytest.fixture
def cross_section_features_map(
    cross_section_feature_near,
    cross_section_feature_middle,
    cross_section_feature_far,
    cross_section_feature_same_distance,
):
    """Create a map of cross section features."""
    return {
        10: cross_section_feature_near,
        11: cross_section_feature_middle,
        12: cross_section_feature_far,
        13: cross_section_feature_same_distance,
    }


class TestChannelStructureIntegration:
    """Tests for channel structure integration methods of the LinearIntegrator class."""

    def test_get_conduit_matches(self, channel_fields, structure_fields):
        """get_conduit_matches correctly handles single-match, multi-match and no-match structures.

        Setup (snapping_distance=2):
        - conduit A at y=0, conduit B at y=1, conduit C at y=200
        - structure_multi at y=0.5: 0.5m from A and 0.5m from B -> snaps both -> excluded, warning
        - structure_single at y=-1.5: 1.5m from A, 2.5m from B -> snaps A only -> returned for A
        - structure_none at y=100: far from all -> absent from result
        """
        snapping_distance = 2.0

        conduit_a = QgsFeature(channel_fields)
        conduit_a.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
        )
        conduit_a.setAttribute("id", 10)

        conduit_b = QgsFeature(channel_fields)
        conduit_b.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 1), QgsPointXY(100, 1)])
        )
        conduit_b.setAttribute("id", 20)

        conduit_c = QgsFeature(channel_fields)
        conduit_c.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 200), QgsPointXY(100, 200)])
        )
        conduit_c.setAttribute("id", 30)

        structure_multi = QgsFeature(structure_fields)
        structure_multi.setId(1)
        structure_multi.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 0.5)))
        structure_multi.setAttribute("id", 1)
        structure_multi.setAttribute("length", 5.0)

        structure_single = QgsFeature(structure_fields)
        structure_single.setId(2)
        structure_single.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, -1.5)))
        structure_single.setAttribute("id", 2)
        structure_single.setAttribute("length", 5.0)

        structure_none = QgsFeature(structure_fields)
        structure_none.setId(3)
        structure_none.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 100)))
        structure_none.setAttribute("id", 3)
        structure_none.setAttribute("length", 5.0)

        index = QgsSpatialIndex()
        structure_features_map = {}
        for s in [structure_multi, structure_single, structure_none]:
            index.addFeature(s)
            structure_features_map[s.id()] = s

        integrator = MagicMock()
        integrator.snapping_distance = snapping_distance
        integrator.point_to_line_settings = sm.PointToLineSettings(
            length={
                "method": "source_attribute",
                "source_attribute": "length",
                "default_value": 5.0,
            },
            azimuth={"method": "default", "default_value": 0.0},
        )
        integrator.spatial_indexes_map = {"source": (structure_features_map, index)}
        integrator.integrate_layer.getFeatures.return_value = [
            conduit_a,
            conduit_b,
            conduit_c,
        ]

        with pytest.warns(StructuresIntegratorWarning):
            result = LinearIntegrator.get_conduit_matches(integrator)

        # Only conduit_a should appear in result (conduit_b lost its only structure
        # to multi-match exclusion; conduit_c had no matches at all)
        assert len(result) == 1
        matched_conduit, matched_structures = result[0]
        assert matched_conduit["id"] == conduit_a["id"]
        # structure_single is matched; structure_multi is excluded; structure_none is absent
        assert structure_single in matched_structures
        assert structure_multi not in matched_structures
        assert structure_none not in matched_structures

    def test_get_conduit_matches_selected_ids(self, channel_fields, structure_fields):
        """Structure outside selected_ids is not counted as a match."""
        fields_c = QgsFields()
        fields_c.append(QgsField("id", QVariant.Int))
        conduit = QgsFeature(fields_c)
        conduit.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
        )
        conduit.setAttribute("id", 10)

        structure = QgsFeature(structure_fields)
        structure.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 1)))
        structure.setAttribute("id", 99)
        structure.setAttribute("length", 5.0)
        structure_fid = structure.id()

        integrator = MagicMock()
        integrator.snapping_distance = 5.0
        integrator.point_to_line_settings = sm.PointToLineSettings(
            length={
                "method": "source_attribute",
                "source_attribute": "length",
                "default_value": 5.0,
            },
            azimuth={"method": "default", "default_value": 0.0},
        )
        structure_index = MagicMock()
        structure_index.intersects.return_value = [structure_fid]
        integrator.spatial_indexes_map = {
            "source": ({structure_fid: structure}, structure_index)
        }
        integrator.integrate_layer.getFeatures.return_value = [conduit]

        result = LinearIntegrator.get_conduit_matches(integrator, selected_ids={999})

        assert result == []

    def test_get_conduit_matches_structure_outside_raw_bbox_within_snapping_distance(
        self, channel_fields, structure_fields
    ):
        """Structure outside conduit raw bounding box but within snapping distance is matched.

        A horizontal conduit at y=0 has a degenerate bounding box (zero height).
        A structure at y=8 is outside that raw bbox but within snapping_distance=10,
        so it should still be found and returned as a match.
        """
        conduit = QgsFeature(channel_fields)
        conduit.setGeometry(
            QgsGeometry.fromPolylineXY([QgsPointXY(0, 0), QgsPointXY(100, 0)])
        )
        conduit.setAttribute("id", 10)

        structure = QgsFeature(structure_fields)
        structure.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(50, 8)))
        structure.setAttribute("id", 99)
        structure.setAttribute("length", 5.0)
        structure_fid = structure.id()

        # Use a real spatial index so the bounding box query is exercised.
        index = QgsSpatialIndex()
        index.addFeature(structure)
        structure_features_map = {structure_fid: structure}

        integrator = MagicMock()
        integrator.snapping_distance = 10.0
        integrator.point_to_line_settings = sm.PointToLineSettings(
            length={
                "method": "source_attribute",
                "source_attribute": "length",
                "default_value": 5.0,
            },
            azimuth={"method": "default", "default_value": 0.0},
        )
        integrator.spatial_indexes_map = {"source": (structure_features_map, index)}
        integrator.integrate_layer.getFeatures.return_value = [conduit]

        result = LinearIntegrator.get_conduit_matches(integrator)

        assert len(result) == 1
        matched_conduit, matched_structures = result[0]
        assert matched_conduit.id() == conduit.id()
        assert structure in matched_structures

    def test_get_conduit_structure_from_point(
        self, channel_feature, point_structure_feature
    ):
        """get_conduit_structure_from_point takes no snapping_distance, returns data."""
        length_config = sm.FieldMapConfig(
            method=sm.ColumnImportMethod.ATTRIBUTE,
            source_attribute="length",
            default_value=5.0,
        )
        result = LinearIntegrator.get_conduit_structure_from_point(
            point_structure_feature, channel_feature, length_config
        )
        assert result.conduit_id == 1
        assert result.feature["id"] == 4
        assert result.m == 50.0
        assert result.length == 10.0

    def test_get_conduit_structure_from_line(
        self, channel_feature, line_structure_feature
    ):
        """get_conduit_structure_from_line takes no snapping_distance, returns data."""
        result = LinearIntegrator.get_conduit_structure_from_line(
            line_structure_feature, channel_feature
        )
        assert result.conduit_id == 1
        assert result.feature["id"] == 3
        assert result.m == 50.0
        assert result.length == 50.0


class TestCrossSectionIntegration:
    """Tests for cross section integration methods of the LinearIntegrator class."""

    @pytest.mark.parametrize(
        "cross_section_fids, expected_result", [([10, 11, 12], [10, 11]), ([12], [])]
    )
    def test_get_cross_sections_for_channel(
        self,
        cross_section_fids,
        expected_result,
        channel_feature,
        cross_section_features_map,
    ):
        """Test get_cross_sections_for_channel with features that intersect and don't intersect."""
        # The near and middle cross sections should intersect, but the far one shouldn't
        result = ChannelIntegrator.get_cross_sections_for_channel(
            channel_feature, cross_section_fids, cross_section_features_map
        )
        assert expected_result == result

    @pytest.mark.parametrize(
        "features, expected_id",
        [
            (
                ["cross_section_feature_near", "cross_section_feature_middle"],
                11,  # Middle feature is closest to the channel
            ),
            (
                ["cross_section_feature_near"],
                10,  # Only one feature, so it's the closest
            ),
            (
                [
                    "cross_section_feature_near",
                    "cross_section_feature_middle",
                    "cross_section_feature_far",
                ],
                11,  # Middle feature is closest to the channel
            ),
            (
                ["cross_section_feature_middle", "cross_section_feature_same_distance"],
                11,  # Both features have the same distance, but the first one in the list is returned
            ),
            (
                [],
                None,  # No source IDs, should return None
            ),
        ],
        ids=[
            "multiple_features",
            "single_feature",
            "all_features",
            "same_distance_features",
            "empty_source_ids",
        ],
    )
    @patch(
        "threedi_schematisation_editor.vector_data_importer.integrators.get_features_by_expression"
    )
    def test_get_closest_cross_section_location(
        self, mock_get_features, channel_feature, features, expected_id, request
    ):
        """Test get_closest_cross_section_location with different scenarios."""
        # Mock the get_features_by_expression function to return our test features
        if features:
            mock_get_features.return_value = [
                request.getfixturevalue(fixture_name) for fixture_name in features
            ]
        else:
            mock_get_features.return_value = []
        source_ids = [feature.id() for feature in mock_get_features.return_value]
        # Create a mock cross section layer
        mock_cross_section_layer = MagicMock()
        # Call the method with source channel cross section locations
        result = ChannelIntegrator.get_closest_cross_section_location(
            channel_feature, mock_cross_section_layer, source_ids
        )
        if expected_id is None:
            assert result is None
        else:
            assert result["id"] == expected_id

    @pytest.mark.parametrize(
        "cross_section_feature, expected_result",
        [
            ("cross_section_feature_near", True),  # Intersects with channel
            ("cross_section_feature_far", False),  # Doesn't intersect with any channel
        ],
        ids=["intersects", "no_intersect"],
    )
    def test_is_hanging_cross_section(
        self, channel_feature, cross_section_feature, expected_result, request
    ):
        """Test is_hanging_cross_section with different cross-section features."""
        # Get the actual fixture from the parameter name
        cross_section_feature = request.getfixturevalue(cross_section_feature)
        result = ChannelIntegrator.is_hanging_cross_section(
            cross_section_feature, {1: channel_feature}, [1]
        )
        assert result is expected_result

    @patch(
        "threedi_schematisation_editor.vector_data_importer.integrators.spatial_index"
    )
    def test_get_hanging_cross_sections(self, mock_spatial_index, channel_feature):
        """Test get_hanging_cross_sections collects IDs correctly.

        Note: The core functionality of determining if a cross-section is hanging
        is already tested in test_is_hanging_cross_section_* methods.
        """
        # Create a mock LinearIntegrator instance
        integrator = MagicMock()

        # Create a mock cross-section feature
        mock_feature = MagicMock()
        mock_feature.id.return_value = 10

        # Set up the mock cross_section_layer to return our mock feature
        mock_cross_section_layer = MagicMock()
        mock_cross_section_layer.getFeatures.return_value = [mock_feature]
        integrator.cross_section_layer = mock_cross_section_layer

        # Set up the mock integrate_layer
        integrator.integrate_layer = MagicMock()

        # Set up the mock spatial_index to return our channel feature and a spatial index
        channel_feats = {1: channel_feature}
        channels_spatial_index = MagicMock()
        channels_spatial_index.intersects.return_value = [1]
        mock_spatial_index.return_value = (channel_feats, channels_spatial_index)

        # Mock is_hanging_cross_section to return True
        with patch.object(
            ChannelIntegrator, "is_hanging_cross_section", return_value=True
        ):
            # Call the method with a list of visited channel IDs
            result = ChannelIntegrator.get_hanging_cross_sections(integrator, [1])

        # The method should return a list containing the ID of the hanging cross-section
        assert result == [10]


def test_substring_feature(channel_feature):
    """Test that substring_feature correctly creates a new feature with the provided fields and attributes."""
    curve = channel_feature.geometry().constGet()
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    attributes = {"id": 42}
    result = LinearIntegrator.substring_feature(
        curve, 25, 75, fields, False, **attributes
    )
    assert result["id"] == 42


class TestNodeManagement:
    """Tests for node management methods of the LinearIntegrator class."""

    def test_add_node(self, structure_fields):
        """Test add_node creates a new node with the correct attributes."""
        # Create a LinearIntegrator instance with minimal attributes
        integrator = MagicMock()
        integrator.node_by_location = {}

        # Create a real FeatureManager for the node_manager
        from threedi_schematisation_editor.vector_data_importer.utils import (
            FeatureManager,
        )

        integrator.node_manager = FeatureManager(42)  # Start with ID 42

        # Create a point, node_layer_fields, and node_attributes
        point = QgsPointXY(10, 20)
        node_layer_fields = structure_fields
        node_attributes = {"length": 4.0}

        # Call the add_node method
        result = LinearIntegrator.add_node(
            integrator, point, node_layer_fields, node_attributes
        )

        # Assert that the result is a QgsFeature
        assert isinstance(result, QgsFeature)

        # Assert that the feature has the correct geometry
        assert result.geometry().asPoint() == point

        # Assert that the feature has the correct ID
        assert result["id"] == 42

        # Assert that the feature has the correct attributes
        for field_name, field_value in node_attributes.items():
            assert result[field_name] == field_value

        # Assert that the node_by_location dictionary was updated correctly
        assert integrator.node_by_location[point] == 42

    @pytest.mark.parametrize("initial_nodes", [["start"], [], ["start", "end"]])
    def test_update_feature_endpoints(self, initial_nodes):
        """Test update_feature_endpoints: connection_node_id fields are unset →
        nodes are created/found spatially via node_by_location."""
        integrator = MagicMock(spec=LinearIntegrator)

        points = {"start": (QgsPointXY(0, 0), 101), "end": (QgsPointXY(100, 0), 102)}
        start_point = QgsPointXY(0, 0)
        end_point = QgsPointXY(100, 0)
        integrator.node_by_location = {
            points[name][0]: points[name][1] for name in initial_nodes
        }

        node_layer_fields = QgsFields()
        node_layer_fields.append(QgsField("id", QVariant.Int))
        node_layer_fields.append(QgsField("name", QVariant.String))

        mock_node_layer = MagicMock()
        mock_node_layer.name.return_value = "connection_nodes"
        integrator.node_layer = mock_node_layer
        integrator.layer_fields_mapping = {"connection_nodes": node_layer_fields}

        features_to_add = []
        for name, (pt, node_id) in points.items():
            mock_node_feature = QgsFeature(node_layer_fields)
            mock_node_feature.setGeometry(QgsGeometry.fromPointXY(pt))
            mock_node_feature["id"] = node_id
            if name not in initial_nodes:
                features_to_add.append(mock_node_feature)
        mock_features = features_to_add.copy()

        def mock_add_node(point, fields, attributes):
            feature = mock_features.pop(0)
            integrator.node_by_location[point] = feature["id"]
            return feature

        integrator.add_node.side_effect = mock_add_node

        dst_fields = QgsFields()
        dst_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        dst_fields.append(QgsField("connection_node_id_end", QVariant.Int))
        dst_feature = QgsFeature(dst_fields)
        dst_feature.setGeometry(QgsGeometry.fromPolylineXY([start_point, end_point]))

        result = LinearIntegrator.update_feature_endpoints(
            integrator, dst_feature, {"name": "Test Node"}
        )
        assert result == features_to_add
        assert integrator.node_by_location[start_point] == 101
        assert integrator.node_by_location[end_point] == 102

    def test_update_feature_endpoints_with_attribute_mapped_node_ids(self):
        """Test update_feature_endpoints with overwrite_node_ids=True:
        connection_node_id fields are pre-set → look up node by ID, snap geometry,
        add_node is never called."""
        from qgis.core import QgsVectorLayer

        integrator = MagicMock(spec=LinearIntegrator)

        start_point = QgsPointXY(0, 0)
        end_point = QgsPointXY(100, 0)

        node_layer = QgsVectorLayer("Point?crs=EPSG:4326", "connection_nodes", "memory")
        node_layer.dataProvider().addAttributes(
            [QgsField("id", QVariant.Int), QgsField("name", QVariant.String)]
        )
        node_layer.updateFields()
        for node_id, pt in [(101, start_point), (102, end_point)]:
            feat = QgsFeature(node_layer.fields())
            feat.setGeometry(QgsGeometry.fromPointXY(pt))
            feat.setAttribute("id", node_id)
            node_layer.dataProvider().addFeatures([feat])

        node_layer_fields = node_layer.fields()
        integrator.node_layer = node_layer
        integrator.node_by_location = {}
        integrator.layer_fields_mapping = {"connection_nodes": node_layer_fields}

        dst_fields = QgsFields()
        dst_fields.append(QgsField("connection_node_id_start", QVariant.Int))
        dst_fields.append(QgsField("connection_node_id_end", QVariant.Int))
        dst_feature = QgsFeature(dst_fields)
        dst_feature.setGeometry(QgsGeometry.fromPolylineXY([start_point, end_point]))
        dst_feature["connection_node_id_start"] = 101
        dst_feature["connection_node_id_end"] = 102

        result = LinearIntegrator.update_feature_endpoints(
            integrator, dst_feature, {}, overwrite_node_ids=True
        )

        assert result == []
        integrator.add_node.assert_not_called()
        assert dst_feature["connection_node_id_start"] == 101
        assert dst_feature["connection_node_id_end"] == 102
        polyline = dst_feature.geometry().asPolyline()
        assert polyline[0] == start_point
        assert polyline[-1] == end_point


@pytest.mark.parametrize("simplify", [True, False])
def test_get_substring_geometry_argument_processing(simplify):
    """Test that get_substring_geometry processes the simplify argument correctly."""
    # Create a simple line geometry for testing
    line_geom = QgsGeometry.fromPolylineXY(
        [QgsPointXY(0, 0), QgsPointXY(50, 0), QgsPointXY(100, 0)]
    )

    # Get the underlying curve object
    curve = line_geom.constGet()

    # Test parameters
    start_distance = 25.0
    end_distance = 75.0

    # Call the function with simplify=False
    result = LinearIntegrator.get_substring_geometry(
        curve, start_distance, end_distance, simplify=simplify
    )

    # Verify that both calls return a QgsGeometry object
    assert isinstance(result, QgsGeometry)

    if simplify:
        assert len(result.asPolyline()) == 2
    else:
        assert len(result.asPolyline()) >= 2

    assert result.length() == end_distance - start_distance


class TestFixPositions:
    @pytest.mark.parametrize(
        "mids, expected_mids",
        [
            ([2], [3]),  # single structure too far to the left
            ([4], [3]),  # single structure leaving too short channel on the left
            ([3], [3]),  # single structure exactly at the start
            ([6], [6]),  # single structure far enough from the start
            ([12, 19], [12, 18]),  # two structures with channel of length 1 in between
            ([12, 17], [12, 18]),  # two overlapping structures
            ([12, 20], [12, 20]),  # two structures with sufficient distance
            ([12, 18], [12, 18]),  # two structures side by side
        ],
    )
    def test_fix_positions_lhs(self, mids, expected_mids):
        minimum_channel_length = 2
        structure_length = 6
        channel_length = 30
        channel_structures = [
            LinearIntegratorStructureData(0, None, mid, structure_length)
            for mid in mids
        ]
        channel_structures_mod = LinearIntegrator.fix_structure_placement_lhs(
            channel_structures, channel_length, minimum_channel_length
        )
        assert expected_mids == [cs.m for cs in channel_structures_mod]

    @pytest.mark.parametrize(
        "mids, expected_mids, expected_lengths",
        [
            ([19], [17], [6]),  # single structure too far to the right
            ([16], [17], [6]),  # single structure with too short channel on the right
            ([17], [17], [6]),  # single structure exactly at the end
            ([10], [10], [6]),  # single structure with enough space at the end
            (
                [15, 19],
                [15, 19],
                [6, 2],
            ),  # second structure past channel and no space to more
            ([15, 17], [15, 19], [6, 2]),  # overlap with no space to move
            (
                [10, 16],
                [10, 16.5],
                [6, 7],
            ),  # too small gap between last and one before last
            ([11, 17], [11, 17], [6, 6]),  # two structures exactly at the end
        ],
    )
    def test_fix_positions_rhs(self, mids, expected_mids, expected_lengths):
        minimum_channel_length = 2
        structure_length = 6
        channel_length = 20
        channel_structures = [
            LinearIntegratorStructureData(0, None, mid, structure_length)
            for mid in mids
        ]
        channel_structures_mod = LinearIntegrator.fix_structure_placement_rhs(
            channel_structures, channel_length, minimum_channel_length
        )
        assert expected_mids == [cs.m for cs in channel_structures_mod]
        assert expected_lengths == [cs.length for cs in channel_structures_mod]

    @pytest.mark.parametrize(
        "mids, lengths, expected_mids, expected_lengths",
        [
            (
                [15, 17],
                [10, 6],
                [12, 17],
                [4, 6],
            ),  # two structures that both end at the channel end
            (
                [15, 17, 18],
                [10, 6, 4],
                [12, 15, 18],
                [4, 2, 4],
            ),  # three structures that both end at the channel end
            (
                [17, 17],
                [6, 6],
                [17, 17],
                [6, 6],
            ),  # two identical structures, should not be moved
        ],
    )
    def test_fix_positions_overlap_at_end(
        self, mids, lengths, expected_mids, expected_lengths
    ):
        channel_length = 20
        channel_structures = [
            LinearIntegratorStructureData(0, None, mid, length)
            for (mid, length) in zip(mids, lengths)
        ]
        channel_structures_mod = (
            LinearIntegrator.fix_structure_placement_overlap_at_end(
                channel_structures, channel_length
            )
        )
        assert expected_mids == [cs.m for cs in channel_structures_mod]
        assert expected_lengths == [cs.length for cs in channel_structures_mod]


@pytest.mark.parametrize(
    "mids, lengths, expected_cuts",
    [
        ([5], [10], [(10, 50)]),  # structure on the left
        ([45], [10], [(0, 40)]),  # structure on the right
        (
            [10, 30],
            [10, 10],
            [(0, 5), (15, 25), (35, 50)],
        ),  # two strcutures on the channel
    ],
)
def test_get_channel_cuts(mids, lengths, expected_cuts):
    channel_length = 50
    channel_structures = [
        LinearIntegratorStructureData(0, None, mid, length)
        for (mid, length) in zip(mids, lengths)
    ]
    assert (
        LinearIntegrator.get_conduit_cuts(channel_structures, channel_length)
        == expected_cuts
    )
