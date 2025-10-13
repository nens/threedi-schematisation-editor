import pytest

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ConnectionNodeSettingsModel,
    IntegrationMode,
    IntegrationSettingsModel,
)
from threedi_schematisation_editor.vector_data_importer.wizard import VDIWizard
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    IntegrationSettingsWidget,
)


def test_wizard(qgis_application):
    wizard = VDIWizard(dm.ConnectionNode, None, None)
    wizard.serialize()


class TestIntegrationSettingsWidget:
    def check_radio_button_state(self, widget, set_integration_mode):
        for integration_mode, radio_button in widget.integration_mode_map.items():
            if integration_mode == set_integration_mode:
                assert radio_button.isChecked()
            else:
                assert not radio_button.isChecked()

    def test_defaults(self, qgis_application):
        widget = IntegrationSettingsWidget()
        model = IntegrationSettingsModel()
        self.check_radio_button_state(widget, IntegrationMode.NONE)
        assert widget.snap_distance.value() == model.snap_distance
        assert widget.min_length.value() == model.min_length

    def test_deserialize(self, qgis_application):
        widget = IntegrationSettingsWidget()
        settings = {
            "integration_mode": IntegrationMode.PIPES,
            "snap_distance": 10.5,
            "min_length": 10.5,
        }
        widget.deserialize(settings)
        self.check_radio_button_state(widget, settings["integration_mode"])
        assert widget.snap_distance.value() == settings["snap_distance"]
        assert widget.min_length.value() == settings["min_length"]

    def test_serialize(self, qgis_application):
        widget = IntegrationSettingsWidget()
        settings = {
            "integration_mode": IntegrationMode.PIPES,
            "snap_distance": 10.5,
            "min_length": 10.5,
        }
        widget.deserialize(settings)
        assert widget.serialize() == settings

    @pytest.mark.parametrize(
        "integration_mode",
        [IntegrationMode.NONE, IntegrationMode.PIPES, IntegrationMode.CHANNELS],
    )
    def test_enable_integration_settings(self, integration_mode, qgis_application):
        widget = IntegrationSettingsWidget()
        widget.deserialize({"integration_mode": integration_mode})
        expected_enabled = False if integration_mode == IntegrationMode.NONE else True
        assert widget.min_length.isEnabled() == expected_enabled
        assert widget.snap_distance.isEnabled() == expected_enabled


class TestConnectNodeSettings:
    def test_defaults(self, qgis_application):
        widget = ConnectionNodeSettingsWidget()
        model = ConnectionNodeSettingsModel()
        assert widget.create_nodes.isChecked() == model.create_nodes
        assert widget.snap.isChecked() == model.snap
        assert widget.snap_distance.value() == model.snap_distance

    def test_deserialize(self, qgis_application):
        widget = ConnectionNodeSettingsWidget()
        settings = {"create_nodes": True, "snap": False, "snap_distance": 10.5}
        widget.deserialize(settings)
        assert widget.create_nodes.isChecked() == settings["create_nodes"]
        assert widget.snap.isChecked() == settings["snap"]
        assert widget.snap_distance.value() == settings["snap_distance"]

    def test_serialize(self, qgis_application):
        widget = ConnectionNodeSettingsWidget()
        settings = {"create_nodes": True, "snap": False, "snap_distance": 10.5}
        widget.deserialize(settings)
        assert widget.serialize() == settings

    @pytest.mark.parametrize("create_nodes", [True, False])
    def test_toggle_snap(self, create_nodes, qgis_application):
        widget = ConnectionNodeSettingsWidget()
        widget.deserialize({"create_nodes": create_nodes})
        assert widget.snap.isEnabled() == create_nodes

    @pytest.mark.parametrize("snap_enabled", [True, False])
    def test_toggle_snap_distance(self, snap_enabled, qgis_application):
        widget = ConnectionNodeSettingsWidget()
        widget.deserialize({"snap": snap_enabled})
        assert widget.snap_distance.isEnabled() == snap_enabled
