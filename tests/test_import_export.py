# Copyright (C) 2023 by Lutra Consulting
from threedi_schematisation_editor.conversion import ModelDataConverter
from threedi_schematisation_editor.data_models import ALL_MODELS
from threedi_schematisation_editor.utils import sqlite_layer


def test_data_import_export_integrity(data_conversion_setup):
    qgis_app, src_sqlite, reference_sqlite, import_export_sqlite, gpkg = data_conversion_setup

    importer = ModelDataConverter(import_export_sqlite, gpkg)
    importer.create_empty_user_layers()
    importer.import_all_model_data()

    exporter = ModelDataConverter(import_export_sqlite, gpkg)
    exporter.trim_sqlite_targets()
    exporter.export_all_model_data()

    for annotated_model_cls in ALL_MODELS:
        for src_table in annotated_model_cls.SQLITE_SOURCES or []:
            ie_layer = sqlite_layer(import_export_sqlite, src_table)
            ref_layer = sqlite_layer(reference_sqlite, src_table)
            if not ie_layer.isValid():
                ie_layer = sqlite_layer(import_export_sqlite, src_table, geom_column=None)
            if not ref_layer.isValid():
                ref_layer = sqlite_layer(reference_sqlite, src_table, geom_column=None)
            ie_lyr_count, ref_lyr_count = ie_layer.featureCount(), ref_layer.featureCount()
            assert ref_lyr_count == ie_lyr_count
            id_field = annotated_model_cls.IMPORT_FIELD_MAPPINGS.get("id", "id")
            ie_feats = {f[id_field]: f for f in ie_layer.getFeatures()}
            ref_feats = {f[id_field]: f for f in ref_layer.getFeatures()}
            ie_field_types = {field.name(): field.typeName() for field in ie_layer.fields()}
            ref_field_types = {field.name(): field.typeName() for field in ref_layer.fields()}
            assert ie_field_types == ref_field_types
            field_names = list(ref_field_types.keys())
            for feat_id, ref_feat in ref_feats.items():
                ie_feat = ie_feats[feat_id]
                assert ie_feat.geometry().asWkt() == ref_feat.geometry().asWkt()
                for field_name in field_names:
                    ie_value = ie_feat[field_name]
                    ref_value = ref_feat[field_name]
                    if field_name == "timeseries":
                        ie_value = [float(value_str) for row in ie_value.split("\n") for value_str in row.split(",")]
                        ref_value = [float(value_str) for row in ref_value.split("\n") for value_str in row.split(",")]
                    assert ie_value == ref_value
