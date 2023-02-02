# Copyright (C) 2023 by Lutra Consulting
import os.path
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject
from threedi_schematisation_editor.communication import UICommunication
from threedi_schematisation_editor.user_layer_manager import LayersManager
from threedi_schematisation_editor.conversion import ModelDataConverter
from threedi_schematisation_editor.utils import (
    can_write_in_dir,
    create_empty_model,
    get_filepath,
    remove_user_layers,
    add_settings_entry,
    check_enable_macros_option,
    is_gpkg_connection_exists,
    add_gpkg_connection,
    migrate_spatialite_schema,
    ConversionError,
)


def classFactory(iface):
    return ThreediModelBuilderPlugin(iface)


class ThreediModelBuilderPlugin:
    PLUGIN_NAME = "3Di Model Builder"
    THREEDI_GPKG_VAR_NAME = "threedi_gpkg_var"

    def __init__(self, iface):
        self.iface = iface
        self.uc = UICommunication(self.iface, "3Di Model Builder")
        self.action_open = None
        self.action_import = None
        self.action_export = None
        self.action_export_as = None
        self.action_remove = None
        self.model_gpkg = None
        self.layer_manager = None
        self.form_factory = None
        self.project = QgsProject.instance()
        self.project.removeAll.connect(self.on_project_close)
        self.project.readProject.connect(self.on_3di_project_read)
        self.project.projectSaved.connect(self.on_3di_project_save)

    def initGui(self):
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
        self.iface.addToolBarIcon(self.action_open)
        self.iface.addToolBarIcon(self.action_import)
        self.iface.addToolBarIcon(self.action_export)
        self.iface.addToolBarIcon(self.action_export_as)
        self.iface.addToolBarIcon(self.action_remove)
        self.toggle_active_project_actions()

    def unload(self):
        self.iface.removeToolBarIcon(self.action_open)
        del self.action_open
        self.iface.removeToolBarIcon(self.action_import)
        del self.action_import
        self.iface.removeToolBarIcon(self.action_export)
        del self.action_export
        self.iface.removeToolBarIcon(self.action_export_as)
        del self.action_export_as
        self.iface.removeToolBarIcon(self.action_remove)
        del self.action_remove

    def toggle_active_project_actions(self):
        if self.model_gpkg is None:
            self.action_export.setDisabled(True)
            self.action_export_as.setDisabled(True)
            self.action_remove.setDisabled(True)
        else:
            self.action_export.setEnabled(True)
            self.action_export_as.setEnabled(True)
            self.action_remove.setEnabled(True)

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
        self.action_export.setDisabled(True)
        custom_vars = self.project.customVariables()
        try:
            self.model_gpkg = custom_vars[self.THREEDI_GPKG_VAR_NAME]
        except KeyError:
            self.model_gpkg = None
            self.toggle_active_project_actions()
            return
        self.layer_manager = LayersManager(self.iface, self.uc, self.model_gpkg)
        self.layer_manager.load_all_layers(from_project=True)
        self.uc.bar_info("3Di User Layers registered!")
        self.check_macros_status()
        self.toggle_active_project_actions()

    def on_3di_project_save(self):
        if self.model_gpkg is not None:
            self.project.setCustomVariables({self.THREEDI_GPKG_VAR_NAME: self.model_gpkg})

    def open_model_from_geopackage(self):
        model_gpkg = self.select_user_layers_geopackage()
        if not model_gpkg:
            return
        if self.layer_manager is not None:
            self.layer_manager.remove_groups()
            self.model_gpkg = None
            self.toggle_active_project_actions()
        self.model_gpkg = model_gpkg
        self.layer_manager = LayersManager(self.iface, self.uc, self.model_gpkg)
        self.layer_manager.load_all_layers()
        self.uc.bar_info("3Di User Layers registered!")
        self.check_macros_status()
        self.project.setCustomVariables({self.THREEDI_GPKG_VAR_NAME: self.model_gpkg})
        self.toggle_active_project_actions()
        if self.model_gpkg and not is_gpkg_connection_exists(self.model_gpkg):
            add_gpkg_connection(self.model_gpkg, self.iface)

    def load_from_spatialite(self):
        src_sqlite = self.select_sqlite_database(title="Select database to load features from")
        if not src_sqlite:
            return
        if not can_write_in_dir(os.path.dirname(src_sqlite)):
            warn_msg = "You don't have required write permissions to load data from the selected spatialite."
            self.uc.show_warn(warn_msg)
            return
        schema_version = ModelDataConverter.spatialite_schema_version(src_sqlite)
        if schema_version != ModelDataConverter.SUPPORTED_SCHEMA_VERSION:
            warn_and_ask_msg = (
                "The selected spatialite cannot be used because its database schema version is out of date. "
                "Would you like to migrate your spatialite to the current schema version?"
            )
            do_migration = self.uc.ask(None, "Missing migration", warn_and_ask_msg)
            if do_migration:
                migration_succeed, migration_feedback_msg = migrate_spatialite_schema(src_sqlite)
                if not migration_succeed:
                    self.uc.show_warn(migration_feedback_msg)
                    return
            else:
                self.uc.bar_warn("Loading from the Spatialite aborted!")
                return
        if self.layer_manager is not None:
            self.layer_manager.remove_groups()
            self.model_gpkg = None
            self.toggle_active_project_actions()
        dst_gpkg = src_sqlite.replace(".sqlite", ".gpkg")
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
        self.model_gpkg = dst_gpkg
        self.layer_manager = LayersManager(self.iface, self.uc, self.model_gpkg)
        self.layer_manager.load_all_layers()
        self.uc.show_info("Loading from the Spatialite finished!")
        self.check_macros_status()
        self.project.setCustomVariables({self.THREEDI_GPKG_VAR_NAME: self.model_gpkg})
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
        if schema_version != ModelDataConverter.SUPPORTED_SCHEMA_VERSION:
            schema_version_str = f" ({schema_version}) " if schema_version else " "
            warn_msg = (
                "The spatialite you have selected could not be used for saving, "
                f"because its database schema version{schema_version_str}is not up to date. "
                "Please find your model revision on 3di.lizard.net/models, "
                "download the spatialite from there and try again."
            )
            self.uc.show_warn(warn_msg)
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
            self.layer_manager.remove_groups()
            self.model_gpkg = None
        custom_vars = self.project.customVariables()
        if self.THREEDI_GPKG_VAR_NAME in custom_vars:
            del custom_vars[self.THREEDI_GPKG_VAR_NAME]
            self.project.setCustomVariables(custom_vars)
        self.toggle_active_project_actions()
        self.iface.mapCanvas().refresh()

    def on_project_close(self):
        if self.layer_manager is None:
            return
        self.save_to_spatialite_on_action()
        self.layer_manager.remove_loaded_layers(dry_remove=True)
        self.layer_manager = None
        self.model_gpkg = None
        self.toggle_active_project_actions()
