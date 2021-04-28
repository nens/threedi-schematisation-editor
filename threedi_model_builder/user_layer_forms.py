from types import MappingProxyType
from .forms.manhole_form import ManholeEditForm
from .forms.pipe_form import PipeEditForm


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


ALL_FORMS = (
    ManholeEditForm,
    PipeEditForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})
