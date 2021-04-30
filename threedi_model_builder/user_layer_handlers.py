# Copyright (C) 2021 by Lutra Consulting
import threedi_model_builder.data_models as dm
from threedi_model_builder.enumerators import CalculationTypeNode, CrossSectionShape, FrictionType, PipeMaterial
from threedi_model_builder.utils import connect_signal, disconnect_signal
from types import MappingProxyType
from qgis.core import (
    NULL,
    QgsFeature,
    QgsProject,
    QgsSnappingConfig,
    QgsTolerance,
    QgsGeometry,
)


class UserLayerHandler:
    MODEL = dm.ModelObject
    RELATED_MODELS = MappingProxyType({})  # model_cls: number of model instances
    DEFAULTS = MappingProxyType({})

    def __init__(self, layer_manager, layer):
        self.layer_manager = layer_manager
        self.form_factory = self.layer_manager.form_factory
        self.layer = layer
        self.snapped_models = tuple()
        self.linked_table_models = tuple()

    def connect_handler_signals(self):
        self.layer.editingStarted.connect(self.on_editing_started)
        self.layer.beforeRollBack.connect(self.on_rollback)
        self.layer.beforeCommitChanges.connect(self.on_commit_changes)

    def disconnect_handler_signals(self):
        self.layer.editingStarted.disconnect(self.on_editing_started)
        self.layer.beforeRollBack.connect(self.on_rollback)
        self.layer.beforeCommitChanges.connect(self.on_commit_changes)

    @property
    def snapped_handlers(self):
        snapped_handlers = [self.layer_manager.model_handlers[model_cls] for model_cls in self.snapped_models]
        return snapped_handlers

    @property
    def linked_table_handlers(self):
        table_handlers = [self.layer_manager.model_handlers[model_cls] for model_cls in self.linked_table_models]
        return table_handlers

    def set_layer_snapping(self, enable=True):
        if not self.snapped_models:
            return
        project = QgsProject.instance()
        project.setTopologicalEditing(True)
        snap_config = project.snappingConfig()
        snap_config.setMode(QgsSnappingConfig.AdvancedConfiguration)
        snap_config.setIntersectionSnapping(True)
        individual_configs = snap_config.individualLayerSettings()
        snapped_layers = [handler.layer for handler in self.snapped_handlers] + [self.layer]
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.editingStarted, layer_handler.on_editing_started)
            layer.startEditing()
            for link_table_handler in layer_handler.linked_table_handlers:
                link_table_handler.layer.startEditing()
        for layer in snapped_layers:
            iconf = individual_configs[layer]
            iconf.setTolerance(10)
            iconf.setTypeFlag(QgsSnappingConfig.VertexFlag)
            iconf.setUnits(QgsTolerance.Pixels)
            iconf.setEnabled(enable)
            snap_config.setIndividualLayerSettings(layer, iconf)
        if snap_config.enabled() is False:
            snap_config.setEnabled(True)
        project.setSnappingConfig(snap_config)
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            connect_signal(layer.editingStarted, layer_handler.on_editing_started)

    @staticmethod
    def reset_snapping():
        project = QgsProject.instance()
        project.setTopologicalEditing(True)
        snap_config = project.snappingConfig()
        snap_config.setMode(QgsSnappingConfig.AllLayers)
        snap_config.setIntersectionSnapping(True)
        if snap_config.enabled() is False:
            snap_config.setEnabled(True)
        project.setSnappingConfig(snap_config)

    def validate_feature(self):
        raise Exception("Not implemented")

    def on_editing_started(self):
        for link_table_handler in self.linked_table_handlers:
            link_table_handler.layer.startEditing()
        self.set_layer_snapping(enable=True)

    def on_rollback(self):
        self.reset_snapping()
        for link_table_handler in self.linked_table_handlers:
            link_table_handler.layer.rollBack()
        if not self.snapped_models:
            return
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.beforeRollBack, layer_handler.on_rollback)
            layer.rollBack()
            for link_table_handler in layer_handler.linked_table_handlers:
                link_table_handler.layer.rollBack()
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            connect_signal(layer.beforeRollBack, layer_handler.on_rollback)

    def on_commit_changes(self):
        self.reset_snapping()
        for link_table_handler in self.linked_table_handlers:
            link_table_handler.layer.commitChanges(stopEditing=False)
        if not self.snapped_models:
            return
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)
            layer.commitChanges(stopEditing=False)
            for link_table_handler in layer_handler.linked_table_handlers:
                link_table_handler.layer.commitChanges(stopEditing=False)
        for layer_handler in self.snapped_handlers:
            layer = layer_handler.layer
            connect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)

    def on_add_feature(self, fid):
        raise Exception("Not implemented")

    def on_added_features(self, layer_id, added_features):
        raise Exception("Not implemented")

    def on_removed_features(self, layer_id, feature_ids):
        raise Exception("Not implemented")

    def on_changed_geometries(self, layer_id, changed_geometry_map):
        raise Exception("Not implemented")

    def on_changed_attributes(self, layer_id, changed_attribute_map):
        raise Exception("Not implemented")

    def get_feat_by_id(self, object_id):
        """Return layer feature with the given id."""
        feat = None
        if object_id not in (None, NULL):
            feats = self.layer_manager.get_layer_features(self.MODEL, f'"id" = {object_id}')
            try:
                feat = next(feats)
            except StopIteration:
                pass
        return feat

    def get_next_id(self, layer=None):
        if layer is None:
            layer = self.layer
        id_idx = layer.fields().indexFromName("id")
        # Ensure the id attribute is unique
        try:
            next_id = max(layer.uniqueValues(id_idx)) + 1
        except ValueError:
            # this is the first feature
            next_id = 1
        return next_id

    def set_feature_values(self, feat, set_id=True, **custom_values):
        values_to_set = dict(self.DEFAULTS)
        values_to_set.update(custom_values)
        fields = self.layer.fields()
        for field in fields:
            field_name = field.name()
            if field_name in values_to_set:
                feat[field_name] = values_to_set[field_name]
        if set_id:
            next_id = self.get_next_id()
            feat["id"] = next_id

    def create_new_feature(self, geometry=None, use_defaults=True):
        """Create a new feature for the handler layer with the geometry, if given. Return the id of the feature."""
        fields = self.layer.fields()
        feat = QgsFeature(fields)
        if use_defaults:
            self.set_feature_values(feat)
        if geometry is not None:
            feat.setGeometry(geometry)
        return feat

    def create_new_feature_from_template(self, template_feat, geometry=None, fields_to_skip=None):
        """
        Take all attributes from the template feature and create a new feature with the given geometry.
        Do not copy fields values listed in fields_to_skip.
        """
        field_values = dict()
        for field in template_feat.fields():
            field_name = field.name()
            if fields_to_skip is not None and field_name in fields_to_skip:
                continue
            field_values[field_name] = template_feat[field_name]
        new_feat = self.create_new_feature(geometry=geometry, use_defaults=False)
        self.set_feature_values(new_feat, **field_values)
        return new_feat


