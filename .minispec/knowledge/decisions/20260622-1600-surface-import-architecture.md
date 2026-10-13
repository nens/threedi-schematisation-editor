---
type: decision
id: 20260622-1600-surface-import-architecture
date: 2026-06-22
status: accepted
supersedes: null
superseded_by: null
impacts:
  - threedi_schematisation_editor/vector_data_importer/importers.py
  - threedi_schematisation_editor/vector_data_importer/processors.py
  - threedi_schematisation_editor/vector_data_importer/wizard/wizard.py
tags: [surface-import, vdi, architecture]
participants: [engineer, ai-assistant]
---

# Surface Import: Core Logic in VDI Module, Processing Algorithm Wrapper Later

## Context

Surface/surface_map import does not exist yet. The existing VDI wizard module
handles conduits, structures, cross-sections, and connection nodes. The BGT
inlooptabel use case requires importing surfaces AND creating surface_map linkages
in one operation.

Three approaches were considered: full VDI wizard, standalone processing algorithm,
or hybrid (algorithm + thin wizard wrapper).

## Options Considered

### Option 1: VDI Wizard Extension
Put core logic in the VDI importer/processor hierarchy, expose via a wizard.
- ✅ Consistent UX with existing importers
- ✅ Re-uses threading, progress, field map, save/load config infrastructure
- ✅ Saved JSON config naturally becomes the preset mechanism
- ❌ Writes to two target layers (surface + surface_map) — slight extension of pattern

### Option 2: Standalone Processing Algorithm
Single processing algorithm taking all parameters, producing both layers.
- ✅ Scriptable, batchable
- ❌ No visual field mapping or save/load presets
- ❌ Different workflow from all other imports in the plugin

### Option 3: Hybrid (algorithm + wizard wrapper)
Algorithm for core logic, wizard wraps it.
- ✅ Scriptable + user-friendly
- ❌ Most complex — two interfaces for one feature
- ❌ Doesn't actually re-use VDI wizard infrastructure

## Decision

We chose **Option 1** (VDI wizard extension) with the explicit plan to add a
processing algorithm wrapper later — the same pattern used for other importers
(conduits, structures, etc.) where the algorithm wraps the same core logic.

Core logic lives in `SurfaceImporter` and `SurfaceProcessor` in the VDI module.
The processing algorithm is deferred.

## Consequences

### Positive
- ✅ Single source of truth for core logic when algorithm is added later
- ✅ Consistent UX with existing plugin workflow
- ✅ Config save/load = preset mechanism (no extra infrastructure needed)

### Negative
- ⚠️ SurfaceImporter must manage two target layers in edit mode simultaneously

### Neutral
- Pattern extension is minor: SpatialImporter already manages multiple layers
  (e.g. target + connection nodes layer)

## Code References

- Existing importer hierarchy: `vector_data_importer/importers.py`
- Existing wizard: `vector_data_importer/wizard/wizard.py`
- Parallel: `processing/alghorithms_inflow.py:LinkSurfacesWithConnectionNodes`
