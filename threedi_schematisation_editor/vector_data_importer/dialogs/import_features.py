import json
import os
import traceback
from functools import cached_property, partial
from typing import Any, Dict, List, Optional, Tuple, Type

from qgis.core import (
    Qgis,
    QgsMapLayer,
    QgsMapLayerProxyModel,
    QgsMessageLog,
    QgsSettings,
)
from qgis.gui import QgsFieldComboBox, QgsFieldExpressionWidget, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import get_filepath, is_optional, optional_type
from threedi_schematisation_editor.vector_data_importer.dialogs.import_widgets import (
    CONFIG_HEADER,
    CONFIG_KEYS,
    create_widgets,
)
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import (
    CatchThreediWarnings,
    ColumnImportIndex,
    ImportFieldMappingUtils,
    JoinFieldsRow,
    create_font,
)
from threedi_schematisation_editor.vector_data_importer.importers import (
    ChannelsImporter,
    ConnectionNodesImporter,
    CrossSectionLocationImporter,
    CulvertsImporter,
    OrificesImporter,
    PipesImporter,
    WeirsImporter,
)
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


class ImportDialog(QDialog):
    """Base class for import dialogs that handles common functionality."""

    IMPORTERS = {
        dm.ConnectionNode: ConnectionNodesImporter,
        dm.Culvert: CulvertsImporter,
        dm.Orifice: OrificesImporter,
        dm.Weir: WeirsImporter,
        dm.Pipe: PipesImporter,
        dm.Channel: ChannelsImporter,
        dm.CrossSectionLocation: CrossSectionLocationImporter,
    }

    def __init__(
        self,
        import_model_cls: Type,
        model_gpkg: str,
        layer_manager: Any,
        uc: Any,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.import_model_cls = import_model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc

        # Create UI elements
        self.setup_ui()
        self.setup_models()
        self.set_source_layer_filter()
        self.create_conversion_settings_widget()
        self.connect_conversion_settings_widget()
        self.on_layer_changed(self.source_layer)
        self.setup_labels()

    def setup_ui(self):
        """Set up the UI elements common to all import dialogs."""
        # Set window properties
        self.setWindowTitle("Import {}s")
        self.resize(1000, 750)

        # Create main layout
        self.gridLayout = QGridLayout(self)

        # Create source layer label and combo box
        self.source_layer_label = QLabel("Source layer")
        self.source_layer_label.setFont(self.create_font(10))
        self.gridLayout.addWidget(self.source_layer_label, 0, 0)

        self.source_layer_cbo = QgsMapLayerComboBox()
        self.source_layer_cbo.setFont(self.create_font(10))
        self.source_layer_cbo.setAllowEmptyLayer(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.source_layer_cbo.setSizePolicy(sizePolicy)
        self.source_layer_cbo.setCurrentIndex(0)
        self.source_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.gridLayout.addWidget(self.source_layer_cbo, 0, 1)

        # Create save button
        self.save_pb = QPushButton("Save as template...")
        self.save_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.save_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.save_pb, 0, 4, 1, 2)
        self.save_pb.clicked.connect(self.save_import_settings)

        # Create load button
        self.load_pb = QPushButton("Load template...")
        self.load_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.load_pb, 1, 4, 1, 2)
        self.load_pb.clicked.connect(self.load_import_settings)

        # Create selected features checkbox
        self.selected_only_cb = QCheckBox("Selected features only")
        self.selected_only_cb.setFont(self.create_font(10))
        self.selected_only_cb.setLayoutDirection(Qt.LeftToRight)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.create_font(10))

        # Create vertical spacer
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(verticalSpacer, 9, 5)

        # Create run and close buttons
        layout_run_close = QGridLayout()
        layout_run_close.setContentsMargins(-1, -1, 0, 0)

        self.run_pb = QPushButton("Run")
        self.run_pb.setFont(self.create_font(10, bold=True))
        self.run_pb.clicked.connect(self.run_import)
        layout_run_close.addWidget(self.run_pb, 0, 0)

        self.close_pb = QPushButton("Close")
        self.close_pb.setFont(self.create_font(10))
        self.close_pb.clicked.connect(self.close)
        layout_run_close.addWidget(self.close_pb, 0, 1)

        self.gridLayout.addLayout(layout_run_close, 10, 5)

    def create_font(self, point_size: int, bold: bool = False):
        return create_font(self, point_size, bold=bold)

    def setup_models(self):
        """Set up the models for the tree views. To be implemented by subclasses."""
        raise NotImplementedError

    def setup_labels(self):
        """Set up the labels with the model name."""
        model_name = self.import_model_cls.__layername__
        self.setWindowTitle(self.windowTitle().format(model_name.lower()))
        self.source_layer_label.setText(
            self.source_layer_label.text().format(model_name.lower())
        )
        self.tab_widget.setTabText(0, self.tab_widget.tabText(0).format(model_name))

    def set_source_layer_filter(self):
        """Set the filter for the source layer combo box based on the model's geometry type."""
        raise NotImplementedError

    @property
    def source_layer(self) -> Optional[QgsMapLayer]:
        """Get the currently selected source layer."""
        return self.source_layer_cbo.currentLayer()

    @property
    def data_models_tree_views(
        self,
    ) -> Dict[Type, Tuple[QTreeView, QStandardItemModel]]:
        """Get the tree views and models for the data models. To be implemented by subclasses."""
        raise NotImplementedError

    @property
    def models(self) -> List[Type]:
        """Get the list of models to import. To be implemented by subclasses."""
        raise NotImplementedError

    @property
    def layer_dependent_widgets(self) -> List[QWidget]:
        """Get the list of widgets that depend on the source layer. To be implemented by subclasses."""
        raise NotImplementedError

    def on_layer_changed(self, layer: Optional[QgsMapLayer]):
        """Handle layer change events.

        Args:
            layer: The new layer
        """
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
            self.activate_layer_dependent_widgets()
        else:
            self.deactivate_layer_dependent_widgets()

        for model_cls in self.models:
            source_attribute_widgets = self.get_column_widgets(
                ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX, model_cls
            )
            for combobox in source_attribute_widgets:
                combobox.clear()
                combobox.addItems(layer_field_names)
                combobox.setCurrentText(combobox.data_model_field_name)

            expression_widgets = self.get_column_widgets(
                ColumnImportIndex.EXPRESSION_COLUMN_IDX, model_cls
            )
            for expression_widget in expression_widgets:
                expression_widget.setLayer(layer)

    def collect_settings(self) -> Dict[str, Any]:
        """Collect the import settings. To be implemented by subclasses."""
        raise NotImplementedError

    def source_fields_missing(self) -> bool:
        """Check if any required source fields are missing. To be implemented by subclasses."""
        raise NotImplementedError

    def save_import_settings(self):
        """Save the import settings to a template file."""
        template_filepath = self.get_filepath(save=True)
        if not template_filepath:
            return

        try:
            with open(template_filepath, "w") as template_file:
                json.dump(self.collect_settings(), template_file, indent=2)
            self.uc.show_info(f"Settings saved to the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def load_import_settings(self):
        """Load import settings from a template file."""
        template_filepath = self.get_filepath(save=False)
        if not template_filepath:
            return

        try:
            with open(template_filepath, "r") as template_file:
                import_settings = json.loads(template_file.read())
            self.update_settings_from_template(import_settings)
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def update_settings_from_template(self, import_settings: Dict[str, Any]):
        """Update settings from a template. To be implemented by subclasses."""
        self.reset_settings_widget()
        self.update_fields_settings(self.import_model_cls, import_settings["fields"])

    def collect_fields_settings(self, model_cls: Type) -> Dict[str, Any]:
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        fields_settings = {}
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(field_name):
                continue
            field_config = {}
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                config = ImportFieldMappingUtils.collect_config_from_widget(
                    widget, key_name, field_type, column_idx
                )
                if config is not None:
                    field_config[key_name] = config
            fields_settings[field_name] = field_config
            row_idx += 1
        return fields_settings

    def get_rows_from_settings_widget(self, model_cls, row_idx, column_indices):
        widgets = []
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        for col_idx in column_indices:
            item_idx = tree_view_model.item(row_idx, col_idx).index()
            widgets.append(tree_view.indexWidget(item_idx))
        return widgets

    def source_fields_missing_for_models(self, *model_classes: Type) -> bool:
        if not self.source_layer:
            self.uc.show_warning("Please select a source layer first.", self)
            return True

        missing_fields = []
        for model_cls in model_classes:
            field_labels = self.get_column_widgets(
                ColumnImportIndex.FIELD_NAME_COLUMN_IDX, model_cls
            )
            method_widgets = self.get_column_widgets(
                ColumnImportIndex.METHOD_COLUMN_IDX, model_cls
            )
            source_attribute_widgets = self.get_column_widgets(
                ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX, model_cls
            )
            for field_lbl, method_cbo, source_attribute_cbo in zip(
                field_labels, method_widgets, source_attribute_widgets
            ):
                field_name, method_txt, source_attribute_txt = (
                    field_lbl.text().strip(),
                    method_cbo.currentText(),
                    source_attribute_cbo.currentText(),
                )
                if (
                    method_txt == str(ColumnImportMethod.ATTRIBUTE)
                    and not source_attribute_txt
                ):
                    missing_fields.append(field_name)

        if missing_fields:
            self.uc.show_warn(
                f"The following fields are missing a source attribute or expression: {', '.join(missing_fields)}",
                self,
            )
            return True
        return False

    def reset_settings_widget(self):
        """Reset the settings widgets to their default values."""
        for model_cls in self.models:
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            for row in range(tree_view_model.rowCount()):
                for col in range(tree_view_model.columnCount()):
                    widget = tree_view.indexWidget(tree_view_model.index(row, col))
                    # Reset widgets based on their type
                    if isinstance(widget, QComboBox):
                        widget.setCurrentIndex(0)
                    elif isinstance(widget, QLineEdit):
                        widget.setText("")
                    elif isinstance(widget, QgsFieldExpressionWidget):
                        widget.setExpression("")

    def run_import(self):
        """Run the import process."""
        if self.source_fields_missing():
            return

        handlers, layers = self.prepare_import()
        selected_feat_ids = (
            self.source_layer.selectedFeatureIds()
            if self.selected_only_cb.isChecked()
            else None
        )
        import_settings = self.collect_settings()
        try:
            for handler in handlers:
                handler.disconnect_handler_signals()
            structures_importer = self.IMPORTERS[self.import_model_cls](
                self.source_layer,
                self.model_gpkg,
                import_settings,
                **layers,
            )
            with CatchThreediWarnings() as warnings_catcher:
                structures_importer.import_features(selected_ids=selected_feat_ids)
            success_msg = (
                "Import completed successfully.\n\n"
                "The layers to which the data has been added are still in editing mode, "
                "so you can review the changes before saving them to the layers."
                f"{warnings_catcher.warnings_msg}"
            )
            self.uc.show_info(success_msg, self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)
            QgsMessageLog.logMessage(
                f"Import failed with traceback:\n{traceback.format_exc()}",
                "Warning",
                Qgis.Warning,
            )
        finally:
            for handler in handlers:
                handler.connect_handler_signals()
        for handler in handlers:
            handler.layer.triggerRepaint()

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        raise NotImplementedError

    def is_obsolete_field(self, field_name: str) -> bool:
        return field_name in self.import_model_cls.obsolete_fields()

    def activate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setEnabled(True)

    def deactivate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setDisabled(True)

    def get_filepath(self, save: bool = False) -> Optional[str]:
        extension_filter = "JSON (*.json)"
        filepath = get_filepath(
            self,
            extension_filter,
            save=save,
            default_settings_entry=ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY,
        )
        if not filepath:
            return None
        settings = QgsSettings()
        settings.setValue(
            ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY, os.path.dirname(filepath)
        )
        return filepath

    def update_fields_settings(self, model_cls: Type, fields_setting: Dict[str, Any]):
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(field_name):
                continue
            if is_optional(field_type):
                field_type = optional_type(field_type)
            field_config = fields_setting.get(field_name, {})
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                ImportFieldMappingUtils.update_widget_with_config(
                    widget, key_name, field_type, field_config
                )
            row_idx += 1

    def get_column_widgets(self, column_idx: int, data_model: Type) -> List[QWidget]:
        model_widgets = []
        if data_model not in self.data_models_tree_views:
            return model_widgets
        tree_view, tree_view_model = self.data_models_tree_views[data_model]
        row_idx = 0
        for field_name in data_model.__annotations__.keys():
            if self.is_obsolete_field(field_name):
                continue
            item = tree_view_model.item(row_idx, column_idx)
            index = item.index()
            widget = tree_view.indexWidget(index)
            widget.data_model_field_name = field_name
            model_widgets.append(widget)
            row_idx += 1
        return model_widgets

    def connect_conversion_settings_widget(self):
        for model_cls in self.models:
            row_idx = 0
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            for field_name in model_cls.__annotations__.keys():
                if self.is_obsolete_field(field_name):
                    continue
                method_combobox = tree_view.indexWidget(
                    tree_view_model.item(
                        row_idx, ColumnImportIndex.METHOD_COLUMN_IDX
                    ).index()
                )
                source_attribute_combobox = tree_view.indexWidget(
                    tree_view_model.item(
                        row_idx, ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX
                    ).index()
                )
                expression_widget = tree_view.indexWidget(
                    tree_view_model.item(
                        row_idx, ColumnImportIndex.EXPRESSION_COLUMN_IDX
                    ).index()
                )
                value_map_button = tree_view.indexWidget(
                    tree_view_model.item(
                        row_idx, ColumnImportIndex.VALUE_MAP_COLUMN_IDX
                    ).index()
                )
                method_combobox.currentTextChanged.connect(
                    partial(
                        ImportFieldMappingUtils.on_method_changed,
                        source_attribute_combobox,
                        value_map_button,
                        expression_widget,
                    )
                )
                method_combobox.currentTextChanged.emit(method_combobox.currentText())
                source_attribute_combobox.currentTextChanged.connect(
                    partial(
                        ImportFieldMappingUtils.on_source_attribute_value_changed,
                        method_combobox,
                        source_attribute_combobox,
                    )
                )
                value_map_button.clicked.connect(
                    partial(
                        ImportFieldMappingUtils.on_value_map_clicked,
                        self.source_layer_cbo,
                        source_attribute_combobox,
                        value_map_button,
                        self.uc,
                        self,
                    )
                )
                row_idx += 1

    def get_widgets(self):
        raise NotImplementedError

    def create_conversion_settings_widget(self):
        """Create conversion settings widgets.

        Args:
            models: List of models
            data_models_tree_views: Dictionary mapping model classes to tree views and models
        """
        widgets_to_add = self.get_widgets()
        for model_cls in self.models:
            model_widgets = widgets_to_add[model_cls]
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            tree_view_model.clear()
            tree_view_model.setHorizontalHeaderLabels(CONFIG_HEADER)
            for (row_idx, column_idx), widget in model_widgets.items():
                tree_view_model.setItem(row_idx, column_idx, QStandardItem(""))
                tree_view.setIndexWidget(
                    tree_view_model.index(row_idx, column_idx), widget
                )
            for i in range(len(CONFIG_HEADER)):
                tree_view.resizeColumnToContents(i)

    def get_snap_settings(self):
        snap_gb = QGroupBox("Snap within:")
        snap_gb.setFont(self.create_font(9))
        snap_gb.setCheckable(True)
        layout = QGridLayout(snap_gb)
        snap_dsb = QDoubleSpinBox()
        snap_dsb.setFont(self.create_font(10))
        snap_dsb.setSuffix(" meters")
        snap_dsb.setMaximum(1000000.0)
        snap_dsb.setValue(0.1)
        layout.addWidget(snap_dsb, 0, 0)
        return snap_gb, snap_dsb, layout


class ImportFeaturesDialog(ImportDialog):
    """Dialog for importing features."""

    def setup_ui(self):
        super().setup_ui()

        # Create selected features checkbox with horizontal layout
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)

        horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        horizontalLayout.addItem(horizontalSpacer)

        horizontalLayout.addWidget(self.selected_only_cb)
        self.gridLayout.addLayout(horizontalLayout, 1, 1)

        # Create field map tab
        self.field_map_tab = QWidget()
        self.field_map_tab.setObjectName("field_map_tab")
        gridLayout_3 = QGridLayout(self.field_map_tab)

        self.field_map_tv = QTreeView()
        gridLayout_3.addWidget(self.field_map_tv, 0, 0)

        self.tab_widget.addTab(self.field_map_tab, "{}")
        self.gridLayout.addWidget(self.tab_widget, 6, 0, 4, 4)

    def setup_models(self):
        """Set up the models for the tree views."""
        self.field_map_model = QStandardItemModel()
        self.field_map_tv.setModel(self.field_map_model)

    def get_widgets(self):
        return create_widgets(*self.models)

    def set_source_layer_filter(self):
        """Set the filter for the source layer combo box based on the model's geometry type."""
        if self.import_model_cls.__geometrytype__ == dm.GeometryType.Point:
            layer_filter = QgsMapLayerProxyModel.PointLayer
        elif self.import_model_cls.__geometrytype__ == dm.GeometryType.Linestring:
            layer_filter = QgsMapLayerProxyModel.LineLayer
        elif self.import_model_cls.__geometrytype__ == dm.GeometryType.Polygon:
            layer_filter = QgsMapLayerProxyModel.PolygonLayer
        else:
            layer_filter = None
        if layer_filter is not None:
            self.source_layer_cbo.setFilters(layer_filter)

    @property
    def data_models_tree_views(
        self,
    ) -> Dict[Type, Tuple[QTreeView, QStandardItemModel]]:
        return {self.import_model_cls: (self.field_map_tv, self.field_map_model)}

    @property
    def models(self) -> List[Type]:
        return [self.import_model_cls]

    @property
    def layer_dependent_widgets(self) -> List[QWidget]:
        return [
            self.tab_widget,
            self.save_pb,
            self.load_pb,
            self.run_pb,
            self.selected_only_cb,
        ]

    def collect_settings(self) -> Dict[str, Any]:
        return {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
        }

    def source_fields_missing(self) -> bool:
        return self.source_fields_missing_for_models(self.import_model_cls)

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        handler = self.layer_manager.model_handlers[self.import_model_cls]
        return [handler], {"target_layer": handler.layer}


