# Copyright (C) 2023 by Lutra Consulting
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
