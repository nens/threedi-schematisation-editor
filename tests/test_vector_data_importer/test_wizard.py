import pytest

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ConnectionNodeSettingsModel,
)
from threedi_schematisation_editor.vector_data_importer.wizard import VDIWizard
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
)


def test_wizard(qgis_application):
    wizard = VDIWizard(dm.ConnectionNode, None, None)
    wizard.serialize()


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
