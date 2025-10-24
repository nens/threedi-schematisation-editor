from dataclasses import fields
from typing import Optional, Type

from pydantic import BaseModel
from qgis.core import Qgis, QgsMessageLog
from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
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
    QRadioButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
    FieldMapColumn,
    FieldMapRow,
    FieldMapWidget,
)
from threedi_schematisation_editor.vector_data_importer.wizard.models import (
    GenericSettingsModel,
)


class GenericSettingsWidget(QWidget):
    layer_changed = pyqtSignal(str)  # Add this signal

    def __init__(self):
        super().__init__()
        self.model = GenericSettingsModel()
        self.setup_ui()
        self.selected_layer = None

    def setup_ui(self):
        # create widgets
        label = QLabel("Select layer to import:")
        layer_selector = QgsMapLayerComboBox()
        layer_selector.setAllowEmptyLayer(True)
        layer_selector.layerChanged.connect(self.update_layer)
        layer_selector.setCurrentIndex(0)
        layer_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # TODO: remove this, was added for debugging
        self.layer_selector = layer_selector
        use_selected = QCheckBox("Only use selected features")
        # set up layout
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(layer_selector)
        layout.addWidget(use_selected)
        # Connect widgets to model updates
        use_selected.toggled.connect(self.update_use_selected)

    def update_layer(self, layer):
        if layer:
            self.selected_layer = layer
            self.model.selected_layer = layer.name()
            self.layer_changed.emit(layer.name())  # Emit with layer name
        else:
            self.selected_layer = None
            self.model.selected_layer = ""
            self.layer_changed.emit("")

    def update_use_selected(self, checked):
        self.model.use_selected_features = checked

    def get_importer(self, import_settings: dict, layer_dict):
        return self.IMPORTERS[self.import_model_cls](
            self.source_layer,
            self.model_gpkg,
            import_settings,
            **layer_dict,
        )

    def serialize(self):
        return self.model


class SettingsWidget(QWidget):
    dataChanged = pyqtSignal()
    model = None

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def group_name(self) -> str:
        raise NotImplementedError

    @property
    def is_valid(self) -> bool:
        return True

    def get_settings(self) -> BaseModel:
        # loudly fail when model is missing
        assert self.model is not None
        return self.model


class ConnectionNodeSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.ConnectionNodeSettingsModel()
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
        self.snap.setEnabled(False)
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setSuffix(" m")
        self.snap_distance.setDecimals(1)
        self.snap_distance.setEnabled(False)
        self.snap_distance.setMinimum(sm.get_field_min(self.model, "snap_distance"))
        self.snap_distance.setMaximum(sm.get_field_max(self.model, "snap_distance"))

        # Connect widgets to model updates
        self.create_nodes.toggled.connect(self.update_create_nodes)
        self.create_nodes.toggled.connect(self.on_create_nodes_toggled)
        self.snap.toggled.connect(self.update_snap_enabled)
        self.snap.toggled.connect(self.on_snap_toggled)
        self.snap_distance.valueChanged.connect(self.update_snap_distance)

        # Add widgets to layout
        layout = QVBoxLayout()
        layout.addWidget(self.create_nodes)
        layout.addWidget(self.snap)
        layout.addWidget(self.snap_distance)
        self.setLayout(layout)
        # set all widgets to default values
        self.deserialize({})

    def on_create_nodes_toggled(self, checked):
        self.snap.setEnabled(checked)

    def on_snap_toggled(self, checked):
        self.snap_distance.setEnabled(checked)

    def update_create_nodes(self, checked):
        self.model.create_nodes = checked

    def update_snap_enabled(self, checked):
        self.model.snap = checked

    def update_snap_distance(self, value):
        self.model.snap_distance = value

    def serialize(self):
        return self.model.model_dump()

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.create_nodes.setChecked(self.model.create_nodes)
        self.snap.setChecked(self.model.snap)
        self.snap_distance.setValue(self.model.snap_distance)


class IntegrationSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.IntegrationSettingsModel()
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
        # TODO: update labels on settings
        grid_layout.addWidget(QLabel("Snap to channel/pipe withing"), 0, 0)
        grid_layout.addWidget(
            QLabel("Minimum length of a channel/pipe after edit"), 1, 0
        )
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setMinimum(sm.get_field_min(self.model, "snap_distance"))
        self.snap_distance.setMaximum(sm.get_field_max(self.model, "snap_distance"))
        self.min_length = QDoubleSpinBox()
        self.min_length.setMinimum(sm.get_field_min(self.model, "min_length"))
        self.min_length.setMaximum(sm.get_field_max(self.model, "min_length"))
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

    def serialize(self):
        return self.model.model_dump()

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.integration_mode_map[self.model.integration_mode].setChecked(True)
        self.snap_distance.setValue(self.model.snap_distance)
        self.min_length.setValue(self.model.min_length)


