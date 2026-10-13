---
feature: feat_282_generic_vdi
status: complete
created: 2026-07-22
topic: wizard
---

# Generic Importer Wizard Design

## Overview

A 3-page wizard (`ImportGenericWizard`) for the generic importer. Unlike all other
wizards where the target layer is fixed at construction time, here the user picks
both source and target layer on page 1. The field map page (page 2) rebuilds its
rows whenever the target selection changes. Draft save/restore is fully supported,
keyed by wizard class name.

## Pages

1. **GenericStartPage** — dual layer selection with mutual geometry-type filtering
2. **FieldMapPage** (existing, with new `rebuild` method) — field mapping for the
   selected target model
3. **RunPage** (existing, unchanged) — progress, log, cancel

## Components

### `SchematisationLayerProxyModel(QgsMapLayerProxyModel)` — `wizard.py`

Filters `QgsMapLayerComboBox` to show only layers that come from the target gpkg
**and** whose name is a tablename in `dm.ALL_MODELS`.

```python
class SchematisationLayerProxyModel(QgsMapLayerProxyModel):
    def __init__(self, model_gpkg, parent=None):
        super().__init__(parent)
        self._model_gpkg = model_gpkg
        self._tablenames = {cls.__tablename__ for cls in dm.ALL_MODELS if cls.__tablename__}

    def filterAcceptsRow(self, source_row, source_parent):
        if not super().filterAcceptsRow(source_row, source_parent):
            return False
        layer = ...  # retrieve layer from source model
        source = layer.source()
        return self._model_gpkg in source and layer.name() in self._tablenames
```

Geometry icons come for free because `QgsMapLayerComboBox` renders them natively.

### `GenericStartPage(QWizardPage)` — `pages.py`

Owns both selectors and all cross-filtering logic.

**Widgets:**
- Target selector: `QgsMapLayerComboBox` with `SchematisationLayerProxyModel`
  (no "selected features only", no expression filter — target is always fully loaded)
- Source selector: reuses existing `LayerSettingsWidget` (filter updated dynamically)

**Cross-filtering rules:**
- On target change → derive `QgsMapLayerProxyModel` filter from target geometry type:
  - target has geometry → source must match that geometry type
  - target has no geometry (`NullGeometry`) → source filter = `TypeVector` (all layers)
- On source change → update target filter to layers matching source geometry type,
  plus always include `NoGeometry` target layers

**Signals:**
- `target_layer_changed(model_cls)` — emitted when target selection changes; consumed
  by `ImportGenericWizard` to rebuild the field map page
- `layer_changed` — re-emitted from both selectors for `isComplete`

**`isComplete`:** both source and target must be selected.

**`get_settings`:** returns `{"source": ...}` from `LayerSettingsWidget` as usual;
target selection is communicated via `target_model_cls` property, not import settings.

**`deserialize`:**
1. Restore target layer selection → triggers `target_layer_changed` signal synchronously
   (which calls `field_map_page.rebuild(model_cls)` before page 2 deserialises)
2. Restore source layer selection via `LayerSettingsWidget.deserialize`

**Properties:**
- `selected_layer` — the selected source layer (from `LayerSettingsWidget`)
- `target_model_cls` — the `dm.ModelObject` subclass matching the selected target layer
  (looked up from `dm.ALL_MODELS` by tablename)

### `FieldMapPage.rebuild(model_cls)` — addition to `pages.py`

New public method on the existing `FieldMapPage`. Clears `row_dict`, recreates rows
for `model_cls`, and refreshes the `FieldMapWidget`. Called by `ImportGenericWizard`
when `target_layer_changed` fires.

```python
def rebuild(self, model_cls):
    self.row_dict = self.create_rows(model_cls) if model_cls else {}
    self.field_map_widget.set_rows(self.row_dict)  # clears and repopulates widget
    self.title_suffix = model_cls.__layername__.lower() + "s" if model_cls else ""
    self.completeChanged.emit()
```

`FieldMapWidget` needs a `set_rows` method (or `rebuild`) that clears the table and
repopulates it — this is a small addition to `field_map.py`.

