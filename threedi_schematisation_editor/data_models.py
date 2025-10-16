# Copyright (C) 2025 by Lutra Consulting
import re
from dataclasses import dataclass, field, fields
from itertools import chain
from types import MappingProxyType, SimpleNamespace
from typing import Optional

from threedi_schematisation_editor.enumerators import (
    ActionType,
    AggregationMethod,
    BoundaryType1D,
    BoundaryType2D,
    ControlType,
    CrestType,
    CrossSectionShape,
    ExchangeTypeChannel,
    ExchangeTypeCulvert,
    ExchangeTypeNode,
    ExchangeTypePipe,
    FlowVariable,
    FrictionShallowWaterDepthCorrection,
    FrictionType,
    FrictionTypeExtended,
    GeometryType,
    InfiltrationSurfaceOption,
    InitializationType,
    InterflowType,
    Later2DType,
    LimiterSlopeCrossSectionalArea2D,
    MaxDegreeGaussSeidel,
    MeasureOperator,
    MeasureVariable,
    NodeOpenWaterDetection,
    PipeMaterial,
    PumpType,
    SewerageType,
    TargetType,
    TimeIntegrationMethod,
    TimeUnit,
    Unit,
    UseAdvection1D,
    UseNestedNewton,
    Visualisation,
)

DISPLAY_NAME_FIELD = "display_name"
DISPLAY_UNIT_FIELD = "display_unit"
METHODS_FIELD = "methods"


class HighPrecisionFloat(float):
    """
    Used to set the widget type for a field to TextEdit
    so users can fill in any number of decimals and use scientific notation
    """

    pass


@dataclass
class ModelObject:
    __tablename__ = None
    __layername__ = None
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = tuple()

    @classmethod
    def fields_namespace(cls) -> SimpleNamespace:
        field_names_dict = {k: k for k in cls.__annotations__.keys()}
        namespace = SimpleNamespace(**field_names_dict)
        return namespace

    @staticmethod
    def default_display_name(display_name):
        REPLACEMENTS = [
            (r"\bcross section\b", "cross-section"),
            (r"\btags\b", "tag"),
        ]
        for pattern, replacement in REPLACEMENTS:
            display_name = re.sub(
                pattern, replacement, display_name, flags=re.IGNORECASE
            )
        display_name = display_name.replace("_", " ").capitalize()
        # replace ID after capitalization so ID won't become Id
        display_name = re.sub(r"\bid\b", "ID", display_name, flags=re.IGNORECASE)
        return display_name

    @classmethod
    def display_names(cls) -> list:
        display_names = []
        for field in fields(cls):
            display_name = field.metadata.get(
                DISPLAY_NAME_FIELD, cls.default_display_name(field.name)
            )
            if DISPLAY_UNIT_FIELD in field.metadata:
                display_name += f" [{field.metadata[DISPLAY_UNIT_FIELD]}]"
            display_names.append(display_name)
        return display_names

    @classmethod
    def fields_display_names(cls) -> dict:
        display_names_mapping = {
            field_name: display_name
            for field_name, display_name in zip(
                cls.__annotations__.keys(), cls.display_names()
            )
        }
        return display_names_mapping

    @staticmethod
    def obsolete_fields() -> set:
        return set()

    @classmethod
    def hidden_fields(cls) -> set:
        return set()


@dataclass
class ConnectionNode(ModelObject):
    __tablename__ = "connection_node"
    __layername__ = "Connection node"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    storage_area: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "m²"})
    initial_water_level: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "m"})
    visualisation: Optional[Visualisation]
    manhole_surface_level: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "m MSL"}
    )
    bottom_level: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "m MSL"})
    exchange_level: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "m MSL"})
    exchange_type: Optional[ExchangeTypeNode]
    exchange_thickness: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "m"})
    hydraulic_conductivity_in: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "m/d"}
    )
    hydraulic_conductivity_out: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "m/d"}
    )
    tags: Optional[str]


@dataclass
class Material(ModelObject):
    __tablename__ = "material"
    __layername__ = "Material"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    description: str
    friction_coefficient: float
    friction_type: FrictionType


@dataclass
class BoundaryCondition1D(ModelObject):
    __tablename__ = "boundary_condition_1d"
    __layername__ = "1D Boundary condition"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    type: BoundaryType1D
    connection_node_id: int
    timeseries: str
    time_units: TimeUnit
    interpolate: bool
    tags: Optional[str]


