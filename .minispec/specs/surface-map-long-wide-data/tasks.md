---
feature: surface-map-long-wide-data
status: complete
created: 2026-07-01
chunk_size: medium
total_tasks: 7
estimated_lines: 360
---

# Surface Map Long/Wide Data Support — Tasks

## Overview

Merge `SurfaceMapPercentageSettings` + `SurfaceLinkingSettings` into `SurfaceMapSettings`,
replace the two existing widgets with a single `SurfaceMapSettingsWidget`, and update
`SurfaceProcessor` to handle both long and wide input data.

## Task List

### Foundation

#### Task 1: Merge settings models
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Add `SurfaceMapSettings` combining the fields of `SurfaceMapPercentageSettings`
  and `SurfaceLinkingSettings` plus new fields (`data_format`, `percentage_column`,
  `sewage_type_column`, `use_sewage_type_for_attribute_match`). Remove the two old classes.
  Update `ImportSettings` to use `surface_map: SurfaceMapSettings` (drop `surface_map_percentage`
  and `surface_linking` keys). No backward compatibility required.
- **Depends on:** None
- **Acceptance:** `ImportSettings` instantiates with default values; old class names are gone.
- **Evidence:** `pytest tests/ -q --tb=short` passes (update any tests referencing old models).

#### Task 2: Update wizard wiring (stub)
- **Estimate:** ~30 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py`
- **Description:** Update imports to remove old widget names; add a stub import for
  `SurfaceMapSettingsWidget` (can be a placeholder class at this point). Replace the two old
  widget references at lines 617–618 and the `surface_linking` reference at line 633 with the
  new single widget and `surface_map` settings key.
- **Depends on:** Task 1
- **Acceptance:** Wizard module imports without error.
- **Evidence:** `python -c "from threedi_schematisation_editor.vector_data_importer.wizard import wizard"` succeeds.

### Core Implementation

#### Task 3: SurfaceMapSettingsWidget — format toggle + long data section [P]
- **Estimate:** ~70 lines
- **Parallel:** Can run with Task 4
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Add `SurfaceMapSettingsWidget` class (stub `update_model`/`is_valid` for now).
  Implement the data format radio buttons (Long / Wide) and the long data section:
  percentage column dropdown (required) and sewage type column dropdown ("None" + all source
  columns). Wire show/hide of the long data section to the format radio.
- **Depends on:** Task 1
- **Acceptance:** Widget renders; switching to Long shows the column dropdowns; switching to Wide
  hides them; dropdowns populate from the source layer columns.
- **Evidence:** Manual smoke test in headless QGIS or `pytest` widget test.

#### Task 4: SurfaceMapSettingsWidget — wide data section + linking [P]
- **Estimate:** ~70 lines
- **Parallel:** Can run with Task 3
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Add the wide data section (inline table with `SewerTypeMappingDelegate`,
  Add/Remove buttons — reuse logic from old `SurfaceMapPercentageSettingsWidget`). Add the
  linking section: match mode radios, field map widget, "Use sewage type for attribute matching"
  checkbox (enabled only when match mode ≠ None AND sewage type source present), spatial matching
  checkbox + search distance spinbox on one line, "Only match selected pipes" checkbox.
  Wire show/hide of the wide data section to the format radio.
- **Depends on:** Task 1
- **Acceptance:** Table add/remove works; linking controls appear and disable correctly per rules.
- **Evidence:** Manual smoke test; `SewerTypeMappingDelegate` reused without duplication.

#### Task 5: Wire SurfaceMapSettingsWidget into wizard
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`,
  `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py`
- **Description:** Implement `update_model()` (UI → `SurfaceMapSettings`) and `is_valid()`
  (long: percentage_column set; wide: ≥1 mapping; both: field map complete if attribute match
  enabled). Replace the Task 2 placeholder with the real `SurfaceMapSettingsWidget`. Confirm
  the wizard settings round-trip correctly.
- **Depends on:** Tasks 2, 3, 4
- **Acceptance:** Wizard saves and restores `SurfaceMapSettings`; validation blocks progress when
  required fields are missing.
- **Evidence:** `pytest tests/ -q --tb=short` passes.

### Processor

#### Task 6: Add long data path to SurfaceProcessor
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Branch `_create_surface_map_features` on `settings.data_format`. For the long
  path: read percentage from `percentage_column`; skip row if ≤ 0; read sewage type from
  `sewage_type_column` when set (None otherwise); run attribute match if enabled; run spatial
  search (always pass `sewage_type` as filter — no filter when None); create exactly one
  `surface_map` row. Update the processor to read from `settings.surface_map` instead of the
  old two settings keys.
- **Depends on:** Task 1
- **Acceptance:** Long-format fixture produces exactly one `surface_map` row per source row;
  sewage type filter is applied to spatial search when column is set.
- **Evidence:** Unit test with long-format fixture passes (`pytest tests/ -k surface -q --tb=short`).

#### Task 7: Update wide data path — sewage type verification
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** In the wide data iteration, apply the same sewage type matching rules as the
  long path: spatial search always passes `mapping.sewage_type` as filter. When
  `use_sewage_type_for_attribute_match` is True, verify the attribute-matched pipe's sewage type
  equals `mapping.sewage_type`; reject (set to None) on mismatch.
- **Depends on:** Task 6
- **Acceptance:** Wide-format fixture with attribute match + sewage type verification rejects
  mismatched pipes and falls through to spatial search.
- **Evidence:** Unit test covering mismatch rejection passes (`pytest tests/ -k surface -q --tb=short`).

## Notes

- No backward compatibility for saved settings files — `surface_map_percentage` and
  `surface_linking` keys are dropped.
- `use_sewage_type_for_attribute_match` is global (applies to all mapping rows in wide mode).
- Sewage type filtering for spatial search is unconditional — independent of the attribute
  match toggle.
- `SewerTypeMappingDelegate` logic should be reused from the old widget, not duplicated.

## Progress

- [x] Task 1: Merge settings models
- [x] Task 2: Update wizard wiring (stub)
- [x] Task 3: SurfaceMapSettingsWidget — format toggle + long data section
- [x] Task 4: SurfaceMapSettingsWidget — wide data section + linking
- [x] Task 5: Wire SurfaceMapSettingsWidget into wizard
- [x] Task 6: Add long data path to SurfaceProcessor
- [x] Task 7: Update wide data path — sewage type verification
