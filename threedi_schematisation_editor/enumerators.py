# Copyright (C) 2025 by Nelen & Schuurmans
from enum import Enum, IntEnum


# define own StrEnum for easy serialization and deserialization
# this is include in python from 3.11 onwards
class StrEnum(str, Enum):
    """Enum where members are also (and must be) strings"""

    def __str__(self) -> str:
        return self.value

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return f"{self.__class__.__name__}.{self._name_}"


class GeometryType(Enum):
    NoGeometry = "NoGeometry"
    Point = "Point"
    Linestring = "LineString"
    Polygon = "Polygon"


class BoundaryType1D(IntEnum):
    WATER_LEVEL = 1
    VELOCITY = 2
    DISCHARGE = 3
    SOMMERFELD = 5
    GROUNDWATER_LEVEL = 6
    GROUNDWATER_DISCHARGE = 7


class BoundaryType2D(IntEnum):
    WATER_LEVEL = 1
    VELOCITY = 2
    SOMMERFELD = 5
    GROUNDWATER_LEVEL = 6
    DISCHARGE_TOTAL = 8
    GROUNDWATER_DISCHARGE_TOTAL = 9
    DISCHARGE_PER_FLOWLINE = 3
    GROUNDWATER_DISCHARGE_PER_FLOWLINE = 7


class Later2DType(IntEnum):
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


class ExchangeTypeChannel(IntEnum):
    EMBEDDED = 100
    ISOLATED = 101
    CONNECTED = 102
    DOUBLE_CONNECTED = 105


class ExchangeTypeCulvert(IntEnum):
    EMBEDDED = 100
    ISOLATED = 101
    CONNECTED = 102
    DOUBLE_CONNECTED = 105


class ExchangeTypeNode(IntEnum):
    EMBEDDED = 0
    ISOLATED = 1
    CONNECTED = 2


class ExchangeTypePipe(IntEnum):
    EMBEDDED = 0
    ISOLATED = 1
    CONNECTED = 2


class CrossSectionShape(IntEnum):
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


class Visualisation(IntEnum):
    MANHOLE = 0
    OUTLET = 1
    PUMP_CHAMBER = 2
    INFILTRATION_MANHOLE = 3
    GULLY = 4
    OTHER = 99


class FrictionType(IntEnum):
    CHEZY = 1
    MANNING = 2


class FrictionTypeExtended(IntEnum):
    CHEZY = 1
    MANNING = 2
    CHEZY_WITH_CONVEYANCE = 3
    MANNING_WITH_CONVEYANCE = 4


class InitializationType(IntEnum):
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


class InterflowType(IntEnum):
    NO_INTERLFOW = 0
    LOCAL_DEEPEST_POINT_SCALED_POROSITY = 1
    GLOBAL_DEEPEST_POINT_SCALED_POROSITY = 2
    LOCAL_DEEPEST_POINT_CONSTANT_POROSITY = 3
    GLOBAL_DEEPEST_POINT_CONSTANT_POROSITY = 4


class LeveeMaterial(IntEnum):
    SAND = 1
    CLAY = 2


class PipeMaterial(IntEnum):
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


class CrestType(IntEnum):
    BROAD_CRESTED = 3
    SHORT_CRESTED = 4


class SewerageType(IntEnum):
    COMBINED_SEWER = 0
    STORM_DRAIN = 1
    SANITARY_SEWER = 2
    TRANSPORT = 3
    SPILLWAY = 4
    SYPHON = 5
    STORAGE = 6
    STORAGE_AND_SETTLEMENT_TANK = 7
    INFILTRATION_DRAIN = 8
    SLOT_OR_TRENCH_DRAIN = 9
    PRESSURE_SEWER = 10


class PumpType(IntEnum):
    SUCTION_SIDE = 1
    DELIVERY_SIDE = 2


class InfiltrationSurfaceOption(IntEnum):
    WHOLE_SURFACE_WHEN_RAINING = 0
    ALWAYS_WHOLE_SURFACE = 1
    WET_SURFACE_ONLY = 2


class ZoomCategories(IntEnum):
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
    M3_SECONDS = "m3/s"  # will be displayed as m³/s


class MeasureVariable(Enum):
    WATER_LEVEL = "water_level"
    VOLUME = "volume"


class ControlType(Enum):
    TABLE = "table"
    MEMORY = "memory"


class ActionType(Enum):
    SET_DISCHARGE_COEFFICIENTS = "set_discharge_coefficients"  # not pump
    SET_CREST_LEVEL = "set_crest_level"  # orifice, weir only
    SET_PUMP_CAPACITY = "set_pump_capacity"  # only pump
    SET_GATE_LEVEL = "set_gate_level"


class TargetType(Enum):
    ORIFICE = "orifice"
    PUMP = "pump"
    WEIR = "weir"


class MeasureOperator(Enum):
    LARGER_THAN = ">"
    SMALLER_THAN = "<"


class FrictionShallowWaterDepthCorrection(IntEnum):
    OFF = 0
    MAX_BETWEEN_AVERAGE_AND_DIVIDED_CHANNEL_BASED_FRICTION = 1
    ALWAYS_LINEARIZED = 2
    LINEARIZED_DEPTH_BASED_ON_WEIGHTED_AVERAGE = 3


class TimeIntegrationMethod(IntEnum):
    EULER_IMPLICIT = 0


class LimiterSlopeCrossSectionalArea2D(IntEnum):
    OFF = 0
    HIGHER_ORDER_SCHEME = 1
    VOLUME_DIVIDED_BY_SURFACE_AREA = 2
    THIN_WATER_LAYER_APPROACH = 3


class MaxDegreeGaussSeidel(IntEnum):
    FOR_ONLY_2D_SURFACE_FLOW = 5
    FOR_1D_AND_2D_FLOW = 7
    FOR_1D_FLOW_2D_SURFACE_FLOW_AND_GROUNDWATER_FLOW = 70
    FOR_ONLY_1D_FLOW = 700


class UseNestedNewton(IntEnum):
    FOR_SCHEMATISATIONS_WITHOUT_CLOSED_CROSS_SECTIONS = 0
    FOR_SCHEMATISATIONS_WITH_CLOSED_CROSS_SECTIONS = 1


class NodeOpenWaterDetection(IntEnum):
    NODE_IS_REGARDED_AS_OPEN_WATER_IF_AT_LEAST_ONE_CHANNEL_CONNECTS_TO_IT = 0
    NODE_IS_REGARDED_AS_OPEN_WATER_IF_IT_HAS_NO_STORAGE_AREA_FOR_BACKWARDS_COMPATIBILITY_ONLY = 1


class UseAdvection1D(IntEnum):
    NO_1D_ADVECTION = 0
    MOMENTUM_CONSERVATIVE_SCHEME = 1
    ENERGY_CONSERVATIVE_SCHEME = 2
    COMBINED_MOMENTUM_AND_ENERGY_CONSERVATIVE_SCHEME = 3


class CrossSectionDataTargetType(StrEnum):
    CULVERT = "culvert"
    CROSS_SECTION_LOCATION = "cross-section location"
    ORIFICE = "orifice"
    PIPE = "pipe"
    WEIR = "weir"
