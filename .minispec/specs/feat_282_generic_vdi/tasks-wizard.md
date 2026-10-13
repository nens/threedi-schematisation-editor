---
feature: feat_282_generic_vdi
status: complete
created: 2026-07-22
chunk_size: medium
total_tasks: 5
estimated_lines: 270
---

# Generic Importer Wizard Tasks

## Overview
3-page wizard for the generic importer: dual layer selection with cross-filtering
(page 1), field map (page 2), run (page 3).

## Task List

### Foundation

#### Task 1: FieldMapWidget.set_rows + FieldMapPage null guard + rebuild
- **Estimate:** ~60 lines
- **Files:** `wizard/field_map.py`, `wizard/pages.py`
- **Description:** Add `FieldMapWidget.set_rows(row_dict)` to replace rows in place.
  Guard `FieldMapPage.create_rows` and `initializePage` for `model_cls=None`.
  Add `FieldMapPage.rebuild(model_cls)`.
- **Depends on:** None
- **Evidence:** Importable without error; `FieldMapPage(model_cls=None, name="fields")` does not crash

#### Task 2: SchematisationLayerProxyModel
- **Estimate:** ~40 lines
- **Files:** `wizard/wizard.py`
- **Description:** `QgsMapLayerProxyModel` subclass filtering to layers whose source
  contains `model_gpkg` and whose name is in `dm.ALL_MODELS` tablenames.
- **Depends on:** None (parallel with Task 1)
- **Evidence:** Importable without error

### Core Implementation

#### Task 3: GenericStartPage
- **Estimate:** ~90 lines
- **Files:** `wizard/pages.py`
- **Description:** Dual-selector page. Target: `QgsMapLayerComboBox` +
  `SchematisationLayerProxyModel`. Source: `LayerSettingsWidget`. Cross-filtering
  on both selectors. Signals, `isComplete`, `get_settings`, `deserialize`,
  `target_model_cls` property.
- **Depends on:** Task 2
- **Evidence:** Importable without error

#### Task 4: ImportGenericWizard
- **Estimate:** ~60 lines
- **Files:** `wizard/wizard.py`
- **Description:** Subclasses `VDIWizard(model_cls=None)`. Overrides `start_page`,
  `field_map_page`, `wizard_title`, `prepare_import`, `get_importer`. Wires
  `target_layer_changed` → `field_map_page.rebuild`.
- **Depends on:** Tasks 1, 3
- **Evidence:** Importable without error

### Integration

#### Task 5: Registration
- **Estimate:** ~20 lines
- **Files:** `wizard/__init__.py`, `__init__.py` (plugin)
- **Description:** Export `ImportGenericWizard`. Add `import_external_generic`
  method and menu entry to plugin.
- **Depends on:** Task 4
- **Evidence:** Menu entry appears; wizard opens without error

## Notes
- No automated tests: UI/QGIS widget code; consistent with existing wizard test approach
- Draft support works via existing page-order iteration in `restore_draft_lenient`

## Progress
- [x] Task 1: FieldMapWidget.set_rows + FieldMapPage null guard + rebuild
- [x] Task 2: SchematisationLayerProxyModel
- [x] Task 3: GenericStartPage
- [x] Task 4: ImportGenericWizard
- [x] Task 5: Registration
