from pathlib import Path

from qgis.PyQt import uic

ui_path = Path(__file__).parent.joinpath("ui")

load_basecls, load_uicls = uic.loadUiType(ui_path.joinpath("load_schematisation.ui"))