### `ImportGenericWizard(VDIWizard)` — `wizard.py`

Subclasses `VDIWizard`. Overrides only what differs:

```python
class ImportGenericWizard(VDIWizard):
    def __init__(self, model_gpkg, layer_manager, parent=None):
        # model_cls=None; VDIWizard stores it but wizard_title and
        # field_map_page are overridden so it's never used directly
        super().__init__(None, model_gpkg, layer_manager, parent)

    @property
    def wizard_title(self):
        return "Generic import"

    @cached_property
    def start_page(self):
        page = GenericStartPage(self.model_gpkg)
        page.target_layer_changed.connect(self.field_map_page.rebuild)
        return page

    @cached_property
    def field_map_page(self):
        return FieldMapPage(model_cls=None, name="fields")

    @property
    def target_model_cls(self):
        return self.start_page.target_model_cls

    @property
    def selected_layer(self):
        return self.start_page.selected_layer

    def prepare_import(self):
        handler = self.layer_manager.model_handlers[self.target_model_cls]
        return [handler], {"target_layer": handler.layer}

    def get_importer(self, import_settings, layer_dict):
        return vdi_importers.GenericImporter(
            self.selected_layer,
            self.model_gpkg,
            import_settings,
            self.target_model_cls,
            **layer_dict,
        )
```

**Draft support:** `VDIWizard`'s existing draft mechanism keys on
`type(self).__name__` = `"ImportGenericWizard"`. `get_draft_settings()` and
`restore_draft_lenient()` iterate pages in order — `GenericStartPage.deserialize`
runs first, restoring the target (which synchronously fires `target_layer_changed`
and rebuilds field map rows), then `FieldMapPage.deserialize` runs with the correct
rows already in place. No overrides needed for draft support.

### Registration — `__init__.py` (plugin entry point)

`ImportGenericWizard` takes `(model_gpkg, layer_manager)` rather than
`(model_cls, model_gpkg, layer_manager)`. The existing `import_external` helper
passes `model_cls` as the first arg; a separate call path is needed:

```python
# In ThreediSchematisationEditorPlugin or wherever importers are triggered:
wizard = ImportGenericWizard(self.model_gpkg, self.layer_manager)
wizard.show()
```

This needs a new menu/toolbar action "Generic import..." separate from the
per-object-type import actions.

## Key Decisions

| # | Decision | Choice | Reason |
|---|----------|--------|--------|
| 1 | Target layer selector | `QgsMapLayerComboBox` + `SchematisationLayerProxyModel` | Geometry icons for free; gpkg + tablename filtering |
| 2 | Cross-filtering location | `GenericStartPage` | Self-contained; `StartPage` and `LayerSettingsWidget` unchanged |
| 3 | Wizard base class | Subclass `VDIWizard`, override `start_page` | Reuses threading, cancel, draft, progress logic |
| 4 | Field map update on target change | `FieldMapPage.rebuild(model_cls)` in place | Simpler than remove/re-add; page stays registered with wizard |
| 5 | Draft support | Full — deserialise target first (triggers rebuild), then field map | Works with existing page-order iteration in `restore_draft_lenient` |

## Files Changed

| File | Change |
|------|--------|
| `wizard/wizard.py` | Add `SchematisationLayerProxyModel`, `ImportGenericWizard` |
| `wizard/pages.py` | Add `GenericStartPage`; add `FieldMapPage.rebuild` |
| `wizard/field_map.py` | Add `FieldMapWidget.set_rows` (clears + repopulates table) |
| `wizard/__init__.py` | Export `ImportGenericWizard` |
| `__init__.py` (plugin) | Add "Generic import" action wired to `ImportGenericWizard` |

## Open Questions

- `FieldMapPage.__init__` currently crashes if `model_cls=None` (calls
  `model_cls.fields_display_names()`). Either guard it or pass a sentinel.
  Simplest: guard `create_rows` to return `{}` when `model_cls is None`.
- The `initializePage` on `FieldMapPage` calls `self.wizard().selected_layer.name()`
  — needs a guard when called before a target is selected.