@dataclass
class Lateral1D(ModelObject):
    __tablename__ = "lateral_1d"
    __layername__ = "1D Lateral"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    time_units: TimeUnit
    interpolate: bool
    offset: int
    units: Unit
    connection_node_id: int
    timeseries: str
    tags: Optional[str]


@dataclass
class Pump(ModelObject):
    __tablename__ = "pump"
    __layername__ = "Pump"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    start_level: float
    lower_stop_level: float
    upper_stop_level: Optional[float]
    capacity: float
    type: PumpType
    sewerage: Optional[bool]
    connection_node_id: int
    tags: Optional[str]


@dataclass
class PumpMap(ModelObject):
    __tablename__ = "pump_map"
    __layername__ = "Pump map"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    pump_id: int
    connection_node_id_end: int
    tags: Optional[str]


@dataclass
class Weir(ModelObject):
    __tablename__ = "weir"
    __layername__ = "Weir"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    crest_level: float
    crest_type: CrestType
    discharge_coefficient_positive: Optional[float]
    discharge_coefficient_negative: Optional[float]
    material_id: Optional[int]
    friction_value: float
    friction_type: FrictionType
    sewerage: bool
    external: Optional[bool]
    connection_node_id_start: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node start ID"}
    )
    connection_node_id_end: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node end ID"}
    )
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_table: Optional[str]
    tags: Optional[str]


@dataclass
class Culvert(ModelObject):
    __tablename__ = "culvert"
    __layername__ = "Culvert"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    exchange_type: Optional[ExchangeTypeCulvert]
    calculation_point_distance: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m]"}
    )
    invert_level_start: float
    invert_level_end: float
    discharge_coefficient_positive: Optional[float]
    discharge_coefficient_negative: Optional[float]
    material_id: Optional[int]
    friction_value: float
    friction_type: FrictionType
    connection_node_id_start: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node start ID"}
    )
    connection_node_id_end: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node end ID"}
    )
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_table: Optional[str]
    tags: Optional[str]


@dataclass
class Orifice(ModelObject):
    __tablename__ = "orifice"
    __layername__ = "Orifice"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    crest_level: float
    crest_type: CrestType
    discharge_coefficient_positive: Optional[float]
    discharge_coefficient_negative: Optional[float]
    material_id: Optional[int]
    friction_value: float
    friction_type: FrictionType
    sewerage: bool
    connection_node_id_start: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node start ID"}
    )
    connection_node_id_end: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node end ID"}
    )
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_table: Optional[str]
    tags: Optional[str]


@dataclass
class Pipe(ModelObject):
    __tablename__ = "pipe"
    __layername__ = "Pipe"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    exchange_type: ExchangeTypePipe
    calculation_point_distance: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m]"}
    )
    invert_level_start: float
    invert_level_end: float
    material_id: Optional[int]
    friction_value: float
    friction_type: FrictionType
    sewerage_type: Optional[SewerageType]
    connection_node_id_start: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node start ID"}
    )
    connection_node_id_end: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node end ID"}
    )
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_table: Optional[str]
    exchange_thickness: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    hydraulic_conductivity_in: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m/d]"}
    )
    hydraulic_conductivity_out: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m/d]"}
    )
    tags: Optional[str]


@dataclass
class CrossSectionLocation(ModelObject):
    __tablename__ = "cross_section_location"
    __layername__ = "Cross section location"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    reference_level: float
    friction_type: FrictionTypeExtended
    friction_value: float
    bank_level: Optional[float]
    channel_id: int
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_table: Optional[str]
    cross_section_friction_values: Optional[str]
    cross_section_vegetation_table: Optional[str]
    vegetation_stem_density: Optional[float]
    vegetation_stem_diameter: Optional[float]
    vegetation_height: Optional[float]
    vegetation_drag_coefficient: Optional[float]
    tags: Optional[str]


@dataclass
class CrossSectionData(ModelObject):
    """Data class for cross section data import. This class does NOT match a class in threedi-schema!"""

    __tablename__ = "Cross section data"
    __layername__ = "Cross section data"
    __geometrytype__ = None

    target_object_type: str
    target_object_id: int
    target_object_code: str
    order_by: float
    cross_section_shape: CrossSectionShape
    cross_section_width: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_height: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_y: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    cross_section_z: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})


