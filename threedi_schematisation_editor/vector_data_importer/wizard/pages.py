import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFileDialog,
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
    QWizardPage,
)
from qgis.core import Qgis, QgsMessageLog

from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
    DefaultValueDelegate,
    FieldMapDelegate,
    FieldMapModel,
    Row,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettings,
    GenericSettings,
    IntegrationSettings,
    PointToLIneConversionSettings,
)


class SettingsPage(QWizardPage):
    def __init__(
        self,
        connection_node_settings: bool = False,
        point_to_line_conversion: bool = False,
        integration_settings: bool = False,
    ):
        super().__init__()
        self.setTitle("Import settings")
        self.connection_node_settings = None
        self.setup_ui(
            connection_node_settings, point_to_line_conversion, integration_settings
        )

    def setup_ui(
        self,
        connection_node_settings: bool,
        point_to_line_conversion: bool,
        integration_settings: bool,
    ):
        layout = QVBoxLayout(self)

        # Top row
        self.generic_settings = GenericSettings()
        self.generic_settings.layer_changed.connect(self.completeChanged)
        load_settings_button = QPushButton("Load settings")
        load_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        load_settings_button.clicked.connect(self.load_settings_from_json)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.generic_settings)
        top_layout.addWidget(load_settings_button)
        layout.addLayout(top_layout)

        # specific settings widgets
        if connection_node_settings:
            self.connection_node_settings = ConnectionNodeSettings()
            group_box = QGroupBox("Connection node settings")
            group_box.setLayout(self.connection_node_settings.layout())
            layout.addWidget(group_box)

        if point_to_line_conversion:
            self.point_to_line_conversion_settings = PointToLIneConversionSettings()
            group_box = QGroupBox("Point to line conversion settings")
            group_box.setLayout(self.point_to_line_conversion_settings.layout())
            layout.addWidget(group_box)

        if integration_settings:
            self.integration_settings = IntegrationSettings()
            group_box = QGroupBox("Integration settings")
            group_box.setLayout(self.integration_settings.layout())
            layout.addWidget(group_box)
        self.setLayout(layout)

    def update_layer(self):
        # fieldmap pages
        pass

    @property
    def create_nodes(self):
        # Easy and safe access to the create nodes settings that is used to
        # determine if field map pages for nodes are shown
        if self.connection_node_settings:
            return self.connection_node_settings.create_nodes
        return False

    def get_all_settings(self) -> dict:
        settings = {}
        if self.connection_node_settings:
            settings["connection_nodes"] = self.connection_node_settings.serialize()
        return settings

    def load_settings_from_json(self):
        # TODO fix for current wizard and move logic to wizard
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Settings", str(Path.home()), "JSON Files (*.json)"
        )
        if file_path:
            with open(file_path, "r") as f:
                settings = json.load(f)
            # Get the wizard instance and its pages
            wizard = self.wizard()
            settings_page = wizard.page(0)  # SettingsPage
            field_map_page = wizard.page(1)  # FieldMapPage
            try:
                # Load settings for each page
                if "page1" in settings:
                    settings_page.deserialize(settings["page1"])
                if "page2" in settings:
                    field_map_page.deserialize(settings["page2"])

                QMessageBox.information(
                    self, "Success", "Settings loaded successfully!"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Failed to load settings: {str(e)}"
                )

    def deserialize(self, data):
        """Load settings from serialized data"""
        if "connection" in data:
            self.connection_node_settings.deserialize(data["connection"])

    def isComplete(self) -> bool:
        # Return True only if a layer is selected
        return bool(self.generic_settings.selected_layer)


class FieldMapPage(QWizardPage):
    def __init__(self, model_cls):
        super().__init__()
        self.row_dict = {
            field_name: Row(label=display_name)
            for field_name, display_name in model_cls.fields_display_names().items()
        }
        self.rows = list(self.row_dict.values())
        self.row_names = list(self.row_dict.keys())
        self.setTitle(f"{model_cls.__tablename__}")
        self.setup_ui()

    def setup_ui(self):
        # Table view for rows
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

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)

    def initializePage(self):
        layer = self.wizard().selected_layer
        if layer:
            self.table_model.current_layer_attributes = [
                field.name() for field in layer.fields()
            ]
        # Open persistent editors initially (before layer selection)
        self.open_persistent_editors()
        # Set initial widget states (all disabled since no layer is selected)
        self.update_widget_states()
        super().initializePage()

    def open_persistent_editors(self):
        """Open persistent editors for columns with always-visible widgets"""
        for row in range(self.table_model.rowCount()):
            for col in [1, 2, 3, 4]:
                self.table_view.openPersistentEditor(self.table_model.index(row, col))

    def update_widget_states(self):
        """Update the enabled/disabled state of all persistent editor widgets"""
        for row in range(self.table_model.rowCount()):
            QgsMessageLog.logMessage(f"{row=}", "DEBUG", Qgis.Warning)
            for col in [1, 2, 3, 4]:  # Columns with persistent editors
                index = self.table_model.index(row, col)
                editor = self.table_view.indexWidget(index)
                if editor:
                    editor.setEnabled(True)
                    row_obj = self.rows[row]
                    if col == 1:  # Method column - enabled only when layer is selected
                        QgsMessageLog.logMessage(
                            f"column 1: set enabled", "DEBUG", Qgis.Warning
                        )
                        editor.setEnabled(True)
                    elif row_obj.method:
                        QgsMessageLog.logMessage(
                            f"column {col}, set enabled", "DEBUG", Qgis.Warning
                        )
                        editor.setEnabled(row_obj.is_editable(col))
                    else:
                        QgsMessageLog.logMessage(
                            f"other {col}, set disabled", "DEBUG", Qgis.Warning
                        )
                        editor.setEnabled(False)

    def serialize(self):
        {}

    def deserialize(self, data):
        return {}


class RunPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Run")
        self.setup_ui()

    def setup_ui(self):
        run_button = QPushButton("Run")
        run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        progress_bar = QProgressBar()
        save_settings_button = QPushButton("Save template")
        save_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
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
