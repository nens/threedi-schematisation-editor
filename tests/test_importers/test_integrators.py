import pytest
from unittest.mock import MagicMock, patch
from qgis.core import QgsFeature, QgsGeometry, QgsWkbTypes, QgsPointXY, QgsFields, QgsField
from PyQt5.QtCore import QVariant

from threedi_schematisation_editor.custom_tools.integrators import LinearIntegrator
from threedi_schematisation_editor.custom_tools.utils import DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS


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
    feature.setGeometry(QgsGeometry.fromPolylineXY([
        QgsPointXY(0, 0),
        QgsPointXY(100, 0)
    ]))
    feature.setAttribute("id", 1)
    return feature


@pytest.fixture
def line_structure_feature(structure_fields):
    """Create a line structure feature perpendicular to the channel."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(QgsGeometry.fromPolylineXY([
        QgsPointXY(50, -10),
        QgsPointXY(50, 10)
    ]))
    feature.setAttribute("id", 2)
    return feature


@pytest.fixture
def line_structure_feature_both_ends_intersect(structure_fields):
    """Create a line structure feature that intersects the channel at both ends."""
    feature = QgsFeature(structure_fields)
    feature.setGeometry(QgsGeometry.fromPolylineXY([
        QgsPointXY(25, 0),
        QgsPointXY(75, 0)
    ]))
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
def cross_section_features_map(cross_section_feature_near, cross_section_feature_middle, cross_section_feature_far):
    """Create a map of cross section features."""
    return {
        10: cross_section_feature_near,
        11: cross_section_feature_middle,
        12: cross_section_feature_far
    }


class TestLinearIntegrator:
    """Tests for the LinearIntegrator class."""

    def test_get_channel_structure_from_line(self, channel_feature, line_structure_feature):
        """Test get_channel_structure_from_line with a line that intersects the channel."""
        snapping_distance = 5.0
        result = LinearIntegrator.get_channel_structure_from_line(
            line_structure_feature, channel_feature, snapping_distance
        )

        # Check that the result is not None
        assert result is not None

        # Check that the result has the expected attributes
        assert result.channel_id == 1
        assert result.feature["id"] == 2
        assert result.m == 50.0  # The line is at x=50, so the intersection is at 50% of the channel
        assert result.length == 20.0  # The line is 20 units long

    def test_get_channel_structure_from_line_both_ends_intersect(self, channel_feature, line_structure_feature_both_ends_intersect):
        """Test get_channel_structure_from_line with a line that intersects the channel at both ends."""
        snapping_distance = 5.0
        result = LinearIntegrator.get_channel_structure_from_line(
            line_structure_feature_both_ends_intersect, channel_feature, snapping_distance
        )

        # The method should return None if both ends of the line intersect the channel
        assert result is None

    def test_get_channel_structure_from_point(self, channel_feature, point_structure_feature):
        """Test get_channel_structure_from_point with a point near the channel."""
        snapping_distance = 5.0
        length_source_field = "length"
        length_fallback_value = 5.0

        result = LinearIntegrator.get_channel_structure_from_point(
            point_structure_feature, channel_feature, snapping_distance,
            length_source_field, length_fallback_value
        )

        # Check that the result is not None
        assert result is not None

        # Check that the result has the expected attributes
        assert result.channel_id == 1
        assert result.feature["id"] == 4
        assert result.m == 50.0  # The point is at x=50, so the intersection is at 50% of the channel
        assert result.length == 10.0  # The length from the feature attribute

    def test_get_channel_structure_from_point_with_fallback(self, channel_feature, point_structure_feature):
        """Test get_channel_structure_from_point with a fallback length value."""
        snapping_distance = 5.0
        length_source_field = None  # No source field, use fallback
        length_fallback_value = 5.0

        result = LinearIntegrator.get_channel_structure_from_point(
            point_structure_feature, channel_feature, snapping_distance,
            length_source_field, length_fallback_value
        )

        # Check that the result is not None
        assert result is not None

        # Check that the result has the expected attributes
        assert result.channel_id == 1
        assert result.feature["id"] == 4
        assert result.m == 50.0
        assert result.length == 5.0  # The fallback length value

    def test_get_channel_structure_from_point_too_far(self, channel_feature, point_structure_feature_far):
        """Test get_channel_structure_from_point with a point too far from the channel."""
        snapping_distance = 5.0
        length_source_field = "length"
        length_fallback_value = 5.0

        result = LinearIntegrator.get_channel_structure_from_point(
            point_structure_feature_far, channel_feature, snapping_distance,
            length_source_field, length_fallback_value
        )

        # The method should return None if the point is too far from the channel
        assert result is None

    def test_get_cross_sections_for_channel(self, channel_feature, cross_section_features_map):
        """Test get_cross_sections_for_channel with features that intersect and don't intersect."""
        # The near and middle cross sections should intersect, but the far one shouldn't
        cross_section_fids = [10, 11, 12]

        result = LinearIntegrator.get_cross_sections_for_channel(
            channel_feature, cross_section_fids, cross_section_features_map
        )

        # Check that the result contains the expected cross section IDs
        assert 10 in result  # Near cross section should intersect
        assert 11 in result  # Middle cross section should intersect
        assert 12 not in result  # Far cross section should not intersect

    def test_get_cross_sections_for_channel_none_intersect(self, channel_feature, cross_section_features_map):
        """Test get_cross_sections_for_channel with features that don't intersect."""
        # Only include the far cross section
        cross_section_fids = [12]

        result = LinearIntegrator.get_cross_sections_for_channel(
            channel_feature, cross_section_fids, cross_section_features_map
        )

        # Check that the result is empty
        assert len(result) == 0

    @patch('threedi_schematisation_editor.custom_tools.integrators.get_features_by_expression')
    def test_get_closest_cross_section_location(self, mock_get_features, channel_feature, 
                                               cross_section_feature_near, cross_section_feature_middle):
        """Test get_closest_cross_section_location with features at different distances."""
        # Mock the get_features_by_expression function to return our test features
        mock_get_features.return_value = [cross_section_feature_near, cross_section_feature_middle]

        # Create a mock cross section layer
        mock_cross_section_layer = MagicMock()

        # Call the method with source channel cross section locations
        result = LinearIntegrator.get_closest_cross_section_location(
            channel_feature, mock_cross_section_layer, [10, 11]
        )

        # Check that the result is not None
        assert result is not None

        # Check that the result is a copy of the middle cross section (which is closest to the channel)
        assert result["id"] == 11

    @patch('threedi_schematisation_editor.custom_tools.integrators.get_features_by_expression')
    def test_get_closest_cross_section_location_empty(self, mock_get_features, channel_feature):
        """Test get_closest_cross_section_location with no source channel cross section locations."""
        # Create a mock cross section layer
        mock_cross_section_layer = MagicMock()

        # Call the method with no source channel cross section locations
        result = LinearIntegrator.get_closest_cross_section_location(
            channel_feature, mock_cross_section_layer, []
        )

        # Check that the result is None
        assert result is None

        # Verify that get_features_by_expression was not called
        mock_get_features.assert_not_called()
