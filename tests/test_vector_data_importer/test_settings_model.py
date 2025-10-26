from dataclasses import MISSING, Field, dataclass, field, fields
from typing import Optional

import pytest

import threedi_schematisation_editor.data_models as dm
import threedi_schematisation_editor.vector_data_importer.settings_models as sm
from threedi_schematisation_editor.vector_data_importer.utils import ColumnImportMethod


@pytest.mark.parametrize(
    "config_dict,expected_error",
    [
        ({"method": ColumnImportMethod.AUTO, "source_attribute": "foo"}, None),
        ({"method": ColumnImportMethod.IGNORE}, None),
        (
            {"method": ColumnImportMethod.ATTRIBUTE},
            sm.FieldMapConfigSourceAttributeMissingError,
        ),
        ({"method": ColumnImportMethod.ATTRIBUTE, "source_attribute": "foo"}, None),
        (
            {
                "method": "source_attribute",
                "source_attribute": "foo",
                "default_value": "bar",
            },
            None,
        ),
        (
            {"method": ColumnImportMethod.EXPRESSION},
            sm.FieldMapConfigExpressionMissingError,
        ),
        ({"method": ColumnImportMethod.EXPRESSION, "expression": "foo"}, None),
        (
            {
                "method": ColumnImportMethod.EXPRESSION,
                "expression": "foo",
                "default_value": "bar",
            },
            None,
        ),
        (
            {"method": ColumnImportMethod.DEFAULT},
            sm.FieldMapConfigDefaultValueMissingError,
        ),
        ({"method": ColumnImportMethod.DEFAULT, "default_value": "foo"}, None),
        ({}, sm.FieldMapConfigMethodMissingError),
    ],
)
def test_field_map_config(config_dict, expected_error):
    if not expected_error:
        assert sm.FieldMapConfig(**config_dict)
    else:
        with pytest.raises(ValueError):
            sm.FieldMapConfig(**config_dict)


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
    validator = sm.FieldsSectionValidator(Test)
    if valid:
        valid_config = validator.validate(**config_dict)
        assert sorted(valid_config.keys()) == sorted(expected_keys)
        for value in valid_config.values():
            assert isinstance(value, sm.FieldMapConfig)
    else:
        with pytest.raises(ValueError):
            validator.validate(**config_dict)


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
    def get_metadata(allowed_methods, excluded_methods):
        metadata = {}
        if allowed_methods:
            metadata[dm.ALLOWED_METHODS_FIELD] = allowed_methods
        if excluded_methods:
            metadata[dm.EXLUCDED_METHODS_FIELD] = excluded_methods
        return metadata

    @pytest.mark.parametrize("is_optional", [False, True])
    @pytest.mark.parametrize("allowed_methods", [None, [ColumnImportMethod.IGNORE]])
    def test_optional(self, is_optional, allowed_methods):
        # By not including metadata in this test we test for the case where all methods are allowed
        # If allowed or excluded fields are specified, IGNORE may not be allowed even for an optional type
        @dataclass
        class Test:
            foo: Optional[str] if is_optional else str = field(
                metadata=self.get_metadata(allowed_methods, None)
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
            id: str = field(metadata=self.get_metadata(allowed_methods, None))

        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == expected_methods
        )

    def test_excluded(self):
        excluded_methods = [ColumnImportMethod.AUTO, ColumnImportMethod.ATTRIBUTE]
        metadata = self.get_metadata(
            allowed_methods=None, excluded_methods=excluded_methods
        )

        @dataclass
        # test with optional so excluded methods is not modified
        class Test:
            foo: Optional[str] = field(metadata=metadata)

        allowed_methods = sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
        for method in excluded_methods:
            assert method not in allowed_methods

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
        metadata = self.get_metadata(
            allowed_methods=allowed_methods, excluded_methods=None
        )

        @dataclass
        # test with optional so excluded methods is not modified
        class Test:
            foo: Optional[str] = field(metadata=metadata)

        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == allowed_methods
        )

    @pytest.mark.parametrize(
        "allowed_methods, excluded_methods, expected_methods",
        [
            ([ColumnImportMethod.ATTRIBUTE], None, [ColumnImportMethod.ATTRIBUTE]),
            ([ColumnImportMethod.ATTRIBUTE], [ColumnImportMethod.ATTRIBUTE], []),
            (
                [ColumnImportMethod.ATTRIBUTE],
                [ColumnImportMethod.IGNORE],
                [ColumnImportMethod.ATTRIBUTE],
            ),
        ],
    )
    def test_allowed_and_excluded(
        self, allowed_methods, excluded_methods, expected_methods
    ):
        @dataclass
        # test with optional so excluded methods is not modified
        class Test:
            foo: Optional[str] = field(
                metadata=self.get_metadata(allowed_methods, excluded_methods)
            )

        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == expected_methods
        )


def test_get_settings_model():
    models = [
        sm.ConnectionNodeSettingsModel,
        sm.IntegrationSettingsModel,
        sm.CrossSectionDataRemapModel,
        sm.CrossSectionLocationSettingsModel,
        sm.PointToLineSettingsModel,
    ]
    settings_dict = {model.name: model() for model in models}
    settings_model = sm.ConversionSettingsModel(**settings_dict)
    for model_name in settings_dict:
        assert hasattr(settings_model, model_name)
        assert getattr(settings_model, model_name) == settings_dict[model_name]
