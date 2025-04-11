# Copyright (C) 2025 by Lutra Consulting
from collections import defaultdict
from functools import cached_property, partial
from types import MappingProxyType

from qgis.core import NULL, QgsExpression, QgsFeature, QgsFeatureRequest, QgsGeometry
from qgis.PyQt.QtCore import QTimer

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.enumerators import (
    BoundaryType1D,
    BoundaryType2D,
    CrestType,
    CrossSectionShape,
    GeometryType,
    Later2DType,
    MeasureVariable,
    PumpType,
    TimeUnit,
    Unit,
    Visualisation,
)
from threedi_schematisation_editor.utils import (
    connect_signal,
    count_vertices,
    disconnect_signal,
    find_linestring_nodes,
    find_point_nodes,
    find_point_polygons,
    find_point_polyline,
    get_next_feature_id,
)
from threedi_schematisation_editor.validators import CrossSectionTableValidator


class UserLayerHandler:
    """Base handler class for 3Di User Layer that adds extra logic to the standard QGIS layer actions."""

    MODEL = dm.ModelObject
    RELATED_MODELS = MappingProxyType({})  # model_cls: number of model instances
    DEFAULTS = MappingProxyType({})
    FORM_CUSTOMIZATIONS = MappingProxyType({})
    VALIDATORS = tuple()

    def __init__(self, layer_manager, layer):
        self.layer_manager = layer_manager
        self.form_factory = self.layer_manager.form_factory
        self.layer = layer
        self.layer_dt = layer.dataProvider()
        self.layer_modified = False
        self.fields_to_nullify = {}

    def connect_handler_signals(self):
        """Connecting layer signals."""
        self.layer.editingStarted.connect(self.on_editing_started)
        self.layer.beforeRollBack.connect(self.on_rollback)
        self.layer.beforeCommitChanges.connect(self.on_commit_changes)
        self.layer.featureAdded.connect(self.on_added_feature)
        self.layer.featuresDeleted.connect(self.on_delete_features)
        if self.MODEL in self.layer_manager.VALUE_RELATIONS:
            self.layer.styleChanged.connect(self.trigger_setup_value_relation_widgets)
        self.connect_additional_signals()

    def disconnect_handler_signals(self):
        """Disconnecting layer signals."""
        self.layer.editingStarted.disconnect(self.on_editing_started)
        self.layer.beforeRollBack.disconnect(self.on_rollback)
        self.layer.beforeCommitChanges.disconnect(self.on_commit_changes)
        self.layer.featureAdded.disconnect(self.on_added_feature)
        self.layer.featuresDeleted.disconnect(self.on_delete_features)
        if self.MODEL in self.layer_manager.VALUE_RELATIONS:
            self.layer.styleChanged.disconnect(self.trigger_setup_value_relation_widgets)
        self.disconnect_additional_signals()

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        pass

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        pass

    @cached_property
    def field_indexes(self):
        """Return field name to its index map"""
        field_names = [field.name() for field in self.layer.fields()]
        field_index_map = {field_name: self.layer.fields().lookupField(field_name) for field_name in field_names}
        return field_index_map

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
            layer_handler.disconnect_handler_signals()
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
            layer_handler.connect_handler_signals()

    def fix_validation_error(self, validation_error):
        """Fix validation error using automatic fixes."""
        if not self.layer.isEditable():
            self.layer.startEditing()
        for fix in validation_error.fixes:
            field_idx = self.field_indexes[fix.field_name]
            self.layer.changeAttributeValue(validation_error.feature_id, field_idx, fix.fixed_value)

    def validate_features(self, autofix=True):
        """Validate features (and fix on the fly if required)."""
        fixed_validation_errors, unsorted_validation_errors = [], []
        for feat in self.layer.getFeatures():
            for validator_cls in self.VALIDATORS:
                validator = validator_cls(self, feat, autofix=autofix)
                for validation_method in validator.validation_methods:
                    validation_method()
                    for validation_error in validator.validation_errors:
                        if validation_error.fixes:
                            self.fix_validation_error(validation_error)
                            fixed_validation_errors.append(validation_error)
                        else:
                            unsorted_validation_errors.append(validation_error)
                    validator.clear()
        if autofix and self.layer.isModified():
            self.layer.commitChanges()
        return fixed_validation_errors, unsorted_validation_errors

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

    def on_added_feature(self, feature_id):
        """Action on feature added signal."""
        if self.fields_to_nullify and not self.layer.isEditable():
            self.layer.startEditing()
        for field_idx, changes in self.fields_to_nullify.items():
            self.layer.changeAttributeValues(feature_id, changes)
        self.fields_to_nullify.clear()

    def detect_dependent_features(self, fid, model_cls, visited_features):
        """Recursively detect all dependent features of the model element with given FID."""
        dependent_features = set()
        feature_unique_key = (model_cls, fid)
        if model_cls not in dm.MODEL_DEPENDENCIES or feature_unique_key in visited_features:
            return dependent_features
        visited_features.add(feature_unique_key)
        handler = self.layer_manager.model_handlers[model_cls]
        request = QgsFeatureRequest(fid)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        try:
            feat_real = next(handler.layer_dt.getFeatures(request))
        except StopIteration:  # Feature not committed
            return dependent_features
        feat_table_name = model_cls.__tablename__
        feat_real_id = feat_real["id"]
        for dependent_data_model, dependent_fields in dm.MODEL_DEPENDENCIES[model_cls].items():
            dependent_layer = self.layer_manager.model_handlers[dependent_data_model].layer
            expr_parts = []
            for dependent_feat_id_field in dependent_fields:
                if isinstance(dependent_feat_id_field, tuple):
                    # We have a pair of fields: field with dependent feature ID and field with dependent feature type
                    dependent_feat_id_field, dependent_feat_type_field = dependent_feat_id_field
                    expr_part = f'("{dependent_feat_id_field}" = {feat_real_id} AND "{dependent_feat_type_field}" = \'{feat_table_name}\')'
                else:
                    expr_part = f'"{dependent_feat_id_field}" = {feat_real_id}'
                expr_parts.append(expr_part)
            expr_str = " OR ".join(expr_parts)
            expr = QgsExpression(expr_str)
            for dependent_feat in dependent_layer.getFeatures(QgsFeatureRequest(expr)):
                dependent_fid = dependent_feat.id()
                dependent_feat_key = (dependent_data_model, dependent_fid)
                if dependent_feat_key in visited_features:
                    continue
                dependent_features.add(dependent_feat_key)
        if dependent_features:
            sub_dependent_features = set()
            for dep_model_cls, dep_fid in dependent_features:
                sub_dependent_features |= self.detect_dependent_features(dep_fid, dep_model_cls, visited_features)
            dependent_features |= sub_dependent_features
        dependent_features.add(feature_unique_key)
        return dependent_features

    def on_delete_features(self, feature_ids):
        """Action on delete features signal."""
        if self.MODEL not in dm.MODEL_DEPENDENCIES:
            return
        features_to_delete, visited_features, grouped_features_to_delete = set(), set(), defaultdict(list)
        for deleted_fid in feature_ids:
            features_to_delete |= self.detect_dependent_features(deleted_fid, self.MODEL, visited_features)
        for model_cls, feat_id in features_to_delete:
            grouped_features_to_delete[model_cls].append(feat_id)
        if len(features_to_delete) > len(feature_ids):
            title = "Referenced features"
            msg = (
                f"There are other features referencing to the deleted '{self.MODEL.__layername__}' element(s). "
                "Please decide how do you want to proceed."
            )
            delete_feat, delete_all, cancel = "Delete this feature only", "Delete all referenced features", "Cancel"
            clicked_button = self.layer_manager.uc.custom_ask(None, title, msg, delete_feat, delete_all, cancel)
            if clicked_button == delete_feat:
                pass
            elif clicked_button == delete_all:
                for dependent_model, dependent_feat_ids in grouped_features_to_delete.items():
                    dependent_handler = self.layer_manager.model_handlers[dependent_model]
                    try:
                        dependent_handler.disconnect_handler_signals()
                        dependent_layer = dependent_handler.layer
                        if not dependent_layer.isEditable():
                            dependent_layer.startEditing()
                        dependent_layer.deleteFeatures(dependent_feat_ids)
                    finally:
                        dependent_handler.connect_handler_signals()
                self.layer_manager.iface.mapCanvas().refresh()
            else:
                self.layer.rollBack()

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

    def get_multiple_feats_by_id(self, object_id, id_field="id"):
        """Return layer multiple features with the given id."""
        feats = []
        if object_id not in (None, NULL):
            for feat in self.layer_manager.get_layer_features(self.MODEL, f'"{id_field}" = {object_id}'):
                feats.append(feat)
        return feats

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
            if fields_to_skip is not None and field_name in fields_to_skip:
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
            linestring = geometry.asPolyline()
            start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, node_layer)
            changes = {}
            start_connection_node_id = start_connection_node_feat["id"] if start_connection_node_feat else None
            start_connection_node_id_idx = layer_fields.lookupField("connection_node_id_start")
            changes[start_connection_node_id_idx] = start_connection_node_id
            end_connection_node_id = end_connection_node_feat["id"] if end_connection_node_feat else None
            end_connection_node_id_idx = layer_fields.lookupField("connection_node_id_end")
            changes[end_connection_node_id_idx] = end_connection_node_id
            if self.MODEL == dm.PumpMap:
                pump_layer = self.layer_manager.model_handlers[dm.Pump].layer
                start_pump_feat = find_point_nodes(linestring[0], pump_layer)
                start_pump_id = start_pump_feat["id"] if start_pump_feat else None
                start_pump_id_idx = layer_fields.lookupField("pump_id")
                changes[start_pump_id_idx] = start_pump_id
            self.layer.changeAttributeValues(feat_id, changes)

    def trigger_update_node_references(self, feat_id, geometry):
        """Triggering update of the node references after feature geometry change."""
        update_node_references_method = partial(self.update_node_references, feat_id, geometry)
        QTimer.singleShot(0, update_node_references_method)

    def trigger_setup_value_relation_widgets(self):
        """Triggering update of the value relation widgets after layer style change."""
        setup_value_relation_widgets_method = partial(self.layer_manager.setup_value_relation_widgets, self.MODEL)
        QTimer.singleShot(0, setup_value_relation_widgets_method)