@dataclass
class Channel(ModelObject):
    __tablename__ = "channel"
    __layername__ = "Channel"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    exchange_type: ExchangeTypeChannel
    calculation_point_distance: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m]"}
    )
    connection_node_id_start: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node start ID"}
    )
    connection_node_id_end: int = field(
        metadata={DISPLAY_NAME_FIELD: "Connection node end ID"}
    )
    exchange_thickness: Optional[float] = field(metadata={DISPLAY_UNIT_FIELD: "[m]"})
    hydraulic_conductivity_in: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m/d]"}
    )
    hydraulic_conductivity_out: Optional[float] = field(
        metadata={DISPLAY_UNIT_FIELD: "[m/d]"}
    )
    tags: Optional[str]


@dataclass
class BoundaryCondition2D(ModelObject):
    __tablename__ = "boundary_condition_2d"
    __layername__ = "2D Boundary condition"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    type: BoundaryType2D
    timeseries: str
    time_units: TimeUnit
    interpolate: bool
    tags: Optional[str]


@dataclass
class Lateral2D(ModelObject):
    __tablename__ = "lateral_2d"
    __layername__ = "2D Lateral"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    type: Later2DType
    time_units: TimeUnit
    interpolate: bool
    offset: int
    units: Unit
    timeseries: str
    tags: Optional[str]


@dataclass
class Obstacle(ModelObject):
    __tablename__ = "obstacle"
    __layername__ = "Obstacle"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    crest_level: float
    affects_2d: bool
    affects_1d2d_open_water: bool
    affects_1d2d_closed: bool
    tags: Optional[str]


@dataclass
class GridRefinementLine(ModelObject):
    __tablename__ = "grid_refinement_line"
    __layername__ = "Grid refinement line"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    grid_level: int
    tags: Optional[str]


@dataclass
class GridRefinementArea(ModelObject):
    __tablename__ = "grid_refinement_area"
    __layername__ = "Grid refinement area"
    __geometrytype__ = GeometryType.Polygon

    id: int
    code: Optional[str]
    display_name: Optional[str]
    grid_level: int
    tags: Optional[str]


@dataclass
class DEMAverageArea(ModelObject):
    __tablename__ = "dem_average_area"
    __layername__ = "DEM average area"
    __geometrytype__ = GeometryType.Polygon

    id: int
    code: Optional[str]
    display_name: Optional[str]
    tags: Optional[str]


@dataclass
class Windshielding1D(ModelObject):
    __tablename__ = "windshielding_1d"
    __layername__ = "1D Wind shielding"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    north: Optional[float]
    northeast: Optional[float]
    east: Optional[float]
    southeast: Optional[float]
    south: Optional[float]
    southwest: Optional[float]
    west: Optional[float]
    northwest: Optional[float]
    channel_id: int
    tags: Optional[str]


@dataclass
class PotentialBreach(ModelObject):
    __tablename__ = "potential_breach"
    __layername__ = "Potential breach"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    channel_id: int
    initial_exchange_level: float
    final_exchange_level: Optional[float]
    levee_material: Optional[Material]
    tags: Optional[str]


@dataclass
class ExchangeLine(ModelObject):
    __tablename__ = "exchange_line"
    __layername__ = "Exchange line"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    channel_id: int
    exchange_level: Optional[float]
    tags: Optional[str]


@dataclass
class Surface(ModelObject):
    __tablename__ = "surface"
    __layername__ = "Surface"
    __geometrytype__ = GeometryType.Polygon

    id: int
    code: Optional[str]
    display_name: Optional[str]
    area: float
    surface_parameters_id: int
    tags: Optional[str]


@dataclass
class SurfaceMap(ModelObject):
    __tablename__ = "surface_map"
    __layername__ = "Surface map"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    percentage: float
    surface_id: int
    connection_node_id: int
    tags: Optional[str]


@dataclass
class SurfaceParameters(ModelObject):
    __tablename__ = "surface_parameters"
    __layername__ = "Surface parameters"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    description: str
    outflow_delay: float
    surface_layer_thickness: float
    infiltration: bool
    max_infiltration_capacity: float
    min_infiltration_capacity: float
    infiltration_decay_constant: float
    infiltration_recovery_constant: float
    tags: Optional[str]


