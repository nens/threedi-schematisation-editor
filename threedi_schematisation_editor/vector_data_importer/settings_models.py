from dataclasses import dataclass, field, fields
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    create_model,
    field_validator,
    model_validator,
)

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.utils import (
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_MINIMUM_CHANNEL_LENGTH,
    ColumnImportMethod,
)


def get_field_min(
    model_class: BaseModel, field_name: str, default: Optional[float] = 0
) -> float:
    field_info = model_class.model_fields[field_name]
    return getattr(field_info, "ge", default)


def get_field_max(
    model_class: BaseModel, field_name: str, default: Optional[float] = 1000000.0
) -> float:
    field_info = model_class.model_fields[field_name]
    return getattr(field_info, "le", default)


class IntegrationMode(str, Enum):
    NONE = "None"
    CHANNELS = "channels"
    PIPES = "pipes"


class ConnectionNodeSettingsModel(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "connection_nodes"

    create_nodes: bool = False
    snap: bool = False
    snap_distance: float = Field(default=1.0, ge=0, le=1000000.0)

    def serialize(self):
        return asdict(self)


class IntegrationSettingsModel(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "integration"

    integration_mode: IntegrationMode = IntegrationMode.NONE
    snap_distance: float = Field(default=1.0, ge=0, le=1000000.0)
    min_length: float = Field(default=5.0, ge=0, le=1000000.0)


class CrossSectionDataRemapModel(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "cross_section_data_remap"

    set_lowest_point_to_zero: bool = False
    use_lowest_point_as_reference: bool = False


class ConversionSettings(BaseModel):
    """Model for the conversion_settings field"""

    use_snapping: bool = False
    snapping_distance: float = DEFAULT_INTERSECTION_BUFFER
    minimum_channel_length: float = DEFAULT_MINIMUM_CHANNEL_LENGTH
    create_connection_nodes: bool = False
    edit_channels: bool = False
    edit_pipes: bool = False
    length_source_field: str = ""
    length_fallback_value: float = 1.0
    azimuth_source_field: str = ""
    azimuth_fallback_value: float = 90.0
    set_lowest_point_to_zero: bool = False
    use_lowest_point_as_reference: bool = False
    # These are odd fields because they actually use a field mapping
    # In the new UI they will be moved to a field map, so for now we just validate
    # that they are dicts
    join_field_src: dict = {}
    join_field_tgt: dict = {}
    order_by_field: dict = {}


class FieldMapConfigExpressionMissingError(ValueError):
    pass


class FieldMapConfigDefaultValueMissingError(ValueError):
    pass


class FieldMapConfigSourceAttributeMissingError(ValueError):
    pass


class FieldMapConfigMethodMissingError(ValueError):
    pass


@dataclass
class FieldMapMetadata:
    allowed_methods: list[ColumnImportMethod] = field(
        default_factory=lambda: ColumnImportMethod.all()
    )
    required_field_map: ClassVar[dict[ColumnImportMethod, str]] = {
        ColumnImportMethod.ATTRIBUTE: "source_attribute",
        ColumnImportMethod.EXPRESSION: "expression",
        ColumnImportMethod.DEFAULT: "default_value",
    }


DefaultValueType = TypeVar("DefaultValueType")


class FieldMapConfig(BaseModel, Generic[DefaultValueType]):
    _metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata()
    method: ColumnImportMethod
    source_attribute: Optional[str] = None
    value_map: dict[str, Any] = {}
    expression: Optional[str] = None
    default_value: Optional[DefaultValueType] = None

    @classmethod
    def with_metadata(cls, metadata: FieldMapMetadata) -> Type["FieldMapConfig"]:
        """Returns a subclass with specific metadata"""
        return type("CustomFieldMapConfig", (cls,), {"_metadata": metadata})

    # TODO: consider if we want to keep dict access support
    def get(self, key, default=None):
        return self.dict().get(key, default)

    def __getitem__(self, item):
        return self.dict().get(item)

    def dict(self, **kwargs):
        return super().model_dump(**kwargs)

    @field_validator("method", mode="before")
    def validate_method_presence(cls, value):
        # TODO: consider if custom check is necessary just to raise
        if value is None:
            raise FieldMapConfigMethodMissingError("The 'method' field is required")
        return value

    @model_validator(mode="after")
    def validate_required_fields(self) -> "FieldConfig":
        """Validate if correct fields are set based on the selected method"""
        method = self.method
        if method in self._metadata.required_field_map and getattr(
            self, self._metadata.required_field_map[method]
        ) in [None, ""]:
            # TODO: reconsider specific errors
            if method == ColumnImportMethod.EXPRESSION:
                raise FieldMapConfigExpressionMissingError(
                    "When method is 'expression', 'expression' field is required"
                )
            elif method == ColumnImportMethod.DEFAULT:
                raise FieldMapConfigDefaultValueMissingError(
                    "When method is 'default', 'default_value' field is required"
                )
            elif method == ColumnImportMethod.ATTRIBUTE:
                raise FieldMapConfigSourceAttributeMissingError(
                    "When method is 'source_attribute', 'source_attribute' field is required"
                )
        return self

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: ColumnImportMethod) -> ColumnImportMethod:
        """Validate if selected method is in allowe methods"""
        # Get the allowed_methods from _metadata
        allowed_methods = None
        if cls._metadata is not None:
            allowed_methods = cls._metadata.allowed_methods

        if allowed_methods is not None and v not in allowed_methods:
            raise ValueError(
                f"Method {v} is not allowed. "
                f"Allowed methods are: {', '.join(str(m) for m in allowed_methods)}"
            )
        return v


def create_field_map_config(
    allowed_methods: Optional[list[ColumnImportMethod]],
    field_type: Type[DefaultValueType] = Any,
) -> Type[FieldMapConfig]:
    """Creates a FieldMapConfig class for a specific field based on its metadata"""
    metadata = FieldMapMetadata(allowed_methods=allowed_methods)
    return FieldMapConfig[field_type].with_metadata(metadata)


def get_field_map_config_for_model_class_field(
    field_name: str, model_class: Type
) -> Type[FieldMapConfig]:
    """Creates FieldMapConfig class for a specific field of a data model"""
    class_field = next((f for f in fields(model_class) if f.name == field_name), None)
    if not class_field:
        raise ValueError(f"Field {field_name} not found in {model_class.__name__}")
    return create_field_map_config(
        get_allowed_methods_for_model_class_field(class_field),
        field_type=class_field.type,
    )


def get_allowed_methods_for_model_class_field(
    model_field,
) -> list[ColumnImportMethod]:
    # TODO: check if excluded is actually needed
    # Try to find allowed_methods from metadata
    allowed_methods = model_field.metadata.get(dm.ALLOWED_METHODS_FIELD)
    # Use defaults if not defined
    if not allowed_methods:
        if model_field.name == "id":
            allowed_methods = [ColumnImportMethod.AUTO]
        else:
            allowed_methods = [
                method
                for method in ColumnImportMethod
                if method != ColumnImportMethod.AUTO
            ]
    # Find excluded methods
    excluded_methods = model_field.metadata.get(dm.EXLUCDED_METHODS_FIELD, [])
    # check if field type is optional and if so add it to the excluded_methods
    type_constructor = get_origin(model_field.type)
    # Optional fields have type Union[T, None]
    if not type_constructor is Union or type(None) not in get_args(model_field.type):
        excluded_methods.append(ColumnImportMethod.IGNORE)
    # Remove excluded methods
    for method in excluded_methods:
        if method in allowed_methods:
            allowed_methods.remove(method)
    return sorted(
        allowed_methods, key=lambda method: list(ColumnImportMethod).index(method)
    )


class FieldConfigDataModel:
    @classmethod
    def get_settings_model(cls, field_config: dict):
        field_map_config = get_field_map_config(field_config, cls)
        # Create field definitions dynamically from the class
        cls_fields = {field.name: (FieldMapConfig, ...) for field in fields(cls)}
        # Create the model class dynamically
        FieldConfigModel = create_model(
            "FieldConfigModel", __base__=BaseModel, **cls_fields
        )
        if hasattr(cls, "name"):
            FieldConfigModel.name = cls.name
        return FieldConfigModel(**field_map_config)


class PointToLineSettingsModel(BaseModel):
    metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[
            ColumnImportMethod.ATTRIBUTE,
            ColumnImportMethod.DEFAULT,
            ColumnImportMethod.EXPRESSION,
        ]
    )
    name: ClassVar[str] = "point_to_line_conversion"
    length: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.DEFAULT, default_value=1.0
    )
    azimuth: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.DEFAULT, default_value=90
    )


