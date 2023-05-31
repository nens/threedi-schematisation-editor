# Copyright (C) 2023 by Lutra Consulting
import bisect
import statistics
from collections import defaultdict
from operator import attrgetter

from osgeo import gdal, ogr, osr

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor import enumerators as en
from threedi_schematisation_editor.mike.mike_parser import MikeParser, NWKComponent, XSComponent
from threedi_schematisation_editor.mike.utils import (
    ResistanceTypes,
    create_data_model_layer,
    gdal_linestring,
    gdal_point,
    interpolate_chainage_point,
)

gdal.SetConfigOption("OGR_SQLITE_SYNCHRONOUS", "OFF")  # Speed up the runtime on EXT4 filesystems


class MIKEConverter:
    def __init__(self, sim11_filepath, threedi_gpkg_filepath):
        self.parser = MikeParser(sim11_filepath)
        self.threedi_gpkg_filepath = threedi_gpkg_filepath
        self.crs = osr.SpatialReference()
        self.nwk_component = None
        self.xs_component = None
        self.visited_node_values = {}

    def mike2threedi(self):
        self.parser.detect_components()
        for component in self.parser.components.values():
            component.parse_component_data()
        self.initialize_threedi_dataset()
        threedi_dataset = gdal.OpenEx(self.threedi_gpkg_filepath, gdal.OF_UPDATE)
        self.process_network(threedi_dataset)
        threedi_dataset = None

    def initialize_threedi_dataset(self):
        projection = self.parser.projection
        self.crs.ImportFromProj4(projection)
        ogr.GetDriverByName("GPKG").CreateDataSource(self.threedi_gpkg_filepath)
        threedi_dataset = gdal.OpenEx(self.threedi_gpkg_filepath, gdal.OF_UPDATE)
        for model_cls in dm.ALL_MODELS:
            create_data_model_layer(model_cls, threedi_dataset, self.crs)
        threedi_dataset = None

    def _enriched_branch(self, branch):
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

    def _create_channel_feature(self, channel_layer, branch, current_channel_id, current_node_id):
        channel_feature = ogr.Feature(channel_layer.GetLayerDefn())
        branch_points = branch.points
        start_point, end_point = branch_points[0], branch_points[-1]
        start_point_id, end_point_id = start_point.id, end_point.id
        try:
            start_node_values = self.visited_node_values[start_point_id]
        except KeyError:
            start_node_values = {"id": current_node_id, "code": str(start_point_id)}
            current_node_id += 1
            self.visited_node_values[start_point_id] = start_node_values
        try:
            end_node_values = self.visited_node_values[end_point_id]
        except KeyError:
            end_node_values = {"id": current_node_id, "code": str(end_point_id)}
            current_node_id += 1
            self.visited_node_values[end_point_id] = end_node_values
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
        multiplied_cross_sections = defaultdict(list)
        branches_without_xs = {}
        ignore_m_values = {float("-inf"), float("inf")}
        available_xs_chainages = [xs.chainage for xs in branch_cross_sections]
        max_xs_idx = len(branch_cross_sections) - 1
        for sub_branch in separated_branches:
            no_xs = True
            sub_branch_points = [p for p in sub_branch.points if p.m not in ignore_m_values]
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

    def _create_cross_section_feature(self, cross_section_layer, xs, current_xs_id, branch, current_channel_id):
        if branch.downstream_chainage < xs.chainage:  # Skip cross-section with chainage beyond branch range
            return None
        xs_feature = ogr.Feature(cross_section_layer.GetLayerDefn())
        resistance_type = ResistanceTypes(xs.resistance_type)
        lowest_level = 0.0
        if resistance_type in [ResistanceTypes.MANNING_N, ResistanceTypes.MANNING_M]:
            friction_type = en.FrictionType.MANNING.value
        elif resistance_type == ResistanceTypes.CHEZY:
            friction_type = en.FrictionType.CHEZY.value
        else:
            friction_type = None
        distances, elevation_levels, resistance_values, bank_levels = [], [], [], []
        for distance, elevation, resistance, marker in xs.profile:
            distances.append(distance)
            elevation_float = float(elevation)
            resistance_float = (
                1 / float(resistance) if resistance_type == ResistanceTypes.MANNING_M else float(resistance)
            )
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
            xs_chainage_pid = self.nwk_component.chainage_points[branch.name, xs.chainage]
            xs_chainage_point = self.nwk_component.points[xs_chainage_pid]
            xs_geom = gdal_point(xs_chainage_point)
        except KeyError:
            xs_geom = interpolate_chainage_point(branch, xs.chainage)
        xs_values = {
            "id": current_xs_id,
            "code": f"{xs.name}_{xs.chainage}",
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

    def process_network(self, threedi_dataset):
        node_layer = threedi_dataset.GetLayerByName(dm.ConnectionNode.__tablename__)
        channel_layer = threedi_dataset.GetLayerByName(dm.Channel.__tablename__)
        cross_section_layer = threedi_dataset.GetLayerByName(dm.CrossSectionLocation.__tablename__)
        self.nwk_component = self.parser.components[NWKComponent]
        self.xs_component = self.parser.components[XSComponent]
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
                    channel_layer, sub_branch, current_channel_id, current_node_id
                )
                for xs in sub_branch_cross_sections:
                    xs_feature = self._create_cross_section_feature(
                        cross_section_layer, xs, current_xs_id, branch, current_channel_id
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
            node_feature = ogr.Feature(node_layer.GetLayerDefn())
            for field_name, field_value in node_values.items():
                node_feature.SetField(field_name, field_value)
            point = self.nwk_component.points[node_point_id]
            node_geom = gdal_point(point)
            node_feature.SetGeometry(node_geom)
            node_layer.CreateFeature(node_feature)
            node_feature = None
