from dataclasses import dataclass, field, fields

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
from threedi_schema.domain.constants import CrossSectionShape

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.processors import (
    CrossSectionDataProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    ConversionSettings,
)


@dataclass
class SourceData:
    object_type: str
    object_id: int
    object_code: str
    cross_section_shape: int
    cross_section_width: float
    cross_section_height: float
    cross_section_y: float
    cross_section_z: float
    distance: float
    profile_id: int


@pytest.fixture
def field_config():
    config_fields = [
        "cross_section_shape",
        "cross_section_width",
        "cross_section_height",
        "cross_section_y",
        "cross_section_z",
    ]
    method = ColumnImportMethod.ATTRIBUTE.value
    return {
        config_field: {"method": method, method: config_field}
        for config_field in config_fields
    }


@pytest.fixture
def source_fields():
    source_fields = QgsFields()
    for field_ in fields(SourceData):
        qvariant_type = (
            QVariant.String
            if field_.type == str
            else QVariant.Double
            if field_.type == float
            else QVariant.Int
        )
        source_fields.append(QgsField(field_.name, qvariant_type))
    source_fields.append(QgsField("id", QVariant.Int))
    return source_fields


@pytest.mark.parametrize(
    "cs_shape,cs_widths,cs_heights,distances,expected_table",
    [
        (CrossSectionShape.TABULATED_RECTANGLE, [1, 2], [10, 20], [1, 2], "10,1\n20,2"),
        (CrossSectionShape.TABULATED_TRAPEZIUM, [1, 2], [10, 20], [1, 2], "10,1\n20,2"),
        (CrossSectionShape.TABULATED_RECTANGLE, [1, 2], [10, 20], [2, 1], "20,2\n10,1"),
        (CrossSectionShape.TABULATED_RECTANGLE, [1], [10], [1], "10,1"),
    ],
)
def test_get_cross_section_table_tabulated(
    source_fields,
    field_config,
    cs_shape,
    cs_widths,
    cs_heights,
    distances,
    expected_table,
):
    features = []
    cs_data = zip(cs_widths, cs_heights, distances)
    for width, height, distance in cs_data:
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_width", width)
        feature.setAttribute("cross_section_height", height)
        feature.setAttribute("distance", distance)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, cs_shape, "distance", field_config
    )
    assert table == expected_table


def test_get_cross_section_table_yz(source_fields, field_config):
    features = []
    cs_data = [[1, 10, 0], [2, 20, 1]]
    for y, z, distance in cs_data:
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_y", y)
        feature.setAttribute("cross_section_z", z)
        feature.setAttribute("distance", distance)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, CrossSectionShape.TABULATED_YZ, "distance", field_config
    )
    assert table == "1,10\n2,20"


@pytest.mark.parametrize(
    "cs_shape",
    [
        CrossSectionShape.TABULATED_RECTANGLE,
        CrossSectionShape.TABULATED_TRAPEZIUM,
        CrossSectionShape.TABULATED_YZ,
    ],
)
def test_get_cross_section_table_missing_data(source_fields, field_config, cs_shape):
    features = []
    for distance in [1, 2]:
        feature = QgsFeature(source_fields)
        feature.setAttribute("distance", distance)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, cs_shape, "distance", field_config
    )
    assert table == "NULL,NULL\nNULL,NULL"


@pytest.mark.parametrize(
    "cs_shape",
    [
        CrossSectionShape.CLOSED_RECTANGLE,
        CrossSectionShape.RECTANGLE,
        CrossSectionShape.CIRCLE,
        CrossSectionShape.EGG,
        CrossSectionShape.INVERTED_EGG,
    ],
)
def test_get_cross_section_table_missing_data(source_fields, field_config, cs_shape):
    features = []
    for distance in [1, 2]:
        feature = QgsFeature(source_fields)
        feature.setAttribute("id", 1)
        feature.setAttribute("distance", distance)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, cs_shape, "distance", field_config
    )
    assert table is None


@pytest.mark.parametrize(
    "profile_ids,expected_group_ids",
    [
        ([1, 1, 2, 2, 3, 3], [[0, 1], [2, 3], [4, 5]]),
        ([1, 2, 3], [[0], [1], [2]]),
        ([1, 1, 2], [[0, 1], [2]]),
    ],
)
def test_group_features(source_fields, field_config, profile_ids, expected_group_ids):
    features = []
    feature_map = {}
    for i, profile_id in enumerate(profile_ids):
        feature = QgsFeature(source_fields)
        feature.setAttribute("profile_id", profile_id)
        feature.setAttribute("distance", 0)
        feature.setAttribute("id", i)
        feature.setId(i)
        feature.setAttribute(
            "cross_section_shape", CrossSectionShape.TABULATED_RECTANGLE.value
        )
        features.append(feature)
        feature_map[i] = feature
    groups = CrossSectionDataProcessor.group_features(
        features, "profile_id", field_config
    )
    expected_groups = [
        [feature_map[feat_id] for feat_id in group] for group in expected_group_ids
    ]
    assert groups == expected_groups


