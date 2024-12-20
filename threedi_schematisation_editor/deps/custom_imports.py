# Copyright (C) 2025 by Lutra Consulting
import importlib
import os
import sys

import pkg_resources

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIRED_3DI_SCHEMA_VERSION = "0.230.0.dev0"
REQUIRED_3DI_MI_UTILS_VERSION = "0.1.5"
THREEDI_SCHEMA_WHEEL = os.path.join(MAIN_DIR, f"threedi_schema-{REQUIRED_3DI_SCHEMA_VERSION}-py3-none-any.whl")
MI_UTILS_WHEEL = os.path.join(MAIN_DIR, f"threedi_mi_utils-{REQUIRED_3DI_MI_UTILS_VERSION}-py3-none-any.whl")


def patch_wheel_imports():
    """
    Function that tests if extra modules are installed.
    If modules are not available then it will add missing modules wheels to the Python path.
    """
    requirement = "threedi_mi_utils" + "==" + REQUIRED_3DI_MI_UTILS_VERSION
    try:
        pkg_resources.require(requirement)
    except Exception:
        if "threedi_mi_utils" in sys.modules:
            del sys.modules["threedi_mi_utils"]
        sys.path.insert(0, MI_UTILS_WHEEL)

        _refresh_python_import_mechanism()
        importlib.import_module("threedi_mi_utils")

def _refresh_python_import_mechanism():
    """Refresh the import mechanism.

    This is required when deps are dynamically installed/removed. The modules
    'importlib' and 'pkg_resources' need to update their internal data structures.
    """
    # This function should be called if any modules are created/installed while your
    # program is running to guarantee all finders will notice the new module’s existence.
    importlib.invalidate_caches()

    # https://stackoverflow.com/questions/58612272/pkg-resources-get-distributionmymodule-version-not-updated-after-reload
    # Apparantely pkg_resources needs to be reloaded to be up-to-date with newly installed packages
    importlib.reload(pkg_resources)
