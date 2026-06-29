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
        label = QLabel("Select layer to import:")
        self.layer_selector = QgsMapLayerComboBox()
        self.layer_selector.setAllowEmptyLayer(True)
        if layer_filter:
            self.layer_selector.setFilters(layer_filter)
        self.layer_selector.layerChanged.connect(self.update_layer)
        self.layer_selector.setCurrentIndex(0)
        self.layer_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.use_selected = QCheckBox("Selected features only")
        self.use_selected.setEnabled(False)
        self.filter_expression = QgsFieldExpressionWidget()
        self.filter_expression.setAllowEmptyFieldName(True)
        self.filter_expression.setEnabled(False)
        expr_layout = QHBoxLayout()
        expr_layout.addWidget(QLabel("Filter expression:"))
        expr_layout.addWidget(self.filter_expression)
        # set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.layer_selector)
        layout.addWidget(self.use_selected)
        layout.addLayout(expr_layout)
        # Connect widgets to model updates
        self.use_selected.toggled.connect(self.update_use_selected)
        self.filter_expression.fieldChanged.connect(self.update_filter_expression)

    def update_layer(self, layer):
        if layer:
            self.selected_layer = layer
            self.model.selected_layer_name = layer.name()
            self.layer_changed.emit(layer.name())
            self.use_selected.setEnabled(len(layer.selectedFeatureIds()) > 0)
            self.filter_expression.setLayer(layer)
            self.filter_expression.setEnabled(True)
            self._clear_expression_if_invalid()
        else:
            self.selected_layer = None
            self.model.selected_layer_name = ""
            self.layer_changed.emit("")
            self.use_selected.setEnabled(False)
            self.filter_expression.setLayer(None)
            self.filter_expression.setEnabled(False)

    def _clear_expression_if_invalid(self):
        """Clear the expression if it references fields not present in the current layer."""
        expr_str = self.filter_expression.expression()
        if not expr_str or self.selected_layer is None:
            return
        expr = QgsExpression(expr_str)
        if expr.hasParserError():
            self.filter_expression.setExpression("")
            self.model.filter_expression = None
            return
        field_names = {f.name() for f in self.selected_layer.fields()}
        unknown = expr.referencedColumns() - field_names - {"*"}
        if unknown:
            self.filter_expression.setExpression("")
            self.model.filter_expression = None

    def update_use_selected(self, checked):
        self.model.use_selected_features = checked

    def update_filter_expression(self, expression):
        self.model.filter_expression = expression or None

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
        expr = data.get("filter_expression") or ""
        self.filter_expression.setExpression(expr)
        self.model.filter_expression = expr or None
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


class SewerTypeMappingModel(QAbstractTableModel):
    """Table model backing the sewerage type → percentage column mapping table."""

    SEWERAGE_TYPE_COL = 0
    PERCENTAGE_COL = 1
    HEADERS = ["Sewerage type", "Percentage column"]

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
            self._rows = [[None, None]]
        self.endResetModel()


class SewerTypeMappingDelegate(QStyledItemDelegate):
    """Combobox delegate for both columns of the sewerage type mapping table."""

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        model = index.model()
        if index.column() == SewerTypeMappingModel.SEWERAGE_TYPE_COL:
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


