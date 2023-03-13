# Copyright (C) 2023 by Lutra Consulting
import os
import shutil
import sys

import pytest

from threedi_schematisation_editor.utils import get_qgis


@pytest.fixture
def data_conversion_setup():
    # assume the tests run on linux, provide non-default folders
    qgis_folder = ""
    proj_folder = ""
    if sys.platform == "linux":
        qgis_folder = "/QGIS"
        proj_folder = "/usr/share/proj"

    qgis_app = get_qgis(qgis_folder, proj_folder)
    current_dir = os.path.dirname(__file__)
    tmp_dir = os.path.join(current_dir, "tmp")
    src_sqlite = os.path.join(current_dir, "test_data", "v2_bergermeer_orifices.sqlite")
    reference_sqlite = os.path.join(tmp_dir, "v2_bergermeer_orifices_ref.sqlite")
    import_export_sqlite = os.path.join(tmp_dir, "v2_bergermeer_orifices_ie.sqlite")
    gpkg = os.path.join(tmp_dir, "v2_bergermeer_orifices_ie.gpkg")

    try:
        shutil.rmtree(tmp_dir)
    except OSError:
        pass  # directory not present at all

    os.makedirs(tmp_dir, exist_ok=True)
    shutil.copy(src_sqlite, reference_sqlite)
    shutil.copy(src_sqlite, import_export_sqlite)

    return qgis_app, src_sqlite, reference_sqlite, import_export_sqlite, gpkg
