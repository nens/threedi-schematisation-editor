import shutil
import os
import gc
import pytest

from functools import wraps
from pathlib import Path

from qgis.core import QgsApplication, QgsProcessingFeedback, QgsVectorLayer, QgsWkbTypes, NULL
from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
from threedi_schematisation_editor.processing import ThreediSchematisationEditorProcessingProvider


def read_layer(gpkg_path, layername, id_field='id', fields_to_include=None):
    """
    Read the connection_nodes table from a GeoPackage and return a dictionary of dictionaries.

    Args:
        gpkg_path: Path to the GeoPackage
        layername: Name of the layer to read
        id_field: Field to use as the primary key (default: 'id')
        fields_to_include: List of field names to include

    Returns:
        Dictionary with structure {id: {'geom': geometry_obj, 'field1': value1, ...}}
    """

    # Create a vector layer
    layer_uri = f"{gpkg_path}|layername={layername}"
    layer = QgsVectorLayer(layer_uri, layername, "ogr")

    if not layer.isValid():
        print(f"Layer '{layername}' failed to load from {gpkg_path}")
        return None

    if fields_to_include is None:
        fields_to_include = []

    # Get field names
    all_field_names = [field.name() for field in layer.fields()]

    # Check if id_field exists
    if id_field not in all_field_names:
        print(f"Error: ID field '{id_field}' not found in layer. Available fields: {all_field_names}")
        return None

    # Read features
    result_dict = {}
    for feature in layer.getFeatures():
        # Skip if ID is NULL
        if feature[id_field] == NULL:
            continue

        feature_id = feature[id_field]

        # Initialize feature dictionary
        feature_dict = {}

        # Add requested fields
        for field in fields_to_include:
            if field in all_field_names:
                feature_dict[field] = feature[field] if feature[field] != NULL else None

        # Add geometry
        geom = feature.geometry()
        if geom and not geom.isNull():
            # Get geometry type
            geom_type = QgsWkbTypes.displayString(geom.wkbType())
            # Create geometry dictionary based on type
            if 'Point' in geom_type:
                point = geom.asPoint()
                feature_dict['geom'] = {
                    'type': geom_type,
                    'coords': (point.x(), point.y()),
                    'wkt': geom.asWkt()
                }
            elif 'LineString' in geom_type:
                line = geom.asPolyline()
                feature_dict['geom'] = {
                    'type': geom_type,
                    'coords': [(p.x(), p.y()) for p in line],
                    'wkt': geom.asWkt()
                }
            elif 'Polygon' in geom_type:
                polygon = geom.asPolygon()
                feature_dict['geom'] = {
                    'type': geom_type,
                    'coords': [[(p.x(), p.y()) for p in ring] for ring in polygon],
                    'wkt': geom.asWkt()
                }
            else:
                # For other geometry types, just store WKT
                feature_dict['geom'] = {
                    'type': geom_type,
                    'wkt': geom.asWkt()
                }
        else:
            feature_dict['geom'] = None

        # Add to result
        result_dict[feature_id] = feature_dict

    return result_dict


def get_schematisation_path(schematisation):
    return Path(__file__).parent.absolute().joinpath('data', 'originals', schematisation)


def get_schematisation_copy(schematisation, test_name):
    data_dir = Path(__file__).parent.absolute().joinpath('data')
    tgt = data_dir.joinpath('results', test_name)
    shutil.copy(get_schematisation_path(schematisation), tgt)
    return str(tgt.absolute())


def get_source_layer_path(source_layer):
    return str(Path(__file__).parent.absolute().joinpath('data', source_layer))


def get_import_config_path(import_config_name):
    return str(Path(__file__).parent.absolute().joinpath('data', import_config_name).with_suffix('.json'))


