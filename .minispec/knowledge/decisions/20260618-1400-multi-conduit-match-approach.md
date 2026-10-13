# Decision: Multi-Conduit Match Handling Approach

**Date**: 2026-06-18
**Status**: Accepted
**Feature**: margriet_408_handle_multi_conduit_match

## Context

When importing structures via the Vector Data Importer, a source structure
(point or line) can be within snapping distance of multiple conduits (channels
or pipes). The current code silently integrates the structure into every
matching conduit, producing duplicates.

## Decision

### Behavior: Warn and skip entirely

When a structure matches multiple conduits, skip it from all conduits and emit
a warning. This was chosen over "use first match" or "use closest match" because
the ambiguity means the user needs to resolve it (e.g. by reducing snapping
distance or moving the structure).

### Approach: Pre-scan with exclusion set

A pre-scan method (`find_ambiguous_structures`) runs before the main integration
loop. It reuses the existing snapping-check methods to identify structures
matching multiple conduits, then passes an exclusion set to
`get_conduit_structures_data`.

**Rejected alternative**: Full restructure (collect all matches first, iterate
conduit->structures map). This was the WIP branch approach. Rejected because it
requires significant refactoring of the integration loop, introduces QgsFeature-
as-dict-key issues, and changes more code than necessary.

**Rejected alternative**: Single-pass with `all_processed_structure_ids` fed
back. Cannot satisfy "skip entirely" -- the first conduit doesn't know the
structure will match another conduit later.

### Scope: Both integrators

Implemented in `LinearIntegrator` base class so both `ChannelIntegrator` and
`PipeIntegrator` benefit. The problem exists in both.

### Warning format: One batched warning

A single `StructuresIntegratorWarning` lists all skipped structures and their
matching conduit IDs. Chosen over per-structure warnings for cleaner output.

### Snapping check in pre-scan: Reuse existing methods

The pre-scan calls `get_conduit_structure_from_point`/`_from_line` and checks
for non-None return. This means the snapping check runs twice per structure
(once in pre-scan, once in integration). Accepted because:
- Buffer+intersect is the dominant cost regardless.
- Extra `lineLocatePoint` and field lookups are trivial.
- Caching or a dedicated lighter method would add complexity for marginal gain.

## Consequences

- Structures near conduit intersections will be skipped with a clear warning.
- Users must resolve ambiguity (adjust snapping distance or move structures).
- No changes to the integration logic itself, only an additional filtering step.
