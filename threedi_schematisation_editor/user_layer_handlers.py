# Copyright (C) 2023 by Lutra Consulting
from collections import defaultdict
from functools import cached_property, partial
from types import MappingProxyType

from qgis.core import NULL, QgsExpression, QgsFeature, QgsFeatureRequest, QgsGeometry
from qgis.PyQt.QtCore import QTimer

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.enumerators import (
    CalculationTypeCulvert,
    CalculationTypeNode,
    CrestType,
    FrictionType,
    GeometryType,
    ManholeIndicator,
    ManholeShape,
    PipeMaterial,
    PumpType,
    ZoomCategories,
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
        self.connect_additional_signals()

    def disconnect_handler_signals(self):
        """Disconnecting layer signals."""
        self.layer.editingStarted.disconnect(self.on_editing_started)
        self.layer.beforeRollBack.disconnect(self.on_rollback)
        self.layer.beforeCommitChanges.disconnect(self.on_commit_changes)
        self.layer.featureAdded.disconnect(self.on_added_feature)
        self.layer.featuresDeleted.disconnect(self.on_delete_features)
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
        feat_real_id = feat_real["id"]
        for dependent_data_model, dependent_fields in dm.MODEL_DEPENDENCIES[model_cls].items():
            dependent_layer = self.layer_manager.model_handlers[dependent_data_model].layer
            expr_str = " OR ".join(f'"{field_name}" = {feat_real_id}' for field_name in dependent_fields)
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
            linestring = geometry.asPolyline()
            start_connection_node_feat, end_connection_node_feat = find_linestring_nodes(linestring, node_layer)
            changes = {}
            start_connection_node_id = start_connection_node_feat["id"] if start_connection_node_feat else None
            start_connection_node_id_idx = layer_fields.lookupField("connection_node_start_id")
            changes[start_connection_node_id_idx] = start_connection_node_id
            end_connection_node_id = end_connection_node_feat["id"] if end_connection_node_feat else None
            end_connection_node_id_idx = layer_fields.lookupField("connection_node_end_id")
            changes[end_connection_node_id_idx] = end_connection_node_id
            if self.MODEL == dm.PumpstationMap:
                pumpstation_layer = self.layer_manager.model_handlers[dm.Pumpstation].layer
                start_pump_feat = find_point_nodes(linestring[0], pumpstation_layer)
                start_pump_id = start_pump_feat["id"] if start_pump_feat else None
                start_pump_id_idx = layer_fields.lookupField("pumpstation_id")
                changes[start_pump_id_idx] = start_pump_id
            self.layer.changeAttributeValues(feat_id, changes)

    def trigger_update_node_references(self, feat_id, geometry):
        """Triggering update of the node references after feature geometry change."""
        update_node_references_method = partial(self.update_node_references, feat_id, geometry)
        QTimer.singleShot(0, update_node_references_method)


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
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.adjust_manhole_indicator)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

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
        self.layer.geometryChanged.connect(self.trigger_update_node_references)

    def disconnect_additional_signals(self):
        """Disconnecting signals to action specific for the particular layers."""
        self.layer.featureAdded.disconnect(self.trigger_simplify_pumpstation_map)
        self.layer.geometryChanged.disconnect(self.trigger_update_node_references)

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
                intermediate_bottom_levels[point] = pipe_feat["invert_level_end_point"]
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
    RELATED_MODELS = MappingProxyType(
        {
            dm.Channel: 1,
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
    DEFAULTS = MappingProxyType(
        {
            "zoom_category": ZoomCategories.LOWEST_VISIBILITY.value,
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


class PotentialBreachHandler(UserLayerHandler):
    MODEL = dm.PotentialBreach
    RELATED_MODELS = MappingProxyType(
        {
            dm.Channel: 1,
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

    DEFAULTS = MappingProxyType(
        {
            "display_name": "new",
            "code": "new",
        }
    )


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
        surface_handler = self.layer_manager.model_handlers[dm.ImperviousSurface]
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
        start_surface_id_idx = layer_fields.lookupField("impervious_surface_id")
        end_connection_node_id_idx = layer_fields.lookupField("connection_node_id")
        changes[start_surface_id_idx] = start_surface_id
        changes[end_connection_node_id_idx] = end_connection_node_id
        self.layer.changeAttributeValues(feat_id, changes)


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


class SchemaVersionHandler(UserLayerHandler):
    MODEL = dm.SchemaVersion


class VegetationDragHandler(UserLayerHandler):
    MODEL = dm.VegetationDrag


class ControlHandler(UserLayerHandler):
    MODEL = dm.Control


class ControlDeltaHandler(UserLayerHandler):
    MODEL = dm.ControlDelta


class ControlGroupHandler(UserLayerHandler):
    MODEL = dm.ControlGroup


class ControlMeasureGroupHandler(UserLayerHandler):
    MODEL = dm.ControlMeasureGroup


class ControlMeasureMapHandler(UserLayerHandler):
    MODEL = dm.ControlMeasureMap


class ControlMemoryHandler(UserLayerHandler):
    MODEL = dm.ControlMemory


class ControlPIDHandler(UserLayerHandler):
    MODEL = dm.ControlPID


class ControlTableHandler(UserLayerHandler):
    MODEL = dm.ControlTable


class ControlTimedHandler(UserLayerHandler):
    MODEL = dm.ControlTimed


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
    PotentialBreachHandler,
    ExchangeLineHandler,
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
    SchemaVersionHandler,
    VegetationDragHandler,
    ControlHandler,
    ControlDeltaHandler,
    ControlGroupHandler,
    ControlMeasureGroupHandler,
    ControlMeasureMapHandler,
    ControlMemoryHandler,
    ControlPIDHandler,
    ControlTableHandler,
    ControlTimedHandler,
)

MODEL_HANDLERS = MappingProxyType({handler.MODEL: handler for handler in ALL_HANDLERS})
