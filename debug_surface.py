"""Debug script to inspect the wide import result."""

import shutil
import sys
import warnings
from pathlib import Path

PLUGIN_ROOT = Path(
    "/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
    "/threedi_schematisation_editor"
)
DATA = PLUGIN_ROOT / "tests/vector_data_importer/data"
SOURCE = DATA / "source"
SCHEMATA = DATA / "schematisations"

sys.path.insert(0, str(PLUGIN_ROOT.parent))

from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication, QgsFeatureRequest

app = QgsApplication([], False)
app.initQgis()
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

import os
import tempfile

from threedi_schematisation_editor.utils import gpkg_layer
from threedi_schematisation_editor.vector_data_importer.importers import SurfaceImporter
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ImportSettings,
    SewerTypeMapping,
    SourceSettings,
    SurfaceLinkingSettings,
)


def make_temp_copy(src):
    suffix = Path(src).suffix
    fd, tgt = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    shutil.copy(src, tgt)
    return tgt


# Check source layer feature count
wide_src_path = make_temp_copy(SOURCE / "surfaces_wide.gpkg")
wide_src = gpkg_layer(wide_src_path, "surfaces")
print(f"Source feature count: {wide_src.featureCount()}")
for feat in wide_src.getFeatures():
    maaiveld = feat["maaiveld"]
    open_water = feat["open_water"]
    total = (maaiveld or 0) + (open_water or 0)
    print(
        f"  id={feat['id']} desc={feat['description']!r} maaiveld={maaiveld} open_water={open_water} sum={total}"
    )

print()

# Check what SourceSettings.include_expression does
import_config = ImportSettings(
    surface_linking=SurfaceLinkingSettings(
        data_format="wide",
        sewerage_type_mappings=[
            SewerTypeMapping(sewerage_type=0, percentage_column="pct_combined"),
            SewerTypeMapping(sewerage_type=1, percentage_column="pct_storm"),
        ],
        search_distance=40.0,
        spatial_match_enabled=True,
    ),
    fields={
        "id": {"method": "auto"},
        "area": {"method": "auto"},
        "surface_parameters_id": {
            "method": "source_attribute",
            "source_attribute": "surface_parameters_id",
        },
        "code": {"method": "ignore"},
        "display_name": {"method": "ignore"},
        "tags": {"method": "ignore"},
    },
)
print(f"source setting: {import_config.source}")
print(f"include_expression: {import_config.source.include_expression!r}")
