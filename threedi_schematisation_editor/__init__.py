# Copyright (C) 2025 by Lutra Consulting
import os.path
import platform
from collections import defaultdict
from pathlib import Path

import pyplugin_installer
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsLayerTreeNode,
    QgsMessageLog,
    QgsProject,
    QgsSettings,
)
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QCursor, QIcon
from qgis.PyQt.QtWidgets import QAction, QComboBox, QDialog, QMenu, QMessageBox
from qgis.utils import isPluginLoaded, startPlugin


def check_dependency_loader():
    required_plugin = "nens_dependency_loader"
    if not isPluginLoaded(required_plugin):
        if (
            QMessageBox.question(
                None,
                "N&S Dependency Loader",
                "N&S Dependency Loader is required, but not loaded. Would you like to load it?",
            )
            == QMessageBox.Yes
        ):
            try:  # This is basically what qgis.utils.loadPlugin() does, but that also shows errors, so we need to do it explicitly
                __import__(required_plugin)
                plugin_loadable = True
            except:
                plugin_loadable = False

            if plugin_loadable:
                if not startPlugin(required_plugin):
                    QMessageBox.warning(
                        None,
                        "N&S Dependency Loader",
                        "Unable to start N&S Dependency Loader, please enable the plugin manually",
                    )
                    return
            else:
                pyplugin_installer.instance().fetchAvailablePlugins(True)
                pyplugin_installer.instance().installPlugin(required_plugin)

            QgsSettings().setValue("/PythonPlugins/" + required_plugin, True)
            QgsSettings().remove("/PythonPlugins/watchDogTimestamp/" + required_plugin)


PLUGIN_DIR = Path(__file__).parent

from threedi_mi_utils.news import QgsNewsSettingsInjector
from threedi_schema import ThreediDatabase

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.communication import UICommunication
from threedi_schematisation_editor.load_schematisation.load_schematisation import (
    LoadSchematisationDialog,
)
from threedi_schematisation_editor.processing import (
    ThreediSchematisationEditorProcessingProvider,
)
from threedi_schematisation_editor.user_layer_manager import LayersManager
from threedi_schematisation_editor.utils import (
    ConversionError,
    add_gpkg_connection,
    add_settings_entry,
    can_write_in_dir,
    check_enable_embedded_python_option,
    check_enable_macros_option,
    check_wal_for_sqlite,
    get_filepath,
    get_icon_path,
    is_gpkg_connection_exists,
    migrate_schematisation_schema,
    progress_bar_callback_factory,
    set_wal_for_sqlite_mode,
)
from threedi_schematisation_editor.vector_data_importer.dialogs.import_features import (
    ImportCrossSectionDataDialog,
    ImportCrossSectionLocationDialog,
    ImportFeaturesDialog,
    ImportStructuresDialog,
)
from threedi_schematisation_editor.vector_data_importer.wizard import (
    ImportConduitWizard,
    ImportCrossSectionDataWizard,
    ImportCrossSectionLocationWizard,
    ImportStructureWizard,
    VDIWizard,
)
from threedi_schematisation_editor.workspace import WorkspaceContextManager


