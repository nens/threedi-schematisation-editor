import json
from functools import cached_property
from pathlib import Path
from typing import Any, Optional, Type

from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox, QWidget, QWizard, QWizardPage

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import create_font
from threedi_schematisation_editor.vector_data_importer.wizard.pages import (
    FieldMapPage,
    RunPage,
    SettingsPage,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    CrossSectionDataRemapSettingsWidget,
    CrossSectionLocationMappingSettingsWidget,
    IntegrationSettingsWidget,
    PointToLIneConversionSettingsWidget,
)


class VDIWizard(QWizard):
    def __init__(
        self,
        model_cls: Type,
        model_gpkg: str,
        layer_manager: Any,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.model_cls = model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.setup_ui()
        self.setOption(QWizard.NoCancelButton, True)

    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__tablename__.lower()}s"

    @cached_property
    def settings_page(self):
        return SettingsPage()

    @cached_property
    def field_map_page(self):
        return FieldMapPage(model_cls=self.model_cls, name="fields")

    @cached_property
    def connection_node_pages(self):
        return []

    @cached_property
    def run_page(self):
        return RunPage()

    def setup_ui(self):
        # set appearance
        font = create_font(self, 10)
        self.setFont(font)
        self.setWindowTitle(self.wizard_title)
        # TODO is this the right size?
        self.resize(1000, 750)

        # add pages
        self.addPage(self.settings_page)
        if self.field_map_page:
            self.addPage(self.field_map_page)
        for page in self.connection_node_pages:
            self.addPage(page)
        self.addPage(self.run_page)

    @property
    def selected_layer(self):
        return self.settings_page.generic_settings.selected_layer

    def load_settings_from_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Settings", str(Path.home()), "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, "r") as f:
                settings = json.load(f)
            # Get the wizard instance and its pages
            try:
                self.deserialize(settings)
                QMessageBox.information(
                    self, "Success", "Settings loaded successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to load settings: {str(e)}"
                )

    def deserialize(self, data):
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, "deserialize"):
                page.deserialize(data)

    def save_settings_to_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Settings", str(Path.home()), "JSON Files (*.json)"
        )
        if file_path:
            try:
                settings = self.serialize()
                with open(file_path, "w") as f:
                    json.dump(settings, f, indent=4)
                QMessageBox.information(self, "Success", "Settings saved successfully!")
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to save settings: {str(e)}"
                )

    def serialize(self):
        data = {}
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, "serialize"):
                data.update(page.serialize())
        return data


class ImportWithCreateConnectionNodesWizard(VDIWizard):
    @cached_property
    def connection_node_pages(self):
        return [
            FieldMapPage(model_cls=dm.ConnectionNode, name="connection_node_fields")
        ]

    @property
    def connect_node_page_ids(self):
        return [
            id for id in self.pageIds() if self.page(id) in self.connection_node_pages
        ]

    def nextId(self):
        next_id = super().nextId()
        # If there's no next page, return -1 (standard Qt behavior)
        if next_id == -1:
            return next_id
        # If no connection nodes are added, skip settings for connection nodes
        if not self.settings_page.create_nodes:
            while next_id in self.connect_node_page_ids:
                next_id += 1
        return next_id


class ImportConduitWizard(ImportWithCreateConnectionNodesWizard):
    @cached_property
    def settings_page(self):
        return SettingsPage(
            settings_widgets=[ConnectionNodeSettingsWidget],
        )


class ImportStructureWizard(ImportWithCreateConnectionNodesWizard):
    @cached_property
    def settings_page(self):
        return SettingsPage(
            [
                ConnectionNodeSettingsWidget,
                PointToLIneConversionSettingsWidget,
                IntegrationSettingsWidget,
            ]
        )


class ImportCrossSectionDataWizard(VDIWizard):
    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__tablename__.lower()}"

    @cached_property
    def settings_page(self):
        return SettingsPage([CrossSectionDataRemapSettingsWidget])


class ImportCrossSectionLocationWizard(VDIWizard):
    @cached_property
    def settings_page(self):
        return SettingsPage([CrossSectionLocationMappingSettingsWidget])
