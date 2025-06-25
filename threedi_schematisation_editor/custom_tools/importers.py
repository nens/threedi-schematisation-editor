import warnings
from _operator import attrgetter, itemgetter
from collections import namedtuple, defaultdict
from functools import cached_property
from abc import ABC

from qgis.core import (
    NULL,
    QgsCoordinateTransform,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsGeometry,
    QgsPointLocator,
    QgsProject,
    QgsWkbTypes,
)

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor.custom_tools.import_config import ColumnImportMethod
from threedi_schematisation_editor.utils import gpkg_layer, convert_to_type, TypeConversionError, find_connection_node, \
    get_next_feature_id, spatial_index, get_features_by_expression
from threedi_schematisation_editor.warnings import FeaturesImporterWarning, StructuresIntegratorWarning

DEFAULT_INTERSECTION_BUFFER = 1
DEFAULT_INTERSECTION_BUFFER_SEGMENTS = 5

def update_attributes(fields_config, model_cls, source_feat, *new_features):
    expression_context = QgsExpressionContext()
    expression_context.setFeature(source_feat)
    type_annotations = model_cls.__annotations__
    for new_feat in new_features:
        for field_name, field_type in type_annotations.items():
            try:
                field_config = fields_config[field_name]
            except KeyError:
                continue
            method = ColumnImportMethod(field_config["method"])
            if method == ColumnImportMethod.AUTO:
                continue
            field_value = NULL
            if method == ColumnImportMethod.ATTRIBUTE:
                src_field_name = field_config[ColumnImportMethod.ATTRIBUTE.value]
                src_value = source_feat[src_field_name]
                value_map = field_config.get("value_map", {})
                # Prevent type mismatches in keys by casting keys to strings to match those the dict in src_value['value_map'] which is also forced to be strings
                field_value = value_map.get(str(src_value), src_value)
                if field_value == NULL:
                    field_value = field_config.get("default_value", NULL)
            elif method == ColumnImportMethod.EXPRESSION:
                expression_str = field_config["expression"]
                expression = QgsExpression(expression_str)
                field_value = expression.evaluate(expression_context)
            elif method == ColumnImportMethod.DEFAULT:
                field_value = field_config["default_value"]
            try:
                new_feat[field_name] = convert_to_type(field_value, field_type)
            except TypeConversionError as e:
                new_feat[field_name] = NULL
                feat_id = new_feat["id"]
                message = f"Attribute {field_name} of feature with id {feat_id} was not filled in"
                warnings.warn(f"{message}. {e}", FeaturesImporterWarning)


def create_new_point_geometry(src_feat):
    # TODO: add test
    """Create a new point feature geometry based on the source feature."""
    src_geometry = QgsGeometry(src_feat.geometry())
    if src_geometry.isMultipart():
        src_geometry.convertToSingleType()
    src_point = src_geometry.asPoint()
    dst_point = src_point
    dst_geometry = QgsGeometry.fromPointXY(dst_point)
    return dst_geometry



def get_substring_geometry(curve, start_distance, end_distance, simplify=False):
    curve_substring = curve.curveSubstring(start_distance, end_distance)
    substring_geometry = QgsGeometry(curve_substring)
    if simplify:
        substring_polyline = substring_geometry.asPolyline()
        substring_geometry = QgsGeometry.fromPolylineXY([substring_polyline[0], substring_polyline[-1]])
    return substring_geometry

def snap_connection_node(feat, point, snapping_distance, locator, connection_id_name):
    node = find_connection_node(point, locator, snapping_distance)
    if node:
        feat.setGeometry(QgsGeometry.fromPointXY(node.geometry().asPoint()))
        feat[connection_id_name] = node["id"]
        return True
    else:
        return False

def add_connection_node(feat, geom, node_manager, connection_id_name, node_fields):
    new_node_feat = node_manager.create_new(QgsGeometry.fromPointXY(geom), node_fields)
    feat[connection_id_name] = new_node_feat["id"]
    return new_node_feat


class FeatureManager:
    def __init__(self, next_id=1):
        self.next_id = next_id

    def create_new(self, geom, fields, attributes=None):
        new_feat = QgsFeature(fields)
        new_feat.setGeometry(geom)
        if attributes:
            for field_name, field_value in attributes.items():
                new_feat[field_name] = field_value
        new_feat["id"] = self.next_id
        self.next_id += 1
        return new_feat


