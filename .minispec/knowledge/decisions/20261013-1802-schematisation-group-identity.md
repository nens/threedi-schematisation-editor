# Decision: Stable schematisation group identity across reloads

**Date:** 2026-10-13
**Status:** Accepted

## Context

`register_groups()` and `remove_groups()` locate the main group by its
recomputed name. With an explicit display-name override, project reload creates
a new manager without the original call argument, so name matching alone
cannot reliably find the persisted group or restore the override.

## Decision

Persist the normalized model GeoPackage path as
`threedi_schematisation_editor/model_gpkg_path` on the main group. Persist
`threedi_schematisation_editor/display_name_override` when an override exists.
Use the model path to locate the group for registration and removal, falling
back to the current name lookup when the property is absent. Registration
restores the display override when present. Removal deletes the located group
node directly rather than relying on its display name.

## Reasoning

The GeoPackage path is already the editor's stable schematisation identity in
`WorkspaceContextManager` and survives project save/reload. Property-based
lookup lets the display string change independently while name fallback keeps
older projects compatible.

## Consequences

The editor needs a recursive layer-tree lookup by model path and custom
properties on the main group. Existing projects without the properties retain
their current name-based registration and removal behavior.

## Related Decisions

- `20261013-1800-schematisation-group-name-override.md`
- `20261013-1801-schematisation-group-detection-tag.md`