class SewerTypePreferenceModel(QAbstractTableModel):
    """Table model backing the sewerage type → preference offset (m) table."""

    SEWERAGE_TYPE_COL = 0
    PREFERENCE_COL = 1
    HEADERS = ["Sewerage type", "Preference (m)"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

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
        return value if value is not None else 0.0

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
        self._rows.append([None, 0.0])
        self.endInsertRows()

    def remove_rows(self, rows):
        for row in sorted(rows, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row)
            self._rows.pop(row)
            self.endRemoveRows()

    def get_preferences(self):
        result = []
        for sewerage_type, preference in self._rows:
            if sewerage_type is not None:
                result.append(
                    sm.SewerTypePreference(
                        sewerage_type=sewerage_type,
                        preference=preference or 0.0,
                    )
                )
        return result

    def set_preferences(self, preferences):
        self.beginResetModel()
        self._rows = [[p.sewerage_type, p.preference] for p in preferences]
        self.endResetModel()


class SewerTypePreferenceDelegate(QStyledItemDelegate):
    """Delegate for the sewerage type preference table.

    Column 0: sewerage type combobox (same items as SewerTypeMappingDelegate).
    Column 1: plain double editor.
    """

    def createEditor(self, parent, option, index):
        if index.column() == SewerTypePreferenceModel.SEWERAGE_TYPE_COL:
            combo = QComboBox(parent)
            combo.addItem("", None)
            for name, value in _SEWERAGE_TYPE_ITEMS:
                combo.addItem(name, value)
            combo.currentIndexChanged.connect(lambda _: self.commitData.emit(combo))
            return combo
        spinbox = QDoubleSpinBox(parent)
        spinbox.setDecimals(1)
        spinbox.setRange(0, 1000000.0)
        spinbox.setSuffix(" m")
        return spinbox

    def setEditorData(self, editor, index):
        value = index.model()._rows[index.row()][index.column()]
        if index.column() == SewerTypePreferenceModel.SEWERAGE_TYPE_COL:
            idx = editor.findData(value)
            editor.setCurrentIndex(max(idx, 0))
        else:
            editor.setValue(value or 0.0)

    def setModelData(self, editor, model, index):
        if index.column() == SewerTypePreferenceModel.SEWERAGE_TYPE_COL:
            model.setData(index, editor.currentData(), Qt.EditRole)
        else:
            model.setData(index, editor.value(), Qt.EditRole)


class SurfaceMapPercentageSettingsWidget(SettingsWidget):
    """Maps sewerage types to the source percentage column for surface_map creation."""

    expanding = True  # tells SettingsPage to give this widget vertical stretch

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.SurfaceMapPercentageSettings()
        self.setup_ui()

    @property
    def name(self) -> str:
        return sm.SurfaceMapPercentageSettings.name

    @property
    def group_name(self) -> str:
        return "Sewerage type → percentage column"

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self._sewer_model = SewerTypeMappingModel()
        self._sewer_model.add_row()  # start with one empty row
        self._sewer_model.dataChanged.connect(self._update_sewer_model)
        self._sewer_model.rowsInserted.connect(self._update_sewer_model)
        self._sewer_model.rowsRemoved.connect(self._update_sewer_model)

        self._sewer_table = QTableView()
        self._sewer_table.setModel(self._sewer_model)
        self._sewer_table.setItemDelegate(SewerTypeMappingDelegate())
        self._sewer_table.verticalHeader().hide()
        self._sewer_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._sewer_table.setEditTriggers(
            QAbstractItemView.CurrentChanged | QAbstractItemView.SelectedClicked
        )
        header = self._sewer_table.horizontalHeader()
        header.setSectionResizeMode(
            SewerTypeMappingModel.SEWERAGE_TYPE_COL, QHeaderView.Stretch
        )
        header.setSectionResizeMode(
            SewerTypeMappingModel.PERCENTAGE_COL, QHeaderView.Stretch
        )
        self._sewer_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        add_btn = QPushButton("Add row")
        add_btn.setIcon(QIcon.fromTheme("list-add"))
        add_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_btn.clicked.connect(self._sewer_model.add_row)
        del_btn = QPushButton("Delete row")
        del_btn.setIcon(QIcon.fromTheme("list-remove"))
        del_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        del_btn.clicked.connect(self._delete_sewer_rows)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(add_btn)

        layout.addWidget(self._sewer_table)
        layout.addLayout(btn_layout)

    def update_layer(self, layer):
        """Populate percentage column combo with numeric fields from source layer."""
        numeric_fields = (
            [f.name() for f in layer.fields() if f.type() in _NUMERIC_QTYPES]
            if layer
            else []
        )
        self._sewer_model.set_numeric_fields(numeric_fields)

    def _delete_sewer_rows(self):
        rows = sorted(
            {idx.row() for idx in self._sewer_table.selectedIndexes()}, reverse=True
        )
        if rows:
            self._sewer_model.remove_rows(rows)

    def _update_sewer_model(self):
        self.model.sewer_type_mappings = self._sewer_model.get_mappings()
        self.dataChanged.emit()

    @property
    def is_valid(self) -> bool:
        return True

    def validate(self) -> bool:
        if not self._sewer_model.get_mappings():
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

    def get_settings(self) -> sm.SurfaceMapPercentageSettings:
        return self.model

    def deserialize(self, data):
        self.model = (
            sm.SurfaceMapPercentageSettings(**data)
            if data
            else sm.SurfaceMapPercentageSettings()
        )
        self._sewer_model.set_mappings(self.model.sewer_type_mappings)


class SurfaceConnectionSettingsWidget(SettingsWidget):
    """Settings for linking surfaces to pipes and connection nodes."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.SurfaceLinkingSettings()
        self.setup_ui()

    @property
    def name(self) -> str:
        return sm.SurfaceLinkingSettings.name

    @property
    def group_name(self) -> str:
        return "Spatial linking"

    def setup_ui(self):
        layout = QGridLayout()

        layout.addWidget(QLabel("Surface map layer:"), 0, 0)
        self._surface_map_layer = QgsMapLayerComboBox()
        self._surface_map_layer.setAllowEmptyLayer(True)
        self._surface_map_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
        self._surface_map_layer.setCurrentText(dm.SurfaceMap.__layername__)
        layout.addWidget(self._surface_map_layer, 0, 1)

        layout.addWidget(QLabel("Pipe layer:"), 1, 0)
        self._pipe_layer = QgsMapLayerComboBox()
        self._pipe_layer.setAllowEmptyLayer(True)
        self._pipe_layer.setFilters(QgsMapLayerProxyModel.LineLayer)
        self._pipe_layer.setCurrentText(dm.Pipe.__layername__)
        self._selected_pipes_only = QCheckBox("Selected only")
        pipe_row = QHBoxLayout()
        pipe_row.addWidget(self._pipe_layer)
        pipe_row.addWidget(self._selected_pipes_only)
        layout.addLayout(pipe_row, 1, 1)

        layout.addWidget(QLabel("Connection node layer:"), 2, 0)
        self._node_layer = QgsMapLayerComboBox()
        self._node_layer.setAllowEmptyLayer(True)
        self._node_layer.setFilters(QgsMapLayerProxyModel.PointLayer)
        self._node_layer.setCurrentText(dm.ConnectionNode.__layername__)
        layout.addWidget(self._node_layer, 2, 1)

        _defaults = sm.SurfaceLinkingSettings()

        layout.addWidget(QLabel("Search distance (m):"), 3, 0)
        self._search_distance = QDoubleSpinBox()
        self._search_distance.setDecimals(1)
        self._search_distance.setMinimum(
            sm.get_field_min(sm.SurfaceLinkingSettings, "search_distance")
        )
        self._search_distance.setMaximum(
            sm.get_field_max(sm.SurfaceLinkingSettings, "search_distance")
        )
        self._search_distance.setValue(_defaults.search_distance)
        self._search_distance.setSuffix(" m")
        layout.addWidget(self._search_distance, 3, 1)

        self._search_distance.valueChanged.connect(self._update_model)
        self._surface_map_layer.layerChanged.connect(self._update_model)
        self._pipe_layer.layerChanged.connect(self._update_model)
        self._node_layer.layerChanged.connect(self._update_model)
        self._selected_pipes_only.toggled.connect(self._update_model)

        # Preference table — placed below the grid in a VBoxLayout wrapper
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addLayout(layout)

        pref_label = QLabel("Sewerage type preference offsets:")
        outer_layout.addWidget(pref_label)

        self._pref_model = SewerTypePreferenceModel()
        self._pref_model.dataChanged.connect(self._update_model)
        self._pref_model.rowsInserted.connect(self._update_model)
        self._pref_model.rowsRemoved.connect(self._update_model)

        self._pref_table = QTableView()
        self._pref_table.setModel(self._pref_model)
        self._pref_table.setItemDelegate(SewerTypePreferenceDelegate())
        self._pref_table.verticalHeader().hide()
        self._pref_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._pref_table.setEditTriggers(
            QAbstractItemView.CurrentChanged | QAbstractItemView.SelectedClicked
        )
        header = self._pref_table.horizontalHeader()
        header.setSectionResizeMode(
            SewerTypePreferenceModel.SEWERAGE_TYPE_COL, QHeaderView.Stretch
        )
        header.setSectionResizeMode(
            SewerTypePreferenceModel.PREFERENCE_COL, QHeaderView.Stretch
        )
        outer_layout.addWidget(self._pref_table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add row")
        add_btn.setIcon(QIcon.fromTheme("list-add"))
        add_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_btn.clicked.connect(self._pref_model.add_row)
        del_btn = QPushButton("Delete row")
        del_btn.setIcon(QIcon.fromTheme("list-remove"))
        del_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        del_btn.clicked.connect(self._delete_pref_rows)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(add_btn)
        outer_layout.addLayout(btn_layout)

        self.setLayout(outer_layout)
        self.deserialize({})

    def _delete_pref_rows(self):
        rows = sorted(
            {idx.row() for idx in self._pref_table.selectedIndexes()}, reverse=True
        )
        if rows:
            self._pref_model.remove_rows(rows)

    def _update_model(self):
        layer_name_selector_map = {
            "surface_map_layer_name": self._surface_map_layer,
            "pipe_layer_name": self._pipe_layer,
            "node_layer_name": self._node_layer,
        }
        layer_names = {
            name: selector.currentLayer().name()
            for name, selector in layer_name_selector_map.items()
            if selector.currentLayer() is not None
        }
        self.model = sm.SurfaceLinkingSettings(
            search_distance=self._search_distance.value(),
            sewer_type_preferences=self._pref_model.get_preferences(),
            selected_pipes_only=self._selected_pipes_only.isChecked(),
            **layer_names,
        )
        self.dataChanged.emit()

    @property
    def is_valid(self) -> bool:
        return True

    def get_settings(self) -> sm.SurfaceLinkingSettings:
        return self.model

    def deserialize(self, data):
        self.model = (
            sm.SurfaceLinkingSettings(**data) if data else sm.SurfaceLinkingSettings()
        )
        self._search_distance.setValue(self.model.search_distance)
        self._pref_model.set_preferences(self.model.sewer_type_preferences)
        self._selected_pipes_only.setChecked(self.model.selected_pipes_only)
        self._surface_map_layer.setCurrentText(self.model.surface_map_layer_name)
        self._pipe_layer.setCurrentText(self.model.pipe_layer_name)
        self._node_layer.setCurrentText(self.model.node_layer_name)