@dataclass
class DryWeatherFlow(ModelObject):
    __tablename__ = "dry_weather_flow"
    __layername__ = "Dry weather flow"
    __geometrytype__ = GeometryType.Polygon

    id: int
    code: Optional[str]
    display_name: Optional[str]
    multiplier: float
    daily_total: float
    interpolate: bool
    dry_weather_flow_distribution_id: int
    tags: Optional[str]


@dataclass
class DryWeatherFlowMap(ModelObject):
    __tablename__ = "dry_weather_flow_map"
    __layername__ = "Dry weather flow map"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    percentage: float
    dry_weather_flow_id: int
    connection_node_id: int
    tags: Optional[str]


@dataclass
class DryWeatherFlowDistribution(ModelObject):
    __tablename__ = "dry_weather_flow_distribution"
    __layername__ = "Dry weather flow distribution"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    description: str
    distribution: str
    tags: Optional[str]


@dataclass
class ModelSettings(ModelObject):
    __tablename__ = "model_settings"
    __layername__ = "Model settings"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("dem_file", "Digital elevation model [m MSL]"),
        ("friction_coefficient_file", "Friction coefficient [-]"),
    )

    id: int
    use_2d_flow: bool
    use_1d_flow: bool
    manhole_aboveground_storage_area: Optional[float]
    minimum_cell_size: float
    calculation_point_distance_1d: float
    nr_grid_levels: int
    node_open_water_detection: NodeOpenWaterDetection
    minimum_table_step_size: float
    dem_file: Optional[str]
    friction_type: Optional[FrictionType]
    friction_coefficient: float
    friction_coefficient_file: Optional[str]
    embedded_cutoff_threshold: Optional[float]
    epsg_code: Optional[int]
    max_angle_1d_advection: Optional[HighPrecisionFloat]
    friction_averaging: Optional[bool]
    table_step_size_1d: Optional[float]
    use_2d_rain: bool
    use_interflow: bool
    use_simple_infiltration: bool
    use_groundwater_flow: bool
    use_groundwater_storage: bool
    use_interception: bool
    maximum_table_step_size: Optional[float]
    use_vegetation_drag_2d: Optional[bool]


@dataclass
class InitialConditionsSettings(ModelObject):
    __tablename__ = "initial_conditions"
    __layername__ = "Initial conditions"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("initial_groundwater_level_file", "Initial groundwater level [m MSL]"),
        ("initial_water_level_file", "Initial water level [m MSL]"),
    )

    id: int
    initial_water_level: Optional[float]
    initial_water_level_file: Optional[str]
    initial_groundwater_level: Optional[float]
    initial_groundwater_level_file: Optional[str]
    initial_groundwater_level_aggregation: Optional[InitializationType]


@dataclass
class InterceptionSettings(ModelObject):
    __tablename__ = "interception"
    __layername__ = "Interception"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (("interception_file", "Interception [m]"),)

    id: int
    interception: Optional[float]
    interception_file: Optional[str]


@dataclass
class AggregationSettings(ModelObject):
    __tablename__ = "aggregation_settings"
    __layername__ = "Aggregation settings"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    flow_variable: FlowVariable
    aggregation_method: AggregationMethod
    interval: int


@dataclass
class SimpleInfiltrationSettings(ModelObject):
    __tablename__ = "simple_infiltration"
    __layername__ = "Simple infiltration"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("infiltration_rate_file", "Infiltration rate [mm/d]"),
        ("max_infiltration_volume_file", "Max infiltration volume [m]"),
    )

    id: int
    infiltration_rate: Optional[float]
    infiltration_rate_file: Optional[str]
    infiltration_surface_option: Optional[InfiltrationSurfaceOption]
    max_infiltration_volume_file: Optional[str]
    max_infiltration_volume: Optional[float]


