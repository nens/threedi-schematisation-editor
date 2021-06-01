from dataclasses import dataclass
from typing import Optional
from types import MappingProxyType
from threedi_model_builder.enumerators import (
    AggregationMethod,
    BoundaryType,
    CalculationType,
    CalculationTypeNode,
    CalculationTypeCulvert,
    CrestType,
    CrossSectionShape,
    FlowVariable,
    FrictionType,
    GeometryType,
    InfiltrationSurfaceOption,
    InterflowType,
    InitializationType,
    Later2DType,
    ManholeIndicator,
    ManholeShape,
    Material,
    ObstacleType,
    PipeCalculationType,
    PipeMaterial,
    PumpType,
    SewerageType,
    SurfaceClass,
    SurfaceInclinationType,
    ZoomCategories,
)


class ModelObject:
    __tablename__ = None
    __layername__ = None
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = tuple()
    SQLITE_TARGETS = tuple()
    IMPORT_FIELD_MAPPINGS = MappingProxyType({})
    EXPORT_FIELD_MAPPINGS = MappingProxyType({})
    RELATED_RASTERS = tuple()


@dataclass
class ConnectionNode(ModelObject):
    __tablename__ = "connection_node"
    __layername__ = "Connection Node"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_connection_nodes",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    initial_waterlevel: Optional[float]
    storage_area: Optional[float]


@dataclass
class BoundaryCondition1D(ModelObject):
    __tablename__ = "1d_boundary_condition"
    __layername__ = "1D Boundary Condition"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_1d_boundary_conditions_view",)
    SQLITE_TARGETS = ("v2_1d_boundary_conditions",)

    id: int
    boundary_type: BoundaryType
    connection_node_id: int
    timeseries: str  # TODO: This is just temporary - remove after finishing Timeseries implementation


@dataclass
class Lateral1D(ModelObject):
    __tablename__ = "1d_lateral"
    __layername__ = "1D Lateral"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_1d_lateral_view",)
    SQLITE_TARGETS = ("v2_1d_lateral",)

    id: int
    connection_node_id: int
    timeseries: str  # TODO: This is just temporary - remove after finishing Timeseries implementation


@dataclass
class Manhole(ModelObject):
    __tablename__ = "manhole"
    __layername__ = "Manhole"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_manhole_view",)
    SQLITE_TARGETS = ("v2_manhole",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "manh_id",
            "code": "manh_code",
            "display_name": "manh_display_name",
            "calculation_type": "manh_calculation_type",
            "shape": "manh_shape",
            "width": "manh_width",
            "length": "manh_length",
            "bottom_level": "manh_bottom_level",
            "surface_level": "manh_surface_level",
            "drain_level": "manh_drain_level",
            "sediment_level": "manh_sediment_level",
            "manhole_indicator": "manh_manhole_indicator",
            "zoom_category": "manh_zoom_category",
            "connection_node_id": "manh_connection_node_id",
        }
    )

    id: int
    code: str
    display_name: str
    calculation_type: Optional[CalculationTypeNode]
    shape: Optional[ManholeShape]
    width: Optional[float]
    length: Optional[float]
    bottom_level: float
    surface_level: Optional[float]
    drain_level: Optional[float]
    sediment_level: Optional[float]
    manhole_indicator: Optional[ManholeIndicator]
    zoom_category: Optional[ZoomCategories]
    connection_node_id: int


@dataclass
class Pumpstation(ModelObject):
    __tablename__ = "pumpstation"
    __layername__ = "Pumpstation (without end node)"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_pumpstation_point_view",)
    SQLITE_TARGETS = ("v2_pumpstation",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "pump_id",
        }
    )

    EXPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "connection_node_id": "connection_node_start_id",
        }
    )

    id: int
    code: str
    display_name: str
    start_level: float
    lower_stop_level: float
    upper_stop_level: Optional[float]
    capacity: float
    type: PumpType
    sewerage: bool
    zoom_category: Optional[ZoomCategories]
    connection_node_id: int


