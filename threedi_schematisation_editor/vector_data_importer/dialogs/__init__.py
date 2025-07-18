# Copyright (C) 2025 by Lutra Consulting
from pathlib import Path

from qgis.PyQt import uic

ui_path = Path(__file__).parent.joinpath("ui")

# UI classes for ImportFeaturesDialog and ImportStructuresDialog are now defined in code
# and no longer use loadUiType

vm_basecls, vm_uicls = uic.loadUiType(ui_path.joinpath("attribute_value_map.ui"))
load_basecls, load_uicls = uic.loadUiType(ui_path.joinpath("load_schematisation.ui"))