class CrossSectionLocationSettingsModel(BaseModel):
    metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[
            ColumnImportMethod.AUTO,
            ColumnImportMethod.ATTRIBUTE,
            ColumnImportMethod.EXPRESSION,
        ]
    )
    name: ClassVar[str] = "cross_section_location_mapping"
    join_field_src: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.AUTO, default_value=""
    )
    join_field_tgt: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.AUTO, default_value=""
    )
    snap_distance: float = Field(default=1.0, ge=0, le=1000000.0)


# TODO: combine stuff above and below in 1 consistent approach


class FieldsSectionValidator:
    """Validator for a fields section against a dataclass."""

    def __init__(self, dataclass_type: type):
        """
        Initialize validator for a specific dataclass.

        Args:
            dataclass_type: The dataclass to validate against
        """
        self.dataclass_type = dataclass_type
        self.expected_fields = {f.name for f in fields(dataclass_type)}

    def validate(self, **fields_data) -> dict[str, FieldMapConfig]:
        """
        Validate a fields section.

        Args:
            fields_data: Dictionary mapping field names to field configurations

        Returns:
            FieldsSection model with validated field configurations

        Raises:
            ValueError: If validation fails
        """
        # First, validate each field configuration with Pydantic
        validated_fields = {}
        for field_name, field_config in fields_data.items():
            if field_name not in self.expected_fields:
                # ignore
                continue
            try:
                if isinstance(field_config, FieldMapConfig):
                    # TODO enforce validation?
                    validated_fields[field_name] = field_config
                else:
                    validated_fields[field_name] = FieldMapConfig(**field_config)
            except Exception as e:
                raise ValueError(f"Invalid configuration for field '{field_name}': {e}")
        return validated_fields


def get_field_map_config(
    field_config: dict, model_cls: Type
) -> dict[str, FieldMapConfig]:
    validator = FieldsSectionValidator(model_cls)
    return validator.validate(**field_config)


class ConversionSettingsModel(BaseModel):
    connection_nodes: ConnectionNodeSettingsModel = ConnectionNodeSettingsModel()
    integration: IntegrationSettingsModel = IntegrationSettingsModel()
    cross_section_data_remap: CrossSectionDataRemapModel = CrossSectionDataRemapModel()
    point_to_line_conversion: PointToLineSettingsModel = PointToLineSettingsModel()
    cross_section_location_mapping: CrossSectionLocationSettingsModel = (
        CrossSectionLocationSettingsModel()
    )
    fields: dict[str, FieldMapConfig] = {}
    connection_node_fields: dict[str, FieldMapConfig] = {}
