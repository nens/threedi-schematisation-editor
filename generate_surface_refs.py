"""Script to generate reference GPKGs for surface importer integration tests.

Run inside the Docker container:
  QT_QPA_PLATFORM=offscreen python3 generate_surface_refs.py
"""

import os
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

PLUGIN_ROOT = Path(
    "/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
    "/threedi_schematisation_editor"
)
DATA = PLUGIN_ROOT / "tests/vector_data_importer/data"
SOURCE = DATA / "source"
SCHEMATA = DATA / "schematisations"
REF = DATA / "ref"

sys.path.insert(0, str(PLUGIN_ROOT.parent))

from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsApplication

app = QgsApplication([], False)
app.initQgis()
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

from threedi_schematisation_editor.utils import gpkg_layer
from threedi_schematisation_editor.vector_data_importer.importers import SurfaceImporter
from threedi_schematisation_editor.vector_data_importer.settings_models import (
    ImportSettings,
    SewerTypeMapping,
    SurfaceLinkingSettings,
)


def make_temp_copy(src):
    suffix = Path(src).suffix
    fd, tgt = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    shutil.copy(src, tgt)
    return tgt


# ---- WIDE FORMAT REF -------------------------------------------------------
print("Generating test_import_surface_wide.gpkg ...")

wide_config = ImportSettings(
    surface_linking=SurfaceLinkingSettings(
        data_format="wide",
        sewerage_type_mappings=[
            SewerTypeMapping(sewerage_type=0, percentage_column="pct_combined"),
        ],
        search_distance=200.0,
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

wide_schematisation = make_temp_copy(SCHEMATA / "schematisation_surface_pipe.gpkg")
wide_src = gpkg_layer(str(make_temp_copy(SOURCE / "surfaces_wide.gpkg")), "surfaces")
wide_surface = gpkg_layer(wide_schematisation, "surface")
wide_surface_map = gpkg_layer(wide_schematisation, "surface_map")

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    importer = SurfaceImporter(
        wide_src,
        wide_schematisation,
        wide_config,
        surface_layer=wide_surface,
        surface_map_layer=wide_surface_map,
    )
    importer.import_features()

importer.commit_pending_changes()

for w in caught:
    print(f"  warning: {w.category.__name__}: {w.message}")

surface_count = wide_surface.featureCount()
surface_map_count = wide_surface_map.featureCount()
print(f"  surface rows: {surface_count} (expected 10)")
print(f"  surface_map rows: {surface_map_count} (expected 7)")

print("  surface_map details:")
for feat in sorted(wide_surface_map.getFeatures(), key=lambda f: f["id"]):
    print(
        f"    id={feat['id']} surface_id={feat['surface_id']} "
        f"connection_node_id={feat['connection_node_id']} "
        f"percentage={feat['percentage']}"
    )

assert surface_count == 7, f"Expected 7 surface rows, got {surface_count}"
assert surface_map_count == 7, f"Expected 7 surface_map rows, got {surface_map_count}"

shutil.copy(wide_schematisation, REF / "test_import_surface_wide.gpkg")
print("  -> saved to ref/test_import_surface_wide.gpkg")


# ---- LONG FORMAT ATTR MATCH REF --------------------------------------------
print()
print("Generating test_import_surface_long_attr_match.gpkg ...")

long_config = ImportSettings(
    surface_linking=SurfaceLinkingSettings(
        data_format="long",
        sewerage_type_config={
            "method": "source_attribute",
            "source_attribute": "sewage_type",
        },
        search_distance=100.0,
        attribute_match_enabled=True,
        attribute_match_table="pipe",
        attribute_match_target_config={
            "method": "source_attribute",
            "source_attribute": "code",
        },
        attribute_match_input_config={
            "method": "source_attribute",
            "source_attribute": "pipe_code",
        },
        spatial_match_enabled=True,
    ),
    fields={
        "id": {"method": "auto"},
        "area": {"method": "auto"},
        "display_name": {
            "method": "source_attribute",
            "source_attribute": "expected_outcome",
        },
    },
    surface_map_fields={
        "id": {"method": "auto"},
        "percentage": {
            "method": "source_attribute",
            "source_attribute": "runoff_pct",
        },
        "display_name": {
            "method": "source_attribute",
            "source_attribute": "expected_outcome",
        },
    },
)

long_schematisation = make_temp_copy(
    SCHEMATA / "schematisation_surface_attr_match.gpkg"
)
long_src = gpkg_layer(
    str(make_temp_copy(SOURCE / "surfaces_long_attr_match.gpkg")), "surface"
)
long_surface = gpkg_layer(long_schematisation, "surface")
long_surface_map = gpkg_layer(long_schematisation, "surface_map")

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    importer = SurfaceImporter(
        long_src,
        long_schematisation,
        long_config,
        surface_layer=long_surface,
        surface_map_layer=long_surface_map,
    )
    importer.import_features()

importer.commit_pending_changes()

for w in caught:
    print(f"  warning: {w.category.__name__}: {w.message}")

surface_count = long_surface.featureCount()
surface_map_count = long_surface_map.featureCount()
print(f"  surface rows: {surface_count}")
print(f"  surface_map rows: {surface_map_count}")

print("  surfaces:")
for feat in sorted(long_surface.getFeatures(), key=lambda f: f["id"]):
    print(f"    id={feat['id']} display_name={feat['display_name']!r}")

print("  surface_map:")
for feat in sorted(long_surface_map.getFeatures(), key=lambda f: f["id"]):
    print(
        f"    id={feat['id']} surface_id={feat['surface_id']} "
        f"connection_node_id={feat['connection_node_id']} "
        f"percentage={feat['percentage']} display_name={feat['display_name']!r}"
    )

# Expected per README:
# 6 surfaces (all 7 source features create a surface row — including zero_pct)
# 5 surface_map rows (no_match_no_spatial warns + no row; zero_pct_skipped has pct=0)
assert surface_count == 5, f"Expected 5 surface rows, got {surface_count}"
assert surface_map_count == 5, f"Expected 5 surface_map rows, got {surface_map_count}"

shutil.copy(long_schematisation, REF / "test_import_surface_long_attr_match.gpkg")
print("  -> saved to ref/test_import_surface_long_attr_match.gpkg")

print("\nDone!")
