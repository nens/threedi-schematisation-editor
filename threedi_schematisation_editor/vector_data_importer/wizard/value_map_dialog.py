from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QPushButton,
    QTableView,
    QVBoxLayout,
)


class ValueMapModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._sources: List[str] = []
        self._targets: List[str] = []

    @property
    def sources(self):
        return self._sources

    def rowCount(self, parent=None):
        return len(self._sources)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        row = index.row()
        if index.column() == 0:
            return self._sources[row]
        else:
            return self._targets[row]

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        row = index.row()
        value = str(value)
        if index.column() == 0:
            self._sources[row] = value
        else:
            self._targets[row] = value
        self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ["Source attribute value", "Target attribute value"][section]
        return str(section + 1)

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def addRow(self, source="", target=""):
        row = len(self._sources)
        self.beginInsertRows(self.index(row, 0).parent(), row, row)
        self._sources.append(source)
        self._targets.append(target)
        self.endInsertRows()

    def removeRow(self, row):
        self.beginRemoveRows(self.index(row, 0).parent(), row, row)
        self._sources.pop(row)
        self._targets.pop(row)
        self.endRemoveRows()

    def getDict(self) -> dict[str, str]:
        return {src: tgt for src, tgt in zip(self._sources, self._targets) if src}

    def setFromDict(self, data: dict[str, str]):
        self.beginResetModel()
        self._sources = list(data.keys())
        self._targets = list(data.values())
        self.endResetModel()


class ValueMapDialog(QDialog):
    SRC_COLUMN_IDX = 0
    TGT_COLUMN_IDX = 1

    def __init__(self, row, layer, parent=None):
        self.row = row
        self.layer = layer
        self.model = ValueMapModel()
        super().__init__(parent)
        self.setWindowTitle("Value Map")
        self.setup_ui()
        self.setMinimumSize(self.sizeHint())
        self.model.setFromDict(self.row.config.value_map)

    def sizeHint(self):
        # Get the width needed for the columns plus some padding
        width = sum(self.table.horizontalHeader().sectionSize(i) for i in range(2)) + 50
        # Height for about 10 rows plus buttons and margins
        height = (
            self.table.verticalHeader().defaultSectionSize() * 10
            + self.add_button.sizeHint().height()
            + 100
        )
        return QSize(width, height)

    def setup_ui(self):
        # Create and setup table
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.verticalHeader().hide()

        # Set table columns to stretch
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(self.SRC_COLUMN_IDX, QHeaderView.Stretch)
        header.setSectionResizeMode(self.TGT_COLUMN_IDX, QHeaderView.Stretch)

        # Create buttons for table interaction
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.add_button.setToolTip(
            "Add a new after selected row(s) or at the end of the table"
        )
        self.delete_button = QPushButton("Delete")
        self.delete_button.setToolTip("Delete selected rows")
        self.load_layer_button = QPushButton("Load from source layer")

        # Add buttons to layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.load_layer_button)

        # Connect signals
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_selected_rows)
        self.load_layer_button.clicked.connect(self.load_from_source_layer)

        # Create buttons for accepting / closing
        dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal,
            self,
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(dialog_buttons)

    def add_row(self):
        """Add a new empty row to the table"""
        self.model.addRow()

    def delete_selected_rows(self):
        """Delete selected rows from the table"""
        selected_rows = sorted(
            {idx.row() for idx in self.table.selectedIndexes()}, reverse=True
        )
        for row in selected_rows:
            self.model.removeRow(row)

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

    def load_from_source_layer(self):
        # Create dialog to select layer
        field_names = [field.name() for field in self.layer.fields()]
        title = "Load source layer values"
        message = "Unique values source field"
        source_attribute = self.row.config.source_attribute
        current_idx = (
            field_names.index(source_attribute)
            if source_attribute in field_names
            else 0
        )
        selected_field_name, accept = QInputDialog.getItem(
            self, title, message, field_names, current_idx, editable=False
        )
        if not accept:
            return
        # Copy new data to table
        selected_field_idx = self.layer.fields().lookupField(selected_field_name)
        for value in self.layer.uniqueValues(selected_field_idx):
            if value in self.model.sources:
                continue
            self.model.addRow(source=value)

    def get_value_map(self):
        return self.model.getDict()
