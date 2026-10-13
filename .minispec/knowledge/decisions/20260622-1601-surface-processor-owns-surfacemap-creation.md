---
type: decision
id: 20260622-1601-surface-processor-owns-surfacemap-creation
date: 2026-06-22
status: accepted
supersedes: null
superseded_by: null
impacts:
  - threedi_schematisation_editor/vector_data_importer/processors.py
  - threedi_schematisation_editor/vector_data_importer/importers.py
tags: [surface-import, processor, surface-map]
participants: [engineer, ai-assistant]
---

# Surface_map Creation Lives in SurfaceProcessor, Not SurfaceImporter

## Context

The surface import needs to create features in two layers: `surface` (one per
source polygon) and `surface_map` (one per surface × sewer type with non-zero
percentage). The question was where to put the surface_map creation logic: in the
importer (orchestration layer) or the processor (per-feature logic layer).

## Options Considered

### Option 1: SurfaceImporter handles surface_map creation
Importer iterates surfaces after processor, runs spatial linking, writes surface_map.
- ✅ Keeps processor focused on single-feature transformation
- ❌ Splits related logic across two classes
- ❌ Inconsistent with how LineProcessor handles all per-feature logic including
  node creation

### Option 2: SurfaceProcessor handles everything
Processor does filter, geometry conversion, area, field mapping, AND surface_map
creation via spatial linking.
- ✅ Consistent with LineProcessor pattern (all per-feature logic in processor)
- ✅ Single class to understand and test
- ✅ Importer stays thin (orchestration only)

## Decision

We chose **Option 2**: `SurfaceProcessor` owns all per-feature logic including
surface_map creation. This is consistent with how `LineProcessor` works, which
also handles connection node creation/snapping as part of its processing.

`SurfaceImporter` receives the spatial index (built once from pipe layer) and
passes it to the processor. The importer then collects both surface features and
surface_map features returned by the processor and adds them to their respective
layers.

## Consequences

### Positive
- ✅ Consistent with existing processor pattern
- ✅ All surface-related logic in one place — easier to test

### Negative
- ⚠️ SurfaceProcessor is slightly heavier than typical processors (handles two
  output feature types)

### Neutral
- Spatial index is built in the importer (once) and passed to the processor to
  avoid rebuilding per sewer type iteration

## Code References

- Comparable pattern: `vector_data_importer/processors.py:LineProcessor`
- Spatial index utility: `utils.py:spatial_index`
