---
feature: pump-map-import
status: complete
created: 2026-07-16
related: .minispec/specs/feat_392_pump_import/design.md
---

# Pump Map Import Design

## Overview

Extend pump import to support `PumpMap` creation from point sources. Two methods are
supported for resolving the pump_map end point: attribute mapping (a connection node ID
mapped from the source feature) and point-to-line projection (length + azimuth from
`PointToLineSettings`). Attribute mapping takes priority; point-to-line is the fallback.
If no end point can be resolved, only a pump is created (no pump_map).

The existing line-source pump import (`PumpLineProcessor`) is removed. All pump import
modes are now point-source only.

## Context

Built on top of `feat_392_pump_import`, which introduced:
- `PointStructurePlacement` strategy for pump integration onto conduits
- `StructurePlacementStrategy` ABC + `LineStructurePlacement`
- `LinearIntegrator` strategy composition

This design extends that foundation with a `node_handler` composition layer and a
multi-phase import flow in `PumpsImporter`.

## User Stories

- As a modeller, I want to import pumps from a point layer and have pump_maps created
  automatically using a mapped connection node ID from my source data.
- As a modeller, I want to import pumps from a point layer and have pump_maps created
  using a projected line (length + azimuth) when no connection node is mapped.
- As a modeller, I want attribute mapping to take priority over point-to-line projection
  when both are configured.
- As a modeller, I want pump_maps to be integrated onto pipes or channels, with the pump
  placed at the correct position on the conduit.
- As a modeller, I want pumps without pump_maps to still be importable (and integratable)
  as before.

## Import Flow

```
PumpsImporter.import_features():

Phase A: Pump_map creation + integration

  1. Build in-memory PumpMap source layer
     - For each source feature (transformed to target CRS):
       a. Try attribute mapping: get_field_config_value → look up connection node → get location
       b. Fallback: point_to_line → project end point (pump location is START of line, not center)
       c. If end point found → add to in-memory layer:
            geometry = line(pump point → end point)
            fields   = copy of all source layer fields
       d. If no end point → feature goes to {without_map} set

  2. Integrate pump_maps  [if integration enabled]
     - Standard integrator flow on in-memory source layer
     - Uses LineStructurePlacement (existing) + PumpMapNodeHandler (new)
     - PumpMapNodeHandler per placed pump_map:
         Start: find/create node → create pump (geometry + connection_node_id) → set pump_map.pump_id
         End:   find/create node → set pump_map.connection_node_id_end
         Adjust pump_map geometry to line between start node and end node
     - Returns integrated_ids + remaining (non-integrated) source feature ids

  3. Process remaining pump_maps  (no conduit match, or integration disabled)
     - For each remaining in-memory source feature:
         Create pump: snap/create node at start point (per ConnectionNodeSettings)
         Create pump_map: snap/create node at end point (per ConnectionNodeSettings)
           → if no node can be found/created: skip pump_map, pump still created
         Adjust pump_map geometry to line between nodes
         Set pump_map.pump_id + connection_node_id_end

Phase B: Pumps without maps

  4. Integrate pumps without maps  [if integration enabled]
     - Standard integrator flow on {without_map} source features
     - Uses PointStructurePlacement (existing) + StructureNodeHandler (new, extracted)

  5. Process remaining pumps without maps
     - Standard PointProcessor flow (snap/create node, set connection_node_id)

  6. Add all features to layers
```

## Key Geometry Note

For pump_maps, the pump location is the **start** of the line, not the center.
This differs from weirs/orifices where `PointToLineSettings` places the source point
at the center. The pump_map geometry is:

```
start_point = pump location (transformed source feature point)
end_point   = location of mapped connection node
            OR start_point.project(length, azimuth)  [point_to_line fallback]
```

## Components

### 1. `PumpMapNodeHandler`  (new, `integrators.py`)

Handles node assignment and pump creation for integrated pump_map features.
Composed into `LinearIntegrator` alongside the existing `strategy`.

**Responsibilities:**
- Start point: find/create connection node, create pump feature (geometry = node
  location, `connection_node_id` = node id), set `pump_map.pump_id`
- End point: find/create connection node, set `pump_map.connection_node_id_end`
- Adjust pump_map geometry to the line between start node and end node

**Receives:** pump layer + pump fields + pump `FeatureManager` + `fields_configurations`
for pump attribute mapping.

### 2. `StructureNodeHandler`  (new, extracted, `integrators.py`)

Extracted from the current inline `update_feature_endpoints` logic on `LinearIntegrator`.
Handles the standard two-connection-node case (`connection_node_id_start` +
`connection_node_id_end`) used by Weir, Orifice, Culvert, and pumps-without-maps.

This extraction is needed so both handlers share the same interface and `LinearIntegrator`
can delegate to either.

### 3. `LinearIntegrator` — add `node_handler` composition

Add a `node_handler` parameter (default: `StructureNodeHandler`). In
`integrate_structure_features`, replace the direct call to `self.update_feature_endpoints`
with `self.node_handler.update_nodes(...)`. Both `PipeIntegrator` and `ChannelIntegrator`
inherit this automatically — no subclass changes needed.

### 4. In-memory PumpMap source layer  (`importers.py`)

A temporary `QgsVectorLayer("LineString", ..., "memory")` built in
`PumpsImporter.import_features`. Schema = copy of all source layer fields plus line
geometry. Fed to the standard integrator as if it were a real external source layer.

### 5. `PumpsImporter.import_features` override  (`importers.py`)

Override with the multi-phase flow described above. Uses `FeatureManager.create_new` +
`update_attributes` directly for pump creation in phases A and B (rather than
`PointProcessor`) to avoid the node-creation side effect.

### 6. Remove `PumpLineProcessor`  (`processors.py`)

No longer needed. Line-source pump import is removed entirely.

### 7. Remove `PumpSettings`  (`settings_models.py`)

The `direction` field is no longer relevant. Direction is expressed via `azimuth` in
`PointToLineSettings`.

## Data Model

No schema changes. Uses existing:
- `dm.Pump` (point geometry, `connection_node_id`)
- `dm.PumpMap` (line geometry, `pump_id`, `connection_node_id_end`)
- `PointToLineSettings` (existing, `length` + `azimuth` field map configs)
- `ConnectionNodeSettings` (existing, controls snap + create_nodes behaviour)

## Connection Node Behaviour

Both endpoints of a pump_map use `ConnectionNodeSettings` for node resolution:
- `snap_distance` — used on both start and end points
- `create_nodes` — controls whether new nodes are created when none is found

The pump's `connection_node_id` and geometry are set by `PumpMapNodeHandler` after
`fix_structure_placement` has determined the final position on the conduit. This ensures
the pump always matches the pump_map start point, even if placement shifted the pump_map.

## Scope

**In scope:**
- Multi-phase `PumpsImporter.import_features` override
- `PumpMapNodeHandler` + `StructureNodeHandler` composition on `LinearIntegrator`
- In-memory pump_map source layer construction
- Attribute mapping + point_to_line fallback for end point resolution
- Unit tests: new and modified tests for affected components
- Remove `PumpLineProcessor` and `PumpSettings`

**Out of scope:**
- Integration tests (`test_conversion`) — no new ones needed
- UI / wizard changes for new pump_map settings
- Processing algorithm updates

## Open Questions

- When building the in-memory source layer, attribute mapping uses
  `get_field_config_value` to resolve a connection node ID. Should this silently skip
  features where the mapped node ID does not exist in the schematisation, or emit a
  `ProcessorWarning`? (Likely: emit a warning and fall through to point_to_line.)
