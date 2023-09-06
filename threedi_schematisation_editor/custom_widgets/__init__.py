# Copyright (C) 2023 by Lutra Consulting
import ast
import json
import os
from functools import partial
from itertools import chain

from qgis.core import QgsMapLayerProxyModel
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import QComboBox

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.custom_tools import ColumnImportMethod, CulvertImportConfig, CulvertsImporter
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

    REQUIRED_VALUE_STYLESHEET = "background-color: rgb(255, 224, 178);"

    def __init__(self, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc
        self.import_configuration = CulvertImportConfig()
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
        self.culvert_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.create_nodes_cb.stateChanged.connect(self.on_create_nodes_change)
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import_culverts)
        self.close_pb.clicked.connect(self.close)

    def on_create_nodes_change(self, is_checked):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
        source_attribute_widgets = self.get_column_widgets(
            CulvertImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX, dm.Culvert, dm.ConnectionNode
        )
        for combobox in chain.from_iterable(source_attribute_widgets.values()):
            combobox.clear()
            combobox.addItems(layer_field_names)

    def on_method_changed(self, source_attribute_combobox, value_map_widget, current_text):
        if current_text != ColumnImportMethod.ATTRIBUTE.name.capitalize():
            source_attribute_combobox.setDisabled(True)
            value_map_widget.setDisabled(True)
            source_attribute_combobox.setStyleSheet("")
        else:
            source_attribute_combobox.setEnabled(True)
            value_map_widget.setEnabled(True)
            if source_attribute_combobox.currentText():
                source_attribute_combobox.setStyleSheet("")
            else:
                source_attribute_combobox.setStyleSheet(self.REQUIRED_VALUE_STYLESHEET)

    def on_source_attribute_value_changed(self, method_combobox, source_attribute_combobox, current_text):
        if method_combobox.currentText() == ColumnImportMethod.ATTRIBUTE.name.capitalize() and not current_text:
            source_attribute_combobox.setStyleSheet(self.REQUIRED_VALUE_STYLESHEET)
        else:
            source_attribute_combobox.setStyleSheet("")

    def get_column_widgets(self, column_idx, *data_models):
        column_widgets = {}
        for model_cls in data_models:
            model_widgets = []
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            for row_idx, field_name in enumerate(model_cls.__annotations__.keys()):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                model_widgets.append(widget)
            column_widgets[model_cls] = model_widgets
        return column_widgets

    def populate_conversion_settings_widgets(self):
        widgets_to_add = self.import_configuration.culvert_widgets()
        for model_cls, (tree_view, tree_view_model) in self.data_models_tree_views.items():
            tree_view_model.clear()
            tree_view_model.setHorizontalHeaderLabels(self.import_configuration.config_header)
            model_widgets = widgets_to_add[model_cls]
            for (row_idx, column_idx), widget in model_widgets.items():
                tree_view_model.setItem(row_idx, column_idx, QStandardItem(""))
                tree_view.setIndexWidget(tree_view_model.index(row_idx, column_idx), widget)
            for i in range(len(self.import_configuration.config_header)):
                tree_view.resizeColumnToContents(i)
        self.connect_configuration_widgets()
        self.on_layer_changed(self.culvert_layer_cbo.currentLayer())

    def connect_configuration_widgets(self):
        for model_cls in [dm.Culvert, dm.ConnectionNode]:
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            for row_idx, field_name in enumerate(model_cls.__annotations__.keys()):
                method_item = tree_view_model.item(row_idx, CulvertImportConfig.METHOD_COLUMN_IDX)
                method_index = method_item.index()
                method_combobox = tree_view.indexWidget(method_index)
                source_attribute_item = tree_view_model.item(row_idx, CulvertImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX)
                source_attribute_index = source_attribute_item.index()
                source_attribute_combobox = tree_view.indexWidget(source_attribute_index)
                value_map_item = tree_view_model.item(row_idx, CulvertImportConfig.VALUE_MAP_COLUMN_IDX)
                value_map_index = value_map_item.index()
                value_map_widget = tree_view.indexWidget(value_map_index)
                method_combobox.currentTextChanged.connect(
                    partial(self.on_method_changed, source_attribute_combobox, value_map_widget)
                )
                method_combobox.currentTextChanged.emit(method_combobox.currentText())
                source_attribute_combobox.currentTextChanged.connect(
                    partial(self.on_source_attribute_value_changed, method_combobox, source_attribute_combobox)
                )

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
            for column_idx, key_name in enumerate(self.import_configuration.config_keys, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                if isinstance(widget, QComboBox):
                    key_value = (
                        widget.currentText()
                        if column_idx == CulvertImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX
                        else widget.currentData()
                    )
                else:
                    key_value = widget.text()
                    if not key_value:
                        continue
                    if column_idx == CulvertImportConfig.DEFAULT_VALUE_COLUMN_IDX and key_name != "NULL":
                        key_value = field_type(key_value)
                    elif column_idx == CulvertImportConfig.VALUE_MAP_COLUMN_IDX:
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
            for column_idx, key_name in enumerate(self.import_configuration.config_keys, start=1):
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
                        if key_name == "method":
                            widget.setCurrentText(enum_entry_name_format(ColumnImportMethod(key_value).name))
                        elif key_name == "default_value":
                            widget.setCurrentText(enum_entry_name_format(field_type(key_value).name))
                        else:
                            widget.setCurrentText(str(key_value))
                else:
                    widget.setText(str(key_value))
                    widget.setCursorPosition(0)

    def save_import_settings(self):
        try:
            extension_filter = "JSON (*.json)"
            template_filepath = get_filepath(self, extension_filter)
            import_settings = self.collect_settings()
            with open(template_filepath, "w") as template_file:
                json.dump(import_settings, template_file, indent=2)
            self.uc.show_info(f"Settings saved to the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def load_import_settings(self):
        try:
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
                self.update_fields_settings(dm.ConnectionNode, connection_node_fields)
            except KeyError:
                pass
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def missing_source_fields(self):
        data_models = [dm.Culvert]
        if self.create_nodes_cb.isChecked():
            data_models.append(dm.ConnectionNode)
        field_labels = self.get_column_widgets(CulvertImportConfig.FIELD_NAME_COLUMN_IDX, *data_models)
        method_widgets = self.get_column_widgets(CulvertImportConfig.METHOD_COLUMN_IDX, *data_models)
        source_attribute_widgets = self.get_column_widgets(
            CulvertImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX, *data_models
        )
        missing_fields = {}
        for model_cls in data_models:
            model_missing_fields = []
            model_field_labels, model_method_widgets, model_source_attribute_widgets = [
                column_widgets[model_cls] for column_widgets in [field_labels, method_widgets, source_attribute_widgets]
            ]
            for field_lbl, method_cbo, source_attribute_cbo in zip(
                model_field_labels, model_method_widgets, model_source_attribute_widgets
            ):
                field_name, method_txt, source_attribute_txt = (
                    field_lbl.text().strip(),
                    method_cbo.currentText(),
                    source_attribute_cbo.currentText(),
                )
                if method_txt == ColumnImportMethod.ATTRIBUTE.name.capitalize() and not source_attribute_txt:
                    model_missing_fields.append(field_name)
            missing_fields[model_cls] = model_missing_fields
        return missing_fields

    def run_import_culverts(self):
        missing_fields = self.missing_source_fields()
        if missing_fields:
            missing_fields_lines = []
            for model_cls, model_missing_fields in missing_fields.items():
                model_name = model_cls.__layername__
                for missing_field in model_missing_fields:
                    missing_fields_lines.append(f"{model_name}: {missing_field}")
            missing_fields_txt = "\n".join(missing_fields_lines)
            self.uc.show_warn(
                f"Please specify a source field for a following attribute(s) and try again:\n{missing_fields_txt}", self
            )
            return
        source_layer = self.culvert_layer_cbo.currentLayer()
        culvert_handler = self.layer_manager.model_handlers[dm.Culvert]
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        culvert_layer = culvert_handler.layer
        node_layer = node_handler.layer
        selected_feat_ids = None
        if self.selected_only_cb.isChecked():
            selected_feat_ids = source_layer.selectedFeatureIds()
        import_settings = self.collect_settings()
        try:
            culvert_handler.disconnect_handler_signals()
            node_handler.disconnect_handler_signals()
            culverts_importer = CulvertsImporter(
                source_layer, self.model_gpkg, import_settings, culvert_layer=culvert_layer, node_layer=node_layer
            )
            success, commit_errors = culverts_importer.import_culverts(selected_ids=selected_feat_ids)
            if not success:
                commit_errors_message = "\n".join(commit_errors)
                self.uc.show_warn(f"Import failed due to the following errors:\n{commit_errors_message}")
            else:
                self.uc.show_info(f"Culverts successfully imported.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)
        finally:
            culvert_handler.connect_handler_signals()
            node_handler.connect_handler_signals()
        for layer in [culvert_layer, node_layer]:
            layer.triggerRepaint()
