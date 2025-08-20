from unittest.mock import MagicMock, patch

import pytest
from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.importers import (
    Importer,
    LinesImporter,
)


@pytest.fixture
def import_settings():
    """Create a basic import settings dictionary."""
    return {
        "conversion_settings": {
            "use_snapping": True,
            "snapping_distance": 5.0,
            "create_connection_nodes": True,
            "length_source_field": "length",
            "length_fallback_value": 10.0,
            "azimuth_source_field": "azimuth",
            "azimuth_fallback_value": 90.0,
            "edit_channels": False,
        },
        "fields": {"id": {"method": "auto"}},
        "connection_node_fields": {"id": {"method": "auto"}},
    }


@pytest.fixture
def external_source():
    """Create a mock external source layer."""
    source = MagicMock()
    source.name.return_value = "external_source"
    source.sourceCrs.return_value = "EPSG:28992"
    return source


@pytest.fixture
def target_gpkg():
    """Create a mock target gpkg path."""
    return "/path/to/target.gpkg"


@pytest.fixture
def target_layer():
    """Create a mock target layer."""
    layer = MagicMock()
    layer.name.return_value = "pipes"
    layer.crs.return_value = "EPSG:28992"

    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    layer.fields.return_value = fields

    return layer


@pytest.fixture
def node_layer():
    """Create a mock node layer."""
    layer = MagicMock()
    layer.name.return_value = "connection_nodes"

    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    layer.fields.return_value = fields

    return layer


@pytest.fixture
def channel_layer():
    """Create a mock channel layer."""
    layer = MagicMock()
    layer.name.return_value = "channels"

    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    layer.fields.return_value = fields

    return layer


@pytest.fixture
def cross_section_location_layer():
    """Create a mock cross section location layer."""
    layer = MagicMock()
    layer.name.return_value = "cross_section_locations"

    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("channel_id", QVariant.Int))
    layer.fields.return_value = fields

    return layer


@pytest.fixture
def importer(external_source, target_gpkg, import_settings, target_layer, node_layer):
    """Create an Importer instance with standard parameters."""
    return Importer(
        external_source, target_gpkg, import_settings, dm.Pipe, target_layer, node_layer
    )


@pytest.fixture
def importer_different_crs(
    external_source, target_gpkg, import_settings, target_layer, node_layer
):
    """Create an Importer instance with different CRS."""
    external_source.sourceCrs.return_value = "EPSG:4326"
    return Importer(
        external_source, target_gpkg, import_settings, dm.Pipe, target_layer, node_layer
    )


@pytest.fixture
def mock_project():
    with patch(
        "threedi_schematisation_editor.vector_data_importer.importers.QgsProject"
    ) as mock:
        mock_instance = MagicMock()
        mock.instance.return_value = mock_instance
        mock_instance.transformContext.return_value = "transform_context"
        yield mock


