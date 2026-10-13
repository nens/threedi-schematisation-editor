# Decision: Generic Importer Design

**ID**: 20260722-071549-generic-importer-design
**Date**: 2026-07-22
**Status**: accepted
**Feature**: generic-importer

## Context

Designing a generic importer for the vector data importer subsystem. Unlike existing
importers (Pipes, Channels, etc.) where the target layer is predefined, the generic
importer lets users choose any source and target layer with a simple field map.

## Decisions

### 1. New `GenericProcessor` class (not reuse `ConnectionNodeProcessor`)

Reusing `ConnectionNodeProcessor` would require parameterizing away its point-coercion
logic, making it confusing. A new class is cleaner.

### 2. Geometry check in `GenericImporter._validate_geometry_compatibility`

The importer already holds both `external_source` and `target_layer`. Checking there
allows failing before `start_editing()` is called, giving a clear error without
partial state.

### 3. Geometry coercion via `get_src_geometry(none_ok=True)`

Using the existing utility keeps behaviour consistent with all other processors
(linearize, flatten to 2D, single-part). `none_ok=True` allows non-spatial features
to pass through silently.

### 4. Reuse `ImportSettings` — only read `.fields`

A new minimal settings model would be another class to maintain. The generic importer
only needs `import_settings.fields`; the unused sub-models on `ImportSettings` are
harmless.

### 5. Base `GenericProcessor` on `SpatialProcessor`

`SpatialProcessor.__init__` provides `target_manager`, `target_fields`, `target_name`,
`transformation`, and `context` for free. The unused methods (`snap_connection_node`,
`create_new_point_geometry`) are harmless static/class methods.

### 6. Non-spatial target support

`new_geometry` returns `None` for features without geometry. `FeatureManager.create_new`
already calls `new_feat.setGeometry(geom)` only when `geom` is truthy, so `None` is
safely ignored — no geometry is set on the output feature.

## Consequences

- Two small new classes added to existing files (`processors.py`, `importers.py`).
- No new settings models, no new utilities.
- Processing algorithm and UI are deferred to follow-up work.
