from dataclasses import dataclass

import pytest

import threedi_schematisation_editor.data_models as dm
from threedi_schematisation_editor.vector_data_importer.dialogs.import_widgets import (
    ColumnImportMethod,
    create_widgets,
    get_field_methods_mapping,
)


@dataclass
class Model(dm.ModelObject):
    id: int
    text: str
    value: float
    auto_field: str
    auto_attr_field: str
    required_field: str
    no_default_field: str

    @staticmethod
    def display_names() -> list:
        return [
            "ID",
            "Text",
            "Value",
            "Auto Field",
            "Auto Attr Field",
            "Required Field",
            "No Default Field",
        ]


@dataclass
class NodeModel(dm.ModelObject):
    id: int
    text: str
    value: float

    @staticmethod
    def display_names() -> list:
        return ["ID", "Text"]

    @staticmethod
    def obsolete_fields() -> set:
        return ["text"]


class SimpleModel(dm.ModelObject):
    id: int
    value: float

    @staticmethod
    def display_names() -> list:
        return ["Value"]


def test_create_widgets_single_row(qgis_application):
    widgets = create_widgets(
        NodeModel,
    )
    # There should be one row of 6 widgets for NodeModel
    assert len(widgets) == 6
    assert all(key[0] == 0 for key in widgets.keys())
    label = widgets[(0, 0)]
    assert label.text().strip() == "ID"


def test_get_field_methods_mapping_defaults():
    methods_mapping = get_field_methods_mapping(SimpleModel)
    assert methods_mapping["value"] == [
        ColumnImportMethod.ATTRIBUTE,
        ColumnImportMethod.DEFAULT,
        ColumnImportMethod.EXPRESSION,
        ColumnImportMethod.IGNORE,
    ]
    assert methods_mapping["id"] == [ColumnImportMethod.AUTO]


def test_get_field_methods_mapping_field_spec():
    methods_mapping = get_field_methods_mapping(
        SimpleModel,
        field_spec={
            "value": [ColumnImportMethod.ATTRIBUTE, ColumnImportMethod.DEFAULT]
        },
    )
    assert methods_mapping["value"] == [
        ColumnImportMethod.ATTRIBUTE,
        ColumnImportMethod.DEFAULT,
    ]
    assert methods_mapping["id"] == [ColumnImportMethod.AUTO]
