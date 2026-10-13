# Feature: Replace attribute_match_col with attribute_match_target_config

**Feature Branch**: `20260714-145809-change-surface-importer`  
**Created**: 2026-07-14  
**Status**: Complete

## Overview

Replace the plain string `attribute_match_col` in `SurfaceLinkingSettings` with a `FieldMapConfig` (`attribute_match_target_config`) that supports ATTRIBUTE and EXPRESSION methods. This makes the target side consistent with the source side (`attribute_match_input_config`) and mirrors the `CrossSectionLocationSettings` pattern.

## Key Decisions

1. **`attribute_match_table` stays** — user still selects pipe or connection_node as the target table.
2. **Allowed methods**: ATTRIBUTE and EXPRESSION only (no AUTO).
3. **Shared utility**: Extract `channel_mapping` logic from `CrossSectionLocationProcessor` into a reusable function in the processors module utils (e.g., `build_feature_mapping(layer, field_config_dict)`).
4. **Dynamic label**: The target FieldMapWidget row label reflects the selected table ("Match field in pipe" / "Match field in connection_node").
5. **No backward compatibility** for saved config JSON files.

## Components & Changes

### 1. `settings_models.py`

- Remove: `attribute_match_col: Optional[str] = None`
- Add: `attribute_match_target_config: Optional[FieldMapConfig] = None`

### 2. `processors.py` — shared utility

Extract from `CrossSectionLocationProcessor.channel_mapping`:

```python
def build_feature_mapping(layer, field_config_dict):
    """Build {value: feature} mapping from a layer using a FieldMapConfig dict.
    
    Supports ATTRIBUTE and EXPRESSION methods.
    Returns empty dict on invalid/missing config.
    """
    if not field_config_dict:
        return {}
    method = field_config_dict.get("method")
    if method == ColumnImportMethod.ATTRIBUTE.value:
        col = field_config_dict.get(ColumnImportMethod.ATTRIBUTE.value)
        if col:
            return {f[col]: f for f in layer.getFeatures()}
    elif method == ColumnImportMethod.EXPRESSION.value:
        expression_str = field_config_dict.get(ColumnImportMethod.EXPRESSION.value)
        expression = QgsExpression(expression_str)
        if expression.isValid():
            context = QgsExpressionContext()
            mapping = {}
            for feature in layer.getFeatures():
                context.setFeature(feature)
                mapping[expression.evaluate(context)] = feature
            return mapping
    return {}
```

### 3. `processors.py` — CrossSectionLocationProcessor

Refactor `channel_mapping` to use `build_feature_mapping(self.channel_layer, self.join_field_tgt)`.

### 4. `processors.py` — SurfaceProcessor.get_attribute_match

Replace iteration with column lookup:
- Build mapping using `build_feature_mapping(node_layer_or_pipe_layer, linking.attribute_match_target_config)`
- Look up `input_val` in the mapping
- For pipes: still filter by sewerage_type if applicable

### 5. `settings_widgets.py`

- Replace `match_table_col` QComboBox with a `FieldMapWidget` for the target config.
- Use `set_fixed_source_attributes_from_data_model` with `dm.Pipe` or `dm.ConnectionNode` based on table selection.
- Update the row label dynamically when table radio changes (e.g., "Match field in pipe" / "Match field in connection_node").
- Update `_update_model`, `_on_match_table_changed`, `deserialize`, `is_valid` accordingly.

### 6. Tests & config files

- Update `test_processors_surface.py`: replace `attribute_match_col="code"` with `attribute_match_target_config=FieldMapConfig(method="attribute", attribute="code")`.
- Update JSON config fixtures (`import_surfaces_long.json`, `import_surfaces_wide.json`).
- Update `generate_surface_refs.py`.

## Open Questions

- Where exactly to place `build_feature_mapping` — top of `processors.py` or in a separate utils module within `vector_data_importer/`? (Leaning toward keeping it in `processors.py` near existing logic, unless there's a better home.)
