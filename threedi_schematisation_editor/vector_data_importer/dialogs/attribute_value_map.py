import ast

from qgis.core import NULL
from qgis.PyQt.QtWidgets import QInputDialog, QTableWidgetItem

from threedi_schematisation_editor.utils import QUOTED_NULL


class AttributeValueMapDialog:
    """Dialog for setting attribute value mappings."""

    SRC_COLUMN_IDX = 0
    DST_COLUMN_IDX = 1

    def __init__(
        self, pressed_button, source_attribute_combobox, source_layer, parent=None
    ):
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
        for row_number, (source_value, target_value) in enumerate(
            self.pressed_button.value_map.items()
        ):
            source_value = self.format_value_map_data(source_value)
            target_value = self.format_value_map_data(target_value)
            self.value_map_table.insertRow(row_number)
            self.value_map_table.setItem(
                row_number, self.SRC_COLUMN_IDX, QTableWidgetItem(source_value)
            )
            self.value_map_table.setItem(
                row_number, self.DST_COLUMN_IDX, QTableWidgetItem(target_value)
            )
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
            selected_rows = {
                idx.row() for idx in self.value_map_table.selectedIndexes()
            }
            if selected_rows:
                last_row_number = max(selected_rows) + 1
            else:
                last_row_number = row_count
            unique_values = self.source_layer.uniqueValues(selected_field_name_idx)
            existing_values = {
                self.value_map_table.item(row, self.SRC_COLUMN_IDX).text()
                for row in range(row_count)
            }
            skipped_rows = 0
            for i, source_value in enumerate(
                sorted(unique_values), start=last_row_number
            ):
                source_value_str = self.format_value_map_data(source_value)
                if source_value_str in existing_values:
                    skipped_rows += 1
                    continue
                new_row_number = i - skipped_rows
                self.value_map_table.insertRow(new_row_number)
                self.value_map_table.setItem(
                    new_row_number,
                    self.SRC_COLUMN_IDX,
                    QTableWidgetItem(source_value_str),
                )
                self.value_map_table.setItem(
                    new_row_number, self.DST_COLUMN_IDX, QTableWidgetItem(QUOTED_NULL)
                )

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
