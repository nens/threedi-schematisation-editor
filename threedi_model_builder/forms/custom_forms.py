import threedi_model_builder.data_models as dm
from threedi_model_builder.utils import find_point_node, find_linestring_nodes
from collections import defaultdict
from enum import Enum
from types import MappingProxyType
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QSpinBox,
)

from qgis.core import NULL, QgsGeometry
from qgis.gui import QgsDoubleSpinBox, QgsSpinBox

field_types_widgets = {
    bool: QCheckBox,
    int: QgsSpinBox,
    float: QgsDoubleSpinBox,
    str: QLineEdit,
}


class BaseEditForm(QObject):
    """Base edit form for user layers edit form logic."""

    MODEL = None
    FOREIGN_MODEL_FIELDS = MappingProxyType({})

    def __init__(self, layer_manager, dialog, layer, feature):
        super(BaseEditForm, self).__init__(parent=dialog)  # We need to set dialog as a parent to keep form alive
        self.layer_manager = layer_manager
        self.iface = layer_manager.iface
        self.uc = layer_manager.uc
        self.dialog = dialog
        self.layer = layer
        self.feature = feature
        self.new_feature = False
        self.model_widgets = defaultdict(list)  # {data_model_cls: list of tuples (widget, layer field name)}
        self.name_to_widget = {}
        self.foreign_widgets = {}
        self.set_foreign_widgets()
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)

    def set_foreign_widgets(self):
        for foreign_widget_name in self.FOREIGN_MODEL_FIELDS.keys():
            foreign_widget = self.dialog.findChild(QObject, foreign_widget_name)
            self.foreign_widgets[foreign_widget_name] = foreign_widget

    def setup_form_widgets(self):
        if self.feature is None:
            return
        if self.feature.id() < 0:
            geometry = self.feature.geometry()
            if not geometry:
                return  # form open for an invalid feature
            else:
                self.new_feature = True
        self.populate_widgets()
        self.populate_extra_widgets()
        self.toggle_edit_mode()

    def toggle_edit_mode(self):
        editing_active = self.layer.isEditable()
        for widget in self.foreign_widgets.values():
            widget.setEnabled(editing_active)

    def populate_widgets(self, data_model_cls=None, feature=None, start_end_modifier=None):
        """
        Populate form's widgets - widgets are named after their attributes in the data model.
        If data_model_cls is given, then populate widgets for this class and feature.
        start_end_modifier is used when there are multiple features edited in the form, for example two manholes in
        a pipe form. The modifier should be 1 for starting point and 2 for ending.
        """

        if data_model_cls is not None:
            field_name_prefix = data_model_cls.__tablename__ + "_"
            if start_end_modifier is not None:
                field_name_prefix += str(start_end_modifier) + "_"
        else:
            data_model_cls = self.MODEL
            feature = self.feature
            field_name_prefix = ""
        for field_name, field_type in data_model_cls.__annotations__.items():
            widget_name = field_name_prefix + field_name
            widget = self.dialog.findChild(QObject, widget_name)
            if widget is None:
                # the filed might not be shown in the form
                continue
            if issubclass(field_type, Enum):
                cbo_items = {t.name: t.value for t in field_type}
                self.populate_combo(widget, cbo_items)
            self.set_widget_value(widget, feature[field_name], var_type=field_type)
            self.model_widgets[data_model_cls].append((widget, field_name))
            self.name_to_widget[widget.objectName()] = widget

    @staticmethod
    def populate_combo(combo_widget, value_map):
        """Populates combo box with value map items (map key = displayed text, map value = data)."""
        combo_widget.clear()
        combo_widget.addItem("", None)
        for text, data in value_map.items():
            combo_widget.addItem(text, data)

    def set_widget_value(self, widget, value, var_type=None):
        if isinstance(widget, QLineEdit):
            widget.setText(str(value))
            widget.setCursorPosition(0)
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, (QgsSpinBox, QSpinBox, QgsDoubleSpinBox, QDoubleSpinBox)):
            if value not in (None, NULL):
                value = var_type(value) if var_type is not None else value
                widget.setValue(value)
            else:
                if isinstance(widget, (QgsSpinBox, QgsDoubleSpinBox)):
                    widget.setClearValueMode(widget.__class__.CustomValue, "")
                widget.clear()
        elif isinstance(widget, QComboBox):
            item_idx = widget.findData(value)
            if item_idx >= 0:
                widget.setCurrentIndex(item_idx)
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")

    def get_widget_value(self, widget, var_type=None):
        if isinstance(widget, QLineEdit):
            value = var_type(widget.text())
        elif isinstance(widget, QCheckBox):
            value = var_type(widget.isChecked())
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = var_type(widget.value()) if var_type is not None else widget.value()
        elif isinstance(widget, QComboBox):
            value = widget.currentData()
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            value = None
        return value

    def populate_extra_widgets(self):
        raise NotImplementedError()


class ConnectionNodeEditForm(BaseEditForm):
    """Connection node edit form logic."""
    MODEL = dm.ConnectionNode

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""


