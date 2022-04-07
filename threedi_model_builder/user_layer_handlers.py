# Copyright (C) 2022 by Lutra Consulting
import threedi_model_builder.data_models as dm
from threedi_model_builder.enumerators import (
    CalculationTypeCulvert,
    CalculationTypeNode,
    CrestType,
    GeometryType,
    ManholeIndicator,
    ManholeShape,
    FrictionType,
    PipeMaterial,
    PumpType,
)
from types import MappingProxyType
from functools import partial
from threedi_model_builder.utils import (
    connect_signal,
    disconnect_signal,
    count_vertices,
    find_point_nodes,
    find_linestring_nodes,
    get_next_feature_id,
)
from qgis.core import QgsFeature, QgsGeometry, NULL
from qgis.PyQt.QtCore import QTimer


class UserLayerHandler:
    """Base handler class for 3Di User Layer that adds extra logic to the standard QGIS layer actions."""

    MODEL = dm.ModelObject
    RELATED_MODELS = MappingProxyType({})  # model_cls: number of model instances
    DEFAULTS = MappingProxyType({})

    def __init__(self, layer_manager, layer):
        self.layer_manager = layer_manager
        self.form_factory = self.layer_manager.form_factory
        self.layer = layer
        self.layer_modified = False

    def connect_handler_signals(self):
        """Connecting layer signals."""
        self.layer.editingStarted.connect(self.on_editing_started)
        self.layer.beforeRollBack.connect(self.on_rollback)
        self.layer.beforeCommitChanges.connect(self.on_commit_changes)
        self.connect_additional_signals()

    def disconnect_handler_signals(self):
        """Disconnecting layer signals."""
        self.layer.editingStarted.disconnect(self.on_editing_started)
        self.layer.beforeRollBack.disconnect(self.on_rollback)
        self.layer.beforeCommitChanges.disconnect(self.on_commit_changes)
        self.disconnect_additional_signals()

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        pass

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        pass

    @property
    def other_linked_handlers(self):
        """Getting other handlers within 1D group."""
        other_handlers = [
            self.layer_manager.model_handlers[model_cls]
            for model_cls in self.layer_manager.common_editing_group
            if model_cls != self.MODEL
        ]
        return other_handlers

    @property
    def other_linked_layers(self):
        """Getting other layers within 1D group."""
        other_layers = [handler.layer for handler in self.other_linked_handlers]
        return other_layers

    def multi_start_editing(self):
        """Start editing for all layers with 1D group."""
        if self.MODEL not in self.layer_manager.common_editing_group:
            return
        other_1d_handlers = self.other_linked_handlers
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.editingStarted, layer_handler.on_editing_started)
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            if not layer.isEditable():
                layer.startEditing()
        for layer_handler in self.other_linked_handlers:
            layer = layer_handler.layer
            connect_signal(layer.editingStarted, layer_handler.on_editing_started)

    def multi_rollback(self):
        """Rollback changes for all layers with 1D group."""
        if self.MODEL not in self.layer_manager.common_editing_group:
            return
        other_1d_handlers = self.other_linked_handlers
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.beforeRollBack, layer_handler.on_rollback)
            disconnect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            if layer.isEditable():
                if layer.isModified():
                    title = "Stop Editing"
                    question = f"Do you want to save changes to layer {layer.name()}?"
                    answer = self.layer_manager.uc.ask(None, title, question)
                    if answer is True:
                        layer.commitChanges(stopEditing=True)
                        continue
                layer.rollBack()
        for layer_handler in self.other_linked_handlers:
            layer = layer_handler.layer
            connect_signal(layer.beforeRollBack, layer_handler.on_rollback)
            connect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)

    def multi_commit_changes(self):
        """Commit changes for all layers with 1D group."""
        self.layer_modified = True
        if self.MODEL not in self.layer_manager.common_editing_group:
            return
        other_1d_handlers = self.other_linked_handlers
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            disconnect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)
        for layer_handler in other_1d_handlers:
            layer = layer_handler.layer
            if layer.isEditable():
                layer.commitChanges(stopEditing=True)
        for layer_handler in self.other_linked_handlers:
            layer = layer_handler.layer
            connect_signal(layer.beforeCommitChanges, layer_handler.on_commit_changes)

    def on_editing_started(self):
        """Action on editing started signal."""
        self.multi_start_editing()

    def on_rollback(self):
        """Action on rollback signal."""
        self.multi_rollback()

    def on_commit_changes(self):
        """Action on commit changes signal."""
        self.multi_commit_changes()

    def get_feat_by_id(self, object_id, id_field="id"):
        """Return layer feature with the given id."""
        feat = None
        if object_id not in (None, NULL):
            feats = self.layer_manager.get_layer_features(self.MODEL, f'"{id_field}" = {object_id}')
            try:
                feat = next(feats)
            except StopIteration:
                pass
        return feat

    def get_next_id(self, layer=None):
        """Return first available ID within layer features."""
        if layer is None:
            layer = self.layer
        next_id = get_next_feature_id(layer)
        return next_id

    def set_feature_values(self, feat, set_id=True, **custom_values):
        """Setting values for feature."""
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
            if field_name == "fid" or (fields_to_skip is not None and field_name in fields_to_skip):
                continue
            field_values[field_name] = template_feat[field_name]
        new_feat = self.create_new_feature(geometry=geometry, use_defaults=False)
        self.set_feature_values(new_feat, **field_values)
        return new_feat

    def simplify_linear_feature(self, feat_id):
        """Simplifying feature geometry to the 2 vertices form."""
        if self.MODEL.__geometrytype__ != GeometryType.Linestring:
            return
        feat = self.layer.getFeature(feat_id)
        geom = feat.geometry()
        vertices_count = count_vertices(geom)
        if vertices_count < 3:
            return
        start_vertex_idx, end_vertex_idx = 0, vertices_count - 1
        start_point, end_point = geom.vertexAt(start_vertex_idx), geom.vertexAt(end_vertex_idx)
        new_source_geom = QgsGeometry.fromPolyline([start_point, end_point])
        feat.setGeometry(new_source_geom)
        self.layer.updateFeature(feat)

    def update_node_references(self, feat_id, geometry):
        """Update references to the connections nodes after geometry change."""
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        node_layer = node_handler.layer
        model_geometry_type = self.MODEL.__geometrytype__
        layer_fields = self.layer.fields()
        if model_geometry_type == GeometryType.Point:
            point = geometry.asPoint()
            connection_node_feat = find_point_nodes(point, node_layer)
            connection_node_id = connection_node_feat["id"] if connection_node_feat else None
            connection_node_id_idx = layer_fields.lookupField("connection_node_id")
            changes = {connection_node_id_idx: connection_node_id}
            self.layer.changeAttributeValues(feat_id, changes)
        elif model_geometry_type == GeometryType.Linestring:
            is_surface_link = self.MODEL in {dm.ImperviousSurfaceMap, dm.SurfaceMap}
            linestring = geometry.asPolyline()
            start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, node_layer)
            changes = {}
            if not is_surface_link:
                start_connection_node_id = start_connection_node_feat["id"] if start_connection_node_feat else None
                start_connection_node_id_idx = layer_fields.lookupField("connection_node_start_id")
                changes[start_connection_node_id_idx] = start_connection_node_id
            end_connection_node_id = end_connection_node_feat["id"] if end_connection_node_feat else None
            end_connection_node_id_idx = layer_fields.lookupField(
                "connection_node_end_id" if not is_surface_link else "connection_node_id"
            )
            changes[end_connection_node_id_idx] = end_connection_node_id
            if self.MODEL == dm.PumpstationMap:
                pumpstation_layer = self.layer_manager.model_handlers[dm.Pumpstation].layer
                start_pump_feat = find_point_nodes(linestring[0], pumpstation_layer)
                start_pump_id = start_pump_feat["id"] if start_pump_feat else None
                start_pump_id_idx = layer_fields.lookupField("pumpstation_id")
                changes[start_pump_id_idx] = start_pump_id
            self.layer.changeAttributeValues(feat_id, changes)


