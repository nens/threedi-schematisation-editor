from osgeo import gdal

gdal.UseExceptions()

from tests.utils import DATA_DIR
from threedi_schematisation_editor.processing.deps.merge import merge_rasters


def test_merge_rasters():
    rasters = [gdal.Open(str(DATA_DIR / f"raster{i}.tif")) for i in [1, 2, 3]]
    merge_rasters(
        rasters,
        tile_size=10,
        aggregation_method="min",
        output_filename=str(DATA_DIR / "merged.tif"),
        output_pixel_size=0.5,
        output_nodatavalue=-9999,
    )
    assert (DATA_DIR / "merged.tif").is_file()
