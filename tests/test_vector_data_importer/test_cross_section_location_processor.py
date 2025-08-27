import pytest
import shapely
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsVectorLayer,
)
from shapely.testing import assert_geometries_equal

from threedi_schematisation_editor.vector_data_importer.processors import (
    CrossSectionLocationProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import ConversionSettings


@pytest.fixture(scope="function")
def target_layer():
    target_layer = QgsVectorLayer(
        "Point?crs=EPSG:4326", "cross_section_location", "memory"
    )
    provider = target_layer.dataProvider()
    provider.addAttributes([QgsField("id", QVariant.Int)])
    target_layer.updateFields()
    return target_layer


@pytest.fixture(scope="session")
def import_config():
    return {
        "conversion_settings": {
            "join_field_src": {
                "method": "source_attribute",
                "source_attribute": "channel_id",
            },
            "join_field_tgt": {
                "method": "source_attribute",
                "source_attribute": "id",
            },
            "snapping_distance": 6,
            "use_snapping": True,
        }
    }


@pytest.fixture(scope="function")
def processor(channels, target_layer, import_config):
    return CrossSectionLocationProcessor(
        target_layer=target_layer,
        target_model_cls=None,
        channel_layer=channels,
        conversion_settings=ConversionSettings(import_config["conversion_settings"]),
        target_fields_config=None,
    )


@pytest.fixture
def feature(scope="function"):
    """Create a source feature with point geometry."""
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("channel_id", QVariant.Int))
    feature = QgsFeature(fields)
    feature.setAttribute("id", 1)
    return feature


