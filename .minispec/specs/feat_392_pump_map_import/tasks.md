---
feature: pump-map-import
status: complete
created: 2026-07-16
chunk_size: medium
total_tasks: 7
estimated_lines: 400
---

# Pump Map Import Tasks

## Overview

Extends pump import to support PumpMap creation from point sources via attribute mapping
and point-to-line projection. Introduces `PumpProcessor` (pump + optional pump_map side
effect), `PumpMapNodeHandler` (node assignment during integration), and `StructureNodeHandler`
(extracted from existing `update_feature_endpoints`). Removes `PumpLineProcessor` and
`PumpSettings`. Overrides `PumpsImporter.import_features` with a multi-phase flow.

## Task List

### Foundation

#### Task 1: Extract `StructureNodeHandler` + add `node_handler` to `LinearIntegrator`
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/integrators.py`
- **Description:** Extract the current `update_feature_endpoints` logic into a
  `StructureNodeHandler` class with an `update_nodes(feat, node_attributes,
  respect_mapped_node_ids)` interface. Add `node_handler` parameter to
  `LinearIntegrator.__init__` (default: `StructureNodeHandler` instance). Replace the
  direct `self.update_feature_endpoints` call in `integrate_structure_features` with
  `self.node_handler.update_nodes(...)`. Update `PipeIntegrator.from_importer` and
  `ChannelIntegrator.from_importer` to pass a `StructureNodeHandler` instance.
  Remove `update_feature_endpoints` as a method on `LinearIntegrator`.
- **Depends on:** None
- **Acceptance:** All existing integrator behaviour is preserved; no logic change,
  only extraction and delegation.
- **Evidence:** `pytest tests/vector_data_importer/test_integrators.py -q --tb=short` passes.

#### Task 2: `PumpMapNodeHandler`
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/integrators.py`
- **Description:** Implement `PumpMapNodeHandler` with the same `update_nodes` interface
  as `StructureNodeHandler`. Receives a pump features dict (keyed by a location-to-pump
  mapping built from the in-memory source layer), pump layer fields, and pump
  `FeatureManager`. For each placed pump_map feature:
  - Start point: find/create node in `node_by_location`, create pump feature
    (geometry = node location, `connection_node_id` = node id), set `pump_map.pump_id`.
  - End point: find/create node in `node_by_location`, set `pump_map.connection_node_id_end`.
  - Adjust pump_map geometry to the line between start node and end node locations.
- **Depends on:** Task 1 (shared interface)
- **Acceptance:** Class instantiates and `update_nodes` correctly creates pump + sets
  pump_map fields for both integrated and shifted (post-fix_structure_placement) cases.
- **Evidence:** Unit tests in Task 6 pass.

### Core Implementation

#### Task 3: `PumpProcessor`
- **Estimate:** ~70 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Implement `PumpProcessor(StructureProcessor)`. Takes point source
  features and creates pumps with optional pump_map as a side effect (analogous to
  `SurfaceProcessor` creating `surface_map` entries). For each source feature:
  - Create pump feature (geometry + attributes + connection node via `get_node`).
  - Try attribute mapping (`get_field_config_value`) → look up connection node → end point.
  - Fallback: point_to_line (`PointToLineSettings`) → `start_point.project(length, azimuth)`
    → snap end point to existing node (`get_node`). Note: pump is at START of line, not center.
  - If end point resolved: create pump_map feature (line geometry, `pump_id`,
    `connection_node_id_end`), snap end geometry to node.
  - If no end point: pump only, no pump_map.
  - Returns `{pump_layer_name: [pump_feat]}` or
    `{pump_layer_name: [pump_feat], pump_map_layer_name: [pump_map_feat]}`.
  - Manages `pump_map_manager` (`FeatureManager`) for pump_map ID tracking.
- **Depends on:** None
- **Acceptance:** Processor creates pump-only or pump+pump_map correctly per settings;
  attribute mapping takes priority over point_to_line.
- **Evidence:** Unit tests in Task 6 pass.

