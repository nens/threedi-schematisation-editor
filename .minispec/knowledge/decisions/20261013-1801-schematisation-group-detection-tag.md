# Decision: Tag-based schematisation group discovery

**Date:** 2026-10-13
**Status:** Accepted

## Context

`_find_schematisation_groups()` currently identifies roots by the
`Rana schematisation:` name prefix. It feeds `model_layers_map` and
`switch_workspace_context()`, which activate the correct schematisation when
a user selects one of its layers. An explicit group name may omit that prefix.

## Decision

Set `threedi_schematisation_editor/is_model_group` on created main groups.
Update group discovery to match either this marker or the legacy name prefix.

## Reasoning

The marker allows custom display names without losing workspace switching.
Retaining the prefix check preserves discovery for existing projects and
groups without the new property.

## Consequences

Group creation adds one custom property and group discovery checks it in
addition to the existing prefix. No existing group needs migration.

## Related Decisions

- `20261013-1800-schematisation-group-name-override.md`
