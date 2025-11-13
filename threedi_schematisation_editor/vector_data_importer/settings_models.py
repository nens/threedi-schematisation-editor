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
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


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


class ConnectionNodeSettings(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "connection_nodes"

    create_nodes: bool = True
    snap: bool = True
    snap_distance: float = Field(default=1.0, ge=0, le=1000000.0)

    def serialize(self):
        return asdict(self)


class IntegrationSettings(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "integration"

    integration_mode: IntegrationMode = IntegrationMode.NONE
    snap_distance: float = Field(default=1.0, ge=0, le=1000000.0)
    min_length: float = Field(default=5.0, ge=0, le=1000000.0)


class CrossSectionDataRemap(BaseModel):
    # class variables used to identify model
    name: ClassVar[str] = "cross_section_data_remap"

    set_lowest_point_to_zero: bool = True
    use_lowest_point_as_reference: bool = True


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

    def get(self, key, default=None):
        return self.dict().get(key, default)

    def __getitem__(self, item):
        return self.dict().get(item)

    def dict(self, **kwargs):
        return super().model_dump(**kwargs)

    @model_validator(mode="after")
    def validate_required_fields(self) -> "FieldConfig":
        """Validate if correct fields are set based on the selected method"""
        method = self.method
        if method in self._metadata.required_field_map and getattr(
            self, self._metadata.required_field_map[method]
        ) in [None, ""]:
            loc = self._metadata.required_field_map[method]
            msg = f"When method is '{str(method)}', a value for {loc} is required"
            raise PydanticCustomError("value_error.missing", msg)

        return self

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: ColumnImportMethod) -> ColumnImportMethod:
        """Validate if selected method is in allowed methods"""
        # Get the allowed_methods from _metadata
        allowed_methods = None
        if cls._metadata is not None:
            allowed_methods = cls._metadata.allowed_methods
        if allowed_methods is not None and v not in allowed_methods:
            msg = f"Method {v} is not allowed; allowed methods are: {', '.join(str(m) for m in allowed_methods)}"
            raise PydanticCustomError("value_error.invalid", msg)
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
    # check if field type is optional and if so add it to the excluded_methods
    type_constructor = get_origin(model_field.type)
    # Optional fields have type Union[T, None]
    is_optional = type_constructor is Union and type(None) in get_args(model_field.type)
    if is_optional and ColumnImportMethod.IGNORE not in allowed_methods:
        allowed_methods.append(ColumnImportMethod.IGNORE)
    if not is_optional and ColumnImportMethod.IGNORE in allowed_methods:
        allowed_methods.remove(ColumnImportMethod.IGNORE)
    return sorted(
        allowed_methods, key=lambda method: list(ColumnImportMethod).index(method)
    )


class PointToLineSettings(BaseModel):
    metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[
            ColumnImportMethod.ATTRIBUTE,
            ColumnImportMethod.DEFAULT,
            ColumnImportMethod.EXPRESSION,
        ]
    )
    name: ClassVar[str] = "point_to_line_conversion"
    length: FieldMapConfig = FieldMapConfig[float].with_metadata(metadata)(
        method=ColumnImportMethod.DEFAULT, default_value=1.0
    )
    azimuth: FieldMapConfig = FieldMapConfig[float].with_metadata(metadata)(
        method=ColumnImportMethod.DEFAULT, default_value=90
    )


class CrossSectionLocationSettings(BaseModel):
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


class ImportSettings(BaseModel):
    connection_nodes: ConnectionNodeSettings = ConnectionNodeSettings()
    integration: IntegrationSettings = IntegrationSettings()
    cross_section_data_remap: CrossSectionDataRemap = CrossSectionDataRemap()
    point_to_line_conversion: PointToLineSettings = PointToLineSettings()
    cross_section_location_mapping: CrossSectionLocationSettings = (
        CrossSectionLocationSettings()
    )
    fields: dict[str, FieldMapConfig] = {}
    connection_node_fields: dict[str, FieldMapConfig] = {}
