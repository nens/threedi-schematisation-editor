from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Any, Optional

from pydantic import ValidationError
from qgis.core import Qgis, QgsMessageLog, QgsVectorLayer
from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
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
    create_field_map_config,
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
    # Using a factory ensures that a unique instance is created for each row
    config: FieldMapConfig = field(
        default_factory=lambda: FieldMapConfig.model_construct(method=None)
    )

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
        if FieldMapColumn.from_index(index) == FieldMapColumn.VALUE_MAP:
            if (
                self.config.method == ColumnImportMethod.ATTRIBUTE
                and self.config.source_attribute not in [None, ""]
            ):
                return True
        # in any other case the method determines what is editable
        else:
            # identify required attribute, if any
            required_attribute = self.config._metadata.required_field_map.get(
                self.config.method
            )
            # find column where this attribute is expected
            required_column_idx = self.field_name_map.get(required_attribute, -1)
            return index == required_column_idx
        return False

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

    @property
    def valid_config(self) -> FieldMapConfig:
        return FieldMapConfig.model_validate(self.config.model_dump())

    def serialize(self) -> dict[str, Any]:
        return self.valid_config.model_dump()

    def deserialize(self, data: dict[str, Any]) -> None:
        # validation is done on initalization of FieldMapConfig
        self.config = FieldMapConfig(**data)

    @property
    def is_valid(self) -> bool:
        try:
            self.valid_config
            return True
        except ValidationError as e:
            return False


