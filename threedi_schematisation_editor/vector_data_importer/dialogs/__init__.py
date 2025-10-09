# Copyright (C) 2025 by Lutra Consulting
from pathlib import Path

from qgis.PyQt import uic

ui_path = Path(__file__).parent.joinpath("ui")

vm_basecls, vm_uicls = uic.loadUiType(ui_path.joinpath("attribute_value_map.ui"))
