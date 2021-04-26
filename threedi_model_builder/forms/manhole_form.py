from qgis.PyQt.QtCore import NULL
from qgis.PyQt.QtWidgets import QMessageBox

from qgis.core import QgsAbstractFeatureIterator

from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm
from ..enumerators import CalculationTypeNode


class ManholeEditForm(BaseEditForm):
    """Manhole user layer edit form logic."""
    MODEL = dm.Manhole
    WIDGET_NAMES = [
        "cbo_calculation_type", "edit_shape", "edit_code", "edit_display_name", "sbox_id",
        "sbox_bottom_level", "sbox_drain_level", "sbox_width", "sbox_length", "sbox_surface_level",
        "sbox_conn_node_id", "edit_conn_node_code", "sbox_conn_node_init_waterlevel", "sbox_conn_node_storage_area",
        "btn_save"
    ]

    def populate_widgets(self):
        """Get data from all the layers needed and populate the form widgets."""
        if self.feature.id() < 0:
            # form open for an invalid feature
            return

        # General
        self.set_widget_value(self.sbox_id, self.feature["id"])
        self.set_widget_value(self.edit_code, self.feature["code"])
        self.set_widget_value(self.edit_display_name, self.feature["display_name"])
        calc_types = {i.name: i.value for i in CalculationTypeNode}
        self.populate_combo(self.cbo_calculation_type, calc_types)
        self.set_widget_value(self.cbo_calculation_type, self.feature["calculation_type"])

        # Characteristics
        self.set_widget_value(self.edit_shape, self.feature["shape"])
        self.set_widget_value(self.sbox_width, self.feature["width"])
        self.set_widget_value(self.sbox_length, self.feature["length"])
        self.set_widget_value(self.sbox_bottom_level, self.feature["bottom_level"])
        self.set_widget_value(self.sbox_surface_level, self.feature["surface_level"])
        self.set_widget_value(self.sbox_drain_level, self.feature["drain_level"])

        # Connection node
        conn_node_id = self.feature["connection_node_id"]
        if conn_node_id not in (None, NULL):
            conn_node_feats = self.layer_manager.get_layer_features(dm.ConnectionNode, f'"id" = {conn_node_id}')
            if conn_node_feats.isValid():
                conn_node_feat = next(conn_node_feats)
                if conn_node_feat.isValid():
                    self.set_widget_value(self.sbox_conn_node_id, conn_node_feat["id"])
                    self.set_widget_value(self.edit_conn_node_code, conn_node_feat["code"])
                    self.set_widget_value(self.sbox_conn_node_init_waterlevel, conn_node_feat["initial_waterlevel"])
                    self.set_widget_value(self.sbox_conn_node_storage_area, conn_node_feat["storage_area"])

        self.dialog.setEnabled(self.layer.isEditable())

    def save_changes(self):
        self.uc.show_info("Not implemented")

