import shutil
import tempfile
from pathlib import Path

TEMP_DIR = Path(tempfile.gettempdir())

DATA_PATH = Path(__file__).parent.absolute().joinpath("data")
SCHEMATISATION_PATH = DATA_PATH.joinpath("schematisations")
CONFIG_PATH = DATA_PATH.joinpath("config")
SOURCE_PATH = DATA_PATH.joinpath("source")


def get_temp_copy(src):
    tgt = TEMP_DIR.joinpath(src.name)
    shutil.copy(src, tgt)
    return tgt.absolute()
