# Copyright (C) 2025 by Lutra Consulting
from threedi_schematisation_editor.forms.custom_forms import MODEL_FORMS
from threedi_schematisation_editor.utils import disconnect_signal


class LayerEditFormFactory:
    """Factory for user layers edit forms."""

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager

    def set_layer_form_logic(self, dialog, layer, feature):
        """Check the layer handler and set the dialog logic accordingly."""
        layer_handler = self.layer_manager.layer_handlers[layer.id()]
        layer_form = MODEL_FORMS[layer_handler.MODEL]
        # Disconnect signals from previous form view
        if hasattr(dialog, "active_form_signals"):
            for signal, slot in dialog.active_form_signals:
                disconnect_signal(signal, slot)
            dialog.active_form_signals.clear()
        else:
            setattr(dialog, "active_form_signals", set())
        # New form initializing
        current_instance = layer_form(self.layer_manager, dialog, layer, feature)
        current_instance.setup_form_widgets()
