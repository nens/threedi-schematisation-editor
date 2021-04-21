# Copyright (C) 2021 by Lutra Consulting
from qgis.PyQt.QtWidgets import QAction
from .user_layers.conversion import ModelDataConverter
from .user_layers.utils import (
    load_user_layers,
    create_empty_model,
    get_filepath,
    remove_user_layers,
)
from .communication import UICommunication


def classFactory(iface):
    return ThreediModelBuilderPlugin(iface)


class ThreediModelBuilderPlugin:
    PLUGIN_NAME = "3Di Model Builder"

    def __init__(self, iface):
        self.iface = iface
        self.ui = UICommunication(self.iface, "3Di Model Builder")
        self.action_import = None
        self.action_export = None
        self.current_gpkg = None

    def initGui(self):
        self.action_import = QAction("Import from Spatialite", self.iface.mainWindow())
        self.action_import.triggered.connect(self.import_from_spatialite)
        self.action_export = QAction("Export to Spatialite", self.iface.mainWindow())
        self.action_export.triggered.connect(self.export_to_spatialite)
        self.iface.addToolBarIcon(self.action_import)
        self.iface.addToolBarIcon(self.action_export)

    def unload(self):
        self.iface.removeToolBarIcon(self.action_import)
        del self.action_import
        self.iface.removeToolBarIcon(self.action_export)
        del self.action_export

    def select_import_database(self):
        name_filter = "Spatialite Database (*.sqlite)"
        filename = get_filepath(self.iface.mainWindow(), filter=name_filter, extension=".sqlite", save=False)
        return filename

    def select_export_database(self):
        name_filter = "Spatialite Database (*.sqlite)"
        filename = get_filepath(self.iface.mainWindow(), filter=name_filter, extension=".sqlite", save=True)
        return filename

    def import_from_spatialite(self):
        src_sqlite = self.select_import_database()
        if not src_sqlite:
            return
        remove_user_layers()
        dst_gpkg = src_sqlite.replace(".sqlite", ".gpkg")
        converter = ModelDataConverter(src_sqlite, dst_gpkg)
        converter.create_empty_user_layers()
        converter.import_all_model_data()
        load_user_layers(dst_gpkg)
        self.current_gpkg = dst_gpkg
        self.ui.show_info("Import finished!")

    def export_to_spatialite(self):
        if not self.current_gpkg:
            return
        dst_sqlite = self.select_export_database()
        if not dst_sqlite:
            return
        create_empty_model(dst_sqlite)
        converter = ModelDataConverter(dst_sqlite, self.current_gpkg)
        converter.export_all_model_data()
        self.ui.show_info("Export finished!")
