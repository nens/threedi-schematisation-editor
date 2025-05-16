# Copyright (C) 2025 by Lutra Consulting
import sys
from collections import defaultdict
from enum import Enum
from functools import cached_property, partial
from operator import itemgetter
from types import MappingProxyType

from qgis.core import NULL, QgsGeometry
from qgis.gui import QgsCheckableComboBox, QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
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
    setup_cross_section_definition_widgets,
    setup_cross_section_widgets,
    setup_friction_and_vegetation_widgets,
)

field_types_widgets = MappingProxyType(
    {
        bool: QCheckBox,
        int: QgsSpinBox,
        float: QgsDoubleSpinBox,
        str: QLineEdit,
    }
)


class AbstractBaseForm(QObject):
    """Base edit form for user layers edit form logic."""

    MODEL = None
    MIN_FID = -sys.maxsize - 1
    AUTOGENERATE_ID = "Autogenerate"

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

    def purge_form_dialog_signals(self):
        """Remove all signals created by this form."""
        for signal, slot in self.dialog.active_form_signals:
            disconnect_signal(signal, slot)
        self.dialog.active_form_signals.clear()

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {}
        return fm_features

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        for field, customisation_fn in self.handler.FORM_CUSTOMIZATIONS.items():
            widget = self.dialog.findChild(QObject, field)
            customisation_fn(widget)
        if self.feature is None:
            return
        fid = self.feature.id()
        if fid < 0:
            try:
                feature_id = self.feature["id"]
            except KeyError:
                return  # form open for an invalid feature
            self.creation = feature_id == self.AUTOGENERATE_ID
            self.handler.set_feature_values(self.feature)
        self.activate_field_based_conditions()
        self.toggle_edit_mode()
        self.populate_with_extra_widgets()
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
        start_end_modifier is used when there are multiple features edited in the form, for example two connection nodes
         in a pipe form. The modifier should be 1 for starting point and 2 for ending.
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
                    edit_signal = self.get_widget_editing_signal(widget)
                    edit_slot = partial(self.set_validation_background, widget, field_type)
                    connect_signal(edit_signal, edit_slot)
                    self.dialog.active_form_signals.add((edit_signal, edit_slot))
                    self.set_validation_background(widget, field_type)
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


