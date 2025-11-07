from typing import Optional, Type

from pydantic import BaseModel
from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor, QIcon, QPalette, QTextBlockFormat, QTextCharFormat
from qgis.PyQt.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTableView,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QWizardPage,
)

from threedi_schematisation_editor.vector_data_importer.settings_models import (
    get_field_map_config_for_model_class_field,
)
from threedi_schematisation_editor.vector_data_importer.wizard.field_map import (
    FieldMapRow,
    FieldMapWidget,
)
from threedi_schematisation_editor.vector_data_importer.wizard.settings_widgets import (
    ConnectionNodeSettingsWidget,
    FieldMapSettingsWidget,
    LayerSettingsWidget,
)


class StartPage(QWizardPage):
    def __init__(
        self,
        layer_filter=None,
    ):
        super().__init__()
        self.setTitle("Source layer")
        self.setup_ui(layer_filter)

    def setup_ui(self, layer_filter):
        self.layer_settings_widget = LayerSettingsWidget(layer_filter)
        self.layer_settings_widget.layer_changed.connect(self.completeChanged)
        layer_box = QGroupBox("Select layer to import")
        layer_box.setLayout(self.layer_settings_widget.layout())
        load_box = QGroupBox("Load import configuration from template (optional)")
        load_settings_button = QPushButton("Choose file...")
        load_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        load_settings_button.clicked.connect(self.on_load_button_clicked)
        self.loaded_status = QLabel("No import configuration loaded")
        layout = QVBoxLayout()
        layout.addWidget(load_settings_button)
        layout.addWidget(self.loaded_status)
        load_box.setLayout(layout)
        layout = QVBoxLayout(self)
        layout.addWidget(layer_box)
        layout.addWidget(load_box)

    def on_load_button_clicked(self):
        file_path = self.wizard().load_settings_from_json()
        if file_path:
            self.loaded_status.setText(f"Loaded import configuration from {file_path}")

    def isComplete(self) -> bool:
        return self.layer_settings_widget.selected_layer not in [None, ""]

    @property
    def selected_layer(self):
        return self.layer_settings_widget.selected_layer

    @property
    def use_selected_features(self):
        return self.layer_settings_widget.model.use_selected_features


class SettingsPage(QWizardPage):
    def __init__(
        self,
        settings_widgets_classes: Optional[list[Type[QWidget]]] = None,
    ):
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
        # add settings widgets
        for widget in self.settings_widgets:
            widget.dataChanged.connect(self.completeChanged)
            group_box = QGroupBox(widget.group_name)
            group_box.setLayout(widget.layout())
            layout.addWidget(group_box)
        self.setLayout(layout)

    def initializePage(self):
        # update layers just before showing
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
                return widget.model.create_nodes
        return False

    def get_settings(self) -> dict[str, BaseModel]:
        # return non-serialized settings
        return {widget.name: widget.get_settings() for widget in self.settings_widgets}

    def deserialize(self, data):
        """Load settings from serialized data"""
        settings_widget_map = {
            widget.model.name: widget for widget in self.settings_widgets
        }
        for name, settings in data.items():
            if name in settings_widget_map:
                settings_widget_map[name].deserialize(settings)

    def isComplete(self) -> bool:
        for widget in self.settings_widgets:
            if not widget.is_valid:
                return False
        return True


class FieldMapPage(QWizardPage):
    def __init__(self, model_cls, name):
        super().__init__()
        self.row_dict = self.create_rows(model_cls)
        self.layer_name = model_cls.__layername__.lower()
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
        self.setTitle(
            f"Map {self.wizard().selected_layer.name()} fields to {self.layer_name}s"
        )
        super().initializePage()

    def deserialize(self, data):
        return self.field_map_widget.deserialize(data[self.name])

    def isComplete(self) -> bool:
        return self.field_map_widget.is_valid

    def get_settings(self) -> dict[str, dict[str, BaseModel]]:
        # return non-serialized settings
        return {self.name: self.field_map_widget.get_settings()}


class RunPage(QWizardPage):
    cancel_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setTitle("Run")
        self.setup_ui()

    def on_save_button_clicked(self):
        file_path = self.wizard().save_settings_to_json()
        if file_path:
            self.saved_status.setText(f"Saved import configuration to {file_path}")

    def setup_ui(self):
        # Progress bar and cancel button
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("import feature %v of %m")
        self.cancel_button = QPushButton("Cancel import")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.on_cancel)
        run_layout = QHBoxLayout()
        run_layout.addWidget(self.progress_bar)
        run_layout.addWidget(self.cancel_button)

        # Logging
        self.log = LogPanel()

        # Save to template
        save_settings_button = QPushButton("Choose file...")
        save_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        save_settings_button.clicked.connect(self.on_save_button_clicked)
        self.saved_status = QLabel("Import configuration not saved")
        save_box = QGroupBox("Save import configuration to template (optional)")
        layout = QVBoxLayout()
        layout.addWidget(save_settings_button)
        layout.addWidget(self.saved_status)
        save_box.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(run_layout)
        main_layout.addWidget(self.log)
        main_layout.addWidget(save_box)
        self.setLayout(main_layout)

    def update_log(self, msg: str, fg_color: Optional[str] = None):
        if msg in [None, ""]:
            return
        format = QTextCharFormat()
        cursor = self.log.text.textCursor()
        if fg_color:
            format.setForeground(QColor(fg_color))
        cursor.insertText(msg + "\n", format)
        self.log.text.ensureCursorVisible()

    def on_cancel(self):
        QgsMessageLog.logMessage("Cancel requested", "DEBUG", Qgis.Info)
        self.cancel_requested.emit()
        self.cancel_button.setEnabled(False)


class LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # --- Text area ---
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        palette = self.palette()
        palette.setColor(QPalette.Base, QColor("white"))
        palette.setColor(QPalette.Text, QColor("black"))
        self.setPalette(palette)

        # --- Buttons ---
        copy_button = QToolButton()
        copy_button.setIcon(QIcon.fromTheme("edit-copy"))
        copy_button.setToolTip("Copy log to clipboard")
        copy_button.clicked.connect(self.copy_log)

        save_button = QToolButton()
        save_button.setIcon(QIcon.fromTheme("document-save"))
        save_button.setToolTip("Save log to file")
        save_button.clicked.connect(self.save_log)

        clear_button = QToolButton()
        clear_button.setIcon(QIcon.fromTheme("edit-clear"))
        clear_button.setToolTip("Clear log")
        clear_button.clicked.connect(self.text.clear)

        # --- Layout ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    # --- Slots ---
    def copy_log(self) -> None:
        self.text.selectAll()
        self.text.copy()

    def save_log(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Log", "log.txt", "Text Files (*.txt)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.text.toPlainText())