class ConversionSettings:
    def __init__(self, conversion_config):
        self.integrate = conversion_config.get("edit_channels", False)
        self.use_snapping = conversion_config.get("use_snapping", False)
        if self.use_snapping:
            self.snapping_distance = conversion_config.get("snapping_distance")
        else:
            self.snapping_distance = DEFAULT_INTERSECTION_BUFFER
        self.create_connection_nodes = conversion_config.get("create_connection_nodes", False)
        self.length_source_field = conversion_config.get("length_source_field", None)
        self.length_fallback_value = conversion_config.get("length_fallback_value", 10.0)
        self.azimuth_source_field = conversion_config.get("azimuth_source_field", None)
        self.azimuth_fallback_value = conversion_config.get("azimuth_fallback_value", 90.0)
        self.edit_channels = conversion_config.get("edit_channels", False)


class Importer(ABC):
    """Base class for the importing features from the external data source."""
    def __init__(self,
                 external_source,
                 target_gpkg,
                 import_settings,
                 target_model_cls,
                 target_layer=None,
                 node_layer=None,
                 channel_layer=None,
                 cross_section_location_layer=None,
                 ):
        self.external_source = external_source
        self.target_gpkg = target_gpkg
        self.import_settings = import_settings
        self.setup_target_layers(target_model_cls, target_layer, node_layer, channel_layer, cross_section_location_layer)
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

    def setup_target_layers(
        self,
        target_model_cls,
        target_layer=None,
        node_layer=None,
    ):
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
        self.node_manager = FeatureManager(get_next_feature_id(self.node_layer))
        self.target_manager = FeatureManager(get_next_feature_id(self.target_layer))

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

    @staticmethod
    def new_polyline_geometry(src_feat):
        """Create a new polyline feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_polyline = src_geometry.asPolyline()
        dst_polyline = src_polyline
        dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        return dst_geometry

    @staticmethod
    def new_polygon_geometry(src_feat):
        """Create a new polygon feature geometry based on the source feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        src_polygon = src_geometry.asPolygon()
        dst_polygon = src_polygon
        dst_geometry = QgsGeometry.fromPolygonXY(dst_polygon)
        return dst_geometry

    def import_features(self, context=None, selected_ids=None):
        """Method responsible for the importing structures from the external feature source."""
        if selected_ids is None:
            selected_ids = []
        self.processor.transformation = self.get_transformation(context)
        self.processor.locator = self.get_locator(context=context)
        if self.integrator:
            input_feature_ids = [feat.id() for feat in self.external_source.getFeatures() if feat.id() not in selected_ids]
            new_features, integrated_ids = self.integrator.integrate_features(input_feature_ids, selected_ids)
            selected_ids += integrated_ids
        else:
            new_features = defaultdict(list)
        for external_src_feat in self.external_source.getFeatures():
            if external_src_feat.id() in selected_ids:
                continue
            processed_features = self.processor.process_feature(external_src_feat)
            for name, features in processed_features.items():
                new_features[name] += features
        for layer in self.modifiable_layers:
            if layer.name() not in new_features:
                continue
            layer.startEditing()
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
        self.processor = LineProcessor(self.target_layer, self.target_model_cls, self.target_manager, self.node_layer, self.node_manager, self.fields_configurations, self.conversion_settings)
        if self.conversion_settings.integrate:
            self.integrator = LinearIntegrator.from_importer(dm.Channel, channel_layer, cross_section_location_layer, self)


class Processor(ABC):
    def __init__(self, target_layer, target_model_cls, target_manager):
        self.target_fields = target_layer.fields()
        self.target_name = target_layer.name()
        self.target_manager = target_manager
        self.target_model_cls = target_model_cls
        self.transformation = None
        self.locator = None

    def process_feature(self, src_feat):
        raise NotImplementedError


class ConnectionNodeProcessor(Processor):

    def process_feature(self, src_feat):
        """Process source point into connection node feature."""
        new_geom = create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        return {self.target_name : [self.target_manager.create_new(new_geom, self.target_fields)]}


