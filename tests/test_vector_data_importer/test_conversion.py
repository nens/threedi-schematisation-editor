import json

import numpy as np
import pytest
import shapely
from shapely.testing import assert_geometries_equal

from threedi_schematisation_editor.utils import gpkg_layer
from threedi_schematisation_editor.vector_data_importer.importers import (
    ConnectionNodesImporter,
    CulvertsImporter,
    WeirsImporter,
)
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


def get_import_config_path(import_config_name):
    src = CONFIG_PATH.joinpath(import_config_name).with_suffix(".json")
    with open(src) as import_config_json:
        return json.loads(import_config_json.read())


def compare_layer(layer, ref_layer):
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


def compare_results(ref_name, layers, target_object, channel_layer_name="channel"):
    src = DATA_PATH.joinpath("ref", ref_name).with_suffix(".gpkg")
    ref_layers = get_schematisation_layers(
        src, target_object, conduit_layer_name=channel_layer_name
    )
    # check attributes: id and geom - anything else is hopefully covered by unit tests
    for name, layer in layers.items():
        compare_layer(layer, ref_layers[name])


def test_multi_import(qgis_application):
    # Test importing two layers without commit in between
    # This uses two instances of the CulvertsImporter, which mimics the procedure in the UI
    layer_pt = get_source_layer("culvert_2layers", "culvert_point")
    layer_line = get_source_layer("culvert_2layers", "culvert_line")
    import_config = get_import_config_path("culvert")
    target_gpkg = SCHEMATISATION_PATH.joinpath("test_2culverts.gpkg")
    layers = get_schematisation_layers(target_gpkg, "culvert")
    importer = CulvertsImporter(layer_pt, target_gpkg, import_config, **layers)
    importer.import_features()
    importer = CulvertsImporter(layer_line, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("multi_import", layers, "culvert")


def test_integrate_weir_too_long(qgis_application):
    # Test integrating multiple weirs on a channel where the total length of the weirs
    # is larger than the channel
    import_config = get_import_config_path("integrate_weirs_nosnap_too_long.json")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg")
    src_layer = get_source_layer("weirs_too_long.gpkg", "dhydro_weir")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    with pytest.warns(StructuresIntegratorWarning):
        importer.import_features()
    # the total length of the weirs to import is longer than the channel so nothing should be imported
    assert len([item for item in layers["structure_layer"].getFeatures()]) == 0


def test_integrate_isolated_weir(qgis_application):
    import_config = get_import_config_path("integrate_weirs_snap.json")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel_with_weir.gpkg")
    src_layer = get_source_layer("weir_isolated.gpkg", "dhydro_weir")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("test_isolated_weir", layers, "weir")


def test_import_connection_nodes(qgis_application):
    import_config = get_import_config_path("import_connection_nodes.json")
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
    compare_layer(target_layer, ref_layer)


@pytest.mark.parametrize(
    "integrate,snap", [(True, True), (True, False), (False, True), (False, False)]
)
def test_import_weirs(qgis_application, integrate: bool, snap: bool):
    target_layer_name = "weir"
    test_name = f"{'integrate' if integrate else 'import'}_weirs_{'no' if snap else ''}snap.json"
    import_config = get_import_config_path(test_name)
    src_layer = get_source_layer("weirs.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel_with_weir.gpkg")
    layers = get_schematisation_layers(target_gpkg, target_layer_name)
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results(f"test_{test_name}", layers, target_layer_name)


def test_fix_positioning(qgis_application):
    import_config = get_import_config_path("import_weirs_fix.json")
    src_layer = get_source_layer("weirs_fix_positions.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg")
    layers = get_schematisation_layers(target_gpkg, "weir")
    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    compare_results("test_weirs_fix_positions", layers, "weir")


def test_integrate_pipe(qgis_application):
    import_config = get_import_config_path("integrate_weirs_nosnap.json")
    import_config["conversion_settings"]["edit_channels"] = False
    import_config["conversion_settings"]["edit_pipes"] = True
    src_layer = get_source_layer("weirs.gpkg", "dhydro_weir")
    target_gpkg = SCHEMATISATION_PATH.joinpath("schematisation_pipe.gpkg")
    layers = get_schematisation_layers(target_gpkg, "weir", conduit_layer_name="pipe")

    importer = WeirsImporter(src_layer, target_gpkg, import_config, **layers)
    importer.import_features()
    # breakpoint()
    compare_results(f"test_integrate_pipe", layers, "weir", channel_layer_name="pipe")
