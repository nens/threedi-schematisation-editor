---
feature: pump-importer-hydamo-line-mode
status: complete
created: 2026-07-14
decisions:
  - 20260714-hydamo-line-pump-import
---

# Pump Import: HyDaMo Line Mode Design

## Overview

Extend `PumpsImporter` to handle two input geometry types, auto-detected from
the source layer:

- **Point source** → existing behaviour (`PointProcessor`, target `dm.Pump`)
- **Line source** → new HyDaMo mode (`PumpLineProcessor`, target `dm.Pump` with
  secondary `dm.PumpMap` output; integration targets `dm.PumpMap`)

In HyDaMo mode each source line represents a pump_map: the pump sits at the
start of the line and a connection node is snapped or created at the end. An
optional direction field (integer, default `1`) can reverse the line before
processing when its value is `-1`.

## User Stories

- As a modeller, I want to import pumps from a HyDaMo pump_map layer (line
  geometry) so that pumps, pump_maps, and connection nodes are created
  automatically.
- As a modeller, I want the pump placed at the start of each source line and a
  connection node snapped or created at the end.
- As a modeller, I want to supply a direction field so that lines with value -1
  are reversed before the pump and connection node are placed.
- As a modeller, I want the imported pump_map to integrate into the pipe network
  the same way a weir or orifice does (conduit split at pump_map endpoints).

## Components

### 1. `PumpDirectionSettings` — `settings_models.py`

New `BaseModel` for the direction field configuration:

```python
class PumpDirectionSettings(BaseModel):
    metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[ColumnImportMethod.ATTRIBUTE, ColumnImportMethod.DEFAULT]
    )
    name: ClassVar[str] = "pump_direction"
    direction: FieldMapConfig[int] = FieldMapConfig[int].with_metadata(metadata)(
        method=ColumnImportMethod.DEFAULT, default_value=1
    )
```

Add to `ImportSettings`:

```python
pump_direction: PumpDirectionSettings = PumpDirectionSettings()
```

### 2. `PumpLineProcessor` — `processors.py`

New class extending `StructureProcessor`. Primary target is `dm.Pump`; creates
`dm.PumpMap` as secondary output (mirrors how `SurfaceProcessor` creates
`SurfaceMap` alongside `Surface`).

**Constructor** — takes `target_layer` (Pump), `pump_map_layer`, `node_layer`,
`import_settings`. Creates:
- `self.pump_map_layer` — the PumpMap layer
- `self.pump_map_manager = FeatureManager(get_next_feature_id(pump_map_layer))`
- `self.direction_config = import_settings.pump_direction.direction`

**`process_feature(src_feat)`**:

1. Get line geometry from source feature.
2. Resolve direction: `get_field_config_value(direction_config, src_feat)`.
   If `-1`, reverse the polyline.
3. Simplify to `[polyline[0], polyline[-1]]`.
4. Snap/create `ConnectionNode` at `polyline[0]`.
5. Create **Pump** (point) at `polyline[0]`; assign `connection_node_id`.
6. Snap/create `ConnectionNode` at `polyline[-1]`.
7. Create **PumpMap** (line `polyline[0]` → `polyline[-1]`);
   assign `pump_id = pump.id` and `connection_node_id_end = end_node.id`.
8. Apply `fields_configurations` to Pump; apply `pump_map_fields_configurations`
   to PumpMap (sourced from `import_settings.pump_map_fields`).
9. Apply `cn_fields_configurations` to new connection nodes.
10. Add new nodes to `node_layer`; rebuild node locator.
11. Return:
    ```python
    {
        self.target_name: [pump_feat],           # Pump layer
        self.pump_map_layer.name(): [pump_map_feat],  # PumpMap layer
    }
    ```

### 3. `PumpsImporter` — `importers.py`

**Changes:**
- Add `pump_map_layer=None` parameter.
- In `__init__`, detect source geometry type from `external_source`:
  - **Point** → `processor = PointProcessor(...)` (unchanged)
  - **Line** → `processor = PumpLineProcessor(target_layer, pump_map_layer, node_layer, import_settings)`

**New integration-target properties** (override to redirect integrator to PumpMap):

