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
from threedi_schematisation_editor.warnings import ProcessorWarning


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
def target_mapping_config():
    config_fields = {
        "target_object_type": "object_type",
        "target_object_id": "object_id",
        "target_object_code": "object_code",
        "order_by": "distance",
    }
    method = ColumnImportMethod.ATTRIBUTE.value
    return {
        target: {"method": method, method: ref} for target, ref in config_fields.items()
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


def test_get_cross_section_table_column(
    source_fields,
    field_config,
):
    features = []
    for width in [1, 2, 3]:
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_width", width)
        features.append(feature)
    column = CrossSectionDataProcessor.get_cross_section_table_column(
        features, "cross_section_width", field_config
    )
    assert column == [1, 2, 3]


def test_get_cross_section_table_column_no_data(
    source_fields,
    field_config,
):
    features = []
    for width in [1, 2]:
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_width", width)
        features.append(feature)
    feature = QgsFeature(source_fields)
    features.append(feature)
    with pytest.warns(ProcessorWarning):
        CrossSectionDataProcessor.get_cross_section_table_column(
            features, "cross_section_width", field_config
        )


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
    target_mapping_config,
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
        features, cs_shape, target_mapping_config["order_by"], field_config
    )
    assert table == expected_table


def test_get_cross_section_table_yz(source_fields, field_config, target_mapping_config):
    features = []
    cs_data = [[1, 10, 0], [2, 20, 1]]
    for y, z, distance in cs_data:
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_y", y)
        feature.setAttribute("cross_section_z", z)
        feature.setAttribute("distance", distance)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        CrossSectionShape.TABULATED_YZ,
        target_mapping_config["order_by"],
        field_config,
    )
    assert table == "1,10\n2,20"


def test_get_cross_section_table_yz_no_sort_by(
    source_fields,
    field_config,
    target_mapping_config,
):
    features = []
    y = [10, 0, 20]
    z = [1, 2, 3]
    for y, z in zip(y, z):
        feature = QgsFeature(source_fields)
        feature.setAttribute("cross_section_y", y)
        feature.setAttribute("cross_section_z", z)
        features.append(feature)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        CrossSectionShape.TABULATED_YZ,
        target_mapping_config["order_by"],
        field_config,
    )
    assert table == "0,2\n10,1\n20,3"


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
    "shapes,expected_ids",
    [
        ([5, 5, 5], [0, 1, 2]),
        ([5, 6, 6], [0, 1, 2]),
        ([0, 5, 0], [1, 0, 2]),
    ],
)
def test_organize_group(source_fields, field_config, shapes, expected_ids):
    provisional_group = []
    for i, shape in enumerate(shapes):
        feature = QgsFeature(source_fields)
        feature.setAttribute("profile_id", 1)
        feature.setAttribute("distance", 0)
        feature.setAttribute("id", i)
        feature.setAttribute("cross_section_shape", shape)
        feature.setId(i)
        provisional_group.append(feature)
    group = CrossSectionDataProcessor.organize_group(
        provisional_group, field_config["cross_section_shape"]
    )
    assert [feature["id"] for feature in group] == expected_ids


@pytest.mark.parametrize("cross_section_shape", [0, 10])
def test_organize_group_shape_mismatch(
    source_fields, field_config, cross_section_shape
):
    feature = QgsFeature(source_fields)
    feature.setAttribute("profile_id", 1)
    feature.setAttribute("id", 1)
    feature.setAttribute("cross_section_shape", cross_section_shape)
    feature.setId(1)
    with pytest.warns(ProcessorWarning):
        group = CrossSectionDataProcessor.organize_group(
            [feature], field_config["cross_section_shape"]
        )
        assert group is None


def test_organize_group_not_tabulated(source_fields, field_config):
    provisional_group = []
    shapes = [5, 6]
    for i, shape in enumerate(shapes):
        feature = QgsFeature(source_fields)
        feature.setAttribute("profile_id", 1)
        feature.setAttribute("distance", 0)
        feature.setAttribute("id", i)
        feature.setAttribute("cross_section_shape", shape)
        feature.setId(i)
        provisional_group.append(feature)
    with pytest.warns(ProcessorWarning):
        CrossSectionDataProcessor.organize_group(
            provisional_group, field_config["cross_section_shape"]
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
    source_fields,
    target_layer,
    target_feat_attributes,
    expected_attributes,
    target_mapping_config,
):
    src_feat = QgsFeature(source_fields)
    for field, value in target_feat_attributes.items():
        src_feat.setAttribute(field, value)
    target_feat = CrossSectionDataProcessor.find_target_object(
        src_feat=src_feat,
        target_layer=target_layer,
        target_object_id_config=target_mapping_config["target_object_id"],
        target_object_code_config=target_mapping_config["target_object_code"],
    )
    for field, value in expected_attributes.items():
        assert target_feat[field] == value


