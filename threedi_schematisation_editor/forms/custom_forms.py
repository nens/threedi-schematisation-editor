# Copyright (C) 2023 by Lutra Consulting
import sys
from collections import defaultdict
from enum import Enum
from functools import partial
from operator import itemgetter
from types import MappingProxyType

from qgis.core import NULL, QgsGeometry
from qgis.gui import QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
)

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.enumerators as en
from threedi_schematisation_editor.utils import (
    REQUIRED_VALUE_STYLESHEET,
    NumericItemDelegate,
    connect_signal,
    disconnect_signal,
    find_linestring_nodes,
    find_point_nodes,
    find_point_polygons,
    find_point_polyline,
    is_optional,
    optional_type,
    setup_cross_section_widgets,
    setup_friction_and_vegetation_widgets,
    setup_cross_section_definition_widgets,
)

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
    MIN_FID = -sys.maxsize - 1

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
        self.extra_logic = {}
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)
        self.button_box = self.dialog.findChild(QObject, "buttonBox")
        self.button_box.accepted.connect(self.postprocess_on_acceptance)
        self.dialog.active_form_signals.add((self.layer.editingStarted, self.toggle_edit_mode))
        self.dialog.active_form_signals.add((self.layer.editingStopped, self.toggle_edit_mode))
        self.dialog.active_form_signals.add((self.button_box.accepted, self.postprocess_on_acceptance))

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {}
        return fm_features

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        # TODO: Improve handling of newly added related features
        for field, customisation_fn in self.handler.FORM_CUSTOMIZATIONS.items():
            widget = self.dialog.findChild(QObject, field)
            customisation_fn(widget)
        if self.feature is None:
            return
        fid = self.feature.id()
        if fid == self.MIN_FID:
            geometry = self.feature.geometry()
            if not geometry:
                return  # form open for an invalid feature
            else:
                if self.feature["id"] is not None:
                    # This is the case after accepting new feature
                    return
                self.creation = True
                self.handler.set_feature_values(self.feature)
        self.activate_field_based_conditions()
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
            related_handler = self.layer_manager.model_handlers[related_cls]
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
                    try:
                        customization_fn = related_handler.FORM_CUSTOMIZATIONS[field_name]
                        customization_fn(widget)
                    except KeyError:
                        pass
                    self.foreign_widgets[widget_name] = (widget, related_cls, numerical_modifier, field_name)

    def toggle_edit_mode(self):
        """Toggling editing for foreign widgets."""
        self.populate_with_extra_widgets()
        editing_active = self.layer.isEditable()
        for widget, related_cls, numerical_modifier, field_name in self.foreign_widgets.values():
            widget.setEnabled(editing_active)
        for widget in self.custom_widgets.values():
            widget.setEnabled(editing_active)
        if hasattr(self, "cross_section_shape"):
            setup_cross_section_widgets(self, self.cross_section_shape, self.cross_section_prefix)
            if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
                friction_type = self.dialog.findChild(QObject, "friction_type")
                setup_friction_and_vegetation_widgets(
                    self, self.cross_section_shape, friction_type, self.cross_section_prefix
                )

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
            else:
                if self.layer.isEditable():
                    self.set_validation_background(widget, field_type)
                    edit_signal = self.get_widget_editing_signal(widget)
                    edit_slot = partial(self.set_validation_background, widget, field_type)
                    connect_signal(edit_signal, edit_slot)
                    self.dialog.active_form_signals.add((edit_signal, edit_slot))
                else:
                    widget.setStyleSheet("")
            real_field_type = optional_type(field_type) if is_optional(field_type) else field_type
            if data_model_cls != self.MODEL:
                # Populate combo boxes of related features only and if it wasn't populated already
                if issubclass(real_field_type, Enum) and widget.count() == 0:
                    cbo_items = {t.name.capitalize().replace("_", " "): t.value for t in real_field_type}
                    self.populate_combo(widget, cbo_items)
            is_foreign = data_model_cls != self.MODEL
            self.set_widget_value(widget, feature[field_name], var_type=real_field_type, is_foreign=is_foreign)
            self.set_validation_background(widget, field_type)
            self.main_widgets[widget_name] = widget
            clear_value_button_name = f"{widget_name}_clear"
            if clear_value_button_name not in self.custom_widgets:
                clear_value_button = self.dialog.findChild(QToolButton, clear_value_button_name)
                if clear_value_button is not None:
                    clear_signal = clear_value_button.clicked
                    clear_slot = partial(self.handle_clear_value, widget, feature, data_model_cls, field_name)
                    connect_signal(clear_signal, clear_slot)
                    self.dialog.active_form_signals.add((clear_signal, clear_slot))
                    self.custom_widgets[clear_value_button_name] = clear_value_button

    def set_validation_background(self, widget, field_type):
        """Setting validation color background if required value is empty."""
        widget_value = self.get_widget_value(widget)
        if is_optional(field_type):
            widget.setStyleSheet("")
        else:
            if issubclass(field_type, Enum):
                valid_values = [e.value for e in field_type]
                if widget_value in valid_values:
                    widget.setStyleSheet("")
                else:
                    widget.setStyleSheet(REQUIRED_VALUE_STYLESHEET)
            else:
                if widget_value not in [None, NULL, ""]:
                    widget.setStyleSheet("")
                else:
                    widget.setStyleSheet(REQUIRED_VALUE_STYLESHEET)

    def handle_clear_value(self, widget, feature, model_cls, field_name):
        """Handling custom clear value action."""
        if feature:
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                handler = self.layer_manager.model_handlers[model_cls]
                layer = handler.layer
                field_idx = layer.fields().lookupField(field_name)
                fid = feature.id()
                if not layer.isEditable():
                    layer.startEditing()
                if model_cls != self.MODEL:
                    widget.setValue(widget.maximum())  # workaround for the issue #129
                widget.clear()
                if fid == self.MIN_FID:
                    # We need to postpone changing field value to NULL as it needs to be done after accepting form
                    if field_idx not in self.extra_logic:
                        self.extra_logic[field_idx] = partial(self.mark_null_field, widget, field_idx)
                else:
                    layer.changeAttributeValue(fid, field_idx, NULL)
                field_type = model_cls.__annotations__[field_name]
                self.set_validation_background(widget, field_type=field_type)

    def mark_null_field(self, widget, field_idx):
        """Mark field which supposed to be set to NULL after accepting creation form."""
        if not widget.text():
            self.handler.fields_to_nullify[field_idx] = {field_idx: NULL}

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

    def set_widget_value(self, widget, value, var_type=None, is_foreign=False):
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
                if is_foreign:
                    widget.setValue(widget.maximum())  # workaround for the issue #129
                widget.clear()
        elif isinstance(widget, QComboBox):
            item_idx = widget.findData(value if value != NULL else None)
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
            widget_text = widget.text()
            value = widget.value() if (widget_text and widget_text != "NULL") else NULL
        elif isinstance(widget, QComboBox):
            value = widget.currentData()
        elif isinstance(widget, QPlainTextEdit):
            value = widget.toPlainText()
        else:
            self.uc.log_warn(f"Unknown widget type: {widget.__class__.__name__}")
            value = None
        return value

    def get_widget_editing_signal(self, widget):
        """Getting widget signal that will be recognized as an editing indication."""
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
            field_idx = layer.fields().lookupField(field_name)
            fid = feature.id()
            if not layer.isEditable():
                layer.startEditing()
            if fid > 0:
                layer.changeAttributeValue(fid, field_idx, value)
            else:
                feature[field_name] = value

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

    def postprocess_on_acceptance(self):
        """Adding related features and triggering extra logic after form acceptance."""
        for handler, features_to_add in self.extra_features.items():
            layer = handler.layer
            if not layer.isEditable():
                layer.startEditing()
            layer.addFeatures(features_to_add)
        self.extra_features.clear()
        for postprocess_fn in self.extra_logic.values():
            postprocess_fn()

    def fill_related_attributes(self):
        """Filling attributes referring to the other layers features."""
        pass

    def connect_custom_widgets(self):
        """Connect other widgets."""
        pass

    def populate_with_extra_widgets(self):
        """Populate widgets with addition of the other layers attributes."""
        pass

    def activate_field_based_conditions(self):
        """Activate filed based conditions."""
        pass


