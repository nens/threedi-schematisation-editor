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


def make_import_settings(**surface_kwargs):
    sewer_type_mappings = surface_kwargs.pop("sewer_type_mappings", [])
    linking = surface_kwargs.pop("linking", sm.SurfaceLinkingSettings())
    return sm.ImportSettings(
        surface_map_percentage=sm.SurfaceMapPercentageSettings(
            sewer_type_mappings=sewer_type_mappings
        ),
        surface_linking=linking,
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


def make_node_feat(node_id, xy):
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    feat = QgsFeature(fields)
    feat.setAttribute("id", node_id)
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
        linking=sm.SurfaceLinkingSettings(search_distance=search_distance),
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
    "pipes_specs, expected_idx",
    [
        ([(0, 10, 11, (5, 0), (5, 2))], 0),  # pipe in range → returns pipe
        ([(0, 10, 11, (500, 0), (500, 2))], None),  # pipe out of range → returns None
        ([(1, 10, 11, (5, 0), (5, 2))], None),  # wrong sewerage type
        (
            [(0, 20, 21, (50, 0), (50, 2)), (0, 10, 11, (5, 0), (5, 2))],
            1,
        ),  # multiple pipes in range
    ],
)
def test_find_nearest_pipe(pipes_specs, expected_idx):
    surface_geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    linking_config = sm.SurfaceLinkingSettings(search_distance=100.0)
    mapping_config = sm.SewerTypeMapping(sewerage_type=0)
    pipe_features = {
        i: make_pipe_feat(i, sewerage_type, start_node, end_node, start_xy, end_xy)
        for i, (sewerage_type, start_node, end_node, start_xy, end_xy) in enumerate(
            pipes_specs
        )
    }
    result = SurfaceProcessor._find_nearest_pipe(
        surface_geom,
        pipe_features,
        list(pipe_features.keys()),
        mapping_config,
        linking_config,
    )
    if expected_idx is None:
        assert result is None
    else:
        assert pipe_features[expected_idx] == result


@pytest.mark.parametrize(
    "sewerage_type, pref_field, pref_value, near_xy, far_xy, expected_id",
    [
        # Storm drain preference offsets distance: far pipe wins after offset
        (1, "stormwater_sewer_preference", 20.0, (50, 0), (5, 0), 2),
        # Sanitary sewer preference offsets distance: far pipe wins after offset
        (2, "sanitary_sewer_preference", 20.0, (50, 0), (5, 0), 2),
    ],
)
def test_find_nearest_pipe_preference_offset(
    sewerage_type, pref_field, pref_value, near_xy, far_xy, expected_id
):
    """Preference offset can make the geometrically farther pipe win."""
    surface_geom = QgsGeometry.fromWkt("Polygon ((0 0, 1 0, 1 1, 0 1, 0 0))")
    near = make_pipe_feat(1, sewerage_type, 10, 11, near_xy, (near_xy[0], 2))
    far = make_pipe_feat(2, sewerage_type, 20, 21, far_xy, (far_xy[0], 2))
    pipe_features = {near.id(): near, far.id(): far}
    mapping_config = sm.SewerTypeMapping(
        sewerage_type=sewerage_type, percentage_column="runoff_pct"
    )
    linking_config = sm.SurfaceLinkingSettings(**{pref_field: pref_value})
    result = SurfaceProcessor._find_nearest_pipe(
        surface_geom,
        pipe_features,
        list(pipe_features.keys()),
        mapping_config,
        linking_config,
    )
    assert result.id() == expected_id


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
