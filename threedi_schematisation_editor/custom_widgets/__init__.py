# Copyright (C) 2025 by Lutra Consulting
from pathlib import Path

from qgis.PyQt import uic

ui_path = Path(__file__).parent.joinpath("ui")

if_basecls, if_uicls = uic.loadUiType(ui_path.joinpath("import_features.ui"))
is_basecls, is_uicls = uic.loadUiType(ui_path.joinpath("import_structures.ui"))
vm_basecls, vm_uicls = uic.loadUiType(ui_path.joinpath("attribute_value_map.ui"))
load_basecls, load_uicls = uic.loadUiType(ui_path.joinpath("load_schematisation.ui"))


