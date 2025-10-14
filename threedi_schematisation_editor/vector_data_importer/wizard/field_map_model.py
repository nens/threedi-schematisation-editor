from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Any, Optional

from qgis.core import QgsVectorLayer
from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, Qt
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from threedi_schematisation_editor.vector_data_importer.settings_models import (
    FieldMapConfig,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod

BACKGROUND_COLOR = "#ff8888"


class FieldMapColumn(Enum):
    LABEL = "Field name"
    METHOD = "Method"
    SOURCE_ATTRIBUTE = "Source attribute"
    VALUE_MAP = "Value map"
    EXPRESSION = "Expression"
    DEFAULT_VALUE = "Default value"

    @staticmethod
    def from_index(index: int) -> "FieldMapColumn":
        members = tuple(FieldMapColumn)
        if 0 <= index < len(members):
            return members[index]

    @staticmethod
    def to_index(column: "FieldMapColumn") -> int:
        return tuple(FieldMapColumn).index(column)


@dataclass
class FieldMapRow:
    label: str
    config: FieldMapConfig = FieldMapConfig()

    @staticmethod
    def header() -> list[str]:
        return [member.value for member in FieldMapColumn]

    @cached_property
    def field_names(self) -> list[str]:
        return list(type(self.config).model_fields.keys())

    @cached_property
    def field_col_idx_map(self) -> dict[int, str]:
        return {i: field_name for i, field_name in enumerate(self.field_names, 1)}

    @cached_property
    def field_name_map(self) -> dict[str, int]:
        return {field_name: i for i, field_name in enumerate(self.field_names, 1)}

    def is_editable(self, index: int) -> bool:
        """Determine if the column is editable base on column index."""
        # label is never selectable or editable
        if FieldMapColumn.from_index(index) == FieldMapColumn.LABEL:
            return False
        # method is always selectable and editable
        if FieldMapColumn.from_index(index) == FieldMapColumn.METHOD:
            return True
        # in any other case the method determines what is editable
        else:
            # identify required attribute, if any
            required_attribute = self.config.required_field_map.get(self.config.method)
            # find column where this attribute is expected
            required_column_idx = self.field_name_map.get(required_attribute, -1)
            return index == required_column_idx

    def set_value(self, value: Any, index: int):
        """Set value in the data model based on the column index."""
        # Do not allow setting of the label
        if FieldMapColumn.from_index(index) == FieldMapColumn.LABEL:
            return
        # Retrieve data from config
        field_name = self.field_col_idx_map.get(index)
        if field_name:
            setattr(self.config, field_name, value)

    def get_value(self, index: int) -> Any | None:
        """Retrieve value for a column index."""
        if FieldMapColumn.from_index(index) == FieldMapColumn.LABEL:
            return self.label
        # Retrieve data from config
        field_name = self.field_col_idx_map.get(index)
        if field_name:
            return getattr(self.config, field_name)

    def serialize(self) -> dict[str, Any]:
        return self.config.model_dump()

    def deserialize(self, data: dict[str, Any]) -> None:
        self.config = FieldMapConfig(**data)


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
        self.row_dict = row_dict
        self.rows = list(row_dict.values())
        self.attr_to_label_map = {
            attr_name: row.label for attr_name, row in row_dict.items()
        }
        self.current_layer_attributes = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.rows) if self.rows else 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.rows[0].field_names) + 1 if self.rows else 0

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return FieldMapRow.header()[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
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

    def set_current_layer(self, layer: QgsVectorLayer):
        """Update list of available attributes based on the current layer."""
        if layer:
            self.current_layer_attributes = [field.name() for field in layer.fields()]
        else:
            self.current_layer_attributes = []
        self.layoutChanged.emit()

    def serialize(self) -> dict[str, dict[str, Any]]:
        return {attr_name: row.serialize() for attr_name, row in self.row_dict.items()}

    def deserialize(self, data: dict[str, dict[str, Any]]):
        for key, row_data in data.items():
            label = self.attr_to_label_map.get(key)
            if label:
                self.row_dict[label].deserialize(row_data)


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
        key = (index.row(), index.column())
        if key in self._editors:
            return self._editors[key]
        if FieldMapColumn.from_index(index.column()) == FieldMapColumn.METHOD:
            combo = CustomComboBox(parent)
            combo.addItem("", None)
            for m in ColumnImportMethod:
                combo.addItem(str(m), m)
            self._editors[(index.row(), index.column())] = combo
            combo.currentIndexChanged.connect(
                lambda idx, editor=combo: self.commitData.emit(editor)
            )
            return combo
        elif (
            FieldMapColumn.from_index(index.column()) == FieldMapColumn.SOURCE_ATTRIBUTE
        ):
            combo = CustomComboBox(parent)
            combo.addItems([""] + index.model().current_layer_attributes)
            combo.currentTextChanged.connect(
                lambda text, idx=index: self.commitAndCloseEditor(text, idx)
            )
            self._editors[key] = combo
            return combo
        elif FieldMapColumn.from_index(index.column()) == FieldMapColumn.VALUE_MAP:
            # TODO: use real value map
            button = QPushButton(parent)
            current_value_map = (
                index.data(Qt.EditRole) if index.data(Qt.EditRole) else ""
            )
            button.setText(
                current_value_map if current_value_map else "Set Value Map..."
            )
            button.clicked.connect(
                lambda checked, idx=index, btn=button: self.openValueMapDialog(idx, btn)
            )
            self._editors[key] = button
            return button
        elif FieldMapColumn.from_index(index.column()) == FieldMapColumn.EXPRESSION:
            current_expression = index.model().rows[index.row()].config.expression
            widget = QsgExpressionWidgetForTableView(
                parent, expression=current_expression
            )
            widget.fieldChanged.connect(
                lambda field, idx=index: self.commitExpressionData(idx, widget)
            )
            self._editors[key] = widget
            return widget
        elif FieldMapColumn.from_index(index.column()) == FieldMapColumn.DEFAULT_VALUE:
            current_value = index.model().rows[index.row()].config.default_value
            widget = QLineEdit(parent)
            widget.setText(current_value if current_value else "")
            widget.editingFinished.connect(
                lambda field, idx=index: self.commitDefaultValueData(idx, widget)
            )
            self._editors[key] = widget
            return widget
        return super().createEditor(parent, option, index)

    def openValueMapDialog(self, index, button):
        """Open the value map dialog and update the model"""
        current_value_map = index.data(Qt.EditRole) if index.data(Qt.EditRole) else ""
        dialog = ValueMapDialog(current_value=current_value_map, parent=button)
        if dialog.exec_() == QDialog.Accepted:
            new_value_map = dialog.get_value_map()
            button.setText(new_value_map if new_value_map else "Set Value Map...")
            index.model().setData(index, new_value_map, Qt.EditRole)

    def commitDefaultValueData(self, index, widget):
        """Commit default value widget data"""
        self.commitData.emit(widget)

    def commitExpressionData(self, index, widget):
        """Commit expression widget data"""
        self.commitData.emit(widget)

    def setEditorData(self, editor, index):
        row = index.model().rows[index.row()]
        has_layer = len(index.model().current_layer_attributes) > 0
        if index.column() == 1:
            is_enabled = has_layer
        else:
            is_enabled = has_layer and row.is_editable(index.column())
        editor.setEnabled(is_enabled)
        if isinstance(editor, QComboBox):
            value = index.data(Qt.EditRole)
            if value:
                editor.setCurrentText(str(value))
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
        elif isinstance(editor, QLineEdit):
            value = index.data(Qt.EditRole)
            editor.setText(value if value else "")
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
            value = editor.currentData()
            model.setData(index, value, Qt.EditRole)
        elif isinstance(editor, QPushButton):
            pass
        elif isinstance(editor, QgsFieldExpressionWidget):
            model.setData(index, editor.expression(), Qt.EditRole)
        elif isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    def destroyEditor(self, editor, index):
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


class FieldMapWidget(QWidget):
    def __init__(self, row_dict):
        super().__init__()
        self.row_dict = row_dict
        self.table_model = FieldMapModel(self.row_dict)
        self.rows = self.table_model.rows
        self.setup_ui()

    def setup_ui(self):
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)

        # Delegate for handling custom widget editing
        self.table_delegate = FieldMapDelegate()
        self.table_view.setItemDelegate(self.table_delegate)
        self.table_view.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Calculate the total height needed
        header_height = self.table_view.horizontalHeader().height()
        row_height = self.table_view.verticalHeader().defaultSectionSize()
        content_height = (row_height * self.table_model.rowCount()) + header_height

        # Set fixed height and vertical size policy
        self.table_view.setMinimumHeight(content_height)
        self.table_view.setMaximumHeight(content_height)
        self.table_view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def update_layer(self, layer):
        """Update the layer and update the table view"""
        self.close_persistent_editors()
        self.table_model.set_current_layer(layer)
        for row in self.table_model.rows:
            current_source_attr = row.config.source_attribute
            if (
                not layer
                or current_source_attr not in self.table_model.current_layer_attributes
            ):
                row.config.source_attribute = ""
        # Notify the model of the changes so the view is updated
        self.table_model.layoutChanged.emit()

        # Clear delegate's editor cache
        self.table_delegate.clear_editors()

        # Open persistent editors for columns with always-visible widgets
        self.open_persistent_editors()

        # Todo updata data
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)

    def open_persistent_editors(self):
        """Open persistent editors for columns with always-visible widgets"""
        for row in range(self.table_model.rowCount()):
            for col, field_map_column in enumerate(FieldMapColumn):
                if field_map_column == FieldMapColumn.LABEL:
                    continue
                self.table_view.openPersistentEditor(self.table_model.index(row, col))

    def close_persistent_editors(self):
        """Close all persistent editors in the table"""
        for row in range(self.table_model.rowCount()):
            for col, field_map_column in enumerate(FieldMapColumn):
                if field_map_column == FieldMapColumn.LABEL:
                    continue
                self.table_view.closePersistentEditor(self.table_model.index(row, col))

    def serialize(self) -> dict[str, dict[str, Any]]:
        return self.table_model.serialize()

    def deserialize(self, data: dict[str, dict[str, Any]]):
        self.table_model.deserialize(data)
