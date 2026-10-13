---
feature: pump-importer-hydamo-line-mode
status: complete
created: 2026-07-14
chunk_size: medium
total_tasks: 4
estimated_lines: 180
---

# Pump Import: HyDaMo Line Mode — Tasks

## Overview

Extend `PumpsImporter` to handle HyDaMo line-geometry pump sources. A line
source creates a Pump at the line start, a ConnectionNode at the line end, and
a PumpMap connecting them. An optional direction field (default `1`, reverse on
`-1`) is configured via `FieldMapConfig`. The pump_map is integrated into the
pipe network using the existing `LineStructurePlacement` strategy.

## Task List

### Foundation

#### Task 1: `PumpDirectionSettings`
- **Estimate:** ~25 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`
- **Description:** Add `PumpDirectionSettings` BaseModel with a single
  `direction: FieldMapConfig[int]` field (allowed methods: `ATTRIBUTE`,
  `DEFAULT`; default value `1`). Add `pump_direction: PumpDirectionSettings`
  to `ImportSettings`.
- **Depends on:** None
- **Acceptance:** `ImportSettings()` serialises with `pump_direction.direction.default_value == 1`.
- **Evidence:** Existing `test_settings_model.py` tests still pass.

### Core Implementation

#### Task 2: `PumpLineProcessor`
- **Estimate:** ~70 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** New class `PumpLineProcessor(StructureProcessor)`. Constructor
  takes `target_layer` (Pump), `pump_map_layer`, `node_layer`, `import_settings`.
  Initialises `pump_map_manager` and `direction_config`.
  `process_feature(src_feat)`:
  1. Get line geometry; resolve direction — reverse polyline if `-1`.
  2. Simplify to `[polyline[0], polyline[-1]]`.
  3. Snap/create ConnectionNode at `polyline[0]`; create Pump point; assign
     `connection_node_id`.
  4. Snap/create ConnectionNode at `polyline[-1]`.
  5. Create PumpMap line; assign `pump_id` and `connection_node_id_end`.
  6. Apply field configs to Pump (`fields_configurations`) and PumpMap
     (`pump_map_fields_configurations` from `import_settings.pump_map_fields`).
  7. Apply `cn_fields_configurations` to new nodes.
  8. Add new nodes to `node_layer`; rebuild locator.
  9. Return `{pump_layer_name: [pump_feat], pump_map_layer_name: [pump_map_feat]}`.
- **Depends on:** Task 1
- **Acceptance:** Given a two-point line feature, `process_feature` returns one
  Pump at the start point and one PumpMap with correct `pump_id` and
  `connection_node_id_end`; direction `-1` swaps start and end.
- **Evidence:** `test_processors.py` tests still pass.

#### Task 3: `PumpsImporter` auto-detection + integration properties + test
- **Estimate:** ~35 lines implementation + ~30 lines test
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/importers.py`
  - `tests/vector_data_importer/test_importers.py`
- **Description:**
  - Add `pump_map_layer=None` parameter to `PumpsImporter.__init__`.
  - Detect source geometry type from `external_source`; select
    `PointProcessor` (point) or `PumpLineProcessor` (line) accordingly.
  - Add `integration_model_cls`, `integration_layer`, `integration_manager`
    properties to `PumpsImporter` (return PumpMap equivalents when processor is
    `PumpLineProcessor`, otherwise delegate to target equivalents).
  - Add the same three properties as no-op defaults on `IntegrationImporter`
    base class (return `target_model_cls`, `target_layer`,
    `processor.target_manager`).
  - **Test:** Two cases — point source constructs `PointProcessor`; line source
    constructs `PumpLineProcessor` and integration properties return PumpMap
    layer/manager.
- **Depends on:** Task 2
- **Acceptance:** Point-mode behaviour is unchanged; line-mode picks
  `PumpLineProcessor` and exposes correct integration properties.
- **Evidence:** New tests pass; existing `test_importers.py` tests still pass.

#### Task 4: `PipeIntegrator.from_importer` integration-property support
- **Estimate:** ~20 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/integrators.py`
- **Description:** Update `PipeIntegrator.from_importer` to read
  `integration_model_cls`, `integration_layer`, and `integration_manager` from
  the importer (using `getattr` with fallback to current attributes) instead of
  always using `target_model_cls`, `target_layer`, and
  `processor.target_manager`. Pass `model_cls` (not `importer.target_model_cls`)
  to the constructor and for strategy selection.
- **Depends on:** Task 3
- **Acceptance:** Existing integrator tests pass unmodified; a `PumpsImporter`
  in line mode with integration enabled produces a `LineStructurePlacement`
  strategy targeting `dm.PumpMap`.
- **Evidence:** `test_integrators.py` tests still pass.

## Notes

- `pump_map_fields` open question (separate key in `ImportSettings` vs merged
  into `fields`) is deferred — Task 2 assumes a separate
  `pump_map_fields: dict[str, FieldMapConfig] = {}` key, consistent with the
  existing `connection_node_fields` pattern.
- Wizard UI wiring (`pump_map_layer` plumbing, PumpMap field mapping exposure)
  is out of scope for this feature.
- `ChannelIntegrator` support for pump_map is out of scope.

## Progress
- [x] Task 1: `PumpDirectionSettings`
- [x] Task 2: `PumpLineProcessor`
- [x] Task 3: `PumpsImporter` auto-detection + integration properties + test
- [x] Task 4: `PipeIntegrator.from_importer` integration-property support