#### Task 4: Remove `PumpLineProcessor` and `PumpSettings`
- **Estimate:** ~30 lines removed
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`,
  `threedi_schematisation_editor/vector_data_importer/settings_models.py`,
  `threedi_schematisation_editor/vector_data_importer/importers.py`
- **Description:** Delete `PumpLineProcessor` from `processors.py`. Delete `PumpSettings`
  (the `direction` field) from `settings_models.py`. Remove all references in
  `importers.py` (`isinstance(self.processor, PumpLineProcessor)` guards,
  `pump_map_manager`, `integration_model_cls`, `integration_layer`,
  `integration_manager` overrides that were specific to line-source mode).
  Remove any line-source-specific tests.
- **Depends on:** None (parallel with Tasks 2, 3)
- **Acceptance:** No references to `PumpLineProcessor` or `PumpSettings.direction` remain.
- **Evidence:** `pytest tests/vector_data_importer/ -q --tb=short` passes (minus
  deleted line-source tests).

### Wire-up

#### Task 5: `PumpsImporter.import_features` multi-phase override
- **Estimate:** ~80 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/importers.py`
- **Description:** Override `import_features` on `PumpsImporter` with the multi-phase
  flow:

  **Phase A — pump_maps:**
  1. Build in-memory PumpMap source layer: for each source feature, try attribute
     mapping then point_to_line to resolve an end point; if found, add a line feature
     (pump point → end point) copying all source fields. Track which source feature IDs
     have no end point as `{without_map}`.
  2. Integrate pump_maps (if integration enabled): create integrator **directly**
     (not via `from_importer`) passing `LineStructurePlacement` + `PumpMapNodeHandler`
     as `node_handler`; run standard integrate flow on in-memory source layer.
  3. Process remaining pump_maps (non-integrated or integration disabled): use
     `PumpProcessor` on remaining in-memory source features.

  **Phase B — pumps without maps:**
  4. Integrate `{without_map}` pumps (if integration enabled): create integrator with
     `PointStructurePlacement` + `StructureNodeHandler`; run on `{without_map}` source
     features.
  5. Process remaining pumps without maps: use `PointProcessor` on remaining
     `{without_map}` source features.

  6. Add all features to layers.

  Wire `pump_map_layer` into `modifiable_layers` when pump_maps are being created.
- **Depends on:** Tasks 2, 3, 4
- **Acceptance:** All four modes work end-to-end: pump-only, attribute-map pump_map,
  point-to-line pump_map, both configured (attribute takes priority).
- **Evidence:** Unit tests in Task 7 pass.

### Tests

#### Task 6: Unit tests for `PumpMapNodeHandler` and `PumpProcessor`
- **Estimate:** ~70 lines
- **Files:** `tests/vector_data_importer/test_integrators.py`,
  `tests/vector_data_importer/test_processors.py`
- **Description:**
  - `PumpMapNodeHandler`: test start node created + pump created with correct geometry
    and `connection_node_id`; test end node created + `connection_node_id_end` set; test
    pump_map geometry adjusted to line between nodes; test pump follows when
    fix_structure_placement shifts the pump_map.
  - `PumpProcessor`: test pump-only (no end node); test attribute mapping → pump +
    pump_map; test point_to_line fallback → pump + pump_map; test attribute mapping
    takes priority; test pump_map skipped when end node snap fails.
- **Depends on:** Tasks 2, 3
- **Acceptance:** All new tests pass; existing processor and integrator tests still pass.
- **Evidence:** `pytest tests/vector_data_importer/test_processors.py tests/vector_data_importer/test_integrators.py -q --tb=short` passes.

#### Task 7: Unit tests for `PumpsImporter` multi-phase flow
- **Estimate:** ~70 lines
- **Files:** `tests/vector_data_importer/test_importers.py`
- **Description:**
  - Test pump-only import (no pump_map settings configured).
  - Test attribute mapping → pump + pump_map created.
  - Test point_to_line fallback → pump + pump_map created.
  - Test attribute mapping takes priority over point_to_line.
  - Test no end node resolvable → pump only (no pump_map).
  - Test pump without map goes through standard PointProcessor flow.
  - Test `modifiable_layers` includes `pump_map_layer` when pump_maps are created.
- **Depends on:** Task 5
- **Acceptance:** All new tests pass; existing pump importer tests still pass.
- **Evidence:** `pytest tests/vector_data_importer/test_importers.py -q --tb=short` passes.

## Notes

- `PumpProcessor` is the primary processor for all pump imports. `PointProcessor` is
  unchanged and remains used by other structures.
- The pump is at the START of the pump_map line, not the center (unlike weirs/orifices
  where `PointToLineSettings` places the point at center).
- Attribute mapping for the end connection node uses `get_field_config_value` (same
  pattern as `LineProcessor.update_connection_nodes`).
- `ConnectionNodeSettings.snap_distance` is used for both start and end point snapping.
- Orphaned nodes do not arise: pumps-with-maps never get a connection node until
  `PumpMapNodeHandler` assigns one after final placement.
- No new integration tests (`test_conversion`) are required.
- Open question from design: should a missing mapped connection node ID emit a
  `ProcessorWarning` and fall through to point_to_line, or silently fall through?
  Resolve during Task 3 implementation.

## Progress

- [x] Task 1: Extract `StructureNodeHandler` + add `node_handler` to `LinearIntegrator`
- [x] Task 2: `PumpMapNodeHandler`
- [x] Task 3: `PumpProcessor`
- [x] Task 4: Remove `PumpLineProcessor` and `PumpSettings`
- [x] Task 5: `PumpsImporter.import_features` multi-phase override
- [x] Task 6: Unit tests for `PumpMapNodeHandler` and `PumpProcessor`
- [x] Task 7: Unit tests for `PumpsImporter` multi-phase flow
