import inspect
import json
from dataclasses import fields
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, model_validator

from threedi_schematisation_editor.vector_data_importer.utils import (
    DEFAULT_INTERSECTION_BUFFER,
    DEFAULT_MINIMUM_CHANNEL_LENGTH,
    ColumnImportMethod,
)


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


class FieldMapConfig(BaseModel):
    method: ColumnImportMethod
    source_attribute: Optional[str] = None
    expression: Optional[str] = None
    default_value: Optional[Any] = None

    # TODO: consider if we want to keep dict access support
    def get(self, key, default=None):
        return self.dict().get(key, default)

    def __getitem__(self, item):
        return self.dict().get(item)

    def dict(self, **kwargs):
        return super().dict(**kwargs)

    @model_validator(mode="after")
    def validate_required_fields(self) -> "FieldConfig":
        method = self.method

        # For expression method, expression is required
        if method == ColumnImportMethod.EXPRESSION and not self.expression:
            raise ValueError(
                "When method is 'expression', 'expression' field is required"
            )

        # For default method, default_value is required
        if method == ColumnImportMethod.DEFAULT and self.default_value is None:
            raise ValueError(
                "When method is 'default', 'default_value' field is required"
            )

        # For source_attribute method, source_attribute is required
        if method == ColumnImportMethod.ATTRIBUTE and not self.source_attribute:
            raise ValueError(
                "When method is 'source_attribute', 'source_attribute' field is required"
            )

        return self


class FieldsSectionValidator:
    """Validator for a fields section against a dataclass."""

    def __init__(self, dataclass_type: type, allow_empty: bool = False):
        """
        Initialize validator for a specific dataclass.

        Args:
            dataclass_type: The dataclass to validate against
            allow_empty: If True, allows empty dictionary as valid input
        """
        self.dataclass_type = dataclass_type
        self.expected_fields = {f.name for f in fields(dataclass_type)}
        self.allow_empty = allow_empty

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
        # Allow empty dictionary if configured
        if not fields_data and self.allow_empty:
            return FieldsSection(fields={})

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


# TODO consider how to use this
class Settings:
    def __init__(self, settings_file, fields_model, cn_model):
        with open(settings_file, "r") as f:
            config_json = json.load(f)
        if "target_layer" not in config_json:
            raise ValueError("Missing 'target_layer' in settings file")
        self.target_layer = config_json["target_layer"]
        self.conversion_settings = ConversionSettings(
            **config_json.get("conversion_settings", {})
        )
        fields_validator = FieldsSectionValidator(fields_model)
        self.fields = fields_validator.validate(**config_json["fields"])
        cn_validator = FieldsSectionValidator(cn_model)
        self.connection_nodes = cn_validator.validate(
            **config_json["connection_node_fields"]
        )


def read_settings(settings_file: str, fields_model, cn_model) -> BaseModel:
    with open(settings_file, "r") as f:
        config_json = json.load(f)
    if "target_layer" not in config_json:
        raise ValueError("Missing 'target_layer' in settings file")
    target_layer = config_json["target_layer"]
    conversion_settings = ConversionSettings(
        **config_json.get("conversion_settings", {})
    )
    fields_validator = FieldsSectionValidator(fields_model)
    fields = fields_validator.validate(**config_json["fields"])
    cn_validator = FieldsSectionValidator(cn_model)
    cn = cn_validator.validate(**config_json["connection_node_fields"])
