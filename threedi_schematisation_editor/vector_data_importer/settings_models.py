from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, ClassVar, Optional, Type

from pydantic import (
    BaseModel,
    ConfigDict,
    create_model,
    field_validator,
    model_validator,
)

# from threedi_schematisation_editor.vector_data_importer.wizard.field_map_model import FieldMapModel
import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.utils import (
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_MINIMUM_CHANNEL_LENGTH,
    ColumnImportMethod,
)


class IntegrationMode(Enum):
    NONE = "None"
    CHANNELS = "channels"
    PIPES = "pipes"


class ConnectionNodeSettingsModel(BaseModel):
    create_nodes: bool = False
    snap: bool = False
    snap_distance: float = 1.0

    def serialize(self):
        return asdict(self)


class IntegrationSettingsModel(BaseModel):
    integration_mode: IntegrationMode = IntegrationMode.NONE
    snap_distance: float = 1.0
    min_length: float = 1.0


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
    allowed_methods: list[ColumnImportMethod]
    required_field_map: ClassVar[dict[ColumnImportMethod, str]] = {
        ColumnImportMethod.ATTRIBUTE: "source_attribute",
        ColumnImportMethod.EXPRESSION: "expression",
        ColumnImportMethod.DEFAULT: "default_value",
    }


class FieldMapConfig(BaseModel):
    _metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[method for method in ColumnImportMethod]
    )
    method: ColumnImportMethod
    source_attribute: Optional[str] = None
    value_map: dict[str, Any] = {}
    expression: Optional[str] = None
    default_value: Optional[Any] = None

    # TODO: consider if we want to keep dict access support
    def get(self, key, default=None):
        return self.dict().get(key, default)

    def __getitem__(self, item):
        return self.dict().get(item)

    def dict(self, **kwargs):
        return super().model_dump(**kwargs)

    @field_validator("method", mode="before")
    def validate_method_presence(cls, value):
        if value is None:
            raise FieldMapConfigMethodMissingError("The 'method' field is required")
        return value

    @model_validator(mode="after")
    def validate_required_fields(self) -> "FieldConfig":
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


def create_field_map_config(
    allowed_methods: Optional[list[ColumnImportMethod]],
) -> BaseModel:
    """Creates a FieldMapConfig class for a specific field based on its metadata"""

    metadata = FieldMapMetadata(allowed_methods=allowed_methods)

    class CustomFieldMapConfig(FieldMapConfig):
        _metadata: ClassVar[FieldMapMetadata] = metadata

        @field_validator("method")
        @classmethod
        def validate_method(cls, v: ColumnImportMethod) -> ColumnImportMethod:
            if allowed_methods is not None and v not in allowed_methods:
                raise ValueError(
                    f"Method {v} is not allowed. "
                    f"Allowed methods are: {', '.join(str(m) for m in allowed_methods)}"
                )
            return v

    return CustomFieldMapConfig


def get_field_map_configs_for_model_class(
    model_class: dm.ModelObject,
) -> dict[str, BaseModel]:
    """Creates FieldMapConfig classes for all fields in a model"""
    all_methods = [method for method in ColumnImportMethod]
    return {
        field.name: create_field_map_config(
            field.name, field.metadata.get(dm.METHOD_FIELDS, all_methods)
        )
        for field in fields(model_class)
    }


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

    def validate(self, **fields_data) -> "FieldsSection":
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
                validated_fields[field_name] = FieldMapConfig(**field_config)
            except Exception as e:
                raise ValueError(f"Invalid configuration for field '{field_name}': {e}")
        return validated_fields


def get_field_map_config(field_config: dict, model_cls: Type):
    validator = FieldsSectionValidator(model_cls)
    return validator.validate(**field_config)


class PointToLineSettingsModel(BaseModel):
    length: FieldMapConfig
    azimuth: FieldMapConfig
