from dataclasses import dataclass, field, fields, make_dataclass
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


def test_create_field_map_config_with_type():
    allowed_methods = [ColumnImportMethod.IGNORE, ColumnImportMethod.DEFAULT]
    config = sm.create_field_map_config(allowed_methods, field_type=Optional[int])
    valid_config = config(method=ColumnImportMethod.IGNORE)
    assert valid_config.model_fields["default_value"].annotation.__args__[0] == int


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
            (
                None,
                [
                    ColumnImportMethod.AUTO,
                    ColumnImportMethod.ATTRIBUTE,
                    ColumnImportMethod.EXPRESSION,
                ],
            ),
            ([ColumnImportMethod.ATTRIBUTE], [ColumnImportMethod.ATTRIBUTE]),
        ],
    )
    def test_id(self, allowed_methods, expected_methods):
        # ID fields without allowed methods allow all methods except IGNORE
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

    @pytest.mark.parametrize(
        "optional, is_id",
        [
            (True, False),
            (False, False),
            (False, True),
        ],
    )
    def test_allowed(self, optional, is_id):
        allowed_methods = [ColumnImportMethod.ATTRIBUTE]
        metadata = self.get_metadata(allowed_methods=allowed_methods)
        expected_allowed_methods = allowed_methods.copy()
        if optional:
            expected_allowed_methods.append(ColumnImportMethod.IGNORE)
        Test = make_dataclass(
            "Test",
            [
                (
                    "id" if is_id else "foo",
                    Optional[str] if optional else str,
                    field(metadata=metadata),
                )
            ],
        )
        print(f"{optional=}, {is_id=}")
        print(f"{expected_allowed_methods=}")
        print(sm.get_allowed_methods_for_model_class_field(fields(Test)[0]))
        assert (
            sm.get_allowed_methods_for_model_class_field(fields(Test)[0])
            == expected_allowed_methods
        )

    @pytest.mark.parametrize(
        "optional, is_id",
        [
            (True, False),
            (False, False),
            (False, True),
        ],
    )
    def test_allowed_use_generic_allowed_methods(self, optional, is_id):
        metadata = self.get_metadata(allowed_methods=[ColumnImportMethod.ATTRIBUTE])
        expected_allowed_methods = ColumnImportMethod.all()
        if not is_id:
            expected_allowed_methods.remove(ColumnImportMethod.AUTO)
        if (not optional) or is_id:
            expected_allowed_methods.remove(ColumnImportMethod.IGNORE)
        if is_id:
            expected_allowed_methods.remove(ColumnImportMethod.DEFAULT)
        Test = make_dataclass(
            "Test",
            [
                (
                    "id" if is_id else "foo",
                    Optional[str] if optional else str,
                    field(metadata=metadata),
                )
            ],
        )
        allowed = sorted(
            sm.get_allowed_methods_for_model_class_field(
                fields(Test)[0], use_generic_allowed_methods=True
            )
        )
        assert allowed == sorted(expected_allowed_methods)


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


@pytest.mark.parametrize(
    "field_map",
    [
        {
            "id": sm.FieldMapConfig(
                method=ColumnImportMethod.ATTRIBUTE, source_attribute="src_id"
            )
        },
        {
            "id": sm.FieldMapConfig(
                method=ColumnImportMethod.EXPRESSION, expression="to_int('1')"
            )
        },
        {
            "id": sm.FieldMapConfig(
                method=ColumnImportMethod.DEFAULT, default_value="foo"
            )
        },
    ],
)
def test_validate_id_method_invalid(field_map):
    with pytest.raises(ValueError, match="AUTO method"):
        sm.validate_id_method(field_map)


def test_validate_field_map_generic_methods_ignore_model_metadata():
    field_map = {
        "id": {
            "method": ColumnImportMethod.ATTRIBUTE,
            "source_attribute": "source_id",
        },
        "surface_id": {
            "method": ColumnImportMethod.ATTRIBUTE,
            "source_attribute": "source_surface_id",
        },
        "connection_node_id": {
            "method": ColumnImportMethod.EXPRESSION,
            "expression": 'to_int("node_id")',
        },
    }

    with pytest.raises(ValidationError):
        sm.validate_field_map(field_map, dm.SurfaceMap)

    sm.validate_field_map(field_map, dm.SurfaceMap, use_generic_allowed_methods=True)