class AbstractFormWithTag(AbstractBaseForm):
    """Base edit form for user layers with tags table reference."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.tags_widget = None
        self.setup_tag_widgets()

    @cached_property
    def all_tags_data(self):
        """Return all available tags data."""
        tags_handler = self.layer_manager.model_handlers[dm.Tag]
        tags_layer = tags_handler.layer
        tags_data = {tag_feat["id"]: tag_feat["description"] for tag_feat in tags_layer.getFeatures()}
        return tags_data

    @property
    def assigned_tag_ids(self):
        """Return all tag IDs assigned to the feature."""
        try:
            assigned_tag_ids_str = self.feature["tags"]
            assigned_tag_ids = (
                [int(tag_id) for tag_id in assigned_tag_ids_str.split(",")] if assigned_tag_ids_str else []
            )
        except KeyError:
            assigned_tag_ids = []
        return assigned_tag_ids

    @property
    def selected_tag_ids(self):
        """Return current tag IDs selected in the form."""
        return ",".join(self.tags_widget.checkedItemsData())

    def setup_tag_widgets(self):
        """Setup tag widgets."""
        tags_widget_name = "add_remove_tags"
        self.tags_widget = self.dialog.findChild(QObject, tags_widget_name)
        if self.tags_widget is None:
            tags_layout = self.dialog.findChild(QObject, "tags_layout")
            self.tags_widget = QgsCheckableComboBox()
            self.tags_widget.setObjectName(tags_widget_name)
            self.tags_widget.setDefaultText("Click to assign tags...")
            tags_layout.addWidget(self.tags_widget)
        self.custom_widgets[tags_widget_name] = self.tags_widget

    def connect_custom_widgets(self):
        """Connect other widgets."""
        super().connect_custom_widgets()
        connect_signal(self.tags_widget.checkedItemsChanged, self.save_tag_edits)
        self.dialog.active_form_signals.add((self.tags_widget.checkedItemsChanged, self.save_tag_edits))

    def save_tag_edits(self):
        """Save tag references to the feature attribute."""
        if self.creation is True:
            self.feature["tags"] = self.selected_tag_ids
        else:
            tags_idx = self.layer.fields().lookupField("tags")
            changes = {tags_idx: self.selected_tag_ids}
            self.layer.changeAttributeValues(self.feature.id(), changes)

    def populate_tag_widgets(self):
        """Populate tag widgets."""
        disconnect_signal(self.tags_widget.checkedItemsChanged, self.save_tag_edits)
        self.tags_widget.clear()
        for tag_id, tag_description in self.all_tags_data.items():
            tag_text = f"{tag_id}: {tag_description}"
            check_state = Qt.Checked if tag_id in self.assigned_tag_ids else Qt.Unchecked
            self.tags_widget.addItemWithCheckState(text=tag_text, state=check_state, userData=tag_id)
        connect_signal(self.tags_widget.checkedItemsChanged, self.save_tag_edits)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class AbstractFormWithDistribution(AbstractBaseForm):
    """Base edit form for user layers with distribution table."""

    NUMBER_OF_ROWS = 24

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.distribution_table_field_name = "distribution"
        self.distribution_table = None
        self.distribution_table_clear = None
        self.setup_distribution_table_widgets()

    @property
    def table_header(self):
        return ["%"]

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        super().setup_form_widgets()
        self.update_distribution_table_header()

    def setup_distribution_table_widgets(self):
        """Setup distribution widgets."""
        distribution_table_widget_name = "distribution_table"
        self.distribution_table = self.dialog.findChild(QTableWidget, distribution_table_widget_name)
        # Somehow `cellChanged` signal keeps connected between feature switch within a form view
        disconnect_signal(self.distribution_table.cellChanged)
        self.distribution_table_clear = self.dialog.findChild(QPushButton, f"{distribution_table_widget_name}_clear")
        for widget in [self.distribution_table, self.distribution_table_clear]:
            self.custom_widgets[widget.objectName()] = self.distribution_table

    def connect_custom_widgets(self):
        """Connect other widgets."""
        super().connect_custom_widgets()
        connect_signal(self.distribution_table.cellChanged, self.save_distribution_table_edits)
        self.dialog.active_form_signals.add((self.distribution_table.cellChanged, self.save_distribution_table_edits))
        connect_signal(self.distribution_table_clear.clicked, self.clear_table_row_values)
        self.dialog.active_form_signals.add((self.distribution_table_clear.clicked, self.clear_table_row_values))

    def update_distribution_table_header(self):
        """Update distribution table headers."""
        self.distribution_table.setHorizontalHeaderLabels(self.table_header)

    def get_distribution_table_values(self):
        """Get distribution table values."""
        distribution_table_values = []
        for row_num in range(self.NUMBER_OF_ROWS):
            item = self.distribution_table.item(row_num, 0)
            row_value = item.text().strip() if item is not None else ""
            distribution_table_values.append(row_value)
        return distribution_table_values

    def get_distribution_table_text(self):
        """Get distribution table data as a string representation."""
        distribution_table_values = self.get_distribution_table_values()
        distribution_table_str = ",".join(row for row in distribution_table_values)
        return distribution_table_str

    def save_distribution_table_edits(self):
        """Slot for handling table cells edits."""
        distribution_table_str = self.get_distribution_table_text()
        if self.creation is True:
            self.feature[self.distribution_table_field_name] = distribution_table_str
        else:
            distribution_table_idx = self.layer.fields().lookupField(self.distribution_table_field_name)
            changes = {distribution_table_idx: distribution_table_str}
            self.layer.changeAttributeValues(self.feature.id(), changes)

    def clear_table_row_values(self):
        """Slot for clearing table values."""
        disconnect_signal(self.distribution_table.cellChanged, self.save_distribution_table_edits)
        for row_num in range(self.NUMBER_OF_ROWS):
            self.distribution_table.setItem(row_num, 0, QTableWidgetItem(""))
        self.save_distribution_table_edits()
        connect_signal(self.distribution_table.cellChanged, self.save_distribution_table_edits)

    def populate_distribution_table_data(self):
        """Populate distribution tabular data in the table widget."""
        disconnect_signal(self.distribution_table.cellChanged, self.save_distribution_table_edits)
        self.distribution_table.clearContents()
        self.distribution_table.setRowCount(self.NUMBER_OF_ROWS)
        self.distribution_table.setColumnCount(1)
        self.update_distribution_table_header()
        self.distribution_table.setItemDelegateForColumn(0, NumericItemDelegate(self.distribution_table))
        if self.feature is not None:
            table = self.feature[self.distribution_table_field_name] or ""
        else:
            table = ""
        for row_number, row_value in enumerate(table.split(",")):
            self.distribution_table.setItem(row_number, 0, QTableWidgetItem(row_value))
        connect_signal(self.distribution_table.cellChanged, self.save_distribution_table_edits)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_distribution_table_data()


class AbstractFormWithMaterial(AbstractBaseForm):
    """Base edit form for user layers with material table reference."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.material_id_field_name = "material_id"
        self.material_id_widget = self.dialog.findChild(QComboBox, self.material_id_field_name)
        connect_signal(self.material_id_widget.activated, self.update_material_friction)
        self.dialog.active_form_signals.add((self.material_id_widget.activated, self.update_material_friction))
        try:
            self.initial_material_id = self.feature[self.material_id_field_name]
        except KeyError:
            self.initial_material_id = None

    @cached_property
    def material_friction_widgets(self):
        """Return material friction widgets."""
        material_friction_widgets_map = {
            "friction_coefficient": self.dialog.findChild(QDoubleSpinBox, "friction_value"),
            "friction_type": self.dialog.findChild(QComboBox, "friction_type"),
        }
        return material_friction_widgets_map

    @cached_property
    def all_material_data(self):
        """Return all materials with characteristics."""
        material_handler = self.layer_manager.model_handlers[dm.Material]
        material_layer = material_handler.layer
        material_field_names = material_layer.fields().names()
        material_data = {
            material_feat["id"]: dict(zip(material_field_names, material_feat.attributes()))
            for material_feat in material_layer.getFeatures()
        }
        return material_data

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        super().setup_form_widgets()
        if self.creation is True:
            self.update_material_friction()

    def update_material_friction(self):
        """Update material friction widgets."""
        if self.feature is None or not self.feature.fields().names():
            return
        current_material_id = self.material_id_widget.currentData()
        if current_material_id not in self.all_material_data:
            return
        if current_material_id == self.initial_material_id:
            return
        current_material_data = self.all_material_data[current_material_id]
        for material_field_name, field_name_widget in self.material_friction_widgets.items():
            widget_value = current_material_data[material_field_name]
            self.set_widget_value(field_name_widget, widget_value)
        self.initial_material_id = self.feature[self.material_id_field_name]