def create_field_map_row(
    label: str, allowed_methods: list[ColumnImportMethod], **kwargs
) -> FieldMapRow:
    field_map_config = create_field_map_config(allowed_methods)
    config = field_map_config.model_construct(method=None, **kwargs)
    return FieldMapRow(label=label, config=config)


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
        self.layer: QgsVectorLayer = None

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
        self.layer = layer
        self.layoutChanged.emit()

    def serialize(self) -> dict[str, dict[str, Any]]:
        return {attr_name: row.serialize() for attr_name, row in self.row_dict.items()}

    def deserialize(self, data: dict[str, dict[str, Any]]):
        for key, row_data in data.items():
            row = self.row_dict.get(key)
            if row:
                row.deserialize(row_data)

    @property
    def is_valid(self) -> bool:
        for row in self.rows:
            if not row.is_valid:
                return False
        return True


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
            combo = QComboBox(parent)
            combo.addItem("", None)
            row = index.model().rows[index.row()]
            for m in row.config._metadata.allowed_methods:
                # for m in ColumnImportMethod:
                combo.addItem(str(m), m)
            self._editors[(index.row(), index.column())] = combo
            combo.currentIndexChanged.connect(
                lambda idx, editor=combo: self.commitData.emit(editor)
            )
            return combo
        elif (
            FieldMapColumn.from_index(index.column()) == FieldMapColumn.SOURCE_ATTRIBUTE
        ):
            combo = QComboBox(parent)
            combo.addItems([""] + index.model().current_layer_attributes)
            combo.currentIndexChanged.connect(
                lambda idx, editor=combo: self.commitData.emit(editor)
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
                current_value_map if len(current_value_map) > 0 else "Set Value Map..."
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
            widget.setLayer(index.model().layer)
            widget.fieldChanged.connect(
                lambda field, idx=index: self.commitExpressionData(idx, widget)
            )
            self._editors[key] = widget
            return widget
        elif FieldMapColumn.from_index(index.column()) == FieldMapColumn.DEFAULT_VALUE:
            current_value = index.model().rows[index.row()].config.default_value
            widget = QLineEdit(parent)
            widget.setText(str(current_value) if current_value else "")
            self._editors[key] = widget
            return widget
        return super().createEditor(parent, option, index)

    def openValueMapDialog(self, index, button):
        """Open the value map dialog and update the model"""
        current_value_map = index.data(Qt.EditRole) if index.data(Qt.EditRole) else ""
        dialog = ValueMapDialog(current_value=current_value_map, parent=button)
        if dialog.exec_() == QDialog.Accepted:
            new_value_map = dialog.get_value_map()
            button.setText(
                new_value_map if len(new_value_map) > 0 else "Set Value Map..."
            )
            index.model().setData(index, new_value_map, Qt.EditRole)

    # def commitDefaultValueData(self, index, widget):
    #     """Commit default value widget data"""
    #     self.commitData.emit(widget)
    #
    def commitExpressionData(self, index, widget):
        """Commit expression widget data"""
        self.commitData.emit(widget)

    @staticmethod
    def get_invalid_style_for_editor(editor):
        if isinstance(editor, QComboBox):
            return f"QComboBox {{ background-color: {BACKGROUND_COLOR};}}"
        elif isinstance(editor, (QLineEdit, QgsFieldExpressionWidget)):
            return f"QLineEdit {{ background-color: {BACKGROUND_COLOR};}}"
        else:
            return ""

    def setEditorData(self, editor, index):
        # TODO: use data model to set styling for missing data!
        # Retrieve info from the model
        row = index.model().rows[index.row()]
        value = index.data(Qt.EditRole)
        has_layer = len(index.model().current_layer_attributes) > 0
        column = FieldMapColumn.from_index(index.column())
        valid = row.is_valid
        # Update enabled status
        if column == FieldMapColumn.LABEL:
            is_enabled = has_layer
        else:
            is_enabled = has_layer and row.is_editable(index.column())
        editor.setEnabled(is_enabled)
        # Update data in widgets
        if column in [FieldMapColumn.METHOD, FieldMapColumn.SOURCE_ATTRIBUTE]:
            if value:
                editor.setCurrentText(str(value))
            else:
                editor.setCurrentIndex(0)
        elif column == FieldMapColumn.VALUE_MAP:
            value_map_title = "Set value map..." if len(value) == 0 else str(value)
            editor.setText(value_map_title)
        elif column == FieldMapColumn.EXPRESSION:
            value = index.data(Qt.EditRole)
            editor.setExpression(value)
        elif column == FieldMapColumn.DEFAULT_VALUE:
            value = index.data(Qt.EditRole)
            editor.setText(str(value) if value else "")
        # update style
        style_sheet = (
            "" if valid or not is_enabled else self.get_invalid_style_for_editor(editor)
        )
        editor.setStyleSheet(style_sheet)

    def setModelData(self, editor, model, index):
        column = FieldMapColumn.from_index(index.column())
        value = None
        # Note that value_map is skipped because that is handled in the dialog
        if column == FieldMapColumn.METHOD:
            value = editor.currentData()
        elif column == FieldMapColumn.SOURCE_ATTRIBUTE:
            value = editor.currentText()
        elif column == FieldMapColumn.EXPRESSION:
            value = editor.expression()
        elif column == FieldMapColumn.DEFAULT_VALUE:
            value = editor.text()
        if value is not None:
            model.setData(index, value, Qt.EditRole)

    def destroyEditor(self, editor, index):
        key = (index.row(), index.column())
        if key in self._editors:
            del self._editors[key]
        super().destroyEditor(editor, index)

    def clear_editors(self):
        """Clear all tracked editors"""
        self._editors.clear()


class FieldMapWidget(QWidget):
    dataChanged = pyqtSignal()

    def __init__(self, row_dict):
        super().__init__()
        self.row_dict = row_dict
        self.table_model = FieldMapModel(self.row_dict)
        self.rows = self.table_model.rows
        self.setup_ui()

    def setup_ui(self):
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)

        # emit dataChanged signal when model data changes
        self.table_model.dataChanged.connect(self.dataChanged.emit)

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
        # TODO check values of value_map and expression after update
        # Notify the model of the changes so the view is updated
        self.table_model.layoutChanged.emit()

        # Clear delegate's editor cache
        self.table_delegate.clear_editors()

        # Open persistent editors for columns with always-visible widgets
        self.open_persistent_editors()

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
        # piggyback on update_layer to handle updating data
        self.update_layer(self.table_model.layer)

    @property
    def is_valid(self) -> bool:
        return self.table_model.is_valid
