from typing import Optional, Type

from pydantic import BaseModel
from qgis.core import (
    QgsApplication,
    QgsMapLayerProxyModel,
    QgsProject,
    QgsWkbTypes,
)
from qgis.gui import QgsMapLayerComboBox
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
    QPushButton,
    QSizePolicy,
    QStyle,
    QTableView,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QWizardPage,
)
from threedi_mi_utils.ui import ColoredProgressBar

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    create_field_map_config,
    get_field_map_config_for_model_class_field,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
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

    def get_settings(self) -> dict:
        return {"source": self.layer_settings_widget.get_settings()}

    def deserialize(self, data):
        source_data = data.get("source", {})
        if source_data:
            self.layer_settings_widget.deserialize(source_data)

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
            widget.group_box = group_box
            expanding = getattr(widget, "expanding", False)
            stretch = 1 if expanding else 0
            if not expanding:
                group_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            layout.addWidget(group_box, stretch)
        layout.addStretch()
        self.setLayout(layout)

    def initializePage(self):
        # update layers and visibility just before showing
        layer = self.wizard().selected_layer
        for widget in self.settings_widgets:
            if hasattr(widget, "update_layer"):
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
        # return non-serialized settings, skipping hidden widgets
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

    def validatePage(self) -> bool:
        """Warn (but don't block) when no sewerage type mappings are configured."""
        for widget in self.settings_widgets:
            if not widget.validate():
                return False
        return True


class FieldMapPage(QWizardPage):
    def __init__(self, model_cls, name, title_suffix=None, restrict_id_to_auto=False):
        super().__init__()
        self.restrict_id_to_auto = restrict_id_to_auto
        self.row_dict = self.create_rows(model_cls)
        self.title_suffix = (
            title_suffix
            if title_suffix
            else (model_cls.__layername__.lower() + "s" if model_cls else "")
        )
        self.setup_ui()
        self.name = name

    def create_rows(self, model_cls):
        if model_cls is None:
            return {}
        row_dict = {}
        for field_name, display_name in model_cls.fields_display_names().items():
            config_class = get_field_map_config_for_model_class_field(
                field_name, model_cls
            )
            if self.restrict_id_to_auto and field_name == "id":
                config_class = create_field_map_config(
                    [ColumnImportMethod.AUTO], field_type=int
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
        if layer and self.title_suffix:
            self.setTitle(f"Map {layer.name()} fields to {self.title_suffix}")
        super().initializePage()

    def rebuild(self, model_cls):
        """Replace field map rows for a new target model class."""
        self.title_suffix = model_cls.__layername__.lower() + "s" if model_cls else ""
        self.row_dict = self.create_rows(model_cls)
        self.field_map_widget.set_rows(self.row_dict)
        self.completeChanged.emit()

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
        self.progress_bar = ColoredProgressBar()
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
        self.save_settings_button = QPushButton("Save as...")
        self.save_settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.save_settings_button.clicked.connect(self.on_save_button_clicked)
        self.saved_status = QLabel("Import configuration not saved")
        save_box = QGroupBox("Save import configuration to template (optional)")
        layout = QVBoxLayout()
        layout.addWidget(self.save_settings_button)
        layout.addWidget(self.saved_status)
        save_box.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(run_layout)
        main_layout.addWidget(self.log)
        main_layout.addWidget(save_box)
        self.setLayout(main_layout)

    def on_run_start(self):
        self.cancel_button.setEnabled(True)
        self.progress_bar.reset()
        self.save_settings_button.setEnabled(False)
        self.clear_log()

    def on_run_finish(self):
        self.cancel_button.setEnabled(False)
        self.save_settings_button.setEnabled(True)

    def update_log(self, msg: str, fg_color: Optional[str] = None):
        if msg in [None, ""]:
            return
        format = QTextCharFormat()
        cursor = self.log.text.textCursor()
        if fg_color:
            format.setForeground(QColor(fg_color))
        cursor.insertText(msg + "\n", format)
        self.log.text.ensureCursorVisible()

    def clear_log(self):
        self.log.text.clear()

    def on_cancel(self):
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

        # --- Copy Button ---
        copy_button = QToolButton(self.text)
        copy_button.setIcon(QgsApplication.getThemeIcon("mActionEditCopy.svg"))
        copy_button.setToolTip("Copy log to clipboard")
        copy_button.clicked.connect(self.copy_log)

        # Make button background transparent
        copy_button.setStyleSheet(
            "QToolButton { background: transparent; border: none; }"
        )

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)

        # Position the copy button in the top-right corner of the text area
        def updateButtonPosition():
            margin = 5  # pixels from the edge
            copy_button.move(self.text.width() - copy_button.width() - margin, margin)

        # Update button position when text area is resized
        self.text.resizeEvent = lambda e: updateButtonPosition()
        updateButtonPosition()

    # --- Slots ---
    def copy_log(self) -> None:
        self.text.selectAll()
        self.text.copy()


