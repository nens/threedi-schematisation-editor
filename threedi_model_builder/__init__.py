# Copyright (C) 2021 by Lutra Consulting
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject
from threedi_model_builder.communication import UICommunication
from threedi_model_builder.user_layer_manager import LayersManager
from threedi_model_builder.conversion import ModelDataConverter
from threedi_model_builder.utils import (
    load_user_layers,
    create_empty_model,
    get_filepath,
    remove_user_layers,
    check_enable_macros_option,
)


def classFactory(iface):
    return ThreediModelBuilderPlugin(iface)


class ThreediModelBuilderPlugin:
    PLUGIN_NAME = "3Di Model Builder"

    def __init__(self, iface):
        self.iface = iface
        self.uc = UICommunication(self.iface, "3Di Model Builder")
        self.action_open = None
        self.action_import = None
        self.action_export = None
        self.model_gpkg = None
        self.layer_manager = None
        self.form_factory = None
        self.project = QgsProject.instance()
        self.project.removeAll.connect(self.on_project_close)

    def initGui(self):
        self.action_open = QAction("Open 3Di Geopackage", self.iface.mainWindow())
        self.action_open.triggered.connect(self.open_model_from_geopackage)
        self.action_import = QAction("Load from Spatialite", self.iface.mainWindow())
        self.action_import.triggered.connect(self.load_from_spatialite)
        self.action_export = QAction("Save to Spatialite", self.iface.mainWindow())
        self.action_export.triggered.connect(self.save_to_spatialite)
        self.iface.addToolBarIcon(self.action_open)
        self.iface.addToolBarIcon(self.action_import)
        self.iface.addToolBarIcon(self.action_export)

    def unload(self):
        self.iface.removeToolBarIcon(self.action_open)
        del self.action_open
        self.iface.removeToolBarIcon(self.action_import)
        del self.action_import
        self.iface.removeToolBarIcon(self.action_export)
        del self.action_export

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
        filename = get_filepath(self.iface.mainWindow(), filter=name_filter, save=False)
        return filename

    def select_sqlite_database(self, title):
        name_filter = "Spatialite Database (*.sqlite)"
        filename = get_filepath(self.iface.mainWindow(), filter=name_filter, save=False, dialog_title=title)
        return filename

    def open_model_from_geopackage(self):
        model_gpkg = self.select_user_layers_geopackage()
        if not model_gpkg:
            return
        if self.layer_manager is not None:
            self.layer_manager.remove_groups()
        self.model_gpkg = model_gpkg
        self.layer_manager = LayersManager(self.iface, self.uc, self.model_gpkg)
        self.layer_manager.load_all_layers()
        self.uc.bar_info("3Di User Layers registered!")
        self.check_macros_status()

    def load_from_spatialite(self):
        src_sqlite = self.select_sqlite_database(title="Select database to load features from")
        if not src_sqlite:
            return
        schema_version = ModelDataConverter.spatialite_schema_version(src_sqlite)
        if schema_version not in ModelDataConverter.SUPPORTED_SCHEMA_VERSIONS:
            warn_msg = (
                "The spatialite you have selected could not be loaded, "
                f"because its database schema version ({schema_version}) is not up to date. "
                "Please find your model revision on 3di.lizard.net/models, "
                "download the spatialite from there and try again."
            )
            self.uc.show_warn(warn_msg)
            return
        if self.layer_manager is not None:
            self.layer_manager.remove_groups()
        dst_gpkg = src_sqlite.replace(".sqlite", ".gpkg")
        converter = ModelDataConverter(src_sqlite, dst_gpkg, user_communication=self.uc)
        converter.create_empty_user_layers()
        converter.import_all_model_data()
        self.model_gpkg = dst_gpkg
        self.layer_manager = LayersManager(self.iface, self.uc, self.model_gpkg)
        self.layer_manager.load_all_layers()
        self.uc.show_info("Loading from the Spatialite finished!")
        self.check_macros_status()

    def save_to_spatialite(self):
        if not self.model_gpkg:
            return
        dst_sqlite = self.select_sqlite_database(title="Select database to save features to")
        if not dst_sqlite:
            return
        schema_version = ModelDataConverter.spatialite_schema_version(dst_sqlite)
        if schema_version not in ModelDataConverter.SUPPORTED_SCHEMA_VERSIONS:
            warn_msg = (
                "The spatialite you have selected could not be used for saving, "
                f"because its database schema version ({schema_version}) is not up to date. "
                "Please find your model revision on 3di.lizard.net/models, "
                "download the spatialite from there and try again."
            )
            self.uc.show_warn(warn_msg)
            return
        converter = ModelDataConverter(dst_sqlite, self.model_gpkg, user_communication=self.uc)
        converter.trim_sqlite_targets()
        converter.export_all_model_data()
        self.uc.show_info("Saving to the Spatialite finished!")

    def on_project_close(self):
        if self.layer_manager is None:
            return
        title = "Save to Spatialite?"
        question = "Would you like to save model to Spatialite before closing project?"
        answer = self.uc.ask(None, title, question)
        if answer is True:
            self.save_to_spatialite()
        self.layer_manager.remove_loaded_layers(dry_remove=True)
        self.layer_manager = None
