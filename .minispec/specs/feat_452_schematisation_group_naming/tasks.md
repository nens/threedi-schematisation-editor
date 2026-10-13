---
feature: feat_452_schematisation_group_naming
status: draft
created: 2026-10-13
chunk_size: adaptive
total_tasks: 5
estimated_lines: 160
---

# Schematisation Group Name Override Tasks

## Overview

Implements `.minispec/specs/feat_452_schematisation_group_naming/design.md`.
Tasks are ordered to establish the optional naming API, preserve discovery and
reload behavior, and then verify direct-editor compatibility. Keep the changes
minimal and close to existing code, as required by the editor's stability
principle.

## Task List

### Core Implementation

#### Task 1: Add the optional display-name override
- **Estimate:** ~30 lines
- **Files:** `threedi_schematisation_editor/user_layer_manager.py`
- **Description:** Add optional `group_name=None` to `LayersManager.__init__`.
  Make `detailed_model_name` and `main_group` return the override verbatim
  when present, with no prefix on `main_group`; preserve existing behavior
  when omitted.
- **Depends on:** None
- **Acceptance:** Both naming properties use the explicit name when supplied
  and preserve their current values/behavior when it is absent.
- **Evidence:** Focused tests for explicit and absent overrides.
- [x] Task 1: Add the optional display-name override

#### Task 2: Expose the override through `load_schematisation()` and UI message
- **Estimate:** ~15 lines
- **Files:** `threedi_schematisation_editor/__init__.py`
- **Description:** Add optional `group_name=None` to
  `ThreediSchematisationEditorPlugin.load_schematisation()` and pass it into
  `LayersManager`. Use `lm.detailed_model_name` for the loaded status message
  when an override is supplied; preserve the current `lm.model_name` message
  when there is no override.
- **Depends on:** Task 1
- **Acceptance:** The plugin entry point passes the supplied name through;
  direct calls that omit it remain compatible.
- **Evidence:** Focused test or manual Python-console call with and without
  `group_name`.
- [x] Task 2: Expose the override through `load_schematisation()` and UI message

#### Task 3: Preserve group discovery and workspace switching
- **Estimate:** ~20 lines
- **Files:** `threedi_schematisation_editor/user_layer_manager.py`,
  `threedi_schematisation_editor/__init__.py`
- **Description:** Mark the main group as a schematisation group when it is
  created. Update `_find_schematisation_groups()` to recognize that marker
  while retaining the existing name-prefix fallback for old projects.
- **Depends on:** Task 1
- **Acceptance:** Both explicitly named groups and existing prefixed groups
  are detected for workspace-context switching.
- **Evidence:** Focused test of group discovery; manual click on layers in
  both group types confirms context switching.
- [x] Task 3: Preserve group discovery and workspace switching

#### Task 4: Persist and use stable group identity
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/user_layer_manager.py`
- **Description:** Persist the normalized model GeoPackage path on the main
  group and persist the display override when present. Add a recursive lookup
  by that identity and use it for registration and removal before falling
  back to the existing name lookup. Remove the located node directly rather
  than passing its possibly overridden name to the existing name-only removal
  helper. During registration, restore any saved display override to the new
  manager instance.
- **Depends on:** Tasks 1-3
- **Acceptance:** An overridden group is registered and removable after a
  project reload; groups without the new properties still use the legacy
  name-based path.
- **Evidence:** Focused tests for property lookup and fallback; manual
  save/reopen test verifies forms/snapping and removal.
- [x] Task 4: Persist and use stable group identity

### Integration & Verification

#### Task 5: Regression pass
- **Estimate:** ~15 lines (verification, minimal code)
- **Files:** No files expected; add or adjust focused tests if needed.
- **Description:** Run the design's manual test paths and the relevant
  schematisation editor tests. Confirm direct loading, explicit naming,
  context switching, reload, removal, and legacy group compatibility.
- **Depends on:** Tasks 1-4
- **Acceptance:** All manual paths pass and the relevant automated tests pass.
- **Evidence:** Focused pytest command output and manual test notes; full test
  suite via `docker compose run --rm qgis-desktop make test` when practical.
- [ ] Task 5: Complete manual QGIS load, context-switch, project-reopen, and removal checks
- Automated focused tests pass. QGIS GUI/manual load, context-switch, and
  project-reopen checks remain to be performed.
