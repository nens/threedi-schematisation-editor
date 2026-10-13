---
feature: generic-surface-import
status: complete
created: 2026-06-22
chunk_size: medium
total_tasks: 8
estimated_lines: ~580
---

# Tasks: Generic Surface Import

## Overview

Implements a VDI wizard that imports polygon surfaces and creates surface_map
linkages in a single operation. Core logic lives in `SurfaceProcessor` and
`SurfaceImporter`; a `SurfaceSettingsWidget` and `ImportSurfaceWizard` expose it
to the user.

---

## Phase 1: Foundation

### T001 — Settings models
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Add `SurfaceFilterSettings`, `SewerTypeMapping`,
  `SurfaceLinkingSettings`, `SurfaceSettings` Pydantic models. Extend
  `ImportSettings` with a `surface: SurfaceSettings` field.
- **Depends on:** None
- **Acceptance:** New models serialize/deserialize the example BGT preset JSON
  from the design doc without validation errors.
- **Evidence:** `pytest tests/vector_data_importer/test_surface_settings.py` passes

---

## Phase 2: Core Logic (TDD)

Tasks T002 and T003 are worked together using TDD: write a failing test, implement
enough to make it pass, repeat. Both tasks are committed together as a unit.

### T002a — Tests + SurfaceProcessor: filter, geometry, field mapping
- **Estimate:** ~80 lines (tests + implementation)
- **Files:**
  - `tests/vector_data_importer/test_surface_processor.py` (new)
  - `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Write tests first (failing), then implement:
  - Surface filter: evaluate ATTRIBUTE or EXPRESSION per feature; skip if
    result >= threshold; NULL evaluates as not-excluded
  - Geometry conversion: CurvePolygon → Polygon + CRS transform
  - Area computation: `QgsGeometry.area()`
  - Field mapping: apply FieldMapConfig for `id` (auto), `code`,
    `display_name`, `surface_parameters_id`, `tags`; `area` is not in field
    map (always computed)
- **Depends on:** T001
- **Acceptance:** Filter excludes correct features; geometry is Polygon type;
  area is set; field mapping applies correctly.
- **Evidence:** `pytest tests/vector_data_importer/test_surface_processor.py -k "filter or geometry or fields"` passes

### T002b — Tests + SurfaceProcessor: spatial linking + surface_map creation
- **Estimate:** ~90 lines (tests + implementation)
- **Files:**
  - `tests/vector_data_importer/test_surface_processor.py` (extend)
  - `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Write tests first (failing), then implement the surface_map
  creation logic in `SurfaceProcessor`:
  - For each sewer type with a configured percentage column:
    - Skip feature if `percentage_column value <= 0`
    - Find nearest pipe of matching `sewerage_type` within `search_distance`
      using spatial index passed from importer
    - Apply stormwater/sanitary preference offsets
    - Pick nearest connection node (start vs end node of pipe)
    - Create surface_map feature: `surface_id`, `connection_node_id`,
      `percentage = actual column value`, linestring geom (centroid → node)
  - Surfaces with no pipe within search_distance: skipped, warning emitted
  - Uses mock pipe + node layers in tests
- **Depends on:** T002a
- **Acceptance:** Correct surface_map features created; percentage = actual
  column value (not 100.0); no entry when percentage = 0; no entry when no pipe
  in range.
- **Evidence:** `pytest tests/vector_data_importer/test_surface_processor.py -k "surface_map or linking"` passes

### T003 — Tests + SurfaceImporter
- **Estimate:** ~60 lines (tests + implementation)
- **Files:**
  - `tests/vector_data_importer/test_surface_processor.py` (extend, or new
    `test_surface_importer.py`)
  - `threedi_schematisation_editor/vector_data_importer/importers.py`
- **Description:** Write tests first (failing), then implement `SurfaceImporter`:
  - Subclass of `SpatialImporter`
  - Builds pipe spatial index once from pipe layer (shared across all features)
  - Puts Surface and Surface_map layers in edit mode
  - Calls `SurfaceProcessor.process()`
  - Adds returned surface features to Surface layer
  - Adds returned surface_map features to Surface_map layer
- **Depends on:** T002b
- **Acceptance:** Both layers enter edit mode; surface features added to Surface
  layer; surface_map features added to Surface_map layer; spatial index passed
  to processor.
- **Evidence:** `pytest tests/vector_data_importer/test_surface_processor.py` (all) passes

---

## Phase 3: UI

### T004a — SurfaceSettingsWidget: filter row + sewer type mapping table
- **Estimate:** ~70 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Implement the first two sections of `SurfaceSettingsWidget`:
  - Surface filter row: method selector (ATTRIBUTE / EXPRESSION), source
    attribute or expression input, threshold float field (default 100.0)
  - Sewer type mapping table: 11 rows (one per `SewerageType` enum value),
    each with a read-only type label and a ComboBox populated from source layer
    fields; blank = skip
  - Widget reads from / writes to `SurfaceSettings` model
