---
feature: attribute-surface-matching
status: complete
created: 2026-06-30
chunk_size: medium
total_tasks: 7
estimated_lines: 290
---

# Attribute-Based Surface Matching Tasks

## Overview

Extend the surface importer with optional attribute-based matching. A value derived
from the source surface feature is matched against a column in either the `pipe` or
`connection_node` table. Exactly one match creates a single `surface_map` entry at
100%. Zero or multiple matches fall back to the existing spatial match.

Three files change; no new files are created.

## Task List

### Foundation

#### Task 1: Extend `SurfaceLinkingSettings`
- **Estimate:** ~20 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Add three optional fields to `SurfaceLinkingSettings`:
  `attribute_match_table` (`Optional[Literal["pipe", "connection_node"]]`),
  `attribute_match_col` (`Optional[str]`), and `attribute_match_input_config`
  (`Optional[FieldMapConfig]`). All default to `None` (attribute matching disabled).
  Pydantic handles serialization via `model_dump()`.
- **Depends on:** None
- **Acceptance:** `SurfaceLinkingSettings()` instantiates with defaults; all three
  fields round-trip through `model_dump()` / `model_validate()`.
- **Evidence:** Existing `test_settings_model.py` suite still passes; manual
  instantiation in a Python shell confirms defaults.

### Core Implementation

#### Task 2: Redesign `SurfaceConnectionSettingsWidget` [P]
- **Estimate:** ~80 lines
- **Parallel:** Can run with Tasks 3a
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Change inheritance from `SettingsWidget` to `FieldMapSettingsWidget`.
  Rebuild `__init__` to:
  1. Construct `extra_layout` (`QGridLayout`) with existing rows (surface map layer,
     pipe layer + selected-only checkbox, connection node layer, search distance) plus
     new rows: section label "Attribute matching", "Match table" `QComboBox`
     (`["", "Pipe", "Connection node"]`), "Match column" `QComboBox`.
  2. Build `row_dict` with one `FieldMapRow` keyed `"attribute_match_input_config"`
     (label "Source value", allowed methods: ATTRIBUTE, EXPRESSION, DEFAULT).
  3. Call `self.setup_ui(row_dict, extra_layout=extra_layout)`.
  4. Connect all signals to `_update_model()`.
  5. Match table combo change → repopulate match column combo from the selected
     layer's fields + cascading enable/disable (match column disabled when match
     table blank; `FieldMapWidget` disabled when match column blank).
  Update `update_layer()` to call `super().update_layer(layer)` and also repopulate
  match column combo. Update `_update_model()`, `get_settings()`, `deserialize()`.
- **Depends on:** Task 1
- **Acceptance:** Widget instantiates; selecting "Pipe" populates match column from
  pipe layer fields; leaving match table blank disables match column and source value
  row; `get_settings()` returns a `SurfaceLinkingSettings` with correct values;
  `deserialize()` restores state.
- **Evidence:** Existing wizard tests pass; manual widget interaction in QGIS.

#### Task 3a: Write failing test for `_choose_closer_node` [P]
- **Estimate:** ~30 lines
- **Parallel:** Can run with Task 2
- **Files:** `tests/vector_data_importer/test_processors_surface.py`
- **Description:** Using the existing `make_node_feat` helper, write two parametrized
  test cases for the not-yet-existing `SurfaceProcessor._choose_closer_node()`
  static method:
  - Surface geometry closer to the start node → returns start node feature
  - Surface geometry closer to the end node → returns end node feature
  Run the tests and confirm they fail with `AttributeError` (method does not exist).
- **Depends on:** None
- **Acceptance:** Tests are written and fail for the right reason (missing method).
- **Evidence:** `pytest tests/vector_data_importer/test_processors_surface.py -q --tb=short`
  shows two failures with `AttributeError`.

#### Task 3b: Extract `_choose_closer_node` + wire expression context
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Write minimal implementation to make Task 3a tests pass:
  - Extract the start/end node distance comparison from `_create_surface_map_features`
    (lines ~1000–1015) into a new `@staticmethod _choose_closer_node(surface_geom,
    pipe_feat, node_layer) -> QgsFeature`.
  - Update the existing spatial-match loop to call the new helper.
  - Build a `QgsExpressionContext` from `src_feat` in `process_feature()` and pass it
    through to `_create_surface_map_features()` to support EXPRESSION method later.
