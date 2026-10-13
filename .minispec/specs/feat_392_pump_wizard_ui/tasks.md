---
feature: pump-wizard-ui
status: complete
created: 2026-07-17
chunk_size: medium
total_tasks: 4
estimated_lines: 155
---

# Pump Wizard UI Tasks

## Overview

Update `ImportPumpWizard` to reflect the backend changes from `feat_392_pump_map_import`:
restrict source layer selection to point layers, add `PumpLinkingSettingsWidget` and
`PointToLIneConversionSettingsWidget` to the settings page, always include `pump_map_layer`
in `prepare_import`, and clean up the wizard DESIGN.md.

## Task List

### Foundation

#### Task 1: `PumpLinkingSettingsWidget`
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:** Add `PumpLinkingSettingsWidget` — a `FieldMapSettingsWidget` subclass
  with a single `FieldMapRow` for `connection_node_id_end`. `group_name` = "Pump linking
  settings". No `should_show` override (always shown).
- **Depends on:** None
- **Acceptance:** Widget can be instantiated; `get_settings()` returns a
  `PumpLinkingSettings` instance with the configured `connection_node_id_end`.
- **Evidence:** Manual smoke test or unit test constructing the widget.

### Core Implementation

#### Task 2: Update `ImportPumpWizard`
- **Estimate:** ~30 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py`
- **Description:** Three changes in `ImportPumpWizard`:
  1. `layer_filter` → return `PointLayer` only (remove `LineLayer`).
  2. `settings_widgets_classes` → `[ConnectionNodeSettingsWidget,
     PumpLinkingSettingsWidget, PointToLIneConversionSettingsWidget,
     IntegrationSettingsWidget]`. Add the two missing imports.
  3. `prepare_import` → always add `pump_map_layer`; remove the
     `LineGeometry` guard (the `if geometryType == LineGeometry` block).
- **Depends on:** Task 1
- **Acceptance:** Wizard opens with a point-layer filter; settings page shows all four
  widget groups; `pump_map_layer` is always passed to the importer.
- **Evidence:** Existing wizard tests pass; manual walkthrough of the wizard shows the
  new settings groups.

### Integration & Polish

#### Task 3: Remove unused `should_show` infrastructure
- **Estimate:** ~25 lines removed
- **Files:**
  - `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
  - `threedi_schematisation_editor/vector_data_importer/wizard/pages.py`
- **Description:** With `PumpDirectionSettingsWidget` gone, no widget overrides
  `should_show` anymore. Remove:
  - `SettingsWidget.should_show()` default method (`settings_widgets.py`)
  - The `should_show` call and `group_box.setVisible(...)` line in
    `SettingsPage.initializePage()` (`pages.py`)
  
  Verify by searching the codebase for any remaining `should_show` overrides before
  deleting. `update_layer` is still used by multiple widgets — leave it untouched.
- **Depends on:** Task 2
- **Acceptance:** No `should_show` references remain in the codebase; all settings
  group boxes remain visible (they were always shown by the default implementation).
- **Evidence:** `grep should_show` returns no results; existing tests pass.

#### Task 4: Update `wizard/DESIGN.md`
- **Estimate:** ~15 lines changed
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/DESIGN.md`
- **Description:** Remove the entry for `PumpDirectionSettingsWidget` and its
  `should_show` override. Remove the documentation of `should_show` from the
  `SettingsWidget` class diagram and prose (it no longer exists). Add an entry for
  `PumpLinkingSettingsWidget` describing its one field row. Update the
  `ImportPumpWizard` `settings_widgets_classes` list in the doc.
- **Depends on:** Task 3
- **Acceptance:** Doc accurately reflects the current wizard state; no mention of
  removed classes or methods.
- **Evidence:** Doc review.

## Notes

- `IntegrationSettingsWidget.update_layer` hides `min_length` for point sources — no
  change needed; it will simply always hide `min_length` in the pump wizard now.
- `PointToLIneConversionSettingsWidget` already exists; it only needs to be added to
  `settings_widgets_classes`, not created.
- A `pump_map_fields` field map page is out of scope for this feature.

## Progress
- [x] Task 1: `PumpLinkingSettingsWidget`
- [x] Task 2: Update `ImportPumpWizard`
- [x] Task 3: Remove unused `should_show` infrastructure
- [x] Task 4: Update `wizard/DESIGN.md`
