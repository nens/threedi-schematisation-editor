---
feature: pump-wizard-ui
status: complete
created: 2026-07-17
related: .minispec/specs/feat_392_pump_map_import/design.md
---

# Pump Wizard UI Design

## Overview

Update `ImportPumpWizard` to reflect the backend changes introduced in
`feat_392_pump_map_import`: pump import is now point-source only, and the wizard
must expose the new `PumpLinkingSettings` and `PointToLineSettings` that control
pump_map creation. Dead code paths for line-source pumps are removed.

## User Stories

- As a modeller, I want to configure how pump_map end nodes are resolved (by mapped
  connection node ID or by point-to-line projection) directly in the import wizard.
- As a modeller, I want to configure point-to-line conversion settings for pump_map
  end-point projection.
- As a modeller, I want the wizard to only offer point layers as source, since line-source
  pump import is no longer supported.

## Changes

### 1. `ImportPumpWizard.layer_filter`

Change from `LineLayer | PointLayer` to `PointLayer` only, since all pump import is now
point-source.

### 2. `ImportPumpWizard.settings_widgets_classes`

Replace the current list:
```python
[ConnectionNodeSettingsWidget, IntegrationSettingsWidget]
```
with:
```python
[
    ConnectionNodeSettingsWidget,
    PumpLinkingSettingsWidget,
    PointToLIneConversionSettingsWidget,
    IntegrationSettingsWidget,
]
```

Order rationale: pump linking (primary end-node resolution) comes before point-to-line
(fallback), mirroring the runtime priority. Integration follows, consistent with
`ImportStructureWizard`.

All four widgets are always shown; no `should_show` override on any of them.

### 3. `PumpLinkingSettingsWidget`  (new, `settings_widgets.py`)

A thin `FieldMapSettingsWidget` subclass — one field map row for
`connection_node_id_end`.

```python
class PumpLinkingSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.PumpLinkingSettings()
        row_dict = {
            "connection_node_id_end": FieldMapRow(
                label="Connection node ID end",
                config=self.model.connection_node_id_end,
            ),
        }
        self.setup_ui(row_dict)

    @property
    def group_name(self):
        return "Pump linking settings"
```

`PumpLinkingSettings.connection_node_id_end` allows methods AUTO / ATTRIBUTE /
EXPRESSION, default AUTO.

### 4. `ImportPumpWizard.prepare_import`

Remove the `LineGeometry` guard that conditionally added `pump_map_layer`. Since pumps
can now always produce pump_maps (from point source), `pump_map_layer` is always
included:

```python
def prepare_import(self):
    processed_handlers, processed_layers = super().prepare_import()
    pump_map_handler = self.layer_manager.model_handlers[dm.PumpMap]
    processed_handlers.append(pump_map_handler)
    processed_layers["pump_map_layer"] = pump_map_handler.layer
    # Conduit layer — based on integration mode (unchanged)
    integration_settings = self.get_settings().integration
    if integration_settings.integration_mode == sm.IntegrationMode.CHANNELS:
        ...
    elif integration_settings.integration_mode == sm.IntegrationMode.PIPES:
        ...
    return processed_handlers, processed_layers
```

### 5. `wizard/DESIGN.md`

Remove the entry for `PumpDirectionSettingsWidget` and its `should_show` override.
Document `PumpLinkingSettingsWidget`.

## Note on `IntegrationSettingsWidget.update_layer`

`update_layer` hides `min_length` for point sources
(`PointStructurePlacement` always produces length 0). Since the pump wizard is now
point-only, this branch will always be triggered. The widget logic is general and used
by other wizards, so no change is needed — it simply always hides `min_length` in the
pump wizard.

## Scope

**In scope:**
- `ImportPumpWizard.layer_filter` restricted to point layers
- `ImportPumpWizard.settings_widgets_classes` updated with two new widgets
- `PumpLinkingSettingsWidget` added to `settings_widgets.py`
- `ImportPumpWizard.prepare_import` — always include `pump_map_layer`
- `wizard/DESIGN.md` updated

**Out of scope:**
- A dedicated `pump_map_fields` field map page (not needed for this feature)
- Processing algorithm UI updates
