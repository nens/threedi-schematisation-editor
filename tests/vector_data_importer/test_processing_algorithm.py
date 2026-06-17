import copy
import json

import processing
import pytest
from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication, QgsProcessingException, QgsProcessingFeedback

from tests.utils import get_temp_copy
from threedi_schematisation_editor.processing import (
    ThreediSchematisationEditorProcessingProvider,
)

from .utils import *


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
    task = {key: str(get_temp_copy(val)) for key, val in task.items()}
    processing.run(
        f"threedi_schematisation_editor:{algo_name}",
        task,
        feedback=QgsProcessingFeedback(),
    )


def test_threedi_import_connection_nodes(qgis_application_with_processor):
    task = {
        "SOURCE_LAYER": SOURCE_PATH.joinpath("connection_nodes.gpkg"),
        "IMPORT_CONFIG": CONFIG_PATH.joinpath("import_connection_nodes.json"),
        "TARGET_GPKG": SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg"),
    }
    try:
        run_processing_operation("threedi_import_connection_nodes", task)
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {e}")


def test_threedi_import_structure(qgis_application_with_processor):
    task = {
        "SOURCE_LAYER": SOURCE_PATH.joinpath("weirs.gpkg"),
        "IMPORT_CONFIG": CONFIG_PATH.joinpath("import_weirs_nosnap.json"),
        "TARGET_GPKG": SCHEMATISATION_PATH.joinpath("schematisation_channel.gpkg"),
    }
    try:
        run_processing_operation("threedi_import_weirs", task)
    except Exception as e:
        pytest.fail(f"Test failed due to an unexpected exception: {e}")


@pytest.mark.parametrize(
    "config_patch,expected_match",
    [
        # Disallowed method for a 'fields' entry (id only allows AUTO)
        (
            {
                "fields": {
                    "id": {"method": "source_attribute", "source_attribute": "id"}
                }
            },
            "Invalid field map \\(fields\\)",
        ),
        # Disallowed method for a 'connection_node_fields' entry (id only allows AUTO)
        (
            {
                "connection_node_fields": {
                    "id": {"method": "source_attribute", "source_attribute": "id"}
                }
            },
            "Invalid field map \\(connection_node_fields\\)",
        ),
        # Invalid ImportSettings schema: snap_distance must be a float
        (
            {"connection_nodes": {"snap_distance": "not_a_number"}},
            "Invalid import settings",
        ),
    ],
)
def test_threedi_import_rejects_invalid_config(
    qgis_application_with_processor, tmp_path, config_patch, expected_match
):
    """Processing algorithm raises QgsProcessingException for invalid import configs."""
    with open(CONFIG_PATH / "import_weirs_nosnap.json") as f:
        config = copy.deepcopy(json.load(f))

    for key, value in config_patch.items():
        if isinstance(value, dict) and isinstance(config.get(key), dict):
            config[key].update(value)
        else:
            config[key] = value

    config_file = tmp_path / "invalid_config.json"
    config_file.write_text(json.dumps(config))

    with pytest.raises(QgsProcessingException, match=expected_match):
        processing.run(
            "threedi_schematisation_editor:threedi_import_weirs",
            {
                "SOURCE_LAYER": str(get_temp_copy(SOURCE_PATH / "weirs.gpkg")),
                "IMPORT_CONFIG": str(config_file),
                "TARGET_GPKG": str(
                    get_temp_copy(SCHEMATISATION_PATH / "schematisation_channel.gpkg")
                ),
            },
            feedback=QgsProcessingFeedback(),
        )


def test_threedi_import_rejects_invalid_json(qgis_application_with_processor, tmp_path):
    """Processing algorithm raises QgsProcessingException for malformed JSON."""
    config_file = tmp_path / "bad.json"
    config_file.write_text("this is not json{{{")

    with pytest.raises(QgsProcessingException, match="Could not read import config"):
        processing.run(
            "threedi_schematisation_editor:threedi_import_weirs",
            {
                "SOURCE_LAYER": str(get_temp_copy(SOURCE_PATH / "weirs.gpkg")),
                "IMPORT_CONFIG": str(config_file),
                "TARGET_GPKG": str(
                    get_temp_copy(SCHEMATISATION_PATH / "schematisation_channel.gpkg")
                ),
            },
            feedback=QgsProcessingFeedback(),
        )
