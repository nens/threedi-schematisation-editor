from collections import defaultdict
from functools import cached_property
from typing import Optional

from qgis.core import (
    QgsCoordinateTransform,
    QgsFeature,
    QgsGeometry,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.utils import get_next_feature_id, gpkg_layer
from threedi_schematisation_editor.vector_data_importer.integrators import (
    LinearIntegrator,
    LineStructurePlacement,
    PointStructurePlacement,
    PumpMapNodeHandler,
    StructureNodeHandler,
)
from threedi_schematisation_editor.vector_data_importer.processors import (
    ConnectionNodeProcessor,
    CrossSectionDataProcessor,
    CrossSectionLocationProcessor,
    LineProcessor,
    PointProcessor,
    PumpProcessor,
    SurfaceProcessor,
)
from threedi_schematisation_editor.vector_data_importer.utils import (
    ColumnImportMethod,
    FeatureManager,
    get_field_config_value,
    get_point_locator,
)


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
    ):
        super().__init__(external_source, target_gpkg, import_settings)
        self.target_model_cls = target_model_cls
        self.target_layer = (
            gpkg_layer(self.target_gpkg, target_model_cls.__tablename__)
            if target_layer is None
            else target_layer
        )
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
        return [self.target_layer]

    def import_features(self, context=None, selected_ids=None, progress_callback=None):
        self.processor.transformation = self.get_transformation(context)
        self.processor.context = context
        self.start_editing()
        input_feature_ids = self.get_input_feature_ids(selected_ids)
        if progress_callback:
            progress_callback(value=0, maximum=len(input_feature_ids))
        new_features = self.process_features(
            input_feature_ids, progress_callback=progress_callback
        )
        self.add_features_to_layers(new_features)


class IntegrationImporter(SpatialImporter):
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
        )
        self.node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__)
            if node_layer is None
            else node_layer
        )
        self.processor = None
        self._conduit_layer = conduit_layer
        self._cross_section_location_layer = cross_section_location_layer

    @cached_property
    def integrator(self):
        return LinearIntegrator.get_integrator(
            self._conduit_layer, self._cross_section_location_layer, self
        )

    @property
    def integration_model_cls(self):
        return self.target_model_cls

    @property
    def integration_layer(self):
        return self.target_layer

    @property
    def integration_manager(self):
        return self.processor.target_manager

    @property
    def modifiable_layers(self):
        layers = [self.target_layer, self.node_layer]
        if self.integrator:
            layers += self.integrator.modifiable_layers
        return layers

    def integrate_features(self, input_feature_ids, progress_callback=None):
        if self.integrator:
            if self.processor.transformation:
                self.integrator.set_transformed_spatial_index(
                    transform=self.processor.transformation
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
        self.processor.transformation = self.get_transformation(context)
        self.processor.node_locator = get_point_locator(
            self.node_layer, context=context
        )
        self.processor.context = context
        self.start_editing()
        input_feature_ids = self.get_input_feature_ids(selected_ids)
        if progress_callback:
            progress_callback(value=0, maximum=len(input_feature_ids))
        new_features, input_feature_ids = self.integrate_features(
            input_feature_ids, progress_callback=progress_callback
        )
        new_features = self.process_features(
            input_feature_ids, new_features, progress_callback
        )
        self.add_features_to_layers(new_features)


class CulvertsImporter(IntegrationImporter):
    """Class with methods responsible for the integrating culverts from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Culvert,
            target_layer=target_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )
        self.processor = LineProcessor(
            self.target_layer, self.target_model_cls, self.node_layer, import_settings
        )


class OrificesImporter(IntegrationImporter):
    """Class with methods responsible for the integrating orifices from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Orifice,
            target_layer=target_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )
        self.processor = LineProcessor(
            self.target_layer, self.target_model_cls, self.node_layer, import_settings
        )


