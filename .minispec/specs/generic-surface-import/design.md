# Feature Specification: Generic Surface Import

**Created**: 2026-06-22  
**Status**: Complete
**Input**: Import surfaces + surface_map from a polygon layer in a single wizard operation, generic enough for any source but pre-configurable for BGT inlooptabel data.

---

## User Scenarios & Testing

### User Story 1 — Import surfaces + surface_map from BGT inlooptabel (Priority: P1)

A modeller has a BGT inlooptabel GeoPackage (`4_BGT_inlooptabel`) with polygon
surfaces, surface type attributes, and per-sewer-type runoff percentage columns.
They want to import all surfaces into the schematisation and have them linked to
the sewer network — in one operation, without manual SQL or multi-step algorithm
runs.

**Why this priority**: This is the primary use case driving the feature. Everything
else is in service of this journey.

**Independent Test**: Can be fully tested by loading the BGT test GeoPackage
(`v1_BGT_inlooptabel_20260318.gpkg`), opening the wizard, configuring filter +
sewer mappings + field map, running import, and verifying that:
- Surface features appear in the Surface layer with correct geometries and `surface_parameters_id`
- Surface_map features appear linking each surface to the correct connection node for each configured sewer type
- Surfaces where `maaiveld + open_water >= 100` are excluded

**Acceptance Scenarios**:

1. **Given** a BGT GeoPackage source layer with 235 features (including some with
   `maaiveld + open_water = 100`), **When** the user runs the wizard with a filter
   expression `"maaiveld" + "open_water"` / threshold `100`, **Then** excluded
   surfaces do not appear in the Surface layer.

2. **Given** a sewer type mapping with `gemengd_riool → Combined sewer` and
   `hemelwaterriool → Storm drain`, **When** import runs, **Then** each surface
   where `gemengd_riool > 0` has a surface_map entry to the nearest combined sewer
   connection node with `percentage = gemengd_riool value`, and likewise for storm
   drain.

3. **Given** a source feature with `CurvePolygon` geometry, **When** the processor
   runs, **Then** it is converted to `Polygon` automatically and `area` is computed
   from the geometry.

4. **Given** a surface with no pipe within `search_distance` for a given sewer
   type, **When** linking runs, **Then** no surface_map entry is created for that
   type (silently skipped, logged as a warning).

---

### User Story 2 — Save and reload import configuration (Priority: P2)

A modeller configures the wizard once for BGT data (filter, sewer mappings, field
map with `surface_parameters_id` expression). They save this as a JSON preset and
reload it next time for a different project.

**Why this priority**: Reduces repeated setup for the common BGT workflow. Directly
supports the "BGT settings from settings file" requirement.

**Independent Test**: Save config → close wizard → reopen wizard → load config →
verify all settings are restored correctly.

**Acceptance Scenarios**:

1. **Given** a fully configured wizard, **When** the user saves the config to JSON,
   **Then** the file contains surface filter, sewer type mappings, spatial linking
   params, and field map entries.

2. **Given** a saved BGT config JSON, **When** the user opens the wizard and loads
   it, **Then** all settings are restored: filter expression, sewer column
   assignments, search distance, and field map.

---

### User Story 3 — Generic import from non-BGT polygon source (Priority: P3)

A modeller has a custom polygon layer with a single percentage column (e.g.
`runoff_pct`) and wants to link all surfaces to the combined sewer only.

**Why this priority**: The generic design should support non-BGT sources, but this
is secondary to the BGT use case.

**Independent Test**: Can be tested with any polygon layer having at least one
numeric column, one configured sewer type row, and a pipe + node layer in the
project.

**Acceptance Scenarios**:

1. **Given** a polygon layer with `runoff_pct` column and only `Combined sewer`
   row filled in the sewer mapping table, **When** the import runs, **Then** only
   combined sewer surface_map entries are created; other sewer types produce no
   entries.

---

### Edge Cases

- Source surface with `percentage_column` value of exactly `0`: excluded from
  linking for that sewer type (no surface_map entry created).
- Source surface with no pipe within `search_distance`: silently skipped for that
  sewer type; warning logged in Run page.
- Filter expression evaluates to NULL: treat as not excluded (safe default).
- `surface_parameters_id` expression returns NULL: feature is still imported; NULL
  value will be caught by schema validation later.
- Source layer CRS differs from project CRS: geometry is reprojected (standard
  SpatialProcessor behaviour).
- Surface_map layer, pipe layer, or connection node layer not set: validation error
  before run starts.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST import polygon features from any user-selected polygon
  layer into the schematisation's Surface layer.
- **FR-002**: System MUST automatically convert CurvePolygon geometry to Polygon.
- **FR-003**: System MUST automatically compute `area` from geometry (not mapped
  from source).
- **FR-004**: System MUST support a configurable filter: surfaces where a
  field/expression evaluates to a value ≥ threshold are excluded.