def classFactory(iface):
    if platform.system() == "Windows":
        check_dependency_loader()

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
        self.action_import_features = None
        self.workspace_context_manager = WorkspaceContextManager(self)
        self.provider = ThreediSchematisationEditorProcessingProvider()
        self.project = QgsProject.instance()
        self.project.removeAll.connect(self.on_project_close)
        self.project.readProject.connect(self.on_3di_project_read)
        self.project.writeProject.connect(self.on_3di_project_save)
        self.iface.currentLayerChanged.connect(self.switch_workspace_context)

        # Inject custom news entries in settings
        QgsNewsSettingsInjector().load(PLUGIN_DIR / "news_feed.json")

    def initGui(self):
        QgsApplication.processingRegistry().addProvider(self.provider)
        self.toolbar = self.iface.addToolBar("Schematisation Editor")
        self.active_schematisation_combo = QComboBox()
        self.active_schematisation_combo.setMinimumWidth(250)
        self.active_schematisation_combo.setPlaceholderText("No active schematisation")
        self.active_schematisation_combo.currentIndexChanged.connect(
            self.active_schematisation_changed
        )
        self.toolbar.addWidget(self.active_schematisation_combo)
        self.toolbar.addSeparator()
        self.action_open = QAction(
            QIcon(get_icon_path("icon_load.svg")),
            "Load 3Di Schematisation",
            self.iface.mainWindow(),
        )
        self.action_open.triggered.connect(self.load_schematisation)
        self.action_remove = QAction(
            QIcon(get_icon_path("icon_unload.svg")),
            "Remove 3Di Schematisation",
            self.iface.mainWindow(),
        )
        self.action_remove.triggered.connect(self.remove_model_from_project)
        import_features_icon_path = get_icon_path("icon_import.png")
        import_actions_spec = [
            ("Connection nodes", self.import_external_connection_nodes, None),
            (
                "Cross-section data",
                self.import_external_cross_section_data,
                None,
            ),
            (
                "Cross-section locations",
                self.import_external_cross_section_locations,
                None,
            ),
            ("Culverts", self.import_external_culverts, None),
            ("Orifices", self.import_external_orifices, None),
            ("Weirs", self.import_external_weirs, None),
            ("Pipes", self.import_external_pipes, None),
            ("Channels", self.import_external_channels, None),
        ]
        self.action_import_features = self.add_multi_action_button(
            "Import schematisation objects",
            import_features_icon_path,
            import_actions_spec,
        )
        self.toolbar.addAction(self.action_open)
        self.toolbar.addAction(self.action_remove)
        self.toolbar.addAction(self.action_import_features)
        self.toggle_active_project_actions()
        self.active_schematisation_changed()
        self.ensure_sqlite_wal_status()
        # TODO: remove this!
        self.load_schematisation(
            "/home/margriet/qgis_workdir/test_253_import_csd/test.gpkg"
        )
        self.action_import_features.menu().actions()[2].trigger()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.active_schematisation_combo.currentIndexChanged.disconnect(
            self.active_schematisation_changed
        )
        del self.toolbar
        del self.active_schematisation_combo
        del self.action_open
        del self.action_remove
        del self.action_import_features

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
            if node.nodeType() == QgsLayerTreeNode.NodeType.NodeGroup
            and node.name().startswith("3Di schematisation:")
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
            model_gpkg = os.path.normpath(
                connection_node_layer.source().rsplit("|", 1)[0]
            )
            for sub_grp in model_groups.values():
                for nested_node in sub_grp.children():
                    if nested_node.nodeType() == QgsLayerTreeNode.NodeType.NodeLayer:
                        model_layer = nested_node.layer()
                        model_layers[model_gpkg].add(model_layer.id())
        return model_layers

    def switch_workspace_context(self, active_layer):
        if not active_layer:
            return
        expected_layer_source = os.path.normpath(
            active_layer.source().rsplit("|", 1)[0]
        )
        if active_layer.id() in self.model_layers_map[expected_layer_source]:
            try:
                lm = self.workspace_context_manager.layer_managers[
                    expected_layer_source
                ]
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
            self.active_schematisation_combo.setToolTip(
                f"Currently active schematisation: {self.model_gpkg}"
            )
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
        for (
            sub_action_name,
            sub_action_callback,
            sub_icon_path,
        ) in actions_specification:
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
            self.action_import_features.setDisabled(True)
        else:
            self.action_remove.setEnabled(True)
            self.action_import_features.setEnabled(True)

    def check_embedded_python_status(self):
        if Qgis.QGIS_VERSION_INT < 34000:
            macros_status = check_enable_macros_option()
            if macros_status != "Always":
                msg = (
                    f"Required 'Macros enabled' option is set to '{macros_status}'. "
                    "Please change it to 'Always' before making edits (Settings -> Options -> General -> Enable macros)."
                )
                self.uc.bar_warn(msg, dur=10)
        else:
            embedded_python_status = check_enable_embedded_python_option()
            if embedded_python_status != "Always":
                msg = (
                    f"Required 'Embedded Python code enabled' option is set to '{embedded_python_status}'. "
                    "Please change it to 'Always' before making edits (Settings -> Options -> General -> Enable project’s embedded Python code)."
                )
                self.uc.bar_warn(msg, dur=10)

    def ensure_sqlite_wal_status(self):
        wal_status = check_wal_for_sqlite()
        if wal_status is not False:
            set_wal_for_sqlite_mode(False)
            msg = f"WAL (Write-Ahead Logging) for GeoPackage format was disabled. To apply changes please restart QGIS."
            self.uc.bar_warn(msg, dur=10)

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
        self.uc.bar_info("Project schematisations loaded!")
        self.check_embedded_python_status()
        self.toggle_active_project_actions()

    def on_3di_project_save(self):
        project_model_gpkgs_str = "|".join(
            lm.model_gpkg_path for lm in self.workspace_context_manager
        )
        if project_model_gpkgs_str:
            self.project.setCustomVariables(
                {self.THREEDI_GPKG_VAR_NAMES: project_model_gpkgs_str}
            )

    def load_schematisation(self, model_gpkg=None):
        if not model_gpkg:
            schematisation_loader = LoadSchematisationDialog(self.uc)
            result = schematisation_loader.exec_()
            if result != QDialog.Accepted:
                return
            schematisation_filepath = (
                schematisation_loader.selected_schematisation_filepath
            )
            if not can_write_in_dir(os.path.dirname(schematisation_filepath)):
                warn_msg = "You don't have required write permissions to load data from the selected location."
                self.uc.show_warn(warn_msg)
                return
            model_gpkg = schematisation_filepath

        if model_gpkg.endswith(".sqlite"):
            QCoreApplication.processEvents()
            migration_info = "Schema migration..."
            self.uc.progress_bar(migration_info, 0, 100, 0, clear_msg_bar=True)
            progress_bar_callback = progress_bar_callback_factory(self.uc)
            migration_succeed, migration_feedback_msg = migrate_schematisation_schema(
                model_gpkg, progress_bar_callback
            )
            self.uc.progress_bar("Migration complete!", 0, 100, 100, clear_msg_bar=True)
            QCoreApplication.processEvents()
            if len(migration_feedback_msg) > 0 and migration_succeed:
                self.uc.show_info(migration_feedback_msg)
                QgsMessageLog.logMessage(
                    migration_feedback_msg, level=Qgis.Warning, tag="Messages"
                )
            elif not migration_succeed:
                self.uc.clear_message_bar()
                self.uc.show_warn(migration_feedback_msg)
                return
            model_gpkg = model_gpkg.rsplit(".", 1)[0] + ".gpkg"
        elif model_gpkg.endswith(".gpkg"):
            version_num = ThreediDatabase(model_gpkg).schema.get_version()
            if version_num < 300:
                warn_msg = "The selected file is not a valid 3Di schematisation database.\n\nYou may have selected a geopackage that was created by an older version of the 3Di Schematisation Editor (before version 2.0). In that case, there will probably be a Spatialite (*.sqlite) in the same folder. Please use that file instead."
                self.uc.show_warn(warn_msg, None, "3Di Schematisation Editor")
                return

        lm = LayersManager(self.iface, self.uc, model_gpkg)
        if lm in self.workspace_context_manager:
            self.uc.clear_message_bar()
            warn_msg = "Selected schematisation is already loaded. Loading canceled."
            self.uc.show_warn(warn_msg)
            return
        lm.load_all_layers()
        self.workspace_context_manager.register_layer_manager(lm)
        self.uc.clear_message_bar()
        self.uc.bar_info(f"Schematisation {lm.model_name} loaded!")
        self.check_embedded_python_status()
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

    def import_external(self, model_cls, dialog_cls):
        if not self.model_gpkg:
            return
        # import_dlg = dialog_cls(model_cls)
        import_dlg = dialog_cls(model_cls, self.model_gpkg, self.layer_manager)
        import_dlg.exec_()

    def import_external_connection_nodes(self):
        self.import_external(dm.ConnectionNode, VDIWizard)

    def import_external_cross_section_data(self):
        self.import_external(dm.CrossSectionData, ImportCrossSectionDataWizard)

    def import_external_cross_section_locations(self):
        self.import_external(dm.CrossSectionLocation, ImportCrossSectionLocationWizard)

    def import_external_culverts(self):
        self.import_external(dm.Culvert, ImportStructureWizard)

    def import_external_orifices(self):
        self.import_external(dm.Orifice, ImportStructureWizard)

    def import_external_weirs(self):
        self.import_external(dm.Weir, ImportStructureWizard)

    def import_external_pipes(self):
        self.import_external(dm.Pipe, ImportConduitWizard)

    def import_external_channels(self):
        self.import_external(dm.Channel, ImportConduitWizard)

    def on_project_close(self):
        if self.layer_manager is None:
            return
        for lm in self.workspace_context_manager:
            lm.remove_loaded_layers(dry_remove=True)
        self.workspace_context_manager.unregister_all()
        self.toggle_active_project_actions()
