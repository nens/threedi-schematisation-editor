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


DATA_DIR = Path(__file__).parent.parent

rasterize_channel_inputs = {
    'INPUT_CHANNELS': QgsProcessingFeatureSourceDefinition(
        str(DATA_DIR / 'rasterize_channels_test_inputs.gpkg') + '|layername=channel'
    ),
    'INPUT_CROSS_SECTION_LOCATIONS': QgsProcessingFeatureSourceDefinition(
        str(DATA_DIR / 'rasterize_channels_test_inputs.gpkg') + '|layername=cross_section_location'
    ),
    'INPUT_DEM': None,
    'PIXEL_SIZE': 0.1,
    'OUTPUT': 'TEMPORARY_OUTPUT',
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