class ConnectionNodeHandler(UserLayerHandler):
    MODEL = dm.ConnectionNode


class BoundaryCondition1DHandler(UserLayerHandler):
    MODEL = dm.BoundaryCondition1D
    DEFAULTS = MappingProxyType(
        {
            "type": BoundaryType1D.WATER_LEVEL.value,
            "time_units": "seconds",
        }
    )
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 1,
        }
    )


class Lateral1DHandler(UserLayerHandler):
    MODEL = dm.Lateral1D
    DEFAULTS = MappingProxyType(
        {
            "offset": 0,
            "units": Unit.M3_SECONDS.value,
            "time_units": TimeUnit.SECONDS.value,
        }
    )
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 1,
        }
    )


class PumpHandler(UserLayerHandler):
    MODEL = dm.Pump
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 1,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "sewerage": False,
            "type": PumpType.SUCTION_SIDE.value,
            "capacity": None,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.adjust_visualisation)
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.adjust_visualisation)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

    def adjust_visualisation(self, feat_id):
        """Adjusting underlying connection node  type."""
        if feat_id < 0:  # This logic should be triggered just once after adding feature, but before committing changes.
            feat = self.layer.getFeature(feat_id)
            point = feat.geometry().asPoint()
            connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
            connection_node_layer = connection_node_handler.layer
            connection_node_feat = find_point_nodes(point, connection_node_layer)
            if connection_node_feat is not None:
                connection_node_fid = connection_node_feat.id()
                if not connection_node_layer.isEditable():
                    connection_node_layer.startEditing()
                visualisation_idx = connection_node_layer.fields().lookupField("visualisation")
                connection_node_layer.changeAttributeValue(
                    connection_node_fid, visualisation_idx, Visualisation.PUMP_CHAMBER.value
                )

    def get_pump_feats_for_node_id(self, node_id):
        """Check if there is a pump features defined for node of the given node_id and return it."""
        pump_feats = []
        if node_id not in (None, NULL):
            exp = f'"connection_node_id" = {node_id}'
            pump_feats = list(self.layer_manager.get_layer_features(dm.Pump, exp))
        return pump_feats

    def create_pump_with_connection_node(self, geometry, template_feat=None):
        """Creating pump with connection node at same location."""
        connection_node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        if template_feat is not None:
            template_connection_node_id = template_feat["connection_node_id"]
            node_template = connection_node_handler.layer.getFeature(template_connection_node_id)
            node_feat = connection_node_handler.create_new_feature_from_template(node_template, geometry=geometry)
            pump_feat = self.create_new_feature_from_template(template_feat, geometry=geometry)
        else:
            node_feat = connection_node_handler.create_new_feature(geometry=geometry)
            pump_feat = self.create_new_feature(geometry=geometry)
        pump_feat["connection_node_id"] = node_feat["id"]
        return pump_feat, node_feat


