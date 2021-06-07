import threedi_model_builder.data_models as dm
import threedi_model_builder.enumerators as en
from functools import partial
from enum import Enum
from types import MappingProxyType
from threedi_model_builder.utils import (
    find_point_nodes,
    find_linestring_nodes,
    connect_signal,
    is_optional,
    optional_type,
)
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
        self.set_foreign_widgets()
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)
        self.dialog.active_form_signals.add((self.layer.editingStarted, self.toggle_edit_mode))
        self.dialog.active_form_signals.add((self.layer.editingStopped, self.toggle_edit_mode))

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {}
        return fm_features

    def setup_form_widgets(self):
        """Setting up all form widgets."""
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
        """Toggling editing for foreign widgets."""
        self.populate_with_extra_widgets()
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
            if is_optional(field_type):
                field_type = optional_type(field_type)
            else:
                if self.layer.isEditable():
                    widget.setStyleSheet("background-color: rgb(255, 224, 178);")
                else:
                    widget.setStyleSheet("")
            if issubclass(field_type, Enum):
                cbo_items = {t.name.capitalize().replace("_", " "): t.value for t in field_type}
                self.populate_combo(widget, cbo_items)
            self.set_widget_value(widget, feature[field_name], var_type=field_type)
            self.main_widgets[widget.objectName()] = widget

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
        for text, data in value_map.items():
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
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            value = None
        return value

    def get_widget_editing_signal(self, widget):
        """Getting widget signal that will be recognize as an editing indication."""
        if isinstance(widget, QLineEdit):
            signal = widget.textChanged
        elif isinstance(widget, QCheckBox):
            signal = widget.stateChanged
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            signal = widget.valueChanged
        elif isinstance(widget, QComboBox):
            signal = widget.activated
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
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        connection_node_feat = find_point_nodes(self.feature.geometry().asPoint(), connection_node_layer)
        if connection_node_feat is None:
            connection_node_feat = connection_node_handler.create_new_feature(self.feature.geometry())
            connection_node_layer.addFeature(connection_node_feat)
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
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, connection_node_layer)
        if start_connection_node_feat is not None and end_connection_node_feat is None:
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                start_connection_node_feat, geometry=end_geom
            )
            connection_node_layer.addFeature(end_connection_node_feat)
        elif start_connection_node_feat is None and end_connection_node_feat is not None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                end_connection_node_feat, geometry=start_geom
            )
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
        # Assign features as an form instance attributes.
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


class FormWithCSDefinition(BaseForm):
    """Base edit form for user layers with Cross Section Definition."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.cross_section_definition = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.CrossSectionDefinition, None): self.cross_section_definition,
        }
        return fm_features

    def setup_cross_section_definition_on_edit(self):
        """Setting up connection nodes during editing feature."""
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_feat = cross_section_def_handler.get_feat_by_id(self.feature["cross_section_definition_id"])
        self.cross_section_definition = cross_section_def_feat

    def setup_cross_section_definition_on_creation(self):
        """Setting up connection nodes during adding feature."""
        cross_section_def_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        cross_section_def_layer = cross_section_def_handler.layer
        cross_section_def_feat = cross_section_def_handler.create_new_feature()
        if not cross_section_def_layer.isEditable():
            cross_section_def_layer.startEditing()
        if self.MODEL == dm.Weir:
            cross_section_def_feat["shape"] = en.CrossSectionShape.RECTANGLE.value
        cross_section_def_layer.addFeature(cross_section_def_feat)
        self.cross_section_definition = cross_section_def_feat

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        self.feature["cross_section_definition_id"] = self.cross_section_definition["id"]

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_cross_section_definition_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_cross_section_definition_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class ConnectionNodeForm(BaseForm):
    """Connection node edit form logic."""

    MODEL = dm.ConnectionNode

    def populate_with_extra_widgets(self):
        # Populate widgets based on features attributes
        self.populate_widgets()


class ManholeForm(FormWithNode):
    """Manhole user layer edit form logic."""

    MODEL = dm.Manhole


class PipeForm(FormWithCSDefinition, FormWithStartEndNode):
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
            (dm.CrossSectionDefinition, None): self.cross_section_definition,
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
                end_geom, template_feat=start_manhole_feat
            )
            connection_node_layer.addFeature(end_connection_node_feat)
            manhole_layer.addFeature(end_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is not None:
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom, template_feat=end_manhole_feat
            )
            connection_node_layer.addFeature(start_connection_node_feat)
            manhole_layer.addFeature(start_manhole_feat)
        elif start_manhole_feat is None and end_manhole_feat is None:
            # Create and add starting points
            start_geom = QgsGeometry.fromPointXY(start_point)
            start_manhole_feat, start_connection_node_feat = manhole_handler.create_manhole_with_connection_node(
                start_geom
            )
            connection_node_layer.addFeature(start_connection_node_feat)
            manhole_layer.addFeature(start_manhole_feat)
            # Create and add ending points
            end_geom = QgsGeometry.fromPointXY(end_point)
            end_manhole_feat, end_connection_node_feat = manhole_handler.create_manhole_with_connection_node(end_geom)
            connection_node_layer.addFeature(end_connection_node_feat)
            manhole_layer.addFeature(end_manhole_feat)
        else:
            start_connection_node_id = start_manhole_feat["connection_node_id"]
            start_connection_node_feat = connection_node_handler.get_feat_by_id(start_connection_node_id)
            end_connection_node_id = end_manhole_feat["connection_node_id"]
            end_connection_node_feat = connection_node_handler.get_feat_by_id(end_connection_node_id)

        # Assign features as an form instance attributes.
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
            self.setup_cross_section_definition_on_creation()
            self.setup_manholes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_cross_section_definition_on_edit()
            self.setup_manholes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class WeirForm(FormWithCSDefinition, FormWithStartEndNode):
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
            (dm.CrossSectionDefinition, None): self.cross_section_definition,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_cross_section_definition_on_creation()
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_cross_section_definition_on_edit()
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class CulvertForm(FormWithCSDefinition, FormWithStartEndNode):
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
            (dm.CrossSectionDefinition, None): self.cross_section_definition,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_cross_section_definition_on_creation()
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_cross_section_definition_on_edit()
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class OrificeForm(FormWithCSDefinition, FormWithStartEndNode):
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
            (dm.CrossSectionDefinition, None): self.cross_section_definition,
        }
        return fm_features

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.setup_cross_section_definition_on_creation()
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_cross_section_definition_on_edit()
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
        pumpstation_layer = pumpstation_handler.layer
        if not connection_node_layer.isEditable():
            connection_node_layer.startEditing()
        if not pumpstation_layer.isEditable():
            pumpstation_layer.startEditing()
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
                connection_node_layer.addFeature(start_connection_node_feat)
            else:
                start_pump_feat = pumpstation_handler.create_new_feature(start_geom)
                start_pump_feat["connection_node_id"] = start_connection_node_feat["id"]
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                connection_node_layer.addFeature(end_connection_node_feat)
            pumpstation_layer.addFeature(start_pump_feat)
        else:
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                connection_node_layer.addFeature(end_connection_node_feat)
        # Assign features as an form instance attributes.
        self.connection_node_start = start_connection_node_feat
        self.connection_node_end = end_connection_node_feat
        self.pumpstation = start_pump_feat

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


ALL_FORMS = (
    ConnectionNodeForm,
    ManholeForm,
    PipeForm,
    WeirForm,
    CulvertForm,
    OrificeForm,
    PumpstationForm,
    PumpstationMapForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
