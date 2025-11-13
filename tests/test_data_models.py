from dataclasses import dataclass, field

import pytest

from threedi_schematisation_editor.data_models import (
    DISPLAY_NAME_FIELD,
    DISPLAY_UNIT_FIELD,
    ModelObject,
)


@dataclass
class Test(ModelObject):
    id: int = field(metadata={DISPLAY_NAME_FIELD: "ID"})
    code: str = field(metadata={DISPLAY_NAME_FIELD: "Code"})
    display_name: str = field(metadata={DISPLAY_NAME_FIELD: "Display name"})
    value: float = field(metadata={DISPLAY_UNIT_FIELD: "m3/s"})
    foo: int


@pytest.mark.parametrize(
    "field_name, expected_display_name",
    [
        ("id", "ID"),
        ("code", "Code"),
        ("display_name", "Display name"),
        ("some id", "Some ID"),
    ],
)
def test_default_display_name(field_name, expected_display_name):
    assert Test.default_display_name(field_name) == expected_display_name


def test_display_names():
    assert Test.display_names() == ["ID", "Code", "Display name", "Value [m3/s]", "Foo"]
