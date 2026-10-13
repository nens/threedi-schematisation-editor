---
feature: allow-custom-id-methods
status: complete
created: 2026-07-07
chunk_size: medium
total_tasks: 6
estimated_lines: 330
---

# Allow Custom ID Methods — Tasks

## Overview

Allows users to set the `id` field of imported features using ATTRIBUTE, EXPRESSION, or DEFAULT methods (in addition to AUTO). Conflict detection skips features whose resolved ID already exists in the target layer or was already assigned in the same import batch, emitting a `FeaturesImporterWarning`.

## Task List

### Foundation

#### Task 1: `FeatureManager` — add `used_ids` + `explicit_id` support
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/utils.py`, `tests/vector_data_importer/test_utils.py`
- **Description:**
  - Add `get_existing_ids(layer)` helper that returns `set(layer.uniqueValues(id_idx))`
  - Update `FeatureManager.__init__` to accept `existing_ids=None`; populate `self.used_ids = set(existing_ids) if existing_ids else set()`
  - Update `FeatureManager.add_feature` to accept `explicit_id=None`:
    - `explicit_id` provided + in `used_ids` → warn (`FeaturesImporterWarning`) + return `None`
    - `explicit_id` provided + not in `used_ids` → set `new_feat["id"] = explicit_id`, add to `used_ids`, return `new_feat`
    - `explicit_id=None` (AUTO) → skip IDs in `used_ids`, assign `next_id`, add to `used_ids`, advance `next_id`
  - Update `FeatureManager.create_new` to accept and thread `explicit_id` through; return `None` on conflict
  - Keep `set_id=True/False` for backward compatibility with integrator call sites
  - Tests: conflict detection, intra-batch dedup, AUTO skips already-used IDs, existing `set_id=False` behaviour unchanged
- **Depends on:** None
- **Acceptance:** `test_utils.py` tests for `FeatureManager` pass; existing tests unchanged
- **Evidence:** `pytest tests/vector_data_importer/test_utils.py -q --tb=short` passes

---

#### Task 2: `settings_models.py` — allow non-AUTO methods for `id` [P]
- **Estimate:** ~30 lines
- **Parallel:** Can run with Task 1
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`, `tests/vector_data_importer/test_settings_model.py`
- **Description:**
  - In `get_allowed_methods_for_model_class_field`, replace the branch:
    ```python
    if model_field.name == "id":
        allowed_methods = [ColumnImportMethod.AUTO]
    ```
    with:
    ```python
    if model_field.name == "id":
        allowed_methods = [
            m for m in ColumnImportMethod
            if m not in (ColumnImportMethod.IGNORE, ColumnImportMethod.DEFAULT)
        ]
    ```
    This yields `[AUTO, ATTRIBUTE, EXPRESSION]`. The existing non-optional guard then has nothing to remove (IGNORE is already excluded). AUTO stays first because it is first in the enum definition.
  - Update `test_id` in `test_settings_model.py`: the parametrize case `(None, [AUTO])` becomes `(None, [AUTO, ATTRIBUTE, EXPRESSION, DEFAULT])`; the docstring "only have AUTO" is updated accordingly
- **Depends on:** None
- **Acceptance:** `test_settings_model.py` passes; `test_id` reflects new allowed methods
- **Evidence:** `pytest tests/vector_data_importer/test_settings_model.py -q --tb=short` passes

---

### Core Implementation