class CrossSectionDataRemapSettingsWidget(SettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.CrossSectionDataRemapModel()
        self.setup_ui()

    @property
    def name(self):
        return "cross_section_data_remap"

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

    def update_set_lowest_point_to_zero(self, checked):
        self.model.set_lowest_point_to_zero = checked

    def update_use_lowest_point_as_reference(self, checked):
        self.model.use_lowest_point_as_reference = checked

    def serialize(self):
        return self.model.model_dump()

    def deserialize(self, data):
        self.model = self.model.model_copy(update=data)
        self.set_lowest_point_to_zero.setChecked(self.model.set_lowest_point_to_zero)
        self.use_lowest_point_as_reference.setChecked(
            self.model.use_lowest_point_as_reference
        )


class FieldMapSettingsWidget(SettingsWidget):
    model_cls: Optional[sm.FieldConfigDataModel] = None

    def create_row_dict(self) -> dict[str, FieldMapRow]:
        row_dict = {}
        if not self.model_cls:
            return row_dict
        # iterate over fields of model (dataclass)
        for field in fields(self.model_cls):
            # create a FieldMapConfig using metadata from model_cls
            config_class = sm.get_field_map_config_for_model_class_field(
                field.name, self.model_cls
            )
            # create FieldMapRow to use in the FieldMapTable
            row_dict[field.name] = FieldMapRow(
                label=field.name,
                config=config_class.model_construct(
                    method=None, default_value=field.default
                ),
            )
        return row_dict

    def setup_ui(self, row_dict):
        self.field_map_widget = FieldMapWidget(row_dict)
        # emit dataChanged signal when field map widget data changes
        self.field_map_widget.dataChanged.connect(self.dataChanged.emit)
        self.table_view = self.field_map_widget.table_view
        self.table_model = self.field_map_widget.table_model
        self.table_delegate = self.field_map_widget.table_delegate
        layout = QVBoxLayout(self)
        layout.addWidget(self.field_map_widget)
        self.field_map_widget.open_persistent_editors()

    def _on_data_changed(self, top_left, bottom_right, roles):
        self.dataChanged.emit()

    def update_layer(self, layer):
        self.field_map_widget.update_layer(layer)

    def serialize(self):
        return self.field_map_widget.serialize()

    def deserialize(self, data):
        self.field_map_widget.deserialize(data)

    @property
    def is_valid(self):
        return self.field_map_widget.is_valid

    def get_settings(self) -> BaseModel:
        if self.model_cls is not None:
            return self.model_cls.get_settings_model(
                self.field_map_widget.get_settings()
            )


class PointToLIneConversionSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model_cls = sm.PointToLineDataModel
        row_dict = self.create_row_dict()
        row_dict["length"].label = "Structure length"
        row_dict["azimuth"].label = "Sturcture direction (azimuth)"
        self.setup_ui(row_dict)

    @property
    def name(self):
        return "point_to_line_conversion"

    @property
    def group_name(self):
        return "Point to line conversion settings"


class CrossSectionLocationMappingSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model_cls = sm.CrossSectionLocationMappingModel
        row_dict = self.create_row_dict()
        row_dict["join_field_src"].label = "Join channel source field"
        row_dict["join_field_tgt"].label = "Join channel target field"
        self.setup_ui(row_dict)

    @property
    def name(self):
        return "cross_section_location_mapping"

    @property
    def group_name(self):
        # TODO: better name
        return "Mapping"

    def get_settings(self) -> BaseModel:
        return
        # sm.get_cross_section_settings_model(self.field_map_widget.get_settings())

    def _sync_auto_methods(self, top_left, bottom_right, roles):
        if not roles or Qt.EditRole in roles:
            row_idx = top_left.row()
            other_row_idx = 0 if top_left.row() == 1 else 1
            method_column = FieldMapColumn.to_index(FieldMapColumn.METHOD)
            method = self.table_model.data(
                self.table_model.index(row_idx, method_column), Qt.EditRole
            )
            other_method = self.table_model.data(
                self.table_model.index(other_row_idx, method_column), Qt.EditRole
            )
            # check if this call was caused by changing the method to auto and if so set other method to auto
            if (
                method == ColumnImportMethod.AUTO
                and other_method != ColumnImportMethod.AUTO
            ):
                self.table_model.setData(
                    self.table_model.index(other_row_idx, method_column),
                    ColumnImportMethod.AUTO,
                    Qt.EditRole,
                )
