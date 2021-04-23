# Copyright (C) 2021 by Lutra Consulting
from types import MappingProxyType
import threedi_model_builder.data_models as dm


class UserLayerHandler:
    MODEL = dm.ModelObject

    def __init__(self, layer, user_communication):
        self.layer = layer
        self.uc = user_communication

    def connect_handler_signals(self):
        self.layer.committedFeaturesAdded.connect(self._on_added_features)
        self.layer.committedFeaturesRemoved.connect(self._on_removed_features)
        self.layer.committedGeometriesChanges.connect(self._on_changed_geometries)
        self.layer.committedAttributeValuesChanges.connect(self._on_changed_attributes)

    def disconnect_handler_signals(self):
        self.layer.committedFeaturesAdded.disconnect(self._on_added_features)
        self.layer.committedFeaturesRemoved.disconnect(self._on_removed_features)
        self.layer.committedGeometriesChanges.disconnect(self._on_changed_geometries)
        self.layer.committedAttributeValuesChanges.disconnect(self._on_changed_attributes)

    def _on_added_features(self, layer_id, added_features):
        raise Exception("Have to be reimplemented")

    def _on_removed_features(self, layer_id, feature_ids):
        raise Exception("Have to be reimplemented")

    def _on_changed_geometries(self, layer_id, changed_geometry_map):
        raise Exception("Have to be reimplemented")

    def _on_changed_attributes(self, layer_id, changed_attribute_map):
        raise Exception("Have to be reimplemented")


class ConnectionNodeHandler(UserLayerHandler):
    MODEL = dm.ConnectionNode


class BoundaryCondition1DHandler(UserLayerHandler):
    MODEL = dm.BoundaryCondition1D


class Lateral1DHandler(UserLayerHandler):
    MODEL = dm.Lateral1D


class ManholeHandler(UserLayerHandler):
    MODEL = dm.Manhole


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
