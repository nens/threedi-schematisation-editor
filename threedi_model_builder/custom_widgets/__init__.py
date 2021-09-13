# Copyright (C) 2021 by Lutra Consulting
import os
from qgis.PyQt import uic


basecls, uicls = uic.loadUiType(os.path.join(os.path.dirname(__file__), "ui", "projection_selection.ui"))


class ProjectionSelectionDialog(basecls, uicls):
    """Dialog with selection of the desired projection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