class WeirsImporter(IntegrationImporter):
    """Class with methods responsible for the integrating weirs from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
        conduit_layer=None,
        cross_section_location_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Weir,
            target_layer=target_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
            cross_section_location_layer=cross_section_location_layer,
        )
        self.processor = LineProcessor(
            self.target_layer, self.target_model_cls, self.node_layer, import_settings
        )


class PipesImporter(IntegrationImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Pipe,
            target_layer=target_layer,
            node_layer=node_layer,
        )
        self.processor = LineProcessor(
            self.target_layer, self.target_model_cls, self.node_layer, import_settings
        )


class ChannelsImporter(IntegrationImporter):
    """Class with methods responsible for the importing channels from the external data source."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Channel,
            target_layer=target_layer,
            node_layer=node_layer,
        )
        self.processor = LineProcessor(
            self.target_layer, self.target_model_cls, self.node_layer, import_settings
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


class PumpsImporter(IntegrationImporter):
    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_layer=None,
        node_layer=None,
        conduit_layer=None,
        pump_map_layer=None,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Pump,
            target_layer=target_layer,
            node_layer=node_layer,
            conduit_layer=conduit_layer,
        )
        self.pump_map_layer = (
            gpkg_layer(self.target_gpkg, dm.PumpMap.__tablename__)
            if pump_map_layer is None
            else pump_map_layer
        )
        self.processor = PointProcessor(
            self.target_layer,
            self.target_model_cls,
            self.node_layer,
            self.import_settings,
        )

    @property
    def integration_model_cls(self):
        return self.target_model_cls

    @property
    def integration_layer(self):
        return self.target_layer

    @property
    def integration_manager(self):
        return self.processor.target_manager

    @property
    def modifiable_layers(self):
        layers = [self.target_layer, self.pump_map_layer, self.node_layer]
        if self.integrator:
            layers += self.integrator.modifiable_layers
        return layers

    def build_pump_map_source_layer(self, context=None):
        """Build an in-memory LineString layer of resolved pump_map lines.

        For each source feature, tries attribute mapping then point_to_line to
        resolve an end point. Features with an end point become line features
        (all source fields copied — required for PumpMapNodeHandler attribute mapping).
        Returns (in_memory_layer, without_map_fids).
        """
        crs = self.target_layer.crs().authid()
        mem_layer = QgsVectorLayer(
            f"LineString?crs={crs}", "pump_map_source", "memory"
        )
        mem_layer.dataProvider().addAttributes(
            self.external_source.fields().toList()
        )
        mem_layer.updateFields()

        transformation = self.get_transformation(context)
        cn_id_end_config = self.import_settings.pump_linking.connection_node_id_end
        ptl = self.import_settings.point_to_line_conversion
        without_map_fids = []

        for src_feat in self.external_source.getFeatures():
            src_geom = src_feat.geometry()
            if transformation:
                src_geom.transform(transformation)
            start_point = src_geom.asPoint()

            end_point = None
            if cn_id_end_config.method != ColumnImportMethod.AUTO:
                node_id = get_field_config_value(cn_id_end_config, src_feat)
                if node_id is not None:
                    node_feat = next(
                        (
                            f for f in self.node_layer.getFeatures()
                            if f["id"] == node_id
                        ),
                        None,
                    )
                    if node_feat is not None:
                        end_point = node_feat.geometry().asPoint()

            if end_point is None:
                length = get_field_config_value(ptl.length, src_feat)
                azimuth = get_field_config_value(ptl.azimuth, src_feat)
                if length is not None and azimuth is not None:
                    end_point = start_point.project(length, azimuth)

            if end_point is not None:
                line_feat = QgsFeature(mem_layer.fields())
                line_feat.setGeometry(
                    QgsGeometry.fromPolylineXY([start_point, end_point])
                )
                # Copy all source fields so PumpMapNodeHandler can map pump attributes
                for field in self.external_source.fields():
                    line_feat[field.name()] = src_feat[field.name()]
                mem_layer.dataProvider().addFeature(line_feat)
            else:
                without_map_fids.append(src_feat.id())

        return mem_layer, without_map_fids

    def import_features(self, context=None, selected_ids=None, progress_callback=None):
        self.start_editing()
        all_features = defaultdict(list)

        # Phase A: pump_maps
        pump_map_source, without_map_fids = self.build_pump_map_source_layer(context)
        pump_map_source_fids = [f.id() for f in pump_map_source.getFeatures()]

        if pump_map_source_fids:
            pump_manager = FeatureManager(get_next_feature_id(self.target_layer))
            node_by_location = {
                f.geometry().asPoint(): f["id"]
                for f in self.node_layer.getFeatures()
            }
            pump_map_node_handler = PumpMapNodeHandler(
                pump_layer=self.target_layer,
                pump_manager=pump_manager,
                node_layer=self.node_layer,
                node_by_location=node_by_location,
                node_manager=FeatureManager(get_next_feature_id(self.node_layer)),
                layer_fields_mapping={
                    self.node_layer.name(): self.node_layer.fields(),
                    self.target_layer.name(): self.target_layer.fields(),
                },
                import_settings=self.import_settings,
            )

            integrated_fids = []
            integration_mode = self.import_settings.integration.integration_mode
            if integration_mode.value != "None" and self._conduit_layer is not None:
                length_config = self.import_settings.point_to_line_conversion.length
                strategy = LineStructurePlacement(length_config, simplify_geometry=True)
                integrator = LinearIntegrator(
                    conduit_layer=self._conduit_layer,
                    target_model_cls=dm.PumpMap,
                    target_layer=self.pump_map_layer,
                    target_manager=FeatureManager(get_next_feature_id(self.pump_map_layer)),
                    node_layer=self.node_layer,
                    node_manager=pump_map_node_handler.node_manager,
                    import_settings=self.import_settings,
                    external_source=pump_map_source,
                    target_gpkg=self.target_gpkg,
                    conduit_model_cls=dm.Pipe,
                    strategy=strategy,
                    node_handler=pump_map_node_handler,
                )
                integrated_features, integrated_fids = integrator.integrate_features(
                    pump_map_source_fids
                )
                for layer_name, feats in integrated_features.items():
                    all_features[layer_name] += feats

            # Remaining pump_maps: use PumpProcessor on the original source features
            remaining_fids = [
                fid for fid in pump_map_source_fids if fid not in integrated_fids
            ]
            if remaining_fids:
                pump_processor = PumpProcessor(
                    self.target_layer,
                    self.pump_map_layer,
                    self.node_layer,
                    self.import_settings,
                )
                pump_processor.transformation = self.get_transformation(context)
                pump_processor.node_locator = get_point_locator(self.node_layer, context)
                pump_processor.context = context
                # Map back from in-memory fids to original source features by field values
                remaining_src_feats = []
                for fid in remaining_fids:
                    mem_feat = pump_map_source.getFeature(fid)
                    for src_feat in self.external_source.getFeatures():
                        if all(
                            src_feat[f.name()] == mem_feat[f.name()]
                            for f in self.external_source.fields()
                        ):
                            remaining_src_feats.append(src_feat)
                            break
                processed = pump_processor.process_features(remaining_src_feats)
                for layer_name, feats in processed.items():
                    all_features[layer_name] += feats

        # Phase B: pumps without maps
        if without_map_fids:
            input_fids = without_map_fids
            if selected_ids:
                input_fids = [fid for fid in input_fids if fid in selected_ids]

            self.processor.transformation = self.get_transformation(context)
            self.processor.node_locator = get_point_locator(self.node_layer, context)
            self.processor.context = context

            if self.integrator:
                if self.processor.transformation:
                    self.integrator.set_transformed_spatial_index(
                        transform=self.processor.transformation
                    )
                integrated_features, input_fids = self.integrator.integrate_features(
                    input_fids
                )
                for layer_name, feats in integrated_features.items():
                    all_features[layer_name] += feats

            processed = self.process_features(input_fids)
            for layer_name, feats in processed.items():
                all_features[layer_name] += feats

        self.add_features_to_layers(all_features)


