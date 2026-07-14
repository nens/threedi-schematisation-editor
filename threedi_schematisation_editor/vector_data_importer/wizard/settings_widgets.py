from dataclasses import fields
from typing import Optional, Type

from pydantic import BaseModel
from qgis.core import Qgis, QgsExpression, QgsMapLayerProxyModel
from qgis.gui import QgsFieldExpressionWidget, QgsMapLayerComboBox
from qgis.PyQt.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, pyqtSignal
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QBoxLayout,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget,
    QWizardPage,
)

import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.enumerators import SewerageType
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    SourceSettings,
    create_field_map_config,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.vector_data_importer.wizard.field_map import (
    FieldMapColumn,
    FieldMapRow,
    FieldMapWidget,
)


def get_wizard(widget) -> Optional["QWizard"]:
    """Helper function to get the parent VDIWizard instance"""
    parent = widget.parent()
    if isinstance(widget.parent(), QWizardPage):
        return parent.wizard()
    return None


class LayerSettingsWidget(QWidget):
    layer_changed = pyqtSignal(str)  # Add this signal

    def __init__(
        self, layer_filter: Optional[Qgis.LayerFilters | Qgis.LayerFilter] = None
    ):
        super().__init__()
        self.model = SourceSettings()
        self.setup_ui(layer_filter)
        self.selected_layer = None

    def setup_ui(self, layer_filter):
        # create widgets
        self.layer_selector = QgsMapLayerComboBox()
        self.layer_selector.setAllowEmptyLayer(True)
        if layer_filter:
            self.layer_selector.setFilters(layer_filter)
        self.layer_selector.layerChanged.connect(self.update_layer)
        self.layer_selector.setCurrentIndex(0)
        self.layer_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.use_selected = QCheckBox("Selected features only")
        self.use_selected.setEnabled(False)
        self.include_expression = QgsFieldExpressionWidget()
        self.include_expression.setAllowEmptyFieldName(True)
        self.include_expression.setEnabled(False)
        expr_layout = QHBoxLayout()
        expr_layout.addWidget(QLabel("Select features with expression:"))
        expr_layout.addWidget(self.include_expression)
        # set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.layer_selector)
        layout.addWidget(self.use_selected)
        layout.addLayout(expr_layout)
        # Connect widgets to model updates
        self.use_selected.toggled.connect(self.update_use_selected)
        self.include_expression.fieldChanged.connect(self.update_include_expression)

    def update_layer(self, layer):
        if layer:
            self.selected_layer = layer
            self.model.selected_layer_name = layer.name()
            self.layer_changed.emit(layer.name())
            self.use_selected.setEnabled(len(layer.selectedFeatureIds()) > 0)
            self.include_expression.setLayer(layer)
            self.include_expression.setEnabled(True)
            self._clear_expression_if_invalid()
        else:
            self.selected_layer = None
            self.model.selected_layer_name = ""
            self.layer_changed.emit("")
            self.use_selected.setEnabled(False)
            self.include_expression.setLayer(None)
            self.include_expression.setEnabled(False)

    def _clear_expression_if_invalid(self):
        """Clear the expression if it references fields not present in the current layer."""
        expr_str = self.include_expression.expression()
        if not expr_str or self.selected_layer is None:
            return
        expr = QgsExpression(expr_str)
        if expr.hasParserError():
            self.include_expression.setExpression("")
            self.model.include_expression = None
            return
        field_names = {f.name() for f in self.selected_layer.fields()}
        unknown = expr.referencedColumns() - field_names - {"*"}
        if unknown:
            self.include_expression.setExpression("")
            self.model.include_expression = None

    def update_use_selected(self, checked):
        self.model.use_selected_features = checked

    def update_include_expression(self, expression):
        self.model.include_expression = expression or None

    def get_settings(self) -> SourceSettings:
        return self.model

    def deserialize(self, data: dict):
        self.use_selected.setChecked(data.get("use_selected_features", False))
        if self.selected_layer is None:
            layer_name = data.get("selected_layer_name") or ""
            if layer_name:
                idx = self.layer_selector.findText(layer_name)
                if idx >= 0:
                    self.layer_selector.setLayer(self.layer_selector.layer(idx))
        expr = data.get("include_expression") or ""
        self.include_expression.setExpression(expr)
        self.model.include_expression = expr or None
        self._clear_expression_if_invalid()


