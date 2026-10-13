# Source filter consolidation

## Overview

Consolidate all source-layer filtering (layer selection, selected features, expression-based filtering) into the Start page via `LayerSettingsWidget`. Remove the surface-specific filter from `SurfaceSettingsWidget`. Make these settings part of the serializable import config via a new `SourceSettings` pydantic model.

## Motivation

Currently, filtering is split across two locations:
- **Start page**: layer combo + "selected features only" checkbox
- **Surface Settings page** (surface wizard only): a threshold-based filter with method/attribute/expression/threshold

This is inconsistent — the surface wizard has filtering capabilities that other importers lack, and it's confusing that you configure *what* to import across two separate pages. A single expression-based filter on the Start page is simpler, more powerful, and works for all importers.

## Design

### New model: `SourceSettings`

In `settings_models.py`:

```python
class SourceSettings(BaseModel):
    name: ClassVar[str] = "source"
    selected_layer_name: str = ""
    use_selected_features: bool = False
    filter_expression: Optional[str] = None
```

Added to `ImportSettings` as `source: SourceSettings = SourceSettings()`.

`GenericSettingsModel` in `wizard/models.py` is **deleted** — `SourceSettings` replaces it entirely. The field mapping is:

| `GenericSettingsModel` | `SourceSettings` |
|---|---|
| `selected_layer: str` | `selected_layer_name: str` |
| `use_selected_features: bool` | `use_selected_features: bool` |
| *(didn't exist)* | `filter_expression: Optional[str]` |

### Updated widget: `LayerSettingsWidget`

In `wizard/settings_widgets.py`:

- Gains a `QgsFieldExpressionWidget` below the "Selected features only" checkbox
- Updates its field list when the layer changes (via `layerChanged` signal → `setLayer()` on the expression widget)
- Writes state to a `SourceSettings` instance (replaces `GenericSettingsModel`)
- Exposes `get_settings() -> SourceSettings` and `deserialize(data: dict)` for round-tripping with the JSON config

### Updated: Start page serialization

The `StartPage` participates in the wizard's `serialize()`/`deserialize()` flow:
- `get_settings()` returns `{"source": layer_settings_widget.get_settings()}`
- `deserialize(data)` pre-selects the source layer by name, restores checkbox, and sets expression

### Updated: `VDIWizard.run_import()`

Computes `selected_feat_ids` from the three inputs:

| `use_selected_features` | `filter_expression` | Result |
|---|---|---|
| False | None | `selected_feat_ids = None` (all features) |
| True | None | `selected_feat_ids = layer.selectedFeatureIds()` |
| False | set | Evaluate expression on all features → list of matching IDs |
| True | set | Evaluate expression on selected features only → list of matching IDs |

Expression evaluation uses `QgsExpression` + `QgsExpressionContext` with the source layer, iterating features and keeping those where the expression evaluates to truthy.

### Updated: Processing algorithms

`BaseImporter.processAlgorithm()` reads `import_config.source.filter_expression`. If set, evaluates the expression on the source layer and passes matching feature IDs as `selected_ids` to `import_features()`.

### Removed

| What | Where |
|---|---|
| `SurfaceFilterSettings` | `settings_models.py` |
| `SurfaceSettings.filter` field | `settings_models.py` |
| Filter section (field map widget + threshold) | `SurfaceSettingsWidget.setup_ui()` |
| `SurfaceImporter.filter_features()` static method | `importers.py` |
| `SurfaceImporter.get_input_feature_ids()` override | `importers.py` |
| `GenericSettingsModel` | `wizard/models.py` (entire file deleted) |

### JSON config: new format

```json
{
    "source": {
        "selected_layer_name": "5_BGT_oppervlakken",
        "use_selected_features": false,
        "filter_expression": "\"maaiveld\" + \"open_water\" < 100"
    },
    "surface": {
        "sewer_type_mappings": [...],
        "linking": {...}
    },
    "fields": {...}
}
```

### Backward compatibility

Old JSON configs with `"surface": {"filter": {...}}` will load without error (pydantic ignores extra fields by default) but the filter will not be applied. Users need to move their expression to `"source": {"filter_expression": "..."}`. This is acceptable since the surface import feature is unreleased.

## Affected files

- `settings_models.py` — add `SourceSettings`, remove `SurfaceFilterSettings`, update `SurfaceSettings`
- `wizard/settings_widgets.py` — update `LayerSettingsWidget`, remove filter section from `SurfaceSettingsWidget`
- `wizard/models.py` — **deleted** (only contained `GenericSettingsModel`)
- `wizard/pages.py` — `StartPage` gains `get_settings()`/`deserialize()`
- `wizard/wizard.py` — `run_import()` evaluates expression, updated serialization flow
- `importers.py` — remove `SurfaceImporter.filter_features()` and `get_input_feature_ids()` override
- `processing/algorithms_vector_data_importer.py` — read and apply `filter_expression`
- `tests/` — update affected tests

## Open questions

- None
