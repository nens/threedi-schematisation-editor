# Copyright (C) 2025 by Lutra Consulting
import importlib
import os
import sys

import pkg_resources

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
THREEDI_SCHEMA_MODULE_NAME = "threedi_schema"
THREEDI_MI_UTILS_MODULE_NAME = "threedi_mi_utils"
GEOALCHEMY_MODULE_NAME = "geoalchemy2"
SQLALCHEMY_MODULE_NAME = "sqlalchemy"
ALEMBIC_MODULE_NAME = "alembic"
MAKO_MODULE_NAME = "mako"

REQUIRED_3DI_SCHEMA_VERSION = "0.300.8"
REQUIRED_3DI_MI_UTILS_VERSION = "0.1.6.dev0"
REQUIRED_GEOALCHEMY2_VERSION = "0.15.2"
REQUIRED_SQLALCHEMY_VERSION = "2.0.6"
REQUIRED_ALEMBIC_VERSION = "1.14.1"
REQUIRED_MAKO_VERSION = "1.3.9"

THREEDI_SCHEMA_WHEEL = os.path.join(
    MAIN_DIR, f"{THREEDI_SCHEMA_MODULE_NAME}-{REQUIRED_3DI_SCHEMA_VERSION}-py3-none-any.whl"
)
MI_UTILS_WHEEL = os.path.join(
    MAIN_DIR, f"{THREEDI_MI_UTILS_MODULE_NAME}-{REQUIRED_3DI_MI_UTILS_VERSION}-py3-none-any.whl"
)
GEOALCHEMY2_WHEEL = os.path.join(MAIN_DIR, f"GeoAlchemy2-{REQUIRED_GEOALCHEMY2_VERSION}-py3-none-any.whl")
SQLALCHEMY_WHEEL = os.path.join(MAIN_DIR, f"SQLAlchemy-{REQUIRED_SQLALCHEMY_VERSION}-py3-none-any.whl")
ALEMBIC_WHEEL = os.path.join(MAIN_DIR, f"alembic-{REQUIRED_ALEMBIC_VERSION}-py3-none-any.whl")
MAKO_WHEEL = os.path.join(MAIN_DIR, f"Mako-{REQUIRED_MAKO_VERSION}-py3-none-any.whl")


def patch_wheel_imports():
    """
    Function that tests if extra modules are installed.
    If modules are not available then it will add missing modules wheels to the Python path.
    """
    requirements = [
        (SQLALCHEMY_MODULE_NAME, REQUIRED_SQLALCHEMY_VERSION, SQLALCHEMY_WHEEL),
        (GEOALCHEMY_MODULE_NAME, REQUIRED_GEOALCHEMY2_VERSION, GEOALCHEMY2_WHEEL),
        (MAKO_MODULE_NAME, REQUIRED_MAKO_VERSION, MAKO_WHEEL),
        (ALEMBIC_MODULE_NAME, REQUIRED_ALEMBIC_VERSION, ALEMBIC_WHEEL),
        (THREEDI_MI_UTILS_MODULE_NAME, REQUIRED_3DI_MI_UTILS_VERSION, MI_UTILS_WHEEL),
        (THREEDI_SCHEMA_MODULE_NAME, REQUIRED_3DI_SCHEMA_VERSION, THREEDI_SCHEMA_WHEEL),
    ]
    for required_module, required_module_version, module_wheel in requirements:
        requirement = f"{required_module}=={required_module_version}"
        try:
            pkg_resources.require(requirement)
        except Exception:
            if required_module in sys.modules:
                del sys.modules[required_module]
            sys.path.insert(0, module_wheel)

            _refresh_python_import_mechanism()
            importlib.import_module(required_module)


def _refresh_python_import_mechanism():
    """
    Refresh the import mechanism.
    This is required when deps are dynamically installed/removed. The modules
    'importlib' and 'pkg_resources' need to update their internal data structures.
    """
    # This function should be called if any modules are created/installed while your
    # program is running to guarantee all finders will notice the new module’s existence.
    importlib.invalidate_caches()

    # https://stackoverflow.com/questions/58612272/pkg-resources-get-distributionmymodule-version-not-updated-after-reload
    # Apparently pkg_resources needs to be reloaded to be up-to-date with newly installed packages
    importlib.reload(pkg_resources)
