import json
import traceback
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, ValidationError
from qgis.core import Qgis, QgsMapLayerProxyModel, QgsMessageLog, QgsProject
from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal
from qgis.PyQt.QtGui import QPalette
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
import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.utils import (
    CancellationToken,
    compute_selected_ids,
)
from threedi_schematisation_editor.vector_data_importer.wizard.pages import (
    FieldMapPage,
    RunPage,
    SettingsPage,
    StartPage,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    CrossSectionDataRemapSettingsWidget,
    CrossSectionLocationMappingSettingsWidget,
    IntegrationSettingsWidget,
    PointToLIneConversionSettingsWidget,
    SettingsWidget,
    SurfaceLinkingSettingsWidget,
)
from threedi_schematisation_editor.vector_data_importer.wizard.utils import (
    CatchThreediWarnings,
    create_font,
    delete_draft,
    get_draft,
    get_last_config_dir,
    save_draft,
    update_last_config_dir,
)


class ImportWorker(QObject):
    progress = pyqtSignal(dict)
    finished = pyqtSignal(bool, str, str, str)  # message, success

    def __init__(self, callable_func, cancellation_token):
        super().__init__()
        self.callable_func = callable_func
        self.cancellation_token = cancellation_token

    def handle_progress(self, value=None, add=None, maximum=None):
        self.progress.emit({"value": value, "add": add, "maximum": maximum})

    def run(self):
        error_msg = ""
        try:
            with CatchThreediWarnings() as warnings_catcher:
                # Import features with warning catching
                self.callable_func(progress_callback=self.handle_progress)
            if self.cancellation_token.was_interrupted:
                status_msg = "Import was cancelled.\n"
            else:
                status_msg = "Import completed successfully.\n"
            success = True
        except Exception as e:
            status_msg = "Import failed with traceback:"
            error_msg = f"{traceback.format_exc()}"
            success = False
        warning_msg = warnings_catcher.warnings_msg
        self.finished.emit(success, status_msg, warning_msg, error_msg)


