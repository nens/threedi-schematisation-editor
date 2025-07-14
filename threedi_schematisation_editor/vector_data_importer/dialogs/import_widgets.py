from collections import defaultdict
from enum import Enum
from itertools import chain

from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton

from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import ColumnImportIndex
from threedi_schematisation_editor.utils import is_optional, optional_type, enum_entry_name_format


def get_field_methods_mapping(fields_iterator):
    """Return a mapping of fields to import methods."""
    methods_mapping = defaultdict(dict)
    auto_fields = {"id"}
    auto_attribute_fields = {"connection_node_id", "connection_node_id_start", "connection_node_id_end"}

    for field_name, model_cls in fields_iterator:
        if field_name in auto_fields:
            methods_mapping[model_cls][field_name] = [ColumnImportMethod.AUTO]
        elif field_name in auto_attribute_fields:
            methods_mapping[model_cls][field_name] = [
                ColumnImportMethod.AUTO,
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.EXPRESSION,
            ]
        else:
            methods_mapping[model_cls][field_name] = [
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.DEFAULT,
                ColumnImportMethod.EXPRESSION,
                ColumnImportMethod.IGNORE,
            ]
    return methods_mapping


def create_widgets(import_model_cls, nodes_model_cls=None):
    """Create widgets for the data model fields."""
    import_fields = ((k, import_model_cls) for k in import_model_cls.__annotations__.keys())
    if nodes_model_cls is not None:
        node_fields = ((k, nodes_model_cls) for k in nodes_model_cls.__annotations__.keys())
    else:
        node_fields = ()
    fields_iterator = chain(import_fields, node_fields)
    field_methods_mapping = get_field_methods_mapping(fields_iterator)
    widgets_to_add = defaultdict(dict)
    for model_cls, fields_mapping in field_methods_mapping.items():
        model_obsolete_fields = model_cls.obsolete_fields()
        model_fields_display_names = model_cls.fields_display_names()
        row_idx = 0

        for field_name, field_methods in fields_mapping.items():
            if field_name in model_obsolete_fields:
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
                elif column_idx == ColumnImportIndex.VALUE_MAP_COLUMN_IDX:
                    widget = create_set_value_map_widget()
                elif column_idx == ColumnImportIndex.EXPRESSION_COLUMN_IDX:
                    widget = create_expression_widget()
                elif column_idx == ColumnImportIndex.DEFAULT_VALUE_COLUMN_IDX:
                    widget = create_default_value_widget(field_type)

                widgets_to_add[model_cls][row_idx, column_idx] = widget

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
            items = [["NULL", "NULL"]] + [[enum_entry_name_format(e), e.value] for e in field_type]
        return create_combobox_widget(items)
    else:
        return QLineEdit()


CONFIG_HEADER = ["Field name", "Method", "Source attribute", "Value map", "Default value", "Expression"]
CONFIG_KEYS = ["method", "source_attribute", "value_map", "default_value", "expression"]
