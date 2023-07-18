# Copyright (C) 2023 by Lutra Consulting
import os

from qgis.PyQt import uic
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.custom_tools import CulvertImportSettings, import_culverts

ps_basecls, ps_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "projection_selection.ui"))
ic_basecls, ic_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "import_culverts.ui"))


class ProjectionSelectionDialog(ps_basecls, ps_uicls):
    """Dialog with selection of the desired projection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class ImportCulvertsDialog(ic_basecls, ic_uicls):
    """Dialog for the importing culverts tool."""

    def __init__(self, model_gpkg, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.model_gpkg = model_gpkg
        self.import_settings = CulvertImportSettings()
        self.culvert_model = QStandardItemModel()
        self.culvert_tv.setModel(self.culvert_model)
        self.connection_node_model = QStandardItemModel()
        self.connection_node_tv.setModel(self.connection_node_model)
        self.data_models_tree_views = {
            dm.Culvert: (self.culvert_tv, self.culvert_model),
            dm.ConnectionNode: (self.connection_node_tv, self.connection_node_model),
        }
        self.populate_widgets()

    def populate_widgets(self):
        widgets_to_add = self.import_settings.culvert_widgets()
        for model_cls, (tree_view, tree_view_model) in self.data_models_tree_views.items():
            tree_view_model.clear()
            tree_view_model.setHorizontalHeaderLabels(self.import_settings.config_header)
            model_widgets = widgets_to_add[model_cls]
            for (row_idx, column_idx), widget in model_widgets.items():
                tree_view_model.setItem(row_idx, column_idx, QStandardItem(""))
                tree_view.setIndexWidget(tree_view_model.index(row_idx, column_idx), widget)
            for i in range(len(self.import_settings.config_header)):
                tree_view.resizeColumnToContents(i)
