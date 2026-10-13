---
type: decision
id: 20260622-1603-surface-import-spatial-linking-only
date: 2026-06-22
status: accepted
supersedes: null
superseded_by: null
impacts:
  - threedi_schematisation_editor/vector_data_importer/processors.py
tags: [surface-import, spatial-linking, pipe-code]
participants: [engineer, ai-assistant]
---

# Surface-to-Node Linking: Spatial Only (No Code-Based Linking)

## Context

The BGT inlooptabel contains both pipe code columns (`leidingcode_gemengd`, etc.)
and enough spatial data to do nearest-pipe matching. The existing
`LinkSurfacesWithConnectionNodes` algorithm only does spatial matching. The
question was whether the new importer should also support code-based linking
(surface → pipe via matching code column → connection node).

## Options Considered

### Option 1: Spatial matching only
Buffer surface by search_distance, find nearest pipe of matching sewerage_type,
pick nearest of pipe's two connection nodes.
- ✅ Consistent with existing algorithm
- ✅ Works for any polygon source (not BGT-specific)
- ✅ Simple, well-understood
- ❌ Does not exploit pipe code columns in BGT data

### Option 2: Spatial + code-based linking
User chooses between spatial matching or linking via a pipe code column in the
source data.
- ✅ More precise for BGT data where pipe codes are available
- ❌ More complex UI and implementation
- ❌ Code-based linking only works for BGT-like sources

### Option 3: Code-first with spatial fallback
Use code column if present, fall back to spatial.
- ✅ Best accuracy when codes are available
- ❌ Complex fallback logic, harder to reason about results

## Decision

We chose **Option 1** (spatial only). The existing spatial logic from
`LinkSurfacesWithConnectionNodes` is reused. Code-based linking can be added as a
future enhancement if users need it.

## Consequences

### Positive
- ✅ Simple, consistent with existing algorithm
- ✅ Generic — works for any polygon source

### Negative
- ⚠️ BGT pipe code columns (`leidingcode_*`) are ignored for now

### Neutral
- `leidingcode_*` columns can still be mapped via Field Map if users want them
  on the Surface feature, but they won't drive the linking logic

## Code References

- Existing spatial linking: `processing/alghorithms_inflow.py:LinkSurfacesWithConnectionNodes.processAlgorithm`
