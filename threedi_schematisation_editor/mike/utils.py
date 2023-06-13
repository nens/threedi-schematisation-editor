# Copyright (C) 2023 by Lutra Consulting
import bisect
from enum import Enum

from osgeo import ogr

from threedi_schematisation_editor.enumerators import GeometryType
from threedi_schematisation_editor.utils import enum_type, is_optional, optional_type

gdal_field_types_mapping = {
    bool: ogr.OFSTBoolean,
    int: ogr.OFTInteger,
    float: ogr.OFTReal,
    str: ogr.OFTString,
}

gdal_geometry_types_mapping = {
    GeometryType.NoGeometry: ogr.wkbNone,
    GeometryType.Point: ogr.wkbPoint,
    GeometryType.Linestring: ogr.wkbLineString,
    GeometryType.Polygon: ogr.wkbPolygon,
}


class ResistanceTypes(Enum):
    """MIKE resistance types."""

    RELATIVE = 0
    MANNING_N = 1
    MANNING_M = 2
    CHEZY = 3
    DARCY_WEISBACH = 4


def create_data_model_layer(annotated_model_cls, dataset, crs):
    """Function that creates GDAL layer based on annotated data model class."""
    geometry_type = gdal_geometry_types_mapping[annotated_model_cls.__geometrytype__]
    layer_name = annotated_model_cls.__tablename__
    layer = dataset.CreateLayer(layer_name, crs, geometry_type)

    for field_name, field_type in annotated_model_cls.__annotations__.items():
        if is_optional(field_type):
            field_type = optional_type(field_type)
        if issubclass(field_type, Enum):
            field_type = enum_type(field_type)
        gdal_field_type = gdal_field_types_mapping[field_type]
        if gdal_field_type == ogr.OFSTBoolean:
            field_definition = ogr.FieldDefn(field_name, ogr.OFTInteger)
            field_definition.SetSubType(gdal_field_type)
        else:
            field_definition = ogr.FieldDefn(field_name, gdal_field_type)
        layer.CreateField(field_definition)


def gdal_point(point, skip_m=True):
    """Create OGR point geometry."""
    if skip_m:
        point_wkt = f"POINT ({point.x} {point.y} {point.m})"
    else:
        point_wkt = f"POINT ({point.x} {point.y} {point.m})"
    geom = ogr.CreateGeometryFromWkt(point_wkt)
    return geom


def gdal_linestring(points, skip_m=True):
    """Create OGR LineString geometry."""
    if skip_m:
        points_txt = ", ".join(f"{point.x} {point.y}" for point in points)
    else:
        points_txt = ", ".join(f"{point.x} {point.y} {point.m}" for point in points)
    linestring_wkt = f"LINESTRING ({points_txt})"
    geom = ogr.CreateGeometryFromWkt(linestring_wkt)
    return geom


def interpolate_chainage_point(branch, chainage):
    """Interpolate MIKE11 branch chainage point."""
    branch_points = branch.points
    branch_points_chainages = [point.m for point in branch_points]
    idx = bisect.bisect_left(branch_points_chainages, chainage)
    up_point = branch_points[idx - 1]
    down_point = branch_points[idx]
    segment_geom = gdal_linestring([up_point, down_point])
    segment_chainage = chainage - up_point.m
    segment_length = segment_geom.Length()
    segment_chainage_distance = down_point.m - up_point.m
    chainage_to_length_coefficient = segment_length / segment_chainage_distance
    chainage_point_geom = segment_geom.Value(segment_chainage * chainage_to_length_coefficient)
    return chainage_point_geom