- **FR-005**: System MUST support mapping up to 11 sewer types (all `SewerageType`
  enum values) to source percentage columns; unmapped types are skipped.
- **FR-006**: System MUST create surface_map entries by spatially linking each
  surface to the nearest pipe of the configured sewer type, then to the nearest of
  that pipe's two connection nodes.
- **FR-007**: System MUST set `surface_map.percentage` to the actual value from the
  configured source column (not 100.0 placeholder).
- **FR-008**: System MUST support configuring search_distance, stormwater sewer
  preference, and sanitary sewer preference for spatial linking.
- **FR-009**: System MUST allow the user to select the target surface_map layer,
  pipe layer, and connection node layer (defaulting to the schematisation's own
  layers).
- **FR-010**: System MUST support save/load of the full configuration as JSON.
- **FR-011**: System MUST keep Surface and Surface_map layers in editing mode after
  import so the user can review before committing.
- **FR-012**: Surfaces where `percentage_column = 0` for a given sewer type MUST
  NOT get a surface_map entry for that type.

### Key Entities

- **Surface**: polygon feature with `id`, `area` (computed), `surface_parameters_id`,
  `code`, `display_name`, `tags`.
- **SurfaceMap**: linestring feature (surface centroid → connection node) with
  `id`, `surface_id`, `connection_node_id`, `percentage`, `code`, `display_name`,
  `tags`.
- **SewerTypeMapping**: runtime config pairing a `SewerageType` to a source column
  name; null column = skip that type.
- **SurfaceFilterConfig**: method (ATTRIBUTE or EXPRESSION) + source_attribute or
  expression + threshold (default 100).
- **SurfaceLinkingSettings**: search_distance, stormwater_sewer_preference,
  sanitary_sewer_preference.

---

## Success Criteria

- **SC-001**: A BGT inlooptabel with 235 features imports in a single wizard run
  with correct surfaces, correct surface_map entries, and correct exclusion of
  maaiveld+open_water=100 surfaces.
- **SC-002**: Saved JSON config round-trips correctly: save → load restores all
  settings.
- **SC-003**: Surfaces with no nearby pipe for a given sewer type are silently
  skipped (no crash, warning logged).
- **SC-004**: Integration tests pass using the BGT test GeoPackage.

---

## Architecture

### Wizard Page Flow

```
Start Page → Surface Settings Page → Field Map Page → Run Page
```

| Page | Purpose |
|------|---------|
| Start | Source polygon layer selection, "use selected features" toggle, load/save config JSON |
| Surface Settings | Filter config, sewer type mapping table (11 rows), spatial linking parameters |
| Field Map | Field map for Surface: `id` (auto), `code`, `display_name`, `surface_parameters_id`, `tags`. `area` is not shown (auto-computed). |
| Run | Progress bar, log panel, cancel button |

No CN Field Map page. No connection node creation. Surface_map features are
created by the processor — not configured by the user directly.

---

### Surface Settings Page — Three Sections

#### Section 1: Surface Filter

| Element | Notes |
|---------|-------|
| Method selector | ATTRIBUTE or EXPRESSION |
| Source attribute / Expression input | Evaluates to a numeric value per feature |
| Threshold | float, default 100.0 |

Semantics: features where `evaluated_value >= threshold` are excluded. If no
filter is configured, all features are imported.

#### Section 2: Sewer Type Mapping Table

One row per `SewerageType` enum value (11 rows):

| Column | Widget |
|--------|--------|
| Sewer type | Read-only label |
| Percentage column | ComboBox populated from source layer fields; blank = skip |

#### Section 3: Spatial Linking Parameters

| Parameter | Default |
|-----------|---------|
| Surface map layer | Schematisation "Surface map" layer |
| Pipe layer | Schematisation "Pipe" layer |
| Selected pipes only | False (checkbox) |
| Connection node layer | Schematisation "Connection node" layer |
| Search distance (m) | 10.0 |
| Stormwater sewer preference (m) | 0.0 |
| Sanitary sewer preference (m) | 0.0 |

---

### Importer & Processor Architecture

#### SurfaceImporter (thin orchestrator)

```
Importer → SpatialImporter → SurfaceImporter (new)
```

Responsibilities:
- Receives all settings and layers
- Puts Surface and Surface_map layers in edit mode
- Builds pipe spatial index (shared across all features/sewer types)
- Calls `SurfaceProcessor.process()`
- Adds returned surface features to Surface layer
- Adds returned surface_map features to Surface_map layer

#### SurfaceProcessor (all per-feature logic)

```
Processor → SpatialProcessor → SurfaceProcessor (new)
```

Responsibilities (in order):
1. **Filter**: evaluate filter field/expression per feature; skip if `>= threshold`
2. **Geometry conversion**: CurvePolygon → Polygon + CRS transform
3. **Area computation**: `QgsGeometry.area()`
4. **Field mapping**: apply standard FieldMapConfig for `id`, `code`,
   `display_name`, `surface_parameters_id`, `tags`