class PumpMapHandler(UserLayerHandler):
    MODEL = dm.PumpMap
    RELATED_MODELS = MappingProxyType(
        {
            dm.Pump: 1,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_pump_map)
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_pump_map)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

    def trigger_simplify_pump_map(self, pump_map_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, pump_map_id)
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
            "crest_type": CrestType.SHORT_CRESTED.value,
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
            "sewerage": False,
            "cross_section_shape": CrossSectionShape.OPEN_RECTANGLE,
        }
    )

    VALIDATORS = (CrossSectionTableValidator,)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_weir)
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_weir)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

    def trigger_simplify_weir(self, weir_feat_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, weir_feat_id)
        QTimer.singleShot(0, simplify_method)


class CulvertHandler(UserLayerHandler):
    MODEL = dm.Culvert
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
        }
    )

    DEFAULTS = MappingProxyType(
        {
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
        }
    )

    VALIDATORS = (CrossSectionTableValidator,)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)


class OrificeHandler(UserLayerHandler):
    MODEL = dm.Orifice
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
        }
    )

    DEFAULTS = MappingProxyType(
        {
            "crest_type": CrestType.SHORT_CRESTED.value,
            "sewerage": False,
            "discharge_coefficient_positive": 0.8,
            "discharge_coefficient_negative": 0.8,
        }
    )

    VALIDATORS = (CrossSectionTableValidator,)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_orifice)
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_orifice)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

    def trigger_simplify_orifice(self, orifice_feat_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, orifice_feat_id)
        QTimer.singleShot(0, simplify_method)