class ImportCrossSectionLocationDialog(ImportFeaturesDialog):
    """Dialog for importing cross section location."""

    def set_source_layer_filter(self):
        self.source_layer_cbo.setFilters(
            QgsMapLayerProxyModel.LineLayer
            | QgsMapLayerProxyModel.PointLayer
            | QgsMapLayerProxyModel.NoGeometry
        )

    def on_layer_changed(self, layer: Optional[QgsMapLayer]):
        super().on_layer_changed(layer)
        self.join_source.input_cbo.setLayer(layer)

    @property
    def layer_dependent_widgets(self) -> List[QWidget]:
        return (
            super().layer_dependent_widgets
            + self.join_source.layer_dependent_widgets
            + self.join_target.layer_dependent_widgets
        )

    def collect_settings(self) -> Dict[str, Any]:
        return {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
            "conversion_settings": {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "join_field_src": self.join_source.value,
                "join_field_tgt": self.join_target.value,
            },
        }

    def setup_ui(self):
        super().setup_ui()
        # self.join_settings = JoinFieldsDialog()
        self.join_source = JoinFieldsRow("Join channel source field", layer_src=True)
        self.join_target = JoinFieldsRow("Join channel reference field")
        join_layout = QGridLayout()
        join_layout.setContentsMargins(-1, -1, -1, 0)
        join_layout.addWidget(self.join_source.lbl, 0, 0)
        join_layout.addWidget(self.join_source.toggle_widget, 0, 1)
        join_layout.addWidget(self.join_source.stack, 0, 2)
        join_layout.addWidget(self.join_target.lbl, 1, 0)
        join_layout.addWidget(self.join_target.toggle_widget, 1, 1)
        join_layout.addWidget(self.join_target.stack, 1, 2)
        self.gridLayout.addLayout(join_layout, 1, 0, 2, 2)

        # Create snap group box
        self.snap_gb, self.snap_dsb, _ = self.get_snap_settings()
        self.gridLayout.addWidget(self.snap_gb, 8, 4, 1, 2)

    def update_settings_from_template(self, import_settings: Dict[str, Any]):
        super().update_settings_from_template(import_settings)
        self.load_conversion_settings(import_settings)

    def load_conversion_settings(self, import_settings: Dict[str, Any]):
        conversion_settings = import_settings["conversion_settings"]
        self.snap_gb.setChecked(conversion_settings.get("use_snapping", True))
        self.snap_dsb.setValue(conversion_settings.get("snapping_distance", 0.1))
        self.join_source.value = conversion_settings.get("join_field_src", "")
        self.join_target.value = conversion_settings.get("join_field_tgt", "")

    def source_fields_missing(self) -> bool:
        missing_fields = super().source_fields_missing()
        if missing_fields:
            return True
        if self.source_layer and not self.source_layer.isSpatial():
            missing = []
            if not self.join_source.value:
                missing.append("Join channel source field")
            if not self.join_target.value:
                missing.append("Join channel reference field")
            if len(missing) > 0:
                self.uc.show_warn(
                    f"The following fields are missing a source attribute or expression: {', '.join(missing)}",
                    self,
                )
                return True
        return False


