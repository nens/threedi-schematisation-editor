from enum import Enum, IntEnum
from typing import Optional

import pytest
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsRectangle,
    QgsVectorLayer,
)

from threedi_schematisation_editor.utils import (
    TypeConversionError,
    convert_to_type,
    get_type_for_casting,
    spatial_index,
)


# Define example Enum and IntEnum classes for testing
class TestEnum(Enum):
    OPTION1 = "option1"


class TestIntEnum(IntEnum):
    ONE = 1


@pytest.mark.parametrize("full_type", [str, Optional[str]])
def test_get_type_for_casting(full_type):
    assert get_type_for_casting(full_type) == str


@pytest.mark.parametrize(
    "value,field_type,expected_value",
    [
        # Original test cases
        (1, int, 1),
        (1.0, int, 1),
        (1.1, int, 1),
        (1, float, 1.0),
        (1.0, float, 1.0),
        (1, str, "1"),
        ("1", str, "1"),
        (1, bool, True),
        (True, bool, True),
        (None, Optional[int], None),
        # enum contents are not checked, but values are just casted
        ("option2", TestEnum, "option2"),
        (2, TestIntEnum, 2),
    ],
)
def test_convert_to_type(value, field_type, expected_value):
    assert convert_to_type(value, field_type) == expected_value


# anything can be casted to bool or int, so these are not tested
@pytest.mark.parametrize("field_type,", [int, float, TestIntEnum])
def test_convert_to_type_invalid(field_type):
    with pytest.raises(TypeConversionError):
        convert_to_type("foo", field_type)


@pytest.mark.parametrize("bbox_crs", ["EPSG:4326", "EPSG:28991"])
def test_spatial_index(bbox_crs):
    layer_crs = "EPSG:4326"
    # create layer with two points
    layer = QgsVectorLayer(f"Point?{layer_crs}", "test", "memory")
    layer.startEditing()
    for pt in ([0, 0], [2, 2]):
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pt[0], pt[1])))
        layer.dataProvider().addFeatures([feat])
    layer.commitChanges()
    # create bounding box that covers one of the two points
    bbox = QgsRectangle(-1, -1, 1, 1)
    transform = None
    if bbox_crs != layer_crs:
        # transform bbox to other crs
        transform_ctx = QgsProject.instance().transformContext()
        transform = QgsCoordinateTransform(
            layer.crs(), QgsCoordinateReferenceSystem(bbox_crs), transform_ctx
        )
        bbox = transform.transformBoundingBox(bbox)
    # check for intersections
    features, index = spatial_index(layer, transform=transform)
    intersecting_ids = index.intersects(bbox)
    # assert matches
    assert len(intersecting_ids) == 1
    assert intersecting_ids[0] == 1