class AbstractFormWithTable(AbstractBaseForm):
    """Base edit form for user layers with table."""

    TABLE_NAME = ""
    ROW_SEPARATOR = "\n"
    COLUMN_SEPARATOR = ","

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.table = None
        self.table_add = None
        self.table_delete = None
        self.table_copy = None
        self.table_paste = None
        self.setup_table_widgets()

    @property
    def table_header(self):
        """Return table header."""
        raise NotImplementedError("Table header not implemented.")

    def setup_form_widgets(self):
        """Setting up all form widgets."""
        super().setup_form_widgets()
        self.update_table_header()

    def setup_table_widgets(self):
        """Setup timeseries widgets."""
        table_widget_name = f"{self.TABLE_NAME}_table"
        self.table = self.dialog.findChild(QTableWidget, table_widget_name)
        # Somehow `cellChanged` signal keeps connected between feature switch within a form view
        disconnect_signal(self.table.cellChanged)
        self.table_add = self.dialog.findChild(QPushButton, f"{table_widget_name}_add")
        self.table_delete = self.dialog.findChild(QPushButton, f"{table_widget_name}_delete")
        self.table_copy = self.dialog.findChild(QPushButton, f"{table_widget_name}_copy")
        self.table_paste = self.dialog.findChild(QPushButton, f"{table_widget_name}_paste")
        for widget in [
            self.table,
            self.table_add,
            self.table_delete,
            self.table_copy,
            self.table_paste,
        ]:
            self.custom_widgets[widget.objectName()] = widget

    def connect_custom_widgets(self):
        """Connect other widgets."""
        super().connect_custom_widgets()
        connect_signal(self.table.cellChanged, self.save_table_edits)
        self.dialog.active_form_signals.add((self.table.cellChanged, self.save_table_edits))
        connect_signal(self.table_add.clicked, self.add_table_row)
        self.dialog.active_form_signals.add((self.table_add.clicked, self.add_table_row))
        connect_signal(self.table_delete.clicked, self.delete_table_rows)
        self.dialog.active_form_signals.add((self.table_delete.clicked, self.delete_table_rows))
        connect_signal(self.table_paste.clicked, self.paste_table_rows)
        self.dialog.active_form_signals.add((self.table_paste.clicked, self.paste_table_rows))
        connect_signal(self.table_copy.clicked, self.copy_table_rows)
        self.dialog.active_form_signals.add((self.table_copy.clicked, self.copy_table_rows))

    def update_table_header(self):
        """Update table headers."""
        self.table.setHorizontalHeaderLabels(self.table_header)

    def get_table_values(self):
        """Get table values."""
        num_of_rows = self.table.rowCount()
        num_of_cols = self.table.columnCount()
        table_values = []
        for row_num in range(num_of_rows):
            row_values = []
            for col_num in range(num_of_cols):
                item = self.table.item(row_num, col_num)
                if item is not None:
                    item_text = item.text().strip()
                else:
                    item_text = ""
                row_values.append(item_text)
            table_values.append(row_values)
        return table_values

    def get_table_text(self):
        """Get table data as a string representation."""
        table_values = self.get_table_values()
        table_str = self.ROW_SEPARATOR.join(self.COLUMN_SEPARATOR.join(row) for row in table_values)
        return table_str

    def save_table_edits(self):
        """Slot for handling table cells edits."""
        table_str = self.get_table_text()
        if self.creation is True:
            self.feature[self.TABLE_NAME] = table_str
        else:
            table_idx = self.layer.fields().lookupField(self.TABLE_NAME)
            changes = {table_idx: table_str}
            self.layer.changeAttributeValues(self.feature.id(), changes)

    def add_table_row(self):
        """Slot for handling new row addition."""
        selected_rows = {idx.row() for idx in self.table.selectedIndexes()}
        if selected_rows:
            last_row_number = max(selected_rows) + 1
        else:
            last_row_number = self.table.rowCount()
        self.table.insertRow(last_row_number)

    def delete_table_rows(self):
        """Slot for handling deletion of the selected rows."""
        selected_rows = {idx.row() for idx in self.table.selectedIndexes()}
        for row_number in sorted(selected_rows, reverse=True):
            self.table.removeRow(row_number)
        self.save_table_edits()

    def paste_table_rows(self):
        """Handling pasting new rows from the clipboard."""
        text = QApplication.clipboard().text()
        rows = text.split(self.ROW_SEPARATOR)
        last_row_num = self.table.rowCount()
        disconnect_signal(self.table.cellChanged, self.save_table_edits)
        for row in rows:
            try:
                height_str, width_str = row.replace(" ", "").split(self.COLUMN_SEPARATOR)
            except ValueError:
                continue
            self.table.insertRow(last_row_num)
            self.table.setItem(last_row_num, 0, QTableWidgetItem(height_str))
            self.table.setItem(last_row_num, 1, QTableWidgetItem(width_str))
            last_row_num += 1
        connect_signal(self.table.cellChanged, self.save_table_edits)
        self.save_table_edits()

    def copy_table_rows(self):
        """Slot for copying table values into the clipboard."""
        table_values = self.get_table_values()
        clipboard_values = "\n".join([",".join(row_values) for row_values in table_values])
        QApplication.clipboard().setText(clipboard_values)

    def clear_table_row_values(self):
        """Slot for clearing table values."""
        num_of_rows = self.table.rowCount()
        num_of_cols = self.table.columnCount()
        disconnect_signal(self.table.cellChanged, self.save_table_edits)
        for row_num in range(num_of_rows):
            for col_num in range(num_of_cols):
                self.table.setItem(row_num, col_num, QTableWidgetItem(""))
        connect_signal(self.table.cellChanged, self.save_table_edits)
        self.save_table_edits()

    def populate_table_data(self):
        """Populate timeseries tabular data in the table widget."""
        disconnect_signal(self.table.cellChanged, self.save_table_edits)
        table = self.feature[self.TABLE_NAME] or ""
        number_of_rows_main = len(table.split(self.ROW_SEPARATOR))
        table_columns_count = len(self.table_header)
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setColumnCount(table_columns_count)
        self.update_table_header()
        for column_idx in range(table_columns_count):
            self.table.setItemDelegateForColumn(column_idx, NumericItemDelegate(self.table))
        for row_num_main in range(number_of_rows_main):
            self.table.insertRow(row_num_main)
        if self.feature is not None:
            table = self.feature[self.TABLE_NAME] or ""
        else:
            table = ""
        for row_number, row in enumerate(table.split(self.ROW_SEPARATOR)):
            row_values = [val for val in row.replace(" ", "").split(self.COLUMN_SEPARATOR)]
            for col_idx, row_value in enumerate(row_values):
                self.table.setItem(row_number, col_idx, QTableWidgetItem(row_value))
        connect_signal(self.table.cellChanged, self.save_table_edits)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_table_data()


class AbstractFormWithTimeseries(AbstractFormWithTable):
    """Base edit form for user layers with timeseries table."""

    TABLE_NAME = "timeseries"

    @property
    def table_header(self):
        return ["Time", "Value"]


class AbstractFormWithActionTable(AbstractFormWithTable):
    """Base edit form for user layers with action table."""

    TABLE_NAME = "action_table"

    @property
    def table_header(self):
        return ["Measured value", "Action value 1", "Action value 2"]