@dataclass
class PumpstationMap(ModelObject):
    __tablename__ = "pumpstation_map"
    __layername__ = "Pumpstation (with end node)"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_pumpstation_view",)
    SQLITE_TARGETS = ("v2_pumpstation",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "pump_id",
            "code": "pump_code",
            "display_name": "pump_display_name",
            "pumpstation_id": "pump_id",
            "connection_node_start_id": "pump_connection_node_start_id",
            "connection_node_end_id": "pump_connection_node_end_id",
        }
    )

    id: int
    code: str
    display_name: str
    pumpstation_id: int
    connection_node_start_id: int
    connection_node_end_id: int


@dataclass
class Weir(ModelObject):
    __tablename__ = "weir"
    __layername__ = "Weir"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_weir_view",)
    SQLITE_TARGETS = ("v2_weir",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "weir_id",
            "code": "weir_code",
            "display_name": "weir_display_name",
            "crest_level": "weir_crest_level",
            "crest_type": "weir_crest_type",
            "discharge_coefficient_positive": "weir_discharge_coefficient_positive",
            "discharge_coefficient_negative": "weir_discharge_coefficient_negative",
            "friction_value": "weir_friction_value",
            "friction_type": "weir_friction_type",
            "sewerage": "weir_sewerage",
            "external": "weir_external",
            "zoom_category": "weir_zoom_category",
            "connection_node_start_id": "weir_connection_node_start_id",
            "connection_node_end_id": "weir_connection_node_end_id",
            "cross_section_definition_id": "weir_cross_section_definition_id",
        }
    )

    id: int
    code: str
    display_name: str
    crest_level: float
    crest_type: CrestType
    discharge_coefficient_positive: Optional[float]
    discharge_coefficient_negative: Optional[float]
    friction_value: float
    friction_type: FrictionType
    sewerage: bool
    external: Optional[bool]
    zoom_category: Optional[ZoomCategories]
    connection_node_start_id: int
    connection_node_end_id: int
    cross_section_definition_id: int


@dataclass
class Culvert(ModelObject):
    __tablename__ = "culvert"
    __layername__ = "Culvert"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_culvert_view",)
    SQLITE_TARGETS = ("v2_culvert",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "cul_id",
            "code": "cul_code",
            "display_name": "cul_display_name",
            "calculation_type": "cul_calculation_type",
            "dist_calc_points": "cul_dist_calc_points",
            "invert_level_start_point": "cul_invert_level_start_point",
            "invert_level_end_point": "cul_invert_level_end_point",
            "discharge_coefficient_positive": "cul_discharge_coefficient_positive",
            "discharge_coefficient_negative": "cul_discharge_coefficient_negative",
            "friction_value": "cul_friction_value",
            "friction_type": "cul_friction_type",
            "zoom_category": "cul_zoom_category",
            "connection_node_start_id": "cul_connection_node_start_id",
            "connection_node_end_id": "cul_connection_node_end_id",
            "cross_section_definition_id": "cul_cross_section_definition_id",
        }
    )

    id: int
    code: str
    display_name: str
    calculation_type: Optional[CalculationTypeCulvert]
    dist_calc_points: Optional[float]
    invert_level_start_point: float
    invert_level_end_point: float
    discharge_coefficient_positive: float
    discharge_coefficient_negative: float
    friction_value: float
    friction_type: FrictionType
    zoom_category: Optional[ZoomCategories]
    connection_node_start_id: int
    connection_node_end_id: int
    cross_section_definition_id: int


@dataclass
class Orifice(ModelObject):
    __tablename__ = "orifice"
    __layername__ = "Orifice"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_orifice_view",)
    SQLITE_TARGETS = ("v2_orifice",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "orf_id",
            "code": "orf_code",
            "display_name": "orf_display_name",
            "crest_level": "orf_crest_level",
            "crest_type": "orf_crest_type",
            "discharge_coefficient_positive": "orf_discharge_coefficient_positive",
            "discharge_coefficient_negative": "orf_discharge_coefficient_negative",
            "friction_value": "orf_friction_value",
            "friction_type": "orf_friction_type",
            "max_capacity": "orf_max_capacity",
            "sewerage": "orf_sewerage",
            "zoom_category": "orf_zoom_category",
            "connection_node_start_id": "orf_connection_node_start_id",
            "connection_node_end_id": "orf_connection_node_end_id",
            "cross_section_definition_id": "orf_cross_section_definition_id",
        }
    )

    id: int
    code: str
    display_name: str
    crest_level: float
    crest_type: CrestType
    discharge_coefficient_positive: Optional[float]
    discharge_coefficient_negative: Optional[float]
    friction_value: float
    friction_type: FrictionType
    max_capacity: float
    sewerage: bool
    zoom_category: Optional[ZoomCategories]
    connection_node_start_id: int
    connection_node_end_id: int
    cross_section_definition_id: int


