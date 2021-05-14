import threedi_model_builder.data_models as dm
import threedi_model_builder.enumerators as en
from threedi_model_builder.utils import find_point_node, find_linestring_nodes, connect_signal
from functools import partial
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

field_types_widgets = MappingProxyType(
    {
        bool: QCheckBox,
        int: QgsSpinBox,
        float: QgsDoubleSpinBox,
        str: QLineEdit,
    }
)


class BaseForm(QObject):
    """Base edit form for user layers edit form logic."""

    MODEL = None

    def __init__(self, layer_manager, dialog, layer, feature):
        super().__init__(parent=dialog)  # We need to set dialog as a parent to keep form alive
        self.layer_manager = layer_manager
        self.iface = layer_manager.iface
        self.uc = layer_manager.uc
        self.dialog = dialog
        self.layer = layer
        self.handler = self.layer_manager.model_handlers[self.MODEL]
        self.feature = feature
        self.creation = False
        self.main_widgets = {}
        self.foreign_widgets = {}
        self.foreign_models_features = {}
        self.connected_signals = set()
        self.set_foreign_widgets()
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)

    def setup_form_widgets(self):
        if self.feature is None:
            return
        if self.feature.id() < 0:
            geometry = self.feature.geometry()
            if not geometry:
                return  # form open for an invalid feature
            else:
                self.creation = True
                self.handler.set_feature_values(self.feature)
        self.populate_widgets()
        self.populate_extra_widgets()
        self.toggle_edit_mode()
        self.connect_foreign_widgets()

    def set_foreign_widgets(self):
        main_fields = set(self.MODEL.__annotations__.keys())
        for related_cls, relations_number in self.handler.RELATED_MODELS.items():
            table_name = related_cls.__tablename__
            for related_number in range(1, relations_number + 1):
                if relations_number > 1:
                    numerical_modifier = related_number
                    str_num_mod = f"_{related_number}"
                else:
                    numerical_modifier = None
                    str_num_mod = ""
                for field_name in related_cls.__annotations__.keys():
                    widget_name = f"{table_name}{str_num_mod}_{field_name}"
                    if widget_name in main_fields:
                        continue
                    widget = self.dialog.findChild(QObject, widget_name)
                    if widget is None:
                        continue
                    self.foreign_widgets[widget_name] = (widget, related_cls, numerical_modifier, field_name)

    def toggle_edit_mode(self):
        editing_active = self.layer.isEditable()
        for widget, related_cls, numerical_modifier, field_name in self.foreign_widgets.values():
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
                cbo_items = {t.name.capitalize().replace("_", " "): t.value for t in field_type}
                self.populate_combo(widget, cbo_items)
            self.set_widget_value(widget, feature[field_name], var_type=field_type)
            self.main_widgets[widget.objectName()] = widget

    @staticmethod
    def populate_combo(combo_widget, value_map):
        """Populates combo box with value map items (map key = displayed text, map value = data)."""
        combo_widget.clear()
        combo_widget.addItem("", None)
        for text, data in value_map.items():
            combo_widget.addItem(text, data)

    def set_widget_value(self, widget, value, var_type=None):
        if isinstance(widget, QLineEdit):
            widget.setText(str(value) if value is not None else "")
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

    def get_widget_value(self, widget):
        if isinstance(widget, QLineEdit):
            value = widget.text()
        elif isinstance(widget, QCheckBox):
            value = widget.isChecked()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = widget.value()
        elif isinstance(widget, QComboBox):
            value = widget.currentData()
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            value = None
        return value

    def get_widget_editing_signal(self, widget):
        if isinstance(widget, QLineEdit):
            signal = widget.textChanged
        elif isinstance(widget, QCheckBox):
            signal = widget.stateChanged
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            signal = widget.valueChanged
        elif isinstance(widget, QComboBox):
            signal = widget.currentIndexChanged
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            signal = None
        return signal

    def set_value_from_widget(self, widget, feature, model_cls, field_name):
        if feature:
            value = self.get_widget_value(widget)
            handler = self.layer_manager.model_handlers[model_cls]
            feature[field_name] = value
            handler.layer.updateFeature(feature)

    def connect_foreign_widgets(self):
        """Connect widgets for other layers attributes."""
        for widget_name, (widget, model_cls, numerical_modifier, field_name) in self.foreign_widgets.items():
            signal = self.get_widget_editing_signal(widget)
            try:
                feature = self.foreign_models_features[model_cls, numerical_modifier]
            except KeyError:
                continue
            slot = partial(self.set_value_from_widget, widget, feature, model_cls, field_name)
            connect_signal(signal, slot)
            self.connected_signals.add((signal, slot))

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        pass


