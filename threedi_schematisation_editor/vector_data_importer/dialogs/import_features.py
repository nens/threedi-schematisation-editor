import json
import os
from functools import partial, cached_property

from qgis.core import QgsMapLayerProxyModel, QgsSettings
from qgis.gui import QgsFieldExpressionWidget, QgsMapLayerComboBox
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import (
    QComboBox, QLineEdit, QDialog, QGridLayout, QLabel, QPushButton, 
    QTabWidget, QTreeView, QWidget, QHBoxLayout, QCheckBox, QSpacerItem,
    QSizePolicy
)
from qgis.PyQt.QtCore import Qt
from qgis.core import (
    Qgis,
    QgsMessageLog,
)
from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.dialogs.import_widgets import create_widgets, CONFIG_HEADER, CONFIG_KEYS
from threedi_schematisation_editor.utils import core_field_type, is_optional, optional_type, get_filepath
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod
from threedi_schematisation_editor.vector_data_importer.importers import ConnectionNodesImporter, CulvertsImporter, \
    OrificesImporter, WeirsImporter, PipesImporter
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import CatchThreediWarnings, ImportFieldMappingUtils, \
    ColumnImportIndex


class ImportDialogUtils:
    IMPORTERS = {
        dm.ConnectionNode: ConnectionNodesImporter,
        dm.Culvert: CulvertsImporter,
        dm.Orifice: OrificesImporter,
        dm.Weir: WeirsImporter,
        dm.Pipe: PipesImporter,
    }

    @staticmethod
    def is_obsolete_field(model_cls, field_name):
        return field_name in model_cls.obsolete_fields()

    @staticmethod
    def activate_widgets(widgets):
        for widget in widgets:
            widget.setEnabled(True)

    @staticmethod
    def deactivate_widgets(widgets):
        for widget in widgets:
            widget.setDisabled(True)

    @staticmethod
    def get_filepath(parent, save=False):
        extension_filter = "JSON (*.json)"
        filepath = get_filepath(
            parent, extension_filter, save=save, default_settings_entry=ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY
        )
        if not filepath:
            return
        settings = QgsSettings()
        settings.setValue(ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY, os.path.dirname(filepath))
        return filepath

    @staticmethod
    def save_import_settings(import_settings, parent, uc):
        template_file = ImportDialogUtils.get_filepath(parent, save=True)
        try:
            with open(template_filepath, "w") as template_file:
                json.dump(import_settings, template_file, indent=2)
            uc.show_info(f"Settings saved to the template.", self)
        except Exception as e:
            uc.show_error(f"Import failed due to the following error:\n{e}", self)

    @staticmethod
    def update_fields_settings(tree_view, tree_view_model, model_cls, fields_setting):
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if ImportDialogUtils.is_obsolete_field(model_cls, field_name):
                continue
            if is_optional(field_type):
                field_type = optional_type(field_type)
            field_config = fields_setting.get(field_name, {})
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                ImportFieldMappingUtils.update_widget_with_config(widget, key_name, field_type, field_config)
            row_idx += 1

    @staticmethod
    def run_import(import_settings, model_gpkg, source_layer, selected_feat_ids, importer_cls, uc, handlers=None, layers=None):
        handlers = [] if handlers is None else handlers
        layers = {} if layers is None else layers
        try:
            for handler in handlers:
                handler.disconnect_handler_signals()
            structures_importer = importer_cls(
                source_layer,
                model_gpkg,
                import_settings,
                **layers,
            )
            with CatchThreediWarnings() as warnings_catcher:
                structures_importer.import_features(selected_ids=selected_feat_ids)
            success_msg = (
                "Structures imported successfully.\n\n"
                "The layers to which the structures have been added are still in editing mode, "
                "so you can review the changes before saving them to the layers."
                f"{warnings_catcher.warnings_msg}"
            )
            uc.show_info(success_msg, self)
        except Exception as e:
            uc.show_error(f"Import failed due to the following error:\n{e}", self)
        finally:
            for handler in handlers:
                handler.connect_handler_signals()
        for layer in layers.values():
            layer.triggerRepaint()

    @staticmethod
    def get_column_widgets(data_models_tree_views, column_idx, data_model):
        model_widgets = []
        if data_model not in data_models_tree_views:
            return model_widgets
        tree_view, tree_view_model = data_models_tree_views[data_model]
        row_idx = 0
        for field_name in data_model.__annotations__.keys():
            if ImportDialogUtils.is_obsolete_field(data_model, field_name):
                continue
            item = tree_view_model.item(row_idx, column_idx)
            index = item.index()
            widget = tree_view.indexWidget(index)
            widget.data_model_field_name = field_name
            model_widgets.append(widget)
            row_idx += 1
        return model_widgets

    @staticmethod
    def connect_configuration_widgets(data_models, data_models_tree_views, source_layer_cbo, uc, parent):
        # brrr, I don't like passing the parent class
        for model_cls in data_models:
            tree_view, tree_view_model = data_models_tree_views[model_cls]
            row_idx = 0
            for field_name in model_cls.__annotations__.keys():
                if ImportDialogUtils.is_obsolete_field(model_cls, field_name):
                    continue
                method_item = tree_view_model.item(row_idx, ColumnImportIndex.METHOD_COLUMN_IDX)
                method_index = method_item.index()
                method_combobox = tree_view.indexWidget(method_index)
                source_attribute_item = tree_view_model.item(
                    row_idx, ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX
                )
                source_attribute_index = source_attribute_item.index()
                source_attribute_combobox = tree_view.indexWidget(source_attribute_index)
                value_map_item = tree_view_model.item(row_idx, ColumnImportIndex.VALUE_MAP_COLUMN_IDX)
                value_map_index = value_map_item.index()
                value_map_button = tree_view.indexWidget(value_map_index)
                expression_item = tree_view_model.item(row_idx, ColumnImportIndex.EXPRESSION_COLUMN_IDX)
                expression_index = expression_item.index()
                expression_widget = tree_view.indexWidget(expression_index)
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
                        source_layer_cbo,
                        source_attribute_combobox,
                        value_map_button,
                        uc,
                        parent,
                    )
                )
                row_idx += 1

    @staticmethod
    def create_conversion_settings_widget(models, data_models_tree_views):
        widgets_to_add = create_widgets(*models)
        for model_cls in models:
            model_widgets = widgets_to_add[model_cls]
            tree_view, tree_view_model = data_models_tree_views[model_cls]
            tree_view_model.clear()
            tree_view_model.setHorizontalHeaderLabels(CONFIG_HEADER)
            for (row_idx, column_idx), widget in model_widgets.items():
                tree_view_model.setItem(row_idx, column_idx, QStandardItem(""))
                tree_view.setIndexWidget(tree_view_model.index(row_idx, column_idx), widget)
            for i in range(len(CONFIG_HEADER)):
                tree_view.resizeColumnToContents(i)


