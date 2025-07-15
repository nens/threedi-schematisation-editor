import json
import os
from functools import partial, cached_property

from qgis.core import QgsMapLayerProxyModel, QgsSettings
from qgis.gui import QgsFieldExpressionWidget
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import QComboBox, QLineEdit
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
from threedi_schematisation_editor.vector_data_importer.dialogs import if_basecls, if_uicls, is_basecls, is_uicls
from threedi_schematisation_editor.vector_data_importer.dialogs.utils import CatchThreediWarnings, ImportFieldMappingUtils, \
    ColumnImportIndex


class ImportDialog:

    IMPORTERS = {
        dm.ConnectionNode: ConnectionNodesImporter,
        dm.Culvert: CulvertsImporter,
        dm.Orifice: OrificesImporter,
        dm.Weir: WeirsImporter,
        dm.Pipe: PipesImporter,
    }

    def __init__(self, basecls, uicls, import_model_cls, model_gpkg, layer_manager, uc, parent=None):
        basecls.__init__(self)
        uicls.__init__(self, parent)
        self.setupUi(self)
        self.import_model_cls = import_model_cls
        self.model_gpkg = model_gpkg
        self.layer_manager = layer_manager
        self.uc = uc
        self.set_source_layer_filter()
        self.setup_models()
        self.populate_conversion_settings_widgets()
        self.source_layer_cbo.setCurrentIndex(0)
        self.source_layer_cbo.layerChanged.connect(self.on_layer_changed)
        self.save_pb.clicked.connect(self.save_import_settings)
        self.load_pb.clicked.connect(self.load_import_settings)
        self.run_pb.clicked.connect(self.run_import)
        self.close_pb.clicked.connect(self.close)
        self.setup_labels()

    def set_source_layer_filter(self):
        raise NotImplementedError

    def setup_models(self):
        raise NotImplementedError

    def populate_converstion_settings_widgets(self):
        raise NotImplementedError

    @property
    def models(self):
        raise NotImplementedError

    @property
    def data_models_tree_views(self):
        raise NotImplementedError

    def load_settings_from_file(self, template_filepath):
        raise NotImplementedError

    def setup_labels(self):
        model_name = self.import_model_cls.__layername__
        self.setWindowTitle(self.windowTitle().format(model_name.lower()))
        self.source_layer_label.setText(self.source_layer_label.text().format(model_name.lower()))
        self.tab_widget.setTabText(0, self.tab_widget.tabText(0).format(model_name))

    @staticmethod
    def is_obsolete_field(model_cls, field_name):
        return field_name in model_cls.obsolete_fields()

    @property
    def source_layer(self):
        return self.source_layer_cbo.currentLayer()

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

    def activate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setEnabled(True)

    def deactivate_layer_dependent_widgets(self):
        for widget in self.layer_dependent_widgets:
            widget.setDisabled(True)

    def collect_settings(self):
        import_settings = {
            "target_layer": self.import_model_cls.__tablename__,
            "fields": self.collect_fields_settings(self.import_model_cls),
        }
        return import_settings

    @property
    def extra_settings_loaders(self):
        return []

    def load_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(
            self, extension_filter, save=False, default_settings_entry=ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY
        )
        if not template_filepath:
            return
        settings = QgsSettings()
        settings.setValue(ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY, os.path.dirname(template_filepath))
        self.reset_settings_widget()
        try:
            with open(template_filepath, "r") as template_file:
                import_settings = json.loads(template_file.read())
            self.update_fields_settings(self.import_model_cls, import_settings["fields"])
            for func in self.extra_settings_loaders:
                func(import_settings)
            self.uc.show_info(f"Settings loaded from the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def save_import_settings(self):
        extension_filter = "JSON (*.json)"
        template_filepath = get_filepath(
            self, extension_filter, default_settings_entry=ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY
        )
        if not template_filepath:
            return
        settings = QgsSettings()
        settings.setValue(ImportFieldMappingUtils.LAST_CONFIG_DIR_ENTRY, os.path.dirname(template_filepath))
        try:
            import_settings = self.collect_settings()
            with open(template_filepath, "w") as template_file:
                json.dump(import_settings, template_file, indent=2)
            self.uc.show_info(f"Settings saved to the template.", self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)

    def get_column_widgets(self, column_idx, data_model):
        model_widgets = []
        if data_model not in self.data_models_tree_views:
            return model_widgets
        tree_view, tree_view_model = self.data_models_tree_views[data_model]
        row_idx = 0
        for field_name in data_model.__annotations__.keys():
            if self.is_obsolete_field(data_model, field_name):
                continue
            item = tree_view_model.item(row_idx, column_idx)
            index = item.index()
            widget = tree_view.indexWidget(index)
            widget.data_model_field_name = field_name
            model_widgets.append(widget)
            row_idx += 1
        return model_widgets

    def on_layer_changed(self, layer):
        layer_field_names = [""]
        if layer:
            layer_field_names += [field.name() for field in layer.fields()]
            self.activate_layer_dependent_widgets()
        else:
            self.deactivate_layer_dependent_widgets()
        source_attribute_widgets = self.get_column_widgets(
            ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX, self.import_model_cls)
        for combobox in source_attribute_widgets:
            combobox.clear()
            combobox.addItems(layer_field_names)
            combobox.setCurrentText(combobox.data_model_field_name)
        expression_widgets = self.get_column_widgets(ColumnImportIndex.EXPRESSION_COLUMN_IDX, self.import_model_cls)
        for expression_widget in expression_widgets:
            expression_widget.setLayer(layer)

    def populate_conversion_settings_widgets(self):
        widgets_to_add = create_widgets(*self.models)
        for model_cls in self.models:
            model_widgets = widgets_to_add[model_cls]
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            tree_view_model.clear()
            tree_view_model.setHorizontalHeaderLabels(CONFIG_HEADER)
            for (row_idx, column_idx), widget in model_widgets.items():
                tree_view_model.setItem(row_idx, column_idx, QStandardItem(""))
                tree_view.setIndexWidget(tree_view_model.index(row_idx, column_idx), widget)
            for i in range(len(CONFIG_HEADER)):
                tree_view.resizeColumnToContents(i)
        self.connect_configuration_widgets()
        self.on_layer_changed(self.source_layer)

    def reset_settings_widget(self):
        # Iterate over all settings widgets are stored in the data_models_tree_views
        for tree_view, tree_view_model in self.data_models_tree_views.values():
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

    def connect_configuration_widgets(self):
        data_models = [self.import_model_cls, dm.ConnectionNode]
        for model_cls in data_models:
            tree_view, tree_view_model = self.data_models_tree_views[model_cls]
            row_idx = 0
            for field_name in model_cls.__annotations__.keys():
                if self.is_obsolete_field(model_cls, field_name):
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
                        self.source_layer_cbo,
                        source_attribute_combobox,
                        value_map_button,
                        self.uc,
                        self,
                    )
                )
                row_idx += 1

    def collect_fields_settings(self, model_cls):
        fields_settings = {}
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(model_cls, field_name):
                continue
            single_field_config = {}
            field_type = core_field_type(field_type)
            for column_idx, key_name in enumerate(CONFIG_KEYS, start=1):
                item = tree_view_model.item(row_idx, column_idx)
                index = item.index()
                widget = tree_view.indexWidget(index)
                key_value = ImportFieldMappingUtils.collect_config_from_widget(widget, key_name, field_type, column_idx)
                if key_value is None:
                    continue
                single_field_config[key_name] = key_value
            fields_settings[field_name] = single_field_config
            row_idx += 1
        return fields_settings

    def update_fields_settings(self, model_cls, fields_setting):
        tree_view, tree_view_model = self.data_models_tree_views[model_cls]
        row_idx = 0
        for field_name, field_type in model_cls.__annotations__.items():
            if self.is_obsolete_field(model_cls, field_name):
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

    def source_fields_missing_for_models(self, *data_models):
        missing_fields_lines = []
        for model_cls in data_models:
            missing_fields = self.missing_source_fields(model_cls)
            model_name = model_cls.__layername__
            missing_fields_lines += [f"{model_name}: {missing_field}" for missing_field in missing_fields]
        if missing_fields_lines:
            missing_fields_txt = "\n".join(missing_fields_lines)
            self.uc.show_warn(
                f"Please specify a source field for a following attribute(s) and try again:\n{missing_fields_txt}", self
            )
            return True
        return False

    def missing_source_fields(self, model_cls):
        field_labels = self.get_column_widgets(ColumnImportIndex.FIELD_NAME_COLUMN_IDX, model_cls)
        method_widgets = self.get_column_widgets(ColumnImportIndex.METHOD_COLUMN_IDX, model_cls)
        source_attribute_widgets = self.get_column_widgets(ColumnImportIndex.SOURCE_ATTRIBUTE_COLUMN_IDX, model_cls)
        missing_fields = []
        for field_lbl, method_cbo, source_attribute_cbo in zip(field_labels, method_widgets, source_attribute_widgets):
            field_name, method_txt, source_attribute_txt = (
                field_lbl.text().strip(),
                method_cbo.currentText(),
                source_attribute_cbo.currentText(),
            )
            if method_txt == str(ColumnImportMethod.ATTRIBUTE) and not source_attribute_txt:
                missing_fields.append(field_name)
        return missing_fields

    def source_fields_missing(self):
        raise NotImplementedError

    def prepare_import(self):
        raise NotImplementedError

    def run_import(self):
        if self.source_fields_missing():
            return
        handlers, layers = self.prepare_import()
        source_layer = self.source_layer
        selected_feat_ids = source_layer.selectedFeatureIds() if self.selected_only_cb.isChecked() else None
        importer_cls = self.IMPORTERS[self.import_model_cls]
        import_settings = self.collect_settings()
        try:
            for handler in handlers:
                handler.disconnect_handler_signals()
            structures_importer = importer_cls(
                source_layer,
                self.model_gpkg,
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
            self.uc.show_info(success_msg, self)
        except Exception as e:
            self.uc.show_error(f"Import failed due to the following error:\n{e}", self)
        finally:
            for handler in handlers:
                handler.connect_handler_signals()
        for layer in layers.values():
            layer.triggerRepaint()


class ImportFeaturesDialog(ImportDialog, if_basecls, if_uicls):

    def __init__(self, import_model_cls, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(if_basecls, if_uicls, import_model_cls, model_gpkg, layer_manager, uc, parent)

    def setup_models(self):
        self.field_map_model = QStandardItemModel()
        self.field_map_tv.setModel(self.field_map_model)

    @property
    def data_models_tree_views(self):
        return {self.import_model_cls : (self.field_map_tv, self.field_map_model)}

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

    @property
    def models(self):
        return [self.import_model_cls]

    def source_fields_missing(self):
        return self.source_fields_missing_for_models(self.import_model_cls)

    def prepare_import(self):
        return [], {}


class ImportStructuresDialog(ImportDialog, is_basecls, is_uicls):
    """Dialog for the importing structures tool."""

    HAS_INTEGRATOR = [dm.Culvert, dm.Orifice, dm.Weir]

    def __init__(self, import_model_cls, model_gpkg, layer_manager, uc, parent=None):
        super().__init__(is_basecls, is_uicls, import_model_cls, model_gpkg, layer_manager, uc, parent)
        self.create_nodes_cb.stateChanged.connect(self.on_create_nodes_change)
        if not self.enable_structures_integration:
            for widget in self.structures_integration_widgets:
                widget.hide()

    def setup_models(self):
        self.structure_model = QStandardItemModel()
        self.structure_tv.setModel(self.structure_model)
        self.connection_node_model = QStandardItemModel()
        self.connection_node_tv.setModel(self.connection_node_model)

    @property
    def data_models_tree_views(self):
        return {
            self.import_model_cls: (self.structure_tv, self.structure_model),
            dm.ConnectionNode: (self.connection_node_tv, self.connection_node_model),
        }

    def set_source_layer_filter(self):
        self.source_layer_cbo.setFilters(
            QgsMapLayerProxyModel.PointLayer
            if self.import_model_cls.__geometrytype__ == dm.GeometryType.Point
            else QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer
        )

    @cached_property
    def enable_structures_integration(self):
        return self.structure_model_cls in self.HAS_INTEGRATOR

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

    @property
    def layer_dependent_widgets(self):
        widgets = super().layer_dependent_widgets + [self.create_nodes_cb, self.snap_gb,]
        if self.enable_structures_integration:
            widgets += self.structures_integration_widgets
        return widgets

    def on_create_nodes_change(self, is_checked):
        self.connection_node_tab.setEnabled(is_checked)

    def on_layer_changed(self, layer):
        super().on_layer_changed(layer)
        self.length_source_field_cbo.setLayer(None)
        self.azimuth_source_field_cbo.setLayer(None)

    @property
    def models(self):
        return [self.import_model_cls, dm.ConnectionNode]

    def collect_settings(self):
        import_settings = super().collect_settings()
        import_settings["conversion_settings"] = {
                "use_snapping": self.snap_gb.isChecked(),
                "snapping_distance": self.snap_dsb.value(),
                "create_connection_nodes": self.create_nodes_cb.isChecked(),
                "length_source_field": self.length_source_field_cbo.currentField(),
                "length_fallback_value": self.length_fallback_value_dsb.value(),
                "azimuth_source_field": self.azimuth_source_field_cbo.currentField(),
                "azimuth_fallback_value": self.azimuth_fallback_value_sb.value(),
                "edit_channels": self.edit_channels_cb.isChecked(),
            }
        import_settings["connection_node_fields"] = self.collect_fields_settings(dm.ConnectionNode)
        return import_settings

    @property
    def extra_settings_loaders(self):
        return [self.load_conversion_settings]

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

    def source_fields_missing(self):
        data_models = [self.import_model_cls]
        if self.create_nodes_cb.isChecked():
            data_models.append(dm.ConnectionNode)
        return self.source_fields_missing_for_models(*data_models)

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


