from dataclasses import dataclass, field, fields

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
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
import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.processors import (
    CrossSectionDataProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
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
    config_fields = {
        "target_object_type": "object_type",
        "target_object_id": "object_id",
        "target_object_code": "object_code",
        "order_by": "distance",
        "cross_section_shape": "cross_section_shape",
        "cross_section_width": "cross_section_width",
        "cross_section_height": "cross_section_height",
        "cross_section_y": "cross_section_y",
        "cross_section_z": "cross_section_z",
    }
    method = ColumnImportMethod.ATTRIBUTE.value
    return {
        src_field: sm.FieldMapConfig(**{"method": method, method: target_field})
        for src_field, target_field in config_fields.items()
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


def make_features(attributes: dict[str, list], source_fields):
    features = []
    for i in range(len(list(attributes.values())[0])):
        feature = QgsFeature(source_fields)
        for key, vals in attributes.items():
            feature.setAttribute(key, vals[i])
        features.append(feature)
    return features


def test_get_cross_section_table_column(
    source_fields,
    field_config,
):
    features = make_features({"cross_section_width": [1, 2, 3]}, source_fields)
    column = CrossSectionDataProcessor.get_cross_section_table_column(
        features, "cross_section_width", field_config
    )
    assert column == [1, 2, 3]


def test_get_cross_section_table_column_no_data(
    source_fields,
    field_config,
):
    features = make_features({"cross_section_width": [1, 2]}, source_fields)
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
    cs_shape,
    cs_widths,
    cs_heights,
    distances,
    expected_table,
):
    attributes = {
        "cross_section_width": cs_widths,
        "cross_section_height": cs_heights,
        "distance": distances,
    }
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, cs_shape, field_config
    )
    assert table == expected_table


def test_get_cross_section_table_yz(source_fields, field_config):
    attributes = {
        "cross_section_y": [1, 2],
        "cross_section_z": [10, 20],
        "distance": [0, 1],
    }
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        CrossSectionShape.TABULATED_YZ,
        field_config,
    )
    assert table == "1,10\n2,20"


def test_get_cross_section_table_rounding(source_fields, field_config):
    attributes = {
        "cross_section_y": [1.0, 2.0001],
        "cross_section_z": [9.9999999, 20.00051],
        "distance": [0, 1],
    }
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        CrossSectionShape.TABULATED_YZ,
        field_config,
    )
    assert table == "1.0,10.0\n2.0,20.001"


def test_get_cross_section_table_yz_no_sort_by(
    source_fields,
    field_config,
):
    attributes = {"cross_section_y": [10, 0, 20], "cross_section_z": [1, 2, 3]}
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        CrossSectionShape.TABULATED_YZ,
        field_config,
    )
    assert table == "0,2\n10,1\n20,3"


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
    attributes = {"distance": [1, 2], "id": [1, 1]}
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features, cs_shape, field_config
    )
    assert table is None


@pytest.mark.parametrize(
    "attributes, shape, expected_table",
    [
        (
            {"cross_section_y": [1, 2], "cross_section_z": [10, 20]},
            CrossSectionShape.TABULATED_YZ,
            "0,0\n1,10",
        ),
        (
            {"cross_section_y": [1, 2], "cross_section_z": [-10, 0]},
            CrossSectionShape.TABULATED_YZ,
            "0,0\n1,10",
        ),
        (
            {"cross_section_width": [1, 2], "cross_section_height": [10, 20]},
            CrossSectionShape.TABULATED_RECTANGLE,
            "0,1\n10,2",
        ),
        (
            {"cross_section_width": [1, 2], "cross_section_height": [10, 20]},
            CrossSectionShape.TABULATED_TRAPEZIUM,
            "0,1\n10,2",
        ),
    ],
)
def test_get_cross_section_table_lowest_to_zero(
    source_fields,
    field_config,
    attributes,
    shape,
    expected_table,
):
    features = make_features(attributes, source_fields)
    table = CrossSectionDataProcessor.get_cross_section_table(
        features,
        shape,
        field_config,
        set_lowest_point_to_zero=True,
    )
    assert table == expected_table


