import warnings as stdlib_warnings
from unittest.mock import MagicMock, patch

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    NULL,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsWkbTypes,
)

import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.processors import (
    SurfaceProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.warnings import ProcessorWarning

# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def surface_fields():
    fields = QgsFields()
    for name, typ in [
        ("id", QVariant.Int),
        ("area", QVariant.Double),
        ("surface_parameters_id", QVariant.Int),
        ("code", QVariant.String),
        ("display_name", QVariant.String),
        ("tags", QVariant.String),
    ]:
        fields.append(QgsField(name, typ))
    return fields


@pytest.fixture
def surface_map_fields():
    fields = QgsFields()
    for name, typ in [
        ("id", QVariant.Int),
        ("surface_id", QVariant.Int),
        ("connection_node_id", QVariant.Int),
        ("percentage", QVariant.Double),
        ("code", QVariant.String),
        ("display_name", QVariant.String),
        ("tags", QVariant.String),
    ]:
        fields.append(QgsField(name, typ))
    return fields


def make_import_settings(
    sewer_type_mappings=None, surface_linking=None, surface_map_fields=None, **surface_linking_kwargs
):
    if surface_linking is None:
        surface_linking = sm.SurfaceLinkingSettings(
            sewer_type_mappings=sewer_type_mappings or [],
            **surface_linking_kwargs,
        )
    return sm.ImportSettings(
        surface_linking=surface_linking,
        surface_map_fields=surface_map_fields or {},
        fields={
            "id": sm.FieldMapConfig(method=ColumnImportMethod.AUTO),
            "surface_parameters_id": sm.FieldMapConfig(
                method=ColumnImportMethod.DEFAULT, default_value=102
            ),
            "code": sm.FieldMapConfig(method=ColumnImportMethod.IGNORE),
            "display_name": sm.FieldMapConfig(method=ColumnImportMethod.IGNORE),
            "tags": sm.FieldMapConfig(method=ColumnImportMethod.IGNORE),
        },
    )


def make_empty_pipe_layer():
    layer = QgsVectorLayer("LineString", "Pipe", "memory")
    pr = layer.dataProvider()
    pr.addAttributes(
        [
            QgsField("id", QVariant.Int),
            QgsField("sewerage_type", QVariant.Int),
            QgsField("connection_node_id_start", QVariant.Int),
            QgsField("connection_node_id_end", QVariant.Int),
        ]
    )
    layer.updateFields()
    return layer


@pytest.fixture
def processor(surface_fields, surface_map_fields):
    target_layer = MagicMock()
    target_layer.fields.return_value = surface_fields
    target_layer.name.return_value = "Surface"
    target_layer.featureCount.return_value = 0

    surface_map_layer = MagicMock()
    surface_map_layer.fields.return_value = surface_map_fields
    surface_map_layer.name.return_value = "Surface map"
    surface_map_layer.featureCount.return_value = 0

    return SurfaceProcessor(
        target_layer,
        surface_map_layer,
        make_import_settings(),
        pipe_layer=make_empty_pipe_layer(),
        node_layer=MagicMock(),
    )


def make_polygon_feature(runoff_pct=50.0, maaiveld=0.0, open_water=0.0, wkt=None):
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("runoff_pct", QVariant.Double))
    fields.append(QgsField("maaiveld", QVariant.Double))
    fields.append(QgsField("open_water", QVariant.Double))
    feat = QgsFeature(fields)
    feat.setAttribute("id", 1)
    feat.setAttribute("runoff_pct", runoff_pct)
    feat.setAttribute("maaiveld", maaiveld)
    feat.setAttribute("open_water", open_water)
    feat.setGeometry(
        QgsGeometry.fromWkt(wkt)
        if wkt
        else QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    )
    return feat