class SettingsWidget(QWidget):
    dataChanged = pyqtSignal()
    model = None

    @property
    def name(self) -> str:
        assert self.model is not None
        return self.model.name

    @property
    def group_name(self) -> str:
        raise NotImplementedError

    @property
    def is_valid(self) -> bool:
        return True

    def validate(self) -> bool:
        return self.is_valid

    def get_settings(self) -> BaseModel:
        # loudly fail when model is missing
        assert self.model is not None
        return self.model


class ConnectionNodeSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.ConnectionNodeSettings()
        self.setup_ui()

    @property
    def name(self) -> str:
        return "connection_nodes"

    @property
    def group_name(self):
        return "Connection node settings"

    def setup_ui(self):
        # Create widgets
        self.create_nodes = QCheckBox("Create new connection nodes if needed")
        self.snap = QCheckBox("Snap to existing connection nodes within: ")
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setSuffix(" m")
        self.snap_distance.setDecimals(1)
        self.snap_distance.setEnabled(False)
        self.snap_distance.setMinimum(sm.get_field_min(self.model, "snap_distance"))
        self.snap_distance.setMaximum(sm.get_field_max(self.model, "snap_distance"))
        self.snap_distance.setMaximumWidth(100)  # Set maximum width
        snap_layout = QHBoxLayout()
        snap_layout.addWidget(self.snap)
        snap_layout.addWidget(self.snap_distance)
        snap_layout.addStretch()  # This pushes everything to the left

        # Connect widgets to model updates
        self.create_nodes.toggled.connect(self.update_create_nodes)
        self.snap.toggled.connect(self.update_snap_enabled)
        self.snap.toggled.connect(self.on_snap_toggled)
        self.snap_distance.valueChanged.connect(self.update_snap_distance)

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.create_nodes)
        layout.addLayout(snap_layout)
        self.setLayout(layout)
        # set all widgets to default values
        self.deserialize({})

    def on_snap_toggled(self, checked):
        self.snap_distance.setEnabled(checked)

    def update_create_nodes(self, checked):
        self.model.create_nodes = checked

    def update_snap_enabled(self, checked):
        self.model.snap = checked

    def update_snap_distance(self, value):
        self.model.snap_distance = value

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.create_nodes.setChecked(self.model.create_nodes)
        self.snap.setChecked(self.model.snap)
        self.snap_distance.setValue(self.model.snap_distance)


class IntegrationSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.IntegrationSettings()
        self.setup_ui()

    @property
    def name(self):
        return "integration"

    @property
    def group_name(self):
        return "Integration settings"

    def update_integrate_on(self, checked: bool):
        # set integrate_on to specified value, but only if checked
        for integration_mode, radio_button in self.integration_mode_map.items():
            if radio_button.isChecked():
                self.model.integration_mode = integration_mode
                break

    def enable_integration_settings(self):
        if self.model.integration_mode == sm.IntegrationMode.NONE:
            self.settings_container.setEnabled(False)
        else:
            self.settings_container.setEnabled(True)

    def setup_integration_mode_radio_buttons(self, group_box):
        # Create radio buttons
        use_channels = QRadioButton("Channels")
        use_pipes = QRadioButton("Pipes")
        no_integration = QRadioButton("None")
        # Add all buttons to group to simplify handling behavior
        button_group = QButtonGroup(self)
        button_group.addButton(no_integration)
        button_group.addButton(use_channels)
        button_group.addButton(use_pipes)
        # Map radio buttons to IntegrationMode enum
        self.integration_mode_map = {
            sm.IntegrationMode.NONE: no_integration,
            sm.IntegrationMode.CHANNELS: use_channels,
            sm.IntegrationMode.PIPES: use_pipes,
        }
        # Explicitly link each radio button to updating the integrate_on settings
        for integration_mode, radio_button in self.integration_mode_map.items():
            radio_button.toggled.connect(
                lambda checked: self.update_integrate_on(checked)
            )
        # Link all buttons to updating the ingegration settings
        button_group.buttonToggled.connect(self.enable_integration_settings)
        # Organize vertically and add to layout
        radio_layout = QVBoxLayout()
        for button in button_group.buttons():
            radio_layout.addWidget(button)
        group_box.setLayout(radio_layout)

    def setup_integration_settings(self, settings_container):
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Snap to channel/pipe within"), 0, 0)
        grid_layout.addWidget(
            QLabel("Minimum length of a channel/pipe after edit"), 1, 0
        )
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setMinimum(sm.get_field_min(self.model, "snap_distance"))
        self.snap_distance.setMaximum(sm.get_field_max(self.model, "snap_distance"))
        self.snap_distance.setSuffix(" m")
        self.min_length = QDoubleSpinBox()
        self.min_length.setMinimum(sm.get_field_min(self.model, "min_length"))
        self.min_length.setMaximum(sm.get_field_max(self.model, "min_length"))
        self.min_length.setSuffix(" m")
        grid_layout.addWidget(self.snap_distance, 0, 1)
        grid_layout.addWidget(self.min_length, 1, 1)
        settings_container.setLayout(grid_layout)
        settings_container.setEnabled(False)

    def setup_ui(self):
        # Create radio buttons to choose integration mode
        integration_mode_widget = QGroupBox("Edit")
        self.setup_integration_mode_radio_buttons(integration_mode_widget)

        # Create container with integration settings
        self.settings_container = QWidget()
        self.setup_integration_settings(self.settings_container)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(integration_mode_widget)
        main_layout.addWidget(self.settings_container)
        self.setLayout(main_layout)
        self.deserialize({})

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.integration_mode_map[self.model.integration_mode].setChecked(True)
        self.snap_distance.setValue(self.model.snap_distance)
        self.min_length.setValue(self.model.min_length)


class CrossSectionDataRemapSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.CrossSectionDataRemap()
        self.setup_ui()

    @property
    def group_name(self):
        return "Align cross section table to reference level"

    def setup_ui(self):
        # Create widgets
        self.set_lowest_point_to_zero = QCheckBox("Set lowest point to zero")
        self.use_lowest_point_as_reference = QCheckBox(
            "Use lowest point as reference level"
        )

        # Connect widgets to model updates
        self.set_lowest_point_to_zero.toggled.connect(
            self.update_set_lowest_point_to_zero
        )
        self.use_lowest_point_as_reference.toggled.connect(
            self.update_use_lowest_point_as_reference
        )

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.set_lowest_point_to_zero)
        layout.addWidget(self.use_lowest_point_as_reference)
        self.setLayout(layout)

        # set all widgets to default values
        self.deserialize({})
        self.widget_layout = layout

    def update_set_lowest_point_to_zero(self, checked):
        self.model.set_lowest_point_to_zero = checked

    def update_use_lowest_point_as_reference(self, checked):
        self.model.use_lowest_point_as_reference = checked

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.set_lowest_point_to_zero.setChecked(self.model.set_lowest_point_to_zero)
        self.use_lowest_point_as_reference.setChecked(
            self.model.use_lowest_point_as_reference
        )


class FieldMapSettingsWidget(SettingsWidget):
    def setup_ui(self, row_dict, extra_layout=None):
        self.field_map_widget = FieldMapWidget(row_dict)
        # emit dataChanged signal when field map widget data changes
        self.field_map_widget.dataChanged.connect(self.dataChanged.emit)
        self.field_map_widget.open_persistent_editors()
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.field_map_widget)
        if extra_layout and isinstance(extra_layout, QBoxLayout):
            layout.addLayout(extra_layout)

    def _on_data_changed(self, top_left, bottom_right, roles):
        self.dataChanged.emit()

    def update_layer(self, layer):
        self.field_map_widget.update_layer(layer)

    def deserialize(self, data):
        self.field_map_widget.deserialize(data)

    @property
    def is_valid(self):
        return self.field_map_widget.is_valid

    def get_settings(self) -> BaseModel:
        return self.model


class PointToLIneConversionSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.PointToLineSettings()
        row_dict = {
            "length": FieldMapRow(label="Structure length", config=self.model.length),
            "azimuth": FieldMapRow(
                label="Structure direction (azimuth)", config=self.model.azimuth
            ),
        }
        self.setup_ui(row_dict)
        self.field_map_widget.table_model.set_default_value_units("length", " m")
        self.field_map_widget.table_model.set_default_value_units("azimuth", " °")

    @property
    def group_name(self):
        return "Point to line conversion settings"


class CrossSectionLocationMappingSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.CrossSectionLocationSettings()
        row_dict = {
            "join_field_src": FieldMapRow(
                label="Reference field in channel layer",
                config=self.model.join_field_src,
            ),
            "join_field_tgt": FieldMapRow(
                label="Join field in source layer", config=self.model.join_field_tgt
            ),
        }
        extra_layout = self.get_extra_layout()
        self.setup_ui(row_dict, extra_layout)
        # Use channel layer for join_field_src attributes
        self.field_map_widget.table_model.set_fixed_source_attributes_from_data_model(
            "join_field_src", dm.Channel
        )

    def get_extra_layout(self) -> list[QBoxLayout]:
        snap_distance_label = QLabel("Snap to geometry object within:")
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setSuffix(" m")
        self.snap_distance.setDecimals(1)
        self.snap_distance.setMinimum(sm.get_field_min(self.model, "snap_distance"))
        self.snap_distance.setMaximum(sm.get_field_max(self.model, "snap_distance"))
        self.snap_distance.setMaximumWidth(100)  # Set maximum width
        self.snap_distance.valueChanged.connect(self.update_snap_distance)
        snap_layout = QHBoxLayout()
        snap_layout.addWidget(snap_distance_label)
        snap_layout.addWidget(self.snap_distance)
        snap_layout.addStretch()
        return snap_layout

    def update_snap_distance(self, value):
        self.model.snap_distance = value

    def deserialize(self, data):
        super().deserialize(data)
        # load snap distance
        updated_model = self.model.__class__(**data)
        self.update_snap_distance(updated_model.snap_distance)
        self.snap_distance.setValue(updated_model.snap_distance)

    @property
    def group_name(self):
        return "Join to channel by attribute (optional)"

    def _sync_auto_methods(self, top_left, bottom_right, roles):
        table_model = self.field_map_widget.table_model
        if not roles or Qt.EditRole in roles:
            row_idx = top_left.row()
            other_row_idx = 0 if top_left.row() == 1 else 1
            method_column = FieldMapColumn.to_index(FieldMapColumn.METHOD)
            method = table_model.data(
                table_model.index(row_idx, method_column), Qt.EditRole
            )
            other_method = table_model.data(
                table_model.index(other_row_idx, method_column), Qt.EditRole
            )
            # check if this call was caused by changing the method to auto and if so set other method to auto
            if (
                method == ColumnImportMethod.AUTO
                and other_method != ColumnImportMethod.AUTO
            ):
                table_model.setData(
                    table_model.index(other_row_idx, method_column),
                    ColumnImportMethod.AUTO,
                    Qt.EditRole,
                )


_NUMERIC_QTYPES = {
    QVariant.Int,
    QVariant.LongLong,
    QVariant.Double,
    QVariant.UInt,
    QVariant.ULongLong,
}

# Ordered list of (display_name, sewerage_type_value) for the sewerage type combobox
_SEWERAGE_TYPE_ITEMS = [
    (t.name.replace("_", " ").capitalize(), t.value) for t in SewerageType
]


class SewerageTypeMappingModel(QAbstractTableModel):
    """Table model backing the sewerage type → percentage column mapping table."""

    SEWERAGE_TYPE_COL = 0
    PERCENTAGE_COL = 1
    HEADERS = ["Sewerage type", "Percentage column (%)"]

    def __init__(self, numeric_fields=None, parent=None):
        super().__init__(parent)
        self._rows = []
        self._numeric_fields = numeric_fields or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        value = self._rows[index.row()][index.column()]
        if index.column() == self.SEWERAGE_TYPE_COL:
            if value is None:
                return ""
            return next((n for n, v in _SEWERAGE_TYPE_ITEMS if v == value), "")
        return value or ""

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole or not index.isValid():
            return False
        self._rows[index.row()][index.column()] = value
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def add_row(self):
        row = len(self._rows)
        self.beginInsertRows(QModelIndex(), row, row)
        self._rows.append([None, None])
        self.endInsertRows()

    def remove_rows(self, rows):
        for row in sorted(rows, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._rows.pop(row)
            self.endRemoveRows()

    def set_numeric_fields(self, fields):
        self._numeric_fields = fields
        for row in self._rows:
            if row[self.PERCENTAGE_COL] not in fields:
                row[self.PERCENTAGE_COL] = None
        if self._rows:
            self.dataChanged.emit(
                self.index(0, self.PERCENTAGE_COL),
                self.index(len(self._rows) - 1, self.PERCENTAGE_COL),
            )

    def get_mappings(self):
        result = []
        for sewerage_type, col in self._rows:
            if sewerage_type is not None and col:
                result.append(
                    sm.SewerTypeMapping(
                        sewerage_type=sewerage_type,
                        percentage_column=col,
                    )
                )
        return result

    def set_mappings(self, mappings):
        self.beginResetModel()
        self._rows = [[m.sewerage_type, m.percentage_column] for m in mappings]
        if not self._rows:
            self._rows = [
                [SewerageType.COMBINED_SEWER, None],
                [SewerageType.STORM_DRAIN, None],
                [SewerageType.SANITARY_SEWER, None],
            ]
        self.endResetModel()


class SewerTypeMappingDelegate(QStyledItemDelegate):
    """Combobox delegate for both columns of the sewerage type mapping table."""

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        model = index.model()
        if index.column() == SewerageTypeMappingModel.SEWERAGE_TYPE_COL:
            combo.addItem("", None)
            for name, value in _SEWERAGE_TYPE_ITEMS:
                combo.addItem(name, value)
        else:
            combo.addItem("", None)
            for field_name in model._numeric_fields:
                combo.addItem(field_name, field_name)
        combo.currentIndexChanged.connect(lambda _: self.commitData.emit(combo))
        return combo

    def setEditorData(self, editor, index):
        row_value = index.model()._rows[index.row()][index.column()]
        idx = editor.findData(row_value)
        editor.setCurrentIndex(max(idx, 0))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentData(), Qt.EditRole)


