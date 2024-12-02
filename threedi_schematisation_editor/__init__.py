# Copyright (C) 2023 by Lutra Consulting
import os.path
from collections import defaultdict
from pathlib import Path

from qgis.core import QgsApplication, QgsLayerTreeNode, QgsProject
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QAction, QComboBox, QDialog, QMenu
from threedi_mi_utils.news import QgsNewsSettingsInjector

PLUGIN_DIR = Path(__file__).parent

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.communication import UICommunication
from threedi_schematisation_editor.conversion import ModelDataConverter
from threedi_schematisation_editor.custom_widgets import (
    ImportStructuresDialog, LoadSchematisationDialog)
from threedi_schematisation_editor.processing import \
    ThreediSchematisationEditorProcessingProvider
from threedi_schematisation_editor.user_layer_manager import LayersManager
from threedi_schematisation_editor.utils import (ConversionError,
                                                 add_gpkg_connection,
                                                 add_settings_entry,
                                                 can_write_in_dir,
                                                 check_enable_macros_option,
                                                 create_empty_model,
                                                 ensure_valid_schema,
                                                 get_filepath,
                                                 is_gpkg_connection_exists,
                                                 remove_user_layers)
from threedi_schematisation_editor.workspace import WorkspaceContextManager

from .deps.custom_imports import patch_wheel_imports


def classFactory(iface):
    return ThreediSchematisationEditorPlugin(iface)


