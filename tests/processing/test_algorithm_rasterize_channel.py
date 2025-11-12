from pathlib import Path
from typing import Dict

import pytest
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingFeedback,
)
from qgis.core import QgsVectorLayer, QgsProcessingFeedback

from threedi_schematisation_editor.processing.algorithm_rasterize_channels import RasterizeChannelsAlgorithm
from tests.utils import DATA_DIR


gpkg_path = (DATA_DIR / 'rasterize_channels_test_inputs.gpkg').resolve()
channel_features = str(gpkg_path) + '|layername=channel'
cross_section_location_features = str(gpkg_path) + '|layername=cross_section_location'

rasterize_channel_inputs = {
    'INPUT_CHANNELS': channel_features,
    'INPUT_CROSS_SECTION_LOCATIONS': cross_section_location_features,
    'INPUT_DEM': None,
    'PIXEL_SIZE': 0.1,
    'OUTPUT': str(DATA_DIR / "rasterized_channels.tif"),
}

@pytest.mark.parametrize("alg_class, parameters", [
    (RasterizeChannelsAlgorithm, rasterize_channel_inputs),
])
def test_rasterize_channels_algorithm(alg_class: QgsProcessingAlgorithm, parameters: Dict):
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