class ConnectionNodeHandler(UserLayerHandler):
    MODEL = dm.ConnectionNode

    def __init__(self, *args):
        super().__init__(*args)
        self.snapped_models = (dm.Manhole, dm.Pipe)

    def get_manhole_feat_for_node_id(self, node_id):
        """Check if there is a manhole feature defined for node of the given node_id and return it."""
        manhole_feat = None
        if node_id not in (None, NULL):
            manhole_feats = self.layer_manager.get_layer_features(dm.Manhole, f'"connection_node_id" = {node_id}')
            try:
                manhole_feat = next(manhole_feats)
            except StopIteration:
                pass
        return manhole_feat


class BoundaryCondition1DHandler(UserLayerHandler):
    MODEL = dm.BoundaryCondition1D


class Lateral1DHandler(UserLayerHandler):
    MODEL = dm.Lateral1D


class ManholeHandler(UserLayerHandler):
    MODEL = dm.Manhole
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 1,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "length": 0.8,
            "width": 0.8,
            "shape": CrossSectionShape.CIRCLE.value,
            "manhole_indicator": 1,
        }
    )

    def __init__(self, *args):
        super().__init__(*args)
        self.snapped_models = (dm.ConnectionNode, dm.Pipe)

    def create_manhole_with_connection_node(self, geometry):
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_feat = connection_node_handler.create_new_feature(geometry=geometry)
        manhole_feat = self.create_new_feature(geometry=geometry)
        manhole_feat["connection_node_id"] = connection_node_feat["id"]
        return manhole_feat, connection_node_feat


class PumpstationHandler(UserLayerHandler):
    MODEL = dm.Pumpstation


class PumpstationMapHandler(UserLayerHandler):
    MODEL = dm.PumpstationMap


class WeirHandler(UserLayerHandler):
    MODEL = dm.Weir


class CulvertHandler(UserLayerHandler):
    MODEL = dm.Culvert


class OrificeHandler(UserLayerHandler):
    MODEL = dm.Orifice