class FormWithXSTable(BaseForm):
    """Base edit form for user layers with cross-section table reference."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.cross_section_shape = None
        self.cross_section_table = None
        self.cross_section_friction = None
        self.cross_section_vegetation = None
        self.cross_section_table_edit = None
        self.cross_section_table_add = None
        self.cross_section_table_delete = None
        self.cross_section_table_paste = None
        self.cross_section_friction_clear = None
        self.cross_section_vegetation_clear = None
        self.cross_section_table_cell_changed_signal = None
        self.cross_section_friction_cell_changed_signal = None
        self.cross_section_vegetation_cell_changed_signal = None
        self.cross_section_friction_clear_signal = None
        self.cross_section_vegetation_clear_signal = None
        self.cross_section_table_cell_changed_slot = None
        self.cross_section_friction_cell_changed_slot = None
        self.cross_section_vegetation_cell_changed_slot = None
        self.cross_section_friction_clear_slot = None
        self.cross_section_vegetation_clear_slot = None
        if self.MODEL == dm.Channel:
            self.cross_section_prefix = "cross_section_location_"
            self.current_cross_section_location = None
            self.layer_with_xs = self.layer_manager.model_handlers[dm.CrossSectionLocation].layer
        else:
            self.cross_section_prefix = ""
            self.current_cross_section_location = self.feature
            self.layer_with_xs = self.layer
        self.layer_with_xs_fields = self.layer_with_xs.fields()
        self.setup_cross_section_table_widgets()

    @property
    def cross_section_table_field_widget_map(self):
        field_map = {
            "cross_section_table": self.cross_section_table,
            "cross_section_friction_table": self.cross_section_friction,
            "cross_section_vegetation_table": self.cross_section_vegetation,
        }
        return field_map

    @property
    def cross_section_table_edit_slot_signal_pairs(self):
        slot_signal_pairs = [
            (self.cross_section_table_cell_changed_signal, self.cross_section_table_cell_changed_slot),
            (self.cross_section_friction_cell_changed_signal, self.cross_section_friction_cell_changed_slot),
            (self.cross_section_vegetation_cell_changed_signal, self.cross_section_vegetation_cell_changed_slot),
        ]
        return slot_signal_pairs

    def setup_cross_section_table_widgets(self):
        """Setup cross-section table widgets."""
        xs_table = f"{self.cross_section_prefix}cross_section_table_widget"
        xs_table_add = f"{self.cross_section_prefix}cross_section_table_add"
        xs_table_delete = f"{self.cross_section_prefix}cross_section_table_delete"
        xs_table_paste = f"{self.cross_section_prefix}cross_section_table_paste"
        self.cross_section_shape = self.dialog.findChild(QObject, f"{self.cross_section_prefix}cross_section_shape")
        self.cross_section_table = self.dialog.findChild(QTableWidget, xs_table)
        self.cross_section_table_add = self.dialog.findChild(QPushButton, xs_table_add)
        self.cross_section_table_delete = self.dialog.findChild(QPushButton, xs_table_delete)
        self.cross_section_table_paste = self.dialog.findChild(QPushButton, xs_table_paste)
        self.custom_widgets[xs_table] = self.cross_section_table
        self.custom_widgets[xs_table_add] = self.cross_section_table_add
        self.custom_widgets[xs_table_delete] = self.cross_section_table_delete
        self.custom_widgets[xs_table_paste] = self.cross_section_table_paste
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            xs_friction = f"{self.cross_section_prefix}cross_section_friction_widget"
            xs_vegetation = f"{self.cross_section_prefix}cross_section_vegetation_widget"
            xs_friction_clear = f"{self.cross_section_prefix}cross_section_friction_clear"
            xs_vegetation_clear = f"{self.cross_section_prefix}cross_section_vegetation_clear"
            self.cross_section_friction = self.dialog.findChild(QTableWidget, xs_friction)
            self.cross_section_vegetation = self.dialog.findChild(QTableWidget, xs_vegetation)
            self.cross_section_friction_clear = self.dialog.findChild(QPushButton, xs_friction_clear)
            self.cross_section_vegetation_clear = self.dialog.findChild(QPushButton, xs_vegetation_clear)
            self.custom_widgets[xs_friction] = self.cross_section_friction
            self.custom_widgets[xs_vegetation] = self.cross_section_vegetation
            self.custom_widgets[xs_friction_clear] = self.cross_section_friction_clear
            self.custom_widgets[xs_vegetation_clear] = self.cross_section_vegetation_clear

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        super().setup_form_widgets()
        setup_cross_section_widgets(self, self.cross_section_shape, self.cross_section_prefix)
        friction_type = self.dialog.findChild(QObject, f"{self.cross_section_prefix}friction_type")
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            setup_friction_and_vegetation_widgets(
                self, self.cross_section_shape, friction_type, self.cross_section_prefix
            )

    def connect_custom_widgets(self):
        """Connect other widgets."""
        super().connect_custom_widgets()
        cross_section_table_edit_signal = self.cross_section_table.cellChanged
        cross_section_table_edit_slot = partial(self.edit_table_row, "cross_section_table")
        connect_signal(cross_section_table_edit_signal, cross_section_table_edit_slot)
        self.dialog.active_form_signals.add((cross_section_table_edit_signal, cross_section_table_edit_slot))
        self.cross_section_table_cell_changed_signal = cross_section_table_edit_signal
        self.cross_section_table_cell_changed_slot = cross_section_table_edit_slot

        add_signal = self.cross_section_table_add.clicked
        add_slot = self.add_table_row
        connect_signal(add_signal, add_slot)
        self.dialog.active_form_signals.add((add_signal, add_slot))

        delete_signal = self.cross_section_table_delete.clicked
        delete_slot = self.delete_table_rows
        connect_signal(delete_signal, delete_slot)
        self.dialog.active_form_signals.add((delete_signal, delete_slot))

        paste_signal = self.cross_section_table_paste.clicked
        paste_slot = self.paste_table_rows
        connect_signal(paste_signal, paste_slot)
        self.dialog.active_form_signals.add((paste_signal, paste_slot))
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            cross_section_friction_edit_signal = self.cross_section_friction.cellChanged
            cross_section_vegetation_edit_signal = self.cross_section_vegetation.cellChanged
            cross_section_friction_clear_signal = self.cross_section_friction_clear.clicked
            cross_section_vegetation_clear_signal = self.cross_section_vegetation_clear.clicked
            cross_section_friction_edit_slot = partial(self.edit_table_row, "cross_section_friction_table")
            cross_section_vegetation_edit_slot = partial(self.edit_table_row, "cross_section_vegetation_table")
            cross_section_friction_clear_slot = partial(self.clear_table_row_values, "cross_section_friction_table")
            cross_section_vegetation_clear_slot = partial(self.clear_table_row_values, "cross_section_vegetation_table")
            connect_signal(cross_section_friction_edit_signal, cross_section_friction_edit_slot)
            connect_signal(cross_section_vegetation_edit_signal, cross_section_vegetation_edit_slot)
            connect_signal(cross_section_friction_clear_signal, cross_section_friction_clear_slot)
            connect_signal(cross_section_vegetation_clear_signal, cross_section_vegetation_clear_slot)
            self.dialog.active_form_signals.add((cross_section_friction_edit_signal, cross_section_friction_edit_slot))
            self.dialog.active_form_signals.add(
                (cross_section_vegetation_edit_signal, cross_section_vegetation_edit_slot)
            )
            self.dialog.active_form_signals.add(
                (cross_section_friction_clear_signal, cross_section_friction_clear_slot)
            )
            self.dialog.active_form_signals.add(
                (cross_section_vegetation_clear_signal, cross_section_vegetation_clear_slot)
            )
            self.cross_section_friction_cell_changed_signal = cross_section_friction_edit_signal
            self.cross_section_friction_cell_changed_slot = cross_section_friction_edit_slot
            self.cross_section_vegetation_cell_changed_signal = cross_section_vegetation_edit_signal
            self.cross_section_vegetation_cell_changed_slot = cross_section_vegetation_edit_slot
            self.cross_section_friction_clear_signal = cross_section_friction_clear_signal
            self.cross_section_vegetation_clear_signal = cross_section_vegetation_clear_signal
            self.cross_section_friction_clear_slot = cross_section_friction_clear_slot
            self.cross_section_vegetation_clear_slot = cross_section_vegetation_clear_slot

    def get_cross_section_table_header(self, table_field_name):
        """Get the proper cross-section table header."""
        table_header = []
        if table_field_name == "cross_section_table":
            shape = self.get_widget_value(self.cross_section_shape)
            if shape == en.CrossSectionShape.YZ.value:
                table_header += ["Y [m]", "Z [m]"]
            else:
                table_header += ["Height [m]", "Width [m]"]
        elif table_field_name == "cross_section_friction_table":
            table_header += ["Friction coefficient"]
        elif table_field_name == "cross_section_vegetation_table":
            table_header += ["Stem density [m-2]", "Stem diameter [m]", "Height [m]", "Drag coefficient [-]"]
        else:
            pass
        return table_header

    def update_cross_section_table_header(self, table_field_name="cross_section_table"):
        """Update cross-section table headers."""
        table_widget = self.cross_section_table_field_widget_map[table_field_name]
        table_header = self.get_cross_section_table_header(table_field_name)
        table_widget.setHorizontalHeaderLabels(table_header)

    def get_cross_section_table_text(self, table_field_name="cross_section_table"):
        """Get cross-section table data as a string representation."""
        table_widget = self.cross_section_table_field_widget_map[table_field_name]
        num_of_rows = table_widget.rowCount()
        num_of_cols = table_widget.columnCount()
        cross_section_table_values = []
        for row_num in range(num_of_rows):
            values = []
            for col_num in range(num_of_cols):
                item = table_widget.item(row_num, col_num)
                if item is not None:
                    item_text = item.text().strip()
                else:
                    item_text = ""
                values.append(item_text)
            if all(values):
                cross_section_table_values.append(values)
        cross_section_table_str = "\n".join(", ".join(row) for row in cross_section_table_values)
        return cross_section_table_str

    def save_cross_section_table_edits(self, table_field_name="cross_section_table"):
        """Save cross-section table value to the feature attribute."""
        cross_section_table_str = self.get_cross_section_table_text(table_field_name)
        if self.creation is True:
            self.current_cross_section_location[table_field_name] = cross_section_table_str
        else:
            cross_section_table_idx = self.layer_with_xs_fields.lookupField(table_field_name)
            changes = {cross_section_table_idx: cross_section_table_str}
            self.layer_with_xs.changeAttributeValues(self.current_cross_section_location.id(), changes)

    def edit_table_row(self, table_field_name):
        """Slot for handling table cells edits."""
        self.save_cross_section_table_edits(table_field_name)

    def add_table_row(self):
        """Slot for handling new row addition."""
        selected_rows = {idx.row() for idx in self.cross_section_table.selectedIndexes()}
        if selected_rows:
            last_row_number = max(selected_rows) + 1
        else:
            last_row_number = self.cross_section_table.rowCount()
        self.cross_section_table.insertRow(last_row_number)
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            frict_vege_last_row_number = last_row_number - 1
            self.cross_section_friction.insertRow(frict_vege_last_row_number)
            self.cross_section_vegetation.insertRow(frict_vege_last_row_number)

    def delete_table_rows(self):
        """Slot for handling deletion of the selected rows."""
        selected_rows = {idx.row() for idx in self.cross_section_table.selectedIndexes()}
        for row_number in sorted(selected_rows, reverse=True):
            self.cross_section_table.removeRow(row_number)
            if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
                frict_vege_last_row_number = row_number - 1
                self.cross_section_friction.removeRow(frict_vege_last_row_number)
                self.cross_section_vegetation.removeRow(frict_vege_last_row_number)
        self.save_cross_section_table_edits()
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            self.save_cross_section_table_edits("cross_section_friction_table")
            self.save_cross_section_table_edits("cross_section_vegetation_table")

    def paste_table_rows(self):
        """Handling pasting new rows from the clipboard."""
        text = QApplication.clipboard().text()
        rows = text.split("\n")
        last_row_num = self.cross_section_table.rowCount()
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                disconnect_signal(cell_changed_signal, cell_changed_slot)
        for row in rows:
            try:
                height_str, width_str = row.replace(" ", "").split(",")
            except ValueError:
                continue
            self.cross_section_table.insertRow(last_row_num)
            self.cross_section_table.setItem(last_row_num, 0, QTableWidgetItem(height_str))
            self.cross_section_table.setItem(last_row_num, 1, QTableWidgetItem(width_str))
            if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
                frict_vege_last_row_number = last_row_num - 1
                self.cross_section_friction.insertRow(frict_vege_last_row_number)
                self.cross_section_vegetation.insertRow(frict_vege_last_row_number)
            last_row_num += 1
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                connect_signal(cell_changed_signal, cell_changed_slot)
        self.save_cross_section_table_edits()

    def clear_table_row_values(self, table_field_name):
        """Slot for clearing table values."""
        table_widget = self.cross_section_table_field_widget_map[table_field_name]
        num_of_rows = table_widget.rowCount()
        num_of_cols = table_widget.columnCount()
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                disconnect_signal(cell_changed_signal, cell_changed_slot)
        for row_num in range(num_of_rows):
            for col_num in range(num_of_cols):
                table_widget.setItem(row_num, col_num, QTableWidgetItem(""))
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                connect_signal(cell_changed_signal, cell_changed_slot)
        self.save_cross_section_table_edits(table_field_name)

    def populate_cross_section_table_data(self):
        """Populate cross-section tabular data in the table widget."""
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                disconnect_signal(cell_changed_signal, cell_changed_slot)
        leading_table_name = "cross_section_table"
        table = self.current_cross_section_location[leading_table_name] or ""
        number_of_rows_main = len(table.split("\n"))
        for table_field_name, table_widget in self.cross_section_table_field_widget_map.items():
            if table_widget is None:
                continue
            table_header = self.get_cross_section_table_header(table_field_name)
            table_columns_count = len(table_header)
            table_widget.clearContents()
            table_widget.setRowCount(0)
            table_widget.setColumnCount(table_columns_count)
            self.update_cross_section_table_header(table_field_name)
            for column_idx in range(table_columns_count):
                table_widget.setItemDelegateForColumn(column_idx, NumericItemDelegate(table_widget))
            for row_num_main in range(number_of_rows_main):
                table_widget.insertRow(row_num_main if table_field_name == leading_table_name else row_num_main - 1)
            if self.current_cross_section_location is not None:
                table = self.current_cross_section_location[table_field_name] or ""
            else:
                table = ""
            for row_number, row in enumerate(table.split("\n")):
                row_values = [val for val in row.replace(" ", "").split(",") if val]
                if len(row_values) != table_columns_count:
                    continue
                for col_idx, row_value in enumerate(row_values):
                    table_widget.setItem(row_number, col_idx, QTableWidgetItem(row_value))
        for cell_changed_signal, cell_changed_slot in self.cross_section_table_edit_slot_signal_pairs:
            if cell_changed_signal is not None and cell_changed_slot is not None:
                connect_signal(cell_changed_signal, cell_changed_slot)

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_cross_section_table_data()

    def activate_field_based_conditions(self):
        """Activate filed based conditions."""
        shape_widget = self.dialog.findChild(QObject, f"{self.cross_section_prefix}cross_section_shape")
        friction_widget = self.dialog.findChild(QObject, f"{self.cross_section_prefix}friction_type")
        if shape_widget is not None:
            shape_edit_signal = self.get_widget_editing_signal(shape_widget)
            shape_edit_slot = partial(
                setup_cross_section_definition_widgets, self, shape_widget, friction_widget, self.cross_section_prefix
            )
            connect_signal(shape_edit_signal, shape_edit_slot)
            self.dialog.active_form_signals.add((shape_edit_signal, shape_edit_slot))
        if friction_widget is not None:
            friction_edit_signal = self.get_widget_editing_signal(friction_widget)
            friction_edit_slot = partial(
                setup_friction_and_vegetation_widgets,
                self,
                shape_widget,
                friction_widget,
                self.cross_section_prefix,
            )
            connect_signal(friction_edit_signal, friction_edit_slot)
            self.dialog.active_form_signals.add((friction_edit_signal, friction_edit_slot))


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


class PipeForm(FormWithStartEndNode, FormWithXSTable):
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
        self.populate_cross_section_table_data()


class WeirForm(FormWithStartEndNode, FormWithXSTable):
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
        self.populate_cross_section_table_data()


class CulvertForm(FormWithStartEndNode, FormWithXSTable):
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
        self.populate_cross_section_table_data()


class OrificeForm(FormWithStartEndNode, FormWithXSTable):
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
        self.populate_cross_section_table_data()


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


class ChannelForm(FormWithStartEndNode, FormWithXSTable):
    """Channel user layer edit form logic."""

    MODEL = dm.Channel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.cross_section_locations = None
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
            self.populate_cross_section_table_data()
        setup_cross_section_widgets(self, self.cross_section_shape, self.cross_section_prefix)

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
        super().connect_custom_widgets()
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
        self.populate_cross_section_table_data()


class CrossSectionLocationForm(FormWithXSTable):
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
        channel_feat = find_point_polyline(point, channel_layer)
        if channel_feat:
            channel_id = channel_feat["id"]
            channel_geom = channel_feat.geometry()
            point_distance_on_channel = channel_geom.lineLocatePoint(point_geom)
            other_cross_sections = self.handler.get_multiple_feats_by_id(channel_id, "channel_id")
            other_cross_sections_num = len(other_cross_sections)
            cross_section_num = other_cross_sections_num + 1
            channel_code = channel_feat["code"]
            cross_section_location_code = f"{channel_code}_cross_section_{cross_section_num}"
            self.feature["channel_id"] = channel_id
            self.feature["code"] = cross_section_location_code
            self.channel = channel_feat
            if other_cross_sections:
                new_feat_with_distance = (self.feature, point_distance_on_channel)
                cross_sections_with_distance = [
                    (feat, channel_geom.lineLocatePoint(feat.geometry())) for feat in other_cross_sections
                ]
                cross_sections_with_distance.append(new_feat_with_distance)
                cross_sections_with_distance.sort(key=itemgetter(-1))
                new_feat_index = cross_sections_with_distance.index(new_feat_with_distance)
                near_cross_sections_fields = ["reference_level", "bank_level", "friction_value"]
                near_cross_sections_values = {}
                if new_feat_index == 0:
                    # New cross-section is first along channel
                    closest_existing_cross_section, closest_xs_distance = cross_sections_with_distance[1]
                    for field_name in near_cross_sections_fields:
                        near_cross_sections_values[field_name] = closest_existing_cross_section[field_name]
                elif new_feat_index == other_cross_sections_num:
                    # New cross-section is last along channel
                    closest_existing_cross_section, closest_xs_distance = cross_sections_with_distance[-2]
                    for field_name in near_cross_sections_fields:
                        near_cross_sections_values[field_name] = closest_existing_cross_section[field_name]
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
                    for field_name in near_cross_sections_fields:
                        before_value = before_xs[field_name]
                        after_value = after_xs[field_name]
                        if before_value != NULL and after_value != NULL:
                            value = round(
                                before_value + ((after_value - before_value) * interpolation_coefficient),
                                3,
                            )
                        elif before_value != NULL and after_value == NULL:
                            value = before_value
                        elif before_value == NULL and after_value != NULL:
                            value = after_value
                        else:
                            value = NULL
                        near_cross_sections_values[field_name] = value
                # Set selected values based on near cross-section characteristics
                for field_name, field_value in near_cross_sections_values.items():
                    self.feature[field_name] = field_value
                for xs_field_name in [
                    "cross_section_shape",
                    "cross_section_width",
                    "cross_section_height",
                    "cross_section_table",
                    "cross_section_friction_table",
                    "cross_section_vegetation_table",
                ]:
                    self.feature[xs_field_name] = closest_existing_cross_section[xs_field_name]
        try:
            global_settings_feat = next(global_settings_layer.getFeatures())
            self.feature["friction_type"] = global_settings_feat["frict_type"]
        except StopIteration:
            pass


class PotentialBreachForm(BaseForm):
    """Potential breach user layer edit form logic."""

    MODEL = dm.PotentialBreach

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
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        channel_layer = channel_handler.layer
        line_geom = self.feature.geometry()
        start_point = line_geom.asPolyline()[0]
        channel_node_feat = find_point_polyline(start_point, channel_layer)
        if channel_node_feat:
            channel_id = channel_node_feat["id"]
            self.feature["channel_id"] = channel_id
            self.channel = channel_node_feat

    def populate_with_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()


class ExchangeLineForm(BaseForm):
    """Exchange line user layer edit form logic."""

    MODEL = dm.ExchangeLine

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

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
    PotentialBreachForm,
    ExchangeLineForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
