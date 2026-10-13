---
feature: feat_452_schematisation_group_naming
status: draft
created: 2026-10-13
decisions:
  - 20261013-1800-schematisation-group-name-override
  - 20261013-1801-schematisation-group-detection-tag
  - 20261013-1802-schematisation-group-identity
---

# Schematisation Group Name Override

## Overview

Allow an embedding plugin to pass an explicit display name when loading a
schematisation. The supplied name is used verbatim for the main layer-tree
group, the editor's active-schematisation dropdown, and the loaded message.
Calls that omit the new optional argument retain the editor's current
guess-based naming behavior, including the existing loaded-message text.

The override must not disable workspace-context switching or prevent
schematisations from being registered and removed after a project reload.
Persisting group identity and the optional display-name override on the layer
tree group supports those existing workflows.

## User Stories

- As a plugin integrating the schematisation editor, I want to pass the
  schematisation's canonical display name so its layer group and editor UI
  agree with the name shown by the host plugin.
- As a direct user of the schematisation editor, I want loading without an
  explicit name to keep its existing naming behavior.
- As a user reopening a QGIS project, I want overridden schematisations to
  retain their name and editor behavior, including workspace switching,
  editing configuration, and removal.

## Components

### `LayersManager` (`user_layer_manager.py`)

- Accept optional `group_name=None` in `__init__` and store it as the display
  name override.
- When the override is set, `detailed_model_name` and `main_group` return it
  verbatim. `main_group` does not prepend `Rana schematisation:` in this
  case. With no override, both properties retain the existing behavior.
- When creating the main group, persist its normalized model GeoPackage path
  as its stable identity, mark it as a schematisation group, and persist the
  override when one was supplied.
- On project reload, find the main group by its persisted model path before
  falling back to the existing name-based lookup. Restore any persisted
  display-name override into the new manager instance.
- Use the same identity lookup when removing a group; remove the located group
  node directly, retaining name lookup for groups created before this change.

### `ThreediSchematisationEditorPlugin` (`__init__.py`)

- Extend `load_schematisation()` with optional `group_name=None` and pass it
  to `LayersManager`.
- `_find_schematisation_groups()` recognizes the explicit group marker or
  the existing `Rana schematisation:` name prefix. The prefix fallback keeps
  older saved projects working; the marker allows custom-named groups to be
  found for workspace-context switching.
- Use the manager's detailed display name in the loaded status message when
  an override is supplied; otherwise retain the existing `model_name` message.

## Data Model

Store custom properties on the main `QgsLayerTreeGroup`:

- `threedi_schematisation_editor/model_gpkg_path`: normalized GeoPackage
  path used as stable group identity.
- `threedi_schematisation_editor/is_model_group`: marker used to discover
  schematisation root groups independent of their display name.
- `threedi_schematisation_editor/display_name_override`: explicit display
  name, present only when one was supplied.

These properties are persisted by QGIS with the project. Existing groups
without these properties continue to use the name-based compatibility paths.

## API/Interface

```python
def load_schematisation(
    self, model_gpkg=None, parents: list[str] | None = None,
    group_name: str | None = None,
):
    """Load a schematisation, optionally using an explicit group display name."""
```

`group_name` is optional and appended to the existing call interface so
standalone callers need no changes.

## Error Handling

No new error paths are expected. An omitted or `None` `group_name` selects
the existing behavior. The path identity is normalized consistently with
`LayersManager.model_gpkg_path` before it is persisted and compared.

## Scope Boundaries

- Does not change parent-group construction or persist the parent path; that
  is a pre-existing limitation and unrelated to the explicit leaf name.
- Does not change direct editor use when no override is supplied.
- Does not remove legacy name-prefix/name-match fallbacks for existing
  projects.
- Does not introduce Rana-specific layer-tree properties; the properties
  belong to the schematisation editor and represent editor-level group
  identity and type.

## Manual Testing Paths

- **Standalone load:** Load a schematisation directly without `group_name`;
  confirm the group name, dropdown label, and loaded message remain as before.
- **Explicit name:** Call `load_schematisation()` with a plain display name;
  confirm the group, dropdown, and loaded message show that exact name without
  the `Rana schematisation:` prefix.
- **Context switching:** With an explicitly named group loaded, click its
  layers and confirm the active editor context switches as it does for a
  normally named group.
- **Project reload:** Save and reopen a project containing an explicitly
  named schematisation; confirm its name, active context, edit forms/snapping,
  and layer registration are restored.
- **Removal:** Remove an explicitly named schematisation through the editor;
  confirm its group and layers are removed.
- **Compatibility:** Reopen a project containing a group created before this
  change; confirm name-based registration and removal continue to work.

## Open Questions

- None outstanding. The host will provide the plain item name without a WIP
  or revision suffix.
