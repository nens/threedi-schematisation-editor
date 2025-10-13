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
)
from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
    DefaultValueDelegate,
    FieldMapDelegate,
    FieldMapModel,
    Row,
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
    # TODO: consider duplicate code for fieldmap!
    def __init__(self):
        super().__init__()
        # self.model = ConnectionNodeSettingsModel()
        self.setup_ui()

    def setup_ui(self):
        # # Table view for rows
        self.row_dict = {
            "structure_length": Row(label="Structure length"),
            "azimuth": Row(label="Structure direction (azimuth)"),
        }
        self.rows = list(self.row_dict.values())
        self.row_names = list(self.row_dict.keys())

        self.table_view = QTableView()
        self.table_model = FieldMapModel(self.row_dict)
        self.table_view.setModel(self.table_model)

        # Delegate for handling custom widget editing
        self.table_delegate = FieldMapDelegate()
        self.table_view.setItemDelegate(self.table_delegate)
        self.table_view.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.table_view.resizeColumnsToContents()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setVisible(False)

        default_value_delegate = DefaultValueDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(5, default_value_delegate)
        self.open_persistent_editors()
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Calculate the total height needed
        header_height = self.table_view.horizontalHeader().height()
        row_height = self.table_view.verticalHeader().defaultSectionSize()
        total_rows = len(self.rows)
        content_height = (row_height * total_rows) + header_height

        # Set fixed height and vertical size policy
        self.table_view.setMinimumHeight(content_height)
        self.table_view.setMaximumHeight(content_height)
        self.table_view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def open_persistent_editors(self):
        """Open persistent editors for columns with always-visible widgets"""
        for row in range(self.table_model.rowCount()):
            for col in [1, 2, 3, 4]:
                self.table_view.openPersistentEditor(self.table_model.index(row, col))

    def serialize(self):
        return {}

    def deserialize(self, data):
        pass


class IntegrationSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.model = IntegrationSettingsModel()
        self.setup_ui()
        self.integrate_on = None

    def update_integrate_on(self, value: Optional[str], checked: bool):
        # set integrate_on to specified value, but only if checked
        if checked:
            self.integrate_on = value

    def enable_integration_settings(self):
        if self.integrate_on:
            self.settings_container.setEnabled(True)
        else:
            self.settings_container.setEnabled(False)

    def setup_integration_mode_radio_buttons(self, group_box):
        # Create radio buttons
        use_channels = QRadioButton("Channels")
        use_pipes = QRadioButton("Pipes")
        no_integration = QRadioButton("None")
        # Add all buttons to group to simplify handling behavior
        button_group = QButtonGroup(self)
        button_group.addButton(use_channels)
        button_group.addButton(use_pipes)
        button_group.addButton(no_integration)
        # Explicitly link each radio button to updating the integrate_on settings
        use_channels.toggled.connect(
            lambda checked: self.update_integrate_on("channels", checked)
        )
        use_pipes.toggled.connect(
            lambda checked: self.update_integrate_on("pipes", checked)
        )
        no_integration.toggled.connect(
            lambda checked: self.update_integrate_on(None, checked)
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
        snap_distance = QDoubleSpinBox()
        min_length = QDoubleSpinBox()
        grid_layout.addWidget(snap_distance, 0, 1)
        grid_layout.addWidget(min_length, 1, 1)
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

    def save_settings_to_json(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Settings", str(Path.home()), "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, "r") as f:
                settings = json.load(f)
            # Get the wizard instance and its pages
            self.wizard().deserialize(settings)

    def serialize(self):
        return {}

    def deserialize(self, data):
        pass
