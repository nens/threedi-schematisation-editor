from dataclasses import dataclass

import pytest

from threedi_schematisation_editor.vector_data_importer.settings_model import (
    FieldMapConfig,
    FieldMapConfigDefaultValueMissingError,
    FieldMapConfigExpressionMissingError,
    FieldMapConfigMethodMissingError,
    FieldMapConfigSourceAttributeMissingError,
    FieldsSectionValidator,
)


@pytest.mark.parametrize(
    "config_dict,expected_error",
    [
        ({"method": "auto", "source_attribute": "foo"}, None),
        ({"method": "ignore"}, None),
        ({"method": "source_attribute"}, FieldMapConfigSourceAttributeMissingError),
        ({"method": "source_attribute", "source_attribute": "foo"}, None),
        (
            {
                "method": "source_attribute",
                "source_attribute": "foo",
                "default_value": "bar",
            },
            None,
        ),
        ({"method": "expression"}, FieldMapConfigExpressionMissingError),
        ({"method": "expression", "expression": "foo"}, None),
        ({"method": "expression", "expression": "foo", "default_value": "bar"}, None),
        ({"method": "default"}, FieldMapConfigDefaultValueMissingError),
        ({"method": "default", "default_value": "foo"}, None),
        ({}, FieldMapConfigMethodMissingError),
    ],
)
def test_field_map_config(config_dict, expected_error):
    if not expected_error:
        assert FieldMapConfig(**config_dict)
    else:
        with pytest.raises(ValueError):
            FieldMapConfig(**config_dict)


@dataclass
class Test:
    foo: int
    bar: str


@pytest.mark.parametrize(
    "config_dict,valid,expected_keys",
    [
        (
            {
                "foo": {"method": "auto"},
                "bar": {"method": "source_attribute", "source_attribute": "baz"},
            },
            True,
            ["foo", "bar"],
        ),
        ({"foo": {"this": "that"}}, False, []),
        ({"fooo": {"this": "that"}}, True, []),
        ({"foo": {"method": "auto"}}, True, ["foo"]),
    ],
)
def test_field_map_config_validator(config_dict, valid, expected_keys):
    validator = FieldsSectionValidator(Test)
    if valid:
        valid_config = validator.validate(**config_dict)
        assert sorted(valid_config.keys()) == sorted(expected_keys)
        for value in valid_config.values():
            assert isinstance(value, FieldMapConfig)
    else:
        with pytest.raises(ValueError):
            validator.validate(**config_dict)