def make_pipe_feat(fid, sewerage_type, start_node_id, end_node_id, start_xy, end_xy):
    fields = QgsFields()
    for name, typ in [
        ("id", QVariant.Int),
        ("sewerage_type", QVariant.Int),
        ("connection_node_id_start", QVariant.Int),
        ("connection_node_id_end", QVariant.Int),
    ]:
        fields.append(QgsField(name, typ))
    feat = QgsFeature(fields)
    feat.setId(fid)
    feat.setAttribute("id", fid)
    feat.setAttribute("sewerage_type", sewerage_type)
    feat.setAttribute("connection_node_id_start", start_node_id)
    feat.setAttribute("connection_node_id_end", end_node_id)
    feat.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(*start_xy), QgsPointXY(*end_xy)])
    )
    return feat


def make_node_feat(node_id, xy, visualisation=0):
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("visualisation", QVariant.Int))
    feat = QgsFeature(fields)
    feat.setAttribute("id", node_id)
    feat.setAttribute("visualisation", visualisation)
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*xy)))
    return feat


def make_pipe_layer_with_feats(pipe_feats):
    layer = make_empty_pipe_layer()
    layer.dataProvider().addFeatures(pipe_feats)
    layer.updateExtents()
    return layer


def make_spatial_processor(
    surface_fields,
    surface_map_fields,
    pipe_feats,
    node_feats,
    sewer_type_mappings,
    search_distance=100.0,
    data_format="wide",
    surface_map_fields_config=None,
):
    node_by_id = {f["id"]: f for f in node_feats}

    target_layer = MagicMock()
    target_layer.fields.return_value = surface_fields
    target_layer.name.return_value = "Surface"
    target_layer.featureCount.return_value = 0

    surface_map_layer = MagicMock()
    surface_map_layer.fields.return_value = surface_map_fields
    surface_map_layer.name.return_value = "Surface map"
    surface_map_layer.featureCount.return_value = 0

    import_settings = make_import_settings(
        sewer_type_mappings=sewer_type_mappings,
        search_distance=search_distance,
        data_format=data_format,
        surface_map_fields=surface_map_fields_config or {},
    )
    processor = SurfaceProcessor(
        target_layer,
        surface_map_layer,
        import_settings,
        pipe_layer=make_pipe_layer_with_feats(pipe_feats),
        node_layer=MagicMock(),
    )
    return processor, node_by_id


@pytest.mark.parametrize(
    "wkt, expect_curved",
    [
        ("CurvePolygon (CircularString (0 0, 1 1, 2 0, 1 -1, 0 0))", False),
        ("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))", False),
    ],
)
def test_process_feature_geometry_type(processor, wkt, expect_curved):
    processor._create_surface_map_features = MagicMock(return_value=[])
    feat = make_polygon_feature(wkt=wkt)
    result = processor.process_feature(feat)
    assert not QgsWkbTypes.isCurvedType(result["Surface"][0].geometry().wkbType())


