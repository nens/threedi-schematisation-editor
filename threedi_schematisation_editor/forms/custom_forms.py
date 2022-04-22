# Copyright (C) 2022 by Lutra Consulting
import threedi_schematisation_editor.data_models as dm
from collections import defaultdict
from operator import itemgetter
from functools import partial
from enum import Enum
from types import MappingProxyType
from threedi_schematisation_editor.utils import (
    find_point_nodes,
    find_linestring_nodes,
    find_point_polygons,
    connect_signal,
    disconnect_signal,
    is_optional,
    optional_type,
    enum_type,
)
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QSpinBox,
    QPlainTextEdit,
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
        self.custom_widgets = {}
        self.set_foreign_widgets()
        self.extra_features = defaultdict(list)
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)
        self.button_box = self.dialog.findChild(QObject, "buttonBox")
        self.button_box.accepted.connect(self.add_related_features)
        self.dialog.active_form_signals.add((self.layer.editingStarted, self.toggle_edit_mode))
        self.dialog.active_form_signals.add((self.layer.editingStopped, self.toggle_edit_mode))
        self.dialog.active_form_signals.add((self.button_box.accepted, self.add_related_features))

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {}
        return fm_features

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        # TODO: Improve handling of newly added related features
        if self.feature is None:
            return
        if self.feature.id() < 0:
            geometry = self.feature.geometry()
            if not geometry:
                return  # form open for an invalid feature
            else:
                if self.feature["id"] is not None:
                    # This is the case after accepting new feature
                    return
                self.creation = True
                self.handler.set_feature_values(self.feature)
        self.toggle_edit_mode()
        self.connect_foreign_widgets()
        self.connect_custom_widgets()

    def set_foreign_widgets(self):
        """Setting up widgets handling values from related models features."""
        main_fields = set(self.MODEL.__annotations__.keys())
        infinity = float("inf")
        for related_cls, relations_number in self.handler.RELATED_MODELS.items():
            table_name = related_cls.__tablename__
            range_end = relations_number + 1 if relations_number < infinity else 2
            for related_number in range(1, range_end):
                if relations_number == infinity:
                    numerical_modifier = infinity
                    str_num_mod = ""
                elif relations_number > 1:
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
        """Toggling editing for foreign widgets."""
        self.populate_with_extra_widgets()
        editing_active = self.layer.isEditable()
        for widget, related_cls, numerical_modifier, field_name in self.foreign_widgets.values():
            widget.setEnabled(editing_active)
        for widget in self.custom_widgets.values():
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
            if start_end_modifier is not None and start_end_modifier != float("inf"):
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
            if is_optional(field_type):
                field_type = optional_type(field_type)
            else:
                if self.layer.isEditable():
                    self.set_validation_background(widget, field_type)
                    edit_signal = self.get_widget_editing_signal(widget)
                    edit_slot = partial(self.set_validation_background, widget, field_type)
                    connect_signal(edit_signal, edit_slot)
                    self.dialog.active_form_signals.add((edit_signal, edit_slot))
                else:
                    widget.setStyleSheet("")
            if issubclass(field_type, Enum):
                cbo_items = {t.name.capitalize().replace("_", " "): t.value for t in field_type}
                self.populate_combo(widget, cbo_items)
            self.set_widget_value(widget, feature[field_name], var_type=field_type)
            self.main_widgets[widget.objectName()] = widget

    def set_validation_background(self, widget, field_type):
        """Setting validation color background if required value is empty."""
        widget_value = self.get_widget_value(widget)
        required_value_stylesheet = "background-color: rgb(255, 224, 178);"
        if issubclass(field_type, Enum):
            valid_values = [e.value for e in field_type]
            if widget_value in valid_values:
                widget.setStyleSheet("")
            else:
                widget.setStyleSheet(required_value_stylesheet)
        else:
            if widget_value is not None and widget_value != "":
                widget.setStyleSheet("")
            else:
                widget.setStyleSheet(required_value_stylesheet)

    def populate_foreign_widgets(self):
        """Populating values within foreign layers widgets."""
        for (data_model_cls, start_end_modifier), feature in self.foreign_models_features.items():
            if feature is not None:
                self.populate_widgets(data_model_cls, feature, start_end_modifier)

    @staticmethod
    def populate_combo(combo_widget, value_map, add_empty_entry=True):
        """Populates combo box with value map items (map key = displayed text, map value = data)."""
        combo_widget.clear()
        if add_empty_entry:
            combo_widget.addItem("", None)
        for text, data in sorted(value_map.items(), key=itemgetter(0)):
            combo_widget.addItem(text, data)

    def set_widget_value(self, widget, value, var_type=None):
        """Setting widget value."""
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
        elif isinstance(widget, QPlainTextEdit):
            widget.setPlainText(str(value) if value is not None else "")
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")

    def get_widget_value(self, widget):
        """Getting value from widget."""
        if isinstance(widget, QLineEdit):
            value = widget.text()
        elif isinstance(widget, QCheckBox):
            value = widget.isChecked()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = widget.value()
        elif isinstance(widget, QComboBox):
            value = widget.currentData()
        elif isinstance(widget, QPlainTextEdit):
            value = widget.toPlainText()
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            value = None
        return value

    def get_widget_editing_signal(self, widget):
        """Getting widget signal that will be recognize as an editing indication."""
        if isinstance(widget, (QLineEdit, QPlainTextEdit)):
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
        """Setting value from widget to associated feature."""
        if feature:
            value = self.get_widget_value(widget)
            handler = self.layer_manager.model_handlers[model_cls]
            layer = handler.layer
            if not layer.isEditable():
                layer.startEditing()
            feature[field_name] = value
            layer.updateFeature(feature)

    def connect_foreign_widgets(self):
        """Connect widget signals responsible for handling related layers attributes."""
        for widget_name, (widget, model_cls, numerical_modifier, field_name) in self.foreign_widgets.items():
            signal = self.get_widget_editing_signal(widget)
            try:
                feature = self.foreign_models_features[model_cls, numerical_modifier]
            except KeyError:
                continue
            slot = partial(self.set_value_from_widget, widget, feature, model_cls, field_name)
            connect_signal(signal, slot)
            self.dialog.active_form_signals.add((signal, slot))

    def sequence_related_features_ids(self):
        """Sequencing new feature 'id' values."""
        for features_to_add in self.extra_features.values():
            if len(features_to_add) > 1:
                increment_by = 0
                for feat in features_to_add:
                    feat["id"] = feat["id"] + increment_by
                    increment_by += 1

    def add_related_features(self):
        """Adding related features that should be added along currently added feature."""
        for handler, features_to_add in self.extra_features.items():
            layer = handler.layer
            if not layer.isEditable():
                layer.startEditing()
            layer.addFeatures(features_to_add)
        self.extra_features.clear()

    def fill_related_attributes(self):
        """Filling attributes referring to the other layers features."""
        pass

    def connect_custom_widgets(self):
        """Connect other widgets."""
        pass

    def populate_with_extra_widgets(self):
        """Populate widgets with addition of the other layers attributes."""
        pass