class TestImporter:
    """Tests for the Importer base class."""

    def test_init(
        self, external_source, target_gpkg, import_settings, target_layer, node_layer
    ):
        """Test that the Importer initializes correctly."""
        importer = Importer(
            external_source,
            target_gpkg,
            import_settings,
            dm.Pipe,
            target_layer,
            node_layer,
        )

        assert importer.external_source == external_source
        assert importer.target_gpkg == target_gpkg
        assert importer.import_settings == import_settings
        assert importer.target_model_cls == dm.Pipe
        assert importer.target_layer == target_layer
        assert importer.node_layer == node_layer
        assert importer.integrator is None
        assert importer.processor is None

    def test_conversion_settings(self, importer, import_settings):
        """Test that conversion_settings returns a ConversionSettings object with the correct values."""
        settings = importer.conversion_settings
        for key, val in import_settings["conversion_settings"].items():
            assert getattr(settings, key) == val

    def test_external_source_name(
        self, target_gpkg, import_settings, importer, target_layer, node_layer
    ):
        """Test that external_source_name returns the correct name when external_source has a name method."""
        assert importer.external_source_name == "external_source"
        alt_external_source = MagicMock()
        alt_external_source.name.side_effect = AttributeError("No name method")
        alt_external_source.sourceName.return_value = "alt_source"
        importer = Importer(
            alt_external_source,
            target_gpkg,
            import_settings,
            dm.Pipe,
            target_layer,
            node_layer,
        )
        assert importer.external_source_name == "alt_source"

    # @patch('threedi_schematisation_editor.vector_data_importer.importers.QgsCoordinateTransform')
    def test_get_transformation_same_crs(self, importer):
        """Test that get_transformation returns None when the CRS is the same."""
        assert importer.get_transformation() is None

    @patch(
        "threedi_schematisation_editor.vector_data_importer.importers.QgsCoordinateTransform"
    )
    def test_get_transformation_different_crs(
        self, mock_transform, mock_project, importer_different_crs
    ):
        """Test that get_transformation returns a QgsCoordinateTransform when the CRS is different."""
        # Mock the QgsProject instance and transform context
        mock_instance = MagicMock()
        mock_project.instance.return_value = mock_instance
        mock_instance.transformContext.return_value = "transform_context"
        result = importer_different_crs.get_transformation()
        mock_transform.assert_called_once_with(
            "EPSG:4326", "EPSG:28992", "transform_context"
        )

    @patch(
        "threedi_schematisation_editor.vector_data_importer.importers.QgsPointLocator"
    )
    def test_get_locator(self, mock_locator, mock_project, importer, node_layer):
        """Test that get_locator returns a QgsPointLocator."""
        # Mock the QgsProject instance and transform context
        mock_instance = MagicMock()
        mock_project.instance.return_value = mock_instance
        mock_instance.transformContext.return_value = "transform_context"
        importer.get_locator(None)
        mock_locator.assert_called_once_with(
            node_layer, "EPSG:28992", "transform_context"
        )

    def test_process_commit_errors(self, importer):
        """Test that process_commit_errors returns the commit errors message."""
        layer = MagicMock()
        layer.commitErrors.return_value = ["Error 1", "Error 2"]
        assert Importer.process_commit_errors(layer) == "Error 1\nError 2"

    def test_commit_pending_changes(self, importer, target_layer, node_layer):
        """Test that commit_pending_changes commits changes for modified layers."""
        target_layer.isModified.return_value = True
        node_layer.isModified.return_value = False
        importer.commit_pending_changes()
        target_layer.commitChanges.assert_called_once()
        node_layer.commitChanges.assert_not_called()

    def test_modifiable_layers_without_integrator(
        self, importer, target_layer, node_layer
    ):
        """Test that modifiable_layers returns the target and node layers when there is no integrator."""
        assert importer.modifiable_layers == [target_layer, node_layer]

    def test_modifiable_layers_with_integrator(
        self, importer, target_layer, node_layer
    ):
        """Test that modifiable_layers includes integrator layers when there is an integrator."""
        # Create a mock integrator
        integrator = MagicMock()
        integrator.integrate_layer = MagicMock()
        integrator.cross_section_layer = MagicMock()
        importer.integrator = integrator
        assert importer.modifiable_layers == [
            target_layer,
            node_layer,
            integrator.integrate_layer,
            integrator.cross_section_layer,
        ]

    @patch(
        "threedi_schematisation_editor.vector_data_importer.importers.ChannelIntegrator.from_importer"
    )
    @patch(
        "threedi_schematisation_editor.vector_data_importer.importers.PipeIntegrator.from_importer"
    )
    @pytest.mark.parametrize(
        "edit_channels, edit_pipes, target_cls, make_channel_integrator, make_pipe_integrator",
        [
            (True, True, dm.Weir, True, False),
            (True, False, dm.Weir, True, False),
            (False, True, dm.Weir, False, True),
            (False, False, dm.Weir, False, False),
            (False, True, dm.Culvert, False, False),
        ],
    )
    def test_init_integrator(
        self,
        mock_pipe_integrator_from_importer,
        mock_channel_integrator_from_importer,
        external_source,
        target_gpkg,
        import_settings,
        target_layer,
        node_layer,
        edit_channels,
        edit_pipes,
        target_cls,
        make_channel_integrator,
        make_pipe_integrator,
    ):
        """Test that the Importer initializes the correct integrator."""
        import_settings["conversion_settings"]["edit_channels"] = edit_channels
        import_settings["conversion_settings"]["edit_pipes"] = edit_pipes
        importer = LinesImporter(
            external_source,
            target_gpkg,
            import_settings,
            target_model_cls=target_cls,
            target_layer=target_layer,
            node_layer=node_layer,
        )
        if make_channel_integrator:
            mock_channel_integrator_from_importer.assert_called_once_with(
                None, None, importer
            )
        else:
            mock_channel_integrator_from_importer.assert_not_called()
        if make_pipe_integrator:
            mock_pipe_integrator_from_importer.assert_called_once_with(
                None, None, importer
            )
        else:
            mock_pipe_integrator_from_importer.assert_not_called()