@pytest.mark.parametrize(
    "shapes,expected_ids",
    [
        ([5, 5, 5], [0, 1, 2]),
        ([5, 6, 6], [0, 1, 2]),
        ([0, 5, 0], [1, 0, 2]),
    ],
)
def test_organize_group(source_fields, field_config, shapes, expected_ids):
    attributes = {
        "cross_section_shape": shapes,
        "distance": [0, 0, 0],
        "id": [0, 1, 2],
        "profile_id": [1, 1, 1],
    }
    provisional_group = make_features(attributes, source_fields)
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
    with pytest.warns(ProcessorWarning):
        group = CrossSectionDataProcessor.organize_group(
            [feature], field_config["cross_section_shape"]
        )
        assert group is None


def test_organize_group_not_tabulated(source_fields, field_config):
    attributes = {
        "cross_section_shape": [5, 6],
        "distance": [0, 0],
        "id": [0, 1],
        "profile_id": [1, 1],
    }
    provisional_group = make_features(attributes, source_fields)
    with pytest.warns(ProcessorWarning):
        CrossSectionDataProcessor.organize_group(
            provisional_group, field_config["cross_section_shape"]
        )


def make_layer(name):
    layer = QgsVectorLayer(
        "Point?crs=EPSG:28992", name, "memory"
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


@pytest.fixture
def target_layer():
    return make_layer("Pipe")


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
    field_config,
):
    src_feat = QgsFeature(source_fields)
    for field, value in target_feat_attributes.items():
        src_feat.setAttribute(field, value)
    target_feat = CrossSectionDataProcessor.find_target_object(
        src_feat=src_feat,
        target_layer=target_layer,
        target_object_id_config=field_config["target_object_id"],
        target_object_code_config=field_config["target_object_code"],
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
def import_settings(field_config):
    return sm.ConversionSettingsModel(
        cross_section_data_remap=sm.CrossSectionDataRemapModel(
            **{
                "set_lowest_point_to_zero": False,
                "use_lowest_point_as_reference": True,
            }
        ),
        fields=field_config,
    )


@pytest.fixture
def processor(target_layer, field_config, import_settings):
    return CrossSectionDataProcessor([target_layer], import_settings)


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
    attributes = {
        "object_id": [0, 1, 1],
        "object_code": ["code_0", "code_1", "code_2"],
        "object_type": 3 * ["pipe"],
    }
    features = make_features(attributes, source_fields)
    target_features = [feat for feat in target_layer.getFeatures()]
    expected_source_feat_map = {
        feat: target_features[feat["object_id"]] for feat in features
    }
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
    attributes = {
        "object_id": object_ids,
        "object_code": ["code_0", "code_1", "code_2"],
        "object_type": 3 * ["pipe"],
        "cross_section_shape": cs_shapes,
    }
    features = make_features(attributes, source_fields)
    processor.build_target_map(features)
    groups = processor.group_features()
    expected_groups = [
        [features[feat_id] for feat_id in group] for group in expected_group_ids
    ]
    assert groups == expected_groups


def test_get_feat_from_group(processor, source_fields, field_config):
    attributes = {
        "id": range(3),
        "distance": 3 * [0],
        "object_id": 3 * [0],
        "object_type": 3 * ["pipe"],
        "cross_section_shape": 3 * [CrossSectionShape.TABULATED_RECTANGLE.value],
    }
    features = make_features(attributes, source_fields)
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


@pytest.mark.parametrize(
    "shape, null_fields",
    [
        (CrossSectionShape.CLOSED_RECTANGLE, ["cross_section_table"]),
        (CrossSectionShape.RECTANGLE, ["cross_section_table", "cross_section_height"]),
        (CrossSectionShape.CIRCLE, ["cross_section_table", "cross_section_height"]),
        (CrossSectionShape.EGG, ["cross_section_table", "cross_section_height"]),
        (
            CrossSectionShape.INVERTED_EGG,
            ["cross_section_table", "cross_section_height"],
        ),
        (
            CrossSectionShape.TABULATED_RECTANGLE,
            ["cross_section_width", "cross_section_height"],
        ),
        (
            CrossSectionShape.TABULATED_TRAPEZIUM,
            ["cross_section_width", "cross_section_height"],
        ),
    ],
)
def test_get_feat_from_group_cross_section_properties_null(
    processor, source_fields, field_config, shape, null_fields
):
    attributes = {
        "id": 2 * [0],
        "distance": 2 * [0],
        "object_id": 2 * [0],
        "object_type": 2 * ["pipe"],
        "cross_section_shape": 2 * [shape.value],
        "cross_section_width": 2 * [10],
        "cross_section_height": 2 * [10],
    }
    features = make_features(attributes, source_fields)
    processor.build_target_map(features)
    new_feat = processor.get_feat_from_group(features)
    for null_field in null_fields:
        assert (null_field not in new_feat.fields().names()) or (
            new_feat[null_field] == NULL
        )


@pytest.mark.parametrize("use_lowest_point_as_reference", [True, False])
def test_get_feat_from_group_use_lowest_as_ref(
    source_fields, use_lowest_point_as_reference, import_settings
):
    import_settings.cross_section_data_remap.use_lowest_point_as_reference = (
        use_lowest_point_as_reference
    )
    target_model_cls = dm.CrossSectionLocation
    layer = make_layer(target_model_cls.__tablename__)
    attributes = {
        "id": range(3),
        "distance": 3 * [0],
        "object_id": 3 * [0],
        "cross_section_y": 3 * [10],
        "cross_section_z": 3 * [10],
        "object_type": 3 * [target_model_cls.__tablename__],
        "cross_section_shape": 3 * [CrossSectionShape.TABULATED_YZ.value],
    }
    features = make_features(attributes, source_fields)
    processor = CrossSectionDataProcessor([layer], import_settings)
    processor.build_target_map(features)
    new_feat = processor.get_feat_from_group(features)
    assert (
        "reference_level" in new_feat.fields().names()
    ) == use_lowest_point_as_reference


@pytest.mark.parametrize(
    "target_model_cls, expected_result",
    [
        (dm.CrossSectionLocation, {"reference_level": 10}),
        (dm.Weir, {"crest_level": 10}),
        (dm.Orifice, {"crest_level": 10}),
        (dm.Culvert, {"invert_level_start": 10, "invert_level_end": 10}),
        (dm.Pipe, {"invert_level_start": 10, "invert_level_end": 10}),
    ],
)
def test_get_reference_levels(
    source_fields, field_config, target_model_cls, expected_result
):
    cross_section_shape = CrossSectionShape.TABULATED_YZ
    attributes = {
        "cross_section_y": 3 * [10],
        "cross_section_z": 3 * [10],
    }
    features = make_features(attributes, source_fields)
    ref_levels = CrossSectionDataProcessor.get_reference_levels(
        features, target_model_cls, cross_section_shape, field_config
    )
    assert ref_levels == expected_result


@pytest.mark.parametrize(
    "cross_section_shape",
    [CrossSectionShape.TABULATED_RECTANGLE, CrossSectionShape.TABULATED_TRAPEZIUM],
)
def test_get_reference_levels_tabulated(
    source_fields, field_config, cross_section_shape
):
    attributes = {
        "cross_section_width": 3 * [20],
        "cross_section_height": 3 * [10],
    }
    target_model_cls = dm.CrossSectionLocation
    features = make_features(attributes, source_fields)
    ref_levels = CrossSectionDataProcessor.get_reference_levels(
        features, target_model_cls, cross_section_shape, field_config
    )
    assert ref_levels["reference_level"] == 10


def test_get_reference_levels_yz(source_fields, field_config):
    cross_section_shape = CrossSectionShape.TABULATED_YZ
    attributes = {
        "cross_section_y": 3 * [20],
        "cross_section_z": 3 * [10],
    }
    target_model_cls = dm.CrossSectionLocation
    features = make_features(attributes, source_fields)
    ref_levels = CrossSectionDataProcessor.get_reference_levels(
        features, target_model_cls, cross_section_shape, field_config
    )
    assert ref_levels["reference_level"] == 10


@pytest.mark.parametrize(
    "cross_section_shape",
    [
        CrossSectionShape.CLOSED_RECTANGLE,
        CrossSectionShape.RECTANGLE,
        CrossSectionShape.CIRCLE,
        CrossSectionShape.EGG,
        CrossSectionShape.INVERTED_EGG,
    ],
)
def test_get_reference_levels_not_tabulated(
    source_fields, field_config, cross_section_shape
):
    attributes = {
        "cross_section_width": 3 * [20],
        "cross_section_height": 3 * [10],
    }
    target_model_cls = dm.CrossSectionLocation
    features = make_features(attributes, source_fields)
    ref_levels = CrossSectionDataProcessor.get_reference_levels(
        features, target_model_cls, cross_section_shape, field_config
    )
    assert ref_levels == {}
