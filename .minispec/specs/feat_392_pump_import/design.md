---
feature: pump-importer
status: complete
created: 2026-07-06
decisions:
  - 20260706-1200-strategy-pattern-composition
  - 20260706-1200-point-structure-placement
---

# Pump Importer Design

## Overview

Add pump import support to the vector_data_importer by introducing a
StructurePlacementStrategy pattern. This separates conduit-generic logic
(matching, cutting, node management) from structure-type-specific placement
(line substring vs point projection), enabling both existing line structures
(Weir, Orifice, Culvert) and new point structures (Pump) to integrate onto
pipes and channels via composition.

## User Stories

- As a modeller, I want to import pumps from a table with point geometries
  so they are placed in my schematisation with correct connection nodes.
- As a modeller, I want to import pumps from a table with line geometries
  (using the line centroid) when my source data represents pumps as lines.
- As a modeller, I want imported pumps to snap to existing connection nodes
  within a configurable distance.
- As a modeller, I want imported pumps to optionally integrate into a
  pipe or channel, cutting the conduit at the pump's projected position.

## Components

### 1. StructurePlacementStrategy (ABC)

**File:** `integrators.py`

**Purpose:** Encapsulates structure-type-specific behaviour for integration.

**Interface:**

```python
class StructurePlacementStrategy(ABC):
    @abstractmethod
    def get_structure_data(self, structure_feat, conduit_feat) -> LinearIntegratorStructureData:
        """Compute position (m) and length for structure on conduit."""
        ...

    @abstractmethod
    def place_structure(self, conduit_geom, structure_data, target_fields, target_manager, fields_configurations, target_model_cls) -> QgsFeature:
        """Create structure feature with correct geometry."""
        ...

    @abstractmethod
    def update_structure_nodes(self, feature, node_by_location, node_layer_fields, node_attributes, node_manager) -> list:
        """Assign connection node(s) and create new nodes if needed."""
        ...
```

### 2. LineStructurePlacement

**Purpose:** Handles line-target structures (Weir, Orifice, Culvert).

**Behaviour:**
- `get_structure_data`: uses `lineLocatePoint(centroid())` for line input,
  `lineLocatePoint(point)` for point input. Length from geometry or config.
- `place_structure`: extracts `curveSubstring(m - l/2, m + l/2)` from conduit.
  Simplifies to 2-point line unless target is Culvert.
- `update_structure_nodes`: assigns `connection_node_id_start` and
  `connection_node_id_end` at feature endpoints.

**Note:** This encapsulates current behaviour from `integrate_structure_features`,
`place_structures_on_conduit`, and `update_feature_endpoints`.

### 3. PointStructurePlacement

**Purpose:** Handles point-target structures (Pump).

**Behaviour:**
- `get_structure_data`: uses `lineLocatePoint(point_geom)`. Length = 0.
- `place_structure`: uses `conduit_geom.interpolate(m)` → point geometry.
- `update_structure_nodes`: assigns single `connection_node_id` at the point.

### 4. Extended PointProcessor

**File:** `processors.py`

**Change:** Extend `create_new_point_geometry` (on `SpatialProcessor`) to handle
line geometry input by extracting the centroid:

```python
@classmethod
def create_new_point_geometry(cls, src_geom):
    geometry_type = src_geom.type()
    if geometry_type == QgsWkbTypes.GeometryType.PointGeometry:
        return QgsGeometry.fromPointXY(src_geom.asPoint())
    elif geometry_type == QgsWkbTypes.GeometryType.LineGeometry:
        centroid = src_geom.centroid()
        return QgsGeometry.fromPointXY(centroid.asPoint())
    else:
        raise NotImplementedError(f"Unsupported geometry type: '{geometry_type}'")
```

### 5. Updated LinearIntegrator

**File:** `integrators.py`

**Changes:**
- Constructor receives a `StructurePlacementStrategy` instance.
- `integrate_structure_features` delegates to strategy for:
  - Structure data computation (instead of inline `get_conduit_structure_from_*`)
  - Structure placement (instead of inline `place_structures_on_conduit`)
  - Node assignment (instead of inline `update_feature_endpoints`)
- `get_conduit_matches`, `cut_conduit`, `get_conduit_cuts`,
  `fix_structure_placement` remain on `LinearIntegrator` (shared).

### 6. Updated get_integrator() Factory

**File:** `integrators.py`

**Change:** Add `dm.Pump` to valid models for both PipeIntegrator and
ChannelIntegrator creation:

```python
@staticmethod
def get_integrator(integrate_layer, cross_section_layer, importer):
    integration_mode = importer.import_settings.integration.integration_mode
    if integration_mode == IntegrationMode.CHANNELS:
        return ChannelIntegrator.from_importer(...)
    elif integration_mode == IntegrationMode.PIPES and importer.target_model_cls in [
        dm.Weir, dm.Orifice, dm.Pump,
    ]:
        return PipeIntegrator.from_importer(integrate_layer, importer)
```

## Data Model

No schema changes. Uses existing:
- `dm.Pump` (point geometry, single `connection_node_id`)
- `LinearIntegratorStructureData` (with `length=0` for point structures)
- `ConnectionNodeSettings` (existing snap/create_nodes config)

## Integration Flow for Pump

```
Source table (point or line geometry)
    ↓
PointProcessor.process_feature()
    - create_new_point_geometry (line → centroid if needed)
    - snap/create connection node
    ↓
Target layer (Pump features with point geometry)
    ↓  (if integration enabled)
LinearIntegrator with PointStructurePlacement strategy
    - get_conduit_matches (buffer point, check intersection)
    - get_structure_data (lineLocatePoint → m, length=0)
    - fix_structure_placement (ensure min segment lengths; shifts m as needed)
    - place_structure (interpolate → point on conduit)
    - cut_conduit (split at m → two segments)
    - update_structure_nodes (single connection_node_id)
    ↓
Result: Pump at projected position on conduit + conduit split into 2 segments
```

## Scope

**In scope:**
- `PointProcessor`: handle line→centroid geometry conversion
- `StructurePlacementStrategy` ABC with `LineStructurePlacement` and `PointStructurePlacement`
- Refactor `LinearIntegrator.integrate_structure_features` to use strategy
- Factory `get_integrator` supports `dm.Pump` for pipe and channel integration

**Out of scope (later tasks):**
- PumpMap entries
- UI / wizard pages
- Processing algorithm

## Open Questions

- Does `fix_structure_placement_rhs` need adjustment for length=0?
  The check `prev_end + cs.length <= conduit_length` with length=0 becomes
  `prev_end <= conduit_length` which is always true. Verify during implementation
  whether this causes any edge case at the right end of a conduit.
- Shared node between pump and adjacent conduit endpoints: the pump and the
  conduit segments share the same connection node (consistent with how
  line structures work today). Confirm during implementation.
