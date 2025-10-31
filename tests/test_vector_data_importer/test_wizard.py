import json

import pytest
from qgis.core import QgsField, QgsVectorLayer
from qgis.PyQt.QtCore import QVariant

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.vector_data_importer.settings_models as sm
import threedi_schematisation_editor.vector_data_importer.wizard.field_map as field_map
import threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets as settings_widgets
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.vector_data_importer.wizard import (
    ImportStructureWizard,
)
from threedi_schematisation_editor.vector_data_importer.wizard.value_map_dialog import (
    ValueMapModel,
)

from .utils import *


def test_wizard_settings(qgis_application):
    model_gpkg = str(SOURCE_PATH.joinpath("empty.gpkg").with_suffix(".gpkg"))
    wizard = ImportStructureWizard(dm.Culvert, model_gpkg, None)
    with open(DATA_PATH.joinpath("import_culvert.json"), "r") as f:
        json_settings = json.load(f)
    wizard.deserialize(json_settings)
    serialized_settings = wizard.serialize()
    assert wizard.get_settings().model_dump() == serialized_settings


class TestIntegrationSettingsWidget:
    def check_radio_button_state(self, widget, set_integration_mode):
        for integration_mode, radio_button in widget.integration_mode_map.items():
            if integration_mode == set_integration_mode:
                assert radio_button.isChecked()
            else:
                assert not radio_button.isChecked()

    def test_defaults(self, qgis_application):
        widget = settings_widgets.IntegrationSettingsWidget()
        model = sm.IntegrationSettings()
        self.check_radio_button_state(widget, sm.IntegrationMode.NONE)
        assert widget.snap_distance.value() == model.snap_distance
        assert widget.min_length.value() == model.min_length

    def test_deserialize(self, qgis_application):
        widget = settings_widgets.IntegrationSettingsWidget()
        settings = {
            "integration_mode": sm.IntegrationMode.PIPES,
            "snap_distance": 10.5,
            "min_length": 10.5,
        }
        widget.deserialize(settings)
        self.check_radio_button_state(widget, settings["integration_mode"])
        assert widget.snap_distance.value() == settings["snap_distance"]
        assert widget.min_length.value() == settings["min_length"]

    def test_get_settings(self, qgis_application):
        widget = settings_widgets.IntegrationSettingsWidget()
        settings = {
            "integration_mode": sm.IntegrationMode.PIPES,
            "snap_distance": 10.5,
            "min_length": 10.5,
        }
        widget.deserialize(settings)
        assert widget.get_settings().model_dump() == settings

    @pytest.mark.parametrize(
        "integration_mode",
        [
            sm.IntegrationMode.NONE,
            sm.IntegrationMode.PIPES,
            sm.IntegrationMode.CHANNELS,
        ],
    )
    def test_enable_integration_settings(self, integration_mode, qgis_application):
        widget = settings_widgets.IntegrationSettingsWidget()
        widget.deserialize({"integration_mode": integration_mode})
        expected_enabled = (
            False if integration_mode == sm.IntegrationMode.NONE else True
        )
        assert widget.min_length.isEnabled() == expected_enabled
        assert widget.snap_distance.isEnabled() == expected_enabled


class TestConnectNodeSettings:
    def test_defaults(self, qgis_application):
        widget = settings_widgets.ConnectionNodeSettingsWidget()
        model = sm.ConnectionNodeSettings()
        assert widget.create_nodes.isChecked() == model.create_nodes
        assert widget.snap.isChecked() == model.snap
        assert widget.snap_distance.value() == model.snap_distance

    def test_deserialize(self, qgis_application):
        widget = settings_widgets.ConnectionNodeSettingsWidget()
        settings = {"create_nodes": True, "snap": False, "snap_distance": 10.5}
        widget.deserialize(settings)
        assert widget.create_nodes.isChecked() == settings["create_nodes"]
        assert widget.snap.isChecked() == settings["snap"]
        assert widget.snap_distance.value() == settings["snap_distance"]

    def test_get_settings(self, qgis_application):
        widget = settings_widgets.ConnectionNodeSettingsWidget()
        settings = {"create_nodes": True, "snap": False, "snap_distance": 10.5}
        widget.deserialize(settings)
        assert widget.get_settings().model_dump() == settings

    @pytest.mark.parametrize("snap_enabled", [True, False])
    def test_toggle_snap_distance(self, snap_enabled, qgis_application):
        widget = settings_widgets.ConnectionNodeSettingsWidget()
        widget.deserialize({"snap": snap_enabled})
        assert widget.snap_distance.isEnabled() == snap_enabled


