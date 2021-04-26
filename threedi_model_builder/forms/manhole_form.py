from qgis.PyQt.QtCore import NULL

from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm


class ManholeEditForm(BaseEditForm):
    """Manhole user layer edit form logic."""
    MODEL = dm.Manhole

    def populate_extra_widgets(self):
        """Populate widgets for other layers attributes."""
        if self.feature.id() < 0:
            return  # form open for an invalid feature
        conn_node_id = self.feature["connection_node_id"]
        if conn_node_id not in (None, NULL):
            conn_node_feats = self.layer_manager.get_layer_features(dm.ConnectionNode, f'"id" = {conn_node_id}')
            if conn_node_feats.isValid():
                conn_node_feat = next(conn_node_feats)
                if conn_node_feat.isValid():
                    self.populate_widgets(dm.ConnectionNode, conn_node_feat)