class PipeHandler(UserLayerHandler):
    MODEL = dm.Pipe
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
        }
    )
    DEFAULTS = MappingProxyType(
        {
            "cross_section_shape": CrossSectionShape.CIRCLE.value,
        }
    )
    VALIDATORS = (CrossSectionTableValidator,)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_segmentize_pipe)
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_segmentize_pipe)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

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
        pipe_feat = self.layer.getFeature(pipe_feat_id)
        pipe_geom = pipe_feat.geometry()
        vertices_count = count_vertices(pipe_geom)
        if vertices_count < 3:
            return
        start_vertex_idx, end_vertex_idx = 0, vertices_count - 1
        points_connection_nodes = {}
        intermediate_bottom_levels = {}
        pipe_polyline = pipe_geom.asPolyline()
        connection_node_template = None
        for idx, point in enumerate(pipe_polyline):
            if idx == start_vertex_idx:
                connection_node_id = pipe_feat["connection_node_id_start"]
                points_connection_nodes[point] = connection_node_id
                connection_node_template = connection_node_handler.get_feat_by_id(connection_node_id)
            elif idx == end_vertex_idx:
                connection_node_id = pipe_feat["connection_node_id_end"]
                points_connection_nodes[point] = connection_node_id
                intermediate_bottom_levels[point] = pipe_feat["invert_level_end"]
            else:
                geom = QgsGeometry.fromPointXY(point)
                existing_node_feat = find_point_nodes(point, connection_node_layer)
                if existing_node_feat is not None:
                    new_node_feat = existing_node_feat
                    points_connection_nodes[point] = new_node_feat["id"]
                    intermediate_bottom_levels[point] = existing_node_feat["bottom_level"]
                else:
                    new_node_feat = connection_node_handler.create_new_feature_from_template(
                        connection_node_template, geom
                    )
                    points_connection_nodes[point] = new_node_feat["id"]
                    intermediate_bottom_levels[point] = new_node_feat["bottom_level"]
                    connection_node_handler.layer.addFeature(new_node_feat)
        # Split pipe into segments
        segments = zip(pipe_polyline, pipe_polyline[1:])
        # Extract first segment and update source pipe
        first_seg_start_point, first_seg_end_point = next(segments)
        new_source_pipe_geom = QgsGeometry.fromPolylineXY([first_seg_start_point, first_seg_end_point])
        pipe_feat.setGeometry(new_source_pipe_geom)
        pipe_feat["connection_node_id_end"] = points_connection_nodes[first_seg_end_point]
        if first_seg_end_point in intermediate_bottom_levels:
            pipe_feat["invert_level_end"] = intermediate_bottom_levels[first_seg_end_point]
        self.layer.updateFeature(pipe_feat)
        # Let's add a new pipes
        skip_fields = ["connection_node_id_start", "connection_node_id_end"]
        for start_point, end_point in segments:
            new_geom = QgsGeometry.fromPolylineXY([start_point, end_point])
            new_feat = self.create_new_feature_from_template(pipe_feat, geometry=new_geom, fields_to_skip=skip_fields)
            new_feat["connection_node_id_start"] = points_connection_nodes[start_point]
            new_feat["connection_node_id_end"] = points_connection_nodes[end_point]
            if start_point in intermediate_bottom_levels:
                new_feat["invert_level_start"] = intermediate_bottom_levels[start_point]
            if end_point in intermediate_bottom_levels:
                new_feat["invert_level_end"] = intermediate_bottom_levels[end_point]
            self.layer.addFeature(new_feat)


class CrossSectionLocationHandler(UserLayerHandler):
    MODEL = dm.CrossSectionLocation
    RELATED_MODELS = MappingProxyType(
        {
            dm.Channel: 1,
        }
    )
    VALIDATORS = (CrossSectionTableValidator,)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.trigger_update_channel_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.trigger_update_channel_references)

    def trigger_update_channel_references(self, feat_id, geometry):
        """Triggering update of the channel references after feature geometry change."""
        update_channel_references_method = partial(self.update_channel_references, feat_id, geometry)
        QTimer.singleShot(0, update_channel_references_method)

    def update_channel_references(self, feat_id, geometry):
        """Update references to the channel after geometry change."""
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        channel_layer = channel_handler.layer
        layer_fields = self.layer.fields()
        point = geometry.asPoint()
        channel_feat = find_point_polyline(point, channel_layer)
        channel_id = channel_feat["id"] if channel_feat else None
        channel_id_idx = layer_fields.lookupField("channel_id")
        changes = {channel_id_idx: channel_id}
        self.layer.changeAttributeValues(feat_id, changes)


