# Point Structure Placement on Conduit

**Date:** 2026-07-06
**Feature:** pump-importer

## Context

`dm.Pump` has POINT geometry and a single `connection_node_id`. When a pump is
integrated onto a conduit it should be placed at its projected position and the
conduit should be split at that point.

## Decision

- **Pump geometry** = point at interpolated position on conduit (`conduit_geom.interpolate(m)`)
- **Conduit cut** at a single point (length=0) → two segments sharing a node
- **`LinearIntegratorStructureData`** reused with `length=0` (no new data class)
- **`fix_structure_placement`** still applies: prevents too-small conduit segments
  when multiple pumps are placed on the same conduit
- Pump shares its `connection_node_id` with the adjacent conduit endpoints

## Alternatives Considered

- **`PointIntegratorStructureData` subclass** — rejected: length=0 is sufficient;
  `get_conduit_cuts` and `fix_structure_placement` both work correctly with it
- **Pump occupies a configurable length (like line structures)** — rejected: pump
  is physically a point; zero-length is the correct model

## Consequences

- `get_conduit_cuts` works correctly with length=0 (two adjacent segments)
- `fix_structure_placement` shifts pump positions along the conduit to maintain
  `minimum_conduit_length` spacing — this is the desired behaviour
- Implementation note: verify `fix_structure_placement_rhs` edge case with length=0
  at right end of conduit