class ManholeEditForm(BaseEditForm):
    """Manhole user layer edit form logic."""
    MODEL = dm.Manhole
    FOREIGN_MODEL_FIELDS = MappingProxyType(
        {
            "connection_node_initial_waterlevel": dm.ConnectionNode,
            "connection_node_storage_area": dm.ConnectionNode,
            "connection_node_code": dm.ConnectionNode,
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        if self.new_feature is True:
            connection_node_feat = find_point_node(self.feature.geometry().asPoint(), connection_node_layer)
            if connection_node_feat is None:
                connection_node_feat = connection_node_handler.create_new_feature(self.feature.geometry())
                self.feature["connection_node_id"] = connection_node_feat["id"]
                connection_node_layer.addFeature(connection_node_feat)
                self.populate_widgets()
        else:
            connection_node_feat = connection_node_handler.get_feat_by_id(self.feature["connection_node_id"])

        if connection_node_feat is not None:
            self.populate_widgets(data_model_cls=dm.ConnectionNode, feature=connection_node_feat)


class PipeEditForm(BaseEditForm):
    """Pipe user layer edit form logic."""

    MODEL = dm.Pipe
    FOREIGN_MODEL_FIELDS = MappingProxyType(
        {
            "connection_node_1_id": dm.ConnectionNode,
            "connection_node_1_initial_waterlevel": dm.ConnectionNode,
            "connection_node_1_storage_area": dm.ConnectionNode,
            "connection_node_1_code": dm.ConnectionNode,
            "connection_node_2_id": dm.ConnectionNode,
            "connection_node_2_initial_waterlevel": dm.ConnectionNode,
            "connection_node_2_storage_area": dm.ConnectionNode,
            "connection_node_2_code": dm.ConnectionNode,
            "manhole_1_id": dm.Manhole,
            "manhole_1_code": dm.Manhole,
            "manhole_1_display_name": dm.Manhole,
            "manhole_1_calculation_type": dm.Manhole,
            "manhole_1_shape": dm.Manhole,
            "manhole_1_width": dm.Manhole,
            "manhole_1_length": dm.Manhole,
            "manhole_1_bottom_level": dm.Manhole,
            "manhole_1_surface_level": dm.Manhole,
            "manhole_1_drain_level": dm.Manhole,
            "manhole_1_manhole_indicator": dm.Manhole,
            "manhole_1_zoom_category": dm.Manhole,
            "manhole_2_id": dm.Manhole,
            "manhole_2_code": dm.Manhole,
            "manhole_2_display_name": dm.Manhole,
            "manhole_2_calculation_type": dm.Manhole,
            "manhole_2_shape": dm.Manhole,
            "manhole_2_width": dm.Manhole,
            "manhole_2_length": dm.Manhole,
            "manhole_2_bottom_level": dm.Manhole,
            "manhole_2_surface_level": dm.Manhole,
            "manhole_2_drain_level": dm.Manhole,
            "manhole_2_manhole_indicator": dm.Manhole,
            "manhole_2_zoom_category": dm.Manhole,
            "cross_section_definition_shape": dm.CrossSectionDefinition,
            "cross_section_definition_width": dm.CrossSectionDefinition,
            "cross_section_definition_height": dm.CrossSectionDefinition,
            "cross_section_definition_code": dm.CrossSectionDefinition,
        }
    )

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.new_feature is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_manholes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_manholes_on_edit()

    def populate_cross_section_definition_on_edit(self):
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_feat = cross_section_def_handler.get_feat_by_id(self.feature["cross_section_definition_id"])
        if cross_section_def_feat is not None:
            self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)

    def populate_cross_section_definition_on_creation(self):
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_layer = cross_section_def_handler.layer
        cross_section_def_feat = cross_section_def_handler.create_new_feature()
        self.feature["cross_section_definition_id"] = cross_section_def_feat["id"]
        if not cross_section_def_layer.isEditable():
            # TODO: We need to add automatic saving of definition
            cross_section_def_layer.startEditing()
        cross_section_def_layer.addFeature(cross_section_def_feat)
        self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)

    def populate_manholes_on_edit(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pipe_iterable = (("start", 1), ("end", 2))
        for name, modifier in pipe_iterable:
            connection_node_id = self.feature[f"connection_node_{name}_id"]
            if connection_node_id:
                connection_node_feat = connection_node_handler.get_feat_by_id(connection_node_id)
                manhole_feat = connection_node_handler.get_manhole_feat_for_node_id(connection_node_id)
                if manhole_feat is not None:
                    self.populate_widgets(
                        data_model_cls=dm.ConnectionNode,
                        feature=connection_node_feat,
                        start_end_modifier=modifier,
                    )
                    self.populate_widgets(
                        data_model_cls=dm.Manhole,
                        feature=manhole_feat,
                        start_end_modifier=modifier,
                    )

    def populate_manholes_on_creation(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        manhole_handler = self.layer_manager.model_handlers[dm.Manhole]
        connection_node_layer = connection_node_handler.layer
        manhole_layer = manhole_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_manhole_feat, end_manhole_feat = find_linestring_nodes(linestring, manhole_layer)
        pipe_iterable = (
            ("start", 1, start_point, start_manhole_feat),
            ("end", 2, end_point, end_manhole_feat)
        )
        for name, modifier, manhole_point, manhole_feat in pipe_iterable:
            if manhole_feat is None:
                point_geom = QgsGeometry.fromPointXY(manhole_point)
                manhole_feat, connection_node_feat = manhole_handler.create_manhole_with_connection_node(point_geom)
                connection_node_id = connection_node_feat["id"]
                connection_node_layer.addFeature(connection_node_feat)
                manhole_layer.addFeature(manhole_feat)
            else:
                connection_node_id = manhole_feat["connection_node_id"]
                connection_node_feat = connection_node_handler.get_feat_by_id(connection_node_id)

            self.feature[f"connection_node_{name}_id"] = connection_node_id
            self.populate_widgets(
                data_model_cls=dm.ConnectionNode,
                feature=connection_node_feat,
                start_end_modifier=modifier,
            )
            self.populate_widgets(
                data_model_cls=dm.Manhole,
                feature=manhole_feat,
                start_end_modifier=modifier,
                )
        self.populate_widgets()


ALL_FORMS = (
    ConnectionNodeEditForm,
    ManholeEditForm,
    PipeEditForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
