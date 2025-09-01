import inspect
import warnings
from enum import IntEnum

from qgis.core import NULL, Qgis, QgsMessageLog, QgsSettings
from qgis.gui import QgsFieldComboBox, QgsFieldExpressionWidget
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QStackedWidget,
    QWidget,
)

from threedi_schematisation_editor import warnings as threedi_warnings
from threedi_schematisation_editor.utils import (
    NULL_STR,
    REQUIRED_VALUE_STYLESHEET,
    enum_entry_name_format,
    get_type_for_casting,
)
from threedi_schematisation_editor.vector_data_importer.dialogs.attribute_value_map import (
    AttributeValueMapDialog,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


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
                QgsMessageLog.logMessage(
                    warning_text, self.log_category, level=Qgis.Warning
                )

        # Reset the warnings filter
        warnings.resetwarnings()

        # Don't suppress any exceptions
        return False


class ImportFieldMappingUtils:
    """Utilities for importing field mappings."""

    LAST_CONFIG_DIR_ENTRY = "threedi/last_import_config_dir"

    @staticmethod
    def on_method_changed(
        source_attribute_combobox, value_map_widget, expression_widget, current_text
    ):
        if current_text != str(ColumnImportMethod.ATTRIBUTE):
            source_attribute_combobox.setDisabled(True)
            value_map_widget.setDisabled(True)
            source_attribute_combobox.setStyleSheet("")
            expression_widget.setEnabled(
                current_text == str(ColumnImportMethod.EXPRESSION)
            )
        else:
            source_attribute_combobox.setEnabled(True)
            value_map_widget.setEnabled(True)
            expression_widget.setDisabled(True)
            if source_attribute_combobox.currentText():
                source_attribute_combobox.setStyleSheet("")
            else:
                source_attribute_combobox.setStyleSheet(REQUIRED_VALUE_STYLESHEET)

    @staticmethod
    def on_source_attribute_value_changed(
        method_combobox, source_attribute_combobox, current_text
    ):
        if (
            method_combobox.currentText() == str(ColumnImportMethod.ATTRIBUTE)
            and not current_text
        ):
            source_attribute_combobox.setStyleSheet(REQUIRED_VALUE_STYLESHEET)
        else:
            source_attribute_combobox.setStyleSheet("")

    @staticmethod
    def on_value_map_clicked(
        source_layer_cbo,
        source_attribute_combobox,
        pressed_button,
        user_communication,
        parent=None,
    ):
        source_layer = source_layer_cbo.currentLayer()
        value_map_dlg = AttributeValueMapDialog(
            pressed_button, source_attribute_combobox, source_layer, parent
        )
        accepted = value_map_dlg.exec_()
        if accepted:
            try:
                value_map_dlg.update_value_map()
            except (SyntaxError, ValueError):
                user_communication.show_error(
                    f"Invalid value map. Action aborted.", parent
                )

    @staticmethod
    def update_widget_with_config(widget, key_name, field_type, field_config):
        field_type = get_type_for_casting(field_type)
        try:
            key_value = field_config[key_name]
        except KeyError:
            return
        if isinstance(widget, QComboBox):
            if key_value == NULL_STR:
                widget.setCurrentText(key_value)
            else:
                if key_name == "method":
                    widget.setCurrentText(
                        enum_entry_name_format(ColumnImportMethod(key_value))
                    )
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
        field_type = get_type_for_casting(field_type)
        if isinstance(widget, QComboBox):
            key_value = (
                widget.currentText()
                if column_idx == ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX
                else widget.currentData()
            )
        elif column_idx == ColumnImportIndex.VALUE_MAP_COLUMN_IDX:
            key_value = {str(key): value for key, value in widget.value_map.items()}
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
            if (
                column_idx == ColumnImportIndex.DEFAULT_VALUE_COLUMN_IDX
                and key_name != NULL_STR
            ):
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


def create_font(dialog, point_size: int, bold: bool = False):
    font = dialog.font()
    font.setPointSize(point_size)
    if bold:
        font.setBold(True)
        font.setWeight(75)
    return font


class JoinFieldsRow(QDialog):
    def __init__(self, label, layer_src=False, parent=None, layout=None, row=0):
        super().__init__(parent)
        self.layout = layout if isinstance(layout, QGridLayout) else QGridLayout()
        self.row_idx = row
        self.setup_ui(label, layer_src)

    def setup_ui(self, label, layer_src):
        # Create labels
        lbl = QLabel(label)
        font = create_font(lbl, 10)
        lbl.setFont(font)
        lbl.setLayoutDirection(Qt.LeftToRight)
        # Create input fields
        if layer_src:
            self.input_cbo = QgsFieldComboBox()
            self.input_cbo.setAllowEmptyFieldName(True)
        else:
            self.input_cbo = QComboBox()
            self.input_cbo.setFont(font)
            self.input_cbo.insertItems(0, ["", "id", "code"])
        self.input_cbo.setFont(font)
        self.input_cbo.setMinimumWidth(200)
        self.input_expr = QgsFieldExpressionWidget()
        self.input_expr.setFont(font)
        # Create toggle
        self.attr_radio = QRadioButton("Attribute")
        self.attr_radio.setFont(font)
        self.expr_radio = QRadioButton("Expression")
        self.expr_radio.setFont(font)
        self.attr_radio.setChecked(True)
        button_group = QButtonGroup(self)
        button_group.addButton(self.attr_radio)
        button_group.addButton(self.expr_radio)
        toggle_widget = QWidget()
        toggle_layout = QHBoxLayout(toggle_widget)
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.addWidget(self.attr_radio)
        toggle_layout.addWidget(self.expr_radio)
        self.stack = QStackedWidget()
        self.stack.addWidget(self.input_cbo)
        self.stack.addWidget(self.input_expr)
        self.attr_radio.toggled.connect(self.toggle_input)
        self.layout.addWidget(lbl, self.row_idx, 0)
        self.layout.addWidget(toggle_widget, self.row_idx, 1)
        self.layout.addWidget(self.stack, self.row_idx, 2)

    @property
    def layer_dependent_widgets(self):
        return [self.attr_radio, self.expr_radio, self.input_cbo, self.input_expr]

    def toggle_input(self):
        if self.attr_radio.isChecked():
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(1)

    @property
    def value(self):
        if self.input_cbo.currentText() == "" and self.input_expr.isValidExpression():
            return {
                "method": ColumnImportMethod.EXPRESSION.value,
                ColumnImportMethod.EXPRESSION.value: self.input_expr.expression(),
            }
        else:
            return {
                "method": ColumnImportMethod.ATTRIBUTE.value,
                ColumnImportMethod.ATTRIBUTE.value: self.input_cbo.currentText(),
            }

    @value.setter
    def value(self, value):
        if value.get("method") == ColumnImportMethod.EXPRESSION.value:
            self.expr_radio.setChecked(True)
            self.input_expr.setExpression(
                value.get(ColumnImportMethod.EXPRESSION.value)
            )
        elif value.get("method") == ColumnImportMethod.ATTRIBUTE.value:
            self.attr_radio.setChecked(True)
            self.input_cbo.setCurrentText(value.get(ColumnImportMethod.ATTRIBUTE.value))

    @property
    def is_set(self):
        if self.input_cbo.currentText() == "" and self.input_expr.isValidExpression():
            return self.input_expr.expression() != ""
        else:
            return self.input_cbo.currentText() != ""
