# Strategy Pattern via Composition for Structure Integration

**Date:** 2026-07-06
**Feature:** pump-importer

## Context

Adding Pump import requires integrating point-geometry structures onto conduits
(channels, pipes). The existing `LinearIntegrator` handles only line-geometry
structures. The axis of variation is **structure geometry type** (line vs point),
not conduit type (both PipeIntegrator and ChannelIntegrator need to handle both).

## Decision

Use composition: inject a `StructurePlacementStrategy` into `LinearIntegrator`.
Two implementations:
- `LineStructurePlacement` — encapsulates existing line structure behaviour
- `PointStructurePlacement` — new, handles point structures (Pump)

## Alternatives Considered

1. **Subclass override** — rejected: creates combinatorial explosion
   (`PipePointIntegrator`, `PipeLineIntegrator`, `ChannelPointIntegrator`, …)
2. **Separate class hierarchy** — rejected: conduit logic (matching, cutting,
   node management) is identical and should be shared
3. **Geometry-type flag on data class** — rejected: mixes data and behaviour,
   doesn't cleanly separate the placement differences

## Consequences

- Refactoring existing `integrate_structure_features` to delegate to strategy
- Clean extension point for any future structure geometry types
- Slightly more indirection, consistent with project's composition style
- Existing line-structure behaviour is preserved; tests should remain green
  after the refactor
