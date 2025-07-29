import os
import gc
import pytest

from qgis.core import QgsApplication, QgsProcessingFeedback


@pytest.fixture(scope="session")
def qgis_application() -> QgsApplication:
    """QGIS app without processing providers"""
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    print("Initializing minimal QGIS...")
    qgs = QgsApplication([], False)
    qgs.initQgis()
    yield qgs
    print("Exiting QGIS (minimal)...")
    gc.collect()
    qgs.exitQgis()
    gc.collect()
    print("Minimal QGIS cleanup complete.")