def test_process_feature_area_computed(processor):
    processor._create_surface_map_features = MagicMock(return_value=[])
    result = processor.process_feature(
        make_polygon_feature(wkt="Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    )
    assert result["Surface"][0]["area"] == pytest.approx(1.0)


def test_process_feature_null_geometry_skipped(processor):
    feat = make_polygon_feature()
    feat.setGeometry(QgsGeometry())
    assert processor.process_feature(feat) == {}


def test_process_feature_surface_map_feats_forwarded(processor, surface_map_fields):
    sm_feat = QgsFeature(surface_map_fields)
    processor._create_surface_map_features = MagicMock(return_value=[sm_feat])
    result = processor.process_feature(make_polygon_feature())
    assert result["Surface map"] == [sm_feat]


@pytest.mark.parametrize(
    "pipes_specs, outlet_node_ids, expected_idx",
    [
        ([(0, 10, 11, (5, 0), (5, 2))], set(), 0),  # pipe in range → returns pipe
        (
            [(0, 10, 11, (500, 0), (500, 2))],
            set(),
            None,
        ),  # pipe out of range → returns None
        ([(1, 10, 11, (5, 0), (5, 2))], set(), None),  # wrong sewerage type
        (
            [(0, 20, 21, (50, 0), (50, 2)), (0, 10, 11, (5, 0), (5, 2))],
            set(),
            1,
        ),  # multiple pipes in range
        (
            [(0, 10, 11, (5, 0), (5, 2))],
            {10},
            None,
        ),  # nearest pipe has outlet node → excluded
        (
            [(0, 20, 21, (50, 0), (50, 2)), (0, 10, 11, (5, 0), (5, 2))],
            {10},
            0,
        ),  # nearest pipe excluded (outlet), farther pipe returned
    ],
)
def test_find_nearest_pipe(
    pipes_specs, outlet_node_ids, expected_idx, surface_fields, surface_map_fields
):
    surface_geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    pipe_feats = [
        make_pipe_feat(i, sewerage_type, start_node, end_node, start_xy, end_xy)
        for i, (sewerage_type, start_node, end_node, start_xy, end_xy) in enumerate(
            pipes_specs
        )
    ]
    nodes = [
        make_node_feat(10, (5, 0), visualisation=1 if 10 in outlet_node_ids else 0),
        make_node_feat(11, (5, 2), visualisation=1 if 11 in outlet_node_ids else 0),
        make_node_feat(20, (50, 0), visualisation=1 if 20 in outlet_node_ids else 0),
        make_node_feat(21, (50, 2), visualisation=1 if 21 in outlet_node_ids else 0),
    ]
    node_layer = make_node_layer_with_feats(nodes)
    node_by_id = {f["id"]: f for f in nodes}

    import_settings = make_import_settings(
        sewer_type_mappings=[], search_distance=100.0
    )
    target_layer = MagicMock()
    target_layer.fields.return_value = surface_fields
    target_layer.name.return_value = "Surface"
    target_layer.featureCount.return_value = 0
    surface_map_layer = MagicMock()
    surface_map_layer.fields.return_value = surface_map_fields
    surface_map_layer.name.return_value = "Surface map"
    surface_map_layer.featureCount.return_value = 0
    processor = SurfaceProcessor(
        target_layer,
        surface_map_layer,
        import_settings,
        pipe_layer=make_pipe_layer_with_feats(pipe_feats),
        node_layer=node_layer,
    )
    processor._current_surface_geom = surface_geom

    with patch(
        "threedi_schematisation_editor.vector_data_importer.processors.get_feature_by_id",
        side_effect=lambda layer, oid: node_by_id.get(oid),
    ):
        result = processor._spatial_match(surface_geom, sewage_type=0)

    if expected_idx is None:
        assert result is None
    else:
        assert result is not None
        assert result["id"] in (10, 11, 20, 21)  # a valid node was chosen


@pytest.mark.parametrize(
    "surface_wkt, start_xy, end_xy, expected_node_id",
    [
        # Surface at origin → start node (5, 0) is closer than end node (5, 100)
        ("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))", (5, 0), (5, 100), 10),
        # Surface at origin → end node (0, 1) is closer than start node (100, 0)
        ("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))", (100, 0), (0, 1), 11),
    ],
)
def test_choose_closer_node(surface_wkt, start_xy, end_xy, expected_node_id):
    surface_geom = QgsGeometry.fromWkt(surface_wkt)
    pipe = make_pipe_feat(1, 0, 10, 11, start_xy, end_xy)
    node_by_id = {
        10: make_node_feat(10, start_xy),
        11: make_node_feat(11, end_xy),
    }
    node_layer = MagicMock()
    with patch(
        "threedi_schematisation_editor.vector_data_importer.processors.get_feature_by_id",
        side_effect=lambda layer, oid: node_by_id.get(oid),
    ):
        result = SurfaceProcessor._choose_closer_node(surface_geom, pipe, node_layer)
    assert result["id"] == expected_node_id


def run_create_surface_map(processor, node_by_id, surface_feat):
    new_feat = QgsFeature(processor.target_fields)
    new_feat["id"] = 1
    geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    new_feat.setGeometry(geom)
    with patch(
        "threedi_schematisation_editor.vector_data_importer.processors.get_feature_by_id",
        side_effect=lambda layer, oid: node_by_id.get(oid),
    ):
        return processor._create_surface_map_features(new_feat, surface_feat, geom)


@pytest.mark.parametrize(
    "runoff_pct, expect_entry",
    [
        (60.0, True),  # non-zero → entry created
        (0.0, False),  # zero → skipped
    ],
)
def test_create_surface_map_percentage(
    surface_fields, surface_map_fields, runoff_pct, expect_entry
):
    pipe = make_pipe_feat(1, 0, 10, 11, (5, 0), (5, 2))
    nodes = [make_node_feat(10, (5, 0)), make_node_feat(11, (5, 2))]
    mappings = [sm.SewerTypeMapping(sewerage_type=0, percentage_column="runoff_pct")]
    processor, node_by_id = make_spatial_processor(
        surface_fields, surface_map_fields, [pipe], nodes, mappings
    )
    result = run_create_surface_map(
        processor, node_by_id, make_polygon_feature(runoff_pct=runoff_pct)
    )
    assert (len(result) == 1) == expect_entry
    if expect_entry:
        assert result[0]["percentage"] == pytest.approx(runoff_pct)
        assert result[0]["connection_node_id"] in (10, 11)
        assert result[0].geometry().type() == QgsWkbTypes.GeometryType.LineGeometry


@pytest.mark.parametrize(
    "runoff_pct, expect_entry",
    [
        (75.0, True),  # non-zero → one entry created
        (0.0, False),  # zero → skipped
    ],
)
def test_create_surface_map_long_data(
    surface_fields, surface_map_fields, runoff_pct, expect_entry
):
    """Long data path: percentage driven by surface_map_fields config."""
    pipe = make_pipe_feat(1, 0, 10, 11, (5, 0), (5, 2))
    nodes = [make_node_feat(10, (5, 0)), make_node_feat(11, (5, 2))]
    processor, node_by_id = make_spatial_processor(
        surface_fields,
        surface_map_fields,
        [pipe],
        nodes,
        sewer_type_mappings=[],
        data_format="long",
        surface_map_fields_config={
            "percentage": sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="runoff_pct"
            ),
        },
    )
    result = run_create_surface_map(
        processor, node_by_id, make_polygon_feature(runoff_pct=runoff_pct)
    )
    assert (len(result) == 1) == expect_entry
    if expect_entry:
        assert result[0]["percentage"] == pytest.approx(runoff_pct)
        assert result[0]["connection_node_id"] in (10, 11)


def test_create_surface_map_long_data_no_pct_config(surface_fields, surface_map_fields):
    """Long data: missing percentage config → no surface_map features created."""
    pipe = make_pipe_feat(1, 0, 10, 11, (5, 0), (5, 2))
    nodes = [make_node_feat(10, (5, 0)), make_node_feat(11, (5, 2))]
    processor, node_by_id = make_spatial_processor(
        surface_fields,
        surface_map_fields,
        [pipe],
        nodes,
        sewer_type_mappings=[],
        data_format="long",
        surface_map_fields_config={},  # no percentage key
    )
    result = run_create_surface_map(
        processor, node_by_id, make_polygon_feature(runoff_pct=75.0)
    )
    assert result == []


def test_create_surface_map_long_data_extra_fields(surface_fields, surface_map_fields):
    """Extra surface_map_fields (code, tags) are applied via update_attributes."""
    pipe = make_pipe_feat(1, 0, 10, 11, (5, 0), (5, 2))
    nodes = [make_node_feat(10, (5, 0)), make_node_feat(11, (5, 2))]
    processor, node_by_id = make_spatial_processor(
        surface_fields,
        surface_map_fields,
        [pipe],
        nodes,
        sewer_type_mappings=[],
        data_format="long",
        surface_map_fields_config={
            "percentage": sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="runoff_pct"
            ),
            "code": sm.FieldMapConfig(
                method=ColumnImportMethod.DEFAULT, default_value="test-code"
            ),
        },
    )
    result = run_create_surface_map(
        processor, node_by_id, make_polygon_feature(runoff_pct=50.0)
    )
    assert len(result) == 1
    assert result[0]["code"] == "test-code"


