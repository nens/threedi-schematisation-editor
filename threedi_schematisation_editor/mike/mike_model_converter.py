# Copyright (C) 2023 by Lutra Consulting
from osgeo import gdal, ogr, osr

from threedi_schematisation_editor import data_models as dm
from threedi_schematisation_editor import enumerators as en
from threedi_schematisation_editor.mike.mike_parser import MikeParser, NWKComponent, XSComponent
from threedi_schematisation_editor.mike.utils import create_data_model_layer

gdal.SetConfigOption("OGR_SQLITE_SYNCHRONOUS", "OFF")  # Speed up the runtime on EXT4 filesystems


class MIKEConverter:
    def __init__(self, sim11_filepath, threedi_gpkg_filepath):
        self.parser = MikeParser(sim11_filepath)
        self.threedi_gpkg_filepath = threedi_gpkg_filepath
        self.crs = osr.SpatialReference()

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

    def process_network(self, threedi_dataset):
        node_layer = threedi_dataset.GetLayerByName(dm.ConnectionNode.__tablename__)
        channel_layer = threedi_dataset.GetLayerByName(dm.Channel.__tablename__)
        cross_section_layer = threedi_dataset.GetLayerByName(dm.CrossSectionLocation.__tablename__)
        nwk_component = self.parser.components[NWKComponent]
        xs_component = self.parser.components[XSComponent]
        current_node_id, current_channel_id, current_xs_id = 1, 1, 1
        visited_node_values = {}
        for branch_topo_id, branch in nwk_component.branches.items():
            channel_feature = ogr.Feature(channel_layer.GetLayerDefn())
            branch_points = branch.points
            start_point, end_point = branch_points[0], branch_points[-1]
            start_point_id, end_point_id = start_point.id, end_point.id
            start_point = nwk_component.points[start_point_id]
            end_point = nwk_component.points[end_point_id]
            try:
                start_node_values = visited_node_values[start_point_id]
            except KeyError:
                start_node_values = {"id": current_node_id, "code": str(start_point.chainage)}
                current_node_id += 1
                visited_node_values[start_point_id] = start_node_values

            try:
                end_node_values = visited_node_values[end_point_id]
            except KeyError:
                end_node_values = {"id": current_node_id, "code": str(end_point.chainage)}
                current_node_id += 1
                visited_node_values[end_point_id] = end_node_values

            channel_values = {
                "id": current_channel_id,
                "code": branch.topo_id,
                "display_name": f"{branch.river_name}_{branch_topo_id}",
                "connection_node_start_id": start_node_values["id"],
                "connection_node_end_id": end_node_values["id"],
            }
            for field_name, field_value in channel_values.items():
                channel_feature.SetField(field_name, field_value)
            points_txt = ", ".join(f"{point.x} {point.y}" for point in branch_points)
            channel_geom_wkt = f"LINESTRING ({points_txt})"
            channel_geom = ogr.CreateGeometryFromWkt(channel_geom_wkt)
            channel_feature.SetGeometry(channel_geom)
            channel_layer.CreateFeature(channel_feature)
            channel_feature = None
            branch_cross_sections = xs_component.cross_section_data[branch_topo_id.upper()]
            for xs in branch_cross_sections:
                xs_feature = ogr.Feature(cross_section_layer.GetLayerDefn())
                xs_chainage = float(xs.chainage)
                xs_table = "\n".join(f"{row[0]}, {row[1]}" for row in xs.profile)

                xs_geom = channel_geom.Value(xs_chainage)
                xs_values = {
                    "id": current_xs_id,
                    "code": f"{branch_topo_id}_{xs.chainage}",
                    "channel_id": current_channel_id,
                    "friction_type": en.FrictionType.MANNING.value,
                    "cross_section_shape": en.CrossSectionShape.TABULATED_TRAPEZIUM.value,
                    "cross_section_table": xs_table,
                }
                for xs_field_name, xs_field_value in xs_values.items():
                    xs_feature.SetField(xs_field_name, xs_field_value)
                xs_feature.SetGeometry(xs_geom)
                cross_section_layer.CreateFeature(xs_feature)
                current_xs_id += 1
                xs_feature = None
        current_channel_id += 1
        for node_point_id, node_values in visited_node_values.items():
            node_feature = ogr.Feature(node_layer.GetLayerDefn())
            for field_name, field_value in node_values.items():
                node_feature.SetField(field_name, field_value)
            point = nwk_component.points[node_point_id]
            node_geom_wkt = f"POINT ({point.x} {point.y})"
            node_geom = ogr.CreateGeometryFromWkt(node_geom_wkt)
            node_feature.SetGeometry(node_geom)
            node_layer.CreateFeature(node_feature)
            node_feature = None
