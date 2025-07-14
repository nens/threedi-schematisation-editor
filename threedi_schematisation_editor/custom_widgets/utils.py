import inspect
import warnings
from enum import IntEnum

from qgis.core import NULL, Qgis, QgsMessageLog, QgsSettings
from qgis.PyQt.QtWidgets import QComboBox

from threedi_schematisation_editor import warnings as threedi_warnings
from threedi_schematisation_editor.custom_tools.utils import ColumnImportMethod
from threedi_schematisation_editor.custom_widgets.dialogs.attribute_value_map import AttributeValueMapDialog
from threedi_schematisation_editor.utils import REQUIRED_VALUE_STYLESHEET, NULL_STR, enum_entry_name_format


class CatchThreediWarnings:
    """
    A context manager that catches warnings from threedi_schematisation_editor.warnings,
    compiles them into a warnings_msg, and logs them to QGIS log system.
    """

    def __init__(self, log_category="Warnings"):
        self.caught_warnings = []
        self.warnings_msg = ""
        self.log_category = log_category

    def __enter__(self):
        # Create a warnings list to store caught warnings
        self._warnings_list = []

        # Save the old showwarning function to restore it later
        self._old_showwarning = warnings.showwarning

        # Define a custom function to intercept warnings
        def _showwarning(message, category, filename, lineno, file=None, line=None):
            self._warnings_list.append((message, category, filename, lineno))

        # Replace the default showwarning with our custom one
        warnings.showwarning = _showwarning

        # Set up the warnings filter
        warnings.simplefilter("ignore")  # Ignore all warnings by default

        # Enable warnings for all warning classes in the threedi module
        for name, obj in inspect.getmembers(threedi_warnings):
            if inspect.isclass(obj) and issubclass(obj, Warning):
                warnings.simplefilter("always", obj)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original showwarning function
        warnings.showwarning = self._old_showwarning

        # Process the warnings
        self.caught_warnings = self._warnings_list

        # Generate the warning message if any warnings were caught
        if self.caught_warnings:
            self.warnings_msg = (
                "\n\nNote: Some warnings were raised during the process. "
                "Check the 'Warnings' log for more details."
            )

            # Log each warning to QGIS
            for warning_info in self.caught_warnings:
                message, category, filename, lineno = warning_info
                warning_text = f"{category.__name__}: {message}"
                QgsMessageLog.logMessage(warning_text, self.log_category, level=Qgis.Warning)

        # Reset the warnings filter
        warnings.resetwarnings()

        # Don't suppress any exceptions
        return False


class ImportFieldMappingUtils:
    """Utilities for importing field mappings."""

    LAST_CONFIG_DIR_ENTRY = "threedi/last_import_config_dir"

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

    @staticmethod
    def on_value_map_clicked(
        source_layer_cbo, source_attribute_combobox, pressed_button, user_communication, parent=None
    ):
        source_layer = source_layer_cbo.currentLayer()
        value_map_dlg = AttributeValueMapDialog(pressed_button, source_attribute_combobox, source_layer, parent)
        accepted = value_map_dlg.exec_()
        if accepted:
            try:
                value_map_dlg.update_value_map()
            except (SyntaxError, ValueError):
                user_communication.show_error(f"Invalid value map. Action aborted.", parent)

    @staticmethod
    def update_widget_with_config(widget, key_name, field_type, field_config):
        try:
            key_value = field_config[key_name]
        except KeyError:
            return
        if isinstance(widget, QComboBox):
            if key_value == NULL_STR:
                widget.setCurrentText(key_value)
            else:
                if key_name == "method":
                    widget.setCurrentText(enum_entry_name_format(ColumnImportMethod(key_value)))
                elif key_name == "default_value" and field_type != bool:
                    widget.setCurrentText(enum_entry_name_format(field_type(key_value)))
                else:
                    widget.setCurrentText(str(key_value))
        elif key_name == "value_map":
            AttributeValueMapDialog.update_value_map_button(widget, key_value)
        elif key_name == "expression":
            widget.setExpression(key_value)
        else:
            widget.setText(str(key_value))
            widget.setCursorPosition(0)

    @staticmethod
    def collect_config_from_widget(widget, key_name, field_type, column_idx):
        if isinstance(widget, QComboBox):
            key_value = (
                widget.currentText()
                if column_idx == ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX
                else widget.currentData()
            )
        elif column_idx == ColumnImportIndex.VALUE_MAP_COLUMN_IDX:
            key_value = {str(key) : value for key, value in widget.value_map.items()}
            if not key_value:
                return None
        elif column_idx == ColumnImportIndex.EXPRESSION_COLUMN_IDX:
            if not widget.isValidExpression():
                return None
            key_value = widget.expression()
        else:
            key_value = widget.text()
            if not key_value:
                return None
            if column_idx == ColumnImportIndex.DEFAULT_VALUE_COLUMN_IDX and key_name != NULL_STR:
                key_value = field_type(key_value)
        return key_value


class ColumnImportIndex(IntEnum):
    """Base class for import tool configuration."""

    FIELD_NAME_COLUMN_IDX = 0
    METHOD_COLUMN_IDX = 1
    SOURCE_ATTRIBUTE_COLUMN_IDX = 2
    VALUE_MAP_COLUMN_IDX = 3
    DEFAULT_VALUE_COLUMN_IDX = 4
    EXPRESSION_COLUMN_IDX = 5
