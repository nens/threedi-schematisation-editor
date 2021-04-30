from threedi_model_builder.forms.custom_forms import MODEL_FORMS
from threedi_model_builder.utils import disconnect_signal


class LayerEditFormFactory:
    """Factory for user layers edit forms."""

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager
        self.connected_signals = set()

    def disconnect_previous_form_signals(self):
        for signal, slot in self.connected_signals:
            disconnect_signal(signal, slot)
        self.connected_signals.clear()

    def set_layer_form_logic(self, dialog, layer, feature):
        """Check the layer handler and set the dialog logic accordingly."""
        layer_handler = self.layer_manager.layer_handlers[layer.id()]
        layer_form = MODEL_FORMS[layer_handler.MODEL]
        # Disconnect signals from previous form view
        self.disconnect_previous_form_signals()
        # New form initializing
        current_instance = layer_form(self.layer_manager, dialog, layer, feature)
        current_instance.setup_form_widgets()
        self.connected_signals |= current_instance.connected_signals