class ImportFeaturesDialog(QDialog):

    def __init__(self, import_model_cls, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(parent)
        self.import_model_cls = import_model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc

        # Create UI elements
        self.setupUi()

        self.set_source_layer_filter()
        self.setup_models()
        self.source_layer_cbo.setCurrentIndex(0)
        self.source_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.populate_conversion_settings_widgets()
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import)
        self.close_pb.clicked.connect(self.close)
        self.setup_labels()

    def setupUi(self):
        # Set window properties
        self.setWindowTitle("Import {}s")
        self.resize(1002, 757)

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
        self.gridLayout.addWidget(self.source_layer_cbo, 0, 1)

        # Create save button
        self.save_pb = QPushButton("Save as template...")
        self.save_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.save_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.save_pb, 0, 4, 1, 2)

        # Create selected features checkbox
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)

        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontalLayout.addItem(horizontalSpacer)

        self.selected_only_cb = QCheckBox("Selected features only")
        self.selected_only_cb.setFont(self.create_font(10))
        self.selected_only_cb.setLayoutDirection(Qt.LeftToRight)
        horizontalLayout.addWidget(self.selected_only_cb)

        self.gridLayout.addLayout(horizontalLayout, 1, 1)

        # Create load button
        self.load_pb = QPushButton("Load template...")
        self.load_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.load_pb, 1, 4, 1, 2)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.create_font(10))

        # Create field map tab
        self.field_map_tab = QWidget()
        self.field_map_tab.setObjectName("field_map_tab")
        gridLayout_3 = QGridLayout(self.field_map_tab)

        self.field_map_tv = QTreeView()
        gridLayout_3.addWidget(self.field_map_tv, 0, 0)

        self.tab_widget.addTab(self.field_map_tab, "{}")
        self.gridLayout.addWidget(self.tab_widget, 6, 0, 4, 4)

        # Create vertical spacer
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(verticalSpacer, 9, 5)

        # Create run and close buttons
        gridLayout_6 = QGridLayout()
        gridLayout_6.setContentsMargins(-1, -1, 0, 0)

        self.run_pb = QPushButton("Run")
        self.run_pb.setFont(self.create_font(10, bold=True))
        gridLayout_6.addWidget(self.run_pb, 0, 0)

        self.close_pb = QPushButton("Close")
        self.close_pb.setFont(self.create_font(10))
        gridLayout_6.addWidget(self.close_pb, 0, 1)

        self.gridLayout.addLayout(gridLayout_6, 10, 5)

    def create_font(self, point_size, bold=False):
        font = self.font()
        font.setPointSize(point_size)
        if bold:
            font.setBold(True)
            font.setWeight(75)
        return font

    def setup_models(self):
        self.field_map_model = QStandardItemModel()
        self.field_map_tv.setModel(self.field_map_model)

    def setup_labels(self):
        model_name = self.import_model_cls.__layername__
        self.setWindowTitle(self.windowTitle().format(model_name.lower()))
        self.source_layer_label.setText(self.source_layer_label.text().format(model_name.lower()))
        self.tab_widget.setTabText(0, self.tab_widget.tabText(0).format(model_name))

    def set_source_layer_filter(self):
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

    def populate_conversion_settings_widgets(self):
        ImportDialogUtils.create_conversion_settings_widget(self.models, self.data_models_tree_views)
        ImportDialogUtils.connect_configuration_widgets([self.import_model_cls], self.data_models_tree_views, self.source_layer_cbo, self.uc, self)
        self.on_layer_changed(self.source_layer)

    @property
    def source_layer(self):
        return self.source_layer_cbo.currentLayer()

    @property
    def data_models_tree_views(self):
        return {self.import_model_cls : (self.field_map_tv, self.field_map_model)}

    @property
    def models(self):
        return [self.import_model_cls]

    @property
    def layer_dependent_widgets(self):
        widgets = [
            self.tab_widget,
            self.save_pb,
            self.load_pb,
            self.run_pb,
            self.selected_only_cb,
        ]
        return widgets

    def on_create_nodes_change(self, is_checked):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
            ImportDialogUtils.activate_widgets(self.layer_dependent_widgets)
        else:
            ImportDialogUtils.deactivate_widgets(self.layer_dependent_widgets)
        source_attribute_widgets = ImportDialogUtils.get_column_widgets(
            self.data_models_tree_views,
            ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX,
            self.import_model_cls)
        for combobox in source_attribute_widgets:
            combobox.clear()
            combobox.addItems(layer_field_names)
            combobox.setCurrentText(combobox.data_model_field_name)
        expression_widgets = ImportDialogUtils.get_column_widgets(
            self.data_models_tree_views,
            ColumnImportIndex.EXPRESSION_COLUMN_IDX,
            self.import_model_cls)
        for expression_widget in expression_widgets:
            expression_widget.setLayer(layer)

    def collect_settings(self):
        return {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
        }

    def source_fields_missing(self):
        return self.source_fields_missing_for_models(self.import_model_cls)

    def save_import_settings(self):
        ImportDialogUtils.save_import_settings(import_settings=self.collect_settings(),
                                               uc=self.uc,
                                               parent=self)

    def load_import_settings(self):
        self.reset_settings_widget()
        try:
            with open(template_filepath, "r") as template_file:
                import_settings = json.loads(template_file.read())
            tree_view, tree_view_model = self.data_models_tree_views[self.import_model_cls]
            ImportDialogUtils.update_fields_settings(tree_view, tree_view_model, self.import_model_cls, import_settings["fields"])
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def run_import(self):
        if self.source_fields_missing():
            return
        selected_feat_ids = source_layer.selectedFeatureIds() if self.selected_only_cb.isChecked() else None
        ImportDialogUtils.import_settings(import_settings=self.collect_settings(),
                                          model_gpkg=self.model_gpkg,
                                          source_layer=self.source_layer,
                                          selected_feat_ids=selected_feat_ids,
                                          importer_cls=ImportDialogUtils.IMPORTERS[self.import_model_cls],
                                          uc=self.uc)