@dataclass
class GroundWaterSettings(ModelObject):
    __tablename__ = "groundwater"
    __layername__ = "Groundwater"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("equilibrium_infiltration_rate_file", "Equilibrium infiltration rate [mm/d]"),
        ("groundwater_hydraulic_conductivity_file", "Hydraulic conductivity [m/day]"),
        ("groundwater_impervious_layer_level_file", "Impervious layer level [m MSL]"),
        ("infiltration_decay_period_file", "Infiltration decay period [d]"),
        ("initial_infiltration_rate_file", "Initial infiltration rate [mm/d]"),
        ("leakage_file", "Leakage [mm/d]"),
        ("phreatic_storage_capacity_file", "Phreatic storage capacity [-]"),
    )

    id: int
    groundwater_impervious_layer_level: Optional[float]
    groundwater_impervious_layer_level_file: Optional[str]
    groundwater_impervious_layer_level_aggregation: Optional[InitializationType]
    phreatic_storage_capacity: Optional[float]
    phreatic_storage_capacity_file: Optional[str]
    phreatic_storage_capacity_aggregation: Optional[InitializationType]
    equilibrium_infiltration_rate: Optional[float]
    equilibrium_infiltration_rate_file: Optional[str]
    equilibrium_infiltration_rate_aggregation: Optional[InitializationType]
    initial_infiltration_rate: Optional[float]
    initial_infiltration_rate_file: Optional[str]
    initial_infiltration_rate_aggregation: Optional[InitializationType]
    infiltration_decay_period: Optional[float]
    infiltration_decay_period_file: Optional[str]
    infiltration_decay_period_aggregation: Optional[InitializationType]
    groundwater_hydraulic_conductivity: Optional[float]
    groundwater_hydraulic_conductivity_file: Optional[str]
    groundwater_hydraulic_conductivity_aggregation: Optional[InitializationType]
    leakage: Optional[float]
    leakage_file: Optional[str]


@dataclass
class InterflowSettings(ModelObject):
    __tablename__ = "interflow"
    __layername__ = "Interflow"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("hydraulic_conductivity_file", "Hydraulic conductivity [m/d]"),
        ("porosity_file", "Porosity [-]"),
    )

    id: int
    interflow_type: InterflowType
    porosity: Optional[float]
    porosity_file: Optional[str]
    porosity_layer_thickness: Optional[float]
    impervious_layer_elevation: Optional[float]
    hydraulic_conductivity: Optional[float]
    hydraulic_conductivity_file: Optional[str]


@dataclass
class NumericalSettings(ModelObject):
    __tablename__ = "numerical_settings"
    __layername__ = "Numerical settings"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    cfl_strictness_factor_1d: Optional[float]
    cfl_strictness_factor_2d: Optional[float]
    convergence_cg: Optional[HighPrecisionFloat]
    convergence_eps: Optional[HighPrecisionFloat]
    flow_direction_threshold: Optional[HighPrecisionFloat]
    friction_shallow_water_depth_correction: Optional[
        FrictionShallowWaterDepthCorrection
    ]
    general_numerical_threshold: Optional[HighPrecisionFloat]
    time_integration_method: Optional[TimeIntegrationMethod]
    limiter_waterlevel_gradient_1d: Optional[bool]
    limiter_waterlevel_gradient_2d: Optional[bool]
    limiter_slope_crossectional_area_2d: Optional[LimiterSlopeCrossSectionalArea2D]
    limiter_slope_friction_2d: Optional[bool]
    max_non_linear_newton_iterations: Optional[int]
    max_degree_gauss_seidel: Optional[MaxDegreeGaussSeidel]
    min_friction_velocity: Optional[HighPrecisionFloat]
    min_surface_area: Optional[HighPrecisionFloat]
    use_preconditioner_cg: Optional[bool]
    preissmann_slot: Optional[HighPrecisionFloat]
    pump_implicit_ratio: Optional[float]
    limiter_slope_thin_water_layer: Optional[float]
    use_of_cg: int
    use_nested_newton: Optional[UseNestedNewton]


@dataclass
class PhysicalSettings(ModelObject):
    __tablename__ = "physical_settings"
    __layername__ = "Physical settings"
    __geometrytype__ = GeometryType.NoGeometry

    use_advection_1d: UseAdvection1D
    use_advection_2d: bool


@dataclass
class SimulationTemplateSettings(ModelObject):
    __tablename__ = "simulation_template_settings"
    __layername__ = "Simulation template settings"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    name: str
    use_0d_inflow: bool
    use_structure_control: bool


@dataclass
class TimeStepSettings(ModelObject):
    __tablename__ = "time_step_settings"
    __layername__ = "Time step settings"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    max_time_step: Optional[float]
    min_time_step: Optional[float]
    output_time_step: Optional[float]
    time_step: Optional[float]
    use_time_step_stretch: Optional[bool]


