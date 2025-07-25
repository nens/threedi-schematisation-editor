from enum import Enum, IntEnum
from typing import Optional

from threedi_schematisation_editor.utils import convert_to_type, TypeConversionError, get_type_for_casting

import pytest


# Define example Enum and IntEnum classes for testing
class TestEnum(Enum):
    OPTION1 = "option1"


class TestIntEnum(IntEnum):
    ONE = 1


@pytest.mark.parametrize('full_type', [str, Optional[str]])
def test_get_type_for_casting(full_type):
    assert get_type_for_casting(full_type) == str


@pytest.mark.parametrize('value,field_type,expected_value',
                         [
                             # Original test cases
                             (1, int, 1),
                             (1.0, int, 1),
                             (1.1, int, 1),
                             (1, float, 1.0),
                             (1.0, float, 1.0),
                             (1, str, '1'),
                             ('1', str, '1'),
                             (1, bool, True),
                             (True, bool, True),
                             (None, Optional[int], None),
                             # enum contents are not checked, but values are just casted
                             ("option2", TestEnum, "option2"),
                             (2, TestIntEnum, 2),
                         ]
                         )
def test_convert_to_type(value, field_type, expected_value):
    assert convert_to_type(value, field_type) == expected_value


# anything can be casted to bool or int, so these are not tested
@pytest.mark.parametrize('field_type,', [int, float, TestIntEnum])
def test_convert_to_type_invalid(field_type):
    with pytest.raises(TypeConversionError):
        convert_to_type('foo', field_type)