class AbstractFormWithXSTable(AbstractBaseForm):
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
        self.cross_section_table_copy = None
        self.cross_section_friction_clear = None
        self.cross_section_vegetation_clear = None
        self.cross_section_friction_copy = None
        self.cross_section_vegetation_copy = None
        self.cross_section_table_cell_changed_signal = None
        self.cross_section_friction_cell_changed_signal = None
        self.cross_section_vegetation_cell_changed_signal = None
        self.cross_section_friction_clear_signal = None
        self.cross_section_vegetation_clear_signal = None
        self.cross_section_friction_copy_signal = None
        self.cross_section_vegetation_copy_signal = None
        self.cross_section_table_cell_changed_slot = None
        self.cross_section_friction_cell_changed_slot = None
        self.cross_section_vegetation_cell_changed_slot = None
        self.cross_section_friction_clear_slot = None
        self.cross_section_vegetation_clear_slot = None
        self.cross_section_friction_copy_slot = None
        self.cross_section_vegetation_copy_slot = None
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
            "cross_section_friction_values": self.cross_section_friction,
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
        xs_table_copy = f"{self.cross_section_prefix}cross_section_table_copy"
        self.cross_section_shape = self.dialog.findChild(QObject, f"{self.cross_section_prefix}cross_section_shape")
        self.cross_section_table = self.dialog.findChild(QTableWidget, xs_table)
        self.cross_section_table_add = self.dialog.findChild(QPushButton, xs_table_add)
        self.cross_section_table_delete = self.dialog.findChild(QPushButton, xs_table_delete)
        self.cross_section_table_paste = self.dialog.findChild(QPushButton, xs_table_paste)
        self.cross_section_table_copy = self.dialog.findChild(QPushButton, xs_table_copy)
        self.custom_widgets[xs_table] = self.cross_section_table
        self.custom_widgets[xs_table_add] = self.cross_section_table_add
        self.custom_widgets[xs_table_delete] = self.cross_section_table_delete
        self.custom_widgets[xs_table_paste] = self.cross_section_table_paste
        self.custom_widgets[xs_table_copy] = self.cross_section_table_copy
        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            xs_friction = f"{self.cross_section_prefix}cross_section_friction_widget"
            xs_vegetation = f"{self.cross_section_prefix}cross_section_vegetation_widget"
            xs_friction_clear = f"{self.cross_section_prefix}cross_section_friction_clear"
            xs_vegetation_clear = f"{self.cross_section_prefix}cross_section_vegetation_clear"
            xs_friction_copy = f"{self.cross_section_prefix}cross_section_friction_copy"
            xs_vegetation_copy = f"{self.cross_section_prefix}cross_section_vegetation_copy"
            self.cross_section_friction = self.dialog.findChild(QTableWidget, xs_friction)
            self.cross_section_vegetation = self.dialog.findChild(QTableWidget, xs_vegetation)
            self.cross_section_friction_clear = self.dialog.findChild(QPushButton, xs_friction_clear)
            self.cross_section_vegetation_clear = self.dialog.findChild(QPushButton, xs_vegetation_clear)
            self.cross_section_friction_copy = self.dialog.findChild(QPushButton, xs_friction_copy)
            self.cross_section_vegetation_copy = self.dialog.findChild(QPushButton, xs_vegetation_copy)
            self.custom_widgets[xs_friction] = self.cross_section_friction
            self.custom_widgets[xs_vegetation] = self.cross_section_vegetation
            self.custom_widgets[xs_friction_clear] = self.cross_section_friction_clear
            self.custom_widgets[xs_vegetation_clear] = self.cross_section_vegetation_clear
            self.custom_widgets[xs_friction_copy] = self.cross_section_friction_copy
            self.custom_widgets[xs_vegetation_copy] = self.cross_section_vegetation_copy

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

        copy_signal = self.cross_section_table_copy.clicked
        copy_slot = partial(self.copy_table_rows, "cross_section_table")
        connect_signal(copy_signal, copy_slot)
        self.dialog.active_form_signals.add((copy_signal, copy_slot))

        if self.MODEL in [dm.CrossSectionLocation, dm.Channel]:
            cross_section_friction_edit_signal = self.cross_section_friction.cellChanged
            cross_section_vegetation_edit_signal = self.cross_section_vegetation.cellChanged
            cross_section_friction_clear_signal = self.cross_section_friction_clear.clicked
            cross_section_vegetation_clear_signal = self.cross_section_vegetation_clear.clicked
            cross_section_friction_copy_signal = self.cross_section_friction_copy.clicked
            cross_section_vegetation_copy_signal = self.cross_section_vegetation_copy.clicked
            cross_section_friction_edit_slot = partial(self.edit_table_row, "cross_section_friction_values")
            cross_section_vegetation_edit_slot = partial(self.edit_table_row, "cross_section_vegetation_table")
            cross_section_friction_clear_slot = partial(self.clear_table_row_values, "cross_section_friction_values")
            cross_section_vegetation_clear_slot = partial(self.clear_table_row_values, "cross_section_vegetation_table")
            cross_section_friction_copy_slot = partial(self.copy_table_rows, "cross_section_friction_values")
            cross_section_vegetation_copy_slot = partial(self.copy_table_rows, "cross_section_vegetation_table")
            connect_signal(cross_section_friction_edit_signal, cross_section_friction_edit_slot)
            connect_signal(cross_section_vegetation_edit_signal, cross_section_vegetation_edit_slot)
            connect_signal(cross_section_friction_clear_signal, cross_section_friction_clear_slot)
            connect_signal(cross_section_vegetation_clear_signal, cross_section_vegetation_clear_slot)
            connect_signal(cross_section_friction_copy_signal, cross_section_friction_copy_slot)
            connect_signal(cross_section_vegetation_copy_signal, cross_section_vegetation_copy_slot)
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
            self.dialog.active_form_signals.add((cross_section_friction_copy_signal, cross_section_friction_copy_slot))
            self.dialog.active_form_signals.add(
                (cross_section_vegetation_copy_signal, cross_section_vegetation_copy_slot)
            )
            self.cross_section_friction_cell_changed_signal = cross_section_friction_edit_signal
            self.cross_section_friction_cell_changed_slot = cross_section_friction_edit_slot
            self.cross_section_vegetation_cell_changed_signal = cross_section_vegetation_edit_signal
            self.cross_section_vegetation_cell_changed_slot = cross_section_vegetation_edit_slot
            self.cross_section_friction_clear_signal = cross_section_friction_clear_signal
            self.cross_section_vegetation_clear_signal = cross_section_vegetation_clear_signal
            self.cross_section_friction_clear_slot = cross_section_friction_clear_slot
            self.cross_section_vegetation_clear_slot = cross_section_vegetation_clear_slot
            self.cross_section_friction_copy_signal = cross_section_friction_copy_signal
            self.cross_section_vegetation_copy_signal = cross_section_vegetation_copy_signal
            self.cross_section_friction_copy_slot = cross_section_friction_copy_slot
            self.cross_section_vegetation_copy_slot = cross_section_vegetation_copy_slot

    def get_cross_section_table_header(self, table_field_name):
        """Get the proper cross-section table header."""
        table_header = []
        if table_field_name == "cross_section_table":
            shape = self.get_widget_value(self.cross_section_shape)
            if shape == en.CrossSectionShape.YZ.value:
                table_header += ["Y [m]", "Z [m]"]
            else:
                table_header += ["Height [m]", "Width [m]"]
        elif table_field_name == "cross_section_friction_values":
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

    def get_cross_section_table_values(self, table_field_name="cross_section_table"):
        """Get cross-section table values."""
        table_widget = self.cross_section_table_field_widget_map[table_field_name]
        num_of_rows = table_widget.rowCount()
        num_of_cols = table_widget.columnCount()
        cross_section_table_values = []
        for row_num in range(num_of_rows):
            row_values = []
            for col_num in range(num_of_cols):
                item = table_widget.item(row_num, col_num)
                if item is not None:
                    item_text = item.text().strip()
                else:
                    item_text = ""
                row_values.append(item_text)
            cross_section_table_values.append(row_values)
        return cross_section_table_values

    def get_cross_section_table_text(self, table_field_name="cross_section_table"):
        """Get cross-section table data as a string representation."""
        cross_section_table_values = self.get_cross_section_table_values(table_field_name)
        cross_section_table_str = "\n".join(", ".join(row) for row in cross_section_table_values if all(row))
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
            frict_vegetation_last_row_number = last_row_number - 1
            self.cross_section_friction.insertRow(frict_vegetation_last_row_number)
            self.cross_section_vegetation.insertRow(frict_vegetation_last_row_number)

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
            self.save_cross_section_table_edits("cross_section_friction_values")
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

    def copy_table_rows(self, table_field_name):
        """Slot for copying table values into the clipboard."""
        cross_section_table_values = self.get_cross_section_table_values(table_field_name)
        clipboard_values = "\n".join([",".join(row_values) for row_values in cross_section_table_values])
        QApplication.clipboard().setText(clipboard_values)

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
        """Populate basic and extra widgets for the given custom form."""
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
        if friction_widget is not None and self.MODEL in {dm.Channel, dm.CrossSectionLocation}:
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


