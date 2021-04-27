from collections import defaultdict
from enum import Enum

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QSpinBox, QGroupBox

from qgis.core import NULL
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
    WIDGET_NAMES = None

    def __init__(self, layer_manager, dialog, layer, feature, parent=None):
        super(BaseEditForm, self).__init__(parent)
        self.layer_manager = layer_manager
        self.iface = layer_manager.iface
        self.uc = layer_manager.uc
        self.dialog = dialog
        self.layer = layer
        self.feature = feature
        self.model_widgets = defaultdict(list)  # {data_model_cls: list of tuples (widget, layer field name)}
        self.layer.editingStarted.connect(self.toggle_edit_mode)
        self.layer.editingStopped.connect(self.toggle_edit_mode)

    def setup_form_widgets(self):
        self.populate_widgets()
        self.populate_extra_widgets()
        self.toggle_edit_mode()

    def toggle_edit_mode(self):
        editing_active = self.layer.isEditable()
        print(editing_active)
        for widget in self.dialog.children():
            if isinstance(widget, QGroupBox):
                widget.setEnabled(editing_active)

    def populate_widgets(self, data_model_cls=None, feature=None):
        """Populate form's widgets - widgets are named after their attributes in the data model."""
        field_name_prefix = ""
        if data_model_cls is not None:
            field_name_prefix = data_model_cls.__tablename__ + "_"
        else:
            data_model_cls = self.MODEL
            feature = self.feature
        if feature.id() < 0:
            return  # form open for an invalid feature
        for field_name, field_type in data_model_cls.__annotations__.items():
            widget = self.dialog.findChild(QObject, field_name_prefix + field_name)
            if widget is None:
                # the filed might not be shown in the form
                continue
            if issubclass(field_type, Enum):
                cbo_items = {t.name: t.value for t in field_type}
                self.populate_combo(widget, cbo_items)
            self.set_widget_value(widget, feature[field_name])
            self.model_widgets[data_model_cls].append((widget, field_name))

    def populate_extra_widgets(self):
        raise NotImplementedError()

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
        elif isinstance(widget, (QgsSpinBox, QgsDoubleSpinBox, QDoubleSpinBox, QSpinBox)):
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
