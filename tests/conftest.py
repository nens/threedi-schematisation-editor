import pytest

from qgis.core import QgsApplication
from qgis.analysis import QgsNativeAlgorithms
from qgis._3d import Qgs3DAlgorithms

from processing.algs.gdal.GdalAlgorithmProvider import GdalAlgorithmProvider 
from processing.core.Processing import Processing

_singletons = {}


def ensure_qgis_app_is_initialized():
    """Make sure qgis is initialized for testing."""
    # Note: if you just need the QT app to be there, you can use the qtbot fixture
    # from https://pytest-qt.readthedocs.io/en/latest/index.html
    if "app" not in _singletons:
        app = QgsApplication([], False)
        app.initQgis()
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        QgsApplication.processingRegistry().addProvider(Qgs3DAlgorithms())
        QgsApplication.processingRegistry().addProvider(GdalAlgorithmProvider())
        _singletons["app"] = app


@pytest.fixture(autouse=True)
def qgis_app_initialized():
    ensure_qgis_app_is_initialized()
