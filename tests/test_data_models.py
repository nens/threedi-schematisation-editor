from dataclasses import dataclass, field

from threedi_schematisation_editor.data_models import DISPLAY_NAME_FIELD, ModelObject


@dataclass
class Test(ModelObject):
    id: int = field(metadata={DISPLAY_NAME_FIELD: "ID"})
    code: str = field(metadata={DISPLAY_NAME_FIELD: "Code"})
    display_name: str = field(metadata={DISPLAY_NAME_FIELD: "Display name"})
    foo: int


def test_display_names():
    assert Test.display_names() == ["ID", "Code", "Display name", "foo"]
