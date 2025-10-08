from dataclasses import dataclass, fields
from functools import cached_property
from typing import Optional

from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QVBoxLayout,
)

from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod

BACKGROUND_COLOR = "#ff8888"


@dataclass
class Row:
    label: str
    method: Optional[str] = None
    source_attribute: str = ""
    value_map: str = ""
    expression: str = ""
    default_value: str = ""

    @staticmethod
    def header():
        return [
            "Field name",
            "Method",
            "Source attribute",
            "Value map",
            "Expression",
            "Default value",
        ]

    @cached_property
    def field_names(self):
        return [field.name for field in fields(self)]

    @cached_property
    def field_col_idx_map(self):
        return {i: field_name for i, field_name in enumerate(self.field_names)}

    @cached_property
    def field_name_map(self):
        return {field_name: i for i, field_name in enumerate(self.field_names)}

    def _get_required_column(self):
        method_map = {
            ColumnImportMethod.ATTRIBUTE.value: self.field_name_map["source_attribute"],
            ColumnImportMethod.EXPRESSION.value: self.field_name_map["expression"],
            ColumnImportMethod.DEFAULT.value: self.field_name_map["default_value"],
        }
        return method_map.get(self.method)

    def is_editable(self, index):
        # label is never selectable or editable
        if self.field_col_idx_map[index] == "label":
            return False
        # method is always selectable and editable
        if self.field_col_idx_map[index] == "method":
            return True
        # in any other case the method determines what is editable
        else:
            return index == self._get_required_column()

    def set_value(self, value, index):
        field_name = self.field_col_idx_map.get(index)
        if field_name:
            setattr(self, field_name, value)

    def get_value(self, index):
        field_name = self.field_col_idx_map.get(index)
        if field_name:
            return getattr(self, field_name)


class ValueMapDialog(QDialog):
    def __init__(self, current_value="", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Set Value Map")
        self.setModal(True)

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setText(current_value)

        # Dialog buttons (OK and Cancel)
        self.dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        # Layout for dialog
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Value Map:"))
        layout.addWidget(self.input_field)
        layout.addWidget(self.dialog_buttons)

        self.setLayout(layout)

    def get_value_map(self):
        """
        Return the value entered in the QLineEdit.
        """
        return self.input_field.text()


class FieldMapModel(QAbstractTableModel):
    def __init__(self, row_dict, parent=None):
        super().__init__(parent)
        self.rows = list(row_dict.values())
        self.row_names = list(row_dict.keys())
        self.current_layer_attributes = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows) if self.rows else 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.rows[0].field_names) if self.rows else 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return Row.header()[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def get_placeholder(self, column, row, value):
        if value is not None and value != "":
            return None
        if column == 1 and not row.method:
            return "required"
        if column > 1 and row.method:
            if row.is_editable(column):
                return "required"
            else:
                return "disabled"
        return None

    def data(self, index, role=Qt.DisplayRole):
        row = self.rows[index.row()]
        value = row.get_value(index.column())
        if role == Qt.EditRole or role == Qt.DisplayRole:
            return value
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            row = self.rows[index.row()]
            row.set_value(value, index.column())
            leftIndex = self.index(index.row(), 0)
            rightIndex = self.index(index.row(), self.columnCount() - 1)
            self.dataChanged.emit(leftIndex, rightIndex)
            return True
        return False

    def flags(self, index):
        row = self.rows[index.row()]
        if row.is_editable(index.column()):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def set_current_layer(self, layer):
        if layer:
            self.current_layer_attributes = layer.attributes
        else:
            self.current_layer_attributes = []
        self.layoutChanged.emit()


class QsgExpressionWidgetForTableView(QgsFieldExpressionWidget):
    def __init__(self, parent=None, expression=None):
        super().__init__(parent)
        self._expression = expression

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "_expression") and self._expression is not None:
            self.setExpression(self._expression)
            # Clear it so we don't keep setting it on every show
            self._expression = None


class FieldMapDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._editors = {}  # Track editors to prevent recreation

    def createEditor(self, parent, option, index):
        # Check if we already have an editor for this index
        key = (index.row(), index.column())
        if key in self._editors:
            return self._editors[key]

        if index.column() == 1:  # Method column
            combo = CustomComboBox(parent)
            combo.addItems([""] + [m.value for m in ColumnImportMethod])
            # Store the editor
            self._editors[(index.row(), index.column())] = combo
            # Connect signal for immediate updates
            combo.currentIndexChanged.connect(
                lambda idx, editor=combo: self.commitData.emit(editor)
            )

            # Style the dropdown list items too (different from the main box)
            combo.setItemData(
                0, QColor(255, 0, 0), Qt.ForegroundRole
            )  # Red text for dropdown item

            return combo
        elif index.column() == 2:  # Source attribute column
            combo = CustomComboBox(parent)
            combo.addItems([""] + index.model().current_layer_attributes)
            # Connect to handle changes immediately
            combo.currentTextChanged.connect(
                lambda text, idx=index: self.commitAndCloseEditor(text, idx)
            )
            self._editors[key] = combo
            return combo
        elif index.column() == 3:  # Value map column
            button = QPushButton(parent)
            current_value_map = (
                index.data(Qt.EditRole) if index.data(Qt.EditRole) else ""
            )
            button.setText(
                current_value_map if current_value_map else "Set Value Map..."
            )
            # Connect button click to open dialog
            button.clicked.connect(
                lambda checked, idx=index, btn=button: self.openValueMapDialog(idx, btn)
            )
            self._editors[key] = button
            return button
        elif index.column() == 4:  # Expression column
            current_expression = index.model().rows[index.row()].expression
            widget = QsgExpressionWidgetForTableView(
                parent, expression=current_expression
            )
            # Connect expression changes to commit data
            widget.fieldChanged.connect(
                lambda field, idx=index: self.commitExpressionData(idx, widget)
            )
            self._editors[key] = widget
            return widget
        elif index.column() == 5:  # Default value column
            return QLineEdit(parent)
        return super().createEditor(parent, option, index)

    def openValueMapDialog(self, index, button):
        """Open the value map dialog and update the model"""
        current_value_map = index.data(Qt.EditRole) if index.data(Qt.EditRole) else ""
        dialog = ValueMapDialog(current_value=current_value_map, parent=button)
        if dialog.exec_() == QDialog.Accepted:
            new_value_map = dialog.get_value_map()
            button.setText(new_value_map if new_value_map else "Set Value Map...")
            index.model().setData(index, new_value_map, Qt.EditRole)

    def commitExpressionData(self, index, widget):
        """Commit expression widget data"""
        self.commitData.emit(widget)

    def commitAndCloseEditor(self, text, index):
        """Handle combobox selection changes"""
        # TODO: don't know how this works
        editor = self.sender()
        if editor:
            self.commitData.emit(editor)
            # After method changes, we need to update widget states
            # Get the main  window and trigger widget state update
            view = editor.parent()
            view.update_widget_states()

    def setEditorData(self, editor, index):
        row = index.model().rows[index.row()]
        has_layer = len(index.model().current_layer_attributes) > 0
        if index.column() == 1:
            is_enabled = has_layer
        else:
            is_enabled = has_layer and row.is_editable(index.column())
        # this setEnabled wins!
        editor.setEnabled(is_enabled)
        if isinstance(editor, QComboBox):
            value = index.data(Qt.EditRole)
            if value:
                editor.setCurrentText(value)
        elif isinstance(editor, QPushButton):
            value = index.data(Qt.EditRole)
            if value or not is_enabled:
                editor.setText(value)
                editor.setStyleSheet("")
            else:
                editor.setText("Set Value Map...")
                editor.setStyleSheet(
                    f"QPushButton {{ background-color: {BACKGROUND_COLOR};}}"
                )
        elif isinstance(editor, QgsFieldExpressionWidget):
            value = index.data(Qt.EditRole)
            editor.setExpression(value)
            if value or not is_enabled:
                editor.setStyleSheet("")
            else:
                editor.setStyleSheet(
                    f"QLineEdit {{ background-color: {BACKGROUND_COLOR};}}"
                )
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            model.setData(index, value, Qt.EditRole)
        elif isinstance(editor, QPushButton):
            # Button doesn't directly set data - it's handled by the dialog
            pass
        elif isinstance(editor, QgsFieldExpressionWidget):
            model.setData(index, editor.expression(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    def destroyEditor(self, editor, index):
        """Clean up when editor is destroyed"""
        key = (index.row(), index.column())
        if key in self._editors:
            del self._editors[key]
        super().destroyEditor(editor, index)

    def clear_editors(self):
        """Clear all tracked editors"""
        self._editors.clear()


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentIndexChanged.connect(self.updateStyle)

    def setEnabled(self, enabled):
        """Override setEnabled to update the style when enabled state changes"""
        super().setEnabled(enabled)
        # Call updateStyle to update appearance based on the new enabled state
        self.updateStyle(self.currentIndex())

    def updateStyle(self, index):
        if index == 0 and self.isEnabled():
            self.setStyleSheet(f"QComboBox {{ background-color: {BACKGROUND_COLOR};}}")
        else:
            self.setStyleSheet("")  # Clear stylesheet


class DefaultValueDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # Copy the style option to modify it
        opt = QStyleOptionViewItem(option)
        # Get data from the model
        row = index.model().rows[index.row()]
        is_required = row.is_editable(index.column())
        has_value = bool(
            index.model().data(index, Qt.DisplayRole)
        )  # Check if display value is non-empty
        # Modify background for required fields with no value
        if is_required and not has_value:
            painter.save()
            painter.fillRect(option.rect, QColor(BACKGROUND_COLOR))
            painter.restore()

        # Call parent class to paint the cell content
        super().paint(painter, opt, index)