class FormWithNode(BaseForm):
    """Base edit form for user layers with a single connection node."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.connection_node = None
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node,
        }

    def populate_connection_node(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        if self.creation is True:
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
            self.connection_node = connection_node_feat


class FormWithStartEndNode(BaseForm):
    """Base edit form for user layers start and end connection nodes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.connection_node_start = None
        self.connection_node_end = None
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
        }

    def populate_connection_nodes_on_creation(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, connection_node_layer)
        if start_connection_node_feat is not None and end_connection_node_feat is None:
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                start_connection_node_feat, geometry=end_geom)
            connection_node_layer.addFeature(end_connection_node_feat)
        elif start_connection_node_feat is None and end_connection_node_feat is not None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                end_connection_node_feat, geometry=start_geom)
            connection_node_layer.addFeature(start_connection_node_feat)
        elif start_connection_node_feat is None and end_connection_node_feat is None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_connection_node_feat = connection_node_handler.create_new_feature(geometry=start_geom)
            connection_node_layer.addFeature(start_connection_node_feat)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_connection_node_feat = connection_node_handler.create_new_feature(geometry=end_geom)
            connection_node_layer.addFeature(end_connection_node_feat)

        # Set feature specific attributes
        code_display_name = f"{start_connection_node_feat['code']}-{end_connection_node_feat['code']}"
        self.feature["connection_node_start_id"] = start_connection_node_feat["id"]
        self.feature["connection_node_end_id"] = end_connection_node_feat["id"]
        self.feature["code"] = code_display_name
        self.feature["display_name"] = code_display_name
        # Assign features as an form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat

        # Populate widgets based on features attributes
        node_iterable = (
            (1, start_connection_node_feat),
            (2, end_connection_node_feat),
        )
        for modifier, connection_node_feat in node_iterable:
            self.populate_widgets(
                data_model_cls=dm.ConnectionNode,
                feature=connection_node_feat,
                start_end_modifier=modifier,
            )
        self.populate_widgets()

    def populate_connection_nodes_on_edit(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        node_iterable = (("start", 1), ("end", 2))
        for name, modifier in node_iterable:
            connection_node_id = self.feature[f"connection_node_{name}_id"]
            if connection_node_id:
                connection_node_feat = connection_node_handler.get_feat_by_id(connection_node_id)
                if modifier == 1:
                    self.connection_node_start = connection_node_feat
                else:
                    self.connection_node_end = connection_node_feat
                if connection_node_feat is not None:
                    self.populate_widgets(
                        data_model_cls=dm.ConnectionNode,
                        feature=connection_node_feat,
                        start_end_modifier=modifier,
                    )

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_connection_nodes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_connection_nodes_on_edit()


class FormWithCSDefinition(BaseForm):
    """Base edit form for user layers with Cross Section Definition."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.cross_section_definition = None
        self.foreign_models_features = {
            (dm.CrossSectionDefinition, 1):  self.cross_section_definition,
        }

    def populate_cross_section_definition_on_edit(self):
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_feat = cross_section_def_handler.get_feat_by_id(self.feature["cross_section_definition_id"])
        if cross_section_def_feat is not None:
            self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)
            self.cross_section_definition = cross_section_def_feat

    def populate_cross_section_definition_on_creation(self):
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_layer = cross_section_def_handler.layer
        cross_section_def_feat = cross_section_def_handler.create_new_feature()
        if not cross_section_def_layer.isEditable():
            cross_section_def_layer.startEditing()
        if self.MODEL == dm.Weir:
            cross_section_def_feat["shape"] = en.CrossSectionShape.RECTANGLE.value
        cross_section_def_layer.addFeature(cross_section_def_feat)
        self.feature["cross_section_definition_id"] = cross_section_def_feat["id"]
        self.populate_widgets(data_model_cls=dm.CrossSectionDefinition, feature=cross_section_def_feat)
        self.cross_section_definition = cross_section_def_feat


class ConnectionNodeForm(BaseForm):
    """Connection node edit form logic."""
    MODEL = dm.ConnectionNode


class ManholeForm(FormWithNode):
    """Manhole user layer edit form logic."""
    MODEL = dm.Manhole

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        self.populate_connection_node()


class PipeForm(FormWithCSDefinition, FormWithStartEndNode):
    """Pipe user layer edit form logic."""

    MODEL = dm.Pipe

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.manhole_start = None
        self.manhole_end = None
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.Manhole, 1): self.manhole_start,
            (dm.Manhole, 2): self.manhole_end,
            (dm.CrossSectionDefinition, 1): self.cross_section_definition,
        }

    def populate_manholes_on_edit(self):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pipe_iterable = (("start", 1), ("end", 2))
        for name, modifier in pipe_iterable:
            connection_node_id = self.feature[f"connection_node_{name}_id"]
            if connection_node_id:
                connection_node_feat = connection_node_handler.get_feat_by_id(connection_node_id)
                manhole_feat = connection_node_handler.get_manhole_feat_for_node_id(connection_node_id)
                if modifier == 1:
                    self.connection_node_start = connection_node_feat
                    self.manhole_start = manhole_feat
                else:
                    self.connection_node_end = connection_node_feat
                    self.manhole_end = manhole_feat
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
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        if not manhole_layer.isEditable():
            manhole_layer.startEditing()
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_manhole_feat, end_manhole_feat = find_linestring_nodes(linestring, manhole_layer)
        if start_manhole_feat is not None and end_manhole_feat is None:
            start_connection_node_id = start_manhole_feat["connection_node_id"]
            start_connection_node_feat = connection_node_handler.get_feat_by_id(start_connection_node_id)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_manhole_feat, end_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                end_geom, template_feat=start_manhole_feat)
            end_connection_node_id = end_connection_node_feat["id"]
            connection_node_layer.addFeature(end_connection_node_feat)
            manhole_layer.addFeature(end_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is not None:
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom, template_feat=end_manhole_feat)
            start_connection_node_id = start_connection_node_feat["id"]
            connection_node_layer.addFeature(start_connection_node_feat)
            manhole_layer.addFeature(start_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom)
            start_connection_node_id = start_connection_node_feat["id"]
            connection_node_layer.addFeature(start_connection_node_feat)
            manhole_layer.addFeature(start_manhole_feat)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_manhole_feat, end_connection_node_feat = manhole_handler.create_manhole_with_connection_node(end_geom)
            end_connection_node_id = end_connection_node_feat["id"]
            connection_node_layer.addFeature(end_connection_node_feat)
            manhole_layer.addFeature(end_manhole_feat)
        else:
            start_connection_node_id = start_manhole_feat["connection_node_id"]
            start_connection_node_feat = connection_node_handler.get_feat_by_id(start_connection_node_id)
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)

        # Set pipe specific attributes
        code_display_name = f"{start_manhole_feat['code']}-{end_manhole_feat['code']}"
        self.feature["connection_node_start_id"] = start_connection_node_id
        self.feature["connection_node_end_id"] = end_connection_node_id
        self.feature["code"] = code_display_name
        self.feature["display_name"] = code_display_name
        self.feature["invert_level_start_point"] = start_manhole_feat["bottom_level"]
        self.feature["invert_level_end_point"] = end_manhole_feat["bottom_level"]
        # Assign features as an form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat
        self.manhole_start = start_manhole_feat
        self.manhole_end = end_manhole_feat

        # Populate widgets based on features attributes
        pipe_iterable = (
            (1, start_connection_node_feat, start_manhole_feat),
            (2, end_connection_node_feat, end_manhole_feat),
        )
        for modifier, connection_node_feat, manhole_feat in pipe_iterable:
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

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_manholes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_manholes_on_edit()


class WeirForm(FormWithCSDefinition, FormWithStartEndNode):
    """Weir user layer edit form logic."""

    MODEL = dm.Weir

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.CrossSectionDefinition, 1): self.cross_section_definition,
        }

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_connection_nodes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_connection_nodes_on_edit()


class CulvertForm(FormWithCSDefinition, FormWithStartEndNode):
    """Culvert user layer edit form logic."""
    MODEL = dm.Culvert

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.CrossSectionDefinition, 1): self.cross_section_definition,
        }

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_connection_nodes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_connection_nodes_on_edit()


class OrificeForm(FormWithCSDefinition, FormWithStartEndNode):
    """Orifice user layer edit form logic."""

    MODEL = dm.Orifice

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.foreign_models_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.CrossSectionDefinition, 1): self.cross_section_definition,
        }

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.populate_cross_section_definition_on_creation()
            self.populate_connection_nodes_on_creation()
        else:
            self.populate_cross_section_definition_on_edit()
            self.populate_connection_nodes_on_edit()


ALL_FORMS = (
    ConnectionNodeForm,
    ManholeForm,
    PipeForm,
    WeirForm,
    CulvertForm,
    OrificeForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
