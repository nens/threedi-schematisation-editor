from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QSpinBox, QWidget

from qgis.core import NULL
from qgis.gui import QgsDoubleSpinBox, QgsSpinBox


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
        self.widgets = None  # Form's widgets map {widget_name: widget}

        self.get_form_widgets()
        self.populate_widgets()

        self.btn_save.clicked.connect(self.save_changes)

    def get_form_widgets(self):
        """Make some references to form's widgets."""
        self.widgets = dict()
        for widget_name in self.WIDGET_NAMES:
            widget = self.dialog.findChild(QWidget, widget_name)
            if widget is None:
                self.uc.log_warn(f"Can't find widget {widget_name} for layer {self.layer.name()}")
                continue
            setattr(self, widget_name, widget)
            self.widgets[widget_name] = widget

    @staticmethod
    def populate_combo(combo_widget, value_map):
        """Populates combo box with value map's items (map key = displayed text, map value = data)."""
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

    def save_changes(self):
        """Get modified attributes values and save them."""
        raise Exception("Not implemented")