class AbstractFormWithNode(AbstractBaseForm):
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
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_node_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_connection_node_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class AbstractFormWithStartEndNode(AbstractBaseForm):
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
        connection_node_id_start = self.feature["connection_node_id_start"]
        connection_node_id_end = self.feature["connection_node_id_end"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_id_start)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_id_end)

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
        connection_node_id_start = self.connection_node_start["id"]
        connection_node_id_end = self.connection_node_end["id"]
        connection_node_start_code = self.connection_node_start["code"]
        connection_node_end_code = self.connection_node_end["code"]
        self.feature["connection_node_id_start"] = connection_node_id_start
        self.feature["connection_node_id_end"] = connection_node_id_end
        if connection_node_start_code and connection_node_end_code:
            code_display_name = f"{connection_node_start_code}-{connection_node_end_code}"
        else:
            code_display_name = None
        try:
            self.feature["code"] = code_display_name
            self.feature["display_name"] = code_display_name
        except KeyError:
            pass  # Some layers might not have code and display name

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class AbstractNodeToSurfaceMapForm(AbstractFormWithTag):
    """Basic surface to node map edit form logic."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = None
        self.surface_id_field = None
        self.surface_feature = None

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
        if self.surface_feature is None:
            self.surface_feature = find_point_polygons(start_point, surface_layer)
        if self.surface_feature is not None:
            self.feature[self.surface_id_field] = self.surface_feature["id"]

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.surface_feature = self.select_start_surface()
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


class AbstractFormWithTargetStructure(AbstractBaseForm):
    """Base edit form for user layers with a single structure."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.structure_feature = None
        self.structure_feature_type = None

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        if self.structure_feature is not None:
            self.feature["target_type"] = self.structure_feature_type
            self.feature["target_id"] = self.structure_feature["id"]

    @cached_property
    def target_structure_types(self):
        """Return supported target structure type data models."""
        target_structure_data_models = {
            model_cls.__tablename__: model_cls for model_cls in [dm.Weir, dm.Orifice, dm.Pump]
        }
        return target_structure_data_models

    def setup_target_structure_on_edit(self):
        """Setting up target structure during editing feature."""
        try:
            target_structure_type = self.target_structure_types[self.feature["target_type"]]
            model_cls = self.target_structure_types[target_structure_type]
            structure_handler = self.layer_manager.model_handlers[model_cls]
            structure_feat = structure_handler.get_feat_by_id(self.feature["target_id"])
        except KeyError:
            return
        self.structure_feature = structure_feat
        self.structure_feature_type = target_structure_type

    def setup_target_structure_on_creation(self):
        """Setting up target structure during adding feature."""
        feature_point = self.feature.geometry().asPoint()
        for structure_type, model_cls in self.target_structure_types.items():
            structure_handler = self.layer_manager.model_handlers[model_cls]
            structure_layer = structure_handler.layer
            dm_geometry_type = model_cls.__geometrytype__
            if dm_geometry_type == en.GeometryType.Point:
                structure_feat = find_point_nodes(feature_point, structure_layer)
            elif dm_geometry_type == en.GeometryType.Linestring:
                structure_feat = find_point_polyline(feature_point, structure_layer)
            else:
                continue
            if structure_feat is not None:
                self.structure_feature, self.structure_feature_type = structure_feat, structure_type
                break

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_target_structure_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_target_structure_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()