@pytest.fixture
def channels(scope="session"):
    """Create a vector layer with two channel features, each having a line geometry."""
    layer = QgsVectorLayer("LineString?crs=EPSG:4326", "channels", "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField("id", QVariant.Int)])
    provider.addAttributes([QgsField("code", QVariant.String)])
    layer.updateFields()

    # Create two channel features with line geometries
    feature1 = QgsFeature(layer.fields())
    feature1.setGeometry(QgsGeometry.fromPolyline([QgsPoint(10, 20), QgsPoint(20, 30)]))
    feature1.setAttributes([1, "channel1"])

    feature2 = QgsFeature(layer.fields())
    feature2.setGeometry(QgsGeometry.fromPolyline([QgsPoint(50, 50), QgsPoint(60, 60)]))
    feature2.setAttributes([2, "channel2"])

    # these channels are for testing multiple intersection
    feature3 = QgsFeature(layer.fields())
    feature3.setGeometry(
        QgsGeometry.fromPolyline([QgsPoint(500, 500), QgsPoint(510, 500)])
    )
    feature3.setAttributes([3, "channel3"])

    feature4 = QgsFeature(layer.fields())
    feature4.setGeometry(
        QgsGeometry.fromPolyline([QgsPoint(500, 410), QgsPoint(510, 410)])
    )
    feature4.setAttributes([4, "channel4"])

    provider.addFeatures([feature1, feature2, feature3, feature4])
    return layer


@pytest.mark.parametrize(
    "point,expected_channel_id",
    [
        (QgsPointXY(9, 19), 1),  # snapping
        (QgsPointXY(15, 25), 1),  # on the channel
        (QgsPointXY(55, 55), 2),  # on the other channel
        (QgsPointXY(100, 100), None),  # on no channel
    ],
)
def test_get_matching_channel_point(processor, feature, point, expected_channel_id):
    feature.setGeometry(QgsGeometry.fromPointXY(point))
    assert (
        processor.get_matching_channel(feature, feature.geometry())
        == expected_channel_id
    )


@pytest.mark.parametrize(
    "line, expected_channel_id",
    [
        ([QgsPoint(15, 20), QgsPoint(15, 30)], 1),  # intersects channel 1
        ([QgsPoint(50, 60), QgsPoint(60, 50)], 2),  # intersects channel 2
        ([QgsPoint(100, 100), QgsPoint(200, 200)], None),  # inteersects no channel
        (
            [QgsPoint(505, 400), QgsPoint(505, 600)],
            3,
        ),  # intersects two channels, snap to first line within snapping distance
    ],
)
def test_get_matching_channel_line(processor, feature, line, expected_channel_id):
    feature.setGeometry(QgsGeometry.fromPolyline(line))
    assert (
        processor.get_matching_channel(feature, feature.geometry())
        == expected_channel_id
    )


@pytest.mark.parametrize(
    "channel_id, expected_channel_id", [(1, 1), (2, 2), (99, None)]
)
def test_get_matching_channel_no_geometry(
    processor, feature, channel_id, expected_channel_id
):
    feature.setAttribute("channel_id", channel_id)
    assert (
        processor.get_matching_channel(feature, feature.geometry())
        == expected_channel_id
    )


@pytest.mark.parametrize(
    "point, ref_channel_id, expected_geom",
    [
        (QgsPointXY(15, 25), 1, QgsPointXY(15, 25)),  # on channel 1
        (
            QgsPointXY(9, 19),
            1,
            QgsPointXY(10, 20),
        ),  # just before channel 1; snap to closest point
        (
            QgsPointXY(55, 55),
            None,
            QgsPointXY(55, 55),
        ),  # no ref channel; use original position
    ],
)
def test_get_new_geom_point(processor, point, ref_channel_id, expected_geom):
    ref_channel = (
        processor.channel_layer.getFeature(ref_channel_id)
        if ref_channel_id is not None
        else None
    )
    geom = QgsGeometry.fromPointXY(point)
    new_geom = processor.get_new_geom(geom, ref_channel)
    assert_geometries_equal(
        shapely.wkt.loads(new_geom.asWkt()), shapely.wkt.loads(expected_geom.asWkt())
    )


@pytest.mark.parametrize(
    "line, ref_channel_id, expected_geom",
    [
        ([QgsPoint(15, 20), QgsPoint(15, 30)], 1, QgsPointXY(15, 25)),
        # intersects channel, return intersection
        ([QgsPoint(100, 100), QgsPoint(120, 120)], None, QgsPointXY(110, 110)),
        # no channel, return center of line
    ],
)
def test_get_new_geom_line(processor, line, ref_channel_id, expected_geom):
    ref_channel = (
        processor.channel_layer.getFeature(ref_channel_id)
        if ref_channel_id is not None
        else None
    )
    geom = QgsGeometry.fromPolyline(line)
    new_geom = processor.get_new_geom(geom, ref_channel)
    assert_geometries_equal(
        shapely.wkt.loads(new_geom.asWkt()), shapely.wkt.loads(expected_geom.asWkt())
    )


@pytest.mark.parametrize(
    "ref_channel_id, expected_geom", [(1, QgsPointXY(15, 25)), (None, None)]
)
def test_get_new_geom_no_geometry(processor, ref_channel_id, expected_geom):
    ref_channel = (
        processor.channel_layer.getFeature(ref_channel_id)
        if ref_channel_id is not None
        else None
    )
    geom = QgsGeometry()
    new_geom = processor.get_new_geom(geom, ref_channel)
    if expected_geom is None:
        assert new_geom is None
    else:
        assert_geometries_equal(
            shapely.wkt.loads(new_geom.asWkt()),
            shapely.wkt.loads(expected_geom.asWkt()),
        )


@pytest.mark.parametrize(
    "method, column", [("source_attribute", "id"), ("expression", "code")]
)
def test_channel_mapping(channels, target_layer, import_config, method, column):
    conversion_settings = {
        "join_field_tgt": {"method": method, method: column},
        "snapping_distance": 6,
        "use_snapping": True,
    }
    processor = CrossSectionLocationProcessor(
        target_layer=target_layer,
        target_model_cls=None,
        channel_layer=channels,
        conversion_settings=ConversionSettings(conversion_settings),
        target_fields_config=None,
    )
    channel_id_map = {feat[column]: feat for feat in channels.getFeatures()}
    sorted_channel_mapping = dict(sorted(processor.channel_mapping.items()))
    sorted_channel_id_map = dict(sorted(channel_id_map.items()))
    assert sorted_channel_mapping == sorted_channel_id_map


@pytest.mark.parametrize(
    "method, column", [("source_attribute", "id"), ("expression", "code")]
)
def test_get_join_feat_src_value(channels, target_layer, import_config, method, column):
    conversion_settings = {
        "join_field_src": {"method": method, method: column},
        "snapping_distance": 6,
        "use_snapping": True,
    }
    processor = CrossSectionLocationProcessor(
        target_layer=target_layer,
        target_model_cls=None,
        channel_layer=channels,
        conversion_settings=ConversionSettings(conversion_settings),
        target_fields_config=None,
    )
    feat = channels.getFeature(1)
    assert processor.get_join_feat_src_value(feat) == feat[column]