class ImportStructuresDialog(ImportDialog):
    """Dialog for the importing structures tool."""

    HAS_INTEGRATOR = [dm.Culvert, dm.Orifice, dm.Weir]
    HAS_PIPE_INTEGRATOR = [dm.Weir, dm.Orifice]

    def __init__(
        self,
        import_model_cls: Type,
        model_gpkg: str,
        layer_manager: Any,
        uc: Any,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(import_model_cls, model_gpkg, layer_manager, uc, parent)
        self.create_nodes_cb.stateChanged.connect(self.on_create_nodes_change)
        if not self.enable_structures_integration:
            for widget in self.structures_integration_widgets:
                widget.hide()

    def setup_ui(self):
        super().setup_ui()

        # Update source layer label to include model type
        self.source_layer_label.setText("Source {} layer")

        # Create grid layout for checkboxes and fields
        gridLayout_7 = QGridLayout()
        gridLayout_7.setContentsMargins(-1, -1, -1, 0)

        # Create checkboxes
        self.edit_lbl = QLabel("Edit")
        self.edit_lbl.setFont(self.create_font(10))
        self.edit_cb = QComboBox()
        self.edit_cb.setFont(self.create_font(10))
        self.edit_cb.addItems(["None", "Channels"])
        if self.import_model_cls in self.HAS_PIPE_INTEGRATOR:
            self.edit_cb.addItems(["Pipes"])
        gridLayout_7.addWidget(self.edit_lbl, 0, 0)
        gridLayout_7.addWidget(self.edit_cb, 0, 1)

        self.create_nodes_cb = QCheckBox("Create connection nodes")
        self.create_nodes_cb.setFont(self.create_font(10))
        self.create_nodes_cb.setLayoutDirection(Qt.LeftToRight)
        self.create_nodes_cb.setChecked(True)
        gridLayout_7.addWidget(self.create_nodes_cb, 0, 2)

        gridLayout_7.addWidget(self.selected_only_cb, 0, 3)

        # Create length source field widgets
        self.length_source_field_lbl = QLabel("Length source field")
        self.length_source_field_lbl.setFont(self.create_font(10))
        self.length_source_field_lbl.setLayoutDirection(Qt.LeftToRight)
        gridLayout_7.addWidget(self.length_source_field_lbl, 1, 0)

        self.length_source_field_cbo = QgsFieldComboBox()
        self.length_source_field_cbo.setFont(self.create_font(10))
        self.length_source_field_cbo.setAllowEmptyFieldName(True)
        gridLayout_7.addWidget(self.length_source_field_cbo, 1, 1)

        self.length_fallback_value_lbl = QLabel("Length fallback value")
        self.length_fallback_value_lbl.setFont(self.create_font(10))
        gridLayout_7.addWidget(self.length_fallback_value_lbl, 1, 2)

        self.length_fallback_value_dsb = QDoubleSpinBox()
        self.length_fallback_value_dsb.setFont(self.create_font(10))
        self.length_fallback_value_dsb.setMinimum(0.01)
        self.length_fallback_value_dsb.setValue(1.0)
        gridLayout_7.addWidget(self.length_fallback_value_dsb, 1, 3)

        # Create azimuth source field widgets
        self.azimuth_source_field_lbl = QLabel("Azimuth source field")
        self.azimuth_source_field_lbl.setFont(self.create_font(10))
        gridLayout_7.addWidget(self.azimuth_source_field_lbl, 2, 0)

        self.azimuth_source_field_cbo = QgsFieldComboBox()
        self.azimuth_source_field_cbo.setFont(self.create_font(10))
        self.azimuth_source_field_cbo.setAllowEmptyFieldName(True)
        gridLayout_7.addWidget(self.azimuth_source_field_cbo, 2, 1)

        self.azimuth_fallback_value_lbl = QLabel("Azimuth fallback value")
        self.azimuth_fallback_value_lbl.setFont(self.create_font(10))
        gridLayout_7.addWidget(self.azimuth_fallback_value_lbl, 2, 2)

        self.azimuth_fallback_value_sb = QSpinBox()
        self.azimuth_fallback_value_sb.setFont(self.create_font(10))
        self.azimuth_fallback_value_sb.setMaximum(359)
        self.azimuth_fallback_value_sb.setValue(90)
        gridLayout_7.addWidget(self.azimuth_fallback_value_sb, 2, 3)

        self.gridLayout.addLayout(gridLayout_7, 1, 0, 2, 2)

        # Create structure tab
        self.structure_tab = QWidget()
        gridLayout_2 = QGridLayout(self.structure_tab)

        self.structure_tv = QTreeView()
        gridLayout_2.addWidget(self.structure_tv, 1, 0)

        self.tab_widget.addTab(self.structure_tab, "{}")

        # Create connection node tab
        self.connection_node_tab = QWidget()
        gridLayout_3 = QGridLayout(self.connection_node_tab)

        self.connection_node_tv = QTreeView()
        gridLayout_3.addWidget(self.connection_node_tv, 0, 0)

        self.tab_widget.addTab(self.connection_node_tab, "Connection nodes")

        self.gridLayout.addWidget(self.tab_widget, 5, 0, 5, 4)

        # Create snap group box
        self.snap_gb, self.snap_dsb, snap_layout = self.get_snap_settings()
        self.gridLayout.addWidget(self.snap_gb, 8, 4, 1, 2)

        # Create minimum channel length
        self.min_channel_dsb = QDoubleSpinBox()
        self.min_channel_dsb.setFont(self.create_font(10))
        self.min_channel_dsb.setSuffix(" meters")
        self.min_channel_dsb.setMaximum(1000000.0)
        self.min_channel_dsb.setValue(5)
        self.min_channel_gb = QGroupBox("Minimum length:")
        self.min_channel_gb.setToolTip(
            "Structures will be integrated in the network such that no channel or pipe feature is created shorter than this value."
        )
        self.min_channel_gb.setFont(self.create_font(9))
        min_channel_layout = QGridLayout(self.min_channel_gb)
        min_channel_layout.addWidget(self.min_channel_dsb, 0, 0)

        # Place minimum channel length and snapping in one layout
        rhs_layout = QVBoxLayout()
        rhs_layout.addWidget(self.snap_gb)
        rhs_layout.addWidget(self.min_channel_gb)
        self.gridLayout.addLayout(rhs_layout, 8, 4, 1, 2)

    def setup_models(self):
        self.structure_model = QStandardItemModel()
        self.structure_tv.setModel(self.structure_model)
        self.connection_node_model = QStandardItemModel()
        self.connection_node_tv.setModel(self.connection_node_model)

    def set_source_layer_filter(self):
        """Set the filter for the source layer combo box based on the model's geometry type."""
        self.source_layer_cbo.setFilters(
            QgsMapLayerProxyModel.PointLayer
            if self.import_model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )

    @property
    def data_models_tree_views(
        self,
    ) -> Dict[Type, Tuple[QTreeView, QStandardItemModel]]:
        return {
            self.import_model_cls: (self.structure_tv, self.structure_model),
            dm.ConnectionNode: (self.connection_node_tv, self.connection_node_model),
        }

    @property
    def models(self) -> List[Type]:
        return [self.import_model_cls, dm.ConnectionNode]

    @property
    def layer_dependent_widgets(self) -> List[QWidget]:
        widgets = [
            self.tab_widget,
            self.save_pb,
            self.load_pb,
            self.run_pb,
            self.selected_only_cb,
            self.create_nodes_cb,
            self.snap_gb,
        ]
        if self.enable_structures_integration:
            widgets += self.structures_integration_widgets
        return widgets

    @cached_property
    def enable_structures_integration(self) -> bool:
        return self.import_model_cls in self.HAS_INTEGRATOR

    @property
    def structures_integration_widgets(self) -> List[QWidget]:
        return [
            self.edit_cb,
            self.edit_lbl,
            self.length_source_field_lbl,
            self.length_source_field_cbo,
            self.length_fallback_value_lbl,
            self.length_fallback_value_dsb,
            self.azimuth_source_field_lbl,
            self.azimuth_source_field_cbo,
            self.azimuth_fallback_value_lbl,
            self.azimuth_fallback_value_sb,
            self.min_channel_gb,
        ]

    def on_create_nodes_change(self, is_checked: bool):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer: Optional[QgsMapLayer]):
        super().on_layer_changed(layer)
        self.length_source_field_cbo.setLayer(layer)
        self.azimuth_source_field_cbo.setLayer(layer)

    def collect_settings(self) -> Dict[str, Any]:
        return {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
            "conversion_settings": {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "minimum_channel_length": self.min_channel_dsb.value(),
                "create_connection_nodes": self.create_nodes_cb.isChecked(),
                "length_source_field": self.length_source_field_cbo.currentField(),
                "length_fallback_value": self.length_fallback_value_dsb.value(),
                "azimuth_source_field": self.azimuth_source_field_cbo.currentField(),
                "azimuth_fallback_value": self.azimuth_fallback_value_sb.value(),
                "edit_channels": self.edit_cb.currentText().lower() == "channels",
                "edit_pipes": self.edit_cb.currentText().lower() == "pipes",
            },
            "connection_node_fields": self.collect_fields_settings(dm.ConnectionNode),
        }

    def source_fields_missing(self) -> bool:
        data_models = [self.import_model_cls]
        if self.create_nodes_cb.isChecked():
            data_models.append(dm.ConnectionNode)

        # Check if the source layer has no geometry
        missing_fields = self.source_fields_missing_for_models(*data_models)
        if self.source_layer and not self.source_layer.isSpatial():
            if not self.length_source_field_cbo.currentField():
                missing_fields.append("Length source field")
            if not self.azimuth_source_field_cbo.currentField():
                missing_fields.append("Azimuth source field")
        return missing_fields

    def update_settings_from_template(self, import_settings: Dict[str, Any]):
        super().update_settings_from_template(import_settings)
        self.load_conversion_settings(import_settings)

    def load_conversion_settings(self, import_settings: Dict[str, Any]):
        conversion_settings = import_settings["conversion_settings"]
        self.snap_gb.setChecked(conversion_settings.get("use_snapping", True))
        self.snap_dsb.setValue(conversion_settings.get("snapping_distance", 0.1))
        self.min_channel_dsb.setValue(
            conversion_settings.get("minimum_channel_length", 5)
        )
        self.create_nodes_cb.setChecked(
            conversion_settings.get("create_connection_nodes", True)
        )
        if conversion_settings.get("edit_channels", False):
            self.edit_cb.setCurrentIndex(1)
        elif conversion_settings.get("edit_pipes", False):
            self.edit_cb.setCurrentIndex(2)
        else:
            self.edit_cb.setCurrentIndex(0)
        self.length_source_field_cbo.setField(
            conversion_settings.get("length_source_field", "")
        )
        self.length_fallback_value_dsb.setValue(
            conversion_settings.get("length_fallback_value", 1.0)
        )
        self.azimuth_source_field_cbo.setField(
            conversion_settings.get("azimuth_source_field", "")
        )
        self.azimuth_fallback_value_sb.setValue(
            conversion_settings.get("azimuth_fallback_value", 90)
        )
        try:
            connection_node_fields = import_settings["connection_node_fields"]
            self.update_fields_settings(dm.ConnectionNode, connection_node_fields)
        except KeyError:
            pass

    def prepare_import(self) -> Tuple[List[Any], Dict[str, Any]]:
        structures_handler = self.layer_manager.model_handlers[self.import_model_cls]
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        import_settings = self.collect_settings()
        processed_handlers = [structures_handler, node_handler]
        processed_layers = {
            "structure_layer": structures_handler.layer,
            "node_layer": node_handler.layer,
        }
        if import_settings["conversion_settings"].get("edit_channels", False):
            conduit_handler = self.layer_manager.model_handlers[dm.Channel]
            cross_section_location_handler = self.layer_manager.model_handlers[
                dm.CrossSectionLocation
            ]
            processed_handlers += [conduit_handler, cross_section_location_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
            processed_layers["cross_section_location_layer"] = (
                cross_section_location_handler.layer
            )
        if import_settings["conversion_settings"].get("edit_pipes", False):
            conduit_handler = self.layer_manager.model_handlers[dm.Pipe]
            processed_handlers += [conduit_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
        return processed_handlers, processed_layers

    def get_widgets(self):
        return create_widgets(
            *self.models,
            auto_attribute_fields={
                "connection_node_id",
                "connection_node_id_start",
                "connection_node_id_end",
            },
        )