class ImportStructuresDialog(QDialog):
    """Dialog for the importing structures tool."""

    HAS_INTEGRATOR = [dm.Culvert, dm.Orifice, dm.Weir]

    def __init__(self, import_model_cls, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(parent)
        self.import_model_cls = import_model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc

        # Create UI elements
        self.setupUi()

        self.set_source_layer_filter()
        self.setup_models()
        self.source_layer_cbo.setCurrentIndex(0)
        self.source_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.populate_conversion_settings_widgets()
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import)
        self.close_pb.clicked.connect(self.close)
        self.setup_labels()
        self.create_nodes_cb.stateChanged.connect(self.on_create_nodes_change)
        if not self.enable_structures_integration:
            for widget in self.structures_integration_widgets:
                widget.hide()

    def setupUi(self):
        # Set window properties
        self.setWindowTitle("Import {}s")
        self.resize(1000, 750)

        # Create main layout
        self.gridLayout = QGridLayout(self)

        # Create source layer label and combo box
        self.source_layer_label = QLabel("Source {} layer")
        self.source_layer_label.setFont(self.create_font(10))
        self.gridLayout.addWidget(self.source_layer_label, 0, 0)

        self.source_layer_cbo = QgsMapLayerComboBox()
        self.source_layer_cbo.setFont(self.create_font(10))
        self.source_layer_cbo.setAllowEmptyLayer(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.source_layer_cbo.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.source_layer_cbo, 0, 1)

        # Create save button
        self.save_pb = QPushButton("Save as template...")
        self.save_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.save_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.save_pb, 0, 4, 1, 2)

        # Create load button
        self.load_pb = QPushButton("Load template...")
        self.load_pb.setFont(self.create_font(10))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_pb.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.load_pb, 1, 4, 1, 2)

        # Create grid layout for checkboxes and fields
        gridLayout_7 = QGridLayout()
        gridLayout_7.setContentsMargins(-1, -1, -1, 0)

        # Create checkboxes
        self.edit_channels_cb = QCheckBox("Edit channels")
        self.edit_channels_cb.setFont(self.create_font(10))
        self.edit_channels_cb.setLayoutDirection(Qt.LeftToRight)
        gridLayout_7.addWidget(self.edit_channels_cb, 0, 0)

        self.create_nodes_cb = QCheckBox("Create connection nodes")
        self.create_nodes_cb.setFont(self.create_font(10))
        self.create_nodes_cb.setLayoutDirection(Qt.LeftToRight)
        self.create_nodes_cb.setChecked(True)
        gridLayout_7.addWidget(self.create_nodes_cb, 0, 1)

        self.selected_only_cb = QCheckBox("Selected features only")
        self.selected_only_cb.setFont(self.create_font(10))
        self.selected_only_cb.setLayoutDirection(Qt.LeftToRight)
        gridLayout_7.addWidget(self.selected_only_cb, 0, 2)

        # Create length source field widgets
        self.length_source_field_lbl = QLabel("Length source field")
        self.length_source_field_lbl.setFont(self.create_font(10))
        self.length_source_field_lbl.setLayoutDirection(Qt.LeftToRight)
        gridLayout_7.addWidget(self.length_source_field_lbl, 1, 0)

        from qgis.gui import QgsFieldComboBox
        self.length_source_field_cbo = QgsFieldComboBox()
        self.length_source_field_cbo.setFont(self.create_font(10))
        self.length_source_field_cbo.setAllowEmptyFieldName(True)
        gridLayout_7.addWidget(self.length_source_field_cbo, 1, 1)

        self.length_fallback_value_lbl = QLabel("Length fallback value")
        self.length_fallback_value_lbl.setFont(self.create_font(10))
        gridLayout_7.addWidget(self.length_fallback_value_lbl, 1, 2)

        from qgis.PyQt.QtWidgets import QDoubleSpinBox, QSpinBox
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

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(self.create_font(10))

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
        from qgis.PyQt.QtWidgets import QGroupBox
        self.snap_gb = QGroupBox("Snap within:")
        self.snap_gb.setFont(self.create_font(9))
        self.snap_gb.setCheckable(True)
        gridLayout_5 = QGridLayout(self.snap_gb)

        self.snap_dsb = QDoubleSpinBox()
        self.snap_dsb.setFont(self.create_font(10))
        self.snap_dsb.setSuffix(" meters")
        self.snap_dsb.setMaximum(1000000.0)
        self.snap_dsb.setValue(0.1)
        gridLayout_5.addWidget(self.snap_dsb, 0, 0)

        self.gridLayout.addWidget(self.snap_gb, 8, 4, 1, 2)

        # Create vertical spacer
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(verticalSpacer, 9, 5)

        # Create run and close buttons
        gridLayout_6 = QGridLayout()
        gridLayout_6.setContentsMargins(-1, -1, 0, 0)

        self.run_pb = QPushButton("Run")
        self.run_pb.setFont(self.create_font(10, bold=True))
        gridLayout_6.addWidget(self.run_pb, 0, 0)

        self.close_pb = QPushButton("Close")
        self.close_pb.setFont(self.create_font(10))
        gridLayout_6.addWidget(self.close_pb, 0, 1)

        self.gridLayout.addLayout(gridLayout_6, 10, 5)

    def create_font(self, point_size, bold=False):
        font = self.font()
        font.setPointSize(point_size)
        if bold:
            font.setBold(True)
            font.setWeight(75)
        return font

    def setup_models(self):
        self.structure_model = QStandardItemModel()
        self.structure_tv.setModel(self.structure_model)
        self.connection_node_model = QStandardItemModel()
        self.connection_node_tv.setModel(self.connection_node_model)

    def setup_labels(self):
        model_name = self.import_model_cls.__layername__
        self.setWindowTitle(self.windowTitle().format(model_name.lower()))
        self.source_layer_label.setText(self.source_layer_label.text().format(model_name.lower()))
        self.tab_widget.setTabText(0, self.tab_widget.tabText(0).format(model_name))

    def set_source_layer_filter(self):
        self.source_layer_cbo.setFilters(
            QgsMapLayerProxyModel.PointLayer
            if self.import_model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )

    def populate_conversion_settings_widgets(self):
        ImportDialogUtils.create_conversion_settings_widget(self.models, self.data_models_tree_views)
        ImportDialogUtils.connect_configuration_widgets(self.models, self.data_models_tree_views, self.source_layer_cbo, self.uc, self)
        self.on_layer_changed(self.source_layer)

    @property
    def source_layer(self):
        return self.source_layer_cbo.currentLayer()

    @property
    def data_models_tree_views(self):
        return {
            self.import_model_cls: (self.structure_tv, self.structure_model),
            dm.ConnectionNode: (self.connection_node_tv, self.connection_node_model),
        }

    @property
    def models(self):
        return [self.import_model_cls, dm.ConnectionNode]

    @property
    def layer_dependent_widgets(self):
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
    def enable_structures_integration(self):
        return self.import_model_cls in self.HAS_INTEGRATOR

    @property
    def structures_integration_widgets(self):
        return [
            self.edit_channels_cb,
            self.length_source_field_lbl,
            self.length_source_field_cbo,
            self.length_fallback_value_lbl,
            self.length_fallback_value_dsb,
            self.azimuth_source_field_lbl,
            self.azimuth_source_field_cbo,
            self.azimuth_fallback_value_lbl,
            self.azimuth_fallback_value_sb,
        ]

    def on_create_nodes_change(self, is_checked):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
            ImportDialogUtils.activate_widgets(self.layer_dependent_widgets)
        else:
            ImportDialogUtils.deactivate_widgets(self.layer_dependent_widgets)
        source_attribute_widgets = ImportDialogUtils.get_column_widgets(
            self.data_models_tree_views,
            ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX,
            self.import_model_cls)
        for combobox in source_attribute_widgets:
            combobox.clear()
            combobox.addItems(layer_field_names)
            combobox.setCurrentText(combobox.data_model_field_name)
        expression_widgets = ImportDialogUtils.get_column_widgets(
            self.data_models_tree_views,
            ColumnImportIndex.EXPRESSION_COLUMN_IDX,
            self.import_model_cls)
        for expression_widget in expression_widgets:
            expression_widget.setLayer(layer)
        self.length_source_field_cbo.setLayer(None)
        self.azimuth_source_field_cbo.setLayer(None)

    def collect_settings(self):
        return {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
            "conversion_settings": {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "create_connection_nodes": self.create_nodes_cb.isChecked(),
                "length_source_field": self.length_source_field_cbo.currentField(),
                "length_fallback_value": self.length_fallback_value_dsb.value(),
                "azimuth_source_field": self.azimuth_source_field_cbo.currentField(),
                "azimuth_fallback_value": self.azimuth_fallback_value_sb.value(),
                "edit_channels": self.edit_channels_cb.isChecked(),
            },
            "connection_node_fields" : self.collect_fields_settings(dm.ConnectionNode)
        }

    def source_fields_missing(self):
        data_models = [self.import_model_cls]
        if self.create_nodes_cb.isChecked():
            data_models.append(dm.ConnectionNode)
        return self.source_fields_missing_for_models(*data_models)

    def save_import_settings(self):
        ImportDialogUtils.save_import_settings(import_settings=self.collect_settings(),
                                               uc=self.uc,
                                               parent=self)

    def load_import_settings(self):
        self.reset_settings_widget()
        try:
            with open(template_filepath, "r") as template_file:
                import_settings = json.loads(template_file.read())
            tree_view, tree_view_model = self.data_models_tree_views[self.import_model_cls]
            ImportDialogUtils.update_fields_settings(tree_view, tree_view_model, self.import_model_cls, import_settings["fields"])
            self.load_conversion_settings(import_settings)
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def load_conversion_settings(self, import_settings):
        conversion_settings = import_settings["conversion_settings"]
        self.snap_gb.setChecked(conversion_settings.get("use_snapping", True))
        self.snap_dsb.setValue(conversion_settings.get("snapping_distance", 0.1))
        self.create_nodes_cb.setChecked(conversion_settings.get("create_connection_nodes", True))
        self.edit_channels_cb.setChecked(conversion_settings.get("edit_channels", False))
        self.length_source_field_cbo.setField(conversion_settings.get("length_source_field", ""))
        self.length_fallback_value_dsb.setValue(conversion_settings.get("length_fallback_value", 1.0))
        self.azimuth_source_field_cbo.setField(conversion_settings.get("azimuth_source_field", ""))
        self.azimuth_fallback_value_sb.setValue(conversion_settings.get("azimuth_fallback_value", 90))
        self.update_fields_settings(self.import_model_cls, import_settings["fields"])
        try:
            connection_node_fields = import_settings["connection_node_fields"]
            self.update_fields_settings(dm.ConnectionNode, connection_node_fields)
        except KeyError:
            pass

    def run_import(self):
        if self.source_fields_missing():
            return
        handlers, layers = self.prepare_import()
        selected_feat_ids = source_layer.selectedFeatureIds() if self.selected_only_cb.isChecked() else None
        ImportDialogUtils.import_settings(import_settings=self.collect_settings(),
                                          model_gpkg=self.model_gpkg,
                                          source_layer=self.source_layer,
                                          selected_feat_ids=selected_feat_ids,
                                          importer_cls=ImportDialogUtils.IMPORTERS[self.import_model_cls],
                                          uc=self.uc,
                                          handlers=handlers,
                                          layers=layers)

    def prepare_import(self):
        structures_handler = self.layer_manager.model_handlers[self.import_model_cls]
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
        structure_layer = structures_handler.layer
        node_layer = node_handler.layer
        channel_layer = channel_handler.layer
        cross_section_location_layer = cross_section_location_handler.layer
        import_settings = self.collect_settings()
        edit_channels = import_settings["conversion_settings"].get("edit_channels", False)
        processed_handlers = [structures_handler, node_handler]
        processed_layers = {"structure_layer": structure_layer, "node_layer": node_layer}
        if edit_channels:
            processed_handlers += [channel_handler, cross_section_location_handler]
            processed_layers["channel_layer"] = channel_layer
            processed_layers["cross_section_location_layer"] = cross_section_location_layer
        return processed_handlers, processed_layers
