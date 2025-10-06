from dataclasses import dataclass

import pytest

from threedi_schematisation_editor.vector_data_importer.settings_model import (
    FieldMapConfig,
    FieldsSectionValidator,
)


@pytest.mark.parametrize(
    "config_dict,valid",
    [
        ({"method": "auto", "source_attribute": "foo"}, True),
        ({"method": "ignore"}, True),
        ({"method": "source_attribute"}, False),
        ({"method": "source_attribute", "source_attribute": "foo"}, True),
        (
            {
                "method": "source_attribute",
                "source_attribute": "foo",
                "default_value": "bar",
            },
            True,
        ),
        ({"method": "expression"}, False),
        ({"method": "expression", "expression": "foo"}, True),
        ({"method": "expression", "expression": "foo", "default_value": "bar"}, True),
        ({"method": "default"}, False),
        ({"method": "default", "default_value": "foo"}, True),
        ({}, False),
    ],
)
def test_field_map_config(config_dict, valid):
    if valid:
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