class StructureProcessor(Processor, ABC):
    def __init__(self, target_layer, target_model_cls, target_manager, node_layer, node_manager, fields_configurations, conversion_settings):
        super().__init__(target_layer, target_model_cls, target_manager)
        self.node_fields = node_layer.fields()
        self.node_name = node_layer.name()
        self.node_manager = node_manager
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings

    def add_node(self, new_feat, point, name):
        snapped = False
        if self.conversion_settings.use_snapping:
            snapped = snap_connection_node(new_feat, point, self.conversion_settings.snapping_distance, self.locator,
                                           name)
        if not snapped or self.conversion_settings.create_connection_nodes:
            return add_connection_node(new_feat, point, self.node_manager, name, self.node_fields)


class PointProcessor(StructureProcessor):

    def process_feature(self, src_feat):
        """Process source point structure feature."""
        new_nodes = []
        new_geom = create_new_point_geometry(src_feat)
        if self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        point = new_geom.asPoint()
        new_node = self.add_node(new_feat, point, "connection_node_id")
        if new_node:
            new_nodes.append(new_node)
        update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_feat,
                          *new_nodes)
        update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_feat,
                          new_feat)
        return {self.target_name : [new_feat], self.node_name : new_nodes}


class LineProcessor(StructureProcessor):

    @staticmethod
    def new_geometry(src_feat, conversion_settings):
        """Create new structure geometry based on the source structure feature."""
        src_geometry = QgsGeometry(src_feat.geometry())
        if src_geometry.isMultipart():
            src_geometry.convertToSingleType()
        geometry_type = src_geometry.type()
        if geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
            src_polyline = src_geometry.asPolyline()
            dst_polyline = src_polyline if (self.target_model_cls == dm.Culvert or self.target_model_cls == dm.Pipe) else [src_polyline[0], src_polyline[-1]]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        elif geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
            start_point = src_geometry.asPoint()
            length = (
                src_feat[conversion_settings.length_source_field]
                if conversion_settings.length_source_field
                else conversion_settings.length_fallback_value
            )
            azimuth = (
                src_feat[conversion_settings.azimuth_source_field]
                if conversion_settings.azimuth_source_field
                else conversion_settings.azimuth_fallback_value
            )
            end_point = start_point.project(length, azimuth)
            dst_polyline = [start_point, end_point]
            dst_geometry = QgsGeometry.fromPolylineXY(dst_polyline)
        else:
            raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")
        return dst_geometry

    def process_feature(self, src_feat):
        """Process source linear structure feature."""
        new_nodes = []
        new_geom = self.new_geometry(src_feat, self.conversion_settings)
        if self.transformation:
            new_geom.transform(transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        polyline = new_feat.geometry().asPolyline()
        for (idx, name) in [(0, 'connection_node_id_start'), (1, 'connection_node_id_end')]:
            new_node = self.add_node(new_feat, polyline[idx], name)
            if new_node:
                new_nodes.append(new_node)
        update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_feat,
                          new_feat)
        update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_feat,
                          *new_nodes)
        return {self.target_name : [new_feat], self.node_name : new_nodes}


