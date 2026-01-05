from collections import defaultdict
from functools import cached_property
from typing import Optional

from qgis.core import (
    QgsCoordinateTransform,
    QgsPointLocator,
    QgsProcessingFeatureSource,
    QgsProject,
    QgsVectorLayer,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import gpkg_layer
from threedi_schematisation_editor.vector_data_importer.integrators import (
    LinearIntegrator,
)
from threedi_schematisation_editor.vector_data_importer.processors import (
    ConnectionNodeProcessor,
    CrossSectionDataProcessor,
    CrossSectionLocationProcessor,
    LineProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import get_point_locator


class Importer:
    def __init__(self, external_source, target_gpkg, import_settings):
        self.external_source = external_source
        self.target_gpkg = target_gpkg
        self.import_settings = import_settings
        self.processor = None

    @cached_property
    def external_source_name(self):
        try:
            layer_name = self.external_source.name()
        except AttributeError:
            layer_name = self.external_source.sourceName()
        return layer_name

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
        raise NotImplementedError

    def start_editing(self):
        # start editing in all layers to support changes during import
        for layer in self.modifiable_layers:
            layer.startEditing()

    def get_input_feature_ids(self, selected_ids):
        input_feature_ids = [feat.id() for feat in self.external_source.getFeatures()]
        if selected_ids:
            input_feature_ids = [id for id in input_feature_ids if id in selected_ids]
        return input_feature_ids

    def process_features(
        self, input_feature_ids, new_features=None, progress_callback=None
    ):
        external_features = [
            self.external_source.getFeature(feat_id) for feat_id in input_feature_ids
        ]
        processed_features = self.processor.process_features(
            external_features, progress_callback=progress_callback
        )
        if new_features is None or len(new_features) == 0:
            return processed_features
        else:
            for name, features in processed_features.items():
                new_features[name] += features
            return new_features

    def add_features_to_layers(self, new_features):
        for layer in self.modifiable_layers:
            if layer.name() in new_features:
                layer.addFeatures(new_features[layer.name()])

    def import_features(self, context=None, selected_ids=None, progress_callback=None):
        self.start_editing()
        input_feature_ids = self.get_input_feature_ids(selected_ids)
        if progress_callback:
            progress_callback(value=0, maximum=len(input_feature_ids))
        new_features = self.process_features(
            input_feature_ids, progress_callback=progress_callback
        )
        self.add_features_to_layers(new_features)


class CrossSectionDataImporter(Importer):
    def __init__(
        self,
        external_source: QgsVectorLayer,
        target_gpkg,
        import_settings: dict,
        target_layers: Optional[list[QgsVectorLayer]] = None,
    ):
        super().__init__(external_source, target_gpkg, import_settings)
        if not target_layers:
            target_layers = [
                gpkg_layer(target_gpkg, model_cls.__tablename__)
                for model_cls in CrossSectionDataProcessor.target_models
            ]
        self.target_layers = target_layers
        self.processor = CrossSectionDataProcessor(
            target_layers=target_layers, import_settings=self.import_settings
        )

    @property
    def modifiable_layers(self):
        return self.target_layers


class SpatialImporter(Importer):
    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_model_cls,
        target_layer=None,
        node_layer=None,
    ):
        super().__init__(external_source, target_gpkg, import_settings)
        self.target_model_cls = target_model_cls
        self.target_layer = (
            gpkg_layer(self.target_gpkg, target_model_cls.__tablename__)
            if target_layer is None
            else target_layer
        )
        self.node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__)
            if node_layer is None
            else node_layer
        )
        self.integrator = None
        self.processor = None

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
        return QgsCoordinateTransform(
            self.external_source.sourceCrs(), self.target_layer.crs(), transform_ctx
        )

    @property
    def modifiable_layers(self):
        """Return a list of the layers that can be modified."""
        layers = [self.target_layer, self.node_layer]
        if self.integrator:
            layers += self.integrator.modifiable_layers
        return layers

    def integrate_features(self, input_feature_ids, progress_callback=None):
        if self.integrator:
            # TODO: handle transform here?
            if self.processor.transformation:
                from threedi_schematisation_editor.utils import spatial_index

                self.integrator.spatial_indexes_map["source"] = spatial_index(
                    self.external_source, transform=self.processor.transformation
                )
            new_features, integrated_ids = self.integrator.integrate_features(
                input_feature_ids, progress_callback=progress_callback
            )
            input_feature_ids = [
                id for id in input_feature_ids if id not in integrated_ids
            ]
        else:
            new_features = defaultdict(list)
        return new_features, input_feature_ids

    def import_features(self, context=None, selected_ids=None, progress_callback=None):
        """Method responsible for the importing structures from the external feature source."""
        # setup processor
        self.processor.transformation = self.get_transformation(context)
        self.processor.node_locator = get_point_locator(
            self.node_layer, context=context
        )
        self.processor.context = context
        # start editing
        self.start_editing()
        input_feature_ids = self.get_input_feature_ids(selected_ids)
        if progress_callback:
            progress_callback(value=0, maximum=len(input_feature_ids))
        # Integrate features using the integrator (if any)
        # items that are integrated are skipped in further processing
        new_features, input_feature_ids = self.integrate_features(
            input_feature_ids, progress_callback=progress_callback
        )
        # Process remaining features that are not integrated
        new_features = self.process_features(
            input_feature_ids, new_features, progress_callback
        )
        # Add newly created features to layers
        self.add_features_to_layers(new_features)


class LinesImporter(SpatialImporter):
    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_model_cls,
        target_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=target_model_cls,
            target_layer=target_layer,
            node_layer=node_layer,
        )
        self.processor = LineProcessor(
            self.target_layer,
            self.target_model_cls,
            self.node_layer,
            import_settings,
        )
        self.integrator = LinearIntegrator.get_integrator(
            conduit_layer, cross_section_location_layer, self
        )


class CulvertsImporter(LinesImporter):
    """Class with methods responsible for the integrating culverts from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        structure_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Culvert,
            target_layer=structure_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )


class OrificesImporter(LinesImporter):
    """Class with methods responsible for the integrating orifices from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        structure_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Orifice,
            target_layer=structure_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )


class WeirsImporter(LinesImporter):
    """Class with methods responsible for the integrating weirs from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        structure_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Weir,
            target_layer=structure_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )


class PipesImporter(LinesImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        structure_layer=None,
        node_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Pipe,
            target_layer=structure_layer,
            node_layer=node_layer,
        )


class ChannelsImporter(LinesImporter):
    """Class with methods responsible for the importing channels from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        structure_layer=None,
        node_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Channel,
            target_layer=structure_layer,
            node_layer=node_layer,
        )


class CrossSectionLocationImporter(SpatialImporter):
    def __init__(
        self, external_source, target_gpkg, import_settings, target_layer=None
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.CrossSectionLocation,
            target_layer=target_layer,
        )
        self.processor = CrossSectionLocationProcessor(
            target_layer=self.target_layer,
            target_model_cls=dm.CrossSectionLocation,
            channel_layer=gpkg_layer(self.target_gpkg, dm.Channel.__tablename__),
            import_settings=self.import_settings,
        )


class ConnectionNodesImporter(SpatialImporter):
    """Connection nodes importer class."""

    def __init__(
        self, external_source, target_gpkg, import_settings, target_layer=None
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.ConnectionNode,
            target_layer=target_layer,
        )
        self.processor = ConnectionNodeProcessor(
            self.target_layer,
            self.target_model_cls,
            self.import_settings,
        )
