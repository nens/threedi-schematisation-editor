from functools import cached_property
from typing import Any, Optional, Type

from qgis.PyQt.QtWidgets import QWidget, QWizard, QWizardPage

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import create_font
from threedi_schematisation_editor.vector_data_importer.importers import (
    ConnectionNodesImporter,
)
from threedi_schematisation_editor.vector_data_importer.wizard.pages import (
    FieldMapPage,
    RunPage,
    SettingsPage,
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

    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__tablename__.lower()}s"

    @cached_property
    def settings_page(self):
        return SettingsPage()

    @cached_property
    def field_map_page(self):
        return FieldMapPage(self.model_cls)

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


class ImportStructureWizard(VDIWizard):
    @cached_property
    def connection_node_pages(self):
        return [FieldMapPage(dm.ConnectionNode)]

    @cached_property
    def settings_page(self):
        return SettingsPage(
            connection_node_settings=True,
            point_to_line_conversion=True,
            integration_settings=True,
        )

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


class ImportCrossSectionData(VDIWizard):
    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__tablename__.lower()}"