class VDIWizard(QWizard):
    IMPORTERS = {
        dm.ConnectionNode: vdi_importers.ConnectionNodesImporter,
        dm.Culvert: vdi_importers.CulvertsImporter,
        dm.Orifice: vdi_importers.OrificesImporter,
        dm.Weir: vdi_importers.WeirsImporter,
        dm.Pipe: vdi_importers.PipesImporter,
        dm.Channel: vdi_importers.ChannelsImporter,
        dm.CrossSectionLocation: vdi_importers.CrossSectionLocationImporter,
        dm.Surface: vdi_importers.SurfaceImporter,
    }
    settings_widgets_classes: list[SettingsWidget] = []
    import_started = pyqtSignal()
    import_finished = pyqtSignal()

    def __init__(
        self,
        model_cls: Type[dm.ModelObject],
        model_gpkg: str,
        layer_manager: Any,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.model_cls = model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self._import_succeeded = False
        self._draft_restore_offered = False
        self.setup_ui()
        try:
            self._initial_state = self.serialize()
        except Exception:
            self._initial_state = None
        self._initial_draft = self.get_draft_settings()

    def showEvent(self, event):
        super().showEvent(event)
        if not self._draft_restore_offered:
            self._draft_restore_offered = True
            self.offer_draft_restore()

    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__layername__.lower()}s"

    @property
    def layer_filter(self) -> Optional[QgsMapLayerProxyModel]:
        return None

    @cached_property
    def settings_page(self):
        return SettingsPage(
            settings_widgets_classes=self.settings_widgets_classes,
        )

    @cached_property
    def field_map_page(self):
        return FieldMapPage(model_cls=self.model_cls, name="fields")

    @cached_property
    def extra_field_map_pages(self):
        return []

    @cached_property
    def run_page(self):
        return RunPage()

    @cached_property
    def start_page(self):
        return StartPage(layer_filter=self.layer_filter)

    def setup_ui(self):
        # set appearance
        font = create_font(self, 10)
        self.setFont(font)
        self.setWindowTitle(self.wizard_title)
        self.resize(1000, 750)
        # add pages
        self.addPage(self.start_page)
        if len(self.settings_widgets_classes) > 0:
            settings_page = SettingsPage(
                settings_widgets_classes=self.settings_widgets_classes,
            )
            self.addPage(self.settings_page)
        if self.field_map_page:
            self.addPage(self.field_map_page)
        for page in self.extra_field_map_pages:
            self.addPage(page)
        self.addPage(self.run_page)
        # Connect import start and finish signals
        self.import_started.connect(self.run_page.on_run_start)
        self.import_started.connect(lambda: self.set_enabled_nav(False))
        self.import_finished.connect(self.run_page.on_run_finish)
        self.import_finished.connect(lambda: self.set_enabled_nav(True))
        # Rename buttons
        self.setButtonText(self.CancelButton, "Close")
        self.setButtonText(self.FinishButton, "Run import")
        # set up button to run import
        self.finish_button = self.button(self.FinishButton)
        self.finish_button.clicked.disconnect()
        self.finish_button.clicked.connect(self.run_import)
        # Use the same background as standard widgets
        palette = self.palette()
        base_color = palette.color(
            QPalette.Window
        )  # This matches other widgets' gray background
        palette.setColor(QPalette.Base, base_color)
        self.setPalette(palette)
        # Explicitly set wizard style
        self.setWizardStyle(QWizard.ClassicStyle)

    @property
    def selected_layer(self):
        return self.start_page.layer_settings_widget.selected_layer

    @property
    def use_selected_features(self) -> bool:
        return self.start_page.use_selected_features

    def load_settings_from_json(self) -> Optional[str]:
        # Future: take this outside of the wizard so that the processing
        # algorithms can also use the validation
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Settings", get_last_config_dir(), "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, "r") as f:
                try:
                    json_settings = json.load(f)
                except json.JSONDecodeError as e:
                    QMessageBox.critical(
                        self, "Error", f"File {file_path} is not a valid JSON file"
                    )
                    QgsMessageLog.logMessage(
                        f"Cannot read file {file_path}: {e}",
                        "Warning",
                        Qgis.Warning,
                    )
                    return
            update_last_config_dir(file_path)
            # Get the wizard instance and its pages
            try:
                settings = sm.ImportSettings(**json_settings)
                self.deserialize(settings.model_dump())
                try:
                    self._initial_state = self.serialize()
                except Exception:
                    pass
                QMessageBox.information(
                    self, "Success", "Settings loaded successfully!"
                )
                return file_path
            except ValidationError as e:
                msg = "The following errors occurred while loading the settings:"
                for error in e.errors():
                    field_info = ".".join(error["loc"])
                    if error["type"] != "missing":
                        field_info += f" = {error['input']}"
                    msg += f"\n{error['msg']}: {field_info}"
                    QgsMessageLog.logMessage(f"{e}", "Warning", Qgis.Warning)
                QMessageBox.critical(self, "Error", msg)
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Could not load settings from {file_path}"
                )
                QgsMessageLog.logMessage(f"{e}", "Warning", Qgis.Warning)

    def deserialize(self, data):
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, "deserialize"):
                page.deserialize(data)

    def save_settings_to_json(self) -> Optional[str]:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Settings", get_last_config_dir(), "JSON Files (*.json)"
        )
        if file_path:
            update_last_config_dir(file_path)
            if Path(file_path).suffix != ".json":
                file_path += ".json"
            try:
                settings = self.get_settings().model_dump()
                with open(file_path, "w") as f:
                    json.dump(settings, f, indent=4)
                QMessageBox.information(self, "Success", "Settings saved successfully!")
                delete_draft(type(self).__name__)
                return file_path
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to save settings: {str(e)}"
                )

    def serialize(self):
        return self.get_settings().model_dump()

    def get_draft_settings(self):
        data = {}
        for page_id in self.pageIds():
            page = self.page(page_id)
            if isinstance(page, StartPage):
                source_settings = page.get_settings().get("source")
                if source_settings is not None:
                    data["source"] = (
                        source_settings.model_dump()
                        if hasattr(source_settings, "model_dump")
                        else source_settings
                    )
            elif isinstance(page, FieldMapPage):
                data[page.name] = {
                    key: row.config.model_dump()
                    for key, row in page.field_map_widget.row_dict.items()
                    if row.is_valid
                }
            elif isinstance(page, SettingsPage):
                for key, value in page.get_settings().items():
                    data[key] = (
                        value.model_dump() if hasattr(value, "model_dump") else value
                    )
        return data

    @property
    def has_changes(self):
        try:
            current = self.serialize()
        except Exception:
            # serialize() raises when field map rows are incomplete — compare
            # raw draft data against the initial snapshot instead.
            return self.get_draft_settings() != self._initial_draft
        if self._initial_state is None:
            return False
        return current != self._initial_state

    def reject(self):
        if self._import_succeeded:
            delete_draft(type(self).__name__)
            super().reject()
            return
        if not self.has_changes:
            super().reject()
            return
        msg = QMessageBox(self)
        msg.setWindowTitle("Unsaved import settings")
        msg.setText(
            "You have unsaved import settings. Do you want to save them as draft to reuse in a later import of the same type?"
        )
        msg.setStandardButtons(
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        msg.button(QMessageBox.Save).setText("Save draft")
        result = msg.exec_()
        if result == QMessageBox.Save:
            save_draft(type(self).__name__, self.get_draft_settings())
            super().reject()
        elif result == QMessageBox.Discard:
            super().reject()
        # Cancel: do nothing, wizard stays open

    def restore_draft_lenient(self, data):
        for page_id in self.pageIds():
            page = self.page(page_id)
            if hasattr(page, "deserialize"):
                try:
                    page.deserialize(data)
                except Exception:
                    pass

    def offer_draft_restore(self):
        draft = get_draft(type(self).__name__)
        if draft is None:
            return
        msg = QMessageBox(self)
        msg.setWindowTitle("Draft import configuration found")
        msg.setText(
            "A previous import configuration was found for this import type. Do you want to restore these settings?"
        )
        msg.setStandardButtons(QMessageBox.RestoreDefaults | QMessageBox.Cancel)
        msg.button(QMessageBox.RestoreDefaults).setText("Restore draft")
        msg.button(QMessageBox.Cancel).setText("Start fresh")
        result = msg.exec_()
        if result == QMessageBox.RestoreDefaults:
            self.restore_draft_lenient(draft)
            self._initial_draft = self.get_draft_settings()

    def should_collect_page(self, page):
        """Return False to skip collecting settings from a FieldMapPage.

        Subclasses override this to implement conditional-skip logic without
        hardcoding page names in the base class.
        """
        return True

    def get_settings(self) -> BaseModel:
        data = {}
        for page_id in self.pageIds():
            page = self.page(page_id)
            if isinstance(page, FieldMapPage) and not self.should_collect_page(page):
                continue
            if isinstance(page, (StartPage, FieldMapPage, SettingsPage)):
                data.update(page.get_settings())

        return sm.ImportSettings(**data)

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        """Collect layer handlers and map associated layers to dict needed for the importer"""
        handler = self.layer_manager.model_handlers[self.model_cls]
        return [handler], {"target_layer": handler.layer}

    def get_importer(self, import_settings: sm.ImportSettings, layer_dict):
        return self.IMPORTERS[self.model_cls](
            self.selected_layer,
            self.model_gpkg,
            import_settings,
            **layer_dict,
        )

    def set_enabled_nav(self, enabled):
        buttons = [
            self.NextButton,
            self.BackButton,
            self.CancelButton,
            self.FinishButton,
        ]
        for button in buttons:
            self.button(button).setEnabled(enabled)

    def _compute_feature_ids(self, source_settings):
        return compute_selected_ids(self.selected_layer, source_settings)

    def run_import(self):
        self.import_started.emit()
        progress_bar = self.run_page.progress_bar
        settings = self.get_settings()
        selected_feat_ids = self._compute_feature_ids(settings.source)
        handlers, layers = self.prepare_import()
        for handler in handlers:
            handler.disconnect_handler_signals()

        importer = self.get_importer(settings, layers)

        # Connect cancel button
        cancellation_token = CancellationToken()
        self.run_page.cancel_requested.connect(cancellation_token.cancel)
        importer.processor._cancellation_token = cancellation_token
        if isinstance(importer, vdi_importers.IntegrationImporter) and importer.integrator:
            importer.integrator._cancellation_token = cancellation_token

        # Setup worker and thread
        import_callable = lambda progress_callback: importer.import_features(
            selected_ids=selected_feat_ids, progress_callback=progress_callback
        )
        self.thread = QThread()
        self.worker = ImportWorker(import_callable, cancellation_token)
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Connect progress updates
        def update_progress(progress_dict):
            if progress_dict["maximum"] is not None:
                progress_bar.setMaximum(progress_dict["maximum"])
            if progress_dict["value"] is not None:
                progress_bar.setValue(progress_dict["value"])
            elif progress_dict["add"]:
                progress_bar.setValue(progress_bar.value() + progress_dict["add"])

        self.worker.progress.connect(update_progress)

        # Connect finish handling
        def handle_finished(success, status_msg, warning_msg, error_msg):
            self._import_succeeded = success
            if not success:
                progress_bar.set_failed()
            error_color = "#FF0000"
            warning_color = "#FFA500"
            self.run_page.update_log(
                status_msg, fg_color=error_color if not success else None
            )
            self.run_page.update_log(error_msg)
            self.run_page.update_log(warning_msg, fg_color=warning_color)
            final_msg = (
                "\nThe layers to which data has been added are still in editing mode, "
                "so you can review the changes before saving them to the layers."
            )
            self.run_page.update_log(final_msg)
            self.run_page.cancel_button.setEnabled(False)
            for handler in handlers:
                handler.connect_handler_signals()
                handler.layer.triggerRepaint()
            self.import_finished.emit()
            if success:
                self.button(self.CancelButton).setFocus()

        self.worker.finished.connect(handle_finished)

        # Start thread
        self.thread.start()


class ImportWithCreateConnectionNodesWizard(VDIWizard):
    @cached_property
    def extra_field_map_pages(self):
        return [
            FieldMapPage(model_cls=dm.ConnectionNode, name="connection_node_fields")
        ]

    @property
    def extra_field_map_page_ids(self):
        return [
            id for id in self.pageIds() if self.page(id) in self.extra_field_map_pages
        ]

    def should_collect_page(self, page):
        if isinstance(page, FieldMapPage) and page.name == "connection_node_fields":
            return self.settings_page.create_nodes
        return True

    def nextId(self):
        next_id = super().nextId()
        # If there's no next page, return -1 (standard Qt behavior)
        if next_id == -1:
            return next_id
        # If no connection nodes are added, skip settings for connection nodes
        if not self.settings_page.create_nodes:
            while next_id in self.extra_field_map_page_ids:
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


class ImportConnectionNodesWizard(VDIWizard):
    @property
    def layer_filter(self) -> QgsMapLayerProxyModel.Filter:
        return QgsMapLayerProxyModel.PointLayer


class ImportConduitWizard(ImportWithCreateConnectionNodesWizard):
    settings_widgets_classes = [ConnectionNodeSettingsWidget]

    @property
    def layer_filter(self) -> QgsMapLayerProxyModel.Filter:
        """Set the filter for the source layer combo box based on the model's geometry type."""
        return (
            QgsMapLayerProxyModel.PointLayer
            if self.model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )


class ImportStructureWizard(ImportWithCreateConnectionNodesWizard):
    settings_widgets_classes = [
        ConnectionNodeSettingsWidget,
        PointToLIneConversionSettingsWidget,
        IntegrationSettingsWidget,
    ]

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        processed_handlers, processed_layers = super().prepare_import()
        integration_settings = self.get_settings().integration
        if integration_settings.integration_mode == sm.IntegrationMode.CHANNELS:
            conduit_handler = self.layer_manager.model_handlers[dm.Channel]
            cross_section_location_handler = self.layer_manager.model_handlers[
                dm.CrossSectionLocation
            ]
            processed_handlers += [conduit_handler, cross_section_location_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
            processed_layers["cross_section_location_layer"] = (
                cross_section_location_handler.layer
            )
        elif integration_settings.integration_mode == sm.IntegrationMode.PIPES:
            conduit_handler = self.layer_manager.model_handlers[dm.Pipe]
            processed_handlers += [conduit_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
        return processed_handlers, processed_layers

    @property
    def layer_filter(self) -> QgsMapLayerProxyModel.Filter:
        """Set the filter for the source layer combo box based on the model's geometry type."""
        return (
            QgsMapLayerProxyModel.PointLayer
            if self.model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )


class ImportCrossSectionDataWizard(VDIWizard):
    settings_widgets_classes = [CrossSectionDataRemapSettingsWidget]

    @property
    def wizard_title(self):
        return f"Import {self.model_cls.__layername__}"

    @cached_property
    def field_map_page(self):
        return FieldMapPage(
            model_cls=self.model_cls,
            name="fields",
            title_suffix="schematisation objects",
        )

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

    @property
    def layer_filter(self) -> Optional[QgsMapLayerProxyModel]:
        return (
            QgsMapLayerProxyModel.LineLayer
            | QgsMapLayerProxyModel.PointLayer
            | QgsMapLayerProxyModel.NoGeometry
        )


class ImportCrossSectionLocationWizard(VDIWizard):
    settings_widgets_classes = [CrossSectionLocationMappingSettingsWidget]

    @property
    def layer_filter(self) -> QgsMapLayerProxyModel.Filter:
        return (
            QgsMapLayerProxyModel.LineLayer
            | QgsMapLayerProxyModel.PointLayer
            | QgsMapLayerProxyModel.NoGeometry
        )


class ImportSurfaceWizard(VDIWizard):
    settings_widgets_classes = [
        SurfaceLinkingSettingsWidget,
    ]

    @cached_property
    def extra_field_map_pages(self):
        return [FieldMapPage(model_cls=dm.SurfaceMap, name="surface_map_fields")]

    @property
    def extra_field_map_page_ids(self):
        return [
            id for id in self.pageIds() if self.page(id) in self.extra_field_map_pages
        ]

    @property
    def _is_long_format(self):
        return (
            self.settings_page.get_settings()["surface_linking"].data_format == "long"
        )

    def should_collect_page(self, page):
        if isinstance(page, FieldMapPage) and page.name == "surface_map_fields":
            return self._is_long_format
        return True

    def nextId(self):
        next_id = super().nextId()
        if next_id == -1:
            return next_id
        if not self._is_long_format:
            while next_id in self.extra_field_map_page_ids:
                next_id += 1
        return next_id

    @property
    def layer_filter(self) -> QgsMapLayerProxyModel.Filter:
        return QgsMapLayerProxyModel.PolygonLayer

    def prepare_import(self):
        surface_handler = self.layer_manager.model_handlers[dm.Surface]
        surface_map_handler = self.layer_manager.model_handlers[dm.SurfaceMap]
        handlers = [surface_handler, surface_map_handler]
        layers = {
            "surface_layer": surface_handler.layer,
            "surface_map_layer": surface_map_handler.layer,
        }
        return handlers, layers

    def get_importer(self, import_settings: sm.ImportSettings, layer_dict):
        selected_pipes_only = import_settings.surface_linking.selected_pipes_only
        return vdi_importers.SurfaceImporter(
            self.selected_layer,
            self.model_gpkg,
            import_settings,
            selected_pipes_only=selected_pipes_only,
            **layer_dict,
        )
