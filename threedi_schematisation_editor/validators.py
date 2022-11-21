# Copyright (C) 2022 by Lutra Consulting
import threedi_schematisation_editor.enumerators as en
from functools import cached_property
from itertools import chain
from qgis.core import NULL


class ValidationAutofix:
    """Validation autofix object."""

    def __init__(self, field_name, fixed_value):
        self.field_name = field_name
        self.fixed_value = fixed_value


class FieldValidationError:
    """Structure with field validation output."""

    def __init__(self, data_model_cls, feature_id, source_id, field_name, current_value, error_message=None):
        self.data_model_cls = data_model_cls
        self.feature_id = feature_id
        self.source_id = source_id
        self.field_name = field_name
        self.current_value = current_value
        self.error_message = error_message
        self.fixes = []

    def add_autofix(self, fixed_value, field_name=None):
        """Add autofix object with proposed value."""
        fix = ValidationAutofix(field_name if field_name else self.field_name, fixed_value)
        self.fixes.append(fix)


class AttributeValidator:
    """Abstract class of field validator."""

    FIELD_NAME = None
    FIELD_INDEX = None

    def __init__(self, handler, feature, autofix=False):
        self.handler = handler
        self.feature = feature
        self.autofix = autofix
        self.validation_errors = []

    @property
    def model(self):
        """Return associated handler base model class."""
        return self.handler.MODEL

    @property
    def layer(self):
        """Return associated handler layer."""
        return self.handler.layer

    @property
    def field_name(self):
        """Return validated field name."""
        return self.FIELD_NAME

    @cached_property
    def field_index(self):
        """Return validated field index."""
        if self.FIELD_INDEX is None:
            field_idx = self.handler.field_indexes[self.field_name]
        else:
            field_idx = self.FIELD_INDEX
        return field_idx

    @cached_property
    def id(self):
        """Return validated feature source ID."""
        return self.feature["id"]

    @cached_property
    def fid(self):
        """Return validated feature ID."""
        return self.feature.id()

    @cached_property
    def field_value(self):
        """Return validated field value."""
        field_value = self.feature[self.field_name]
        return field_value

    @property
    def empty_values(self):
        """Return empty values representation set."""
        return {None, NULL, ""}

    @property
    def validation_methods(self):
        """Return available validations method list."""
        available_methods = []
        return available_methods

    def clear(self):
        """Clear validation errors list."""
        self.validation_errors.clear()


class CrossSectionTableValidator(AttributeValidator):
    """'cross_section_table' field validator."""

    FIELD_NAME = "cross_section_table"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.invalid_format_detected = False

    @cached_property
    def cross_section_table_rows(self):
        """Return 'cross_section_table' rows."""
        split_values = [row for row in self.field_value.strip().split("\n")]
        return split_values

    @cached_property
    def cross_section_table_values(self):
        """Return 'cross_section_table' values tuples."""
        split_values = []
        for row in self.cross_section_table_rows:
            try:
                h, w = row.split(", ")
            except ValueError:
                h, w = row.split(",")
            split_values.append([h.strip(), w.strip()])
        return split_values

    @property
    def validation_methods(self):
        """Return available validations method list."""
        available_methods = []
        shape = self.feature["cross_section_shape"]
        if shape in {en.CrossSectionShape.TABULATED_RECTANGLE.value, en.CrossSectionShape.TABULATED_TRAPEZIUM.value}:
            available_methods += [
                self._not_empty,
                self._valid_format,
                self._no_trailing_blank_chars,
                self._no_dot_separator,
            ]
        return available_methods

    def _not_empty(self):
        """Check if field value is not empty."""
        error_msg = f"'{self.field_name}' value is NULL"
        if self.field_value in self.empty_values:
            validation_error = FieldValidationError(
                self.model, self.fid, self.id, self.field_name, self.field_value, error_msg
            )
            if self.autofix:
                validation_error.add_autofix(NULL, "cross_section_width")
                validation_error.add_autofix(NULL, "cross_section_height")
            self.validation_errors.append(validation_error)

    def _valid_format(self):
        """Check if field value have format that can be parsed."""
        error_msg = f"'{self.field_name}' value have invalid format"
        if self.field_value not in self.empty_values:
            try:
                _float_values = [
                    (float(h.replace(",", ".")), float(w.replace(",", "."))) for h, w in self.cross_section_table_values
                ]
            except ValueError:
                validation_error = FieldValidationError(
                    self.model, self.fid, self.id, self.field_name, self.field_value, error_msg
                )
                self.validation_errors.append(validation_error)
                self.invalid_format_detected = True

    def _no_trailing_blank_chars(self):
        """Check if field value have no trailing blank characters."""
        error_msg = f"'{self.field_name}' value have trailing whitespaces"
        if self.field_value not in self.empty_values and not self.invalid_format_detected:
            stripped_field_value = self.field_value.rstrip()
            if self.field_value != stripped_field_value:
                validation_error = FieldValidationError(
                    self.model, self.fid, self.id, self.field_name, self.field_value, error_msg
                )
                if self.autofix:
                    validation_error.add_autofix(stripped_field_value)
                self.validation_errors.append(validation_error)

    def _no_dot_separator(self):
        """Check if float values are dot separated."""
        error_msg = f"'{self.field_name}' value contains coma-separated float numbers"
        if self.field_value not in self.empty_values and not self.invalid_format_detected:
            for value in chain.from_iterable(self.cross_section_table_values):
                if "," in value:
                    validation_error = FieldValidationError(
                        self.model, self.fid, self.id, self.field_name, self.field_value, error_msg
                    )
                    if self.autofix:
                        fixed_values_list = [
                            (h.replace(",", "."), w.replace(",", ".")) for h, w in self.cross_section_table_values
                        ]
                        fixed_field_value = "\n".join(f"{h}, {w}" for h, w in fixed_values_list)
                        validation_error.add_autofix(fixed_field_value)
                    self.validation_errors.append(validation_error)
                    break
