# Copyright (C) 2025 by Lutra Consulting
from enum import Enum


class GeometryType(Enum):
    NoGeometry = "NoGeometry"
    Point = "Point"
    Linestring = "LineString"
    Polygon = "Polygon"


class BoundaryType(Enum):
    WATER_LEVEL = 1
    VELOCITY = 2
    DISCHARGE = 3
    SOMMERFELD = 5
    GROUNDWATER_LEVEL = 6
    GROUNDWATER_DISCHARGE = 7


class Later2DType(Enum):
    SURFACE = 1


class FlowVariable(Enum):
    DISCHARGE = "discharge"
    FLOW_VELOCITY = "flow_velocity"
    PUMP_DISCHARGE = "pump_discharge"
    RAIN = "rain"
    WATER_LEVEL = "water_level"
    WET_CROSS_SECTIONAL_AREA = "wet_cross_section"
    WET_SURFACE_AREA = "wet_surface"
    LATERAL_DISCHARGE = "lateral_discharge"
    VOLUME = "volume"
    SIMPLE_INFILTRATION = "simple_infiltration"
    LEAKAGE = "leakage"
    INTERCEPTION = "interception"
    SURFACE_SOURCES_AND_SINKS_DISCHARGE = "surface_source_sink_discharge"


class AggregationMethod(Enum):
    AVERAGE = "avg"
    MINIMUM = "min"
    MAXIMUM = "max"
    CUMULATIVE = "cum"
    MEDIAN = "med"
    CUMULATIVE_NEGATIVE = "cum_negative"
    CUMULATIVE_POSITIVE = "cum_positive"
    CURRENT = "current"


class ExchangeTypeChannel(Enum):
    EMBEDDED = 100
    ISOLATED = 101
    CONNECTED = 102
    DOUBLE_CONNECTED = 105


class ExchangeTypeCulvert(Enum):
    EMBEDDED = 100
    ISOLATED = 101
    CONNECTED = 102
    DOUBLE_CONNECTED = 105


class ExchangeTypeNode(Enum):
    EMBEDDED = 0
    ISOLATED = 1
    CONNECTED = 2


class ExchangeTypePipe(Enum):
    EMBEDDED = 0
    ISOLATED = 1
    CONNECTED = 2


class CrossSectionShape(Enum):
    CLOSED_RECTANGLE = 0
    OPEN_RECTANGLE = 1
    CIRCLE = 2
    EGG = 3
    TABULATED_RECTANGLE = 5
    TABULATED_TRAPEZIUM = 6
    YZ = 7
    INVERTED_EGG = 8


class ManholeShape(Enum):
    SQUARE = "00"
    ROUND = "01"
    RECTANGLE = "02"


class Visualisation(Enum):
    INSPECTION = 0
    OUTLET = 1
    PUMP = 2
    OTHER = 99


class FrictionType(Enum):
    CHEZY = 1
    MANNING = 2


class FrictionTypeExtended(Enum):
    CHEZY = 1
    MANNING = 2
    CHEZY_WITH_CONVEYANCE = 3
    MANNING_WITH_CONVEYANCE = 4


class InitializationType(Enum):
    MAX = 0
    MIN = 1
    AVERAGE = 2


class SurfaceInclinationType(Enum):
    VLAK = "vlak"
    HELLEND = "hellend"
    UITGESTREKT = "uitgestrekt"


class SurfaceClass(Enum):
    GESLOTEN_VERHARDING = "gesloten verharding"
    OPEN_VERHARDING = "open verharding"
    HALF_VERHARD = "half verhard"
    ONVERHARD = "onverhard"
    PAND = "pand"


class InterflowType(Enum):
    NO_INTERLFOW = 0
    LOCAL_DEEPEST_POINT_SCALED_POROSITY = 1
    GLOBAL_DEEPEST_POINT_SCALED_POROSITY = 2
    LOCAL_DEEPEST_POINT_CONSTANT_POROSITY = 3
    GLOBAL_DEEPEST_POINT_CONSTANT_POROSITY = 4


class LeveeMaterial(Enum):
    SAND = 1
    CLAY = 2


class PipeMaterial(Enum):
    CONCRETE = 0
    PVC = 1
    GRES = 2
    CAST_IRON = 3
    BRICKWORK = 4
    HPE = 5
    HDPE = 6
    PLATE_IRON = 7
    STEEL = 8
    STONEWARE = 9
    SHEET_IRON = 10


class CrestType(Enum):
    BROAD_CRESTED = 3
    SHORT_CRESTED = 4


class SewerageType(Enum):
    COMBINED_SEWER = 0
    STORM_DRAIN = 1
    SANITARY_SEWER = 2
    TRANSPORT = 3
    SPILLWAY = 4
    SYPHON = 5
    STORAGE = 6
    STORAGE_AND_SETTLEMENT_TANK = 7


class PumpType(Enum):
    SUCTION_SIDE = 1
    DELIVERY_SIDE = 2


class InfiltrationSurfaceOption(Enum):
    WHOLE_SURFACE_WHEN_RAINING = 0
    ALWAYS_WHOLE_SURFACE = 1
    WET_SURFACE_ONLY = 2


class ZoomCategories(Enum):
    # Visibility in live-site: 0 is lowest for smallest level (i.e. ditch)
    # and 5 for highest (rivers).
    LOWEST_VISIBILITY = 0
    LOW_VISIBILITY = 1
    MEDIUM_LOW_VISIBILITY = 2
    MEDIUM_VISIBILITY = 3
    HIGH_VISIBILITY = 4
    HIGHEST_VISIBILITY = 5


class TimeUnit(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"


class Unit(Enum):
    M3_SECONDS = "m3/s"


class MeasureVariable(Enum):
    WATER_LEVEL = "water_level"
    VOLUME = "volume"


class ControlType(Enum):
    TABLE = "table"
    MEMORY = "memory"
