# Decision: Optional schematisation group display-name override

**Date:** 2026-10-13
**Status:** Accepted

## Context

An embedding plugin needs to provide the canonical name for a schematisation's
main group and for the editor's own active-schematisation dropdown. The current
editor guesses a name from the GeoPackage path and revision-folder layout.
Direct use of the editor without a supplied name must retain current behavior.

## Decision

Add optional `group_name=None` parameters to `LayersManager` and
`load_schematisation()`. When supplied, use the name verbatim for
`detailed_model_name` and `main_group` (without the `Rana schematisation:`
prefix) and use the detailed name in the loaded status message. When omitted,
retain the existing guess-based name, prefix, and loaded status message.

## Reasoning

This lets the host plugin supply its canonical plain item name while leaving
standalone editor use unchanged. One shared override keeps the layer panel,
toolbar dropdown, and load message consistent; renaming the tree group after
the editor loads it would not.

## Consequences

Custom-named groups cannot be identified by the legacy name prefix alone.
The companion decisions below specify additive group marking and stable
identity metadata so workspace switching and project reload continue to work.

## Related Decisions

- `20261013-1801-schematisation-group-detection-tag.md`
- `20261013-1802-schematisation-group-identity.md`