class FormWithNode(BaseForm):
    """Base edit form for user layers with a single connection node."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.connection_node = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, None): self.connection_node,
        }
        return fm_features

    def setup_connection_node_on_edit(self):
        """Setting up connection nodes during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_feat = connection_node_handler.get_feat_by_id(self.feature["connection_node_id"])
        self.connection_node = connection_node_feat

    def setup_connection_node_on_creation(self):
        """Setting up connection nodes during adding feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        connection_node_feat = find_point_nodes(self.feature.geometry().asPoint(), connection_node_layer)
        if connection_node_feat is None:
            connection_node_feat = connection_node_handler.create_new_feature(self.feature.geometry())
            self.extra_features[connection_node_handler].append(connection_node_feat)
        # Sequence related features ids
        self.sequence_related_features_ids()
        # Assign features as a form instance attributes.
        self.connection_node = connection_node_feat

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        self.feature["connection_node_id"] = self.connection_node["id"]

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_node_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_connection_node_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class FormWithStartEndNode(BaseForm):
    """Base edit form for user layers start and end connection nodes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.connection_node_start = None
        self.connection_node_end = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
        }
        return fm_features

    def setup_connection_nodes_on_edit(self):
        """Setting up connection nodes during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_start_id = self.feature["connection_node_start_id"]
        connection_node_end_id = self.feature["connection_node_end_id"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_start_id)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_end_id)

    def setup_connection_nodes_on_creation(self):
        """Setting up connection nodes during adding feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, connection_node_layer)
        if start_connection_node_feat is not None and end_connection_node_feat is None:
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                start_connection_node_feat, geometry=end_geom
            )
            self.extra_features[connection_node_handler].append(end_connection_node_feat)
        elif start_connection_node_feat is None and end_connection_node_feat is not None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                end_connection_node_feat, geometry=start_geom
            )
            self.extra_features[connection_node_handler].append(start_connection_node_feat)
        elif start_connection_node_feat is None and end_connection_node_feat is None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_connection_node_feat = connection_node_handler.create_new_feature(geometry=start_geom)
            self.extra_features[connection_node_handler].append(start_connection_node_feat)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_connection_node_feat = connection_node_handler.create_new_feature(geometry=end_geom)
            self.extra_features[connection_node_handler].append(end_connection_node_feat)
        # Sequence related features ids
        self.sequence_related_features_ids()
        # Assign features as a form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        self.feature["connection_node_start_id"] = self.connection_node_start["id"]
        self.feature["connection_node_end_id"] = self.connection_node_end["id"]
        code_display_name = f"{self.connection_node_start['code']}-{self.connection_node_end['code']}"
        try:
            self.feature["code"] = code_display_name
            self.feature["display_name"] = code_display_name
        except KeyError:
            pass  # Some layers might not have code and display name

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class NodeToSurfaceMapForm(BaseForm):
    """Basic surface to node map edit form logic."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = None
        self.surface_id_field = None
        self.surface = None

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        surface_handler = self.layer_manager.model_handlers[self.surface_model]
        connection_node_layer = connection_node_handler.layer
        surface_layer = surface_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        connection_node_feat = find_point_nodes(end_point, connection_node_layer)
        connection_node = connection_node_feat
        if connection_node is not None:
            self.feature["connection_node_id"] = connection_node["id"]
        if self.surface is None:
            self.surface = find_point_polygons(start_point, surface_layer)
        if self.surface is not None:
            self.feature[self.surface_id_field] = self.surface["id"]

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.surface = self.select_start_surface()
            self.fill_related_attributes()
        self.populate_widgets()

    def select_start_surface(self):
        """Selecting start surface"""
        title = f"Select start {self.surface_model.__layername__}"
        message = f"{self.surface_model.__layername__}s at location"
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        surface_handler = self.layer_manager.model_handlers[self.surface_model]
        surface_layer = surface_handler.layer
        surface_feats = find_point_polygons(start_point, surface_layer, allow_multiple=True)
        surfaces_no = len(surface_feats)
        if surfaces_no == 0:
            surface_feat = None
        elif surfaces_no == 1:
            surface_feat = next(iter(surface_feats))
        else:
            surface_feats_by_id = {int(feat["id"]): feat for feat in surface_feats}
            surface_entries = [f"{feat_id} ({feat['display_name']})" for feat_id, feat in surface_feats_by_id.items()]
            surface_entry = self.uc.pick_item(title, message, None, *surface_entries)
            surface_id = int(surface_entry.split()[0]) if surface_entry else None
            surface_feat = surface_feats_by_id[surface_id] if surface_id else None
        return surface_feat


class ConnectionNodeForm(BaseForm):
    """Connection node edit form logic."""

    MODEL = dm.ConnectionNode

    def populate_with_extra_widgets(self):
        # Populate widgets based on features attributes
        self.populate_widgets()


class ManholeForm(FormWithNode):
    """Manhole user layer edit form logic."""

    MODEL = dm.Manhole


class PipeForm(FormWithStartEndNode):
    """Pipe user layer edit form logic."""

    MODEL = dm.Pipe

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.manhole_start = None
        self.manhole_end = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.Manhole, 1): self.manhole_start,
            (dm.Manhole, 2): self.manhole_end,
        }
        return fm_features

    def setup_manholes_on_edit(self):
        """Setting up manholes during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_start_id = self.feature["connection_node_start_id"]
        connection_node_end_id = self.feature["connection_node_end_id"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_start_id)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_end_id)
        self.manhole_start = connection_node_handler.get_manhole_feat_for_node_id(connection_node_start_id)
        self.manhole_end = connection_node_handler.get_manhole_feat_for_node_id(connection_node_end_id)

    def setup_manholes_on_creation(self):
        """Setting up manholes during adding feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        manhole_handler = self.layer_manager.model_handlers[dm.Manhole]
        manhole_layer = manhole_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_manhole_feat, end_manhole_feat = find_linestring_nodes(linestring, manhole_layer)
        if start_manhole_feat is not None and end_manhole_feat is None:
            start_connection_node_id = start_manhole_feat["connection_node_id"]
            start_connection_node_feat = connection_node_handler.get_feat_by_id(start_connection_node_id)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_manhole_feat, end_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                end_geom, template_feat=start_manhole_feat
            )
            self.extra_features[connection_node_handler].append(end_connection_node_feat)
            self.extra_features[manhole_handler].append(end_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is not None:
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom, template_feat=end_manhole_feat
            )
            self.extra_features[connection_node_handler].append(start_connection_node_feat)
            self.extra_features[manhole_handler].append(start_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom
            )
            self.extra_features[connection_node_handler].append(start_connection_node_feat)
            self.extra_features[manhole_handler].append(start_manhole_feat)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_manhole_feat, end_connection_node_feat = manhole_handler.create_manhole_with_connection_node(end_geom)
            self.extra_features[connection_node_handler].append(end_connection_node_feat)
            self.extra_features[manhole_handler].append(end_manhole_feat)
        else:
            start_connection_node_id = start_manhole_feat["connection_node_id"]
            start_connection_node_feat = connection_node_handler.get_feat_by_id(start_connection_node_id)
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)

        # Sequence related features ids
        self.sequence_related_features_ids()
        # Reassign manholes connection_node_id after sequencing
        start_manhole_feat["connection_node_id"] = start_connection_node_feat["id"]
        end_manhole_feat["connection_node_id"] = end_connection_node_feat["id"]
        # Assign features as a form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat
        self.manhole_start = start_manhole_feat
        self.manhole_end = end_manhole_feat

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        code_display_name = f"{self.manhole_start['code']}-{self.manhole_end['code']}"
        self.feature["code"] = code_display_name
        self.feature["display_name"] = code_display_name
        self.feature["invert_level_start_point"] = self.manhole_start["bottom_level"]
        self.feature["invert_level_end_point"] = self.manhole_end["bottom_level"]

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_manholes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_manholes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class WeirForm(FormWithStartEndNode):
    """Weir user layer edit form logic."""

    MODEL = dm.Weir

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class CulvertForm(FormWithStartEndNode):
    """Culvert user layer edit form logic."""

    MODEL = dm.Culvert

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class OrificeForm(FormWithStartEndNode):
    """Orifice user layer edit form logic."""

    MODEL = dm.Orifice

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class PumpstationForm(FormWithNode):
    """Pumpstation without end node user layer edit form logic."""

    MODEL = dm.Pumpstation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class PumpstationMapForm(FormWithStartEndNode):
    """Pumpstation with end node user layer edit form logic."""

    MODEL = dm.PumpstationMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.pumpstation = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.Pumpstation, None): self.pumpstation,
        }
        return fm_features

    def setup_pumpstation_on_edit(self):
        """Setting up pumpstation during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pumpstation_handler = self.layer_manager.model_handlers[dm.Pumpstation]
        connection_node_start_id = self.feature["connection_node_start_id"]
        connection_node_end_id = self.feature["connection_node_end_id"]
        pumpstation_id = self.feature["pumpstation_id"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_start_id)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_end_id)
        self.pumpstation = pumpstation_handler.get_feat_by_id(pumpstation_id)

    def setup_pumpstation_on_creation(self):
        """Setting up pumpstation during adding feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pumpstation_handler = self.layer_manager.model_handlers[dm.Pumpstation]
        connection_node_layer = connection_node_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, connection_node_layer)
        start_pump_feat = self.pumpstation
        if start_pump_feat is None:
            start_geom = QgsGeometry.fromPointXY(start_point)
            if start_connection_node_feat is None:
                start_pump_feat, start_connection_node_feat = pumpstation_handler.create_pump_with_connection_node(
                    start_geom
                )
                self.extra_features[connection_node_handler].append(start_connection_node_feat)
            else:
                start_pump_feat = pumpstation_handler.create_new_feature(start_geom)
                start_pump_feat["connection_node_id"] = start_connection_node_feat["id"]
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                self.extra_features[connection_node_handler].append(end_connection_node_feat)
            self.extra_features[pumpstation_handler].append(start_pump_feat)
        else:
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                self.extra_features[connection_node_handler].append(end_connection_node_feat)
        # Assign features as a form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat
        self.pumpstation = start_pump_feat
        self.sequence_related_features_ids()

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        self.feature["pumpstation_id"] = self.pumpstation["id"]

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.pumpstation = self.select_start_pumpstation()
            self.setup_pumpstation_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_pumpstation_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()

    def select_start_pumpstation(self):
        """Selecting start pumpstation"""
        title = "Select start pumpstation"
        message = "Pumpstations at location"
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        pumpstation_handler = self.layer_manager.model_handlers[dm.Pumpstation]
        pumpstation_layer = pumpstation_handler.layer
        start_pump_feats = find_point_nodes(start_point, pumpstation_layer, allow_multiple=True)
        pump_no = len(start_pump_feats)
        if pump_no == 0:
            pumpstation_feat = None
        elif pump_no == 1:
            pumpstation_feat = next(iter(start_pump_feats))
        else:
            pump_feats_by_id = {feat["id"]: feat for feat in start_pump_feats}
            pump_entries = [f"{feat_id} ({feat['display_name']})" for feat_id, feat in pump_feats_by_id.items()]
            pumpstation_entry = self.uc.pick_item(title, message, None, *pump_entries)
            pumpstation_id = int(pumpstation_entry.split()[0]) if pumpstation_entry else None
            pumpstation_feat = pump_feats_by_id[pumpstation_id] if pumpstation_id else None
        return pumpstation_feat


class ImperviousSurfaceMapForm(NodeToSurfaceMapForm):
    """Impervious Surface Map user layer edit form logic."""

    MODEL = dm.ImperviousSurfaceMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = dm.ImperviousSurface
        self.surface_id_field = "impervious_surface_id"


class SurfaceMapForm(NodeToSurfaceMapForm):
    """Surface Map user layer edit form logic."""

    MODEL = dm.SurfaceMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = dm.Surface
        self.surface_id_field = "surface_id"


class ChannelForm(FormWithStartEndNode):
    """Channel user layer edit form logic."""

    MODEL = dm.Channel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.cross_section_locations = None
        self.current_cross_section_location = None
        xs_locations_cbo_name = "cross_section_locations"
        self.current_cross_section_locations_cbo = self.dialog.findChild(QComboBox, xs_locations_cbo_name)
        self.custom_widgets[xs_locations_cbo_name] = self.current_cross_section_locations_cbo

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with id and value = data model feature(s)."""
        fm_features = {
            (dm.ConnectionNode, 1): self.connection_node_start,
            (dm.ConnectionNode, 2): self.connection_node_end,
            (dm.CrossSectionLocation, float("inf")): self.cross_section_locations,
        }
        return fm_features

    def setup_cross_section_location_on_edit(self):
        """Setting up cross-section location during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
        connection_node_start_id = self.feature["connection_node_start_id"]
        connection_node_end_id = self.feature["connection_node_end_id"]
        channel_id = self.feature["id"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_start_id)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_end_id)
        self.cross_section_locations = cross_section_location_handler.get_multiple_feats_by_id(channel_id, "channel_id")
        if self.cross_section_locations:
            channel_cross_section_location_ids = {str(feat["id"]): feat for feat in self.cross_section_locations}
            self.populate_combo(self.current_cross_section_locations_cbo, channel_cross_section_location_ids, False)
            self.current_cross_section_location = self.cross_section_locations[0]

    def setup_cross_section_location_on_creation(self):
        """Setting up cross-section location during adding feature."""
        cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
        channel_geom = self.feature.geometry()
        linestring = self.feature.geometry().asPolyline()
        if len(linestring) >= 3:
            cross_section_location_point = linestring[1]
            cross_section_location_geom = QgsGeometry.fromPointXY(cross_section_location_point)
        else:
            cross_section_location_geom = channel_geom.interpolate(channel_geom.length() / 2.0)
        cross_section_location_feat = cross_section_location_handler.create_new_feature(cross_section_location_geom)
        channel_cross_section_location_ids = {str(cross_section_location_feat["id"]): cross_section_location_feat}
        self.populate_combo(self.current_cross_section_locations_cbo, channel_cross_section_location_ids, False)
        self.cross_section_locations = [cross_section_location_feat]
        self.current_cross_section_location = cross_section_location_feat
        self.extra_features[cross_section_location_handler].append(self.current_cross_section_location)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        global_settings_handler = self.layer_manager.model_handlers[dm.GlobalSettings]
        global_settings_layer = global_settings_handler.layer
        channel_code = self.feature["code"]
        cross_section_location_code = f"{channel_code}_cross_section_1"
        self.current_cross_section_location["channel_id"] = self.feature["id"]
        self.current_cross_section_location["code"] = cross_section_location_code
        try:
            global_settings_feat = next(global_settings_layer.getFeatures())
        except StopIteration:
            global_settings_feat = None
        if global_settings_feat:
            self.current_cross_section_location["friction_type"] = global_settings_feat["frict_type"]

    def set_current_cross_section_location(self, current_text):
        """Set handling of selected channel cross-section location."""
        if current_text:
            cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
            for signal, slot in self.dialog.active_form_signals:
                disconnect_signal(signal, slot)
            self.current_cross_section_location = cross_section_location_handler.get_feat_by_id(int(current_text))
            self.populate_foreign_widgets()
            for signal, slot in self.dialog.active_form_signals:
                connect_signal(signal, slot)

    def set_cross_section_location_value_from_widget(self, widget, field_name):
        """Set currently selected cross-section attribute."""
        self.set_value_from_widget(widget, self.current_cross_section_location, dm.CrossSectionLocation, field_name)

    def connect_foreign_widgets(self):
        """Connect widget signals responsible for handling related layers attributes."""
        for widget_name, (widget, model_cls, numerical_modifier, field_name) in self.foreign_widgets.items():
            signal = self.get_widget_editing_signal(widget)
            try:
                feature_or_features = self.foreign_models_features[model_cls, numerical_modifier]
            except KeyError:
                continue
            if model_cls == dm.CrossSectionLocation:
                slot = partial(self.set_cross_section_location_value_from_widget, widget, field_name)
            else:
                slot = partial(self.set_value_from_widget, widget, feature_or_features, model_cls, field_name)
            connect_signal(signal, slot)
            self.dialog.active_form_signals.add((signal, slot))

    def connect_custom_widgets(self):
        """Connect other widgets."""
        signal = self.current_cross_section_locations_cbo.currentTextChanged
        slot = self.set_current_cross_section_location
        connect_signal(signal, slot)
        self.dialog.active_form_signals.add((signal, slot))

    def populate_foreign_widgets(self):
        """Populating values within foreign layers widgets."""
        for (data_model_cls, start_end_modifier), feature_or_features in self.foreign_models_features.items():
            if data_model_cls == dm.CrossSectionLocation:
                feature = self.current_cross_section_location
            else:
                feature = feature_or_features
            if feature is not None:
                self.populate_widgets(data_model_cls, feature, start_end_modifier)

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.setup_cross_section_location_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_cross_section_location_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class CrossSectionLocationForm(BaseForm):
    """Cross-section location user layer edit form logic."""

    MODEL = dm.CrossSectionLocation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.channel = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with id and value = data model feature(s)."""
        fm_features = {
            (dm.Channel, 1): self.channel,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        global_settings_handler = self.layer_manager.model_handlers[dm.GlobalSettings]
        channel_layer = channel_handler.layer
        global_settings_layer = global_settings_handler.layer
        point_geom = self.feature.geometry()
        point = point_geom.asPoint()
        if find_point_nodes(point, connection_node_handler.layer) is not None:
            self.uc.show_warn("WARNING: Cross-section shouldn't be placed at connection node location!")
        channel_node_feat = find_point_nodes(point, channel_layer)
        if channel_node_feat:
            channel_id = channel_node_feat["id"]
            channel_geom = channel_node_feat.geometry()
            point_distance_on_channel = channel_geom.lineLocatePoint(point_geom)
            other_cross_sections = self.handler.get_multiple_feats_by_id(channel_id, "channel_id")
            other_cross_sections_num = len(other_cross_sections)
            cross_section_num = other_cross_sections_num + 1
            channel_code = channel_node_feat["code"]
            cross_section_location_code = f"{channel_code}_cross_section_{cross_section_num}"
            self.feature["channel_id"] = channel_id
            self.feature["code"] = cross_section_location_code
            self.channel = channel_node_feat
            if other_cross_sections:
                new_feat_with_distance = (self.feature, point_distance_on_channel)
                cross_sections_with_distance = [
                    (feat, channel_geom.lineLocatePoint(feat.geometry())) for feat in other_cross_sections
                ]
                cross_sections_with_distance.append(new_feat_with_distance)
                cross_sections_with_distance.sort(key=itemgetter(-1))
                new_feat_index = cross_sections_with_distance.index(new_feat_with_distance)
                if new_feat_index == 0:
                    # New cross-section is first along channel
                    closest_existing_cross_section, closest_xs_distance = cross_sections_with_distance[1]
                    reference_level = closest_existing_cross_section["reference_level"]
                    bank_level = closest_existing_cross_section["bank_level"]
                elif new_feat_index == other_cross_sections_num:
                    # New cross-section is last along channel
                    closest_existing_cross_section, closest_xs_distance = cross_sections_with_distance[-2]
                    reference_level = closest_existing_cross_section["reference_level"]
                    bank_level = closest_existing_cross_section["bank_level"]
                else:
                    # New cross-section is somewhere in the middle
                    before_xs, before_xs_distance = cross_sections_with_distance[new_feat_index - 1]
                    after_xs, after_xs_distance = cross_sections_with_distance[new_feat_index + 1]
                    point_distance_to_before = point_distance_on_channel - before_xs_distance
                    point_distance_to_after = after_xs_distance - point_distance_on_channel
                    if point_distance_to_before < point_distance_to_after:
                        closest_existing_cross_section, closest_xs_distance = before_xs, before_xs_distance
                    else:
                        closest_existing_cross_section, closest_xs_distance = after_xs, after_xs_distance
                    before_to_after_distance = after_xs_distance - before_xs_distance
                    interpolation_coefficient = point_distance_to_before / before_to_after_distance
                    before_reference_level = before_xs["reference_level"]
                    before_bank_level = before_xs["bank_level"]
                    after_reference_level = after_xs["reference_level"]
                    after_bank_level = after_xs["bank_level"]
                    reference_level = round(
                        before_reference_level
                        + ((after_reference_level - before_reference_level) * interpolation_coefficient),
                        3,
                    )
                    bank_level = round(
                        before_bank_level + ((after_bank_level - before_bank_level) * interpolation_coefficient), 3
                    )
                self.feature["reference_level"] = reference_level
                self.feature["bank_level"] = bank_level
                self.feature["cross_section_shape"] = closest_existing_cross_section["cross_section_shape"]
                self.feature["cross_section_width"] = closest_existing_cross_section["cross_section_width"]
                self.feature["cross_section_height"] = closest_existing_cross_section["cross_section_height"]
                self.feature["cross_section_table"] = closest_existing_cross_section["cross_section_table"]
        try:
            global_settings_feat = next(global_settings_layer.getFeatures())
            self.feature["friction_type"] = global_settings_feat["frict_type"]
        except StopIteration:
            pass

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()


ALL_FORMS = (
    ConnectionNodeForm,
    ManholeForm,
    PipeForm,
    WeirForm,
    CulvertForm,
    OrificeForm,
    PumpstationForm,
    PumpstationMapForm,
    ImperviousSurfaceMapForm,
    SurfaceMapForm,
    ChannelForm,
    CrossSectionLocationForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