class LinearIntegrator:
    """ Integrate linear structures onto a channel or similar """
    # shorthand with channel_structure properties
    channel_structure_cls = namedtuple("channel_structure", ["channel_id", "feature", "m", "length"])

    def __init__(self, integrate_model_cls, integrate_layer,
                 target_model_cls, target_layer, target_manager,
                 node_layer, node_manager,
                 fields_configurations, conversion_settings,
                 cross_section_layer, external_source,
                 target_gpkg):
        # TODO: add tests
        self.external_source = external_source
        self.integrate_model_cls = integrate_model_cls
        self.target_model_cls = target_model_cls
        self.fields_configurations = fields_configurations
        self.conversion_settings = conversion_settings
        # set schematisation layer to add - if any are missing retrieve them from the gpkg
        self.integrate_layer = integrate_layer if integrate_layer else gpkg_layer(target_gpkg, self.integrate_model_cls.__tablename__)
        self.target_layer = target_layer if target_layer else gpkg_layer(target_gpkg, self.target_model_cls.__tablename__)
        self.node_layer = node_layer if node_layer else gpkg_layer(target_gpkg, dm.ConnectionNode.__tablename__)
        self.cross_section_layer = cross_section_layer if cross_section_layer else gpkg_layer(target_gpkg, dm.CrossSectionLocation.__tablename__)
        # feature managers that handle id's for added features
        # for target features and nodes a manager can be supplied such that they match the associated importer
        self.target_manager = target_manager if target_manager else FeatureManager(self.target_model_cls)
        self.node_manager = node_manager if node_manager else FeatureManager(dm.ConnectionNode)
        self.integrate_manager = FeatureManager(get_next_feature_id(self.integrate_layer))
        self.cross_section_manager = FeatureManager(get_next_feature_id(self.cross_section_layer))
        # initialize mappings and indices
        self.setup_fields_map()
        self.setup_spatial_indexes()
        self.setup_node_by_location()

    @classmethod
    def from_importer(cls, integrate_model_cls, integrate_layer, cross_section_layer, importer):
        """ extract data from importer to created matching integrator """
        return cls(integrate_model_cls=integrate_model_cls,
                   integrate_layer=integrate_layer,
                   target_model_cls=importer.target_model_cls,
                   target_layer=importer.target_layer,
                   target_manager=importer.target_manager,
                   node_layer=importer.node_layer,
                   node_manager=importer.node_manager,
                   fields_configurations=importer.fields_configurations,
                   conversion_settings=importer.conversion_settings,
                   cross_section_layer=cross_section_layer,
                   external_source=importer.external_source,
                   target_gpkg=importer.target_gpkg)

    def setup_fields_map(self):
        """Setup input layer fields map."""
        self.layer_fields_mapping = {}
        self.layer_field_names_mapping = {}
        for layer in [self.target_layer, self.node_layer, self.integrate_layer, self.cross_section_layer]:
            layer_name = layer.name()
            layer_fields = layer.fields()
            self.layer_fields_mapping[layer_name] = layer_fields
            self.layer_field_names_mapping[layer_name] = [field.name() for field in layer_fields.toList()]

    def setup_spatial_indexes(self):
        """Setup input layer spatial indexes."""
        self.spatial_indexes_map = {}
        self.spatial_indexes_map['source'] = spatial_index(self.external_source)
        for layer in [self.node_layer, self.cross_section_layer]:
            layer_name = layer.name()
            self.spatial_indexes_map[layer_name] = spatial_index(layer)

    def setup_node_by_location(self):
        """Setup nodes by location."""
        self.node_by_location = {}
        for node_feat in self.node_layer.getFeatures():
            node_geom = node_feat.geometry()
            node_point = node_geom.asPoint()
            self.node_by_location[node_point] = node_feat["id"]

    def get_channel_structures_data(self, channel_feat, selected_ids=None):
        """Extract and calculate channel structures data."""
        channel_structures = []
        processed_structure_ids = set()
        if selected_ids is None:
            selected_ids = set()
        channel_id = channel_feat["id"]
        channel_geometry = channel_feat.geometry()
        structure_features_map, structure_index = self.spatial_indexes_map['source']
        structure_fids = structure_index.intersects(channel_geometry.boundingBox())
        for structure_fid in structure_fids:
            if structure_fid in processed_structure_ids:
                continue
            if selected_ids and structure_fid not in selected_ids:
                continue
            structure_feat = structure_features_map[structure_fid]
            structure_geom = structure_feat.geometry()
            structure_geom_type = structure_geom.type()
            if structure_geom_type == QgsWkbTypes.GeometryType.LineGeometry:
                poly_line = structure_geom.asPolyline()
                start_point = poly_line[0]
                end_point = poly_line[-1]
                start_geom, end_geom = QgsGeometry.fromPointXY(start_point), QgsGeometry.fromPointXY(end_point)
                start_buffer = start_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                end_buffer = end_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                intersection_m = channel_geometry.lineLocatePoint(structure_geom.centroid())
                structure_length = structure_geom.length()
                if not all([start_buffer.intersects(channel_geometry), end_buffer.intersects(channel_geometry)]):
                    continue
            elif structure_geom_type == QgsWkbTypes.GeometryType.PointGeometry:
                structure_buffer = structure_geom.buffer(
                    self.conversion_settings.snapping_distance, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                if not structure_buffer.intersects(channel_geometry):
                    continue
                intersection_m = channel_geometry.lineLocatePoint(structure_geom)
                structure_length = (
                    structure_feat[self.conversion_settings.length_source_field]
                    if self.conversion_settings.length_source_field
                    else self.conversion_settings.length_fallback_value
                )
            else:
                continue
            channel_structure = self.channel_structure_cls(channel_id, structure_feat, intersection_m, structure_length)
            channel_structures.append(channel_structure)
            processed_structure_ids.add(structure_fid)
        channel_structures.sort(key=attrgetter("m"))
        return channel_structures, processed_structure_ids

    def update_feature_endpoints(self, dst_feature, **template_node_attributes):
        """Update feature endpoint references."""
        new_nodes = []
        linear_geom = dst_feature.geometry()
        channel_polyline = linear_geom.asPolyline()
        start_node_point, end_node_point = channel_polyline[0], channel_polyline[-1]
        node_layer_name = self.node_layer.name()
        node_layer_fields = self.layer_fields_mapping[node_layer_name]
        # TODO: remove duplicate code
        try:
            start_node_id = self.node_by_location[start_node_point]
        except KeyError:
            start_node_feat = self.node_manager.create_new(QgsGeometry.fromPointXY(start_node_point), node_layer_fields)
            start_node_id = start_node_feat["id"]
            for field_name, field_value in template_node_attributes.items():
                if field_name == "id":
                    continue
                start_node_feat[field_name] = field_value
            self.node_by_location[start_node_point] = start_node_id
            new_nodes.append(start_node_feat)
        try:
            end_node_id = self.node_by_location[end_node_point]
        except KeyError:
            end_node_feat = self.node_manager.create_new(QgsGeometry.fromPointXY(end_node_point), node_layer_fields)
            end_node_id = end_node_feat["id"]
            for field_name, field_value in template_node_attributes.items():
                if field_name == "id":
                    continue
                end_node_feat[field_name] = field_value
            self.node_by_location[end_node_point] = end_node_id
            new_nodes.append(end_node_feat)
        dst_feature["connection_node_id_start"] = start_node_id
        dst_feature["connection_node_id_end"] = end_node_id
        return new_nodes

    def update_channel_cross_section_references(self, new_channels, source_channel_xs_locations):
        """Update channel cross-section references."""
        xs_location_features_map, xs_location_index = self.spatial_indexes_map[self.cross_section_layer.name()]
        xs_fields = self.layer_fields_mapping[self.cross_section_layer.name()]
        channel_id_idx = xs_fields.lookupField("channel_id")
        next_cross_section_location_id = get_next_feature_id(self.cross_section_layer)
        cross_section_location_copies = []
        for channel_feat in new_channels:
            channel_xs_count = 0
            channel_id = channel_feat["id"]
            channel_geometry = channel_feat.geometry()
            channel_geometry_middle = channel_geometry.interpolate(channel_geometry.length() * 0.5)
            xs_fids = xs_location_index.intersects(channel_geometry.boundingBox())
            for xs_fid in xs_fids:
                xs_feat = xs_location_features_map[xs_fid]
                xs_geom = xs_feat.geometry()
                xs_buffer = xs_geom.buffer(
                    DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS
                )
                if channel_geometry.intersects(xs_buffer):
                    self.cross_section_layer.changeAttributeValue(xs_fid, channel_id_idx, channel_id)
                    channel_xs_count += 1
            if channel_xs_count == 0:
                src_channel_xs_ids = [str(xs_id) for xs_id in source_channel_xs_locations]
                if src_channel_xs_ids:
                    xs_ids_str = ",".join(src_channel_xs_ids)
                    xs_distance_map = [
                        (xs_feat, channel_geometry.distance(xs_feat.geometry()))
                        for xs_feat in get_features_by_expression(
                            self.cross_section_layer, f'"id" in ({xs_ids_str})', with_geometry=True
                        )
                    ]
                    xs_distance_map.sort(key=itemgetter(1))
                    closest_xs_feat_copy = QgsFeature(xs_distance_map[0][0])
                    closest_xs_feat_copy.setGeometry(channel_geometry_middle)
                    closest_xs_feat_copy["channel_id"] = channel_id
                    closest_xs_feat_copy["id"] = next_cross_section_location_id
                    next_cross_section_location_id += 1
                    cross_section_location_copies.append(closest_xs_feat_copy)
        if cross_section_location_copies:
            self.cross_section_layer.addFeatures(cross_section_location_copies)

    def remove_hanging_cross_sections(self, visited_channel_ids):
        """Remove cross-sections not aligned with the channels."""
        xs_leftovers = []
        channel_feats, channels_spatial_index = spatial_index(self.integrate_layer)
        for xs_feat in self.cross_section_layer.getFeatures():
            xs_geom = xs_feat.geometry()
            xs_buffer = xs_geom.buffer(DEFAULT_INTERSECTION_BUFFER, DEFAULT_INTERSECTION_BUFFER_SEGMENTS)
            channel_fids = channels_spatial_index.intersects(xs_buffer.boundingBox())
            # only modify channels that were visited
            channel_fids = list(set(channel_fids).intersection(visited_channel_ids))
            if len(channel_fids) == 0:
                continue
            xs_intersects = False
            for channel_fid in channel_fids:
                channel_feat = channel_feats[channel_fid]
                if xs_buffer.intersects(channel_feat.geometry()):
                    xs_intersects = True
                    break
            if not xs_intersects:
                xs_leftovers.append(xs_feat.id())
        if xs_leftovers:
            self.cross_section_layer.deleteFeatures(xs_leftovers)

    @staticmethod
    def substring_feature(curve, start_distance, end_distance, fields, simplify=False, **attributes):
        """Extract part of the curve as a new structure feature."""
        substring_feat = QgsFeature(fields)
        substring_feat.setGeometry(get_substring_geometry(curve, start_distance, end_distance, simplify))
        for field_name, field_value in attributes.items():
            substring_feat[field_name] = field_value
        return substring_feat

    def integrate_structure_features(self, channel_feat, channel_structures):
        """Integrate structures with a channel network."""
        channel_layer_name = self.integrate_layer.name()
        channel_fields = self.layer_fields_mapping[channel_layer_name]
        channel_field_names = self.layer_field_names_mapping[channel_layer_name]
        channel_attributes = {field_name: channel_feat[field_name] for field_name in channel_field_names}
        channel_geom = channel_feat.geometry()
        first_node_id = channel_attributes['connection_node_id_start']
        first_node_feat = next(get_features_by_expression(self.node_layer, f'"id" = {first_node_id}'))
        node_field_names = self.layer_field_names_mapping[self.node_layer.name()]
        node_attributes = {field_name: first_node_feat[field_name] for field_name in node_field_names}
        channel_curve = channel_geom.constGet()
        previous_structure_end = 0
        simplify_structure_geometry = self.target_model_cls != dm.Culvert
        structure_fields = self.layer_fields_mapping[self.target_layer.name()]
        structure_field_names = self.layer_field_names_mapping[self.target_layer.name()]
        total_length = sum(channel_structure.length for channel_structure in channel_structures)
        added_features = defaultdict(list)
        if channel_geom.length() < total_length:
            id_str = ', '.join(str(channel_structure.feature.id()) for channel_structure in channel_structures)
            message = (f'Cannot integrate {self.target_model_cls.__tablename__}s with total length {total_length:.2f} '
                       f'into channel {channel_feat["id"]} with length {channel_geom.length():.2f}. '
                       f'Primary keys {self.target_model_cls.__tablename__}s: {id_str}')
            warnings.warn(f"{message}", StructuresIntegratorWarning)
            return
        next_channel_id = get_next_feature_id(self.integrate_layer)
        for i, channel_structure in enumerate(sorted(channel_structures, key=lambda x: x.m)):
            new_nodes = []
            src_structure_feat = channel_structure.feature
            structure_feat = QgsFeature(structure_fields)
            # Update with values from the widgets.
            update_attributes(self.fields_configurations[self.target_model_cls], self.target_model_cls, src_structure_feat, structure_feat)
            structure_attributes = {field_name: structure_feat[field_name] for field_name in structure_field_names}
            structure_length = channel_structure.length
            channel_structure_m = channel_structure.m
            half_length = structure_length * 0.5
            # when structures overlap, move them to the end of the previous structure
            if channel_structure_m - half_length < previous_structure_end:
                channel_structure_m = previous_structure_end + half_length
            start_distance = channel_structure_m - half_length
            end_distance = channel_structure_m + half_length
            # Setup structure feature
            substring_geom = get_substring_geometry(channel_curve, start_distance, end_distance, simplify_structure_geometry)
            substring_feat = self.target_manager.create_new(substring_geom, structure_fields, structure_attributes)
            added_features[self.node_layer.name()] += self.update_feature_endpoints(substring_feat, **node_attributes)
            added_features[self.target_layer.name()].append(substring_feat)
            # Setup channel leftover feature
            # todo: is this check necessary?
            if start_distance > previous_structure_end:
                before_substring_feat = self.substring_feature(
                    channel_curve, previous_structure_end, start_distance, channel_fields, False, **channel_attributes
                )
                added_features[self.node_layer.name()] += self.update_feature_endpoints(before_substring_feat, **node_attributes)
                if i > 0:
                    before_substring_feat["id"] = next_channel_id
                    next_channel_id += 1
                added_features[channel_layer_name].append(before_substring_feat)
            previous_structure_end = end_distance
            if new_nodes:
                update_attributes(self.fields_configurations[dm.ConnectionNode], dm.ConnectionNode, src_structure_feat, *new_nodes)
        # Setup last channel leftover feature
        last_substring_end = channel_geom.length()
        if last_substring_end - previous_structure_end > 0:
            last_substring_feat = self.substring_feature(
                channel_curve, previous_structure_end, last_substring_end, channel_fields, False, **channel_attributes
            )
            added_features[self.node_layer.name()] += self.update_feature_endpoints(last_substring_feat, **node_attributes)
            last_substring_feat["id"] = next_channel_id
            added_features[channel_layer_name].append(last_substring_feat)
        return added_features

    def integrate_features(self, input_feature_ids, selected_ids):
        """Method responsible for the importing/integrating structures from the external feature source."""
        all_processed_structure_ids = set()
        features_to_add = defaultdict(list)
        channels_replaced = []
        for channel_feature in self.integrate_layer.getFeatures():
            channel_structures, processed_structures_fids = self.get_channel_structures_data(
                channel_feature, selected_ids
            )
            ch_id = channel_feature["id"]
            source_channel_xs_locations = [xs["id"] for xs in get_features_by_expression(self.cross_section_layer, f'"channel_id" = {ch_id}')]
            if channel_structures:
                added_features = self.integrate_structure_features(channel_feature, channel_structures)
                self.update_channel_cross_section_references(added_features[self.integrate_layer.name()], source_channel_xs_locations)
                for key in added_features:
                    features_to_add[key] += added_features[key]
                all_processed_structure_ids |= processed_structures_fids
                channels_replaced.append(ch_id)
        self.integrate_layer.startEditing()
        for ch_id in channels_replaced:
            self.integrate_layer.deleteFeature(ch_id)
        return features_to_add, list(all_processed_structure_ids)


class CulvertsImporter(LinesImporter):
    """Class with methods responsible for the importing culverts from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args, target_model_cls=dm.Culvert, target_layer=structure_layer,
                         node_layer=node_layer)


class CulvertsIntegrator(LinesImporter):
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
                         node_layer=node_layer, channel_layer=channel_layer, cross_section_location_layer=cross_section_location_layer)


class OrificesImporter(LinesImporter):
    """Class with methods responsible for the importing orifices from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args, target_model_cls=dm.Orifice, target_layer=structure_layer,
                         node_layer=node_layer)


class OrificesIntegrator(LinesImporter):
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
                         node_layer=node_layer, cchannel_layer=channel_layer, cross_section_location_layer=cross_section_location_layer)


class WeirsImporter(LinesImporter):
    """Class with methods responsible for the importing weirs from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args, target_model_cls=dm.Weir, target_layer=structure_layer,
                         node_layer=node_layer)


class WeirsIntegrator(LinesImporter):
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
                         node_layer=node_layer, channel_layer=channel_layer, cross_section_location_layer=cross_section_location_layer)


class PipesImporter(LinesImporter):
    """Class with methods responsible for the importing pipes from the external data source."""

    def __init__(self, *args, structure_layer=None, node_layer=None):
        super().__init__(*args, target_model_cls=dm.Pipe, target_layer=structure_layer,
                         node_layer=node_layer)


class ConnectionNodesImporter(Importer):
    """Connection nodes importer class."""

    def __init__(self, *args, target_layer=None):
        super().__init__(*args, target_model_cls=dm.ConnectionNode, target_layer=target_layer)
        self.processor = ConnectionNodeProcessor(self.target_layer, self.target_model_cls, self.target_manager)
