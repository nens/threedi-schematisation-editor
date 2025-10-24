import json
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel
from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QWidget,
    QWizard,
    QWizardPage,
)

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.vector_data_importer.importers as vdi_importers
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import (
    CatchThreediWarnings,
    create_font,
)
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    IntegrationMode,
)
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
    IMPORTERS = {
        dm.ConnectionNode: vdi_importers.ConnectionNodesImporter,
        dm.Culvert: vdi_importers.CulvertsImporter,
        dm.Orifice: vdi_importers.OrificesImporter,
        dm.Weir: vdi_importers.WeirsImporter,
        dm.Pipe: vdi_importers.PipesImporter,
        dm.Channel: vdi_importers.ChannelsImporter,
        dm.CrossSectionLocation: vdi_importers.CrossSectionLocationImporter,
    }

    def __init__(
        self,
        model_cls: Type,
        model_gpkg: str,
        layer_manager: Any,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.import_finished = False
        self.model_cls = model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.setup_ui()
        self.setOption(QWizard.NoCancelButton, True)

    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__layername__.lower()}s"

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
        self.currentIdChanged.connect(self.handle_page_change)
        self.map_finish_button()

    def map_finish_button(self):
        if self.import_finished:
            self.setButtonText(self.FinishButton, "Finish")
            finish_button = self.button(self.FinishButton)
            finish_button.clicked.disconnect()
            finish_button.clicked.connect(self.accept)  # accept() will close the dialog
        else:
            self.setButtonText(self.FinishButton, "Run")
            finish_button = self.button(self.FinishButton)
            finish_button.clicked.disconnect()
            finish_button.clicked.connect(self.run_import)

    def handle_page_change(self, _):
        # Reset import_finished if we navigate to any page
        if self.import_finished:
            self.import_finished = False
            self.map_finish_button()

    @property
    def selected_layer(self):
        return self.settings_page.generic_settings.selected_layer

    @property
    def use_selected_features(self) -> bool:
        return self.settings_page.generic_settings.model.selected_layer

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

    def get_settings(self) -> dict[str, Any]:
        data = {}
        for page_id in self.pageIds():
            page = self.page(page_id)
            if callable(getattr(page, "get_settings", None)):
                data.update(page.get_settings())
        return data

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        """Collect layer handlers and map associated layers to dict needed for the importer"""
        handler = self.layer_manager.model_handlers[self.model_cls]
        return [handler], {"target_layer": handler.layer}

    def get_importer(self, import_settings: dict, layer_dict):
        return self.IMPORTERS[self.model_cls](
            self.selected_layer,
            self.model_gpkg,
            import_settings,
            **layer_dict,
        )

    def run_import(self):
        text_output = self.run_page.text
        text_output.insertPlainText("Process settings")
        settings = self.get_settings()
        selected_feat_ids = (
            self.selected_layer.selectedFeatureIds()
            if self.use_selected_features
            else None
        )

        # depends on model iirc
        handlers, layers = self.prepare_import()
        text_output.appendPlainText(f"Load source and target layers")
        # needs settings and selected layer

        try:
            text_output.appendPlainText("Disconnect layer handler signals:")
            for handler in handlers:
                text_output.appendPlainText(f"\t- {handler.layer.name()}")
                handler.disconnect_handler_signals()
            # depends on model
            text_output.appendPlainText(f"Initialize importer")
            importer = self.get_importer(settings, layers)
            # put warnings in text box
            with CatchThreediWarnings() as warnings_catcher:
                importer.import_features(selected_ids=selected_feat_ids)
            result_msg = (
                "Import completed successfully.\n"
                "The layers to which the data has been added are still in editing mode, "
                "so you can review the changes before saving them to the layers."
                f"{warnings_catcher.warnings_msg}"
            )
            # QMessageBox.information(self, "Success", success_msg)
            self.import_finished = True
        except Exception as e:
            self.import_finished = False
            result_msg = f"Import failed with traceback:\n{traceback.format_exc()}"
            # QMessageBox.information(self, "Failure", f"Import failed due to the following error:\n{e}",)
            QgsMessageLog.logMessage(
                f"Import failed with traceback:\n{traceback.format_exc()}",
                "Warning",
                Qgis.Warning,
            )
        finally:
            text_output.appendPlainText("Reconnect layer handler signals:")
            for handler in handlers:
                text_output.appendPlainText(f"\t- {handler.layer.name()}")
                handler.connect_handler_signals()
        text_output.appendPlainText("Repaint layers:")
        for handler in handlers:
            text_output.appendPlainText(f"\t- {handler.layer.name()}")
            handler.layer.triggerRepaint()
        text_output.appendPlainText(f"{result_msg}")
        self.map_finish_button()


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

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        structures_handler = self.layer_manager.model_handlers[self.model_cls]
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        processed_handlers = [structures_handler, node_handler]
        processed_layers = {
            "structure_layer": structures_handler.layer,
            "node_layer": node_handler.layer,
        }
        return processed_handlers, processed_layers


class ImportConduitWizard(ImportWithCreateConnectionNodesWizard):
    @cached_property
    def settings_page(self):
        return SettingsPage(
            settings_widgets=[ConnectionNodeSettingsWidget],
        )


class ImportStructureWizard(ImportWithCreateConnectionNodesWizard):
    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        processed_handlers, processed_layers = super().prepare_import()
        settings = self.get_settings().get("integration")
        if not settings:
            return processed_handlers, processed_layers
        if settings.integration_mode == IntegrationMode.CHANNELS:
            conduit_handler = self.layer_manager.model_handlers[dm.Channel]
            cross_section_location_handler = self.layer_manager.model_handlers[
                dm.CrossSectionLocation
            ]
            processed_handlers += [conduit_handler, cross_section_location_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
            processed_layers["cross_section_location_layer"] = (
                cross_section_location_handler.layer
            )
        elif settings.integration_mode == IntegrationMode.PIPES:
            conduit_handler = self.layer_manager.model_handlers[dm.Pipe]
            processed_handlers += [conduit_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
        return processed_handlers, processed_layers

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
        return f"Import {self.model_cls.__layername__}"

    @cached_property
    def settings_page(self):
        return SettingsPage([CrossSectionDataRemapSettingsWidget])

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        handlers = [
            self.layer_manager.model_handlers[model_cls]
            for model_cls in vdi_importers.CrossSectionDataProcessor.target_models
        ]
        layer_dict = {handler.layer.name(): handler.layer for handler in handlers}
        return handlers, layer_dict

    def get_importer(self, import_settings, layer_dict):
        return vdi_importers.CrossSectionDataImporter(
            self.selected_layer,
            self.model_gpkg,
            import_settings,
            list(layer_dict.values()),
        )


class ImportCrossSectionLocationWizard(VDIWizard):
    @cached_property
    def settings_page(self):
        return SettingsPage([CrossSectionLocationMappingSettingsWidget])