@dataclass
class Tag(ModelObject):
    __tablename__ = "tags"
    __layername__ = "Tag"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    description: str


@dataclass
class CrossSectionDefinition(ModelObject):
    __tablename__ = "cross_section_definition"
    __layername__ = "Cross section definition"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    code: str
    width: Optional[str]
    height: Optional[str]
    shape: Optional[CrossSectionShape]
    friction_values: Optional[str]
    vegetation_stem_densities: Optional[str]
    vegetation_stem_diameters: Optional[str]
    vegetation_heights: Optional[str]
    vegetation_drag_coefficients: Optional[str]


@dataclass
class MeasureLocation(ModelObject):
    __tablename__ = "measure_location"
    __layername__ = "Measure location"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    measure_variable: MeasureVariable
    connection_node_id: int
    tags: Optional[str]


@dataclass
class MeasureMap(ModelObject):
    __tablename__ = "measure_map"
    __layername__ = "Measure map"
    __geometrytype__ = GeometryType.Linestring

    id: int
    code: Optional[str]
    display_name: Optional[str]
    weight: float
    measure_location_id: int
    control_id: int
    control_type: ControlType
    tags: Optional[str]


@dataclass
class MemoryControl(ModelObject):
    __tablename__ = "memory_control"
    __layername__ = "Memory control"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    action_type: ActionType
    action_value_1: float
    action_value_2: Optional[float]
    is_inverse: bool
    is_active: bool
    lower_threshold: float
    upper_threshold: float
    target_type: TargetType
    target_id: int
    tags: Optional[str]


@dataclass
class TableControl(ModelObject):
    __tablename__ = "table_control"
    __layername__ = "Table control"
    __geometrytype__ = GeometryType.Point

    id: int
    code: Optional[str]
    display_name: Optional[str]
    action_type: ActionType
    action_table: str
    target_type: TargetType
    target_id: int
    measure_operator: MeasureOperator
    tags: Optional[str]


@dataclass
class VegetationDrag2D(ModelObject):
    __tablename__ = "vegetation_drag_2d"
    __layername__ = "2D Vegetation drag"
    __geometrytype__ = GeometryType.NoGeometry

    RELATED_RASTERS = (
        ("vegetation_height_file", "Vegetation height [m]"),
        ("vegetation_stem_count_file", "Vegetation stem count [-]"),
        ("vegetation_stem_diameter_file", "Vegetation stem diameter [m]"),
        ("vegetation_drag_coefficient_file", "Vegetation drag coefficient [-]"),
    )

    id: int
    vegetation_height: Optional[float]
    vegetation_height_file: Optional[str]
    vegetation_stem_count: Optional[float]
    vegetation_stem_count_file: Optional[str]
    vegetation_stem_diameter: Optional[float]
    vegetation_stem_diameter_file: Optional[str]
    vegetation_drag_coefficient: Optional[float]
    vegetation_drag_coefficient_file: Optional[str]


MODEL_1D_ELEMENTS = (
    BoundaryCondition1D,
    ConnectionNode,
    Pipe,
    Culvert,
    Weir,
    Orifice,
    Pump,
    PumpMap,
    CrossSectionLocation,
    Windshielding1D,
    Channel,
    Material,
)
MODEL_1D2D_ELEMENTS = (
    PotentialBreach,
    ExchangeLine,
)
MODEL_2D_ELEMENTS = (
    BoundaryCondition2D,
    Obstacle,
    GridRefinementArea,
    GridRefinementLine,
    DEMAverageArea,
)
MODEL_0D_INFLOW_ELEMENTS = (
    Lateral1D,
    Lateral2D,
    DryWeatherFlowMap,
    DryWeatherFlow,
    DryWeatherFlowDistribution,
    SurfaceMap,
    Surface,
    SurfaceParameters,
)
STRUCTURE_CONTROL_ELEMENTS = (
    MeasureLocation,
    MemoryControl,
    TableControl,
    MeasureMap,
)
HYDROLOGICAL_PROCESSES = (
    InitialConditionsSettings,
    InterceptionSettings,
    InterflowSettings,
    GroundWaterSettings,
    SimpleInfiltrationSettings,
    VegetationDrag2D,
)
SETTINGS_ELEMENTS = (
    ModelSettings,
    AggregationSettings,
    NumericalSettings,
    PhysicalSettings,
    SimulationTemplateSettings,
    TimeStepSettings,
    Tag,
)
HIDDEN_ELEMENTS = tuple()
ALL_MODELS = (
    MODEL_1D_ELEMENTS
    + MODEL_1D2D_ELEMENTS
    + MODEL_2D_ELEMENTS
    + MODEL_0D_INFLOW_ELEMENTS
    + STRUCTURE_CONTROL_ELEMENTS
    + HYDROLOGICAL_PROCESSES
    + SETTINGS_ELEMENTS
)
ALL_MODELS = ALL_MODELS + (CrossSectionDefinition,)
ALL_MODELS = ALL_MODELS + HIDDEN_ELEMENTS
ELEMENTS_WITH_XS_DEF = (
    Weir,
    Culvert,
    Orifice,
    Pipe,
    CrossSectionLocation,
)
ELEMENTS_WITH_TIMESERIES = (
    BoundaryCondition1D,
    Lateral1D,
    BoundaryCondition2D,
    Lateral2D,
)

