from typing import Optional, Type

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

from threedi_schematisation_editor.vector_data_importer.settings_models import (
    get_field_map_config_for_model_class_field,
)
from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import (
    FieldMapRow,
    FieldMapWidget,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    FieldMapSettingsWidget,
    GenericSettingsWidget,
)


class SettingsPage(QWizardPage):
    def __init__(self, settings_widgets_classes: Optional[list[Type[QWidget]]] = None):
        super().__init__()
        self.setTitle("Import settings")
        self.settings_widgets = []
        if settings_widgets_classes:
            self.settings_widgets = [
                widget_class(parent=self) for widget_class in settings_widgets_classes
            ]
        self.setup_ui()

    def on_load_button_clicked(self):
        self.wizard().load_settings_from_json()

    def setup_ui(self):
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
        # add settings widgets
        for widget in self.settings_widgets:
            widget.dataChanged.connect(self.completeChanged)
            group_box = QGroupBox(widget.group_name)
            group_box.setLayout(widget.layout())
            layout.addWidget(group_box)
        self.setLayout(layout)

    def update_layer(self):
        layer = self.wizard().selected_layer
        for widget in self.settings_widgets:
            if isinstance(widget, FieldMapSettingsWidget):
                widget.update_layer(layer)

    @property
    def create_nodes(self):
        # Easy and safe access to the create nodes settings that is used to
        # determine if field map pages for nodes are shown
        for widget in self.settings_widgets:
            if isinstance(widget, ConnectionNodeSettingsWidget):
                return widget.create_nodes
        return False

    def serialize(self) -> dict:
        settings = {}
        for widget in self.settings_widgets:
            settings[widget.name] = widget.serialize()
        return settings

    def deserialize(self, data):
        """Load settings from serialized data"""
        settings_widget_map = {widget.name: widget for widget in self.settings_widgets}
        for name, settings in data.items():
            if name in settings_widget_map:
                settings_widget_map[name].deserialize(settings)

    def isComplete(self) -> bool:
        if not self.generic_settings.selected_layer:
            return False
        for widget in self.settings_widgets:
            if not widget.is_valid:
                return False
        return True


class FieldMapPage(QWizardPage):
    def __init__(self, model_cls, name):
        super().__init__()
        self.row_dict = self.create_rows(model_cls)
        self.setTitle(f"{model_cls.__tablename__}")
        self.setup_ui()
        self.name = name

    def create_rows(self, model_cls):
        row_dict = {}
        for field_name, display_name in model_cls.fields_display_names().items():
            config_class = get_field_map_config_for_model_class_field(
                field_name, model_cls
            )
            row_dict[field_name] = FieldMapRow(
                label=display_name, config=config_class.model_construct(method=None)
            )
        return row_dict

    def setup_ui(self):
        self.field_map_widget = FieldMapWidget(self.row_dict, parent=self)
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