class TestCrossSectionDataRemapSettingsWidget:
    def test_defaults(self, qgis_application):
        widget = settings_widgets.CrossSectionDataRemapSettingsWidget()
        model = sm.CrossSectionDataRemap()
        assert (
            widget.set_lowest_point_to_zero.isChecked()
            == model.set_lowest_point_to_zero
        )
        assert (
            widget.use_lowest_point_as_reference.isChecked()
            == model.use_lowest_point_as_reference
        )

    def test_deserialize(self, qgis_application):
        widget = settings_widgets.CrossSectionDataRemapSettingsWidget()
        settings = {
            "set_lowest_point_to_zero": True,
            "use_lowest_point_as_reference": True,
        }
        widget.deserialize(settings)
        assert (
            widget.set_lowest_point_to_zero.isChecked()
            == settings["set_lowest_point_to_zero"]
        )
        assert (
            widget.use_lowest_point_as_reference.isChecked()
            == settings["use_lowest_point_as_reference"]
        )

    def test_get_settings(self, qgis_application):
        widget = settings_widgets.CrossSectionDataRemapSettingsWidget()
        settings = {
            "set_lowest_point_to_zero": True,
            "use_lowest_point_as_reference": True,
        }
        widget.deserialize(settings)
        assert widget.get_settings().model_dump() == settings


class TestCrossSectionLocationMappingSettingsWidget:
    def test_deserialize(self, qgis_application):
        widget = settings_widgets.CrossSectionLocationMappingSettingsWidget()
        settings = {"snap_distance": 100}
        widget.deserialize(settings)
        assert widget.snap_distance.value() == settings["snap_distance"]

    def test_get_settings(self, qgis_application):
        widget = settings_widgets.CrossSectionLocationMappingSettingsWidget()
        settings = {"snap_distance": 100}
        widget.deserialize(settings)
        serialized_settings = widget.get_settings()
        assert serialized_settings.snap_distance == settings["snap_distance"]


class TestFieldMapWidget:
    def test_get_settings(self, qgis_application):
        row_dict = {
            "foo": field_map.FieldMapRow(
                label="foo",
                config=sm.FieldMapConfig(
                    method=ColumnImportMethod.DEFAULT, default_value=1337
                ),
            )
        }
        widget = field_map.FieldMapWidget(row_dict)
        assert widget.get_settings() == {
            key: row.config for key, row in row_dict.items()
        }