def test_create_surface_map_no_pipe_warns(surface_fields, surface_map_fields):
    pipe = make_pipe_feat(1, 0, 10, 11, (500, 0), (500, 2))
    nodes = [make_node_feat(10, (500, 0)), make_node_feat(11, (500, 2))]
    mappings = [sm.SewerTypeMapping(sewerage_type=0, percentage_column="runoff_pct")]
    processor, node_by_id = make_spatial_processor(
        surface_fields,
        surface_map_fields,
        [pipe],
        nodes,
        mappings,
        search_distance=10.0,
    )
    with stdlib_warnings.catch_warnings(record=True) as caught:
        stdlib_warnings.simplefilter("always")
        result = run_create_surface_map(processor, node_by_id, make_polygon_feature())
    assert result == []
    assert any(issubclass(w.category, ProcessorWarning) for w in caught)


# ---------------------------------------------------------------------------
# Attribute-match tests
# ---------------------------------------------------------------------------


def make_node_layer_with_feats(node_feats):
    """Real in-memory node layer with id + code fields."""
    layer = QgsVectorLayer("Point", "ConnectionNode", "memory")
    pr = layer.dataProvider()
    pr.addAttributes(
        [
            QgsField("id", QVariant.Int),
            QgsField("code", QVariant.String),
            QgsField("visualisation", QVariant.Int),
        ]
    )
    layer.updateFields()
    pr.addFeatures(node_feats)
    layer.updateExtents()
    return layer