class ConnectionNodeForm(AbstractFormWithTag):
    """Connection node edit form logic."""

    MODEL = dm.ConnectionNode


class PipeForm(AbstractFormWithStartEndNode, AbstractFormWithXSTable, AbstractFormWithTag, AbstractFormWithMaterial):
    """Pipe user layer edit form logic."""

    MODEL = dm.Pipe

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
        self.feature["invert_level_start"] = self.connection_node_start["bottom_level"]
        self.feature["invert_level_end"] = self.connection_node_end["bottom_level"]

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_cross_section_table_data()
        self.populate_tag_widgets()


class WeirForm(AbstractFormWithStartEndNode, AbstractFormWithXSTable, AbstractFormWithTag, AbstractFormWithMaterial):
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
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_cross_section_table_data()
        self.populate_tag_widgets()


class CulvertForm(AbstractFormWithStartEndNode, AbstractFormWithXSTable, AbstractFormWithTag, AbstractFormWithMaterial):
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
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_cross_section_table_data()
        self.populate_tag_widgets()


class OrificeForm(AbstractFormWithStartEndNode, AbstractFormWithXSTable, AbstractFormWithTag, AbstractFormWithMaterial):
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
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_nodes_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_nodes_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_cross_section_table_data()
        self.populate_tag_widgets()


class PumpForm(AbstractFormWithNode, AbstractFormWithTag):
    """Pump without end node user layer edit form logic."""

    MODEL = dm.Pump

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class PumpMapForm(AbstractFormWithTag):
    """Pump with end node user layer edit form logic."""

    MODEL = dm.PumpMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.connection_node_end = None
        self.pump = None

    @property
    def foreign_models_features(self):
        """Property returning dictionary where key = data model class with identifier and value = data model feature."""
        fm_features = {
            (dm.ConnectionNode, None): self.connection_node_end,
            (dm.Pump, None): self.pump,
        }
        return fm_features

    def setup_pump_on_edit(self):
        """Setting up pump during editing feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pump_handler = self.layer_manager.model_handlers[dm.Pump]
        connection_node_id_end = self.feature["connection_node_id_end"]
        pump_id = self.feature["pump_id"]
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_id_end)
        self.pump = pump_handler.get_feat_by_id(pump_id)

    def setup_pump_on_creation(self):
        """Setting up pump during adding feature."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        pump_handler = self.layer_manager.model_handlers[dm.Pump]
        connection_node_layer = connection_node_handler.layer
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, connection_node_layer)
        start_pump_feat = self.pump
        if start_pump_feat is None:
            start_geom = QgsGeometry.fromPointXY(start_point)
            if start_connection_node_feat is None:
                start_pump_feat, start_connection_node_feat = pump_handler.create_pump_with_connection_node(start_geom)
                self.extra_features[connection_node_handler].append(start_connection_node_feat)
            else:
                start_pump_feat = pump_handler.create_new_feature(start_geom)
                start_pump_feat["connection_node_id"] = start_connection_node_feat["id"]
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                self.extra_features[connection_node_handler].append(end_connection_node_feat)
            self.extra_features[pump_handler].append(start_pump_feat)
        else:
            if end_connection_node_feat is None:
                end_geom = QgsGeometry.fromPointXY(end_point)
                end_connection_node_feat = connection_node_handler.create_new_feature_from_template(
                    start_connection_node_feat, geometry=end_geom
                )
                self.extra_features[connection_node_handler].append(end_connection_node_feat)
        # Assign features as a form instance attributes.
        self.connection_node_end = end_connection_node_feat
        self.pump = start_pump_feat
        self.sequence_related_features_ids()

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        self.feature["pump_id"] = self.pump["id"]
        self.feature["connection_node_id_end"] = self.connection_node_end["id"]

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.pump = self.select_start_pump()
            self.setup_pump_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_pump_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_tag_widgets()

    def select_start_pump(self):
        """Selecting start pump"""
        title = "Select start pump"
        message = "pumps at location"
        linestring = self.feature.geometry().asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        pump_handler = self.layer_manager.model_handlers[dm.Pump]
        pump_layer = pump_handler.layer
        start_pump_feats = find_point_nodes(start_point, pump_layer, allow_multiple=True)
        pump_no = len(start_pump_feats)
        if pump_no == 0:
            pump_feat = None
        elif pump_no == 1:
            pump_feat = next(iter(start_pump_feats))
        else:
            pump_feats_by_id = {feat["id"]: feat for feat in start_pump_feats}
            pump_entries = [f"{feat_id} ({feat['display_name']})" for feat_id, feat in pump_feats_by_id.items()]
            pump_entry = self.uc.pick_item(title, message, None, *pump_entries)
            pump_id = int(pump_entry.split()[0]) if pump_entry else None
            pump_feat = pump_feats_by_id[pump_id] if pump_id else None
        return pump_feat


class SurfaceForm(AbstractFormWithTag):
    """Surface user layer edit form logic."""

    MODEL = dm.Surface

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class SurfaceMapForm(AbstractNodeToSurfaceMapForm, AbstractFormWithTag):
    """Surface Map user layer edit form logic."""

    MODEL = dm.SurfaceMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = dm.Surface
        self.surface_id_field = "surface_id"


class DryWeatherFlowForm(AbstractFormWithTag):
    """Dry weather flow user layer edit form logic."""

    MODEL = dm.DryWeatherFlow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)


class DryWeatherFlowMapForm(AbstractNodeToSurfaceMapForm, AbstractFormWithTag):
    """Dry weather flow Map user layer edit form logic."""

    MODEL = dm.DryWeatherFlowMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.surface_model = dm.DryWeatherFlow
        self.surface_id_field = "dry_weather_flow_id"


