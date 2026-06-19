import inspect
import json
import warnings
from pathlib import Path

from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QSettings

from threedi_schematisation_editor import warnings as threedi_warnings

VDI_DRAFTS_FOLDER = "vdi_preset_drafts"


class CatchThreediWarnings:
    """
    A context manager that catches warnings from threedi_schematisation_editor.warnings,
    compiles them into a warnings_msg, and logs them to QGIS log system.
    """

    def __init__(self, log_category="Warnings"):
        self.caught_warnings = []
        self.warnings_msg = ""
        self.log_category = log_category

    def __enter__(self):
        # Create a warnings list to store caught warnings
        self._warnings_list = []

        # Save the old showwarning function to restore it later
        self._old_showwarning = warnings.showwarning

        # Define a custom function to intercept warnings
        def _showwarning(message, category, filename, lineno, file=None, line=None):
            self._warnings_list.append((message, category, filename, lineno))

        # Replace the default showwarning with our custom one
        warnings.showwarning = _showwarning

        # Set up the warnings filter
        warnings.simplefilter("ignore")  # Ignore all warnings by default

        # Enable warnings for all warning classes in the threedi module
        for name, obj in inspect.getmembers(threedi_warnings):
            if inspect.isclass(obj) and issubclass(obj, Warning):
                warnings.simplefilter("always", obj)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original showwarning function
        warnings.showwarning = self._old_showwarning

        # Process the warnings
        self.caught_warnings = self._warnings_list

        # Generate the warning message if any warnings were caught
        if self.caught_warnings:
            self.warnings_msg = "Note: Some warnings were raised during the process:"

            # Log each warning to QGIS
            for warning_info in self.caught_warnings:
                message, category, filename, lineno = warning_info
                self.warnings_msg += f"\n⚠ {category.__name__}: {message}"

        # Reset the warnings filter
        warnings.resetwarnings()

        # Don't suppress any exceptions
        return False


def create_font(dialog, point_size: int, bold: bool = False):
    font = dialog.font()
    font.setPointSize(point_size)
    if bold:
        font.setBold(True)
        font.setWeight(75)
    return font


LAST_CONFIG_DIR_ENTRY = "threedi/last_vdi_config_dir"


def get_last_config_dir() -> str:
    settings = QSettings()
    return settings.value(LAST_CONFIG_DIR_ENTRY, str(Path.home()))


def update_last_config_dir(config_dir: str):
    settings = QSettings()
    if Path(config_dir).is_dir():
        settings.setValue(LAST_CONFIG_DIR_ENTRY, config_dir)
    elif Path(config_dir).is_file():
        settings.setValue(LAST_CONFIG_DIR_ENTRY, str(Path(config_dir).parent))


def _draft_path(wizard_class_name):
    folder = Path(QgsApplication.qgisSettingsDirPath()) / VDI_DRAFTS_FOLDER
    return folder / f"{wizard_class_name}.json"


def get_draft(wizard_class_name):
    path = _draft_path(wizard_class_name)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def save_draft(wizard_class_name, data):
    path = _draft_path(wizard_class_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def delete_draft(wizard_class_name):
    path = _draft_path(wizard_class_name)
    try:
        path.unlink()
    except FileNotFoundError:
        pass
