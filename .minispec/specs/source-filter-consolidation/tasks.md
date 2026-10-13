# Source Filter Consolidation — Tasks

## Overview

Implement the source filter consolidation design: move filtering to the Start page, add expression support for all importers, remove the surface-specific filter.

## Task List

### Foundation

#### Task 1: Add `SourceSettings` model and wire into `ImportSettings`
- **Estimate:** ~30 lines
- **Files:** `settings_models.py`, `wizard/models.py`
- **Description:** Create `SourceSettings` pydantic model with `selected_layer_name`, `use_selected_features`, `filter_expression`. Add to `ImportSettings`. Delete `wizard/models.py` (GenericSettingsModel).
- **Depends on:** None
- **Evidence:** `ImportSettings(source=SourceSettings(...))` round-trips through `model_dump()`/construction; existing tests still pass

#### Task 2: Update `LayerSettingsWidget` to use `SourceSettings` + add expression widget
- **Estimate:** ~60 lines
- **Files:** `wizard/settings_widgets.py`
- **Description:** Replace `GenericSettingsModel` usage with `SourceSettings`. Add `QgsFieldExpressionWidget` below the checkbox. Connect layer changes to update expression widget fields. Add `get_settings()` and `deserialize()`.
- **Depends on:** Task 1
- **Evidence:** Widget renders; changing layer updates expression field list; `get_settings()` returns populated `SourceSettings`

### Core Implementation

#### Task 3: Update `StartPage` to participate in serialize/deserialize
- **Estimate:** ~40 lines
- **Files:** `wizard/pages.py`
- **Description:** Add `get_settings()` returning `{"source": ...}` and `deserialize(data)` that restores layer name, checkbox, and expression from `data["source"]`. Remove `GenericSettingsModel` import.
- **Depends on:** Task 2
- **Parallel:** Can run with Task 4 once Task 2 is done
- **Evidence:** Load a JSON config with `"source": {...}` → Start page pre-fills layer, checkbox, expression

#### Task 4: Update `VDIWizard.run_import()` to evaluate expression
- **Estimate:** ~40 lines
- **Files:** `wizard/wizard.py`
- **Description:** Implement 4-case selected_feat_ids logic. Extract expression evaluation helper (iterate features, evaluate QgsExpression, return matching IDs).
- **Depends on:** Task 2, 3
- **Evidence:** Import with expression set → only matching features are processed; import without expression → all features (or selected) processed as before

#### Task 5: Remove surface-specific filter
- **Estimate:** ~-80 lines (net removal)
- **Files:** `settings_models.py`, `wizard/settings_widgets.py`, `importers.py`
- **Description:** Remove `SurfaceFilterSettings`, `SurfaceSettings.filter` field, filter section from `SurfaceSettingsWidget.setup_ui()`, `SurfaceImporter.filter_features()`, `SurfaceImporter.get_input_feature_ids()` override.
- **Depends on:** Task 4 (new path works before removing old)
- **Evidence:** Surface import still works using the Start page expression instead; old filter UI gone

#### Task 6: Update processing algorithms to apply `filter_expression`
- **Estimate:** ~30 lines
- **Files:** `processing/algorithms_vector_data_importer.py`
- **Description:** In `processAlgorithm()`, read `import_config.source.filter_expression`, evaluate on source layer if set, pass resulting IDs to `import_features(selected_ids=...)`.
- **Depends on:** Task 1
- **Parallel:** Can run alongside Tasks 2–5
- **Evidence:** Processing algorithm with config containing `filter_expression` → only matching features imported

### Testing

#### Task 7: Update tests
- **Estimate:** ~80 lines
- **Files:** `tests/vector_data_importer/test_wizard.py`, `tests/vector_data_importer/test_importers.py`
- **Description:** Update deserialize tests for new `SourceSettings` flow. Remove surface filter tests. Add test for expression evaluation logic in `run_import`. Update `test_importers.py` (remove `filter_features` tests or convert to expression tests).
- **Depends on:** All other tasks
- **Evidence:** `docker compose run qgis-desktop make test` passes

## Notes
- Test the wizard after each task (1→2→3→4) before removing old code in task 5
- Task 5 is pure removal — if anything breaks, the problem is in tasks 1–4
- Update `import_surface_bgt.json` and `import_surface.json` test configs to new format after task 5

## Progress
- [x] Task 1: Add `SourceSettings` model
- [x] Task 2: Update `LayerSettingsWidget`
- [x] Task 3: Update `StartPage` serialization
- [x] Task 4: Expression evaluation in `run_import()`
- [x] Task 5: Remove surface-specific filter
- [x] Task 6: Update processing algorithms
- [x] Task 7: Update tests