class DryWeatherFlowDistributionForm(AbstractFormWithTag, AbstractFormWithDistribution):
    """Dry weather flow Distribution user layer edit form logic."""

    MODEL = dm.DryWeatherFlowDistribution

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        # Populate widgets based on features attributes
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_distribution_table_data()
        self.populate_tag_widgets()


class ChannelForm(AbstractFormWithStartEndNode, AbstractFormWithXSTable, AbstractFormWithTag):
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
        connection_node_id_start = self.feature["connection_node_id_start"]
        connection_node_id_end = self.feature["connection_node_id_end"]
        channel_id = self.feature["id"]
        self.connection_node_start = connection_node_handler.get_feat_by_id(connection_node_id_start)
        self.connection_node_end = connection_node_handler.get_feat_by_id(connection_node_id_end)
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
        global_settings_handler = self.layer_manager.model_handlers[dm.ModelSettings]
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
            self.current_cross_section_location["friction_type"] = global_settings_feat["friction_type"]

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
        """Populate basic and extra widgets for the given custom form."""
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
        self.populate_tag_widgets()


class CrossSectionLocationForm(AbstractFormWithXSTable):
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
        global_settings_handler = self.layer_manager.model_handlers[dm.ModelSettings]
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
                    "cross_section_friction_values",
                    "cross_section_vegetation_table",
                ]:
                    self.feature[xs_field_name] = closest_existing_cross_section[xs_field_name]
        try:
            global_settings_feat = next(global_settings_layer.getFeatures())
            self.feature["friction_type"] = global_settings_feat["friction_type"]
        except StopIteration:
            pass


class PotentialBreachForm(AbstractFormWithTag):
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
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class ExchangeLineForm(AbstractFormWithTag):
    """Exchange line user layer edit form logic."""

    MODEL = dm.ExchangeLine

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class BoundaryCondition1D(AbstractFormWithTag, AbstractFormWithNode, AbstractFormWithTimeseries):
    """Boundary Condition 1D user layer edit form logic."""

    MODEL = dm.BoundaryCondition1D

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_node_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_node_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_table_data()
        self.populate_tag_widgets()


class BoundaryCondition2D(AbstractFormWithTag, AbstractFormWithTimeseries):
    """Boundary Condition 2D user layer edit form logic."""

    MODEL = dm.BoundaryCondition2D

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_table_data()
        self.populate_tag_widgets()


class Lateral1D(AbstractFormWithTag, AbstractFormWithNode, AbstractFormWithTimeseries):
    """Lateral 1D user layer edit form logic."""

    MODEL = dm.Lateral1D

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_connection_node_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_connection_node_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_table_data()
        self.populate_tag_widgets()


class Lateral2D(AbstractFormWithTag, AbstractFormWithTimeseries):
    """Lateral 2D user layer edit form logic."""

    MODEL = dm.Lateral2D

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_table_data()
        self.populate_tag_widgets()


class MeasureLocation(AbstractFormWithNode, AbstractFormWithTag):
    """Measure Location user layer edit form logic."""

    MODEL = dm.MeasureLocation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

def map_action_type_to_labels(action_type_str: str):
    if action_type_str == en.ActionType.SET_DISCHARGE_COEFFICIENTS.value.capitalize().replace("_", " "):
        return ("Discharge coefficient positive [-]", "Discharge coefficient negative [-]")
    elif action_type_str == en.ActionType.SET_CREST_LEVEL.value.capitalize().replace("_", " "):
        return ("Crest level [m MSL]", "")
    elif action_type_str == en.ActionType.SET_GATE_LEVEL.value.capitalize().replace("_", " "):
        return ("Gate level [m MSL]", "")
    elif action_type_str == en.ActionType.SET_PUMP_CAPACITY.value.capitalize().replace("_", " "):
        return ("Pump capacity [L/s]", "")
    else:
        raise NotImplementedError(f"Unsupported action type: {action_type_str}")


class MemoryControl(AbstractFormWithTargetStructure, AbstractFormWithTag):
    """Memory Control user layer edit form logic."""

    MODEL = dm.MemoryControl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        action_type_widget = self.dialog.findChild(QComboBox, "action_type")
        action_type_widget.currentIndexChanged.connect(self.update_actions)
        self.dialog.active_form_signals.add((action_type_widget, self.update_actions))
        self.update_actions()

    def update_actions(self):
        action_type_widget = self.dialog.findChild(QComboBox, "action_type")
        action_value_1_label = self.dialog.findChild(QLabel, "action_value_1_label")
        action_value_2_label = self.dialog.findChild(QLabel, "action_value_2_label")
        action_value_2 = self.dialog.findChild(QDoubleSpinBox, "action_value_2")

        action_type_str = action_type_widget.currentText()
        if action_type_str == "(NULL)":
            # Just set the default values
            action_value_1_label.setText("Action value 1")
            action_value_2_label.setText("Action value 2")
            return

        if action_type_str != en.ActionType.SET_DISCHARGE_COEFFICIENTS.value.capitalize().replace("_", " "):
            # If action type is anything other than "set_discharge_coefficients", disable action value 2
            action_value_2.setValue(0.0) # TODO: also fires save_table_edits?
            action_value_2.setEnabled(False) 
        else:
            action_value_2.setEnabled(True)

        label1, label2 = map_action_type_to_labels(action_type_str)
        action_value_1_label.setText(label1 or "Action value")
        action_value_2_label.setText(label2 or "Action value 2")

