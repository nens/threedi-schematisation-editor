---
feature: feat_392_pump_linking_join
status: complete
created: 2026-07-20
chunk_size: medium
total_tasks: 4
estimated_lines: 150
---

# PumpLinkingSettings: Source/Target Join Fields — Tasks

## Overview

Replace `connection_node_id_end` in `PumpLinkingSettings` with `enabled` + `join_field_src`
+ `join_field_tgt`, following the `CrossSectionLocationSettings` pattern. Update the
processor, importer, and UI widget accordingly. Tests broken by Task 1 are fixed in
Tasks 2 and 3 respectively.

## Task List

### Foundation

#### Task 1: Update `PumpLinkingSettings` model
- **Estimate:** ~25 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Replace `connection_node_id_end` with `enabled: bool` (default `False`),
  `join_field_src: FieldMapConfig`, and `join_field_tgt: FieldMapConfig`. Remove
  `ColumnImportMethod.AUTO` from `allowed_methods`. Follow the exact structure of
  `CrossSectionLocationSettings`.
- **Depends on:** None
- **Acceptance:** Model can be instantiated; `enabled`, `join_field_src`, `join_field_tgt`
  are present; `connection_node_id_end` is gone.
- **Evidence:** Module imports without error. Note: `test_processors.py` and
  `test_conversion.py` will be broken after this task — that is expected and fixed in
  Tasks 2 and 3.

### Core Implementation

#### Task 2: Update `PumpProcessor` and fix processor unit tests [P]
- **Estimate:** ~50 lines
- **Parallel:** Can run with Task 3
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/processors.py`
  - `tests/vector_data_importer/test_processors.py`
- **Description:**
  - Add `node_mapping` `@cached_property` to `PumpProcessor` using `build_feature_mapping`
    on the node layer with `join_field_tgt`.
  - Rewrite `resolve_end_point` to check `pump_linking_settings.enabled`, look up
    `join_field_src` value in `node_mapping`, warn if not found, then fall back to
    point-to-line.
  - Update `test_attribute_mapping_takes_priority_over_point_to_line`: rewrite the
    `PumpLinkingSettings(connection_node_id_end=...)` construction to use
    `enabled=True, join_field_src=..., join_field_tgt=...`.
  - Verify `test_pump_only_when_no_end_point`, `test_point_to_line_creates_pump_and_pump_map`,
    and `test_pump_map_skipped_when_end_node_not_found` still pass unchanged (they do not
    use pump linking explicitly).
- **Depends on:** Task 1
- **Acceptance:** All `TestPumpProcessor` tests pass; attribute mapping test exercises the
  new `join_field_src` / `join_field_tgt` path.
- **Evidence:** `pytest tests/vector_data_importer/test_processors.py -q --tb=short`

#### Task 3: Update `PumpsImporter` and fix integration test [P]
- **Estimate:** ~30 lines
- **Parallel:** Can run with Task 2
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/importers.py`
  - `tests/vector_data_importer/test_conversion.py` (and its import config fixture)
- **Description:**
  - In `PumpsImporter.build_pump_map_source_layer`, replace the `get_feature_by_id`
    lookup with `build_feature_mapping` + `get_field_config_value`, guarded by
    `if settings.enabled`.
  - Update the `import_pumps` import config fixture (JSON/dict used by
    `test_import_pumps`) to use the new settings shape: `enabled`, `join_field_src`,
    `join_field_tgt` instead of `connection_node_id_end`.
  - The expected outcome (4 pumps, 3 pump_maps, same geometries) is unchanged; the ref
    gpkg does not need updating.
- **Depends on:** Task 1
- **Acceptance:** `test_import_pumps` passes; case a (end node resolved by attribute
  mapping) still produces a pump_map linked to the correct connection node.
- **Evidence:** `pytest tests/vector_data_importer/test_conversion.py::test_import_pumps -q --tb=short`

### Integration & Polish

#### Task 4: Update `PumpLinkingSettingsWidget` UI
- **Estimate:** ~45 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:**
  - Replace the single `connection_node_id_end` `FieldMapRow` with two rows:
    `join_field_src` ("Join field in import layer") and `join_field_tgt` ("Join field in
    connection node layer").
  - Add an "Enable connection node mapping" checkbox via `get_extra_layout()` (same
    extension point used by `CrossSectionLocationMappingSettingsWidget` for snap distance).
  - Wire `join_field_tgt` attribute dropdown to `dm.ConnectionNode` via
    `set_fixed_source_attributes_from_data_model("join_field_tgt", dm.ConnectionNode)`.
  - Connect checkbox toggle to `field_map_widget.setEnabled(checked)` and update
    `self.model.enabled`.
  - Update `group_name` to `"Pump to Connection Node linking settings"`.
- **Depends on:** Task 1
- **Acceptance:** Widget renders with checkbox and two field map rows; unchecking disables
  rows; `join_field_tgt` dropdown lists connection node attributes; settings serialise
  correctly when read back.
- **Evidence:** Existing wizard tests pass; manual smoke test in the plugin UI.

## Notes

- Tasks 2 and 3 intentionally break after Task 1 and are fixed independently — do not
  run the full test suite after Task 1 alone.
- The ref gpkg (`tests/.../ref/test_import_pumps.gpkg`) does not need to change because
  the expected import output (geometries, counts) is identical under the new settings.
- The `_make_pump_processor` helper in `test_processors.py` (line 472) passes a
  `pump_linking` kwarg — check whether it needs updating alongside the test that uses it.

## Progress
- [x] Task 1: Update `PumpLinkingSettings` model
- [x] Task 2: Update `PumpProcessor` and fix processor unit tests
- [x] Task 3: Update `PumpsImporter` and fix integration test
- [x] Task 4: Update `PumpLinkingSettingsWidget` UI
