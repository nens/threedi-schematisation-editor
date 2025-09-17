from collections import defaultdict
from enum import Enum
from functools import cached_property, partial
from itertools import chain
from typing import Any, Dict, List

from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from threedi_schematisation_editor.utils import (
    enum_entry_name_format,
    is_optional,
    optional_type,
)
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import (
    ColumnImportIndex,
    ImportFieldMappingUtils,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


def get_field_methods_mapping(
    model_cls,
    field_spec=None,
):
    """Return a mapping of fields to import methods."""
    methods_mapping = {}
    for field_name in model_cls.__annotations__.keys():
        if field_spec and field_name in field_spec:
            fields = field_spec[field_name]
        elif field_name == "id":
            fields = [ColumnImportMethod.AUTO]
        else:
            fields = [
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.DEFAULT,
                ColumnImportMethod.EXPRESSION,
                ColumnImportMethod.IGNORE,
            ]
        methods_mapping[field_name] = fields
    return methods_mapping


def create_widgets(
    model_cls,
    field_spec=None,
):
    """Create widgets for the data model fields."""
    fields_mapping = get_field_methods_mapping(model_cls, field_spec)
    model_obsolete_fields = model_cls.obsolete_fields()
    model_fields_display_names = model_cls.fields_display_names()
    row_idx = 0
    widgets_to_add = {}
    for field_name, field_methods in fields_mapping.items():
        if field_name in model_obsolete_fields:
            continue
        if field_name not in model_fields_display_names:
            continue
        field_type = model_cls.__annotations__[field_name]
        if is_optional(field_type):
            field_type = optional_type(field_type)

        for column_idx, column_name in enumerate(CONFIG_HEADER):
            if column_idx == ColumnImportIndex.FIELD_NAME_COLUMN_IDX:
                widget = create_label_widget(model_fields_display_names[field_name])
            elif column_idx == ColumnImportIndex.METHOD_COLUMN_IDX:
                widget = create_method_widget(field_methods)
            elif column_idx == ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX:
                widget = create_combobox_widget()
                if ColumnImportMethod.ATTRIBUTE not in field_methods:
                    widget.setDisabled(True)
            elif column_idx == ColumnImportIndex.VALUE_MAP_COLUMN_IDX:
                # todo: disable value map in some cases?
                widget = create_set_value_map_widget()
            elif column_idx == ColumnImportIndex.EXPRESSION_COLUMN_IDX:
                widget = create_expression_widget()
                if ColumnImportMethod.EXPRESSION not in field_methods:
                    widget.setDisabled(True)
            elif column_idx == ColumnImportIndex.DEFAULT_VALUE_COLUMN_IDX:
                widget = create_default_value_widget(field_type)
                if ColumnImportMethod.DEFAULT not in field_methods:
                    widget.setDisabled(True)
            widgets_to_add[row_idx, column_idx] = widget
        row_idx += 1

    return widgets_to_add


def create_label_widget(field_display_name):
    return QLabel(f"{field_display_name}\t")


def create_method_widget(field_methods):
    items = [[method.name.capitalize(), method.value] for method in field_methods]
    return create_combobox_widget(items)


def create_combobox_widget(items=None):
    widget = QComboBox()
    if items:
        for item in items:
            widget.addItem(*item)
    return widget


def create_set_value_map_widget():
    widget = QPushButton("Set...")
    widget.value_map = {}
    return widget


def create_expression_widget():
    return QgsFieldExpressionWidget()


def create_default_value_widget(field_type):
    if issubclass(field_type, Enum) or field_type == bool:
        if field_type == bool:
            items = [["False", False], ["True", True]]
        else:
            items = [["NULL", "NULL"]] + [
                [enum_entry_name_format(e), e.value] for e in field_type
            ]
        return create_combobox_widget(items)
    else:
        return QLineEdit()


CONFIG_HEADER = [
    "Field name",
    "Method",
    "Source attribute",
    "Value map",
    "Default value",
    "Expression",
]
CONFIG_KEYS = ["method", "source_attribute", "value_map", "default_value", "expression"]


class FieldMapWidget(QWidget):
    def __init__(self, model_cls, widgets, parent=None):
        super().__init__(parent)
        # Create table view and models
        self.table_view = QTableView(self)
        self.table_view.verticalHeader().setVisible(False)
        self.model = QStandardItemModel()
        self.table_view.setModel(self.model)
        self.model_cls = model_cls
        # Create widgets and add them to the table view and model
        self._create(widgets)
        # Setup widget layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def _create(self, widgets):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(CONFIG_HEADER)
        for (row_idx, column_idx), widget in widgets.items():
            self.model.setItem(row_idx, column_idx, QStandardItem(""))
            self.table_view.setIndexWidget(
                self.model.index(row_idx, column_idx), widget
            )
        for i in range(len(CONFIG_HEADER)):
            self.table_view.resizeColumnToContents(i)

    def connect(self, source_layer_cbo, uc, parent):
        row_idx = 0
        for field_name in self.model_cls.__annotations__.keys():
            if field_name in self.model_cls.obsolete_fields():
                continue
            method_combobox = self.get_widget(
                row_idx, ColumnImportIndex.METHOD_COLUMN_IDX
            )
            source_attribute_combobox = self.get_widget(
                row_idx, ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX
            )
            expression_widget = self.get_widget(
                row_idx, ColumnImportIndex.EXPRESSION_COLUMN_IDX
            )
            value_map_button = self.get_widget(
                row_idx, ColumnImportIndex.VALUE_MAP_COLUMN_IDX
            )
            method_combobox.currentTextChanged.connect(
                partial(
                    ImportFieldMappingUtils.on_method_changed,
                    source_attribute_combobox,
                    value_map_button,
                    expression_widget,
                )
            )
            method_combobox.currentTextChanged.emit(method_combobox.currentText())
            source_attribute_combobox.currentTextChanged.connect(
                partial(
                    ImportFieldMappingUtils.on_source_attribute_value_changed,
                    method_combobox,
                    source_attribute_combobox,
                )
            )
            value_map_button.clicked.connect(
                partial(
                    ImportFieldMappingUtils.on_value_map_clicked,
                    source_layer_cbo,
                    source_attribute_combobox,
                    value_map_button,
                    uc,
                    parent,
                )
            )
            row_idx += 1

    def get_widget(self, row_idx, col_idx):
        return self.table_view.indexWidget(self.model.item(row_idx, col_idx).index())

    def collect_fields_settings(self) -> Dict[str, Any]:
        fields_settings = {}
        row_idx = 0
        for field_name, field_type in self.model_cls.__annotations__.items():
            if field_name in self.model_cls.obsolete_fields():
                continue
            field_config = {}
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                widget = self.get_widget(row_idx, column_idx)
                config = ImportFieldMappingUtils.collect_config_from_widget(
                    widget, key_name, field_type, column_idx
                )
                if config is not None:
                    field_config[key_name] = config
            fields_settings[field_name] = field_config
            row_idx += 1
        return fields_settings

    def get_column_widgets(self, column_idx: int) -> List[QWidget]:
        model_widgets = []
        row_idx = 0
        for field_name in self.model_cls.__annotations__.keys():
            if field_name in self.model_cls.obsolete_fields():
                continue
            widget = self.get_widget(row_idx, column_idx)
            widget.data_model_field_name = field_name
            model_widgets.append(widget)
            row_idx += 1
        return model_widgets

    @cached_property
    def source_attribute_widgets(self):
        return self.get_column_widgets(ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX)

    @cached_property
    def field_labels(self):
        return self.get_column_widgets(ColumnImportIndex.FIELD_NAME_COLUMN_IDX)

    @cached_property
    def method_widgets(self):
        return self.get_column_widgets(ColumnImportIndex.METHOD_COLUMN_IDX)

    @cached_property
    def expression_widgets(self):
        return self.get_column_widgets(ColumnImportIndex.EXPRESSION_COLUMN_IDX)

    def get_missing_fields(self):
        missing_fields = []
        for field_lbl, method_cbo, source_attribute_cbo in zip(
            self.field_labels, self.method_widgets, self.source_attribute_widgets
        ):
            field_name, method_txt, source_attribute_txt = (
                field_lbl.text().strip(),
                method_cbo.currentText(),
                source_attribute_cbo.currentText(),
            )
            if (
                method_txt == str(ColumnImportMethod.ATTRIBUTE)
                and not source_attribute_txt
            ):
                missing_fields.append(field_name)
        return missing_fields

    def reset(self):
        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                widget = self.get_widget(row, col)
                # Reset widgets based on their type
                if isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0)
                elif isinstance(widget, QLineEdit):
                    widget.setText("")
                elif isinstance(widget, QgsFieldExpressionWidget):
                    widget.setExpression("")

    def set(self, fields_setting: Dict[str, Any]):
        row_idx = 0
        for field_name, field_type in self.model_cls.__annotations__.items():
            if field_name in self.model_cls.obsolete_fields():
                continue
            if is_optional(field_type):
                field_type = optional_type(field_type)
            field_config = fields_setting.get(field_name, {})
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                widget = self.get_widget(row_idx, column_idx)
                ImportFieldMappingUtils.update_widget_with_config(
                    widget, key_name, field_type, field_config
                )
            row_idx += 1

    def update_layers(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
        for combobox in self.source_attribute_widgets:
            combobox.clear()
            combobox.addItems(layer_field_names)
            combobox.setCurrentText(combobox.data_model_field_name)
        for expression_widget in self.expression_widgets:
            expression_widget.setLayer(layer)