@dataclass
class Pipe(ModelObject):
    __tablename__ = "pipe"
    __layername__ = "Pipe"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_pipe_view",)
    SQLITE_TARGETS = ("v2_pipe",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "pipe_id",
            "code": "pipe_code",
            "display_name": "pipe_display_name",
            "calculation_type": "pipe_calculation_type",
            "dist_calc_points": "pipe_dist_calc_points",
            "invert_level_start_point": "pipe_invert_level_start_point",
            "invert_level_end_point": "pipe_invert_level_end_point",
            "friction_value": "pipe_friction_value",
            "friction_type": "pipe_friction_type",
            "material": "pipe_material",
            "pipe_quality": "pipe_pipe_quality",
            "sewerage_type": "pipe_sewerage_type",
            "zoom_category": "pipe_zoom_category",
            "profile_num": "pipe_profile_num",
            "original_length": "pipe_original_length",
            "connection_node_start_id": "pipe_connection_node_start_id",
            "connection_node_end_id": "pipe_connection_node_end_id",
            "cross_section_definition_id": "pipe_cross_section_definition_id",
        }
    )

    id: int
    code: str
    display_name: str
    calculation_type: PipeCalculationType
    dist_calc_points: Optional[float]
    invert_level_start_point: float
    invert_level_end_point: float
    friction_value: float
    friction_type: FrictionType
    material: Optional[PipeMaterial]
    pipe_quality: float
    sewerage_type: Optional[SewerageType]
    zoom_category: Optional[ZoomCategories]
    profile_num: Optional[int]
    original_length: Optional[float]
    connection_node_start_id: int
    connection_node_end_id: int
    cross_section_definition_id: int


@dataclass
class CrossSectionLocation(ModelObject):
    __tablename__ = "cross_section_location"
    __layername__ = "Cross section location"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_cross_section_location_view",)
    SQLITE_TARGETS = ("v2_cross_section_location",)

    IMPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "id": "loc_id",
            "code": "loc_code",
            "reference_level": "loc_reference_level",
            "friction_value": "loc_friction_value",
            "friction_type": "loc_friction_type",
            "bank_level": "loc_bank_level",
            "channel_id": "loc_channel_id",
            "cross_section_definition_id": "loc_definition_id",
        }
    )

    EXPORT_FIELD_MAPPINGS = MappingProxyType(
        {
            "cross_section_definition_id": "definition_id",
        }
    )

    id: int
    code: str
    reference_level: float
    friction_type: FrictionType
    friction_value: float
    bank_level: Optional[float]
    channel_id: int
    cross_section_definition_id: int


@dataclass
class CrossSectionDefinition(ModelObject):
    __tablename__ = "cross_section_definition"
    __layername__ = "Cross section definition"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_cross_section_definition",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    width: Optional[str]
    height: Optional[str]
    shape: Optional[CrossSectionShape]


@dataclass
class Channel(ModelObject):
    __tablename__ = "channel"
    __layername__ = "Channel"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_channel",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    display_name: str
    calculation_type: CalculationType
    dist_calc_points: Optional[float]
    zoom_category: Optional[ZoomCategories]
    connection_node_start_id: int
    connection_node_end_id: Optional[int]


@dataclass
class BoundaryCondition2D(ModelObject):
    __tablename__ = "2d_boundary_condition"
    __layername__ = "2D Boundary condition"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_2d_boundary_conditions",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    display_name: str
    boundary_type: BoundaryType
    timeseries: str  # TODO: This is just temporary - remove after finishing Timeseries implementation


