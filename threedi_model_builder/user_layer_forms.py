from types import MappingProxyType
from .forms.manhole_form import ManholeEditForm


ALL_FORMS = (
    ManholeEditForm,
)

MODEL_FORMS = MappingProxyType({form.MODEL: form for form in ALL_FORMS})


class LayerEditFormFactory(object):
    """Factory for user layers edit forms."""
    def __init__(self, layer_manager):
        self.layer_manager = layer_manager

    def set_layer_form_logic(self, dialog, layer, feature):
        """Check the layer data model and set the dialog logic accordingly."""
        layer_data_model = self.layer_manager.get_layer_data_model(layer)
        for form_model, form in MODEL_FORMS.items():
            if layer_data_model == form_model:
                form = MODEL_FORMS[form_model](self.layer_manager, dialog, layer, feature)