QGIS_GEOMTYPE_TO_PROXY_FILTER = {
    QgsWkbTypes.GeometryType.PointGeometry: QgsMapLayerProxyModel.PointLayer,
    QgsWkbTypes.GeometryType.LineGeometry: QgsMapLayerProxyModel.LineLayer,
    QgsWkbTypes.GeometryType.PolygonGeometry: QgsMapLayerProxyModel.PolygonLayer,
    QgsWkbTypes.GeometryType.NullGeometry: QgsMapLayerProxyModel.NoGeometry,
}


class GenericStartPage(QWizardPage):
    """Start page for the generic importer wizard.

    Contains a target layer selector (schematisation layers only) and a source
    layer selector (any layer, filtered to matching geometry type once a target
    is selected). The two selectors cross-filter each other.
    """

    target_layer_changed = pyqtSignal(object)  # emits model_cls or None
    layer_changed = pyqtSignal()

    def __init__(self, model_gpkg):
        super().__init__()
        self.setTitle("Source and target layer")
        self._model_gpkg = model_gpkg
        self._target_model_cls = None
        self.setup_ui()

    def setup_ui(self):
        # --- Target selector ---
        self.target_selector = QgsMapLayerComboBox()
        self.target_selector.setAllowEmptyLayer(True)
        self.target_selector.setFilters(QgsMapLayerProxyModel.VectorLayer)
        excepted = [
            layer
            for layer in QgsProject.instance().mapLayers().values()
            if self._model_gpkg not in layer.source()
        ]
        self.target_selector.setExceptedLayerList(excepted)
        # Start with the empty layer selected (index 0 is the empty row).
        self.target_selector.setCurrentIndex(0)
        self.target_selector.layerChanged.connect(self.on_target_changed)

        target_box = QGroupBox("Target layer (schematisation)")
        target_layout = QVBoxLayout()
        target_layout.addWidget(self.target_selector)
        target_box.setLayout(target_layout)

        # --- Source selector ---
        self.source_widget = LayerSettingsWidget(layer_filter=None)
        self.source_widget.layer_changed.connect(self.on_source_changed)

        source_box = QGroupBox("Source layer to import")
        source_box.setLayout(self.source_widget.layout())

        layout = QVBoxLayout(self)
        layout.addWidget(target_box)
        layout.addWidget(source_box)

    def on_target_changed(self, layer):
        """Update source filter and emit target_layer_changed."""
        if layer is None:
            self._target_model_cls = None
            self.source_widget.layer_selector.setFilters(
                QgsMapLayerProxyModel.VectorLayer
            )
        else:
            source = layer.source()
            table_name = (
                source.split("|layername=")[1] if "|layername=" in source else ""
            )
            self._target_model_cls = dm.TABLENAME_TO_MODEL_CLS.get(table_name)
            geom_type = layer.geometryType()
            proxy_filter = QGIS_GEOMTYPE_TO_PROXY_FILTER.get(geom_type)
            if proxy_filter is None or proxy_filter == QgsMapLayerProxyModel.NoGeometry:
                # non-spatial target: any source allowed
                self.source_widget.layer_selector.setFilters(
                    QgsMapLayerProxyModel.VectorLayer
                )
            else:
                self.source_widget.layer_selector.setFilters(proxy_filter)
        self.target_layer_changed.emit(self._target_model_cls)
        self.layer_changed.emit()
        self.completeChanged.emit()

    def on_source_changed(self, layer_name):
        """Update target filter based on selected source geometry type."""
        source_layer = self.source_widget.selected_layer
        if source_layer is None:
            self.target_selector.setFilters(QgsMapLayerProxyModel.VectorLayer)
        else:
            geom_type = source_layer.geometryType()
            proxy_filter = QGIS_GEOMTYPE_TO_PROXY_FILTER.get(
                geom_type, QgsMapLayerProxyModel.VectorLayer
            )
            # Always include non-spatial targets
            self.target_selector.setFilters(
                proxy_filter | QgsMapLayerProxyModel.NoGeometry
            )
        self.layer_changed.emit()
        self.completeChanged.emit()

    @property
    def target_model_cls(self):
        return self._target_model_cls

    @property
    def selected_layer(self):
        return self.source_widget.selected_layer

    @property
    def use_selected_features(self):
        return self.source_widget.model.use_selected_features

    def isComplete(self):
        return self._target_model_cls is not None and self.selected_layer is not None

    def get_settings(self):
        return {"source": self.source_widget.get_settings()}

    def deserialize(self, data):
        # Restore target layer first so field_map_page.rebuild fires before
        # FieldMapPage.deserialize runs on the next page.
        target_layer_name = data.get("target_layer_name")
        if target_layer_name:
            from qgis.core import QgsProject

            layers = QgsProject.instance().mapLayersByName(target_layer_name)
            if layers:
                self.target_selector.setLayer(layers[0])
        source_data = data.get("source", {})
        if source_data:
            self.source_widget.deserialize(source_data)

    def get_settings_with_target(self):
        """Extended settings including target layer name for draft persistence."""
        settings = self.get_settings()
        if self._target_model_cls:
            settings["target_layer_name"] = self._target_model_cls.__tablename__
        return settings
