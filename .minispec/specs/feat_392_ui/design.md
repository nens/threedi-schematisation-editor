---
feature: feat_392_ui
status: complete
created: 2026-07-15
---

# Pump Import Wizard Pages Design

## Overview

Add `ImportPumpWizard` to the vector data importer wizard infrastructure. The wizard supports both point and line source layers, conditionally showing settings based on geometry type. It inherits from `ImportWithCreateConnectionNodesWizard` and adds a new `PumpDirectionSettingsWidget`. Two existing components need small extensions: `IntegrationSettingsWidget` gains an `update_layer()` method to hide `min_length` for point sources, and `SettingsPage` gains group-box-level visibility toggling via a `should_show(layer)` hook on settings widgets.

## User Stories

- As a user, I want to import pumps from a point or line layer so that I can bring external pump data into my schematisation.
- As a user, I want pump direction settings only shown when my source is a line layer, so the UI is not cluttered with irrelevant options.
- As a user, I want to optionally integrate imported pumps onto existing pipes or channels.
- As a user, I want to optionally create connection nodes during import and map their fields.

## Components

### 1. `SettingsWidget` base class (extension, `settings_widgets.py`)

Two new class-level attributes added to the base:

- `group_box = None` — placeholder set by `SettingsPage.setup_ui` when the widget is mounted into a page. Defined on the class so it is always present and never raises `AttributeError`.
- `should_show(layer) -> bool` — default returns `True`. Subclasses override to conditionally hide their group box based on the selected source layer.

```python
class SettingsWidget(QWidget):
    dataChanged = pyqtSignal()
    model = None
    group_box = None  # Set by SettingsPage.setup_ui when the widget is added to a page

    def should_show(self, layer) -> bool:
        """Override to conditionally hide this widget's group box. Default: always show."""
        return True
```

### 2. `PumpDirectionSettingsWidget` (new, `settings_widgets.py`)

Inherits `FieldMapSettingsWidget`. Shows a single `direction` field map row backed by `sm.PumpSettings`. Overrides `should_show(layer)` to return `True` only for line geometry sources.

```python
class PumpDirectionSettingsWidget(FieldMapSettingsWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.model = sm.PumpSettings()
        row_dict = {
            "direction": FieldMapRow(label="Pump direction", config=self.model.direction),
        }
        self.setup_ui(row_dict)

    @property
    def group_name(self):
        return "Pump direction settings"

    def should_show(self, layer) -> bool:
        from qgis.core import QgsWkbTypes
        return layer and layer.geometryType() == QgsWkbTypes.GeometryType.LineGeometry
```

### 3. `IntegrationSettingsWidget.update_layer()` (extension, `settings_widgets.py`)

Hides the `min_length` label and spinbox for point sources, since `PointStructurePlacement` always produces length 0 and the setting has no effect. Requires storing the label as `self.min_length_label` in `setup_integration_settings`.

```python
def update_layer(self, layer):
    from qgis.core import QgsWkbTypes
    is_point = layer and layer.geometryType() == QgsWkbTypes.GeometryType.PointGeometry
    self.min_length_label.setVisible(not is_point)
    self.min_length.setVisible(not is_point)
```

### 4. `SettingsPage` visibility toggling (extension, `pages.py`)

**`setup_ui`:** Store a reference to the group box on the widget instance after creation:
```python
widget.group_box = group_box
```

**`initializePage`:** Call `update_layer` then toggle group box visibility via `should_show`. No `hasattr` guards needed because both methods are defined on `SettingsWidget`:
```python
for widget in self.settings_widgets:
    if hasattr(widget, "update_layer"):
        widget.update_layer(layer)
    widget.group_box.setVisible(widget.should_show(layer))
```

**`isComplete`:** Skip hidden widgets:
```python
def isComplete(self):
    for widget in self.settings_widgets:
        if not widget.group_box.isVisible():
            continue
        if not widget.is_valid:
            return False
    return True
```

**`get_settings`:** Skip hidden widgets:
```python
def get_settings(self):
    return {
        widget.name: widget.get_settings()
        for widget in self.settings_widgets
        if widget.group_box.isVisible()
    }
```

