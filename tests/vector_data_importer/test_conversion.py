import json

import pytest
import shapely
from shapely.testing import assert_geometries_equal

from threedi_schematisation_editor.utils import gpkg_layer
from threedi_schematisation_editor.vector_data_importer.importers import (
    ChannelsImporter,
    ConnectionNodesImporter,
    CrossSectionDataImporter,
    CrossSectionLocationImporter,
    CulvertsImporter,
    WeirsImporter,
)
from threedi_schematisation_editor.vector_data_importer.processors import (
    CrossSectionDataProcessor,
)
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    CrossSectionDataRemap,
    ImportSettings,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.warnings import StructuresIntegratorWarning

from .utils import *


def get_schematisation_layers(target_gpkg, target_object, conduit_layer_name="channel"):
    temp_gpkg = str(get_temp_copy(target_gpkg))
    return {
        "structure_layer": gpkg_layer(temp_gpkg, target_object),
        "conduit_layer": gpkg_layer(temp_gpkg, conduit_layer_name),
        "node_layer": gpkg_layer(temp_gpkg, "connection_node"),
        "cross_section_location_layer": gpkg_layer(temp_gpkg, "cross_section_location"),
    }


def get_source_layer(name, layername):
    src = str(get_temp_copy(SOURCE_PATH.joinpath(name).with_suffix(".gpkg")))
    return gpkg_layer(src, layername)


def get_import_config(import_config_name):
    src = CONFIG_PATH.joinpath(import_config_name).with_suffix(".json")
    with open(src) as import_config_json:
        import_settings_dict = json.loads(import_config_json.read())
    return ImportSettings(**import_settings_dict)


def compare_layer_geom(layer, ref_layer):
    new_res = {
        k: shapely.wkt.loads(v.asWkt())
        for k, v in sorted(
            ((feat["id"], feat.geometry()) for feat in layer.getFeatures())
        )
    }
    ref_res = {
        k: shapely.wkt.loads(v.asWkt())
        for k, v in sorted(
            ((feat["id"], feat.geometry()) for feat in ref_layer.getFeatures())
        )
    }
    assert list(new_res.keys()) == list(ref_res.keys())
    assert_geometries_equal(list(new_res.values()), list(ref_res.values()), 1e-5)


def compare_layer_attributes(layer, ref_layer, attr_name):
    new_res = {
        k: v
        for k, v in sorted(
            ((feat["id"], feat[attr_name]) for feat in layer.getFeatures())
        )
    }
    ref_res = {
        k: v
        for k, v in sorted(
            ((feat["id"], feat[attr_name]) for feat in ref_layer.getFeatures())
        )
    }
    assert list(new_res.keys()) == list(ref_res.keys())
    assert list(new_res.values()) == list(ref_res.values())


def compare_results(ref_name, layers, target_object, channel_layer_name="channel"):
    src = DATA_PATH.joinpath("ref", ref_name).with_suffix(".gpkg")
    ref_layers = get_schematisation_layers(
        src, target_object, conduit_layer_name=channel_layer_name
    )
    # check attributes: id and geom - anything else is hopefully covered by unit tests
    for name, layer in layers.items():
        compare_layer_geom(layer, ref_layers[name])


