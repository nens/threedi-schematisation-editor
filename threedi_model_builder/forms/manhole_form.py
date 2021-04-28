from types import MappingProxyType
from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm


class ManholeEditForm(BaseEditForm):
    """Manhole user layer edit form logic."""

    MODEL = dm.Manhole
    FOREIGN_MODEL_FIELDS = MappingProxyType(
        {
            "connection_node_initial_waterlevel": dm.ConnectionNode,
            "connection_node_storage_area": dm.ConnectionNode,
            "connection_node_code": dm.ConnectionNode,
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.feature.id() < 0:
            return  # form open for an invalid feature

        # Connection node
        connection_node_handler = self.layer_manager.loaded_models[dm.ConnectionNode]
        connection_node_feat = connection_node_handler.get_feat_by_id(self.feature["connection_node_id"])
        if connection_node_feat is not None:
            self.populate_widgets(data_model_cls=dm.ConnectionNode, feature=connection_node_feat)
