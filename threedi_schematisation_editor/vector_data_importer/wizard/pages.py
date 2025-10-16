from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTableView,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QWizardPage,
)
from qgis.core import Qgis, QgsMessageLog

from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
    FieldMapRow,
    FieldMapWidget,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    GenericSettingsWidget,
    IntegrationSettingsWidget,
    PointToLIneConversionSettingsWidget,
)


class SettingsPage(QWizardPage):
    def __init__(
        self,
        add_connection_node_settings: bool = False,
        add_point_to_line_settings: bool = False,
        add_integration_settings: bool = False,
    ):
        super().__init__()
        self.setTitle("Import settings")
        self.connection_node_settings: Optional[QWidget] = None
        self.point_to_line_conversion_settings: Optional[QWidget] = None
        self.integration_settings: Optional[QWidget] = None
        self.setup_ui(
            add_connection_node_settings,
            add_point_to_line_settings,
            add_integration_settings,
        )

    def on_load_button_clicked(self):
        self.wizard().load_settings_from_json()

    def setup_ui(
        self,
        add_connection_node_settings: bool,
        add_point_to_line_conversion_settings: bool,
        add_integration_settings: bool,
    ):
        layout = QVBoxLayout(self)

        # Top row
        self.generic_settings = GenericSettingsWidget()
        self.generic_settings.layer_changed.connect(self.update_layer)
        self.generic_settings.layer_changed.connect(self.completeChanged)
        load_settings_button = QPushButton("Load settings")
        load_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        load_settings_button.clicked.connect(self.on_load_button_clicked)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.generic_settings)
        top_layout.addWidget(load_settings_button)
        layout.addLayout(top_layout)

        # specific settings widgets
        if add_connection_node_settings:
            self.connection_node_settings = ConnectionNodeSettingsWidget()
            group_box = QGroupBox("Connection node settings")
            group_box.setLayout(self.connection_node_settings.layout())
            layout.addWidget(group_box)

        if add_point_to_line_conversion_settings:
            self.point_to_line_conversion_settings = (
                PointToLIneConversionSettingsWidget()
            )
            group_box = QGroupBox("Point to line conversion settings")
            group_box.setLayout(self.point_to_line_conversion_settings.layout())
            layout.addWidget(group_box)
            # connect data changed to isComplete status of the page
            self.point_to_line_conversion_settings.dataChanged.connect(
                self.completeChanged
            )
        if add_integration_settings:
            self.integration_settings = IntegrationSettingsWidget()
            group_box = QGroupBox("Integration settings")
            group_box.setLayout(self.integration_settings.layout())
            layout.addWidget(group_box)
        self.setLayout(layout)

    def update_layer(self):
        layer = self.wizard().selected_layer
        if self.point_to_line_conversion_settings:
            self.point_to_line_conversion_settings.update_layer(layer)

    @property
    def create_nodes(self):
        # Easy and safe access to the create nodes settings that is used to
        # determine if field map pages for nodes are shown
        if self.connection_node_settings:
            return self.connection_node_settings.create_nodes
        return False

    def serialize(self) -> dict:
        settings = {}
        if self.connection_node_settings:
            settings["connection_nodes"] = self.connection_node_settings.serialize()
        if self.point_to_line_conversion_settings:
            settings["point_to_line_conversion"] = (
                self.point_to_line_conversion_settings.serialize()
            )
        if self.integration_settings:
            settings["integration"] = self.integration_settings.serialize()
        return settings

    def deserialize(self, data):
        """Load settings from serialized data"""
        if "connection_nodes" in data and self.connection_node_settings:
            self.connection_node_settings.deserialize(data["connection"])
        if (
            "point_to_line_conversion" in data
            and self.point_to_line_conversion_settings
        ):
            self.point_to_line_conversion_settings.deserialize(
                data["point_to_line_conversion"]
            )
        if "integration" in data and self.integration_settings:
            self.integration_settings.deserialize(data["integration"])

    def isComplete(self) -> bool:
        if not self.generic_settings.selected_layer:
            return False
        elif self.point_to_line_conversion_settings:
            if not self.point_to_line_conversion_settings.is_valid:
                return False
        return True


class FieldMapPage(QWizardPage):
    def __init__(self, model_cls, name):
        super().__init__()
        self.row_dict = {
            field_name: FieldMapRow(label=display_name)
            for field_name, display_name in model_cls.fields_display_names().items()
        }
        self.setTitle(f"{model_cls.__tablename__}")
        self.setup_ui()
        self.name = name

    def setup_ui(self):
        self.field_map_widget = FieldMapWidget(self.row_dict)
        # connect data changed to isComplete status of the page
        self.field_map_widget.dataChanged.connect(self.completeChanged)
        layout = QVBoxLayout(self)
        layout.addWidget(self.field_map_widget)

    def initializePage(self):
        layer = self.wizard().selected_layer
        if layer:
            self.field_map_widget.update_layer(layer)
        super().initializePage()

    def serialize(self):
        return {self.name: self.field_map_widget.serialize()}

    def deserialize(self, data):
        return self.field_map_widget.deserialize(data[self.name])

    def isComplete(self) -> bool:
        return self.field_map_widget.is_valid


class RunPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Run")
        self.setup_ui()

    def on_save_button_clicked(self):
        self.wizard().save_settings_to_json()

    def setup_ui(self):
        run_button = QPushButton("Run")
        run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        progress_bar = QProgressBar()
        save_settings_button = QPushButton("Save template")
        save_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        save_settings_button.clicked.connect(self.on_save_button_clicked)
        text = QTextBrowser()
        text.setReadOnly(True)
        text.currentFont().setPointSize(10)
        text.setText("foo bar")
        layout = QHBoxLayout()
        layout.addWidget(run_button)
        layout.addWidget(progress_bar)
        layout.addWidget(save_settings_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(text)
        self.setLayout(main_layout)