class TestFieldMapRow:
    def test_deserialize(self):
        config = {"method": "source_attribute", "source_attribute": "foo"}
        row = field_map.FieldMapRow(
            label="foo",
            config=sm.FieldMapConfig(
                method=ColumnImportMethod.DEFAULT, default_value=1337
            ),
        )
        row.deserialize(config)
        assert row.label == "foo"
        assert row.config.method == ColumnImportMethod.ATTRIBUTE
        assert row.config.source_attribute == "foo"
        assert row.config.default_value is None

    def test_is_editable_label(self):
        row = field_map.FieldMapRow(label="foo")
        assert not row.is_editable(
            field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.LABEL)
        )

    def test_is_editable_method(self):
        row = field_map.FieldMapRow(label="foo")
        assert row.is_editable(
            field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.METHOD)
        )

    @pytest.mark.parametrize(
        "index,expected_value",
        [
            (field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.LABEL), "foo"),
            (
                field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.METHOD),
                ColumnImportMethod.ATTRIBUTE,
            ),
            (-1, None),
        ],
    )
    def test_get_value(self, index, expected_value):
        row = field_map.FieldMapRow(
            label="foo",
            config=sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="bar"
            ),
        )
        assert row.get_value(index) == expected_value

    @pytest.mark.parametrize(
        "index,set_value, new_value",
        [
            (
                field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.LABEL),
                "oof",
                "foo",
            ),
            (
                field_map.FieldMapColumn.to_index(field_map.FieldMapColumn.METHOD),
                ColumnImportMethod.IGNORE,
                ColumnImportMethod.IGNORE,
            ),
            (-1, None, None),
        ],
    )
    def test_set_value(self, index, set_value, new_value):
        row = field_map.FieldMapRow(
            label="foo",
            config=sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="bar"
            ),
        )
        row.set_value(new_value, index)
        assert row.get_value(index) == new_value

    @pytest.mark.parametrize(
        "method,editable_column",
        [
            (
                ColumnImportMethod.ATTRIBUTE,
                field_map.FieldMapColumn.SOURCE_ATTRIBUTE,
            ),
            (
                ColumnImportMethod.EXPRESSION,
                field_map.FieldMapColumn.EXPRESSION,
            ),
            (
                ColumnImportMethod.DEFAULT,
                field_map.FieldMapColumn.DEFAULT_VALUE,
            ),
            (ColumnImportMethod.AUTO, None),
            (ColumnImportMethod.IGNORE, None),
        ],
    )
    def test_is_editable_with_method(self, method, editable_column):
        row = field_map.FieldMapRow(label="foo")
        row.config.method = method
        for column in field_map.FieldMapColumn:
            if column in [
                field_map.FieldMapColumn.LABEL,
                field_map.FieldMapColumn.METHOD,
            ]:
                continue
            col_idx = field_map.FieldMapColumn.to_index(column)
            if column == editable_column:
                assert row.is_editable(col_idx)
            else:
                assert not row.is_editable(col_idx)

    @pytest.mark.parametrize(
        "kwargs, is_valid",
        [
            ({}, False),
            ({"method": ColumnImportMethod.AUTO}, True),
            ({"method": ColumnImportMethod.IGNORE}, True),
            ({"method": ColumnImportMethod.ATTRIBUTE}, False),
            ({"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": "foo"}, True),
            ({"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": ""}, False),
            ({"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": None}, False),
            ({"method": ColumnImportMethod.EXPRESSION}, False),
            ({"method": ColumnImportMethod.EXPRESSION, "expression": "foo"}, True),
            ({"method": ColumnImportMethod.DEFAULT}, False),
            ({"method": ColumnImportMethod.DEFAULT, "default_value": "foo"}, True),
        ],
    )
    def test_is_valid(self, kwargs, is_valid):
        row = field_map.FieldMapRow(label="foo")
        for attr, value in kwargs.items():
            setattr(row.config, attr, value)
        assert row.is_valid == is_valid


class TestFieldMapModel:
    def test_set_current_layer(self):
        # Create a memory layer
        layer = QgsVectorLayer("Point?crs=EPSG:4326", "TestLayer", "memory")
        provider = layer.dataProvider()
        provider.addAttributes(
            [
                QgsField("id", QVariant.Int),
                QgsField("name", QVariant.String),
                QgsField("value", QVariant.Double),
                QgsField("date", QVariant.String),
            ]
        )
        layer.updateFields()
        model = field_map.FieldMapModel({})
        model.set_current_layer(layer)
        assert model.current_layer_attributes == ["id", "name", "value", "date"]

    def test_deserialize(self):
        row_dict = {"foo": field_map.FieldMapRow(label="foo")}
        model = field_map.FieldMapModel(row_dict)
        data = {
            "foo": {"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": "bar"},
            "bar": {},
        }
        model.deserialize(data)
        assert model.row_dict["foo"] == field_map.FieldMapRow(
            label="foo",
            config=sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="bar"
            ),
        )
        assert "bar" not in model.row_dict


class TestValueMapModel:
    def test_set_from_dict(self):
        data = {"foo": "bar"}
        model = ValueMapModel()
        model.set_from_dict(data)
        assert model._sources == ["foo"]
        assert model._targets == ["bar"]

    @pytest.mark.parametrize(
        "sources, targets, expected_dict",
        [
            ([], [], {}),
            (["foo"], ["bar"], {"foo": "bar"}),
            (["foo"], [], {}),
            ([], ["bar"], {}),
            (["foo", "foo"], ["bar", "barbar"], {"foo": "barbar"}),
        ],
    )
    def test_get_dict(self, sources, targets, expected_dict):
        model = ValueMapModel()
        model._sources = sources
        model._targets = targets
        assert model.get_dict() == expected_dict