```python
@property
def integration_model_cls(self):
    if isinstance(self.processor, PumpLineProcessor):
        return dm.PumpMap
    return self.target_model_cls

@property
def integration_layer(self):
    if isinstance(self.processor, PumpLineProcessor):
        return self.pump_map_layer
    return self.target_layer

@property
def integration_manager(self):
    if isinstance(self.processor, PumpLineProcessor):
        return self.processor.pump_map_manager
    return self.processor.target_manager
```

Optionally, add default implementations of these three properties to the base
`IntegrationImporter` class so all other importers inherit no-op defaults.

### 4. `PipeIntegrator.from_importer` — `integrators.py`

Update to read from integration properties instead of target properties:

```python
@classmethod
def from_importer(cls, integrate_layer, importer):
    model_cls = getattr(importer, 'integration_model_cls', importer.target_model_cls)
    target_layer = getattr(importer, 'integration_layer', importer.target_layer)
    target_manager = getattr(importer, 'integration_manager', importer.processor.target_manager)

    if model_cls.__geometrytype__ == GeometryType.Point:
        strategy = PointStructurePlacement()
    elif model_cls.__geometrytype__ == GeometryType.Linestring:
        strategy = LineStructurePlacement(
            importer.import_settings.point_to_line_conversion.length,
            model_cls != dm.Culvert,
        )
    else:
        raise NotImplementedError(...)

    return cls(
        integrate_layer,
        model_cls,           # was: importer.target_model_cls
        target_layer,        # was: importer.target_layer
        target_manager,      # was: importer.processor.target_manager
        importer.node_layer,
        importer.processor.node_manager,
        importer.import_settings,
        importer.external_source,
        importer.target_gpkg,
        strategy,
    )
```

The allowed-models check at `get_integrator` (currently `[dm.Weir, dm.Orifice,
dm.Pump]`) stays unchanged — `importer.target_model_cls` is still `dm.Pump`.

## Data Model

No schema changes. Uses existing:
- `dm.Pump` — point geometry, single `connection_node_id`
- `dm.PumpMap` — line geometry, `pump_id` + `connection_node_id_end`
- `dm.ConnectionNode` — point geometry

## Integration Flow (HyDaMo line mode)

```
Source layer (LineString geometry)
    ↓
PumpLineProcessor.process_feature()
    - reverse line if direction == -1
    - snap/create ConnectionNode at line[0]
    - create Pump at line[0] → connection_node_id
    - snap/create ConnectionNode at line[-1]
    - create PumpMap (line[0]→line[-1]) → pump_id, connection_node_id_end
    ↓
Target layers: Pump (point) + PumpMap (line)
    ↓  (if integration enabled)
PipeIntegrator with LineStructurePlacement (via integration_model_cls=dm.PumpMap)
    - get_conduit_matches (intersects PumpMap line with conduit buffer)
    - get_structure_data (lineLocatePoint on PumpMap centroid)
    - place_structure (curveSubstring → PumpMap geometry replaced by conduit segment)
    - cut_conduit (split conduit at PumpMap endpoints)
    - update_structure_nodes (assign connection_node_id_start/_end)
    ↓
Result: Pump at start node, PumpMap as conduit segment, conduit split into segments
```

## Scope

**In scope:**
- `PumpDirectionSettings` in `settings_models.py`
- `PumpLineProcessor` in `processors.py`
- `PumpsImporter` auto-detection + integration-target properties
- `PipeIntegrator.from_importer` reading integration properties
- Default integration-target properties on `IntegrationImporter` base class

**Out of scope:**
- Wizard UI wiring (passing `pump_map_layer`, exposing PumpMap field mappings)
- Processing algorithm registration
- ChannelIntegrator support for pump_map (pipes-only for now)

## Open Questions

- What PumpMap field mappings should the wizard expose?
  Candidates: `code`, `display_name`, `tags`. Needs wizard wiring investigation.
- Should `pump_map_fields` be a separate key in `ImportSettings` (like
  `connection_node_fields`) or merged into `fields`?
- Should direction values beyond `1`/`-1` be validated/rejected, or silently
  treated as positive?
