import shutil
import tempfile
from pathlib import Path

TEMP_DIR = Path(tempfile.gettempdir())

DATA_PATH = Path(__file__).parent.absolute().joinpath("data")
SCHEMATISATION_PATH = DATA_PATH.joinpath("schematisations")
CONFIG_PATH = DATA_PATH.joinpath("config")
SOURCE_PATH = DATA_PATH.joinpath("source")


def get_schematisation_copy(schematisation, test_name):
    tgt = TEMP_DIR.joinpath(test_name)
    src = SCHEMATISATION_PATH.joinpath(schematisation).with_suffix(".gpkg")
    shutil.copy(src, tgt)
    return tgt.absolute()