#### Task 3: `resolve_id` helper + `update_attributes` skip `id`
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/utils.py`, `tests/vector_data_importer/test_utils.py`
- **Description:**
  - Add `resolve_id(fields_configuration, src_feat, expression_context=None)` to `utils.py`:
    - Reads `fields_configuration.get("id")`; if absent or method is AUTO → return `(None, False)`
    - Otherwise calls `get_field_config_value` for the id config
    - If result is NULL/None → warn + return `(None, True)`
    - Calls `convert_to_type(result, int)`; on `TypeConversionError` → warn + return `(None, True)`
    - On success → return `(explicit_id, False)`
  - Update `update_attributes` to skip `id` unconditionally (add `or field_name == "id"` to the AUTO-skip guard) — the id is now always handled before `create_new`
  - Tests: AUTO → `(None, False)`; no id config → `(None, False)`; NULL value → `(None, True)` + warning; non-int value → `(None, True)` + warning; valid int → `(resolved_id, False)`
- **Depends on:** Task 1, Task 2
- **Acceptance:** new `resolve_id` tests pass; `update_attributes` no longer touches `id` field
- **Evidence:** `pytest tests/vector_data_importer/test_utils.py -q --tb=short` passes

---

### Integration

#### Task 4: Wire `explicit_id` into processor call sites
- **Estimate:** ~70 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:**
  - In `SpatialProcessor.__init__`, update `FeatureManager` construction to pass `existing_ids=get_existing_ids(target_layer)`
  - Update 5 `process_feature` methods to use `resolve_id` before calling `create_new`:
    - `ConnectionNodeProcessor.process_feature`
    - `PointProcessor.process_feature`
    - `LineProcessor.process_feature`
    - `CrossSectionLocationProcessor.process_feature`
    - `SurfaceProcessor.process_feature`
  - Pattern per call site:
    ```python
    explicit_id, skip = resolve_id(self.fields_configuration, src_feat)
    if skip:
        return {}
    new_feat = self.target_manager.create_new(new_geom, self.target_fields, explicit_id=explicit_id)
    if new_feat is None:  # conflict detected inside FeatureManager
        return {}
    ```
  - `node_manager`, `surface_map_manager`, `integrate_manager` are left unchanged (always AUTO)
- **Depends on:** Task 1, Task 3
- **Acceptance:** existing processor tests still pass; processors return `{}` on ID conflict
- **Evidence:** `pytest tests/vector_data_importer/test_processors.py tests/vector_data_importer/test_processors_surface.py -q --tb=short` passes

---

#### Task 5: Integration tests — end-to-end ID conflict behaviour
- **Estimate:** ~65 lines
- **Files:** `tests/vector_data_importer/test_processors.py`
- **Description:**
  - Test: ATTRIBUTE method for `id`, no conflicts → all features imported with correct IDs
  - Test: ATTRIBUTE method for `id`, one source ID already in target layer → conflicting feature skipped, `FeaturesImporterWarning` emitted, others imported
  - Test: intra-batch conflict (two source features share the same custom ID) → second skipped with `FeaturesImporterWarning`
  - Test: AUTO method still works unchanged after the refactor (regression guard)
- **Depends on:** Task 4
- **Acceptance:** all 4 new tests pass; no regressions in existing test suite
- **Evidence:** `pytest tests/vector_data_importer/ -q --tb=short` passes

---

#### Task 6: Restrict `id` to AUTO for `connection_node_fields`
- **Estimate:** ~55 lines
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/settings_models.py`
  - `threedi_schematisation_editor/vector_data_importer/processing/algorithms_vector_data_importer.py`
  - `threedi_schematisation_editor/vector_data_importer/wizard/pages.py`
  - `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py`
  - `tests/vector_data_importer/test_settings_model.py`
  - `tests/vector_data_importer/test_wizard.py`
- **Description:**
  - `settings_models.py`: Add `allow_non_auto_id=True` parameter to `validate_field_map`. When `False`, if `"id"` is present in the field map with a method other than `None`/`AUTO`, raise `ValueError("The 'id' field in connection_node_fields must use AUTO method.")`
  - `algorithms_vector_data_importer.py`: Update the `validate_field_map` call for `connection_node_fields` to pass `allow_non_auto_id=False`
  - `wizard/pages.py` — `FieldMapPage.__init__`: Add `restrict_id_to_auto=False` parameter. In `create_rows()`, when `field_name == "id"` and `restrict_id_to_auto` is `True`, override the config class: `config_class = create_field_map_config([ColumnImportMethod.AUTO], field_type=int)`
  - `wizard/wizard.py`: Update the `FieldMapPage` instantiation for `connection_node_fields` to pass `restrict_id_to_auto=True`
  - Tests:
    - `test_settings_model.py`: `validate_field_map` with `allow_non_auto_id=False` raises on ATTRIBUTE/EXPRESSION/DEFAULT method for `id`; passes for AUTO and for `fields` without the flag
    - `test_wizard.py`: `FieldMapPage` with `restrict_id_to_auto=True` offers only `[AUTO]` for the `id` row; without the flag the full set is offered
- **Depends on:** Task 2
- **Acceptance:** Non-AUTO method for `id` in `connection_node_fields` is rejected at both validation and UI level; `fields` targeting a connection node as primary target is unaffected
- **Evidence:** `pytest tests/vector_data_importer/test_settings_model.py tests/vector_data_importer/test_wizard.py -q --tb=short` passes

---

## Notes

- `set_id=True/False` on `add_feature` is preserved as-is for backward compatibility with integrator call sites (`integrators.py` line 440: `add_feature(..., set_id=(i > 0))`). No integrator changes needed.
- AUTO remains the first option in the UI because `ColumnImportMethod.AUTO` is first in the enum definition and `get_allowed_methods_for_model_class_field` sorts by enum order.
- `resolve_id` is extracted as a shared helper because it is called from 5 processor `process_feature` methods (meets the 3+ duplication threshold from the constitution).

## Deferred

- Per-model `allowed_methods` metadata on the `id` field — not needed; all models use the same rule.

## Progress

- [x] Task 1: `FeatureManager` — `used_ids` + `explicit_id` support
- [x] Task 2: `settings_models.py` — allow non-AUTO methods for `id`
- [x] Task 3: `resolve_id` helper + `update_attributes` skip `id`
- [x] Task 4: Wire `explicit_id` into processor call sites
- [x] Task 5: Integration tests — end-to-end ID conflict behaviour
- [x] Task 6: Restrict `id` to AUTO for `connection_node_fields`
