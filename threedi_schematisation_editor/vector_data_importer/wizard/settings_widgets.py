from typing import Optional

from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtCore import pyqtSignal
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

from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ConnectionNodeSettingsModel,
    IntegrationMode,
    IntegrationSettingsModel,
)
from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
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

    def serialize(self):
        return self.model


class ConnectionNodeSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = ConnectionNodeSettingsModel()
        self.setup_ui()

    def setup_ui(self):
        # Create widgets
        self.create_nodes = QCheckBox("Create new connection nodes if needed")
        self.snap = QCheckBox("Snap to existing connection nodes within: ")
        self.snap.setEnabled(False)
        self.snap_distance = QDoubleSpinBox()
        self.snap_distance.setRange(0, 100)
        self.snap_distance.setSuffix(" m")
        self.snap_distance.setDecimals(1)
        self.snap_distance.setEnabled(False)

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


class PointToLIneConversionSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        # TODO replace row dict with actual model ?
        self.row_dict = {
            "structure_length": FieldMapRow(label="Structure length"),
            "azimuth": FieldMapRow(label="Structure direction (azimuth)"),
        }
        self.setup_ui()

    def setup_ui(self):
        self.field_map_widget = FieldMapWidget(self.row_dict)
        self.table_view = self.field_map_widget.table_view
        self.table_model = self.field_map_widget.table_model
        self.table_delegate = self.field_map_widget.table_delegate
        layout = QVBoxLayout(self)
        layout.addWidget(self.field_map_widget)
        self.field_map_widget.open_persistent_editors()

    def update_layer(self, layer):
        self.field_map_widget.update_layer(layer)

    def serialize(self):
        return self.field_map_widget.serialize()

    def deserialize(self, data):
        self.field_map_widget.deserialize(data)


class IntegrationSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.model = IntegrationSettingsModel()
        self.setup_ui()

    def update_integrate_on(self, checked: bool):
        # set integrate_on to specified value, but only if checked
        for integration_mode, radio_button in self.integration_mode_map.items():
            if radio_button.isChecked():
                self.model.integration_mode = integration_mode
                break

    def enable_integration_settings(self):
        if self.model.integration_mode == IntegrationMode.NONE:
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
            IntegrationMode.NONE: no_integration,
            IntegrationMode.CHANNELS: use_channels,
            IntegrationMode.PIPES: use_pipes,
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
        self.min_length = QDoubleSpinBox()
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
