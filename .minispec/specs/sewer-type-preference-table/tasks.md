# Sewer Type Preference Table — Tasks

## Overview

Replace the two hardcoded preference spinboxes (`stormwater_sewer_preference`, `sanitary_sewer_preference`) with a configurable table where any sewerage type can have a distance preference offset.

## Task List

### Foundation

#### Task 1: Update `SurfaceLinkingSettings` model
- **Estimate:** ~25 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Add `SewerTypePreference(sewerage_type, preference)` model. Remove `stormwater_sewer_preference` and `sanitary_sewer_preference` from `SurfaceLinkingSettings`. Add `sewer_type_preferences: list[SewerTypePreference] = []`.
- **Depends on:** None
- **Evidence:** Existing tests still pass

#### Task 2: Update `SurfaceProcessor`
- **Estimate:** ~20 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`, `tests/vector_data_importer/test_processors_surface.py`
- **Description:** Build `preference_by_type` dict at init from `sewer_type_preferences`. Replace if/elif in `_find_nearest_pipe` with `preference_by_type.get(sewerage_type, 0.0)`. Update preference offset tests to use new model.
- **Depends on:** Task 1
- **Evidence:** Preference offset tests pass with new model

### Core Implementation

#### Task 3: Add `SewerTypePreferenceModel`
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** New `QAbstractTableModel` with sewerage type combobox column (reusing existing `SewerTypeMappingDelegate`) and editable float preference column. Add/remove rows, `get_preferences()` / `set_preferences()`.
- **Depends on:** Task 1
- **Parallel:** Can run with Task 2
- **Evidence:** Widget renders, rows add/remove correctly

#### Task 4: Update `SurfaceConnectionSettingsWidget`
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Remove two `QDoubleSpinBox` rows (stormwater/sanitary). Add preference table group with add/delete buttons below the existing grid. Wire `_update_model()` and `deserialize()` to the preference table.
- **Depends on:** Task 3
- **Evidence:** Settings page renders correctly, preferences serialize/deserialize

### Cleanup

#### Task 5: Update JSON configs and instructions
- **Estimate:** ~30 lines
- **Files:** `~/test_data/import_bgt.json`, `~/test_data/vdi/bgt/import_surface_bgt.json`, `~/test_data/vdi/bgt/instructions.md`
- **Description:** Replace `stormwater_sewer_preference`/`sanitary_sewer_preference` with `sewer_type_preferences: []` in both JSON configs. Update `instructions.md` to describe the preference table instead of the two spinboxes.
- **Depends on:** Task 4
- **Evidence:** Configs load without validation errors; instructions reflect current UI

## Notes
- Old JSON configs with the two float fields will load silently (pydantic ignores extra fields) but values are dropped — this is acceptable since the feature is unreleased
- `SewerTypeMappingDelegate` is reused for the sewerage type column, no new delegate needed

## Progress
- [x] Task 1: Update `SurfaceLinkingSettings` model
- [x] Task 2: Update `SurfaceProcessor`
- [x] Task 3: Add `SewerTypePreferenceModel`
- [x] Task 4: Update `SurfaceConnectionSettingsWidget`
- [x] Task 5: Update JSON configs and instructions