class ChannelHandler(UserLayerHandler):
    MODEL = dm.Channel
    RELATED_MODELS = MappingProxyType(
        {
            dm.ConnectionNode: 2,
            dm.CrossSectionLocation: float("inf"),
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_fulfill_geometry_requirements)
        self.layer.geometryChanged.connect(self.trigger_on_channel_geometry_change)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_fulfill_geometry_requirements)
        self.layer.geometryChanged.disconnect(self.trigger_on_channel_geometry_change)

    def trigger_fulfill_geometry_requirements(self, channel_fid):
        """Triggering geometry modifications on newly added feature."""
        modify_geometry_method = partial(self.fulfill_geometry_requirements, channel_fid)
        QTimer.singleShot(0, modify_geometry_method)

    def trigger_on_channel_geometry_change(self, channel_fid, new_geometry):
        """Triggering geometry modifications on newly added feature."""
        on_channel_geometry_change_method = partial(self.on_channel_geometry_change, channel_fid, new_geometry)
        QTimer.singleShot(0, on_channel_geometry_change_method)

    def fulfill_geometry_requirements(self, channel_fid):
        """Fulfill geometry requirements for newly added channel."""
        feat = self.layer.getFeature(channel_fid)
        geom = feat.geometry()
        vertices_count = count_vertices(geom)
        linestring = geom.asPolyline()
        if vertices_count < 3:
            middle_point = geom.interpolate(geom.length() / 2.0).asPoint()
            linestring.insert(1, middle_point)
            new_source_geom = QgsGeometry.fromPolylineXY(linestring)
            feat.setGeometry(new_source_geom)
            self.layer.updateFeature(feat)

    def on_channel_geometry_change(self, channel_fid, new_geometry):
        """Update channel node references and dependent features geometry."""
        self.update_node_references(channel_fid, new_geometry)
        feat = self.layer.getFeature(channel_fid)
        channel_id = feat["id"]
        try:
            feat_real = next(self.layer_dt.getFeatures(QgsFeatureRequest(QgsExpression(f'"id" = {channel_id}'))))
        except StopIteration:  # Feature not committed
            return
        old_geometry = feat_real.geometry()
        old_geometry_length, new_geometry_length = old_geometry.length(), new_geometry.length()
        channel_request = QgsFeatureRequest(QgsExpression(f'"channel_id" = {channel_id}'))
        # Adjust cross-section locations
        cross_section_location_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
        cross_section_location_layer = cross_section_location_handler.layer
        channel_cross_section_locations = list(cross_section_location_handler.layer_dt.getFeatures(channel_request))
        for xs_feat in channel_cross_section_locations:
            xs_fid = xs_feat.id()
            xs_geometry = xs_feat.geometry()
            xs_fractional_milage = old_geometry.lineLocatePoint(xs_geometry) / old_geometry_length
            if xs_fractional_milage < 0:
                continue
            new_xs_position = new_geometry.interpolate(xs_fractional_milage * new_geometry_length)
            cross_section_location_layer.changeGeometry(xs_fid, new_xs_position)
        # Adjust potential breaches
        potential_breach_handler = self.layer_manager.model_handlers[dm.PotentialBreach]
        potential_breach_layer = potential_breach_handler.layer
        channel_potential_breaches = list(potential_breach_handler.layer_dt.getFeatures(channel_request))
        for breach_feat in channel_potential_breaches:
            breach_fid = breach_feat.id()
            breach_geometry = breach_feat.geometry()
            breach_start_point, breach_end_point = breach_geometry.asPolyline()
            breach_point_geom = QgsGeometry.fromPointXY(breach_start_point)
            if not old_geometry.intersects(breach_point_geom.buffer(0.0000001, 5)):
                continue
            breach_fractional_milage = old_geometry.lineLocatePoint(breach_point_geom) / old_geometry_length
            if breach_fractional_milage < 0:
                continue
            new_breach_adjacent_position = new_geometry.interpolate(breach_fractional_milage * new_geometry_length)
            breach_start_point = new_breach_adjacent_position.asPoint()
            new_breach_geometry = QgsGeometry.fromPolylineXY([breach_start_point, breach_end_point])
            potential_breach_layer.changeGeometry(breach_fid, new_breach_geometry)


class MaterialHandler(UserLayerHandler):
    MODEL = dm.Material


class BoundaryCondition2DHandler(UserLayerHandler):
    MODEL = dm.BoundaryCondition2D
    DEFAULTS = MappingProxyType(
        {
            "type": BoundaryType2D.WATER_LEVEL.value,
            "time_units": TimeUnit.SECONDS.value,
        }
    )


class Lateral2DHandler(UserLayerHandler):
    MODEL = dm.Lateral2D
    DEFAULTS = MappingProxyType(
        {
            "offset": 0,
            "type": Later2DType.SURFACE.value,
            "units": Unit.M3_SECONDS.value,
            "time_units": TimeUnit.SECONDS.value,
        }
    )


class ObstacleHandler(UserLayerHandler):
    MODEL = dm.Obstacle
    DEFAULTS = MappingProxyType({"affects_2d": True, "affects_1d2d_open_water": True, "affects_1d2d_closed": False})


class GridRefinementLineHandler(UserLayerHandler):
    MODEL = dm.GridRefinementLine


class GridRefinementAreaHandler(UserLayerHandler):
    MODEL = dm.GridRefinementArea


class DEMAverageAreaHandler(UserLayerHandler):
    MODEL = dm.DEMAverageArea


class Windshielding1DHandler(UserLayerHandler):
    MODEL = dm.Windshielding1D


