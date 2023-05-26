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
    if skip_m:
        point_wkt = f"POINT ({point.x} {point.y} {point.m})"
    else:
        point_wkt = f"POINT ({point.x} {point.y} {point.m})"
    geom = ogr.CreateGeometryFromWkt(point_wkt)
    return geom


def gdal_linestring(points, skip_m=True):
    if skip_m:
        points_txt = ", ".join(f"{point.x} {point.y}" for point in points)
    else:
        points_txt = ", ".join(f"{point.x} {point.y} {point.m}" for point in points)
    linestring_wkt = f"LINESTRING ({points_txt})"
    geom = ogr.CreateGeometryFromWkt(linestring_wkt)
    return geom


def interpolate_chainage_point(branch, chainage):
    branch_geom = gdal_linestring(branch.points)
    real_chainage = chainage - float(branch.upstream_chainage)
    chainage_coefficient = branch_geom.Length() / (branch.down_chainage - branch.up_chainage)
    chainage_point_geom = branch_geom.Value(real_chainage * chainage_coefficient)
    return chainage_point_geom


def interpolate_chainage_point_bisect(branch, chainage):
    branch_points = branch.points
    branch_points_chainages = [point.m for point in branch_points]
    max_idx = len(branch_points_chainages) - 1
    idx = bisect.bisect_left(branch_points_chainages, chainage)
    up_point = branch_points[idx - 1] if idx > 0 else branch_points[0]
    down_point = branch_points[idx + 1] if idx < max_idx else branch_points[max_idx]
    segment_geom = gdal_linestring([up_point, down_point])
    segment_chainage = chainage - up_point.m
    segment_distance = segment_geom.Length()
    segment_m_distance = down_point.m - up_point.m
    segment_m_coefficient = segment_distance / segment_m_distance if segment_m_distance else 0.0
    chainage_point_geom = segment_geom.Value(segment_chainage * segment_m_coefficient)
    return chainage_point_geom