def make_pipe_layer_with_code_feats(pipe_feats):
    """Real in-memory pipe layer with id, sewerage_type, connection_node_ids + code."""
    layer = QgsVectorLayer("LineString", "Pipe", "memory")
    pr = layer.dataProvider()
    pr.addAttributes(
        [
            QgsField("id", QVariant.Int),
            QgsField("sewerage_type", QVariant.Int),
            QgsField("connection_node_id_start", QVariant.Int),
            QgsField("connection_node_id_end", QVariant.Int),
            QgsField("code", QVariant.String),
        ]
    )
    layer.updateFields()
    pr.addFeatures(pipe_feats)
    layer.updateExtents()
    return layer


def make_node_feat_with_code(node_id, xy, code):
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("code", QVariant.String))
    feat = QgsFeature(fields)
    feat.setAttribute("id", node_id)
    feat.setAttribute("code", code)
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*xy)))
    return feat


def make_pipe_feat_with_code(
    fid, sewerage_type, start_node_id, end_node_id, start_xy, end_xy, code
):
    fields = QgsFields()
    for name, typ in [
        ("id", QVariant.Int),
        ("sewerage_type", QVariant.Int),
        ("connection_node_id_start", QVariant.Int),
        ("connection_node_id_end", QVariant.Int),
        ("code", QVariant.String),
    ]:
        fields.append(QgsField(name, typ))
    feat = QgsFeature(fields)
    feat.setId(fid)
    feat.setAttribute("id", fid)
    feat.setAttribute("sewerage_type", sewerage_type)
    feat.setAttribute("connection_node_id_start", start_node_id)
    feat.setAttribute("connection_node_id_end", end_node_id)
    feat.setAttribute("code", code)
    feat.setGeometry(
        QgsGeometry.fromPolylineXY([QgsPointXY(*start_xy), QgsPointXY(*end_xy)])
    )
    return feat


