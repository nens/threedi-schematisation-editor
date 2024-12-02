# Copyright (C) 2023 by Lutra Consulting
import os
import sys

REQUIRED_3DI_MI_UTILS_VERSION = "0.1.5"
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
MI_UTILS_WHEEL = os.path.join(MAIN_DIR, f"threedi_mi_utils-{REQUIRED_3DI_MI_UTILS_VERSION}-py3-none-any.whl")

def patch_wheel_imports():
    """
    Function that tests if extra modules are installed.
    If modules are not available then it will add missing modules wheels to the Python path.
    """
    try:
        import threedi_mi_utils
    except ImportError:
        deps_path = MI_UTILS_WHEEL
        sys.path.append(deps_path)
