# Copyright (C) 2025 by Lutra Consulting
import ast
import json
import os
from functools import partial
from itertools import chain

from qgis.core import NULL, QgsMapLayerProxyModel, QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QItemSelectionModel, Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import QComboBox, QInputDialog, QTableWidgetItem

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.custom_tools import (
    ColumnImportMethod,
    CulvertsImporter,
    CulvertsIntegrator,
    OrificesImporter,
    OrificesIntegrator,
    PipesImporter,
    StructuresImportConfig,
    WeirsImporter,
    WeirsIntegrator,
)
from threedi_schematisation_editor.utils import (
    NULL_STR,
    QUOTED_NULL,
    REQUIRED_VALUE_STYLESHEET,
    core_field_type,
    enum_entry_name_format,
    get_filepath,
    is_optional,
    optional_type,
)

ic_basecls, ic_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "import_structures.ui"))
vm_basecls, vm_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "attribute_value_map.ui"))
load_basecls, load_uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "load_schematisation.ui"))


class AttributeValueMapDialog(vm_basecls, vm_uicls):
    """Dialog for setting attribute value mappings."""

    SRC_COLUMN_IDX = 0
    DST_COLUMN_IDX = 1

    def __init__(self, pressed_button, source_attribute_combobox, source_layer, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pressed_button = pressed_button
        self.source_attribute_combobox = source_attribute_combobox
        self.source_layer = source_layer
        self.add_pb.clicked.connect(self.add_value_map_row)
        self.delete_pb.clicked.connect(self.delete_value_map_rows)
        self.load_pb.clicked.connect(self.load_from_source_layer)
        self.header = ["Source attribute value", "Target attribute value"]
        self.populate_data()

    @staticmethod
    def format_value_map_data(data):
        """Create valid data string representation."""
        if isinstance(data, str):
            data_representation = f'"{data}"'
        elif data == NULL:
            data_representation = QUOTED_NULL
        else:
            data_representation = str(data)
        return data_representation

    def populate_data(self):
        """Populate attribute value map data in the table widget."""
        self.value_map_table.clearContents()
        self.value_map_table.setRowCount(0)
        self.value_map_table.setColumnCount(2)
        self.value_map_table.setHorizontalHeaderLabels(self.header)
        for row_number, (source_value, target_value) in enumerate(self.pressed_button.value_map.items()):
            source_value = self.format_value_map_data(source_value)
            target_value = self.format_value_map_data(target_value)
            self.value_map_table.insertRow(row_number)
            self.value_map_table.setItem(row_number, self.SRC_COLUMN_IDX, QTableWidgetItem(source_value))
            self.value_map_table.setItem(row_number, self.DST_COLUMN_IDX, QTableWidgetItem(target_value))
        self.value_map_table.resizeColumnsToContents()

    def add_value_map_row(self):
        """Slot for handling new row addition."""
        selected_rows = {idx.row() for idx in self.value_map_table.selectedIndexes()}
        if selected_rows:
            last_row_number = max(selected_rows) + 1
        else:
            last_row_number = self.value_map_table.rowCount()
        self.value_map_table.insertRow(last_row_number)

    def delete_value_map_rows(self):
        """Slot for handling deletion of the selected rows."""
        selected_rows = {idx.row() for idx in self.value_map_table.selectedIndexes()}
        for row in sorted(selected_rows, reverse=True):
            self.value_map_table.removeRow(row)

    def load_from_source_layer(self):
        """Slot for handling adding rows based on the source layer unique field values."""
        fields = self.source_layer.fields()
        src_layer_field_names = [field.name() for field in fields]
        title = "Load source layer values"
        message = "Unique values source field"
        source_attribute_idx = self.source_attribute_combobox.currentIndex()
        current_idx = source_attribute_idx - 1 if source_attribute_idx > 0 else 0
        selected_field_name, accept = QInputDialog.getItem(
            self, title, message, src_layer_field_names, current_idx, editable=False
        )
        if accept is True:
            row_count = self.value_map_table.rowCount()
            selected_field_name_idx = fields.lookupField(selected_field_name)
            selected_rows = {idx.row() for idx in self.value_map_table.selectedIndexes()}
            if selected_rows:
                last_row_number = max(selected_rows) + 1
            else:
                last_row_number = row_count
            unique_values = self.source_layer.uniqueValues(selected_field_name_idx)
            existing_values = {self.value_map_table.item(row, self.SRC_COLUMN_IDX).text() for row in range(row_count)}
            skipped_rows = 0
            for i, source_value in enumerate(sorted(unique_values), start=last_row_number):
                source_value_str = self.format_value_map_data(source_value)
                if source_value_str in existing_values:
                    skipped_rows += 1
                    continue
                new_row_number = i - skipped_rows
                self.value_map_table.insertRow(new_row_number)
                self.value_map_table.setItem(new_row_number, self.SRC_COLUMN_IDX, QTableWidgetItem(source_value_str))
                self.value_map_table.setItem(new_row_number, self.DST_COLUMN_IDX, QTableWidgetItem(QUOTED_NULL))

    @staticmethod
    def update_value_map_button(pressed_button, value_map):
        """Update value map button attributes."""
        pressed_button.value_map = value_map
        if value_map:
            value_map_str = str(value_map)[:10] + ".."
            pressed_button.setText(value_map_str)
        else:
            pressed_button.setText("Set..")

    def update_value_map(self):
        """Update value map with dictionary with defined data."""
        num_of_rows = self.value_map_table.rowCount()
        new_value_map = {}
        for row_num in range(num_of_rows):
            src_item = self.value_map_table.item(row_num, self.SRC_COLUMN_IDX)
            dst_item = self.value_map_table.item(row_num, self.DST_COLUMN_IDX)
            src_value = ast.literal_eval(src_item.text())
            dst_value = ast.literal_eval(dst_item.text())
            new_value_map[src_value] = dst_value
        self.update_value_map_button(self.pressed_button, new_value_map)


class ImportStructuresDialog(ic_basecls, ic_uicls):
    """Dialog for the importing structures tool."""

    STRUCTURE_IMPORTERS = {
        dm.Culvert: CulvertsImporter,
        dm.Orifice: OrificesImporter,
        dm.Weir: WeirsImporter,
        dm.Pipe: PipesImporter,
    }
    STRUCTURE_INTEGRATORS = {
        dm.Culvert: CulvertsIntegrator,
        dm.Orifice: OrificesIntegrator,
        dm.Weir: WeirsIntegrator,
    }

    LAST_CONFIG_DIR_ENTRY = "threedi/last_import_config_dir"

    def __init__(self, structure_model_cls, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.structure_model_cls = structure_model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc
        self.import_configuration = StructuresImportConfig(self.structure_model_cls)
        self.structure_model = QStandardItemModel()
        self.structure_tv.setModel(self.structure_model)
        self.connection_node_model = QStandardItemModel()
        self.connection_node_tv.setModel(self.connection_node_model)
        self.data_models_tree_views = {
            self.structure_model_cls: (self.structure_tv, self.structure_model),
            dm.ConnectionNode: (self.connection_node_tv, self.connection_node_model),
        }
        self.structure_layer_cbo.setFilters(
            QgsMapLayerProxyModel.PointLayer
            if self.structure_model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )
        self.structure_layer_cbo.setCurrentIndex(0)
        self.populate_conversion_settings_widgets()
        self.structure_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.create_nodes_cb.stateChanged.connect(self.on_create_nodes_change)
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import_structures)
        self.close_pb.clicked.connect(self.close)
        self.setup_labels()
        if not self.enable_structures_integration:
            for widget in self.structures_integration_widgets:
                widget.hide()

    def setup_labels(self):
        structure_name = self.structure_model_cls.__layername__
        structure_name_lower = structure_name.lower()
        self.setWindowTitle(self.windowTitle().format(structure_name_lower))
        self.structure_layer_label.setText(self.structure_layer_label.text().format(structure_name_lower))
        self.tab_widget.setTabText(0, self.tab_widget.tabText(0).format(structure_name))

    @staticmethod
    def is_obsolete_field(model_cls, field_name):
        return field_name in model_cls.obsolete_fields()

    @property
    def enable_structures_integration(self):
        return self.structure_model_cls in self.STRUCTURE_INTEGRATORS

    @property
    def structures_integration_widgets(self):
        return [
            self.edit_channels_cb,
            self.length_source_field_lbl,
            self.length_source_field_cbo,
            self.length_fallback_value_lbl,
            self.length_fallback_value_dsb,
            self.azimuth_source_field_lbl,
            self.azimuth_source_field_cbo,
            self.azimuth_fallback_value_lbl,
            self.azimuth_fallback_value_sb,
        ]

    @property
    def source_layer(self):
        return self.structure_layer_cbo.currentLayer()

    @property
    def layer_dependent_widgets(self):
        widgets = [
            self.tab_widget,
            self.save_pb,
            self.load_pb,
            self.run_pb,
            self.selected_only_cb,
            self.create_nodes_cb,
            self.snap_gb,
        ]
        if self.enable_structures_integration:
            widgets += self.structures_integration_widgets
        return widgets

    def activate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setEnabled(True)

    def deactivate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setDisabled(True)

    def on_create_nodes_change(self, is_checked):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
            self.activate_layer_dependent_widgets()
            self.length_source_field_cbo.setLayer(layer)
            self.azimuth_source_field_cbo.setLayer(layer)
        else:
            self.deactivate_layer_dependent_widgets()
            self.length_source_field_cbo.setLayer(None)
            self.azimuth_source_field_cbo.setLayer(None)
        data_models = [self.structure_model_cls, dm.ConnectionNode]
        source_attribute_widgets = self.get_column_widgets(
            StructuresImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX, *data_models
        )
        for combobox in chain.from_iterable(source_attribute_widgets.values()):
            combobox.clear()
            combobox.addItems(layer_field_names)
            combobox.setCurrentText(combobox.data_model_field_name)
        expression_widgets = self.get_column_widgets(StructuresImportConfig.EXPRESSION_COLUMN_IDX, *data_models)
        for expression_widget in chain.from_iterable(expression_widgets.values()):
            expression_widget.setLayer(layer)

    @staticmethod
    def on_method_changed(source_attribute_combobox, value_map_widget, expression_widget, current_text):
        if current_text != str(ColumnImportMethod.ATTRIBUTE):
            source_attribute_combobox.setDisabled(True)
            value_map_widget.setDisabled(True)
            source_attribute_combobox.setStyleSheet("")
            expression_widget.setEnabled(current_text == str(ColumnImportMethod.EXPRESSION))
        else:
            source_attribute_combobox.setEnabled(True)
            value_map_widget.setEnabled(True)
            expression_widget.setDisabled(True)
            if source_attribute_combobox.currentText():
                source_attribute_combobox.setStyleSheet("")
            else:
                source_attribute_combobox.setStyleSheet(REQUIRED_VALUE_STYLESHEET)

    @staticmethod
    def on_source_attribute_value_changed(method_combobox, source_attribute_combobox, current_text):
        if method_combobox.currentText() == str(ColumnImportMethod.ATTRIBUTE) and not current_text:
            source_attribute_combobox.setStyleSheet(REQUIRED_VALUE_STYLESHEET)
        else:
            source_attribute_combobox.setStyleSheet("")

    def on_value_map_clicked(self, source_attribute_combobox, pressed_button):
        value_map_dlg = AttributeValueMapDialog(pressed_button, source_attribute_combobox, self.source_layer, self)
        accepted = value_map_dlg.exec_()
        if accepted:
            try:
                value_map_dlg.update_value_map()
            except (SyntaxError, ValueError):
                self.uc.show_error(f"Invalid value map. Action aborted.", self)

    def get_column_widgets(self, column_idx, *data_models):
        column_widgets = {}
        for model_cls in data_models:
            model_widgets = []
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            row_idx = 0
            for field_name in model_cls.__annotations__.keys():
                if self.is_obsolete_field(model_cls, field_name):
                    continue
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                widget.data_model_field_name = field_name
                model_widgets.append(widget)
                row_idx += 1
            column_widgets[model_cls] = model_widgets
        return column_widgets

    def populate_conversion_settings_widgets(self):
        widgets_to_add = self.import_configuration.structure_widgets()
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
        self.on_layer_changed(self.source_layer)

    def connect_configuration_widgets(self):
        data_models = [self.structure_model_cls, dm.ConnectionNode]
        for model_cls in data_models:
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            row_idx = 0
            for field_name in model_cls.__annotations__.keys():
                if self.is_obsolete_field(model_cls, field_name):
                    continue
                method_item = tree_view_model.item(row_idx, StructuresImportConfig.METHOD_COLUMN_IDX)
                method_index = method_item.index()
                method_combobox = tree_view.indexWidget(method_index)
                source_attribute_item = tree_view_model.item(
                    row_idx, StructuresImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX
                )
                source_attribute_index = source_attribute_item.index()
                source_attribute_combobox = tree_view.indexWidget(source_attribute_index)
                value_map_item = tree_view_model.item(row_idx, StructuresImportConfig.VALUE_MAP_COLUMN_IDX)
                value_map_index = value_map_item.index()
                value_map_button = tree_view.indexWidget(value_map_index)
                expression_item = tree_view_model.item(row_idx, StructuresImportConfig.EXPRESSION_COLUMN_IDX)
                expression_index = expression_item.index()
                expression_widget = tree_view.indexWidget(expression_index)
                method_combobox.currentTextChanged.connect(
                    partial(self.on_method_changed, source_attribute_combobox, value_map_button, expression_widget)
                )
                method_combobox.currentTextChanged.emit(method_combobox.currentText())
                source_attribute_combobox.currentTextChanged.connect(
                    partial(self.on_source_attribute_value_changed, method_combobox, source_attribute_combobox)
                )
                value_map_button.clicked.connect(
                    partial(self.on_value_map_clicked, source_attribute_combobox, value_map_button)
                )
                row_idx += 1

    def collect_settings(self):
        import_settings = {
            "target_layer": self.structure_model_cls.__tablename__,
            "conversion_settings": {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "create_connection_nodes": self.create_nodes_cb.isChecked(),
                "length_source_field": self.length_source_field_cbo.currentField(),
                "length_fallback_value": self.length_fallback_value_dsb.value(),
                "azimuth_source_field": self.azimuth_source_field_cbo.currentField(),
                "azimuth_fallback_value": self.azimuth_fallback_value_sb.value(),
                "edit_channels": self.edit_channels_cb.isChecked(),
            },
            "fields": self.collect_fields_settings(self.structure_model_cls),
            "connection_node_fields": self.collect_fields_settings(dm.ConnectionNode),
        }
        return import_settings

    def collect_fields_settings(self, model_cls):
        fields_settings = {}
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(model_cls, field_name):
                continue
            single_field_config = {}
            field_type = core_field_type(field_type)
            for column_idx, key_name in enumerate(self.import_configuration.config_keys, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                if isinstance(widget, QComboBox):
                    key_value = (
                        widget.currentText()
                        if column_idx == StructuresImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX
                        else widget.currentData()
                    )
                elif column_idx == StructuresImportConfig.VALUE_MAP_COLUMN_IDX:
                    key_value = widget.value_map
                    if not key_value:
                        continue
                elif column_idx == StructuresImportConfig.EXPRESSION_COLUMN_IDX:
                    if not widget.isValidExpression():
                        continue
                    key_value = widget.expression()
                else:
                    key_value = widget.text()
                    if not key_value:
                        continue
                    if column_idx == StructuresImportConfig.DEFAULT_VALUE_COLUMN_IDX and key_name != NULL_STR:
                        key_value = field_type(key_value)
                single_field_config[key_name] = key_value
            fields_settings[field_name] = single_field_config
            row_idx += 1
        return fields_settings

    def update_fields_settings(self, model_cls, fields_setting):
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(model_cls, field_name):
                continue
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
                    if key_value == NULL_STR:
                        widget.setCurrentText(key_value)
                    else:
                        if key_name == "method":
                            widget.setCurrentText(enum_entry_name_format(ColumnImportMethod(key_value).name))
                        elif key_name == "default_value" and field_type != bool:
                            widget.setCurrentText(enum_entry_name_format(field_type(key_value).name))
                        else:
                            widget.setCurrentText(str(key_value))
                elif key_name == "value_map":
                    AttributeValueMapDialog.update_value_map_button(widget, key_value)
                elif key_name == "expression":
                    widget.setExpression(key_value)
                else:
                    widget.setText(str(key_value))
                    widget.setCursorPosition(0)
            row_idx += 1

    def save_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(self, extension_filter, default_settings_entry=self.LAST_CONFIG_DIR_ENTRY)
        if not template_filepath:
            return
        settings = QgsSettings()
        settings.setValue(self.LAST_CONFIG_DIR_ENTRY, os.path.dirname(template_filepath))
        try:
            import_settings = self.collect_settings()
            with open(template_filepath, "w") as template_file:
                json.dump(import_settings, template_file, indent=2)
            self.uc.show_info(f"Settings saved to the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def load_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(
            self, extension_filter, save=False, default_settings_entry=self.LAST_CONFIG_DIR_ENTRY
        )
        if not template_filepath:
            return
        settings = QgsSettings()
        settings.setValue(self.LAST_CONFIG_DIR_ENTRY, os.path.dirname(template_filepath))
        try:
            with open(template_filepath, "r") as template_file:
                import_settings = json.loads(template_file.read())
            conversion_settings = import_settings["conversion_settings"]
            self.snap_gb.setChecked(conversion_settings.get("use_snapping", False))
            self.snap_dsb.setValue(conversion_settings.get("snapping_distance", 0.1))
            self.create_nodes_cb.setChecked(conversion_settings.get("create_connection_nodes", False))
            self.edit_channels_cb.setChecked(conversion_settings.get("edit_channels", False))
            self.length_source_field_cbo.setField(conversion_settings.get("length_source_field", ""))
            self.length_fallback_value_dsb.setValue(conversion_settings.get("length_fallback_value", 10.0))
            self.azimuth_source_field_cbo.setField(conversion_settings.get("azimuth_source_field", ""))
            self.azimuth_fallback_value_sb.setValue(conversion_settings.get("azimuth_fallback_value", 90))
            self.update_fields_settings(self.structure_model_cls, import_settings["fields"])
            try:
                connection_node_fields = import_settings["connection_node_fields"]
                self.update_fields_settings(dm.ConnectionNode, connection_node_fields)
            except KeyError:
                pass
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def missing_source_fields(self):
        data_models = [self.structure_model_cls]
        if self.create_nodes_cb.isChecked():
            data_models.append(dm.ConnectionNode)
        field_labels = self.get_column_widgets(StructuresImportConfig.FIELD_NAME_COLUMN_IDX, *data_models)
        method_widgets = self.get_column_widgets(StructuresImportConfig.METHOD_COLUMN_IDX, *data_models)
        source_attribute_widgets = self.get_column_widgets(
            StructuresImportConfig.SOURCE_ATTRIBUTE_COLUMN_IDX, *data_models
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
                if method_txt == str(ColumnImportMethod.ATTRIBUTE) and not source_attribute_txt:
                    model_missing_fields.append(field_name)
            if model_missing_fields:
                missing_fields[model_cls] = model_missing_fields
        return missing_fields

    def run_import_structures(self):
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
        source_layer = self.source_layer
        structures_handler = self.layer_manager.model_handlers[self.structure_model_cls]
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
        structure_layer = structures_handler.layer
        node_layer = node_handler.layer
        channel_layer = channel_handler.layer
        cross_section_location_layer = cross_section_location_handler.layer
        selected_feat_ids = None
        if self.selected_only_cb.isChecked():
            selected_feat_ids = source_layer.selectedFeatureIds()
        import_settings = self.collect_settings()
        conversion_settings = import_settings["conversion_settings"]
        edit_channels = conversion_settings.get("edit_channels", False)
        if edit_channels:
            structure_importer_cls = self.STRUCTURE_INTEGRATORS[self.structure_model_cls]
        else:
            structure_importer_cls = self.STRUCTURE_IMPORTERS[self.structure_model_cls]
        processed_handlers = [structures_handler, node_handler]
        processed_layers = {"structure_layer": structure_layer, "node_layer": node_layer}
        if edit_channels:
            processed_handlers += [channel_handler, cross_section_location_handler]
            processed_layers["channel_layer"] = channel_layer
            processed_layers["cross_section_location_layer"] = cross_section_location_layer
        try:
            for handler in processed_handlers:
                handler.disconnect_handler_signals()
            structures_importer = structure_importer_cls(
                source_layer,
                self.model_gpkg,
                import_settings,
                **processed_layers,
            )
            structures_importer.import_structures(selected_ids=selected_feat_ids)
            success_msg = (
                "Features imported successfully.\n\n"
                "The layers to which the features have been added are still in editing mode, "
                "so you can review the changes before saving them to the layers."
            )
            self.uc.show_info(success_msg, self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)
        finally:
            for handler in processed_handlers:
                handler.connect_handler_signals()
        for layer in processed_layers.values():
            layer.triggerRepaint()


class LoadSchematisationDialog(load_basecls, load_uicls):
    """Dialog for loading schematisation."""

    def __init__(self, uc, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.uc = uc
        self.schematisation_model = QStandardItemModel()
        self.schematisation_tv.setModel(self.schematisation_model)
        self.schematisation_list_header = ["Schematisation", "Revision"]
        self.settings = QgsSettings()
        self.working_dir = self.settings.value("threedi/working_dir", "", type=str)
        if self.working_dir:
            self.file_browse_widget.setDefaultRoot(self.working_dir)
        self.selected_schematisation_filepath = None
        self.schematisation_tv.doubleClicked.connect(self.set_schematisation_filepath)
        self.load_pb.clicked.connect(self.set_schematisation_filepath)
        self.cancle_pb.clicked.connect(self.reject)
        self.list_working_dir_schematisations()

    def list_working_dir_schematisations(self):
        """Populate 3Di Working Directory schematisations."""
        try:
            from threedi_mi_utils import WIPRevision, list_local_schematisations, replace_revision_data
        except ImportError:
            self.missing_lib_label.setHidden(False)
            return
        self.missing_lib_label.setHidden(True)
        if not self.working_dir:
            return
        self.schematisation_model.clear()
        self.schematisation_model.setHorizontalHeaderLabels(self.schematisation_list_header)
        local_schematisations = list_local_schematisations(self.working_dir, use_config_for_revisions=False)
        last_used_schematisation_dir = self.settings.value("threedi/last_schematisation_folder", "")
        last_used_schematisation_row_number = None
        for local_schematisation in local_schematisations.values():
            local_schematisation_name = local_schematisation.name
            wip_revision = local_schematisation.wip_revision
            try:
                wip_revision_gpkg = wip_revision.geopackage_filepath
            except (AttributeError, FileNotFoundError):
                wip_revision_gpkg = None
            if wip_revision_gpkg is not None:
                schematisation_name_item = QStandardItem(local_schematisation_name)
                revision_number_str = f"{wip_revision.number} (work in progress)"
                revision_number_item = QStandardItem(revision_number_str)
                revision_number_item.setData(wip_revision_gpkg, Qt.UserRole)
                self.schematisation_model.appendRow([schematisation_name_item, revision_number_item])
                if wip_revision.schematisation_dir == last_used_schematisation_dir:
                    last_used_schematisation_row_number = self.schematisation_model.rowCount() - 1
            for revision_number, revision in local_schematisation.revisions.items():
                try:
                    revision_gpkg = revision.geopackage_filepath
                    if revision_gpkg is None:
                        continue
                except FileNotFoundError:
                    continue
                schematisation_name_item = QStandardItem(local_schematisation_name)
                revision_number_item = QStandardItem(str(revision.number))
                revision_number_item.setData(revision_gpkg, Qt.UserRole)
                self.schematisation_model.appendRow([schematisation_name_item, revision_number_item])
                if revision.schematisation_dir == last_used_schematisation_dir:
                    last_used_schematisation_row_number = self.schematisation_model.rowCount() - 1
        for i in range(len(self.schematisation_list_header)):
            self.schematisation_tv.resizeColumnToContents(i)
        if last_used_schematisation_row_number is not None:
            last_used_schematisation_row_idx = self.schematisation_model.index(last_used_schematisation_row_number, 0)
            self.schematisation_tv.selectionModel().setCurrentIndex(
                last_used_schematisation_row_idx, QItemSelectionModel.ClearAndSelect
            )
            self.schematisation_tv.scrollTo(last_used_schematisation_row_idx)

    def set_schematisation_filepath(self):
        """Set selected schematisation filepath."""
        if self.load_tab.currentIndex() == 0:
            index = self.schematisation_tv.currentIndex()
            if not index.isValid():
                self.uc.show_warn("Nothing selected. Please select schematisation revision to continue.", parent=self)
                return
            current_row = index.row()
            revision_item = self.schematisation_model.item(current_row, 1)
            revision_gpkg = revision_item.data(Qt.UserRole)
            self.selected_schematisation_filepath = revision_gpkg
        else:
            selected_filepath = self.file_browse_widget.filePath()
            if not selected_filepath:
                self.uc.show_warn("No file selected. Please select schematisation file to continue.", parent=self)
                return
            self.selected_schematisation_filepath = self.file_browse_widget.filePath()
        self.accept()