class PotentialBreachHandler(UserLayerHandler):
    MODEL = dm.PotentialBreach
    RELATED_MODELS = MappingProxyType(
        {
            dm.Channel: 1,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_potential_breach)
        self.layer.geometryChanged.connect(self.trigger_update_channel_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_potential_breach)
        self.layer.geometryChanged.disconnect(self.trigger_update_channel_references)

    def trigger_simplify_potential_breach(self, potential_breach_feat_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, potential_breach_feat_id)
        QTimer.singleShot(0, simplify_method)

    def trigger_update_channel_references(self, feat_id, geometry):
        """Triggering update of the channel references after feature geometry change."""
        update_channel_references_method = partial(self.update_channel_references, feat_id, geometry)
        QTimer.singleShot(0, update_channel_references_method)

    def update_channel_references(self, feat_id, geometry):
        """Update references to the channel after geometry change."""
        channel_handler = self.layer_manager.model_handlers[dm.Channel]
        channel_layer = channel_handler.layer
        layer_fields = self.layer.fields()
        polyline = geometry.asPolyline()
        point = polyline[0]
        channel_feat = find_point_polyline(point, channel_layer)
        channel_id = channel_feat["id"] if channel_feat else None
        channel_id_idx = layer_fields.lookupField("channel_id")
        changes = {channel_id_idx: channel_id}
        self.layer.changeAttributeValues(feat_id, changes)


class ExchangeLineHandler(UserLayerHandler):
    MODEL = dm.ExchangeLine


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


class SurfaceMapHandler(UserLayerHandler):
    MODEL = dm.SurfaceMap
    DEFAULTS = MappingProxyType(
        {
            "percentage": 100.00,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.trigger_update_link_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.trigger_update_link_references)

    def trigger_update_link_references(self, feat_id, geometry):
        """Triggering update of the references to the connections nodes and surfaces after geometry change."""
        update_link_references_method = partial(self.update_link_references, feat_id, geometry)
        QTimer.singleShot(0, update_link_references_method)

    def update_link_references(self, feat_id, geometry):
        """Update references to the connections nodes and surfaces after geometry change."""
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        surface_handler = self.layer_manager.model_handlers[dm.Surface]
        node_layer = node_handler.layer
        surface_layer = surface_handler.layer
        layer_fields = self.layer.fields()
        linestring = geometry.asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_surface_feat = find_point_polygons(start_point, surface_layer)
        end_connection_node_feat = find_point_nodes(end_point, node_layer)
        changes = {}
        start_surface_id = start_surface_feat["id"] if start_surface_feat else None
        end_connection_node_id = end_connection_node_feat["id"] if end_connection_node_feat else None
        start_surface_id_idx = layer_fields.lookupField("surface_id")
        end_connection_node_id_idx = layer_fields.lookupField("connection_node_id")
        changes[start_surface_id_idx] = start_surface_id
        changes[end_connection_node_id_idx] = end_connection_node_id
        self.layer.changeAttributeValues(feat_id, changes)


class SurfaceParameterHandler(UserLayerHandler):
    MODEL = dm.SurfaceParameters


class DryWeatherFlowHandler(UserLayerHandler):
    MODEL = dm.DryWeatherFlow
    DEFAULTS = MappingProxyType(
        {
            "multiplier": 1,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.update_dwf_link)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.update_dwf_link)

    def update_dwf_link(self, feat_id, geometry):
        """Update geometry of the DWF area - node link."""
        dwf_handler = self.layer_manager.model_handlers[dm.DryWeatherFlow]
        dwf_layer = dwf_handler.layer
        dwf_link_handler = self.layer_manager.model_handlers[dm.DryWeatherFlowMap]
        dwf_link_layer = dwf_link_handler.layer
        dwf_feat = dwf_layer.getFeature(feat_id)
        link_feat = dwf_link_handler.get_feat_by_id(dwf_feat["id"], "dry_weather_flow_id")
        point = geometry.centroid().asPoint()
        link_linestring = link_feat.geometry().asPolyline()
        link_linestring[0] = point
        link_new_geom = QgsGeometry.fromPolylineXY(link_linestring)
        dwf_link_layer.changeGeometry(link_feat.id(), link_new_geom)


class DryWeatherFlowMapHandler(UserLayerHandler):
    MODEL = dm.DryWeatherFlowMap
    DEFAULTS = MappingProxyType(
        {
            "percentage": 100.00,
        }
    )

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.connect(self.trigger_update_link_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.geometryChanged.disconnect(self.trigger_update_link_references)

    def trigger_update_link_references(self, feat_id, geometry):
        """Triggering update of the references to the connections nodes and surfaces after geometry change."""
        update_link_references_method = partial(self.update_link_references, feat_id, geometry)
        QTimer.singleShot(0, update_link_references_method)

    def update_link_references(self, feat_id, geometry):
        """Update references to the connections nodes and surfaces after geometry change."""
        node_handler = self.layer_manager.model_handlers[dm.ConnectionNode]
        surface_handler = self.layer_manager.model_handlers[dm.DryWeatherFlow]
        node_layer = node_handler.layer
        surface_layer = surface_handler.layer
        layer_fields = self.layer.fields()
        linestring = geometry.asPolyline()
        start_point, end_point = linestring[0], linestring[-1]
        start_surface_feat = find_point_polygons(start_point, surface_layer)
        end_connection_node_feat = find_point_nodes(end_point, node_layer)
        changes = {}
        start_surface_id = start_surface_feat["id"] if start_surface_feat else None
        end_connection_node_id = end_connection_node_feat["id"] if end_connection_node_feat else None
        start_surface_id_idx = layer_fields.lookupField("dry_weather_flow_id")
        end_connection_node_id_idx = layer_fields.lookupField("connection_node_id")
        changes[start_surface_id_idx] = start_surface_id
        changes[end_connection_node_id_idx] = end_connection_node_id
        self.layer.changeAttributeValues(feat_id, changes)


class DryWeatherFlowDistributionHandler(UserLayerHandler):
    MODEL = dm.DryWeatherFlowDistribution


class ModelSettingsHandler(UserLayerHandler):
    MODEL = dm.ModelSettings


class AggregationSettingsHandler(UserLayerHandler):
    MODEL = dm.AggregationSettings


class SimpleInfiltrationSettingsHandler(UserLayerHandler):
    MODEL = dm.SimpleInfiltrationSettings


class GroundWaterSettingsHandler(UserLayerHandler):
    MODEL = dm.GroundWaterSettings


class InterflowSettingsHandler(UserLayerHandler):
    MODEL = dm.InterflowSettings


class InterceptionSettingsHandler(UserLayerHandler):
    MODEL = dm.InterceptionSettings


class InitialConditionsSettingsHandler(UserLayerHandler):
    MODEL = dm.InitialConditionsSettings


class PhysicalSettingsHandler(UserLayerHandler):
    MODEL = dm.PhysicalSettings


class NumericalSettingsHandler(UserLayerHandler):
    MODEL = dm.NumericalSettings


class SimulationTemplateSettingsHandler(UserLayerHandler):
    MODEL = dm.SimulationTemplateSettings


class TimeStepSettingsHandler(UserLayerHandler):
    MODEL = dm.TimeStepSettings


class VegetationDrag2DHandler(UserLayerHandler):
    MODEL = dm.VegetationDrag2D


class TagHandler(UserLayerHandler):
    MODEL = dm.Tag


class AbstractControlHandler(UserLayerHandler):
    @cached_property
    def target_data_models(self):
        return {model_cls.__tablename__: model_cls for model_cls in [dm.Pump, dm.Orifice, dm.Weir]}

    def snap_to_target_centroid(self, feat_id):
        """Move geometry to target centroid (if target is linear)."""
        feat = self.layer.getFeature(feat_id)
        target_feat_id = feat["target_id"]
        if not target_feat_id:
            return
        target_type = feat["target_type"]
        if not target_type:
            return
        try:
            target_model_cls = self.target_data_models[target_type]
        except KeyError:
            return
        if target_model_cls.__geometrytype__ != GeometryType.Linestring:
            return
        target_handler = self.layer_manager.model_handlers[target_model_cls]
        target_layer = target_handler.layer
        target_feat = target_layer.getFeature(target_feat_id)
        target_feat_centroid = target_feat.geometry().centroid()
        new_source_geom = QgsGeometry(target_feat_centroid)
        feat.setGeometry(new_source_geom)
        self.layer.updateFeature(feat)

    def update_target_references(self, feat_id, geometry):
        """Update references to the target after geometry change."""
        feature_point = geometry.asPoint()
        target_feature, target_type = None, None
        layer_fields = self.layer.fields()
        for model_cls in self.target_data_models.values():
            structure_handler = self.layer_manager.model_handlers[model_cls]
            structure_layer = structure_handler.layer
            dm_geometry_type = model_cls.__geometrytype__
            if dm_geometry_type == GeometryType.Point:
                structure_feat = find_point_nodes(feature_point, structure_layer)
            elif dm_geometry_type == GeometryType.Linestring:
                structure_feat = find_point_polyline(feature_point, structure_layer)
            else:
                continue
            if structure_feat is not None:
                target_feature, target_type = structure_feat, model_cls.__tablename__
                break
        target_id = target_feature["id"] if target_feature is not None else None
        target_id_idx = layer_fields.lookupField("target_id")
        target_type_idx = layer_fields.lookupField("target_type")
        changes = {target_id_idx: target_id, target_type_idx: target_type}
        self.layer.changeAttributeValues(feat_id, changes)

    def trigger_snap_to_target_centroid(self, feat_id):
        """Triggering snapping geometry to the target centroid after feature added."""
        snap_to_target_centroid_method = partial(self.snap_to_target_centroid, feat_id)
        QTimer.singleShot(0, snap_to_target_centroid_method)

    def trigger_update_target_references(self, feat_id, geometry):
        """Triggering update of the target references after feature geometry change."""
        update_target_references_method = partial(self.update_target_references, feat_id, geometry)
        QTimer.singleShot(0, update_target_references_method)


class MemoryControlHandler(AbstractControlHandler):
    MODEL = dm.MemoryControl

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_snap_to_target_centroid)
        self.layer.geometryChanged.connect(self.trigger_update_target_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_snap_to_target_centroid)
        self.layer.geometryChanged.disconnect(self.trigger_update_target_references)


class TableControlHandler(AbstractControlHandler):
    MODEL = dm.TableControl

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_snap_to_target_centroid)
        self.layer.geometryChanged.connect(self.trigger_update_target_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_snap_to_target_centroid)
        self.layer.geometryChanged.disconnect(self.trigger_update_target_references)


class MeasureLocationHandler(UserLayerHandler):
    MODEL = dm.MeasureLocation
    DEFAULTS = MappingProxyType({"measure_variable": MeasureVariable.WATER_LEVEL.value})


class MeasureMapHandler(UserLayerHandler):
    MODEL = dm.MeasureMap
    DEFAULTS = MappingProxyType({"measure_variable": MeasureVariable.WATER_LEVEL.value})

    @cached_property
    def control_data_models(self):
        return {model_cls.__tablename__: model_cls for model_cls in [dm.MemoryControl, dm.TableControl]}

    def update_control_references(self, feat_id, geometry):
        """Update references to the control and measure location feature after geometry change."""
        feature_polyline = geometry.asPolyline()
        feature_start_point, feature_end_point = feature_polyline[0], feature_polyline[-1]
        control_feature, control_type = None, None
        layer_fields = self.layer.fields()
        for model_cls in self.control_data_models.values():
            control_handler = self.layer_manager.model_handlers[model_cls]
            control_layer = control_handler.layer
            control_feat = find_point_nodes(feature_end_point, control_layer)
            if control_feat is not None:
                control_feature, control_type = control_feat, model_cls.__tablename__
                break
        control_id = control_feature["id"] if control_feature is not None else None
        control_id_idx = layer_fields.lookupField("control_id")
        control_type_idx = layer_fields.lookupField("control_type")
        changes = {control_id_idx: control_id, control_type_idx: control_type}
        measure_location_handler = self.layer_manager.model_handlers[dm.MeasureLocation]
        measure_location_layer = measure_location_handler.layer
        measure_location_feat = find_point_nodes(feature_start_point, measure_location_layer)
        if measure_location_feat is not None:
            measure_location_id = measure_location_feat["id"] if measure_location_feat is not None else None
            measure_location_id_idx = layer_fields.lookupField("control_measure_location_id")
            changes[measure_location_id_idx] = measure_location_id
        self.layer.changeAttributeValues(feat_id, changes)

    def trigger_update_control_references(self, feat_id, geometry):
        """Triggering update of the control and measure location references after feature geometry change."""
        update_control_references_method = partial(self.update_control_references, feat_id, geometry)
        QTimer.singleShot(0, update_control_references_method)

    def trigger_simplify_measure_map(self, measure_map_id):
        """Triggering geometry simplification on newly added feature."""
        simplify_method = partial(self.simplify_linear_feature, measure_map_id)
        QTimer.singleShot(0, simplify_method)

    def connect_additional_signals(self):
        """Connecting signals to action specific for the particular layers."""
        self.layer.featureAdded.connect(self.trigger_simplify_measure_map)
        self.layer.geometryChanged.connect(self.trigger_update_control_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_measure_map)
        self.layer.geometryChanged.disconnect(self.trigger_update_control_references)


ALL_HANDLERS = (
    ConnectionNodeHandler,
    BoundaryCondition1DHandler,
    Lateral1DHandler,
    PumpHandler,
    PumpMapHandler,
    WeirHandler,
    CulvertHandler,
    OrificeHandler,
    PipeHandler,
    CrossSectionLocationHandler,
    MaterialHandler,
    ChannelHandler,
    BoundaryCondition2DHandler,
    Lateral2DHandler,
    ObstacleHandler,
    GridRefinementLineHandler,
    GridRefinementAreaHandler,
    DEMAverageAreaHandler,
    Windshielding1DHandler,
    PotentialBreachHandler,
    ExchangeLineHandler,
    SurfaceHandler,
    SurfaceMapHandler,
    SurfaceParameterHandler,
    DryWeatherFlowHandler,
    DryWeatherFlowMapHandler,
    DryWeatherFlowDistributionHandler,
    ModelSettingsHandler,
    AggregationSettingsHandler,
    SimpleInfiltrationSettingsHandler,
    GroundWaterSettingsHandler,
    InterflowSettingsHandler,
    InitialConditionsSettingsHandler,
    InterceptionSettingsHandler,
    NumericalSettingsHandler,
    PhysicalSettingsHandler,
    SimulationTemplateSettingsHandler,
    TimeStepSettingsHandler,
    TagHandler,
    VegetationDrag2DHandler,
    MeasureMapHandler,
    MeasureLocationHandler,
    MemoryControlHandler,
    TableControlHandler,
)

MODEL_HANDLERS = MappingProxyType({handler.MODEL: handler for handler in ALL_HANDLERS})