class PipeHandler(UserLayerHandler):
    MODEL = dm.Pipe
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
            dm.Manhole: 2,
            dm.CrossSectionDefinition: 1,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "dist_calc_points": 1000,
            "friction_type": FrictionType.MANNING.value,
            "calculation_type": CalculationTypeNode.ISOLATED.value,
            "material": PipeMaterial.CONCRETE.value,
            "friction_value": dm.TABLE_MANNING[PipeMaterial.CONCRETE]
        }
    )

    def __init__(self, *args):
        super().__init__(*args)
        self.snapped_models = (dm.ConnectionNode, dm.Manhole)
        self.linked_table_models = (dm.CrossSectionDefinition,)

    def create_endpoints_for_pipe(self, pipe_feat):
        manhole_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        cs_definition_handler = self.layer_manager.model_handlers[dm.CrossSectionDefinition]
        pipe_linestring = pipe_feat.geometry().asPolyline()
        start_point, end_point = pipe_linestring[0], pipe_linestring[-1]
        start_geom = QgsGeometry.fromPointXY(start_point)
        end_geom = QgsGeometry.fromPointXY(end_point)
        start_manhole, start_node = manhole_handler.create_manhole_with_connection_node(start_geom)
        end_manhole, end_node = manhole_handler.create_manhole_with_connection_node(end_geom)
        cross_section_def = cs_definition_handler.create_new_feature()
        pipe_feat["connection_node_start_id"] = start_node["id"]
        pipe_feat["connection_node_end_id"] = end_node["id"]
        return start_node, start_manhole, end_node, end_manhole, cross_section_def


class CrossSectionLocationHandler(UserLayerHandler):
    MODEL = dm.CrossSectionLocation


class ChannelHandler(UserLayerHandler):
    MODEL = dm.Channel


class CrossSectionDefinitionHandler(UserLayerHandler):
    MODEL = dm.CrossSectionDefinition


class BoundaryCondition2DHandler(UserLayerHandler):
    MODEL = dm.BoundaryCondition2D


class Lateral2DHandler(UserLayerHandler):
    MODEL = dm.Lateral2D


class LinearObstacleHandler(UserLayerHandler):
    MODEL = dm.LinearObstacle


class GridRefinementHandler(UserLayerHandler):
    MODEL = dm.GridRefinement


class GridRefinementAreaHandler(UserLayerHandler):
    MODEL = dm.GridRefinementArea


class DEMAverageAreaHandler(UserLayerHandler):
    MODEL = dm.DEMAverageArea


class WindshieldingHandler(UserLayerHandler):
    MODEL = dm.Windshielding


class ImperviousSurfaceHandler(UserLayerHandler):
    MODEL = dm.ImperviousSurface


class SurfaceHandler(UserLayerHandler):
    MODEL = dm.Surface


class ImperviousSurfaceMapHandler(UserLayerHandler):
    MODEL = dm.ImperviousSurfaceMap


class SurfaceMapHandler(UserLayerHandler):
    MODEL = dm.SurfaceMap


class SurfaceParameterHandler(UserLayerHandler):
    MODEL = dm.SurfaceParameter


class GlobalSettingsHandler(UserLayerHandler):
    MODEL = dm.GlobalSettings


class AggregationSettingsHandler(UserLayerHandler):
    MODEL = dm.AggregationSettings


class SimpleInfiltrationSettingsHandler(UserLayerHandler):
    MODEL = dm.SimpleInfiltrationSettings


class GroundWaterSettingsHandler(UserLayerHandler):
    MODEL = dm.GroundWaterSettings


class InterflowSettingsHandler(UserLayerHandler):
    MODEL = dm.InterflowSettings


class NumericalSettingsHandler(UserLayerHandler):
    MODEL = dm.NumericalSettings


ALL_HANDLERS = (
    ConnectionNodeHandler,
    BoundaryCondition1DHandler,
    Lateral1DHandler,
    ManholeHandler,
    PumpstationHandler,
    PumpstationMapHandler,
    WeirHandler,
    CulvertHandler,
    OrificeHandler,
    PipeHandler,
    CrossSectionLocationHandler,
    ChannelHandler,
    CrossSectionDefinitionHandler,
    BoundaryCondition2DHandler,
    Lateral2DHandler,
    LinearObstacleHandler,
    GridRefinementHandler,
    GridRefinementAreaHandler,
    DEMAverageAreaHandler,
    WindshieldingHandler,
    ImperviousSurfaceHandler,
    SurfaceHandler,
    ImperviousSurfaceMapHandler,
    SurfaceMapHandler,
    SurfaceParameterHandler,
    GlobalSettingsHandler,
    AggregationSettingsHandler,
    SimpleInfiltrationSettingsHandler,
    GroundWaterSettingsHandler,
    InterflowSettingsHandler,
    NumericalSettingsHandler,
)

MODEL_HANDLERS = MappingProxyType({handler.MODEL: handler for handler in ALL_HANDLERS})