# Define a session-scoped fixture to set up and tear down QGIS once for all tests
@pytest.fixture(scope="session")
def qgis_application():
    """Initialize QGIS application for the test session"""
    # Set environment for headless operation
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    print("Initializing QGIS for test session...")
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Initialize Processing framework
    print("Initializing Processing framework...")
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    # Add the ThreediSchematisationEditorProcessingProvider
    try:
        provider = ThreediSchematisationEditorProcessingProvider()
        QgsApplication.processingRegistry().addProvider(provider)
    except ImportError:
        print("Warning: ThreediSchematisationEditorProcessingProvider not available")

    yield qgs

    # Cleanup when all tests are done
    print("Exiting QGIS...")
    gc.collect()  # Force garbage collection before exit
    qgs.exitQgis()
    gc.collect()  # Final cleanup
    print("QGIS cleanup complete.")


def run_processing_operation(algo_name, task):
    try:
        processing.run(
            f"threedi_schematisation_editor:{algo_name}",
            task,
            feedback=QgsProcessingFeedback()
        )
    except:
        pytest.fail(f"Failed to run {algo_name} with task {task}")


def test_conversion_connection_nodes(qgis_application):
    task = {
        'SOURCE_LAYER': get_source_layer_path('connection_nodes.gpkg'),
        'IMPORT_CONFIG': get_import_config_path('import_connection_nodes'),
        'TARGET_GPKG': get_schematisation_copy('schematisation_channel.gpkg', 'test_connection_node.gpkg')
    }
    run_processing_operation('threedi_import_connection_nodes', task)
    # Read source and target tables
    source_data = read_layer(task['SOURCE_LAYER'], "connection_nodes")
    target_data = read_layer(task['TARGET_GPKG'], "connection_node")
    assert source_data[1] == target_data[1517]
    assert source_data[1069] == target_data[1518]
    assert len(target_data) == 4


class TestConversionWeir:
    source_layer = get_source_layer_path('weir.gpkg')
    schematisation = 'schematisation_channel_with_weir.gpkg'

    def get_task(self, task_name):
        return {
            'SOURCE_LAYER': self.source_layer,
            'IMPORT_CONFIG': get_import_config_path(task_name),
            'TARGET_GPKG': get_schematisation_copy(self.schematisation, f'test_{task_name}.gpkg')
        }

    def check_weir_added(self, task):
        # todo: consider just comparing with reference instead of this complicated stuff!
        lenght = 1
        azimuth  = 90
        original_weirs = read_layer(get_schematisation_path(self.schematisation), 'weir')
        target_weirs = read_layer(task['TARGET_GPKG'], 'weir')
        assert len(target_weirs) - len(original_weirs) == 1
        # check geometry


    def check_connection_nodes_added(self, task):
        original_connection_nodes = read_layer(get_schematisation_path(self.schematisation), 'connection_node')
        target_connection_nodes = read_layer(task['TARGET_GPKG'], 'connection_node')
        assert len(target_connection_nodes) - len(original_connection_nodes) == 2

    def test_import_weir_snap(self, qgis_application):
        task = self.get_task('import_weir_snap')
        run_processing_operation('threedi_import_weirs', task)
        self.check_weir_added(task)
        self.check_connection_nodes_added(task)
        # source_weirs = read_layer(task['SOURCE_LAYER'], 'dhydro weir')
        # target_weirs = read_layer(task['TARGET_GPKG'], 'weir')
        # target_connection_nodes = read_layer(task['TARGET_GPKG'], 'connection_node')
        # # generic
        # assert len(target_weirs) == 2 # 1 added
        # assert len(target_connection_nodes) == 8 # 2 added
        # breakpoint()
        # # source_weirs[1] == target_weirs[2]

    def test_import_weir_nosnap(self, qgis_application):
        task = self.get_task('import_weir_nosnap')
        run_processing_operation('threedi_import_weirs', task)
        self.check_weir_added(task)
        self.check_connection_nodes_added(task)

    def test_integrate_weir_snap(self, qgis_application):
        task = self.get_task('integrate_weir_snap')
        run_processing_operation('threedi_import_weirs', task)
        self.check_weir_added(task)
        self.check_connection_nodes_added(task)

    def test_integrate_weir_nosnap(self, qgis_application):
        task = self.get_task('integrate_weir_nosnap')
        run_processing_operation('threedi_import_weirs', task)
        self.check_weir_added(task)
        self.check_connection_nodes_added(task)