class ConnectionNodeHandler(UserLayerHandler):
    MODEL = dm.ConnectionNode
    DEFAULTS = MappingProxyType(
        {
            "code": "new",
        }
    )

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
            "display_name": "new",
            "code": "new",
            "length": 0.8,
            "width": 0.8,
            "shape": ManholeShape.ROUND.value,
            "manhole_indicator": ManholeIndicator.INSPECTION.value,
            "calculation_type": CalculationTypeNode.ISOLATED.value,
            "bottom_level": -10.0,
        }
    )

    def create_manhole_with_connection_node(self, geometry, template_feat=None):
        """Creating manhole with connection node at same location."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        if template_feat is not None:
            template_connection_node_id = template_feat["connection_node_id"]
            node_template = connection_node_handler.layer.getFeature(template_connection_node_id)
            node_feat = connection_node_handler.create_new_feature_from_template(node_template, geometry=geometry)
            manhole_feat = self.create_new_feature_from_template(template_feat, geometry=geometry)
        else:
            node_feat = connection_node_handler.create_new_feature(geometry=geometry)
            manhole_feat = self.create_new_feature(geometry=geometry)
        manhole_feat["connection_node_id"] = node_feat["id"]
        return manhole_feat, node_feat


class PumpstationHandler(UserLayerHandler):
    MODEL = dm.Pumpstation
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 1,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
            "sewerage": False,
            "type": PumpType.SUCTION_SIDE.value,
            "capacity": None,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.adjust_manhole_indicator)
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.adjust_manhole_indicator)
        self.layer.geometryChanged.disconnect(self.update_node_references)

    def adjust_manhole_indicator(self, feat_id):
        """Adjusting underlying manhole attributes."""
        if feat_id < 0:  # This logic should be triggered just once after adding feature, but before committing changes.
            feat = self.layer.getFeature(feat_id)
            point = feat.geometry().asPoint()
            manhole_handler = self.layer_manager.model_handlers[dm.Manhole]
            manhole_layer = manhole_handler.layer
            manhole_feat = find_point_nodes(point, manhole_layer)
            if manhole_feat is not None:
                manhole_fid = manhole_feat.id()
                if not manhole_layer.isEditable():
                    manhole_layer.startEditing()
                manhole_indicator_idx = manhole_layer.fields().lookupField("manhole_indicator")
                manhole_layer.changeAttributeValue(manhole_fid, manhole_indicator_idx, ManholeIndicator.PUMP.value)

    def get_pumpstation_feats_for_node_id(self, node_id):
        """Check if there is a pumpstation features defined for node of the given node_id and return it."""
        pump_feats = []
        if node_id not in (None, NULL):
            exp = f'"connection_node_id" = {node_id}'
            pump_feats = list(self.layer_manager.get_layer_features(dm.Pumpstation, exp))
        return pump_feats

    def create_pump_with_connection_node(self, geometry, template_feat=None):
        """Creating pumpstation with connection node at same location."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        if template_feat is not None:
            template_connection_node_id = template_feat["connection_node_id"]
            node_template = connection_node_handler.layer.getFeature(template_connection_node_id)
            node_feat = connection_node_handler.create_new_feature_from_template(node_template, geometry=geometry)
            pumpstation_feat = self.create_new_feature_from_template(template_feat, geometry=geometry)
        else:
            node_feat = connection_node_handler.create_new_feature(geometry=geometry)
            pumpstation_feat = self.create_new_feature(geometry=geometry)
        pumpstation_feat["connection_node_id"] = node_feat["id"]
        return pumpstation_feat, node_feat


