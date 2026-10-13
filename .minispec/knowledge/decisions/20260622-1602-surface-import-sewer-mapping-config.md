---
type: decision
id: 20260622-1602-surface-import-sewer-mapping-config
date: 2026-06-22
status: accepted
supersedes: null
superseded_by: null
impacts:
  - threedi_schematisation_editor/vector_data_importer/settings_models.py
  - threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py
tags: [surface-import, sewer-mapping, settings]
participants: [engineer, ai-assistant]
---

# Sewer Type Mapping: Table of 11 Rows with Percentage Column Per Type

## Context

The surface import needs to know, for each sewer type, which source column holds
the runoff percentage. The BGT inlooptabel has 5 such columns; the schematisation
has 11 `SewerageType` enum values. The mapping must be configurable and saveable.

Several UX approaches were considered for how to express this configuration.

## Options Considered

### Option 1: Sewer type mapping table (11 rows, column per type)
UI table with one row per SewerageType. Each row has a label and a combobox for
the source column. Blank = skip that type.
- ✅ Explicit, clear — user sees all types at once
- ✅ Maps directly to SewerageType enum, no ambiguity
- ✅ Easily serializable as list of {sewerage_type, percentage_column}
- ❌ 11 rows may feel verbose for simple cases

### Option 2: Dynamic add/remove rows
User adds only the sewer types they need.
- ✅ Cleaner for simple cases
- ❌ More complex UI; user must know to add rows
- ❌ Harder to see what's missing

### Option 3: Reuse FieldMapConfig per sewer type
Each sewer type gets a full FieldMapConfig row with method/attribute/expression.
- ✅ Maximum flexibility (expression per type)
- ❌ Significantly more complex UI for a simple mapping need

## Decision

We chose **Option 1**: a fixed table of 11 rows, one per SewerageType enum value.
Each row has a read-only type label and a combobox for the source column (blank =
skip). A per-type filter expression column was considered but deferred.

Serialized as `sewer_type_mappings: list[{sewerage_type: int, percentage_column: str|null}]`
in `SurfaceSettings`.

## Consequences

### Positive
- ✅ Simple to implement, simple to understand
- ✅ Directly corresponds to SewerageType enum — no translation layer
- ✅ BGT preset fills 4–5 rows; other rows stay blank

### Negative
- ⚠️ 11-row table is slightly verbose; can be improved with scroll/collapse later

### Neutral
- Per-sewer-type filter expressions are explicitly deferred to a future iteration

## Related Decisions
- 20260622-1600-surface-import-architecture.md
