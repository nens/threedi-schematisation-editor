from pathlib import Path

DATA_PATH = Path(__file__).parent.absolute().joinpath("data")
SCHEMATISATION_PATH = DATA_PATH.joinpath("schematisations")
CONFIG_PATH = DATA_PATH.joinpath("config")
SOURCE_PATH = DATA_PATH.joinpath("source")