class PumpstationMapHandler(UserLayerHandler):
    MODEL = dm.PumpstationMap
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
            dm.Pumpstation: 1,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_pumpstation_map)
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_pumpstation_map)
        self.layer.geometryChanged.disconnect(self.update_node_references)

    def trigger_simplify_pumpstation_map(self, pumpstation_map_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, pumpstation_map_id)
        QTimer.singleShot(0, simplify_method)


class WeirHandler(UserLayerHandler):
    MODEL = dm.Weir
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
        }
    )

    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
            "crest_level": 1.0,
            "crest_type": CrestType.SHORT_CRESTED.value,
            "friction_type": FrictionType.MANNING.value,
            "friction_value": 0.02,
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
            "sewerage": False,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_weir)
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_weir)
        self.layer.geometryChanged.disconnect(self.update_node_references)

    def trigger_simplify_weir(self, weir_feat_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, weir_feat_id)
        QTimer.singleShot(0, simplify_method)


class CulvertHandler(UserLayerHandler):
    MODEL = dm.Culvert
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
            dm.CrossSectionDefinition: 1,
        }
    )

    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
            "dist_calc_points": 1000,
            "calculation_type": CalculationTypeCulvert.ISOLATED.value,
            "friction_type": FrictionType.MANNING.value,
            "friction_value": 0.02,
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
            "invert_level_start_point": -10.0,
            "invert_level_end_point": -10.0,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_node_references)


