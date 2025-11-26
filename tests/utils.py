import shutil
import tempfile
from pathlib import Path

TEMP_DIR = Path(tempfile.gettempdir())
DATA_DIR = Path(__file__).parent / "data"


def get_temp_copy(src):
    tgt = TEMP_DIR.joinpath(src.name)
    shutil.copy(src, tgt)
    return tgt.absolute()
