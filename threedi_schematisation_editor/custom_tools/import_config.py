from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum, IntEnum
from itertools import chain

from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import is_optional, optional_type, enum_entry_name_format

CONFIG_HEADER = ["Field name", "Method", "Source attribute", "Value map", "Default value", "Expression"]
CONFIG_KEYS = ["method", "source_attribute", "value_map", "default_value", "expression"]

class ColumnImportMethod(Enum):
    AUTO = "auto"
    ATTRIBUTE = "source_attribute"
    DEFAULT = "default"
    EXPRESSION = "expression"
    IGNORE = "ignore"

    def __str__(self):
        return self.name.capitalize()


class ColumnImportIndex(IntEnum):
    """Base class for import tool configuration."""

    FIELD_NAME_COLUMN_IDX = 0
    METHOD_COLUMN_IDX = 1
    SOURCE_ATTRIBUTE_COLUMN_IDX = 2
    VALUE_MAP_COLUMN_IDX = 3
    DEFAULT_VALUE_COLUMN_IDX = 4
    EXPRESSION_COLUMN_IDX = 5


class BaseImportConfig(ABC):
    """Base class for import tool configuration."""

    def __init__(self, import_model_cls, nodes_model_cls=None):
        self.import_model_cls = import_model_cls
        self.nodes_model_cls = nodes_model_cls
        self.field_methods_provider = FieldMethodsProvider(self)
        self.widget_factory = ImportWidgetFactory(self)

    @property
    def models_fields_iterator(self):
        structure_fields = ((k, self.import_model_cls) for k in self.import_model_cls.__annotations__.keys())
        if self.nodes_model_cls is not None:
            node_fields = ((k, self.nodes_model_cls) for k in self.nodes_model_cls.__annotations__.keys())
        else:
            node_fields = ()
        fields_iterator = chain(structure_fields, node_fields)
        return fields_iterator

    @property
    def field_methods_mapping(self):
        """Return a mapping of fields to import methods."""
        return self.field_methods_provider.get_field_methods_mapping()

    def data_model_widgets(self):
        """Create widgets for the data model fields."""
        return self.widget_factory.create_widgets()


class FieldMethodsProvider:
    """Class that handles mapping of fields to import methods."""

    def __init__(self, config):
        self.config = config

    def get_field_methods_mapping(self):
        """Return a mapping of fields to import methods."""
        methods_mapping = defaultdict(dict)
        auto_fields = {"id"}
        auto_attribute_fields = {"connection_node_id", "connection_node_id_start", "connection_node_id_end"}
        for field_name, model_cls in self.config.models_fields_iterator:
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


class ImportWidgetFactory:
    """Class that creates UI widgets for import configuration."""

    def __init__(self, config):
        self.config = config

    def create_widgets(self):
        """Create widgets for the data model fields."""
        widgets_to_add = defaultdict(dict)

        for model_cls, field_methods_mapping in self.config.field_methods_mapping.items():
            model_obsolete_fields = model_cls.obsolete_fields()
            model_fields_display_names = model_cls.fields_display_names()
            row_idx = 0

            for field_name, field_methods in field_methods_mapping.items():
                if field_name in model_obsolete_fields:
                    continue

                field_type = model_cls.__annotations__[field_name]
                if is_optional(field_type):
                    field_type = optional_type(field_type)

                for column_idx, column_name in enumerate(CONFIG_HEADER):
                    if column_idx == ColumnImportIndex.FIELD_NAME_COLUMN_IDX:
                        widget = self._create_label_widget(model_fields_display_names[field_name])
                    elif column_idx == ColumnImportIndex.METHOD_COLUMN_IDX:
                        widget = self._create_method_widget(field_methods)
                    elif column_idx == ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX:
                        widget = self._create_combobox_widget()
                    elif column_idx == ColumnImportIndex.VALUE_MAP_COLUMN_IDX:
                        widget = self._create_set_value_map_widget()
                    elif column_idx == ColumnImportIndex.EXPRESSION_COLUMN_IDX:
                        widget = self._create_expression_widget()
                    elif column_idx == ColumnImportIndex.DEFAULT_VALUE_COLUMN_IDX:
                        widget = self._create_default_value_widget(field_type)

                    widgets_to_add[model_cls][row_idx, column_idx] = widget

                row_idx += 1

        return widgets_to_add

    def _create_label_widget(self, field_display_name):
        return QLabel(f"{field_display_name}\t")

    def _create_method_widget(self, field_methods):
        items = [[method.name.capitalize(), method.value] for method in field_methods]
        return self._create_combobox_widget(items)

    def _create_combobox_widget(self, items=None):
        widget = QComboBox()
        if items:
            for item in items:
                widget.addItem(*item)
        return widget

    def _create_set_value_map_widget(self):
        widget = QPushButton("Set...")
        widget.value_map = {}
        return widget

    def _create_expression_widget(self):
        return QgsFieldExpressionWidget()

    def _create_default_value_widget(self, field_type):
        if issubclass(field_type, Enum) or field_type == bool:
            if field_type == bool:
                items = [["False", False], ["True", True]]
            else:
                items = [["NULL", "NULL"]] + [[enum_entry_name_format(e), e.value] for e in field_type]
            return self._create_combobox_widget(items)
        else:
            return QLineEdit()


class FeaturesImportConfig(BaseImportConfig):
    """Features import tool configuration class."""


class StructuresImportConfig(BaseImportConfig):
    """Structures import tool configuration class."""

    def __init__(self, import_model_cls):
        super().__init__(import_model_cls, dm.ConnectionNode)