@dataclass
class Lateral2D(ModelObject):
    __tablename__ = "2d_lateral"
    __layername__ = "2D Lateral"
    __geometrytype__ = GeometryType.Point

    SQLITE_SOURCES = ("v2_2d_lateral",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    type: Later2DType
    timeseries: str  # TODO: This is just temporary - remove after finishing Timeseries implementation


@dataclass
class LinearObstacle(ModelObject):
    __tablename__ = "linear_obstacle"
    __layername__ = "Linear Obstacle"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = (
        "v2_obstacle",
        "v2_levee",
    )
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    type: ObstacleType
    crest_level: float
    material: Optional[Material]
    max_breach_depth: Optional[float]


@dataclass
class GridRefinement(ModelObject):
    __tablename__ = "grid_refinement"
    __layername__ = "Grid refinement"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_grid_refinement",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    display_name: str
    refinement_level: int


@dataclass
class GridRefinementArea(ModelObject):
    __tablename__ = "grid_refinement_area"
    __layername__ = "Grid refinement area"
    __geometrytype__ = GeometryType.Polygon

    SQLITE_SOURCES = ("v2_grid_refinement_area",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    display_name: str
    refinement_level: int


@dataclass
class DEMAverageArea(ModelObject):
    __tablename__ = "dem_average_area"
    __layername__ = "DEM average area"
    __geometrytype__ = GeometryType.Polygon

    SQLITE_SOURCES = ("v2_dem_average_area",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int


@dataclass
class Windshielding(ModelObject):
    __tablename__ = "windshielding"
    __layername__ = "Windshielding"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_windshielding",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    north: Optional[float]
    northeast: Optional[float]
    east: Optional[float]
    southeast: Optional[float]
    south: Optional[float]
    southwest: Optional[float]
    west: Optional[float]
    northwest: Optional[float]
    channel_id: int


@dataclass
class ImperviousSurface(ModelObject):
    __tablename__ = "impervious_surface"
    __layername__ = "Impervious Surface"
    __geometrytype__ = GeometryType.Polygon

    SQLITE_SOURCES = ("v2_impervious_surface",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    display_name: str
    surface_inclination: SurfaceInclinationType
    surface_class: SurfaceClass
    surface_sub_class: Optional[str]
    zoom_category: Optional[ZoomCategories]
    nr_of_inhabitants: Optional[float]
    area: Optional[float]
    dry_weather_flow: Optional[float]
    function: Optional[str]


@dataclass
class ImperviousSurfaceMap(ModelObject):
    __tablename__ = "impervious_surface_map"
    __layername__ = "Impervious surface map"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_impervious_surface_map",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    percentage: float
    impervious_surface_id: int
    connection_node_id: int


@dataclass
class Surface(ModelObject):
    __tablename__ = "surface"
    __layername__ = "Surface"
    __geometrytype__ = GeometryType.Polygon

    SQLITE_SOURCES = ("v2_surface",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    code: str
    display_name: str
    zoom_category: Optional[ZoomCategories]
    nr_of_inhabitants: Optional[float]
    area: Optional[float]
    dry_weather_flow: Optional[float]
    function: Optional[str]
    surface_parameters_id: int


@dataclass
class SurfaceMap(ModelObject):
    __tablename__ = "surface_map"
    __layername__ = "Surface map"
    __geometrytype__ = GeometryType.Linestring

    SQLITE_SOURCES = ("v2_surface_map",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    percentage: Optional[float]
    surface_id: int
    connection_node_id: int


@dataclass
class SurfaceParameters(ModelObject):
    __tablename__ = "surface_parameters"
    __layername__ = "Surface parameters"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_surface_parameters",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    outflow_delay: float
    surface_layer_thickness: float
    infiltration: bool
    max_infiltration_capacity: float
    min_infiltration_capacity: float
    infiltration_decay_constant: float
    infiltration_recovery_constant: float


@dataclass
class GlobalSettings(ModelObject):
    __tablename__ = "global_settings"
    __layername__ = "Global settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_global_settings",)
    SQLITE_TARGETS = SQLITE_SOURCES
    RELATED_RASTERS = (
        ("dem_file", "Digital elevation model [m MSL]"),
        ("frict_coef_file", "Friction coefficient [-]"),
        ("initial_groundwater_level_file", "Initial groundwater level [m MSL]"),
        ("initial_waterlevel_file", "Initial water level [m MSL]"),
        ("interception_file", "Interception [m]"),
    )

    id: int
    use_2d_flow: bool
    use_1d_flow: bool
    manhole_storage_area: Optional[float]
    name: Optional[str]
    sim_time_step: float
    output_time_step: Optional[float]
    nr_timesteps: int
    start_time: Optional[str]
    start_date: str
    grid_space: float
    dist_calc_points: float
    kmax: int
    guess_dams: Optional[int]
    table_step_size: float
    flooding_threshold: float
    advection_1d: int
    advection_2d: int
    dem_file: Optional[str]
    frict_type: Optional[int]
    frict_coef: float
    frict_coef_file: Optional[str]
    water_level_ini_type: Optional[InitializationType]
    initial_waterlevel: float
    initial_waterlevel_file: Optional[str]
    interception_global: Optional[float]
    interception_file: Optional[str]
    dem_obstacle_detection: bool
    dem_obstacle_height: Optional[float]
    embedded_cutoff_threshold: Optional[float]
    epsg_code: Optional[int]
    timestep_plus: bool
    max_angle_1d_advection: Optional[float]
    minimum_sim_time_step: Optional[float]
    maximum_sim_time_step: Optional[float]
    frict_avg: Optional[int]
    wind_shielding_file: Optional[str]
    use_0d_inflow: int
    table_step_size_1d: Optional[float]
    table_step_size_volume_2d: Optional[float]
    use_2d_rain: int
    initial_groundwater_level: Optional[float]
    initial_groundwater_level_file: Optional[str]
    initial_groundwater_level_type: Optional[InitializationType]
    numerical_settings_id: int
    interflow_settings_id: int
    control_group_id: int
    simple_infiltration_settings_id: int
    groundwater_settings_id: int


@dataclass
class AggregationSettings(ModelObject):
    __tablename__ = "aggregation_settings"
    __layername__ = "Aggregation settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_aggregation_settings",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    global_settings_id: int
    var_name: str
    flow_variable: FlowVariable
    aggregation_method: Optional[AggregationMethod]
    aggregation_in_space: str  # This suppose to be boolean
    timestep: int


@dataclass
class SimpleInfiltrationSettings(ModelObject):
    __tablename__ = "simple_infiltration_settings"
    __layername__ = "Simple infiltration settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_simple_infiltration",)
    SQLITE_TARGETS = SQLITE_SOURCES
    RELATED_RASTERS = (
        ("infiltration_rate_file", "Infiltration rate [mm/d]"),
        ("max_infiltration_capacity_file", "Max infiltration capacity [m]"),
    )

    id: int
    infiltration_rate: float
    infiltration_rate_file: Optional[str]
    infiltration_surface_option: Optional[InfiltrationSurfaceOption]
    max_infiltration_capacity_file: Optional[str]
    display_name: str


@dataclass
class GroundWaterSettings(ModelObject):
    __tablename__ = "groundwater_settings"
    __layername__ = "Groundwater settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_groundwater",)
    SQLITE_TARGETS = SQLITE_SOURCES
    RELATED_RASTERS = (
        ("equilibrium_infiltration_rate_file", "Equilibrium infiltration rate [mm/d]"),
        ("groundwater_hydro_connectivity_file", "Hydraulic conductivity [m/day]"),
        ("groundwater_impervious_layer_level_file", "Impervious layer level [m MSL]"),
        ("infiltration_decay_period_file", "Infiltration decay period [d]"),
        ("initial_infiltration_rate_file", "Initial infiltration rate [mm/d]"),
        ("leakage_file", "Leakage [mm/d]"),
        ("phreatic_storage_capacity_file", "Phreatic storage capacity [-]"),
    )

    id: int
    groundwater_impervious_layer_level: Optional[float]
    groundwater_impervious_layer_level_file: Optional[str]
    groundwater_impervious_layer_level_type: Optional[InitializationType]
    phreatic_storage_capacity: Optional[float]
    phreatic_storage_capacity_file: Optional[str]
    phreatic_storage_capacity_type: Optional[InitializationType]
    equilibrium_infiltration_rate: Optional[float]
    equilibrium_infiltration_rate_file: Optional[str]
    equilibrium_infiltration_rate_type: Optional[InitializationType]
    initial_infiltration_rate: Optional[float]
    initial_infiltration_rate_file: Optional[str]
    initial_infiltration_rate_type: Optional[InitializationType]
    infiltration_decay_period: Optional[float]
    infiltration_decay_period_file: Optional[str]
    infiltration_decay_period_type: Optional[InitializationType]
    groundwater_hydro_connectivity: Optional[float]
    groundwater_hydro_connectivity_file: Optional[str]
    groundwater_hydro_connectivity_type: Optional[InitializationType]
    display_name: str
    leakage: Optional[float]
    leakage_file: Optional[str]


@dataclass
class InterflowSettings(ModelObject):
    __tablename__ = "interflow_settings"
    __layername__ = "Interflow settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_interflow",)
    SQLITE_TARGETS = SQLITE_SOURCES
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
    display_name: str


@dataclass
class NumericalSettings(ModelObject):
    __tablename__ = "numerical_settings"
    __layername__ = "Numerical settings"
    __geometrytype__ = GeometryType.NoGeometry

    SQLITE_SOURCES = ("v2_numerical_settings",)
    SQLITE_TARGETS = SQLITE_SOURCES

    id: int
    cfl_strictness_factor_1d: Optional[float]
    cfl_strictness_factor_2d: Optional[float]
    convergence_cg: Optional[float]
    convergence_eps: Optional[float]
    flow_direction_threshold: Optional[float]
    frict_shallow_water_correction: Optional[int]
    general_numerical_threshold: Optional[float]
    integration_method: Optional[int]
    limiter_grad_1d: Optional[int]
    limiter_grad_2d: Optional[int]
    limiter_slope_crossectional_area_2d: Optional[int]
    limiter_slope_friction_2d: Optional[int]
    max_nonlin_iterations: Optional[int]
    max_degree: int
    minimum_friction_velocity: Optional[float]
    minimum_surface_area: Optional[float]
    precon_cg: Optional[int]
    preissmann_slot: Optional[float]
    pump_implicit_ratio: Optional[float]
    thin_water_layer_definition: Optional[float]
    use_of_cg: int
    use_of_nested_newton: int


@dataclass
class Timeseries(ModelObject):
    __tablename__ = "timeseries"
    __layername__ = "Timeseries"
    __geometrytype__ = GeometryType.NoGeometry

    id: int
    reference_layer: str
    reference_id: int
    offset: int  # seconds
    duration: int  # seconds
    value: float


MODEL_1D_ELEMENTS = (
    ConnectionNode,
    BoundaryCondition1D,
    Lateral1D,
    Manhole,
    Pumpstation,
    PumpstationMap,
    Weir,
    Culvert,
    Orifice,
    Pipe,
    CrossSectionLocation,
    Channel,
    CrossSectionDefinition,
)

MODEL_2D_ELEMENTS = (
    BoundaryCondition2D,
    Lateral2D,
    LinearObstacle,
    GridRefinement,
    GridRefinementArea,
    DEMAverageArea,
    Windshielding,
)

INFLOW_ELEMENTS = (
    ImperviousSurfaceMap,
    ImperviousSurface,
    SurfaceMap,
    Surface,
    SurfaceParameters,
)

SETTINGS_ELEMENTS = (
    GlobalSettings,
    AggregationSettings,
    SimpleInfiltrationSettings,
    GroundWaterSettings,
    InterflowSettings,
    NumericalSettings,
)


ALL_MODELS = MODEL_1D_ELEMENTS + MODEL_2D_ELEMENTS + INFLOW_ELEMENTS + SETTINGS_ELEMENTS + (Timeseries,)
ELEMENTS_WITH_TIMESERIES = (
    BoundaryCondition1D,
    Lateral1D,
    BoundaryCondition2D,
    Lateral2D,
)
ELEMENTS_WITH_RASTERS = tuple(model_cls for model_cls in SETTINGS_ELEMENTS if model_cls.RELATED_RASTERS)


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
