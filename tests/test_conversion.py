import shutil
import os
import gc
import json
import pytest

from functools import wraps
from pathlib import Path

from qgis.core import QgsApplication, QgsProcessingFeedback, QgsVectorLayer, QgsWkbTypes, NULL
from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
from threedi_schematisation_editor.processing import ThreediSchematisationEditorProcessingProvider


@pytest.fixture(scope="session")
def ref_data():
    with open(Path(__file__).parent.absolute().joinpath('data', 'ref_conversion.json')) as file:
        return json.load(file)

def read_layer(gpkg_path, layername):
    # Create a vector layer
    layer_uri = f"{gpkg_path}|layername={layername}"
    layer = QgsVectorLayer(layer_uri, layername, "ogr")

    if not layer.isValid():
        print(f"Layer '{layername}' failed to load from {gpkg_path}")
        return None

    # Read features
    result_dict = {}
    for feature in layer.getFeatures():
        result_dict[str(feature['id'])] = feature.geometry().asWkt(6).replace(' (','(').upper()

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


def compare_to_ref(ref_data, task_name, target_gpkg):
    for table, data in ref_data[task_name].items():
        new_data = read_layer(target_gpkg, table)
        assert set(new_data.items()) == set(data.items())


def test_conversion_connection_nodes(qgis_application, ref_data):
    task = {
        'SOURCE_LAYER': get_source_layer_path('connection_nodes.gpkg'),
        'IMPORT_CONFIG': get_import_config_path('import_connection_nodes'),
        'TARGET_GPKG': get_schematisation_copy('schematisation_channel.gpkg', 'test_connection_node.gpkg')
    }
    run_processing_operation('threedi_import_connection_nodes', task)
    compare_to_ref(ref_data, 'test_import_connection_nodes', task['TARGET_GPKG'])


class TestConversionWeir:
    source_layer = get_source_layer_path('weir.gpkg')
    schematisation = 'schematisation_channel_with_weir.gpkg'

    def get_task(self, task_name):
        return {
            'SOURCE_LAYER': self.source_layer,
            'IMPORT_CONFIG': get_import_config_path(task_name),
            'TARGET_GPKG': get_schematisation_copy(self.schematisation, f'test_{task_name}.gpkg')
        }

    # def compare_result(self, task_name):


    def check_weir_added(self, task):
        # todo: consider just comparing with reference instead of this complicated stuff!

        original_weirs = read_layer(get_schematisation_path(self.schematisation), 'weir')
        target_weirs = read_layer(task['TARGET_GPKG'], 'weir')
        assert len(target_weirs) - len(original_weirs) == 1
        # check geometry


    def check_connection_nodes_added(self, task):
        original_connection_nodes = read_layer(get_schematisation_path(self.schematisation), 'connection_node')
        target_connection_nodes = read_layer(task['TARGET_GPKG'], 'connection_node')
        assert len(target_connection_nodes) - len(original_connection_nodes) == 2

    def test_import_weir_snap(self, qgis_application, ref_data):
        task = self.get_task('import_weir_snap')
        run_processing_operation('threedi_import_weirs', task)
        compare_to_ref(ref_data, 'test_import_weir_snap', task['TARGET_GPKG'])

    def test_import_weir_nosnap(self, qgis_application, ref_data):
        task = self.get_task('import_weir_nosnap')
        run_processing_operation('threedi_import_weirs', task)
        compare_to_ref(ref_data, 'test_import_weir_nosnap', task['TARGET_GPKG'])

    def test_integrate_weir_snap(self, qgis_application, ref_data):
        task = self.get_task('integrate_weir_snap')
        run_processing_operation('threedi_import_weirs', task)
        compare_to_ref(ref_data, 'test_integrate_weir_snap', task['TARGET_GPKG'])

    def test_integrate_weir_nosnap(self, qgis_application, ref_data):
        task = self.get_task('integrate_weir_nosnap')
        run_processing_operation('threedi_import_weirs', task)
        compare_to_ref(ref_data, 'test_integrate_weir_nosnap', task['TARGET_GPKG'])