ELEMENTS_WITH_RASTERS = tuple(
    model_cls
    for model_cls in chain(SETTINGS_ELEMENTS, HYDROLOGICAL_PROCESSES)
    if model_cls.RELATED_RASTERS
)

TABLE_MANNING = MappingProxyType(
    {
        PipeMaterial.CONCRETE: 0.0145,
        PipeMaterial.PVC: 0.0110,
        PipeMaterial.STONEWARE: 0.0115,
        PipeMaterial.CAST_IRON: 0.0135,
        PipeMaterial.BRICKWORK: 0.0160,
        PipeMaterial.HPE: 0.0110,
        PipeMaterial.HDPE: 0.0110,
        PipeMaterial.SHEET_IRON: 0.0135,
        PipeMaterial.STEEL: 0.0130,
    }
)

ALL_SHAPES = {e.value for e in CrossSectionShape}
NON_TABLE_SHAPES = {
    CrossSectionShape.CLOSED_RECTANGLE.value,
    CrossSectionShape.OPEN_RECTANGLE.value,
    CrossSectionShape.CIRCLE.value,
    CrossSectionShape.EGG.value,
    CrossSectionShape.INVERTED_EGG.value,
}
TABLE_SHAPES = {
    CrossSectionShape.TABULATED_RECTANGLE.value,
    CrossSectionShape.TABULATED_TRAPEZIUM.value,
    CrossSectionShape.YZ.value,
}

MODEL_DEPENDENCIES = MappingProxyType(
    {
        ConnectionNode: {
            BoundaryCondition1D: ("connection_node_id",),
            Lateral1D: ("connection_node_id",),
            Channel: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            Culvert: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            DryWeatherFlowMap: ("connection_node_id",),
            SurfaceMap: ("connection_node_id",),
            Orifice: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            Pipe: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            Weir: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            PumpMap: (
                "connection_node_id_start",
                "connection_node_id_end",
            ),
            Pump: ("connection_node_id",),
            MeasureLocation: ("connection_node_id",),
        },
        Channel: {
            CrossSectionLocation: ("channel_id",),
            Windshielding1D: ("channel_id",),
            PotentialBreach: ("channel_id",),
            ExchangeLine: ("channel_id",),
        },
        DryWeatherFlow: {
            DryWeatherFlowMap: ("dry_weather_flow_id",),
        },
        Surface: {
            SurfaceMap: ("surface_id",),
        },
        Pump: {
            PumpMap: ("pump_id",),
            MemoryControl: (("target_id", "target_type"),),
            TableControl: (("target_id", "target_type"),),
        },
        SurfaceParameters: {
            Surface: ("surface_parameters_id",),
        },
        DryWeatherFlowDistribution: {
            DryWeatherFlow: ("dry_weather_flow_distribution_id",),
        },
        Orifice: {
            MemoryControl: (("target_id", "target_type"),),
            TableControl: (("target_id", "target_type"),),
        },
        Weir: {
            MemoryControl: (("target_id", "target_type"),),
            TableControl: (("target_id", "target_type"),),
        },
        MemoryControl: {
            MeasureMap: (("control_id", "control_type"),),
        },
        TableControl: {
            MeasureMap: (("control_id", "control_type"),),
        },
        MeasureLocation: {
            MeasureMap: ("control_measure_location_id",),
        },
    }
)