def test_multi_import():
    # Test importing two layers without commit in between
    # This uses two instances of the CulvertsImporter, which mimics the procedure in the UI
    layer_pt = get_source_layer("culvert_2layers", "culvert_point")
    layer_line = get_source_layer("culvert_2layers", "culvert_line")
    import_config = get_import_config("culvert")
    target_gpkg = SCHEMATISATION_PATH.joinpath("test_2culverts.gpkg")
    layers = get_schematisation_layers(target_gpkg, "culvert")
    importer = CulvertsImporter(layer_pt, target_gpkg, import_config, **layers)
    importer.import_features()
    importer = CulvertsImporter(layer_line, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("multi_import", layers, "culvert")


def test_integrate_weir_too_long():
    # Test integrating multiple weirs on a channel where the total length of the weirs
    # is larger than the channel
    import_config = get_import_config("integrate_weirs_nosnap_too_long.json")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg")
    src_layer = get_source_layer("weirs_too_long.gpkg", "dhydro_weir")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    with pytest.warns(StructuresIntegratorWarning):
        importer.import_features()
    # the total length of the weirs to import is longer than the channel so nothing should be imported
    assert len([item for item in layers["structure_layer"].getFeatures()]) == 0


def test_integrate_isolated_weir():
    import_config = get_import_config("integrate_weirs_snap.json")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel_with_weir.gpkg")
    src_layer = get_source_layer("weir_isolated.gpkg", "dhydro_weir")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("test_isolated_weir", layers, "weir")


def test_import_connection_nodes():
    import_config = get_import_config("import_connection_nodes.json")
    target_gpkg = get_temp_copy(
        SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg")
    )

    src_layer = get_source_layer("connection_nodes.gpkg", "connection_nodes")
    target_layer = gpkg_layer(target_gpkg, "connection_node")
    importer = ConnectionNodesImporter(
        src_layer, target_gpkg, import_config, target_layer=target_layer
    )
    importer.import_features()
    ref_layer = gpkg_layer(
        get_temp_copy(DATA_PATH.joinpath("ref", "test_import_connection_nodes.gpkg")),
        "connection_node",
    )
    compare_layer_geom(target_layer, ref_layer)


@pytest.mark.parametrize(
    "integrate,snap", [(True, True), (True, False), (False, True), (False, False)]
)
def test_import_weirs(integrate: bool, snap: bool):
    target_layer_name = "weir"
    test_name = f"{'integrate' if integrate else 'import'}_weirs_{'no' if snap else ''}snap.json"
    import_config = get_import_config(test_name)
    src_layer = get_source_layer("weirs.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel_with_weir.gpkg")
    layers = get_schematisation_layers(target_gpkg, target_layer_name)
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results(f"test_{test_name}", layers, target_layer_name)


def test_fix_positioning():
    import_config = get_import_config("import_weirs_fix.json")
    src_layer = get_source_layer("weirs_fix_positions.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("test_weirs_fix_positions", layers, "weir")


def test_integrate_pipe():
    import_config = get_import_config("integrate_weirs_nosnap.json")
    import_config.integration.integration_mode = "pipes"
    src_layer = get_source_layer("weirs.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_pipe.gpkg")
    # TODO: target_gpgk is modified
    layers = get_schematisation_layers(target_gpkg, "weir", conduit_layer_name="pipe")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results(f"test_integrate_pipe", layers, "weir", channel_layer_name="pipe")


@pytest.mark.parametrize(
    "test_name", ["test_points", "test_lines", "test_no_geom", "test_var_matching"]
)
def test_import_cross_section_location(test_name):
    import_config = ImportSettings(
        **{
            "cross_section_location_mapping": {
                "join_field_src": {
                    "method": "source_attribute",
                    "source_attribute": "channel_code",
                },
                "join_field_tgt": {
                    "method": "source_attribute",
                    "source_attribute": "code",
                },
            },
            "connection_nodes": {"snap": True, "snap_distance": 6},
        }
    )
    src_layer = get_source_layer("cross_section_location.gpkg", test_name)
    target_gpkg = SCHEMATISATION_PATH.joinpath("channel_wo_csl.gpkg")
    temp_gpkg = str(get_temp_copy(target_gpkg))
    target_layer = gpkg_layer(temp_gpkg, "cross_section_location")
    importer = CrossSectionLocationImporter(
        src_layer,
        temp_gpkg,
        import_config,
        target_layer=target_layer,
    )
    importer.import_features()
    ref_layer = gpkg_layer(
        get_temp_copy(DATA_PATH.joinpath("ref", f"csl_import_{test_name}.gpkg")),
        "cross_section_location",
    )
    compare_layer_geom(target_layer, ref_layer)
    compare_layer_attributes(target_layer, ref_layer, "channel_id")


def test_import_cross_section_location_with_expression():
    test_name = "test_no_geom"
    import_config = ImportSettings(
        **{
            "cross_section_location_mapping": {
                "join_field_src": {"method": "expression", "expression": "channel_id"},
                "join_field_tgt": {"method": "expression", "expression": "id"},
            },
            "connection_nodes": {"snap": True, "snap_distance": 6},
        }
    )
    src_layer = get_source_layer("cross_section_location.gpkg", test_name)
    target_gpkg = SCHEMATISATION_PATH.joinpath("channel_wo_csl.gpkg")
    temp_gpkg = str(get_temp_copy(target_gpkg))
    target_layer = gpkg_layer(temp_gpkg, "cross_section_location")
    importer = CrossSectionLocationImporter(
        src_layer,
        temp_gpkg,
        import_config,
        target_layer=target_layer,
    )
    importer.import_features()
    ref_layer = gpkg_layer(
        get_temp_copy(DATA_PATH.joinpath("ref", f"csl_import_{test_name}.gpkg")),
        "cross_section_location",
    )
    compare_layer_geom(target_layer, ref_layer)
    compare_layer_attributes(target_layer, ref_layer, "channel_id")


def test_import_adjacent_channels():
    import_config = ImportSettings(
        **{
            "connection_nodes": {
                "snap": True,
                "snap_distance": 1,
                "create_nodes": True,
            },
        }
    )
    src_layer = get_source_layer("channels.gpkg", "test_data")
    target_gpkg = SCHEMATISATION_PATH.joinpath("empty.gpkg")
    layers = get_schematisation_layers(target_gpkg, "channel")
    del layers["conduit_layer"]
    del layers["cross_section_location_layer"]
    importer = ChannelsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("test_import_channels", layers, "channel")


def test_import_cross_section_data():
    config_fields = [
        "cross_section_shape",
        "cross_section_width",
        "cross_section_height",
        "cross_section_y",
        "cross_section_z",
    ]
    method = ColumnImportMethod.ATTRIBUTE.value
    field_config = {
        config_field: {"method": method, method: config_field}
        for config_field in config_fields
    }
    target_map_fields = {
        "target_object_type": "object_type",
        "target_object_id": "object_id",
        "target_object_code": "object_code",
        "order_by": "distance",
    }
    for target, ref in target_map_fields.items():
        field_config[target] = {"method": method, method: ref}
    cross_section_data_remap = CrossSectionDataRemap(
        set_lowest_point_to_zero=False, use_lowest_point_as_reference=False
    )
    import_config = ImportSettings(
        fields=field_config, cross_section_data_remap=cross_section_data_remap
    )
    src_layer = get_source_layer("cross_section_data.gpkg", "cross_section_data")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_csd_import.gpkg")
    temp_gpkg = str(get_temp_copy(target_gpkg))
    target_layers = [
        gpkg_layer(temp_gpkg, model_cls.__tablename__)
        for model_cls in CrossSectionDataProcessor.target_models
    ]
    importer = CrossSectionDataImporter(
        src_layer, temp_gpkg, import_config, target_layers
    )
    importer.import_features()
    ref_gpkg = get_temp_copy(DATA_PATH.joinpath("ref", f"csd_import.gpkg"))
    for target_layer in target_layers:
        ref_layer = gpkg_layer(ref_gpkg, target_layer.name())
        for attribute in [
            "id",
            "cross_section_shape",
            "cross_section_width",
            "cross_section_height",
            "cross_section_table",
        ]:
            compare_layer_attributes(target_layer, ref_layer, attribute)


def test_created_connection_nodes_attributes():
    default_storage_area = 0.64
    import_config = ImportSettings(
        **{
            "connection_nodes": {
                "snap": False,
                "create_nodes": True,
            },
        },
        **{
            "connection_node_fields": {
                "storage_area": {
                    "method": "default",
                    "default_value": default_storage_area,
                },
            }
        },
    )
    src_layer = get_source_layer("channels.gpkg", "test_data")
    target_gpkg = SCHEMATISATION_PATH.joinpath("empty.gpkg")
    layers = get_schematisation_layers(target_gpkg, "channel")
    del layers["conduit_layer"]
    del layers["cross_section_location_layer"]
    importer = ChannelsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    assert all(
        [
            feat["storage_area"] == default_storage_area
            for feat in layers["node_layer"].getFeatures()
        ]
    )
