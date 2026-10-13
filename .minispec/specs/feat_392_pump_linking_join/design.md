---
feature: feat_392_pump_linking_join
status: complete
created: 2026-07-20
branch: feat_392_pump_import
---

# PumpLinkingSettings: Source/Target Join Fields

## Overview

Replace the single `connection_node_id_end` field in `PumpLinkingSettings` with a
`join_field_src` / `join_field_tgt` pair (matching the `CrossSectionLocationSettings`
pattern), plus an `enabled` bool to toggle the mapping on/off. Users can now join
on arbitrary attributes of the connection node table (e.g. `code`, a custom identifier)
rather than being locked to matching by feature ID.

## Problem

Users currently can only map a source column to the connection node's feature ID.
They need to join on arbitrary attributes of the connection node table.

## User Story

As a user importing pump data, I want to choose which attribute of my source layer
maps to which attribute of the connection node layer, so that I can link pumps to
connection nodes even when my source data does not contain connection node IDs.

## Changes

### 1. Settings Model — `settings_models.py` (lines 273–285)

Replace `PumpLinkingSettings`:

```python
class PumpLinkingSettings(BaseModel):
    metadata: ClassVar[FieldMapMetadata] = FieldMapMetadata(
        allowed_methods=[
            ColumnImportMethod.ATTRIBUTE,
            ColumnImportMethod.EXPRESSION,
        ]
    )
    name: ClassVar[str] = "pump_linking"
    enabled: bool = Field(default=False)
    join_field_src: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.ATTRIBUTE, default_value=""
    )
    join_field_tgt: FieldMapConfig = FieldMapConfig.with_metadata(metadata)(
        method=ColumnImportMethod.ATTRIBUTE, default_value=""
    )
```

Key changes from the current implementation:
- Remove `connection_node_id_end`
- Remove `ColumnImportMethod.AUTO` from `allowed_methods`
- Add `enabled: bool` (default `False`)
- Add `join_field_src` — column in the user's import layer containing the join key
- Add `join_field_tgt` — column in the connection node layer to match against

### 2. Processor — `processors.py` (PumpProcessor.resolve_end_point, ~line 893)

Replace the current `get_feature_by_id` lookup with the `build_feature_mapping` pattern
used in `CrossSectionLocationProcessor`.

Add a `@cached_property` to build the node lookup map once per import run:

```python
@cached_property
def node_mapping(self):
    """Build {value: feature} mapping from connection node layer using join_field_tgt."""
    tgt_config = self.pump_linking_settings.join_field_tgt.model_dump()
    return build_feature_mapping(self.node_layer.getFeatures(), tgt_config)
```

Update `resolve_end_point`:

```python
def resolve_end_point(self, src_feat, start_point):
    if self.pump_linking_settings.enabled:
        src_config = self.pump_linking_settings.join_field_src.model_dump()
        src_value = get_field_config_value(src_config, src_feat)
        if src_value is not None and src_value is not NULL:
            node_feat = self.node_mapping.get(src_value)
            if node_feat is not None:
                return node_feat.geometry().asPoint()
            else:
                warnings.warn(f"No connection node found for value '{src_value}'")

    # Fallback: point-to-line projection (existing logic unchanged)
    ...
```

### 3. Importer — `importers.py` (PumpsImporter.build_pump_map_source_layer, ~line 518)

Apply the same change as in the processor: replace the `get_feature_by_id` lookup with
`build_feature_mapping` + `get_field_config_value`, guarded by `if settings.enabled`.

### 4. UI — `wizard/settings_widgets.py` (PumpLinkingSettingsWidget, line 441)

Replace the current single-row widget with a pattern that mirrors
`CrossSectionLocationMappingSettingsWidget`, adding a checkbox to enable/disable the
mapping. When disabled, the field map rows are hidden/disabled.

```python
class PumpLinkingSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.PumpLinkingSettings()
        row_dict = {
            "join_field_src": FieldMapRow(
                label="Join field in import layer",
                config=self.model.join_field_src,
            ),
            "join_field_tgt": FieldMapRow(
                label="Join field in connection node layer",
                config=self.model.join_field_tgt,
            ),
        }
        extra_layout = self.get_extra_layout()
        self.setup_ui(row_dict, extra_layout)
        # Populate join_field_tgt attribute dropdown from connection node layer
        self.field_map_widget.table_model.set_fixed_source_attributes_from_data_model(
            "join_field_tgt", dm.ConnectionNode
        )
        self._on_enabled_toggled(self.model.enabled)

    def get_extra_layout(self) -> list[QBoxLayout]:
        self.enabled_checkbox = QCheckBox("Enable connection node mapping")
        self.enabled_checkbox.setChecked(self.model.enabled)
        self.enabled_checkbox.toggled.connect(self._on_enabled_toggled)
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.enabled_checkbox)
        return [checkbox_layout]

    def _on_enabled_toggled(self, checked):
        self.model.enabled = checked
        self.field_map_widget.setEnabled(checked)

    @property
    def group_name(self):
        return "Pump to Connection Node linking settings"
```

Key details:
- `get_extra_layout()` is the same extension point used by
  `CrossSectionLocationMappingSettingsWidget` for its snap distance widget.
- `set_fixed_source_attributes_from_data_model("join_field_tgt", dm.ConnectionNode)`
  populates the attribute dropdown for `join_field_tgt` from the connection node data
  model — exact parallel of how `CrossSectionLocationMappingSettingsWidget` does it for
  `join_field_src` / `dm.Channel`.
- When the checkbox is unchecked, `field_map_widget.setEnabled(False)` greys out the
  rows; no separate show/hide needed.

## Scope Boundaries

**In scope:**
- `PumpLinkingSettings` model (`settings_models.py`)
- `PumpProcessor.resolve_end_point` and `node_mapping` property (`processors.py`)
- `PumpsImporter.build_pump_map_source_layer` (`importers.py`)
- `PumpLinkingSettingsWidget` UI (`wizard/settings_widgets.py`)

**Out of scope:**
- `connection_node_id_start` — not used for pumps or pump_maps
- `CrossSectionLocationSettings` — unchanged, serves as reference only
- Snap distance — not applicable to point-to-point node matching