class ThreediSchematisationEditorPlugin:
    PLUGIN_NAME = "3Di Schematisation Editor"
    THREEDI_GPKG_VAR_NAMES = "threedi_gpkg_var"

    def __init__(self, iface):
        self.iface = iface
        self.uc = UICommunication(self.iface, self.PLUGIN_NAME)
        self.active_schematisation_combo = None
        self.toolbar = None
        self.action_open = None
        self.action_import = None
        self.action_export = None
        self.action_export_as = None
        self.action_remove = None
        self.action_import_culverts = None
        self.workspace_context_manager = WorkspaceContextManager(self)
        self.provider = ThreediSchematisationEditorProcessingProvider()
        self.project = QgsProject.instance()
        self.project.removeAll.connect(self.on_project_close)
        self.project.readProject.connect(self.on_3di_project_read)
        self.project.projectSaved.connect(self.on_3di_project_save)
        self.iface.currentLayerChanged.connect(self.switch_workspace_context)

        patch_wheel_imports()
        # Inject custom news entries in settings
        QgsNewsSettingsInjector().load(PLUGIN_DIR / "news_feed.json")

    def initGui(self):
        QgsApplication.processingRegistry().addProvider(self.provider)
        self.toolbar = self.iface.addToolBar("Schematisation Editor")
        self.active_schematisation_combo = QComboBox()
        self.active_schematisation_combo.setMinimumWidth(250)
        self.active_schematisation_combo.setPlaceholderText("No active schematisation")
        self.active_schematisation_combo.currentIndexChanged.connect(self.active_schematisation_changed)
        self.toolbar.addWidget(self.active_schematisation_combo)
        self.toolbar.addSeparator()
        self.action_open = QAction("Open 3Di Geopackage", self.iface.mainWindow())
        self.action_open.triggered.connect(self.open_model_from_geopackage)
        self.action_import = QAction("Load from Spatialite", self.iface.mainWindow())
        self.action_import.triggered.connect(self.load_from_spatialite)
        self.action_export = QAction("Save to Spatialite", self.iface.mainWindow())
        self.action_export.triggered.connect(self.save_to_default)
        self.action_export_as = QAction("Save As", self.iface.mainWindow())
        self.action_export_as.triggered.connect(self.save_to_selected)
        self.action_remove = QAction("Remove 3Di model", self.iface.mainWindow())
        self.action_remove.triggered.connect(self.remove_model_from_project)
        import_culverts_icon_path = os.path.join(os.path.dirname(__file__), "import.png")
        import_actions_spec = [
            ("Culverts", self.import_external_culverts, None),
            ("Orifices", self.import_external_orifices, None),
            ("Weirs", self.import_external_weirs, None),
            ("Pipes", self.import_external_pipes, None),
            ("Manholes", self.import_external_manholes, None),
        ]
        self.action_import_culverts = self.add_multi_action_button(
            "Import schematisation objects", import_culverts_icon_path, import_actions_spec
        )
        self.toolbar.addAction(self.action_open)
        self.toolbar.addAction(self.action_import)
        self.toolbar.addAction(self.action_export)
        self.toolbar.addAction(self.action_export_as)
        self.toolbar.addAction(self.action_remove)
        self.toolbar.addAction(self.action_import_culverts)
        self.toggle_active_project_actions()
        self.active_schematisation_changed()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.active_schematisation_combo.currentIndexChanged.disconnect(self.active_schematisation_changed)
        del self.toolbar
        del self.active_schematisation_combo
        del self.action_open
        del self.action_import
        del self.action_export
        del self.action_export_as
        del self.action_remove
        del self.action_import_culverts

    @property
    def model_gpkg(self):
        return self.workspace_context_manager.active_layer_manager_geopackage

    @property
    def layer_manager(self):
        return self.workspace_context_manager.active_layer_manager

    @property
    def model_layers_map(self):
        model_layers = defaultdict(set)
        root_node = QgsProject.instance().layerTreeRoot()
        model_nodes = [
            node
            for node in root_node.children()
            if node.nodeType() == QgsLayerTreeNode.NodeType.NodeGroup and node.name().startswith("3Di schematisation:")
        ]
        for model_node in model_nodes:
            model_groups = {
                node.name(): node
                for node in model_node.children()
                if node.nodeType() == QgsLayerTreeNode.NodeType.NodeGroup
            }
            try:
                group_1d_node = model_groups["1D"]
            except KeyError:
                continue
            layer_1d_nodes = {
                node.name(): node
                for node in group_1d_node.children()
                if node.nodeType() == QgsLayerTreeNode.NodeType.NodeLayer
            }
            connection_node_tree_layer = layer_1d_nodes[dm.ConnectionNode.__layername__]
            if connection_node_tree_layer is None:
                continue
            connection_node_layer = connection_node_tree_layer.layer()
            model_gpkg = os.path.normpath(connection_node_layer.source().rsplit("|", 1)[0])
            for sub_grp in model_groups.values():
                for nested_node in sub_grp.children():
                    if nested_node.nodeType() == QgsLayerTreeNode.NodeType.NodeLayer:
                        model_layer = nested_node.layer()
                        model_layers[model_gpkg].add(model_layer.id())
        return model_layers

    def switch_workspace_context(self, active_layer):
        if not active_layer:
            return
        expected_layer_source = os.path.normpath(active_layer.source().rsplit("|", 1)[0])
        if active_layer.id() in self.model_layers_map[expected_layer_source]:
            try:
                lm = self.workspace_context_manager.layer_managers[expected_layer_source]
            except KeyError:
                return
            if lm.model_gpkg_path != self.model_gpkg:
                self.workspace_context_manager.set_active_layer_manager(lm)

    def active_schematisation_changed(self):
        combo_model_gpkg = self.active_schematisation_combo.currentData()
        if self.model_gpkg != combo_model_gpkg:
            lm = self.workspace_context_manager.layer_managers[combo_model_gpkg]
            self.iface.setActiveLayer(lm.model_handlers[dm.ConnectionNode].layer)
        if self.model_gpkg is not None:
            self.active_schematisation_combo.setToolTip(f"Currently active schematisation: {self.model_gpkg}")
        else:
            self.active_schematisation_combo.setToolTip("No active schematisation")

    def add_multi_action_button(self, name, icon_path, actions_specification):
        parent_window = self.iface.mainWindow()
        action_arguments = [name, parent_window]
        if icon_path:
            icon = QIcon(icon_path)
            action_arguments.insert(0, icon)
        main_action = QAction(*action_arguments)
        menu = QMenu()
        for sub_action_name, sub_action_callback, sub_icon_path in actions_specification:
            sub_action_arguments = [sub_action_name, parent_window]
            if sub_icon_path:
                sub_icon = QIcon(sub_icon_path)
                sub_action_arguments.insert(0, sub_icon)
            sub_action = QAction(*sub_action_arguments)
            sub_action.triggered.connect(sub_action_callback)
            menu.addAction(sub_action)
        main_action.setMenu(menu)
        main_action.triggered.connect(lambda: menu.exec(QCursor.pos()))
        return main_action

    def toggle_active_project_actions(self):
        if self.model_gpkg is None:
            self.action_export.setDisabled(True)
            self.action_export_as.setDisabled(True)
            self.action_remove.setDisabled(True)
            self.action_import_culverts.setDisabled(True)
        else:
            self.action_export.setEnabled(True)
            self.action_export_as.setEnabled(True)
            self.action_remove.setEnabled(True)
            self.action_import_culverts.setEnabled(True)

    def check_macros_status(self):
        macros_status = check_enable_macros_option()
        if macros_status != "Always":
            msg = (
                f"Required 'Macros enabled' option is set to '{macros_status}'. "
                "Please change it to 'Always' before making edits (Settings -> Options -> General -> Enable macros)."
            )
            self.uc.bar_warn(msg, dur=10)

    def select_user_layers_geopackage(self):
        name_filter = "3Di User Layers (*.gpkg *.GPKG)"
        filename = get_filepath(self.iface.mainWindow(), extension_filter=name_filter, save=False)
        return filename

    def select_sqlite_database(self, title):
        name_filter = "Spatialite Database (*.sqlite)"
        filename = get_filepath(self.iface.mainWindow(), extension_filter=name_filter, save=False, dialog_title=title)
        return filename

    def on_3di_project_read(self):
        custom_vars = self.project.customVariables()
        try:
            project_model_gpkgs_str = custom_vars[self.THREEDI_GPKG_VAR_NAMES]
            project_model_gpkgs = project_model_gpkgs_str.split("|")
        except KeyError:
            self.toggle_active_project_actions()
            return
        for model_gpkg in project_model_gpkgs:
            lm = LayersManager(self.iface, self.uc, model_gpkg)
            if lm not in self.workspace_context_manager:
                lm.load_all_layers(from_project=True)
                self.workspace_context_manager.register_layer_manager(lm)
        self.uc.bar_info("3Di User Layers registered!")
        self.check_macros_status()
        self.toggle_active_project_actions()

    def on_3di_project_save(self):
        project_model_gpkgs_str = "|".join(lm.model_gpkg_path for lm in self.workspace_context_manager)
        if project_model_gpkgs_str:
            self.project.setCustomVariables({self.THREEDI_GPKG_VAR_NAMES: project_model_gpkgs_str})

    def open_model_from_geopackage(self, model_gpkg=None):
        if not model_gpkg:
            model_gpkg = self.select_user_layers_geopackage()
            if not model_gpkg:
                return
        lm = LayersManager(self.iface, self.uc, model_gpkg)
        if lm in self.workspace_context_manager:
            warn_msg = "Selected schematisation is already loaded. Loading canceled."
            self.uc.show_warn(warn_msg)
            return
        lm.load_all_layers()
        self.workspace_context_manager.register_layer_manager(lm)
        self.uc.bar_info("3Di User Layers registered!")
        self.check_macros_status()
        self.toggle_active_project_actions()
        if self.model_gpkg and not is_gpkg_connection_exists(self.model_gpkg):
            add_gpkg_connection(self.model_gpkg, self.iface)

    def load_from_spatialite(self, src_sqlite=None):
        if not src_sqlite:
            schematisation_loader = LoadSchematisationDialog(self.uc)
            result = schematisation_loader.exec_()
            if result != QDialog.Accepted:
                return
            src_sqlite = schematisation_loader.selected_schematisation_sqlite
        if not can_write_in_dir(os.path.dirname(src_sqlite)):
            warn_msg = "You don't have required write permissions to load data from the selected spatialite."
            self.uc.show_warn(warn_msg)
            return
        schema_version = ModelDataConverter.spatialite_schema_version(src_sqlite)
        if schema_version is None:
            warn_msg = (
                "The selected spatialite cannot be used because its schema version information is missing. "
                "Please upgrade the 3Di Schematisation Editor and try again."
            )
            self.uc.show_warn(warn_msg)
            self.uc.bar_warn("Loading from the Spatialite aborted!")
            return
        if schema_version > ModelDataConverter.SUPPORTED_SCHEMA_VERSION:
            warn_msg = (
                "The selected spatialite cannot be used because its database schema version is newer than expected. "
                "Please upgrade the 3Di Schematisation Editor and try again."
            )
            self.uc.show_warn(warn_msg)
            self.uc.bar_warn("Loading from the Spatialite aborted!")
            return
        else:
            schema_is_valid = ensure_valid_schema(src_sqlite, self.uc)
            if schema_is_valid is False:
                self.uc.bar_warn("Loading from the Spatialite aborted!")
                return
        dst_gpkg = os.path.normpath(src_sqlite.replace(".sqlite", ".gpkg"))
        if dst_gpkg in set(self.workspace_context_manager.layer_managers.keys()):
            warn_msg = "Selected schematisation is already loaded. Loading canceled."
            self.uc.show_warn(warn_msg)
            return
        converter = ModelDataConverter(src_sqlite, dst_gpkg, user_communication=self.uc)
        known_epsg = converter.set_epsg_from_sqlite()
        if known_epsg is False:
            return
        try:
            converter.create_empty_user_layers()
            converter.import_all_model_data()
        except ConversionError:
            self.uc.bar_warn("Loading from the Spatialite failed!")
            return
        if converter.missing_source_settings is True:
            add_settings_entry(dst_gpkg, id=1, epsg_code=converter.epsg_code)
        lm = LayersManager(self.iface, self.uc, dst_gpkg)
        lm.load_all_layers()
        self.workspace_context_manager.register_layer_manager(lm)
        self.uc.show_info("Loading from the Spatialite finished!")
        self.check_macros_status()
        self.toggle_active_project_actions()
        if self.model_gpkg and not is_gpkg_connection_exists(self.model_gpkg):
            add_gpkg_connection(self.model_gpkg, self.iface)

    def save_to_selected(self):
        self.save_to_spatialite()

    def save_to_default(self):
        self.save_to_spatialite(pick_destination=False)

    def save_to_spatialite(self, pick_destination=True):
        if not self.model_gpkg:
            return
        if self.layer_manager is None:
            return
        fixed_errors_msg, unsolved_errors_msg = self.layer_manager.validate_layers()
        if unsolved_errors_msg:
            warn_msg = (
                "Saving to Spatialite failed. "
                "The following features have cross sections with incorrect table inputs:\n"
            )
            warn_msg += unsolved_errors_msg
            self.uc.show_warn(warn_msg)
            return
        self.layer_manager.stop_model_editing()
        if pick_destination:
            dst_sqlite = self.select_sqlite_database(title="Select database to save features to")
        else:
            dst_sqlite = self.model_gpkg.replace(".gpkg", ".sqlite")
        if not dst_sqlite:
            return
        if not os.path.isfile(dst_sqlite):
            warn_msg = "Target spatialite file doesn't exist. Saving to spatialite canceled."
            self.uc.show_warn(warn_msg)
            return
        if not can_write_in_dir(os.path.dirname(dst_sqlite)):
            warn_msg = "You don't have required write permissions to save data into the selected spatialite."
            self.uc.show_warn(warn_msg)
            return
        schema_version = ModelDataConverter.spatialite_schema_version(dst_sqlite)
        if schema_version > ModelDataConverter.SUPPORTED_SCHEMA_VERSION:
            warn_msg = (
                "The selected spatialite cannot be used because its database schema version is newer than expected. "
                "Please upgrade the 3Di Schematisation Editor and try again."
            )
            self.uc.show_warn(warn_msg)
            return
        else:
            schema_is_valid = ensure_valid_schema(dst_sqlite, self.uc)
            if schema_is_valid is False:
                return
        converter = ModelDataConverter(dst_sqlite, self.model_gpkg, user_communication=self.uc)
        known_epsg = converter.set_epsg_from_gpkg()
        if known_epsg is False:
            return
        converter.trim_sqlite_targets()
        converter.report_conversion_errors()
        converter.export_all_model_data()
        self.uc.show_info("Saving to the Spatialite finished!")

    def save_to_spatialite_on_action(self):
        model_modified = self.layer_manager.model_modified()
        if model_modified:
            title = "Save to Spatialite?"
            question = "Would you like to save model to Spatialite before closing project?"
            answer = self.uc.ask(None, title, question)
            if answer is True:
                self.save_to_spatialite()

    def remove_model_from_project(self):
        if not self.model_gpkg:
            return
        if self.layer_manager is not None:
            self.save_to_spatialite_on_action()
            self.iface.currentLayerChanged.disconnect(self.switch_workspace_context)
            self.layer_manager.remove_groups()
            self.iface.currentLayerChanged.connect(self.switch_workspace_context)
            self.workspace_context_manager.unregister_layer_manager(self.layer_manager)
        self.switch_workspace_context(self.iface.activeLayer())
        self.toggle_active_project_actions()
        self.iface.mapCanvas().refresh()

    def import_external_culverts(self):
        if not self.model_gpkg:
            return
        import_culverts_dlg = ImportStructuresDialog(dm.Culvert, self.model_gpkg, self.layer_manager, self.uc)
        import_culverts_dlg.exec_()

    def import_external_orifices(self):
        if not self.model_gpkg:
            return
        import_orifices_dlg = ImportStructuresDialog(dm.Orifice, self.model_gpkg, self.layer_manager, self.uc)
        import_orifices_dlg.exec_()

    def import_external_weirs(self):
        if not self.model_gpkg:
            return
        import_weirs_dlg = ImportStructuresDialog(dm.Weir, self.model_gpkg, self.layer_manager, self.uc)
        import_weirs_dlg.exec_()

    def import_external_pipes(self):
        import_pipes_dlg = ImportStructuresDialog(dm.Pipe, self.model_gpkg, self.layer_manager, self.uc)
        import_pipes_dlg.exec_()

    def import_external_manholes(self):
        import_manholes_dlg = ImportStructuresDialog(dm.Manhole, self.model_gpkg, self.layer_manager, self.uc)
        import_manholes_dlg.exec_()

    def on_project_close(self):
        if self.layer_manager is None:
            return
        self.save_to_spatialite_on_action()
        for lm in self.workspace_context_manager:
            lm.remove_loaded_layers(dry_remove=True)
        self.workspace_context_manager.unregister_all()
        self.toggle_active_project_actions()