def test_get_feat_from_group(source_fields, field_config):
    features = []
    for i in range(3):
        feature = QgsFeature(source_fields)
        feature.setAttribute("id", i)
        feature.setAttribute("distance", 0)
        feature.setAttribute(
            "cross_section_shape", CrossSectionShape.TABULATED_RECTANGLE.value
        )
        features.append(feature)
    new_feat = CrossSectionDataProcessor.get_feat_from_group(
        features, "distance", field_config
    )
    # assure that the new_feat has a value for cross_section_table
    # if this would not be the case, the statement below would raise
    # note that value of cross_section_table is tested elsewhere
    assert new_feat["cross_section_table"] == "NULL,NULL\nNULL,NULL\nNULL,NULL"
    # ensure other attributes are copied
    assert new_feat["distance"] == 0
    assert (
        new_feat["cross_section_shape"] == CrossSectionShape.TABULATED_RECTANGLE.value
    )


@pytest.fixture
def target_layer():
    layer = QgsVectorLayer(
        "Point?crs=EPSG:28992", "Pipe", "memory"
    )  # Create QgsVectorLayer
    layer_data_provider = layer.dataProvider()
    layer_fields = QgsFields()
    layer_fields.append(QgsField("id", QVariant.Int))
    layer_fields.append(QgsField("code", QVariant.String))
    layer_data_provider.addAttributes(layer_fields)
    layer.updateFields()
    for i in range(3):
        feature = QgsFeature(layer_fields)
        feature.setAttribute("id", i)
        feature.setAttribute("code", f"code_{i}")
        layer_data_provider.addFeature(feature)  # Add features to QgsVectorLayer
    return layer


@pytest.mark.parametrize(
    "target_feat_attributes, expected_attributes",
    [
        ({"object_id": 1, "object_code": "code_2"}, {"id": 1, "code": "code_1"}),
        ({"object_id": 1}, {"id": 1, "code": "code_1"}),
        ({"object_id": None, "object_code": "code_2"}, {"id": 2, "code": "code_2"}),
        ({"object_code": "code_2"}, {"id": 2, "code": "code_2"}),
    ],
)
def test_find_target_object(
    source_fields, target_layer, target_feat_attributes, expected_attributes
):
    src_feat = QgsFeature(source_fields)
    for field, value in target_feat_attributes.items():
        src_feat.setAttribute(field, value)
    target_feat = CrossSectionDataProcessor.find_target_object(
        src_feat=src_feat,
        target_layer=target_layer,
        target_object_id_field="object_id",
        target_object_code_field="object_code",
    )
    for field, value in expected_attributes.items():
        assert target_feat[field] == value


@pytest.mark.parametrize(
    "field_kwargs,expected_attributes",
    [
        (
            {"target_object_id_field": "object_id", "target_object_code_field": None},
            {"id": 1, "code": "code_1"},
        ),
        (
            {"target_object_id_field": None, "target_object_code_field": "object_code"},
            {"id": 2, "code": "code_2"},
        ),
    ],
)
def test_find_target_object_missing_target_fields(
    source_fields, target_layer, field_kwargs, expected_attributes
):
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_id", 1)
    src_feat.setAttribute("object_code", "code_2")
    target_feat = CrossSectionDataProcessor.find_target_object(
        src_feat=src_feat, target_layer=target_layer, **field_kwargs
    )
    for field, value in expected_attributes.items():
        assert target_feat[field] == value


@pytest.fixture
def processor(target_layer, field_config):
    conversion_settings = ConversionSettings(
        {
            "order_by": "distance",
            "group_by": "profile_id",
            "target_object_type": "object_type",
            "target_object_id": "object_id",
            "target_object_code": "object_code",
        }
    )
    return CrossSectionDataProcessor(conversion_settings, field_config, [target_layer])


@pytest.mark.parametrize(
    "object_type_str,expected_str",
    [
        ("foo", "foo"),
        ("Foo", "foo"),
        ("fOO", "foo"),
        ("foo-foo", "foofoo"),
        ("foo_foo", "foofoo"),
        ("foo foo", "foofoo"),
    ],
)
def test_get_unified_object_type_int(object_type_str, expected_str):
    assert (
        CrossSectionDataProcessor.get_unified_object_type_str(object_type_str)
        == expected_str
    )


@pytest.mark.parametrize(
    "object_type_str,expected_model_cls",
    [
        ("pipe", dm.Pipe),
        ("cross section location", dm.CrossSectionLocation),
        ("foo", None),
    ],
)
def test_get_target_model_cls(
    processor, source_fields, object_type_str, expected_model_cls
):
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_type", object_type_str)
    assert processor.get_target_model_cls(src_feat) == expected_model_cls


def test_get_target_model_cls_no_object_type(processor, source_fields):
    src_feat = QgsFeature(source_fields)
    assert processor.get_target_model_cls(src_feat) is None


@pytest.mark.parametrize(
    "model_cls,returns_layer",
    [
        (dm.Pipe, True),
        (dm.Culvert, False),
    ],
)
def test_get_target_layer(
    processor, source_fields, target_layer, model_cls, returns_layer
):
    if returns_layer:
        assert processor.get_target_layer(model_cls) == target_layer
    else:
        assert processor.get_target_layer(model_cls) is None
