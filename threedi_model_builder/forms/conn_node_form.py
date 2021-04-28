from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm


class ConnectionNodeEditForm(BaseEditForm):
    """Connection node edit form logic."""

    MODEL = dm.ConnectionNode

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
