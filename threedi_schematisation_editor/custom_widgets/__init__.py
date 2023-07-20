# Copyright (C) 2023 by Lutra Consulting
import ast
import json
import os

from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import QComboBox

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.custom_tools import ColumnImportMethod, CulvertImportSettings, import_culverts
from threedi_schematisation_editor.utils import (
    core_field_type,
    enum_entry_name_format,
    get_filepath,
    is_optional,
    optional_type,
)

ps_basecls, ps_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "projection_selection.ui"))
ic_basecls, ic_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "import_culverts.ui"))


class ProjectionSelectionDialog(ps_basecls, ps_uicls):
    """Dialog with selection of the desired projection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class ImportCulvertsDialog(ic_basecls, ic_uicls):
    """Dialog for the importing culverts tool."""

    def __init__(self, uc, model_gpkg, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.uc = uc
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
        self.culvert_layer_cbo.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.populate_conversion_settings_widgets()
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import_culverts)
        self.close_pb.clicked.connect(self.close)

    def populate_conversion_settings_widgets(self):
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

    def collect_settings(self):
        import_settings = {
            "target_layer": dm.Culvert.__tablename__,
            "conversion_settings": {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "create_connection_nodes": self.create_nodes_cb.isChecked(),
            },
            "fields": self.collect_fields_settings(dm.Culvert),
            "connection_node_fields": self.collect_fields_settings(dm.ConnectionNode),
        }
        return import_settings

    def collect_fields_settings(self, model_cls):
        fields_settings = {}
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        for row_idx, (field_name, field_type) in enumerate(model_cls.__annotations__.items()):
            single_field_config = {}
            field_type = core_field_type(field_type)
            for column_idx, key_name in enumerate(self.import_settings.config_keys, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                if isinstance(widget, QComboBox):
                    key_value = widget.currentData()
                else:
                    key_value = widget.text()
                    if not key_value:
                        continue
                    if key_name == "default_value" and key_name != "NULL":
                        key_value = field_type(key_value)
                    elif key_name == "value_map":
                        key_value = ast.literal_eval(key_value)
                single_field_config[key_name] = key_value
            fields_settings[field_name] = single_field_config
        return fields_settings

    def update_fields_settings(self, model_cls, fields_setting):
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        for row_idx, (field_name, field_type) in enumerate(model_cls.__annotations__.items()):
            if is_optional(field_type):
                field_type = optional_type(field_type)
            field_config = fields_setting.get(field_name, {})
            for column_idx, key_name in enumerate(self.import_settings.config_keys, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                try:
                    key_value = field_config[key_name]
                except KeyError:
                    continue
                if isinstance(widget, QComboBox):
                    if key_value == "NULL":
                        widget.setCurrentText(key_value)
                    else:
                        if key_name == "default_value":
                            widget.setCurrentText(enum_entry_name_format(field_type(key_value).name))
                        else:
                            widget.setCurrentText(enum_entry_name_format(ColumnImportMethod(key_value).name))
                else:
                    widget.setText(str(key_value))
                    widget.setCursorPosition(0)

    def save_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(self, extension_filter)
        import_settings = self.collect_settings()
        with open(template_filepath, "w") as template_file:
            json.dump(import_settings, template_file, indent=2)

    def load_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(self, extension_filter, save=False)
        with open(template_filepath, "r") as template_file:
            import_settings = json.loads(template_file.read())
        conversion_settings = import_settings["conversion_settings"]
        self.snap_gb.setChecked(conversion_settings.get("use_snapping", False))
        self.snap_dsb.setValue(conversion_settings.get("snapping_distance", 0.1))
        self.create_nodes_cb.setChecked(conversion_settings.get("create_connection_nodes", False))
        self.update_fields_settings(dm.Culvert, import_settings["fields"])
        try:
            connection_node_fields = import_settings["connection_node_fields"]
        except KeyError:
            return
        self.update_fields_settings(dm.ConnectionNode, connection_node_fields)

    def run_import_culverts(self):
        source_layer = self.culvert_layer_cbo.currentLayer()
        selected_feat_ids = None
        if self.selected_only_cb.isChecked():
            selected_feat_ids = source_layer.selectedFeatureIds()
        import_settings = self.collect_settings()
        success, commit_errors = import_culverts(
            source_layer, self.model_gpkg, import_settings, selected_ids=selected_feat_ids
        )
        if not success:
            commit_errors_message = "\n".join(commit_errors)
            self.uc.show_warn(f"Import failed due to the following errors:\n{commit_errors_message}")
        else:
            self.uc.show_info(f"Culverts successfully imported.")
