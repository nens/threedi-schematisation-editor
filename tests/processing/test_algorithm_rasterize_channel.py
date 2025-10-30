import tempfile
from pathlib import Path
from typing import Dict

import pytest

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingFeatureSourceDefinition
)
from threedi_schematisation_editor.processing.algorithm_rasterize_channels import (
    RasterizeChannelsAlgorithm,
)
from threedi_schematisation_editor.utils import gpkg_layer

DATA_DIR = Path(__file__).parent / 'data'
TMP_DIR = tempfile.TemporaryDirectory()

gpkg_path = DATA_DIR / 'rasterize_channels_test_inputs.gpkg'
channel_layer = gpkg_layer(gpkg_path, "channel")
cross_section_location_layer = gpkg_layer(gpkg_path, "cross_section_location")

rasterize_channel_inputs = {
    'INPUT_CHANNELS': channel_layer,
    'INPUT_CROSS_SECTION_LOCATIONS': cross_section_location_layer,
    'INPUT_DEM': None,
    'PIXEL_SIZE': 0.1,
    'OUTPUT': str(Path(TMP_DIR.name) / "rasterized_channels.tif"),
}


@pytest.mark.parametrize("alg_class, parameters", [
    (RasterizeChannelsAlgorithm, rasterize_channel_inputs),
])
def test_water_depth_algorithm(alg_class: QgsProcessingAlgorithm, parameters: Dict):
    alg = alg_class()

    # Create the QGIS processing context & feedback
    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()
    output_file = Path(parameters["OUTPUT"])

    try:
        result = alg.run(parameters, context, feedback)
        assert result is not None
        assert output_file.exists()
    finally:
        if output_file.exists():
            output_file.unlink()