### 5. `ImportPumpWizard` (new, `wizard.py`)

```python
class ImportPumpWizard(ImportWithCreateConnectionNodesWizard):
    settings_widgets_classes = [
        ConnectionNodeSettingsWidget,
        PumpDirectionSettingsWidget,
        IntegrationSettingsWidget,
    ]

    @property
    def layer_filter(self):
        return QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PointLayer

    def prepare_import(self):
        from qgis.core import QgsWkbTypes
        processed_handlers, processed_layers = super().prepare_import()

        # PumpMap layer — only needed for line sources
        if self.selected_layer.geometryType() == QgsWkbTypes.GeometryType.LineGeometry:
            pump_map_handler = self.layer_manager.model_handlers[dm.PumpMap]
            processed_handlers.append(pump_map_handler)
            processed_layers["pump_map_layer"] = pump_map_handler.layer

        # Conduit layer — based on integration mode
        integration_settings = self.get_settings().integration
        if integration_settings.integration_mode == sm.IntegrationMode.CHANNELS:
            conduit_handler = self.layer_manager.model_handlers[dm.Channel]
            xsec_handler = self.layer_manager.model_handlers[dm.CrossSectionLocation]
            processed_handlers += [conduit_handler, xsec_handler]
            processed_layers["conduit_layer"] = conduit_handler.layer
            processed_layers["cross_section_location_layer"] = xsec_handler.layer
        elif integration_settings.integration_mode == sm.IntegrationMode.PIPES:
            conduit_handler = self.layer_manager.model_handlers[dm.Pipe]
            processed_handlers.append(conduit_handler)
            processed_layers["conduit_layer"] = conduit_handler.layer

        return processed_handlers, processed_layers
```

### 6. `wizard/__init__.py` and plugin `__init__.py`

- `wizard/__init__.py`: export `ImportPumpWizard`.
- `threedi_schematisation_editor/__init__.py`: import `ImportPumpWizard`; add `"Pumps"` entry to `import_actions_spec` (alphabetically between Pipes and Surfaces); add `import_external_pumps()` method.

## Page Flow

| Page | Point source | Line source |
|------|-------------|-------------|
| 1. StartPage | Point + Line filter | Point + Line filter |
| 2. SettingsPage | ConnectionNode + Integration (min_length hidden) | ConnectionNode + PumpDirection + Integration (all fields) |
| 3. FieldMapPage (`dm.Pump`) | ✅ | ✅ |
| 4. FieldMapPage (`dm.ConnectionNode`) | conditional on `create_nodes` | conditional on `create_nodes` |
| 5. RunPage | ✅ | ✅ |

## Settings Widget Visibility Matrix

| Widget | Point source | Line source | Controlled by |
|--------|-------------|-------------|---------------|
| `ConnectionNodeSettingsWidget` | ✅ shown | ✅ shown | always |
| `PumpDirectionSettingsWidget` | ❌ hidden | ✅ shown | `should_show(layer)` |
| `IntegrationSettingsWidget` | ✅ shown | ✅ shown | always |
| — min_length row (inside Integration) | ❌ hidden | ✅ shown | `update_layer(layer)` |

## Files Modified

| File | Change |
|------|--------|
| `wizard/settings_widgets.py` | Add `group_box = None` and `should_show()` to `SettingsWidget` base; add `PumpDirectionSettingsWidget`; extend `IntegrationSettingsWidget` with `self.min_length_label` and `update_layer()` |
| `wizard/pages.py` | Store `widget.group_box` in `setup_ui`; toggle visibility in `initializePage`; skip hidden widgets in `isComplete` and `get_settings` |
| `wizard/wizard.py` | Import `PumpDirectionSettingsWidget`; add `ImportPumpWizard` |
| `wizard/__init__.py` | Export `ImportPumpWizard` |
| `threedi_schematisation_editor/__init__.py` | Import and wire `ImportPumpWizard`; add "Pumps" menu entry and `import_external_pumps()` method |
