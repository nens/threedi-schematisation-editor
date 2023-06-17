# Copyright (C) 2023 by Lutra Consulting
import bisect
import os
import statistics
from collections import defaultdict
from functools import cached_property
from operator import attrgetter

from osgeo import gdal, ogr, osr

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor import enumerators as en
from threedi_schematisation_editor.mike.mike_parser import HDComponent, MikeParser, NWKComponent, XSComponent
from threedi_schematisation_editor.mike.utils import (
    CulvertGeometryTypes,
    ResistanceTypes,
    StructureTypes,
    create_data_model_layer,
    gdal_linestring,
    gdal_point,
    interpolate_chainage_point,
)

gdal.SetConfigOption("OGR_SQLITE_SYNCHRONOUS", "OFF")  # Speed up the runtime on EXT4 filesystems


class MIKEConverter:
    """MIKE11 -> 3Di models conversion class."""

    def __init__(self, sim11_filepath, threedi_gpkg_filepath):
        self.parser = MikeParser(sim11_filepath)
        self.threedi_gpkg_filepath = threedi_gpkg_filepath
        self.crs = osr.SpatialReference()
        self.nwk_component = None
        self.xs_component = None
        self.hd_component = None
        self.visited_node_values = {}

    @cached_property
    def intermediate_structures_filepath(self):
        """Get output GeoPackage filepath for storing intermediate structures data."""
        threedi_gpkg_dirname = os.path.dirname(self.threedi_gpkg_filepath)
        threedi_gpkg_filename = os.path.basename(self.threedi_gpkg_filepath)
        intermediate_structures_filename = f"{threedi_gpkg_filename[:-5]}_intermediate_structures.gpkg"
        intermediate_structures_gpkg_filepath = os.path.join(threedi_gpkg_dirname, intermediate_structures_filename)
        return intermediate_structures_gpkg_filepath

    def mike2threedi(self):
        """Handle parsing and conversion MIKE11 model data."""
        self.parser.detect_components()
        for component in self.parser.components.values():
            component.parse_component_data()
        self.initialize_threedi_dataset()
        self.initialize_intermediate_structures_dataset()
        self.process_network()
        self.export_network_structures()

    def initialize_threedi_dataset(self):
        """Initialize GeoPackage with 3Di model structure."""
        projection = self.parser.projection
        self.crs.ImportFromProj4(projection)
        self.crs.AutoIdentifyEPSG()
        authority_code = self.crs.GetAttrValue("AUTHORITY", 1)
        ogr.GetDriverByName("GPKG").CreateDataSource(self.threedi_gpkg_filepath)
        threedi_dataset = gdal.OpenEx(self.threedi_gpkg_filepath, gdal.OF_UPDATE)
        for model_cls in dm.ALL_MODELS:
            create_data_model_layer(model_cls, threedi_dataset, self.crs)
        schema_version_layer = threedi_dataset.GetLayerByName(dm.SchemaVersion.__tablename__)
        schema_version_feature = ogr.Feature(schema_version_layer.GetLayerDefn())
        schema_version_feature.SetField("version_num", dm.SchemaVersion.SUPPORTED_SCHEMA_VERSION)
        schema_version_layer.CreateFeature(schema_version_feature)
        schema_version_feature = None
        global_settings_layer = threedi_dataset.GetLayerByName(dm.GlobalSettings.__tablename__)
        global_settings_feature = ogr.Feature(global_settings_layer.GetLayerDefn())
        global_settings_feature.SetField("epsg_code", authority_code)
        global_settings_layer.CreateFeature(global_settings_feature)
        global_settings_feature = None
        threedi_dataset = None

    def initialize_intermediate_structures_dataset(self):
        """Initialize GeoPackage with an intermediate point structures."""
        projection = self.parser.projection
        self.crs.ImportFromProj4(projection)
        ogr.GetDriverByName("GPKG").CreateDataSource(self.intermediate_structures_filepath)
        intermediate_structures_dataset = gdal.OpenEx(self.intermediate_structures_filepath, gdal.OF_UPDATE)
        for model_cls in [dm.Culvert, dm.Orifice, dm.Weir]:
            model_cls.__geometrytype__ = en.GeometryType.Point
            create_data_model_layer(model_cls, intermediate_structures_dataset, self.crs)
            model_cls.__geometrytype__ = en.GeometryType.Linestring
        intermediate_structures_dataset = None

    def _enriched_branch(self, branch):
        """Add extra branch points."""
        branch_points_copy = list(branch.points)
        branch_points_copy.extend(self.nwk_component.extra_branch_points[branch.name])
        branch_points_copy.sort(key=attrgetter("m"))
        start_point, end_point = branch_points_copy[0], branch_points_copy[-1]
        start_point_id, end_point_id = start_point.id, end_point.id
        try:
            start_point_id = self.nwk_component.node_replacements[start_point_id]
            start_point = self.nwk_component.points[start_point_id]
            branch_points_copy.insert(0, start_point)
        except KeyError:
            pass
        try:
            end_point_id = self.nwk_component.node_replacements[end_point_id]
            end_point = self.nwk_component.points[end_point_id]
            branch_points_copy.append(end_point)
        except KeyError:
            pass
        branch_attributes = branch._asdict()
        branch_attributes["points"] = tuple(branch_points_copy)
        enriched_branch = self.nwk_component.branch_cls(**branch_attributes)
        return enriched_branch

    def _split_branch(self, branch):
        """Split branches at crossings."""
        separated_branches = []
        branch_split_points = list(sorted(self.nwk_component.branch_split_points[branch.name], key=attrgetter("m")))
        branch_points = list(branch.points)
        branch_points_ids = [p.id for p in branch_points]
        branch_attributes = branch._asdict()
        for split_point in branch_split_points:
            split_point_idx = branch_points_ids.index(split_point.id)
            sub_branch_points = branch_points[: split_point_idx + 1]
            del branch_points[:split_point_idx]
            del branch_points_ids[:split_point_idx]
            branch_attributes["points"] = tuple(sub_branch_points)
            sub_branch = self.nwk_component.branch_cls(**branch_attributes)
            separated_branches.append(sub_branch)
        branch_attributes["points"] = tuple(branch_points)
        last_branch = self.nwk_component.branch_cls(**branch_attributes)
        separated_branches.append(last_branch)
        return separated_branches

    def _create_channel_feature(self, channel_layer_defn, branch, current_channel_id, current_node_id):
        """Create 3Di channel feature out of the branch object."""
        channel_feature = ogr.Feature(channel_layer_defn)
        branch_points = branch.points
        start_point, end_point = branch_points[0], branch_points[-1]
        start_point_id, end_point_id = start_point.id, end_point.id
        src_start_point_id, src_end_point_id = abs(start_point_id), abs(end_point_id)  # Switch to source point IDs
        try:
            start_node_values = self.visited_node_values[src_start_point_id]
        except KeyError:
            if start_point_id > 0:
                origin_branch = branch
                origin_point = start_point
            else:
                up_link_name, up_link_chainage = branch.upstream_connection
                origin_branch = self.nwk_component.branches[up_link_name]
                origin_point = self.nwk_component.points[src_start_point_id]
            initial_waterlevel = self._node_initial_waterlevel(origin_branch, origin_point)
            start_node_values = {
                "id": current_node_id,
                "code": str(src_start_point_id),
                "initial_waterlevel": initial_waterlevel,
            }
            current_node_id += 1
            self.visited_node_values[src_start_point_id] = start_node_values
        try:
            end_node_values = self.visited_node_values[src_end_point_id]
        except KeyError:
            if end_point_id > 0:
                origin_branch = branch
                origin_point = end_point
            else:
                down_link_name, down_link_chainage = branch.downstream_connection
                origin_branch = self.nwk_component.branches[down_link_name]
                origin_point = self.nwk_component.points[src_end_point_id]
            initial_waterlevel = self._node_initial_waterlevel(origin_branch, origin_point)
            end_node_values = {
                "id": current_node_id,
                "code": str(src_end_point_id),
                "initial_waterlevel": initial_waterlevel,
            }
            current_node_id += 1
            self.visited_node_values[src_end_point_id] = end_node_values
        channel_values = {
            "id": current_channel_id,
            "code": branch.name,
            "calculation_type": en.CalculationType.CONNECTED.value,
            "display_name": f"{branch.name} ({branch.topo_id})",
            "connection_node_start_id": start_node_values["id"],
            "connection_node_end_id": end_node_values["id"],
        }
        for field_name, field_value in channel_values.items():
            channel_feature.SetField(field_name, field_value)
        channel_geom = gdal_linestring(branch_points)
        channel_feature.SetGeometry(channel_geom)
        return channel_feature, current_node_id

    def _multiply_branch_cross_sections(self, separated_branches, branch_cross_sections):
        """Multiply neighbouring cross-sections on branches without any."""
        if not branch_cross_sections:  # Handling "linkchannel" branches
            return {sub_branch: [] for sub_branch in separated_branches}
        multiplied_cross_sections = defaultdict(list)
        branches_without_xs = {}
        available_xs_chainages = [xs.chainage for xs in branch_cross_sections]
        max_xs_idx = len(branch_cross_sections) - 1
        for sub_branch in separated_branches:
            no_xs = True
            sub_branch_points = [p for p in sub_branch.points if p.id > 0]  # Skip points with a negative ID
            start_point, end_point = sub_branch_points[0], sub_branch_points[-1]
            start_m, end_m = start_point.m, end_point.m
            for xs, xs_chainage in zip(branch_cross_sections, available_xs_chainages):
                if start_m <= xs_chainage <= end_m:
                    no_xs = False
                    multiplied_cross_sections[sub_branch].append(xs)
            if no_xs:
                branches_without_xs[start_m, end_m] = sub_branch
        for (start_m, end_m), sub_branch in branches_without_xs.items():
            additional_chainage = round(start_m + ((end_m - start_m) * 0.5), 3)
            closest_xs_idx = bisect.bisect_left(available_xs_chainages, additional_chainage)
            closest_xs = (
                branch_cross_sections[closest_xs_idx]
                if closest_xs_idx <= max_xs_idx
                else branch_cross_sections[max_xs_idx]
            )
            closest_xs_attributes = closest_xs._asdict()
            closest_xs_attributes["chainage"] = additional_chainage
            closest_xs_attributes["name"] = f"cloned_{closest_xs.name}"
            cloned_xs = self.xs_component.xs_cls(**closest_xs_attributes)
            multiplied_cross_sections[sub_branch].append(cloned_xs)
        return multiplied_cross_sections

    def _create_cross_section_feature(self, cross_section_layer_defn, xs, current_xs_id, branch, current_channel_id):
        """Create cross-section location features."""
        xs_chainage = xs.chainage
        if branch.downstream_chainage < xs_chainage:  # Skip cross-section with chainage beyond branch range
            return None
        xs_feature = ogr.Feature(cross_section_layer_defn)
        resistance_type = ResistanceTypes(xs.resistance_type)
        lowest_level = 0.0
        if resistance_type in [ResistanceTypes.MANNING_N, ResistanceTypes.MANNING_M]:
            friction_type = en.FrictionType.MANNING.value
        elif resistance_type == ResistanceTypes.CHEZY:
            friction_type = en.FrictionType.CHEZY.value
        elif resistance_type == ResistanceTypes.RELATIVE:
            friction_type = en.FrictionType.MANNING.value
        else:
            friction_type = None
        distances, elevation_levels, resistance_values, bank_levels = [], [], [], []
        branch_chainage_resistance = self._branch_chainage_resistance(branch, xs_chainage)
        for distance, elevation, resistance, marker in xs.profile:
            distances.append(distance)
            elevation_float = float(elevation)
            if resistance_type == ResistanceTypes.MANNING_N:
                resistance_float = float(resistance)
            elif resistance_type == ResistanceTypes.MANNING_M:
                resistance_float = 1 / float(resistance)
            elif resistance_type == ResistanceTypes.RELATIVE:
                resistance_float = branch_chainage_resistance
            else:
                resistance_float = 1.0
            elevation_levels.append(elevation_float)
            resistance_values.append(resistance_float)
            if marker in self.xs_component.levee_banks_markers:
                bank_levels.append(elevation_float)
            elif marker == self.xs_component.lowest_point_marker:
                lowest_level = elevation_float
        if lowest_level < 0.0:
            elevation_levels = [elevation - lowest_level for elevation in elevation_levels]
            bank_levels = [elevation - lowest_level for elevation in bank_levels]
        xs_table = "\n".join(f"{distance}, {elevation:.3f}" for distance, elevation in zip(distances, elevation_levels))
        reference_level = lowest_level if lowest_level > 0.0 else 0.0
        bank_level = min(bank_levels) if bank_levels else None
        friction_value = round(statistics.fmean(resistance_values), 3)
        try:
            xs_chainage_pid = self.nwk_component.chainage_points[branch.name, xs_chainage]
            xs_chainage_point = self.nwk_component.points[xs_chainage_pid]
            xs_geom = gdal_point(xs_chainage_point)
        except KeyError:
            xs_geom = interpolate_chainage_point(branch, xs.chainage)
        xs_values = {
            "id": current_xs_id,
            "code": f"{xs.name}_{xs_chainage}",
            "channel_id": current_channel_id,
            "reference_level": reference_level,
            "bank_level": bank_level,
            "friction_value": friction_value,
            "friction_type": friction_type,
            "cross_section_shape": en.CrossSectionShape.YZ.value,
            "cross_section_table": xs_table,
        }
        for xs_field_name, xs_field_value in xs_values.items():
            xs_feature.SetField(xs_field_name, xs_field_value)
        xs_feature.SetGeometry(xs_geom)
        return xs_feature

    def _branch_chainage_resistance(self, branch, chainage):
        """Apply resistance values to the cross-sections."""
        branch_name = branch.name
        branch_bed_resistance = self.hd_component.bed_resistance[branch_name]
        if not branch_bed_resistance:
            return 1.0
        branch_bed_resistance_chainages = [bed_resistance.chainage for bed_resistance in branch_bed_resistance]
        branch_bed_resistance_values = [bed_resistance.resistance for bed_resistance in branch_bed_resistance]
        max_idx = len(branch_bed_resistance) - 1
        resistance_idx = bisect.bisect_left(branch_bed_resistance_chainages, chainage)
        resistance_value = (
            branch_bed_resistance_values[resistance_idx]
            if resistance_idx < max_idx
            else branch_bed_resistance_values[max_idx]
        )
        return resistance_value

    def _node_initial_waterlevel(self, branch, point):
        """Apply initial waterlevel values to the nodes."""
        branch_initial_conditions = self.hd_component.initial_conditions[branch.name]
        if not branch_initial_conditions:
            return None
        branch_initials_chainages = [initial_conditions.chainage for initial_conditions in branch_initial_conditions]
        branch_initial_waterlevels = [initial_conditions.h for initial_conditions in branch_initial_conditions]
        max_idx = len(branch_initial_conditions) - 1
        initial_conditions_idx = bisect.bisect_left(branch_initials_chainages, point.m)
        initial_waterlevel_value = (
            branch_initial_waterlevels[initial_conditions_idx]
            if initial_conditions_idx < max_idx
            else branch_initial_waterlevels[max_idx]
        )
        return initial_waterlevel_value

    def process_network(self):
        """Convert parsed MIKE11 model data into 3Di GeoPackage schematization structure."""
        threedi_dataset = gdal.OpenEx(self.threedi_gpkg_filepath, gdal.OF_UPDATE)
        node_layer = threedi_dataset.GetLayerByName(dm.ConnectionNode.__tablename__)
        node_layer_defn = node_layer.GetLayerDefn()
        channel_layer = threedi_dataset.GetLayerByName(dm.Channel.__tablename__)
        channel_layer_defn = channel_layer.GetLayerDefn()
        cross_section_layer = threedi_dataset.GetLayerByName(dm.CrossSectionLocation.__tablename__)
        cross_section_layer_defn = cross_section_layer.GetLayerDefn()
        self.nwk_component = self.parser.components[NWKComponent]
        self.xs_component = self.parser.components[XSComponent]
        self.hd_component = self.parser.components[HDComponent]
        current_node_id, current_channel_id, current_xs_id = 1, 1, 1
        self.visited_node_values.clear()
        for branch_name, branch in self.nwk_component.branches.items():
            if branch.is_link:
                continue
            enriched_branch = self._enriched_branch(branch)
            separated_branches = self._split_branch(enriched_branch)
            branch_cross_sections = self.xs_component.cross_section_data[branch_name]
            multiplied_cross_sections = self._multiply_branch_cross_sections(separated_branches, branch_cross_sections)
            for sub_branch, sub_branch_cross_sections in multiplied_cross_sections.items():
                channel_feature, current_node_id = self._create_channel_feature(
                    channel_layer_defn, sub_branch, current_channel_id, current_node_id
                )
                for xs in sub_branch_cross_sections:
                    xs_feature = self._create_cross_section_feature(
                        cross_section_layer_defn, xs, current_xs_id, branch, current_channel_id
                    )
                    if xs_feature is None:
                        continue
                    cross_section_layer.CreateFeature(xs_feature)
                    current_xs_id += 1
                    xs_feature = None
                channel_layer.CreateFeature(channel_feature)
                current_channel_id += 1
                channel_feature = None
        for node_point_id, node_values in self.visited_node_values.items():
            node_feature = ogr.Feature(node_layer_defn)
            for field_name, field_value in node_values.items():
                node_feature.SetField(field_name, field_value)
            point = self.nwk_component.points[node_point_id]
            node_geom = gdal_point(point)
            node_feature.SetGeometry(node_geom)
            node_layer.CreateFeature(node_feature)
            node_feature = None
        threedi_dataset = None

    def export_network_structures(self):
        """Export structures to the intermediate dataset."""
        intermediate_structures_dataset = gdal.OpenEx(self.intermediate_structures_filepath, gdal.OF_UPDATE)
        weir_layer = intermediate_structures_dataset.GetLayerByName(dm.Weir.__tablename__)
        weir_layer_defn = weir_layer.GetLayerDefn()
        culvert_layer = intermediate_structures_dataset.GetLayerByName(dm.Culvert.__tablename__)
        culvert_layer_defn = culvert_layer.GetLayerDefn()
        orifice_layer = intermediate_structures_dataset.GetLayerByName(dm.Orifice.__tablename__)
        orifice_layer_defn = orifice_layer.GetLayerDefn()
        nwk_component = self.parser.components[NWKComponent]
        weir_id, culvert_id, orifice_id = 1, 1, 1
        for weir in nwk_component.structures["weirs"]:
            weir_branch = nwk_component.branches[weir.river_name]
            weir_geom = interpolate_chainage_point(weir_branch, weir.chainage)
            weir_feature = ogr.Feature(weir_layer_defn)
            weir_feature.SetField("id", weir_id)
            weir_feature.SetField("code", weir.chainage)
            weir_feature.SetField("display_name", f"{weir.river_name} {weir.chainage}")
            weir_feature.SetField("cross_section_shape", en.CrossSectionShape.YZ.value)
            weir_table = "\n".join(f"{y}, {z:.3f}" for y, z in weir.geometry_data)
            weir_feature.SetField("cross_section_table", weir_table)
            weir_feature.SetGeometry(weir_geom)
            weir_layer.CreateFeature(weir_feature)
            weir_id += 1
            weir_feature = None
        for culvert in nwk_component.structures["culverts"]:
            culvert_branch = nwk_component.branches[culvert.river_name]
            culvert_geom = interpolate_chainage_point(culvert_branch, culvert.chainage)
            culvert_feature = ogr.Feature(culvert_layer_defn)
            culvert_feature.SetField("id", culvert_id)
            culvert_feature.SetField("code", culvert.chainage)
            culvert_feature.SetField("display_name", f"{culvert.river_name} {culvert.chainage}")
            culvert_feature.SetField("invert_level_start_point", culvert.upstream_invert)
            culvert_feature.SetField("invert_level_end_point", culvert.downstream_invert)
            culvert_feature.SetField("friction_value", culvert.friction)
            culvert_feature.SetField("friction_type", en.FrictionType.MANNING.value)
            culvert_geometry_type = culvert.geometry_type
            if culvert_geometry_type == CulvertGeometryTypes.RECTANGULAR:
                culvert_width, culvert_height = culvert.geometry_data[0]
                culvert_feature.SetField("cross_section_shape", en.CrossSectionShape.OPEN_RECTANGLE.value)
                culvert_feature.SetField("cross_section_width", culvert_width)
                culvert_feature.SetField("cross_section_height", culvert_height)
            elif culvert_geometry_type == CulvertGeometryTypes.CIRCULAR:
                culvert_width = culvert.geometry_data[0][0]
                culvert_feature.SetField("cross_section_shape", en.CrossSectionShape.CIRCLE.value)
                culvert_feature.SetField("cross_section_width", culvert_width)
            elif culvert_geometry_type in {
                CulvertGeometryTypes.IRREGULAR_DEPTH_WIDTH,
                CulvertGeometryTypes.IRREGULAR_LEVEL_WIDTH,
            }:
                culvert_feature.SetField("cross_section_shape", en.CrossSectionShape.YZ.value)
                culvert_table = "\n".join(f"{y}, {z:.3f}" for y, z in culvert.geometry_data)
                culvert_feature.SetField("cross_section_table", culvert_table)
            culvert_feature.SetGeometry(culvert_geom)
            culvert_layer.CreateFeature(culvert_feature)
            culvert_id += 1
            culvert_feature = None

        for control_structure in nwk_component.structures["control_structures"]:
            control_structure_branch = nwk_component.branches[control_structure.river_name]
            control_structure_geom = interpolate_chainage_point(control_structure_branch, control_structure.chainage)
            if control_structure.structure_type == StructureTypes.OVERFLOW:
                weir_feature = ogr.Feature(weir_layer_defn)
                weir_feature.SetField("id", weir_id)
                weir_feature.SetField("code", control_structure.chainage)
                weir_feature.SetField("display_name", f"{control_structure.river_name} {control_structure.chainage}")
                weir_feature.SetField("cross_section_shape", en.CrossSectionShape.OPEN_RECTANGLE.value)
                weir_feature.SetField("cross_section_width", control_structure.gate_width)
                weir_feature.SetField("cross_section_height", control_structure.sill_level)
                weir_feature.SetGeometry(control_structure_geom)
                weir_layer.CreateFeature(weir_feature)
                weir_id += 1
                weir_feature = None
            else:
                orifice_feature = ogr.Feature(orifice_layer_defn)
                orifice_feature.SetField("id", orifice_id)
                orifice_feature.SetField("code", control_structure.chainage)
                orifice_feature.SetField("display_name", f"{control_structure.river_name} {control_structure.chainage}")
                orifice_feature.SetField("crest_level", control_structure.sill_level)
                orifice_feature.SetField("cross_section_shape", en.CrossSectionShape.OPEN_RECTANGLE.value)
                orifice_feature.SetField("cross_section_width", control_structure.gate_width)
                orifice_feature.SetField("cross_section_height", control_structure.sill_level)
                orifice_feature.SetGeometry(control_structure_geom)
                orifice_layer.CreateFeature(orifice_feature)
                orifice_id += 1
                orifice_feature = None
        intermediate_structures_dataset = None