- **Depends on:** Task 3a
- **Acceptance:** Task 3a tests pass; all existing `test_processors_surface.py` tests
  still pass (no behavioural regression).
- **Evidence:** `pytest tests/vector_data_importer/test_processors_surface.py -q --tb=short`
  all green.

#### Task 4: Add attribute-match path to `SurfaceProcessor`
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Add an attribute-match branch at the top of
  `_create_surface_map_features()`, before the existing spatial-match loop:
  - If `linking.attribute_match_table` is set, derive `input_val` via
    `get_field_config_value(linking.attribute_match_input_config, src_feat,
    expression_context)`.
  - For `"connection_node"`: query `node_layer` for features where
    `attribute_match_col == input_val`. Exactly 1 match → create one `surface_map`
    entry (`connection_node_id`, `percentage=100`). 0 or 2+ → fall through.
  - For `"pipe"`: query `pipe_features` for features where
    `attribute_match_col == input_val`. Exactly 1 match → call `_choose_closer_node`
    to pick the endpoint node, create one `surface_map` entry (`percentage=100`).
    0 or 2+ → fall through.
  - Existing sewerage-type spatial-match loop is unchanged and runs as fallback.
- **Depends on:** Tasks 2, 3b
- **Acceptance:** Attribute-match path creates one `surface_map` entry on success;
  falls back to spatial on 0 or 2+ matches.
- **Evidence:** Task 5 tests pass.

### Tests & Docs

#### Task 5: Tests for attribute-match path in `SurfaceProcessor`
- **Estimate:** ~70 lines
- **Files:** `tests/vector_data_importer/test_processors_surface.py`
- **Description:** Using existing helpers (`make_node_feat`, `make_pipe_layer_with_feats`,
  `make_import_settings`, etc.), add tests for:
  - `test_attr_match_connection_node_success`: single matching node → one surface_map
    entry with `connection_node_id` and `percentage=100`.
  - `test_attr_match_pipe_success`: single matching pipe → one surface_map entry
    linked to the closer endpoint node, `percentage=100`.
  - `test_attr_match_zero_results_falls_back`: 0 matching rows → spatial match runs
    (existing sewerage-type loop produces entries).
  - `test_attr_match_multiple_results_falls_back`: 2+ matching rows → spatial match
    runs.
- **Depends on:** Task 4
- **Acceptance:** All four new tests pass; full suite still green.
- **Evidence:** `pytest tests/vector_data_importer/test_processors_surface.py -q --tb=short`
  all green.

#### Task 6: Update design docs — *@utility*
- **Estimate:** docs only
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/DESIGN.md`
  - `threedi_schematisation_editor/vector_data_importer/wizard/DESIGN.md`
  - `.minispec/specs/attribute-surface-matching/design.md`
- **Description:** Update `DESIGN.md` in `vector_data_importer/` and `wizard/` to
  document the new attribute matching capability (settings model fields, widget
  changes, processor logic). Update `.minispec/specs/attribute-surface-matching/design.md`
  front-matter status from `designed` to `implemented`.
- **Depends on:** Task 5
- **Acceptance:** Design docs reflect the implementation; spec status updated.
- **Evidence:** Files saved and readable.

## Notes

- `_choose_closer_node` extraction is justified: the logic appears in both the
  spatial-match path and the new attribute-match pipe path (used 2 times, matching
  the existing `_find_nearest_pipe` static helper pattern).
- Percentage is hardcoded to 100 for attribute-match entries; making it configurable
  is deferred to a future task.
- No changes to `importers.py`, `wizard.py`, or data models.

## Progress

- [x] Task 1: Extend `SurfaceLinkingSettings`
- [x] Task 2: Redesign `SurfaceConnectionSettingsWidget`
- [x] Task 3a: Write failing test for `_choose_closer_node`
- [x] Task 3b: Extract `_choose_closer_node` + wire expression context
- [x] Task 4: Add attribute-match path to `SurfaceProcessor`
- [x] Task 5: Tests for attribute-match path
 - [x] Task 6: Update design docs