class SurfaceImporter(SpatialImporter):
    """Importer for Surface and SurfaceMap features."""

    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        surface_layer=None,
        surface_map_layer=None,
        pipe_layer=None,
        node_layer=None,
        selected_pipes_only=False,
    ):
        super().__init__(
            external_source=external_source,
            target_gpkg=target_gpkg,
            import_settings=import_settings,
            target_model_cls=dm.Surface,
            target_layer=surface_layer,
        )
        self.surface_map_layer = (
            gpkg_layer(self.target_gpkg, dm.SurfaceMap.__tablename__)
            if surface_map_layer is None
            else surface_map_layer
        )
        pipe_layer = (
            gpkg_layer(self.target_gpkg, dm.Pipe.__tablename__)
            if pipe_layer is None
            else pipe_layer
        )
        node_layer = (
            gpkg_layer(self.target_gpkg, dm.ConnectionNode.__tablename__)
            if node_layer is None
            else node_layer
        )
        self.processor = SurfaceProcessor(
            target_layer=self.target_layer,
            surface_map_layer=self.surface_map_layer,
            import_settings=import_settings,
            pipe_layer=pipe_layer,
            node_layer=node_layer,
            selected_pipes_only=selected_pipes_only,
        )

    @property
    def modifiable_layers(self):
        return [self.target_layer, self.surface_map_layer]
