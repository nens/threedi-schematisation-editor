import pytest
import os
import shutil
from threedi_model_builder.utils import get_qgis


@pytest.fixture
def data_conversion_setup():
    qgis_app = get_qgis()
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
