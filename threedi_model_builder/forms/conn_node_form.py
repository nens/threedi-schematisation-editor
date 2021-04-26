from qgis.PyQt.QtCore import QObject, QDateTime
from qgis.PyQt.QtWidgets import QWidget, QMessageBox

from .base_edit_form import BaseEditForm
import threedi_model_builder.data_models as dm


class ConnectionNodeEditForm(BaseEditForm):
    """Connection node edit form logic."""
    MODEL = dm.ConnectionNode
    WIDGET_NAMES = [
            "sbox_bottom_level", "sbox_drain_level"
        ]

    def populate_widgets(self, connection_node):
        """Get data from all the layers needed and populate the form widgets."""