@pytest.mark.parametrize(
    "target_object_id, target_object_code,expected_attributes",
    [
        (
            "object_id",
            None,
            {"id": 1, "code": "code_1"},
        ),
        (
            None,
            "object_code",
            {"id": 2, "code": "code_2"},
        ),
    ],
)
def test_find_target_object_missing_target_fields(
    source_fields,
    target_layer,
    target_object_id,
    target_object_code,
    expected_attributes,
):
    method = ColumnImportMethod.ATTRIBUTE.value
    target_object_id_config = (
        {"method": method, method: target_object_id} if target_object_id else None
    )
    target_object_code_config = (
        {"method": method, method: target_object_code} if target_object_code else None
    )
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_id", 1)
    src_feat.setAttribute("object_code", "code_2")
    target_feat = CrossSectionDataProcessor.find_target_object(
        src_feat=src_feat,
        target_layer=target_layer,
        target_object_id_config=target_object_id_config,
        target_object_code_config=target_object_code_config,
    )
    for field, value in expected_attributes.items():
        assert target_feat[field] == value


@pytest.mark.parametrize(
    "target_object_id, target_object_code",
    [
        ("object_id", None),
        (None, "object_code"),
    ],
)
def test_find_target_object_no_match(
    source_fields, target_layer, target_object_id, target_object_code
):
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_id", 1337)
    src_feat.setAttribute("object_code", "code_1337")
    method = ColumnImportMethod.ATTRIBUTE.value
    target_object_id_config = (
        {"method": method, method: target_object_id} if target_object_id else None
    )
    target_object_code_config = (
        {"method": method, method: target_object_code} if target_object_code else None
    )
    with pytest.warns(ProcessorWarning):
        target_feat = CrossSectionDataProcessor.find_target_object(
            src_feat=src_feat,
            target_layer=target_layer,
            target_object_id_config=target_object_id_config,
            target_object_code_config=target_object_code_config,
        )
    assert target_feat is None


@pytest.fixture
def processor(target_layer, field_config, target_mapping_config):
    return CrossSectionDataProcessor(
        field_config, target_mapping_config, [target_layer]
    )


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
    ],
)
def test_get_target_model_cls(
    processor, source_fields, object_type_str, expected_model_cls
):
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_type", object_type_str)
    assert processor.get_target_model_cls(src_feat) == expected_model_cls


def test_get_target_model_cls_no_match(processor, source_fields):
    src_feat = QgsFeature(source_fields)
    src_feat.setAttribute("object_type", "foo")
    with pytest.warns(ProcessorWarning):
        assert processor.get_target_model_cls(src_feat) is None


def test_get_target_model_cls_no_object_type(processor, source_fields):
    src_feat = QgsFeature(source_fields)
    with pytest.warns(ProcessorWarning):
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


def test_build_target_map(processor, source_fields, target_layer):
    features = []
    object_ids = [0, 1, 1]
    expected_source_feat_map = {}
    target_features = [feat for feat in target_layer.getFeatures()]
    for i, object_id in enumerate(object_ids):
        feature = QgsFeature(source_fields)
        feature.setAttribute("object_id", object_id)
        feature.setAttribute("object_code", f"code_{i}")
        feature.setAttribute("object_type", "pipe")
        features.append(feature)
        expected_source_feat_map[feature] = target_features[object_id]
    processor.build_target_map(features)
    assert processor.source_feat_map == expected_source_feat_map


@pytest.mark.parametrize(
    "object_ids,cs_shapes,expected_group_ids",
    [
        ([0, 1, 1], [1, 5, 5], [[0], [1, 2]]),  # 2 groups, with valid shapes
        ([0, 1, 1], [1, 1, 1], [[0], [1], [2]]),  # 2 groups, but no tabulated shapes
        ([0, 1, 2], [5, 5, 5], [[0], [1], [2]]),  # no groups
    ],
)
def test_group_features(
    processor, source_fields, object_ids, cs_shapes, expected_group_ids
):
    features = []
    feature_map = {}
    for i, (object_id, cs_shape) in enumerate(zip(object_ids, cs_shapes)):
        feature = QgsFeature(source_fields)
        feature.setAttribute("object_id", object_id)
        feature.setAttribute("object_code", f"code_{i}")
        feature.setAttribute("object_type", "pipe")
        feature.setAttribute("cross_section_shape", cs_shape)
        feature_map[i] = feature
        features.append(feature)
    processor.build_target_map(features)
    groups = processor.group_features()
    expected_groups = [
        [feature_map[feat_id] for feat_id in group] for group in expected_group_ids
    ]
    assert groups == expected_groups


def test_get_feat_from_group(processor, source_fields, field_config):
    features = []
    for i in range(3):
        feature = QgsFeature(source_fields)
        feature.setAttribute("id", i)
        feature.setAttribute("distance", 0)
        feature.setAttribute("object_id", 0)
        feature.setAttribute("object_type", f"pipe")
        feature.setAttribute(
            "cross_section_shape", CrossSectionShape.TABULATED_RECTANGLE.value
        )
        features.append(feature)
    processor.build_target_map(features)
    new_feat = processor.get_feat_from_group(features)
    # assure that the new_feat has a value for cross_section_table
    # if this would not be the case, the statement below would raise
    # note that value of cross_section_table is tested elsewhere
    assert new_feat["cross_section_table"] == ""
    # ensure other attributes are copied
    assert new_feat["distance"] == 0
    assert (
        new_feat["cross_section_shape"] == CrossSectionShape.TABULATED_RECTANGLE.value
    )
    assert processor.source_feat_map[new_feat] == processor.source_feat_map[features[0]]