- **Depends on:** T001
- **Acceptance:** Widget renders 11 sewer type rows; filter fields update
  `SurfaceFilterSettings`; sewer comboboxes update `SewerTypeMapping` list.
- **Evidence:** Manual inspection in QGIS; widget settings round-trip correctly

### T004b — SurfaceSettingsWidget: layer selectors + spatial linking params
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Implement the third section of `SurfaceSettingsWidget`:
  - Surface map layer selector (line geometry, default "Surface map")
  - Pipe layer selector (line geometry, default "Pipe")
  - Selected pipes only checkbox (default False)
  - Connection node layer selector (point geometry, default "Connection node")
  - Search distance float field (default 10.0 m)
  - Stormwater sewer preference float field (default 0.0 m)
  - Sanitary sewer preference float field (default 0.0 m)
  - Widget reads from / writes to `SurfaceLinkingSettings` model
- **Depends on:** T004a
- **Acceptance:** All layer selectors populate from QGIS project layers with
  correct geometry filter; numeric fields update `SurfaceLinkingSettings`.
- **Evidence:** Manual inspection in QGIS; widget settings round-trip correctly

### T005 — ImportSurfaceWizard + registration
- **Estimate:** ~60 lines
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py`
  - `threedi_schematisation_editor/vector_data_importer/wizard/__init__.py`
  - `threedi_schematisation_editor/__init__.py`
- **Description:** Add `ImportSurfaceWizard` subclass to `wizard.py`:
  - Page flow: Start → Surface Settings → Field Map → Run
  - `settings_widgets_classes = [SurfaceSettingsWidget]`
  - `layer_filter = QgsMapLayerProxyModel.PolygonLayer`
  - `target_model_cls = dm.Surface`
  - Field map covers: `id` (auto), `code`, `display_name`,
    `surface_parameters_id`, `tags` — `area` excluded (auto-computed)
  - Export from `wizard/__init__.py`
  - Register in plugin menu in `__init__.py` (same pattern as other importers)
- **Depends on:** T003, T004b
- **Acceptance:** Wizard appears in QGIS plugin menu; all four pages render;
  Field Map page shows only the correct Surface fields; Run page executes import
  and both layers end up in editing mode.
- **Evidence:** End-to-end manual run with a test polygon layer completes without error

---

## Phase 4: Integration Test

### T007 — Integration test with provided test data
- **Estimate:** ~60 lines
- **Files:** `tests/vector_data_importer/test_surface_import_integration.py` (new)
- **Description:** End-to-end integration test using test data to be provided.
  Configure filter + sewer mappings, run importer, assert:
  - Correct surface count (filtered features excluded)
  - Surface features have correct geometry type (Polygon), area computed,
    `surface_parameters_id` set correctly
  - Surface_map features link to correct connection nodes with correct
    percentages
  - No surface_map entries for features where percentage = 0
  - No crash when a surface has no pipe within search_distance
- **Depends on:** T003
- **Note:** Test data will be provided separately by the engineer. Placeholder
  test data path: `tests/test_data/surface_import/`.
- **Evidence:** `pytest tests/vector_data_importer/test_surface_import_integration.py` passes

---

## Dependencies & Execution Order

```
T001
 ├── T002a → T002b → T003 → T005
 │                    └── T007
 └── T004a → T004b → T005
```

**Sequential:** T001 → T002a → T002b → T003 → T007  
**Parallel after T001:** T004a can start alongside T002a (different files, no shared state)  
**T005 blocks on:** both T003 and T004b

---

## Progress

- [x] T001 — Settings models
- [x] T002a — Tests + SurfaceProcessor: filter, geometry, field mapping
- [x] T002b — Tests + SurfaceProcessor: spatial linking + surface_map creation
- [x] T003 — Tests + SurfaceImporter
- [x] T004a — SurfaceSettingsWidget: filter row + sewer type mapping table
- [x] T004b — SurfaceSettingsWidget: layer selectors + spatial linking params
- [x] T005 — ImportSurfaceWizard + registration
- [x] T007 — Integration test with provided test data

---

## Notes

- T002/T003 use TDD: write failing test → implement → make it pass. Both test
  and implementation are committed together per task.
- T007 test data to be provided by the engineer; test file can be stubbed out
  earlier and completed once data arrives.
- No T006 — unit tests are embedded in T002a, T002b, T003 (TDD approach).
- Processing algorithm wrapper is explicitly deferred (see design.md).
- NWRW prerequisite check is explicitly deferred (see design.md).
