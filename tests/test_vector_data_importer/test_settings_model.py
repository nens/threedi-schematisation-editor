from dataclasses import MISSING, Field, dataclass, field, fields
from typing import Optional

import pytest
from pydantic import ValidationError

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


@pytest.mark.parametrize(
    "config_dict",
    [
        {"method": ColumnImportMethod.AUTO, "source_attribute": "foo"},
        {"method": ColumnImportMethod.IGNORE},
        {"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": "foo"},
        {"method": ColumnImportMethod.EXPRESSION, "expression": "foo"},
        {"method": ColumnImportMethod.DEFAULT, "default_value": "foo"},
    ],
)
def test_field_map_config_valid(config_dict):
    assert sm.FieldMapConfig(**config_dict)


@pytest.mark.parametrize(
    "config_dict",
    [
        {"method": ColumnImportMethod.ATTRIBUTE},
        {"method": ColumnImportMethod.EXPRESSION},
        {"method": ColumnImportMethod.DEFAULT},
    ],
)
def test_field_map_config_invalid(config_dict):
    with pytest.raises(ValidationError) as exc_info:
        sm.FieldMapConfig(**config_dict)
    assert exc_info.value.errors()[0]["type"] == "value_error.missing"


@dataclass
class Test:
    foo: int
    bar: str


def test_create_field_map_config():
    allowed_methods = [ColumnImportMethod.AUTO]
    config = sm.create_field_map_config(allowed_methods)
    assert config._metadata.allowed_methods == allowed_methods
    # check if validator works as expected
    with pytest.raises(ValueError):
        config(method=ColumnImportMethod.IGNORE)
    valid_config = config(method=ColumnImportMethod.AUTO)
    assert isinstance(valid_config, sm.FieldMapConfig)


class TestGetAllowedMethodsForModelClassField:
    @staticmethod
    def get_metadata(allowed_methods):
        metadata = {}
        if allowed_methods:
            metadata[dm.ALLOWED_METHODS_FIELD] = allowed_methods
        return metadata

    @pytest.mark.parametrize("is_optional", [False, True])
    @pytest.mark.parametrize(
        "allowed_methods",
        [None, [ColumnImportMethod.IGNORE], [ColumnImportMethod.DEFAULT]],
    )
    def test_optional(self, is_optional, allowed_methods):
        # By not including metadata in this test we test for the case where all methods are allowed
        # If allowed or excluded fields are specified, IGNORE may not be allowed even for an optional type
        @dataclass
        class Test:
            foo: Optional[str] if is_optional else str = field(
                metadata=self.get_metadata(allowed_methods)
            )

        allowed_methods = sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
        assert (ColumnImportMethod.IGNORE in allowed_methods) == is_optional

    @pytest.mark.parametrize(
        "allowed_methods, expected_methods",
        [
            (None, [ColumnImportMethod.AUTO]),
            ([ColumnImportMethod.ATTRIBUTE], [ColumnImportMethod.ATTRIBUTE]),
        ],
    )
    def test_id(self, allowed_methods, expected_methods):
        # ID fields without allowed methods only have an AUTO method as return
        @dataclass
        class Test:
            id: str = field(metadata=self.get_metadata(allowed_methods))

        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == expected_methods
        )

    def test_default(self):
        @dataclass
        class Test:
            foo: Optional[str]

        default_allowed = [
            method for method in ColumnImportMethod if method != ColumnImportMethod.AUTO
        ]
        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == default_allowed
        )

    def test_allowed(self):
        allowed_methods = [ColumnImportMethod.ATTRIBUTE]
        metadata = self.get_metadata(allowed_methods=allowed_methods)

        @dataclass
        # test with optional so excluded methods is not modified
        class Test:
            foo: Optional[str] = field(metadata=metadata)

        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == allowed_methods
        )


def test_get_settings_model():
    models = [
        sm.ConnectionNodeSettings,
        sm.IntegrationSettings,
        sm.CrossSectionDataRemap,
        sm.CrossSectionLocationSettings,
        sm.PointToLineSettings,
    ]
    settings_dict = {model.name: model() for model in models}
    settings_model = sm.ImportSettings(**settings_dict)
    for model_name in settings_dict:
        assert hasattr(settings_model, model_name)
        assert getattr(settings_model, model_name) == settings_dict[model_name]


def test_field_map_config_method_validation():
    # Test valid method with allowed methods
    metadata = sm.FieldMapMetadata(allowed_methods=[ColumnImportMethod.EXPRESSION])

    config_cls = sm.FieldMapConfig.with_metadata(metadata)
    config = config_cls(
        method=ColumnImportMethod.EXPRESSION,
        expression="foo",
    )
    assert config.method == ColumnImportMethod.EXPRESSION

    with pytest.raises(ValidationError) as exc_info:
        config_cls(
            method=ColumnImportMethod.DEFAULT,
            default_value="foo",
        )

    assert exc_info.value.errors()[0]["type"] == "value_error.invalid"
