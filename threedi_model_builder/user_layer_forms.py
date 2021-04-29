from threedi_model_builder.forms.custom_forms import MODEL_FORMS


class LayerEditFormFactory:
    """Factory for user layers edit forms."""

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager

    def set_layer_form_logic(self, dialog, layer, feature):
        """Check the layer handler and set the dialog logic accordingly."""
        layer_handler = self.layer_manager.layer_handlers[layer.id()]
        layer_form = MODEL_FORMS[layer_handler.MODEL]
        # Form initializing
        current_instance = layer_form(self.layer_manager, dialog, layer, feature)
        current_instance.setup_form_widgets()