class OrificeHandler(UserLayerHandler):
    MODEL = dm.Orifice
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
        }
    )

    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
            "crest_level": 1.0,
            "crest_type": CrestType.SHORT_CRESTED.value,
            "friction_type": FrictionType.MANNING.value,
            "friction_value": 0.02,
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
            "sewerage": False,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_orifice)
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_orifice)
        self.layer.geometryChanged.disconnect(self.update_node_references)

    def trigger_simplify_orifice(self, orifice_feat_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, orifice_feat_id)
        QTimer.singleShot(0, simplify_method)


class PipeHandler(UserLayerHandler):
    MODEL = dm.Pipe
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
            dm.Manhole: 2,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
            "dist_calc_points": 1000,
            "friction_type": FrictionType.MANNING.value,
            "calculation_type": CalculationTypeNode.ISOLATED.value,
            "material": PipeMaterial.CONCRETE.value,
            "friction_value": dm.TABLE_MANNING[PipeMaterial.CONCRETE],
            "invert_level_start_point": -10.0,
            "invert_level_end_point": -10.0,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_segmentize_pipe)
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_segmentize_pipe)
        self.layer.geometryChanged.disconnect(self.update_node_references)

    def trigger_segmentize_pipe(self, pipe_feat_id):
        """
        We have to run pipe segmentation after QGIS will finish adding feature procedure.
        Pipe segmentation will be triggered in the next event loop after adding new pipe.
        Editing added pipe directly by the slot connected to the `featureAdded` signal breaks adding feature tool.
        That leads to the QGIS crash.
        """
        segmentize_method = partial(self.segmentize_pipe, pipe_feat_id)
        QTimer.singleShot(0, segmentize_method)

    def segmentize_pipe(self, pipe_feat_id):
        """Method to split single pipe into 2 vertices segments."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        connection_node_layer = connection_node_handler.layer
        manhole_handler = self.layer_manager.model_handlers[dm.Manhole]
        manhole_layer = manhole_handler.layer
        pipe_feat = self.layer.getFeature(pipe_feat_id)
        pipe_geom = pipe_feat.geometry()
        vertices_count = count_vertices(pipe_geom)
        if vertices_count < 3:
            return
        start_vertex_idx, end_vertex_idx = 0, vertices_count - 1
        points_connection_nodes = {}
        intermediate_bottom_levels = {}
        pipe_polyline = pipe_geom.asPolyline()
        manhole_template = None
        for idx, point in enumerate(pipe_polyline):
            if idx == start_vertex_idx:
                connection_node_id = pipe_feat["connection_node_start_id"]
                points_connection_nodes[point] = connection_node_id
                manhole_template = connection_node_handler.get_manhole_feat_for_node_id(connection_node_id)
            elif idx == end_vertex_idx:
                connection_node_id = pipe_feat["connection_node_end_id"]
                points_connection_nodes[point] = connection_node_id
            else:
                geom = QgsGeometry.fromPointXY(point)
                existing_node_feat = find_point_nodes(point, connection_node_layer)
                if existing_node_feat is not None:
                    new_node_feat = existing_node_feat
                    existing_manhole_feat = find_point_nodes(point, manhole_layer)
                    if existing_manhole_feat is None:
                        new_manhole_feat = manhole_handler.create_new_feature(geom)
                        new_manhole_feat["connection_node_id"] = new_node_feat["id"]
                    else:
                        new_manhole_feat = existing_manhole_feat
                        intermediate_bottom_levels[point] = new_manhole_feat["bottom_level"]
                    points_connection_nodes[point] = new_node_feat["id"]
                else:
                    extra_feats = manhole_handler.create_manhole_with_connection_node(
                        geom, template_feat=manhole_template
                    )
                    new_manhole_feat, new_node_feat = extra_feats
                    points_connection_nodes[point] = new_node_feat["id"]
                    intermediate_bottom_levels[point] = new_manhole_feat["bottom_level"]
                    connection_node_handler.layer.addFeature(new_node_feat)
                    manhole_handler.layer.addFeature(new_manhole_feat)
        # Split pipe into segments
        segments = zip(pipe_polyline, pipe_polyline[1:])
        # Extract first segment and update source pipe
        first_seg_start_point, first_seg_end_point = next(segments)
        new_source_pipe_geom = QgsGeometry.fromPolylineXY([first_seg_start_point, first_seg_end_point])
        pipe_feat.setGeometry(new_source_pipe_geom)
        pipe_feat["connection_node_end_id"] = points_connection_nodes[first_seg_end_point]
        if first_seg_start_point in intermediate_bottom_levels:
            pipe_feat["invert_level_start_point"] = intermediate_bottom_levels[first_seg_start_point]
        if first_seg_end_point in intermediate_bottom_levels:
            pipe_feat["invert_level_end_point"] = intermediate_bottom_levels[first_seg_end_point]
        self.layer.updateFeature(pipe_feat)
        # Let's add a new pipes
        skip_fields = ["connection_node_start_id", "connection_node_end_id"]
        for start_point, end_point in segments:
            new_geom = QgsGeometry.fromPolylineXY([start_point, end_point])
            new_feat = self.create_new_feature_from_template(pipe_feat, geometry=new_geom, fields_to_skip=skip_fields)
            new_feat["connection_node_start_id"] = points_connection_nodes[start_point]
            new_feat["connection_node_end_id"] = points_connection_nodes[end_point]
            if start_point in intermediate_bottom_levels:
                new_feat["invert_level_start_point"] = intermediate_bottom_levels[start_point]
            if end_point in intermediate_bottom_levels:
                new_feat["invert_level_end_point"] = intermediate_bottom_levels[end_point]
            self.layer.addFeature(new_feat)


class CrossSectionLocationHandler(UserLayerHandler):
    MODEL = dm.CrossSectionLocation


class ChannelHandler(UserLayerHandler):
    MODEL = dm.Channel


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

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_surface_link)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_surface_link)

    def update_surface_link(self, feat_id, geometry):
        """Update geometry of the surface - node link."""
        surface_handler = self.layer_manager.model_handlers[dm.ImperviousSurface]
        surface_layer = surface_handler.layer
        surface_link_handler = self.layer_manager.model_handlers[dm.ImperviousSurfaceMap]
        surface_link_layer = surface_link_handler.layer
        surface_feat = surface_layer.getFeature(feat_id)
        link_feat = surface_link_handler.get_feat_by_id(surface_feat["id"], "impervious_surface_id")
        point = geometry.centroid().asPoint()
        link_linestring = link_feat.geometry().asPolyline()
        link_linestring[0] = point
        link_new_geom = QgsGeometry.fromPolylineXY(link_linestring)
        surface_link_layer.changeGeometry(link_feat.id(), link_new_geom)


class SurfaceHandler(UserLayerHandler):
    MODEL = dm.Surface

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_surface_link)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_surface_link)

    def update_surface_link(self, feat_id, geometry):
        """Update geometry of the surface - node link."""
        surface_handler = self.layer_manager.model_handlers[dm.Surface]
        surface_layer = surface_handler.layer
        surface_link_handler = self.layer_manager.model_handlers[dm.SurfaceMap]
        surface_link_layer = surface_link_handler.layer
        surface_feat = surface_layer.getFeature(feat_id)
        link_feat = surface_link_handler.get_feat_by_id(surface_feat["id"], "surface_id")
        point = geometry.centroid().asPoint()
        link_linestring = link_feat.geometry().asPolyline()
        link_linestring[0] = point
        link_new_geom = QgsGeometry.fromPolylineXY(link_linestring)
        surface_link_layer.changeGeometry(link_feat.id(), link_new_geom)


class ImperviousSurfaceMapHandler(UserLayerHandler):
    MODEL = dm.ImperviousSurfaceMap
    DEFAULTS = MappingProxyType(
        {
            "percentage": 100.00,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_node_references)


class SurfaceMapHandler(UserLayerHandler):
    MODEL = dm.SurfaceMap
    DEFAULTS = MappingProxyType(
        {
            "percentage": 100.00,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_node_references)


class SurfaceParameterHandler(UserLayerHandler):
    MODEL = dm.SurfaceParameters


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