5. **Surface_map creation**: for each sewer type with a configured percentage
   column:
   - Skip feature if `percentage_column value <= 0`
   - Find nearest pipe of that sewerage_type within search_distance (using
     spatial index from importer)
   - Apply stormwater/sanitary preference offsets
   - Pick nearest connection node (start vs end node)
   - Create surface_map feature: `surface_id`, `connection_node_id`,
     `percentage = actual column value`, linestring geom (centroid → node)

The spatial linking logic is extracted from the existing
`LinkSurfacesWithConnectionNodes.processAlgorithm` into a reusable method so
that the future processing algorithm wrapper can call the same code.

---

### Settings Model (Pydantic, in `settings_models.py`)

```python
class SurfaceFilterSettings(BaseModel):
    method: ColumnImportMethod  # ATTRIBUTE or EXPRESSION
    source_attribute: Optional[str] = None
    expression: Optional[str] = None
    threshold: float = 100.0

class SewerTypeMapping(BaseModel):
    sewerage_type: int          # SewerageType enum value
    percentage_column: Optional[str] = None  # None = skip

class SurfaceLinkingSettings(BaseModel):
    search_distance: float = 10.0
    stormwater_sewer_preference: float = 0.0
    sanitary_sewer_preference: float = 0.0

class SurfaceSettings(BaseModel):
    name: ClassVar[str] = "surface"
    filter: SurfaceFilterSettings = SurfaceFilterSettings()
    sewer_type_mappings: list[SewerTypeMapping] = []
    linking: SurfaceLinkingSettings = SurfaceLinkingSettings()
```

`ImportSettings` gets a new `surface: SurfaceSettings = SurfaceSettings()` field.

Layer references (surface_map, pipe, connection node layers) are NOT serialized —
they are runtime selections resolved from the QGIS project by name.

---

### Example BGT Preset JSON

```json
{
    "surface": {
        "filter": {
            "method": "expression",
            "expression": "\"maaiveld\" + \"open_water\"",
            "threshold": 100.0
        },
        "sewer_type_mappings": [
            {"sewerage_type": 0, "percentage_column": "gemengd_riool"},
            {"sewerage_type": 1, "percentage_column": "hemelwaterriool"},
            {"sewerage_type": 2, "percentage_column": "vuilwaterriool"},
            {"sewerage_type": 8, "percentage_column": "infiltratievoorziening"}
        ],
        "linking": {
            "search_distance": 10.0,
            "stormwater_sewer_preference": 0.0,
            "sanitary_sewer_preference": 0.0
        }
    },
    "fields": {
        "id": {"method": "auto"},
        "surface_parameters_id": {
            "method": "expression",
            "expression": "CASE WHEN \"type_verharding\" = 'dak' AND \"hellingstype\" = 'hellend' THEN 107 WHEN \"type_verharding\" = 'dak' THEN 108 WHEN \"type_verharding\" = 'gesloten verhard' THEN 102 WHEN \"type_verharding\" = 'open verhard' AND \"graad_verharding\" = 100 THEN 105 WHEN \"type_verharding\" = 'open verhard' AND \"graad_verharding\" = 50 THEN 114 WHEN \"type_verharding\" = 'onverhard' THEN 111 ELSE NULL END"
        },
        "code": {"method": "ignore"},
        "display_name": {"method": "ignore"},
        "tags": {"method": "ignore"}
    }
}
```

---

## Files to Create / Modify

| File | Change |
|------|--------|
| `vector_data_importer/settings_models.py` | Add `SurfaceFilterSettings`, `SewerTypeMapping`, `SurfaceLinkingSettings`, `SurfaceSettings`; extend `ImportSettings` |
| `vector_data_importer/processors.py` | Add `SurfaceProcessor` |
| `vector_data_importer/importers.py` | Add `SurfaceImporter` |
| `vector_data_importer/wizard/settings_widgets.py` | Add `SurfaceSettingsWidget` |
| `vector_data_importer/wizard/wizard.py` | Add `ImportSurfaceWizard` |
| `vector_data_importer/wizard/__init__.py` | Export `ImportSurfaceWizard` |
| `__init__.py` (plugin entry) | Register the new wizard in the plugin UI |
| `tests/` | Integration tests using BGT test GeoPackage |

---

## Deferred / Out of Scope

| Item | Notes |
|------|-------|
| Processing algorithm wrapper | "Later we'll add a processing algorithm which wraps around that logic" |
| NWRW prerequisite check | "Skip for now, we'll look into that later" |
| Shipped BGT preset JSON | User saves and reuses their own preset |
| Per-sewer-type filter expression | "Leave that out for now, can add later" |
| Code-based pipe linking | Spatial matching only |