class TableControl(AbstractFormWithTargetStructure, AbstractFormWithActionTable, AbstractFormWithTag):
    """Table Control user layer edit form logic."""

    MODEL = dm.TableControl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        # Populate widgets based on features attributes
        if self.creation is True:
            self.setup_target_structure_on_creation()
            self.fill_related_attributes()
        else:
            self.setup_target_structure_on_edit()
        self.populate_widgets()
        self.populate_foreign_widgets()
        self.populate_table_data()
        self.populate_tag_widgets()

        action_type_widget = self.dialog.findChild(QComboBox, "action_type")
        edit_signal = self.get_widget_editing_signal(action_type_widget)
        edit_slot = partial(self.update_table_header)
        connect_signal(edit_signal, edit_slot)
        self.dialog.active_form_signals.add((edit_signal, edit_slot))

    def update_table_header(self):
        """Update table headers."""
        action_type_widget = self.dialog.findChild(QComboBox, "action_type")
        action_type_str = action_type_widget.currentText()
        if action_type_str == "(NULL)":
            # Just set the default values
            super().update_table_header()
            return

        action_type_column_idx = 2
        if action_type_str != en.ActionType.SET_DISCHARGE_COEFFICIENTS.value.capitalize().replace("_", " "):
            # Clear the values in the to-be-hidden column, also fires save_table_edits
            for r in range(self.table.rowCount()):
                item = self.table.item(r, action_type_column_idx)
                if item:
                    item.setText("")
            # If action type is anything other than "set_discharge_coefficients", do not show the column for Action value 2
            self.table.setColumnHidden(action_type_column_idx, True)
        else:
            self.table.setColumnHidden(action_type_column_idx, False)

        # Update the table headers given the action type
        label1, label2 = map_action_type_to_labels(action_type_str)
        self.table.setHorizontalHeaderLabels(["Measured value", label1, label2])


class MeasureMap(AbstractFormWithTag):
    """Measure Map user layer edit form logic."""

    MODEL = dm.MeasureMap

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.measure_location_feature = None
        self.control_feature = None
        self.control_feature_type = None

    def fill_related_attributes(self):
        """Filling feature values based on related features attributes."""
        super().fill_related_attributes()
        if self.measure_location_feature is not None:
            self.feature["measure_location_id"] = self.measure_location_feature["id"]
        if self.control_feature is not None:
            self.feature["control_id"] = self.control_feature["id"]
            self.feature["control_type"] = self.control_feature_type

    @cached_property
    def control_types(self):
        """Return supported structure control data models."""
        control_data_models = {
            model_cls.__tablename__.split("_", 1)[0]: model_cls for model_cls in [dm.TableControl, dm.MemoryControl]
        }
        return control_data_models

    def setup_measure_location_on_edit(self):
        """Setting up measure map location and structure control during editing feature."""
        try:
            control_type = self.control_types[self.feature["control_type"]]
            control_model_cls = self.control_types[control_type]
            control_handler = self.layer_manager.model_handlers[control_model_cls]
            control_feat = control_handler.get_feat_by_id(self.feature["control_id"])
            self.control_feature = control_feat
            self.control_feature_type = control_type
        except KeyError:
            pass
        try:
            measure_location_handler = self.layer_manager.model_handlers[dm.MeasureLocation]
            measure_location_feat = measure_location_handler.get_feat_by_id(self.feature["measure_location_id"])
            self.measure_location_feature = measure_location_feat
        except KeyError:
            pass

    def setup_measure_control_on_creation(self):
        """Setting up measure map location and structure control during adding feature."""
        measure_location_handler = self.layer_manager.model_handlers[dm.MeasureLocation]
        measure_location_layer = measure_location_handler.layer
        feature_linestring = self.feature.geometry().asPolyline()
        feature_start_point, feature_end_point = feature_linestring[0], feature_linestring[-1]
        measure_location_feat = find_point_nodes(feature_start_point, measure_location_layer)
        if measure_location_feat is not None:
            self.measure_location_feature = measure_location_feat
        for control_type, control_model_cls in self.control_types.items():
            control_handler = self.layer_manager.model_handlers[control_model_cls]
            control_layer = control_handler.layer
            feature_end_point = self.feature.geometry().asPolyline()[-1]
            control_feat = find_point_nodes(feature_end_point, control_layer)
            if control_feat is not None:
                self.control_feature, self.control_feature_type = control_feat, control_type
                break

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.setup_measure_control_on_creation()
            # Set feature specific attributes
            self.fill_related_attributes()
        else:
            self.setup_measure_location_on_edit()
        # Populate widgets based on features attributes
        self.populate_foreign_widgets()
        self.populate_widgets()
        self.populate_tag_widgets()


class GridRefinementLineForm(AbstractFormWithTag):
    """Grid refinement line user layer edit form logic."""

    MODEL = dm.GridRefinementLine

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class GridRefinementAreaForm(AbstractFormWithTag):
    """Grid refinement area user layer edit form logic."""

    MODEL = dm.GridRefinementArea

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class ObstacleForm(AbstractFormWithTag):
    """Obstacle user layer edit form logic."""

    MODEL = dm.Obstacle

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class SurfaceParametersForm(AbstractFormWithTag):
    """Surface parameters user layer edit form logic."""

    MODEL = dm.SurfaceParameters

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


class Windshielding1DForm(AbstractFormWithTag):
    """1D Windshielding user layer edit form logic."""

    MODEL = dm.Windshielding1D

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
        point_geom = self.feature.geometry()
        point = point_geom.asPoint()
        channel_node_feat = find_point_polyline(point, channel_layer)
        if channel_node_feat:
            channel_id = channel_node_feat["id"]
            self.feature["channel_id"] = channel_id
            self.channel = channel_node_feat

    def populate_with_extra_widgets(self):
        """Populate basic and extra widgets for the given custom form."""
        if self.creation is True:
            self.fill_related_attributes()
        self.populate_widgets()
        self.populate_tag_widgets()


ALL_FORMS = (
    ConnectionNodeForm,
    PipeForm,
    WeirForm,
    CulvertForm,
    OrificeForm,
    PumpForm,
    PumpMapForm,
    DryWeatherFlowForm,
    DryWeatherFlowMapForm,
    DryWeatherFlowDistributionForm,
    SurfaceForm,
    SurfaceMapForm,
    ChannelForm,
    CrossSectionLocationForm,
    PotentialBreachForm,
    ExchangeLineForm,
    BoundaryCondition1D,
    Lateral1D,
    BoundaryCondition2D,
    Lateral2D,
    MeasureLocation,
    MemoryControl,
    TableControl,
    MeasureMap,
    GridRefinementLineForm,
    GridRefinementAreaForm,
    ObstacleForm,
    SurfaceParametersForm,
    Windshielding1DForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
