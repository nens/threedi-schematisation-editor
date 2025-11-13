import gc
import os

import pytest
from processing.algs.gdal.GdalAlgorithmProvider import GdalAlgorithmProvider
from processing.core.Processing import Processing
from qgis._3d import Qgs3DAlgorithms
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication, QgsProcessingFeedback

_singletons = {}


def ensure_qgis_app_is_initialized():
    """Make sure qgis is initialized for testing."""
    # Note: if you just need the QT app to be there, you can use the qtbot fixture
    # from https://pytest-qt.readthedocs.io/en/latest/index.html
    if "app" not in _singletons:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
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


@pytest.fixture(scope="session")
def qgis_application() -> QgsApplication:
    ensure_qgis_app_is_initialized()
    return _singletons["app"]
