import processing
import pytest
from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication, QgsProcessingFeedback

from threedi_schematisation_editor.processing import (
    ThreediSchematisationEditorProcessingProvider,
)

from .utils import *

TEMP_DIR = Path(tempfile.gettempdir())


@pytest.fixture(scope="session")
def qgis_application_with_processor(qgis_application: QgsApplication) -> QgsApplication:
    """Full QGIS app with processing providers"""
    print("Initializing Processing framework...")
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    try:
        provider = ThreediSchematisationEditorProcessingProvider()
        QgsApplication.processingRegistry().addProvider(provider)
    except ImportError:
        print("Warning: ThreediSchematisationEditorProcessingProvider not available")
    yield qgis_application


def run_processing_operation(algo_name, task):
    task = {key: str(val) for key, val in task.items()}
    try:
        processing.run(
            f"threedi_schematisation_editor:{algo_name}",
            task,
            feedback=QgsProcessingFeedback(),
        )
    except:
        pytest.fail(f"Failed to run {algo_name} with task {task}")


def test_threedi_import_connection_nodes(qgis_application_with_processor):
    task = {
        "SOURCE_LAYER": SOURCE_PATH.joinpath("connection_nodes.gpkg"),
        "IMPORT_CONFIG": CONFIG_PATH.joinpath("import_connection_nodes.json"),
        "TARGET_GPKG": get_schematisation_copy(
            "schematisation_channel.gpkg", "test_connection_node_processing.gpkg"
        ),
    }
    try:
        run_processing_operation("threedi_import_connection_nodes", task)
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {e}")


def test_threedi_import_structure(qgis_application_with_processor):
    task = {
        "SOURCE_LAYER": SOURCE_PATH.joinpath("weirs.gpkg"),
        "IMPORT_CONFIG": CONFIG_PATH.joinpath("import_weirs_nosnap.json"),
        "TARGET_GPKG": get_schematisation_copy(
            "schematisation_channel.gpkg", "test_weir_processing.gpkg"
        ),
    }
    try:
        run_processing_operation("threedi_import_weirs", task)
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {e}")
