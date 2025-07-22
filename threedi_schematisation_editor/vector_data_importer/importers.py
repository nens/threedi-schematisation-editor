from collections import defaultdict
from functools import cached_property
from abc import ABC

from qgis.core import QgsCoordinateTransform, QgsPointLocator, QgsProject

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.vector_data_importer.integrators import LinearIntegrator
from threedi_schematisation_editor.vector_data_importer.processors import ConnectionNodeProcessor, LineProcessor
from threedi_schematisation_editor.vector_data_importer.utils import ConversionSettings
from threedi_schematisation_editor.utils import gpkg_layer




class Importer(ABC):
    """Base class for the importing features from the external data source."""

    def __init__(self,
                 external_source,
                 target_gpkg,
                 import_settings,
                 target_model_cls,
                 target_layer=None,
                 node_layer=None,
                 ):
        self.external_source = external_source
        self.target_gpkg = target_gpkg
        self.import_settings = import_settings
        self.target_model_cls = target_model_cls
        self.target_layer = (
            gpkg_layer(self.target_gpkg, target_model_cls.__tablename__) if target_layer is None else target_layer
        )
        self.node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__) if node_layer is None else node_layer
        )
        self.fields_configurations = {
            target_model_cls: self.import_settings.get("fields", {}),
            dm.ConnectionNode: self.import_settings.get("connection_node_fields", {}),
        }
        self.integrator = None
        self.processor = None

    @cached_property
    def conversion_settings(self):
        conversion_config = self.import_settings["conversion_settings"]
        return ConversionSettings(conversion_config)

    @cached_property
    def external_source_name(self):
        try:
            layer_name = self.external_source.name()
        except AttributeError:
            layer_name = self.external_source.sourceName()
        return layer_name

    def get_transformation(self, context=None):
        if self.external_source.sourceCrs() == self.target_layer.crs():
            return None
        project = context.project() if context else QgsProject.instance()
        transform_ctx = project.transformContext()
        return QgsCoordinateTransform(self.external_source.sourceCrs(), self.target_layer.crs(), transform_ctx)

    def get_locator(self, context=None):
        project = context.project() if context else QgsProject.instance()
        return QgsPointLocator(self.node_layer, self.target_layer.crs(), project.transformContext())

    @staticmethod
    def process_commit_errors(layer):
        commit_errors = layer.commitErrors()
        commit_errors_message = "\n".join(commit_errors)
        return commit_errors_message

    def commit_pending_changes(self):
        for layer in self.modifiable_layers:
            if layer.isModified():
                layer.commitChanges()

    @property
    def modifiable_layers(self):
        """Return a list of the layers that can be modified."""
        layers = [self.target_layer, self.node_layer]
        if self.integrator:
            layers += [self.integrator.integrate_layer,
                       self.integrator.cross_section_layer]
        return layers

    def import_features(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        self.processor.transformation = self.get_transformation(context)
        self.processor.locator = self.get_locator(context=context)
        # start editing in all layers to support changes during import
        for layer in self.modifiable_layers:
            layer.startEditing()
        # Integrate features using the integrator (if any)
        # items that are integrated are skipped in further processing
        if self.integrator:
            input_feature_ids = [feat.id() for feat in self.external_source.getFeatures()]
            if selected_ids:
                input_feature_ids = [id for id in input_feature_ids if id in selected_ids]
            new_features, integrated_ids = self.integrator.integrate_features(input_feature_ids)
        else:
            new_features = defaultdict(list)
            integrated_ids = []
        # Process remaining features that are not integrated
        for external_src_feat in self.external_source.getFeatures():
            if selected_ids and external_src_feat.id() not in selected_ids:
                continue
            if external_src_feat.id() in integrated_ids:
                continue
            processed_features = self.processor.process_feature(external_src_feat)
            for name, features in processed_features.items():
                new_features[name] += features
        # Add newly created features to layers
        for layer in self.modifiable_layers:
            if layer.name() in new_features:
                layer.addFeatures(new_features[layer.name()])


class LinesImporter(Importer):

    def __init__(
            self,
            *args,
            target_model_cls,
            target_layer=None,
            node_layer=None,
            channel_layer=None,
            cross_section_location_layer=None,
    ):
        super().__init__(*args, target_model_cls=target_model_cls, target_layer=target_layer,
                         node_layer=node_layer)
        self.processor = LineProcessor(self.target_layer, self.target_model_cls, self.node_layer,
                                       self.fields_configurations, self.conversion_settings)
        if self.conversion_settings.integrate:
            self.integrator = LinearIntegrator.from_importer(dm.Channel, channel_layer, cross_section_location_layer,
                                                             self)


class CulvertsImporter(LinesImporter):
    """Class with methods responsible for the integrating culverts from the external data source."""

    def __init__(
            self,
            *args,
            structure_layer=None,
            node_layer=None,
            channel_layer=None,
            cross_section_location_layer=None,
    ):
        super().__init__(*args, target_model_cls=dm.Culvert, target_layer=structure_layer,
                         node_layer=node_layer, channel_layer=channel_layer,
                         cross_section_location_layer=cross_section_location_layer)


class OrificesImporter(LinesImporter):
    """Class with methods responsible for the integrating orifices from the external data source."""

    def __init__(
            self,
            *args,
            structure_layer=None,
            node_layer=None,
            channel_layer=None,
            cross_section_location_layer=None,
    ):
        super().__init__(*args, target_model_cls=dm.Orifice, target_layer=structure_layer,
                         node_layer=node_layer, cchannel_layer=channel_layer,
                         cross_section_location_layer=cross_section_location_layer)


class WeirsImporter(LinesImporter):
    """Class with methods responsible for the integrating weirs from the external data source."""

    def __init__(
            self,
            *args,
            structure_layer=None,
            node_layer=None,
            channel_layer=None,
            cross_section_location_layer=None,
    ):
        super().__init__(*args, target_model_cls=dm.Weir, target_layer=structure_layer,
                         node_layer=node_layer, channel_layer=channel_layer,
                         cross_section_location_layer=cross_section_location_layer)


class PipesImporter(LinesImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args, target_model_cls=dm.Pipe, target_layer=structure_layer,
                         node_layer=node_layer)


class ConnectionNodesImporter(Importer):
    """Connection nodes importer class."""

    def __init__(self, *args, target_layer=None):
        super().__init__(*args, target_model_cls=dm.ConnectionNode, target_layer=target_layer)
        self.processor = ConnectionNodeProcessor(self.target_layer, self.target_model_cls)