class SurfaceLinkingSettingsWidget(SettingsWidget):
    """Combined data format selection, column mapping, and surface linking settings."""

    expanding = False

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.SurfaceLinkingSettings()
        self.setup_ui()
        self.deserialize({})

    @property
    def name(self) -> str:
        return sm.SurfaceLinkingSettings.name

    @property
    def group_name(self) -> str:
        return "Surface settings"

    def _make_sewerage_map_table(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        self._sewerage_model = SewerageTypeMappingModel()
        self._sewerage_model.dataChanged.connect(self._on_sewerage_mappings_changed)
        self._sewerage_model.rowsInserted.connect(self._on_sewerage_mappings_changed)
        self._sewerage_model.rowsRemoved.connect(self._on_sewerage_mappings_changed)
        self._sewerage_table = QTableView()
        self._sewerage_table.setModel(self._sewerage_model)
        self._sewerage_table.setItemDelegate(SewerTypeMappingDelegate())
        self._sewerage_table.verticalHeader().hide()
        self._sewerage_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._sewerage_table.setEditTriggers(
            QAbstractItemView.CurrentChanged | QAbstractItemView.SelectedClicked
        )
        header = self._sewerage_table.horizontalHeader()
        header.setSectionResizeMode(
            SewerageTypeMappingModel.SEWERAGE_TYPE_COL, QHeaderView.Stretch
        )
        header.setSectionResizeMode(
            SewerageTypeMappingModel.PERCENTAGE_COL, QHeaderView.Stretch
        )
        self._sewerage_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        _row_h = self._sewerage_table.verticalHeader().defaultSectionSize()
        _header_h = self._sewerage_table.horizontalHeader().sizeHint().height()
        self._sewerage_table.setMaximumHeight(_header_h + 5 * _row_h + 2)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        self._sewerage_add_btn = QPushButton("Add row")
        self._sewerage_add_btn.setIcon(QIcon.fromTheme("list-add"))
        self._sewerage_add_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._sewerage_add_btn.clicked.connect(self._sewerage_model.add_row)
        self._sewerage_del_btn = QPushButton("Delete row")
        self._sewerage_del_btn.setIcon(QIcon.fromTheme("list-remove"))
        self._sewerage_del_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._sewerage_del_btn.clicked.connect(self._delete_sewerage_rows)
        btn_layout.addWidget(self._sewerage_del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self._sewerage_add_btn)
        layout.addWidget(self._sewerage_table)
        layout.addLayout(btn_layout)
        return layout

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- Format selection ---
        self.fmt_long_radio = QRadioButton(
            "One sewerage type per row, retrieved from the following fields: "
        )
        self.fmt_long_radio.setChecked(True)
        self.fmt_wide_radio = QRadioButton(
            "Multiple sewerage types per row with a percentage column for each:"
        )
        sewerage_type_fm_config = create_field_map_config(
            allowed_methods=[
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.DEFAULT,
                ColumnImportMethod.EXPRESSION,
            ],
            field_type=SewerageType,
        )
        sewerage_type_row_dict = {
            "sewerage_type": FieldMapRow(
                label="Sewerage type",
                config=sewerage_type_fm_config.model_construct(method=None),
            )
        }
        self.sewerage_type_field_map_widget = FieldMapWidget(
            sewerage_type_row_dict,
            hidden_columns=[FieldMapColumn.LABEL],
        )
        self.sewerage_type_field_map_widget.open_persistent_editors()

        fmt_group = QButtonGroup(self)
        fmt_group.addButton(self.fmt_long_radio)
        fmt_group.addButton(self.fmt_wide_radio)
        fmt_layout = QGridLayout()
        fmt_layout.addWidget(QLabel("Input table format:"), 0, 0)
        fmt_layout.addWidget(self.fmt_long_radio, 1, 0)
        fmt_layout.addWidget(self.sewerage_type_field_map_widget, 2, 0, 1, 4)
        fmt_layout.addWidget(self.fmt_wide_radio, 3, 0)
        fmt_layout.addLayout(self._make_sewerage_map_table(), 4, 0, 1, 4)
        layout.addLayout(fmt_layout)

        # --- Linking section ---
        linking_group = QGroupBox("Linking settings")
        linking_layout = QVBoxLayout(linking_group)
        _defaults = sm.SurfaceLinkingSettings()
        self.match_no_table_radio = QRadioButton("None")
        self.match_no_table_radio.setChecked(True)
        self.match_pipe_table_radio = QRadioButton("Pipe")
        self.match_node_table_radio = QRadioButton("Connection node")
        match_table_group = QButtonGroup(self)
        match_table_group.addButton(self.match_no_table_radio)
        match_table_group.addButton(self.match_pipe_table_radio)
        match_table_group.addButton(self.match_node_table_radio)
        match_row = QHBoxLayout()
        match_row.addWidget(self.match_no_table_radio)
        match_row.addWidget(self.match_pipe_table_radio)
        match_row.addWidget(self.match_node_table_radio)
        match_row.addStretch()
        linking_layout.addLayout(match_row)
        target_config = create_field_map_config(
            allowed_methods=[
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.EXPRESSION,
            ]
        )
        source_config = create_field_map_config(
            allowed_methods=[
                ColumnImportMethod.ATTRIBUTE,
                ColumnImportMethod.EXPRESSION,
            ]
        )
        match_row_dict = {
            "attribute_match_target": FieldMapRow(
                label="Match field in pipe", config=target_config.model_construct(method=None)
            ),
            "attribute_match_input": FieldMapRow(
                label="Source value", config=source_config.model_construct(method=None)
            ),
        }
        self.match_field_map_widget = FieldMapWidget(
            match_row_dict,
            hidden_columns=[FieldMapColumn.DEFAULT_VALUE],
        )
        self.match_field_map_widget.open_persistent_editors()
        # Fix the label column width to fit the longest possible label
        # ("Match field in connection node") so it doesn't resize when table changes
        header = self.match_field_map_widget.table_view.horizontalHeader()
        fm = self.match_field_map_widget.table_view.fontMetrics()
        min_width = fm.horizontalAdvance(f"Match field in {dm.ConnectionNode.__layername__}") + 16
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.match_field_map_widget.table_view.setColumnWidth(0, min_width)
        linking_layout.addWidget(self.match_field_map_widget)

        spat_row = QHBoxLayout()
        self.match_spatial_checkbox = QCheckBox(
            "Use spatial matching with search distance:"
        )
        self.search_distance = QDoubleSpinBox()
        self.search_distance.setDecimals(1)
        self.search_distance.setMinimum(
            sm.get_field_min(sm.SurfaceLinkingSettings, "search_distance")
        )
        self.search_distance.setMaximum(
            sm.get_field_max(sm.SurfaceLinkingSettings, "search_distance")
        )
        self.search_distance.setValue(_defaults.search_distance)
        self.search_distance.setSuffix(" m")
        spat_row.addWidget(self.search_distance)
        spat_row.addWidget(self.match_spatial_checkbox)
        spat_row.addStretch()
        linking_layout.addLayout(spat_row)

        self.selected_pipes_only = QCheckBox("Only match selected pipes")
        linking_layout.addWidget(self.selected_pipes_only)
        layout.addWidget(linking_group)
        # Signal connections
        self.fmt_long_radio.toggled.connect(self._on_format_changed)
        self.sewerage_type_field_map_widget.dataChanged.connect(
            self._on_sewerage_type_config_changed
        )
        self.match_no_table_radio.toggled.connect(self._on_match_table_changed)
        self.match_pipe_table_radio.toggled.connect(self._on_match_table_changed)
        self.match_node_table_radio.toggled.connect(self._on_match_table_changed)
        self.match_field_map_widget.dataChanged.connect(self._on_match_input_changed)
        self.match_spatial_checkbox.toggled.connect(self._on_spatial_match_changed)
        self.search_distance.valueChanged.connect(self._on_search_distance_changed)
        self.selected_pipes_only.toggled.connect(self._on_selected_pipes_only_changed)

        self._set_wide_mapping_enabled(not self.fmt_long_radio.isChecked())
        self._update_linking_enabled()

    def _sewerage_type_source_present(self):
        if self.fmt_long_radio.isChecked():
            return self.sewerage_type_field_map_widget.is_valid
        return bool(self._sewerage_model.get_mappings())

    def _update_linking_enabled(self):
        match_active = not self.match_no_table_radio.isChecked()
        self.match_field_map_widget.setEnabled(match_active)
        self.search_distance.setEnabled(self.match_spatial_checkbox.isChecked())

    def _set_wide_mapping_enabled(self, enabled):
        self._sewerage_table.setEnabled(enabled)
        self._sewerage_add_btn.setEnabled(enabled)
        self._sewerage_del_btn.setEnabled(enabled)

    def _on_format_changed(self, long_checked):
        self.sewerage_type_field_map_widget.setEnabled(long_checked)
        self._set_wide_mapping_enabled(not long_checked)
        self.model.data_format = "long" if long_checked else "wide"
        self._update_linking_enabled()
        self.dataChanged.emit()

    def _on_match_table_changed(self):
        match_model = self._match_table_model()
        self.model.attribute_match_enabled = not self.match_no_table_radio.isChecked()
        self.model.attribute_match_table = (
            match_model.__tablename__ if match_model is not None else None
        )
        if match_model is not None:
            self._update_target_label(match_model)
        self._update_linking_enabled()
        self.dataChanged.emit()

    def _update_target_label(self, match_model):
        label = f"Match field in {match_model.__layername__}"
        table_model = self.match_field_map_widget.table_model
        table_model.attr_to_label_map["attribute_match_target"] = label
        table_model.row_dict["attribute_match_target"].label = label
        table_model.set_fixed_source_attributes_from_data_model(
            "attribute_match_target", match_model
        )
        table_model.layoutChanged.emit()

    def _on_sewerage_type_config_changed(self):
        self._sync_sewerage_type_config()
        self._update_linking_enabled()
        self.dataChanged.emit()

    def _sync_sewerage_type_config(self):
        sewerage_type_cfg = (
            self.sewerage_type_field_map_widget.get_settings().get("sewerage_type")
            if self.fmt_long_radio.isChecked()
            and self.sewerage_type_field_map_widget.is_valid
            else None
        )
        self.model.sewerage_type_config = sewerage_type_cfg

    def _on_sewerage_mappings_changed(self, *args):
        self.model.sewerage_type_mappings = self._sewerage_model.get_mappings()
        self._update_linking_enabled()
        self.dataChanged.emit()

    def _on_match_input_changed(self):
        self._sync_match_input_config()
        self.dataChanged.emit()

    def _sync_match_input_config(self):
        if not self.model.attribute_match_enabled or not self.match_field_map_widget.is_valid:
            self.model.attribute_match_target_config = None
            self.model.attribute_match_input_config = None
            return
        settings = self.match_field_map_widget.get_settings()
        self.model.attribute_match_target_config = settings.get("attribute_match_target")
        self.model.attribute_match_input_config = settings.get("attribute_match_input")

    def _on_spatial_match_changed(self, checked):
        self.model.spatial_match_enabled = checked
        self._update_linking_enabled()
        self.dataChanged.emit()

    def _on_search_distance_changed(self, value):
        self.model.search_distance = value
        self.dataChanged.emit()

    def _on_selected_pipes_only_changed(self, checked):
        self.model.selected_pipes_only = checked
        self.dataChanged.emit()

    def _match_table_model(self):
        if self.match_pipe_table_radio.isChecked():
            return dm.Pipe
        elif self.match_node_table_radio.isChecked():
            return dm.ConnectionNode
        return None

    def _delete_sewerage_rows(self):
        rows = sorted(
            {idx.row() for idx in self._sewerage_table.selectedIndexes()}, reverse=True
        )
        if rows:
            self._sewerage_model.remove_rows(rows)

    def update_layer(self, layer):
        """Populate column dropdowns and wide table with fields from source layer."""
        columns = [f.name() for f in layer.fields()] if layer else []
        numeric = (
            [f.name() for f in layer.fields() if f.type() in _NUMERIC_QTYPES]
            if layer
            else []
        )
        self.sewerage_type_field_map_widget.update_layer(layer)
        self._sewerage_model.set_numeric_fields(numeric)
        self.match_field_map_widget.update_layer(layer)
        self._update_model()

    def _update_model(self):
        """Full model rebuild from current UI state. Called after layer changes."""
        match_model = self._match_table_model()
        match_table = match_model.__tablename__ if match_model is not None else None
        match_by_table = not self.match_no_table_radio.isChecked()
        settings = (
            self.match_field_map_widget.get_settings()
            if match_by_table and self.match_field_map_widget.is_valid
            else {}
        )
        target_cfg = settings.get("attribute_match_target")
        input_cfg = settings.get("attribute_match_input")
        sewerage_type_cfg = (
            self.sewerage_type_field_map_widget.get_settings().get("sewerage_type")
            if self.fmt_long_radio.isChecked()
            and self.sewerage_type_field_map_widget.is_valid
            else None
        )
        self.model = sm.SurfaceLinkingSettings(
            data_format="long" if self.fmt_long_radio.isChecked() else "wide",
            sewerage_type_config=sewerage_type_cfg,
            sewerage_type_mappings=self._sewerage_model.get_mappings(),
            search_distance=self.search_distance.value(),
            selected_pipes_only=self.selected_pipes_only.isChecked(),
            attribute_match_enabled=match_by_table,
            spatial_match_enabled=self.match_spatial_checkbox.isChecked(),
            attribute_match_table=match_table,
            attribute_match_target_config=target_cfg,
            attribute_match_input_config=input_cfg,
        )
        self._update_linking_enabled()
        self.dataChanged.emit()

    @property
    def is_valid(self) -> bool:
        if self.fmt_long_radio.isChecked():
            if not self.sewerage_type_field_map_widget.is_valid:
                return False
        else:
            if not self._sewerage_model.get_mappings():
                return False
        if not self.match_no_table_radio.isChecked():
            if not self.match_field_map_widget.is_valid:
                return False
        return True

    def validate(self) -> bool:
        if (
            not self.fmt_long_radio.isChecked()
            and not self._sewerage_model.get_mappings()
        ):
            reply = QMessageBox.warning(
                self,
                "No sewerage type mappings",
                "No sewerage type mappings are configured. "
                "Surfaces will be imported without any surface map entries.\n\n"
                "Continue anyway?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            return reply == QMessageBox.Yes
        return True

    def get_settings(self) -> sm.SurfaceLinkingSettings:
        return self.model

    def deserialize(self, data):
        loaded_model = (
            sm.SurfaceLinkingSettings(**data) if data else sm.SurfaceLinkingSettings()
        )
        is_long = loaded_model.data_format == "long"
        self.fmt_long_radio.setChecked(is_long)
        self.fmt_wide_radio.setChecked(not is_long)
        if loaded_model.sewerage_type_config:
            self.sewerage_type_field_map_widget.deserialize(
                {"sewerage_type": loaded_model.sewerage_type_config.model_dump()}
            )
        self.sewerage_type_field_map_widget.setEnabled(is_long)
        self._sewerage_model.set_mappings(loaded_model.sewerage_type_mappings)
        if loaded_model.attribute_match_enabled:
            if loaded_model.attribute_match_table == dm.Pipe.__tablename__:
                self.match_pipe_table_radio.setChecked(True)
                match_model = dm.Pipe
            else:
                self.match_node_table_radio.setChecked(True)
                match_model = dm.ConnectionNode
            self._update_target_label(match_model)
        else:
            self.match_no_table_radio.setChecked(True)
        deserialize_data = {}
        if loaded_model.attribute_match_target_config:
            deserialize_data["attribute_match_target"] = loaded_model.attribute_match_target_config.model_dump()
        if loaded_model.attribute_match_input_config:
            deserialize_data["attribute_match_input"] = loaded_model.attribute_match_input_config.model_dump()
        if deserialize_data:
            self.match_field_map_widget.deserialize(deserialize_data)
        self.match_spatial_checkbox.setChecked(loaded_model.spatial_match_enabled)
        self.search_distance.setValue(loaded_model.search_distance)
        self.selected_pipes_only.setChecked(loaded_model.selected_pipes_only)
        self.model = loaded_model
        self._update_linking_enabled()
