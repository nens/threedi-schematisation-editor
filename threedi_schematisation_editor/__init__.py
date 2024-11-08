# Copyright (C) 2023 by Lutra Consulting
import os.path
from collections import defaultdict

from qgis.core import QgsApplication, QgsLayerTreeNode, QgsProject
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QAction, QComboBox, QMenu
import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.communication import UICommunication
from threedi_schematisation_editor.custom_widgets import ImportStructuresDialog, LoadSchematisationDialog
from threedi_schematisation_editor.processing import ThreediSchematisationEditorProcessingProvider
from threedi_schematisation_editor.user_layer_manager import LayersManager
from threedi_schematisation_editor.utils import (
    ConversionError,
    add_gpkg_connection,
    add_settings_entry,
    can_write_in_dir,
    check_enable_macros_option,
    create_empty_model,
    ensure_valid_schema,
    get_filepath,
    is_gpkg_connection_exists,
    remove_user_layers,
)
from threedi_schematisation_editor.workspace import WorkspaceContextManager


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
            self.action_remove.setDisabled(True)
            self.action_import_culverts.setDisabled(True)
        else:
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

    def remove_model_from_project(self):
        if not self.model_gpkg:
            return
        if self.layer_manager is not None:
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
        for lm in self.workspace_context_manager:
            lm.remove_loaded_layers(dry_remove=True)
        self.workspace_context_manager.unregister_all()
        self.toggle_active_project_actions()