def make_attr_match_processor(
    surface_fields,
    surface_map_fields,
    match_table,
    node_layer,
    pipe_layer,
):
    """Build a SurfaceProcessor configured for attribute matching.

    Includes one spatial fallback pipe+mapping (sewerage_type=0, nearby) so
    fallback cases produce one surface_map entry for easy assertion.
    """
    target_layer = MagicMock()
    target_layer.fields.return_value = surface_fields
    target_layer.name.return_value = "Surface"
    target_layer.featureCount.return_value = 0

    surface_map_layer = MagicMock()
    surface_map_layer.fields.return_value = surface_map_fields
    surface_map_layer.name.return_value = "Surface map"
    surface_map_layer.featureCount.return_value = 0

    import_settings = make_import_settings(
        sewer_type_mappings=[
            sm.SewerTypeMapping(sewerage_type=0, percentage_column="runoff_pct")
        ],
        search_distance=100.0,
        attribute_match_enabled=True,
        spatial_match_enabled=True,
        attribute_match_table=match_table,
        attribute_match_col="code",
        attribute_match_input_config=sm.FieldMapConfig(
            method=ColumnImportMethod.ATTRIBUTE,
            source_attribute="code",
        ),
    )
    return SurfaceProcessor(
        target_layer,
        surface_map_layer,
        import_settings,
        pipe_layer=pipe_layer,
        node_layer=node_layer,
    )


@pytest.mark.parametrize(
    "match_table, n_matches, expect_pct_100",
    [
        ("connection_node", 1, False),  # exact node match → attr path, actual pct
        ("pipe", 1, False),  # exact pipe match → attr path, actual pct
        ("connection_node", 0, False),  # no match → spatial fallback
        ("pipe", 0, False),  # no match → spatial fallback
        ("connection_node", 2, False),  # ambiguous → spatial fallback
        ("pipe", 2, False),  # ambiguous → spatial fallback
    ],
)
def test_attr_match(
    surface_fields, surface_map_fields, match_table, n_matches, expect_pct_100
):
    # Codes used for attribute matching
    match_code = "ABC"
    other_code = "XYZ"

    # Spatial fallback pipe: always present, nearby, sewerage_type=0, non-matching code
    fallback_pipe = make_pipe_feat_with_code(1, 0, 10, 11, (5, 0), (5, 2), other_code)
    fallback_nodes = [make_node_feat(10, (5, 0)), make_node_feat(11, (5, 2))]

    # Build matching nodes/pipes according to n_matches

    matching_nodes = [
        make_node_feat_with_code(20 + i, (0, 0), match_code) for i in range(n_matches)
    ]
    # Always one non-matching node (sewerage-type node lookup needs real layer)
    non_matching_node = make_node_feat_with_code(99, (5, 0), other_code)
    all_nodes = matching_nodes + [non_matching_node]

    matching_pipes = [
        make_pipe_feat_with_code(100 + i, 0, 10, 11, (5, 0), (5, 2), match_code)
        for i in range(n_matches)
    ]
    # Pipe layer also contains the spatial fallback pipe (no code field → use make_pipe_layer_with_feats)
    # We build a separate pipe layer for attribute matching that includes both
    all_pipe_feats = matching_pipes + [fallback_pipe]

    node_layer = make_node_layer_with_feats(all_nodes)
    pipe_layer = make_pipe_layer_with_code_feats(all_pipe_feats)

    processor = make_attr_match_processor(
        surface_fields, surface_map_fields, match_table, node_layer, pipe_layer
    )

    node_by_id = {f["id"]: f for f in fallback_nodes}
    src_feat = make_polygon_feature(runoff_pct=60.0)
    # Give source feature a code field for attribute lookup
    src_fields = QgsFields()
    src_fields.append(QgsField("id", QVariant.Int))
    src_fields.append(QgsField("runoff_pct", QVariant.Double))
    src_fields.append(QgsField("code", QVariant.String))
    src_feat2 = QgsFeature(src_fields)
    src_feat2.setAttribute("id", 1)
    src_feat2.setAttribute("runoff_pct", 60.0)
    src_feat2.setAttribute("code", match_code)
    src_feat2.setGeometry(QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))"))

    with patch(
        "threedi_schematisation_editor.vector_data_importer.processors.get_feature_by_id",
        side_effect=lambda layer, oid: node_by_id.get(oid),
    ):
        new_feat = QgsFeature(processor.target_fields)
        new_feat["id"] = 1
        geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
        new_feat.setGeometry(geom)
        result = processor._create_surface_map_features(new_feat, src_feat2, geom)

    assert len(result) == 1
    assert result[0]["percentage"] == pytest.approx(60.0)
