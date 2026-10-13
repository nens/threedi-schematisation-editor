# Sewer Type Preference Table

## Overview

Replace the two hardcoded preference spinboxes (`stormwater_sewer_preference`, `sanitary_sewer_preference`) in `SurfaceLinkingSettings` and `SurfaceConnectionSettingsWidget` with a configurable table where any sewerage type can have a distance preference offset. The table follows the same pattern as the existing `SewerTypeMappingModel` in `SurfaceMapPercentageSettingsWidget`.

## Motivation

The current design hardcodes preference offsets for exactly two sewerage types (storm drain and sanitary sewer). A table-based approach allows preference offsets for any sewerage type, is more consistent with the existing sewer type mapping table UI, and requires no code changes when new sewerage types need preferencing.

## Design

### New model: `SewerTypePreference`

In `settings_models.py`:

```python
class SewerTypePreference(BaseModel):
    sewerage_type: int
    preference: float  # metres subtracted from distance when ranking pipes
```

### Updated model: `SurfaceLinkingSettings`

Remove `stormwater_sewer_preference` and `sanitary_sewer_preference`. Add:

```python
sewer_type_preferences: list[SewerTypePreference] = []
```

### New table model: `SewerTypePreferenceModel`

A new `QAbstractTableModel` in `settings_widgets.py`, following the same pattern as `SewerTypeMappingModel`:

- Column 0: Sewerage type — combobox delegate using `_SEWERAGE_TYPE_ITEMS` (same as existing)
- Column 1: Preference (m) — editable float (plain text, not a combobox)
- Headers: `["Sewerage type", "Preference (m)"]`
- `get_preferences()` → `list[SewerTypePreference]`
- `set_preferences(preferences)` restores from model

The sewerage type column reuses the existing `SewerTypeMappingDelegate` for column 0 (combobox). Column 1 is plain editable text (the delegate returns None for that column, falling back to default editing).

### Updated widget: `SurfaceConnectionSettingsWidget`

Remove the two `QDoubleSpinBox` rows (rows 4 and 5 of the grid layout for stormwater/sanitary preference). Replace with a preference table group below the existing grid, styled the same as the sewer type mapping table in `SurfaceMapPercentageSettingsWidget`:

```
[Surface map layer]   [combo]
[Pipe layer]          [combo] [Selected only]
[Connection node]     [combo]
[Search distance]     [spinbox] m
--- Sewerage type preference ---
[Sewerage type | Preference (m)]
[row 1        | value          ]
[Delete row]              [Add row]
```

`_update_model()` reads from both the grid spinbox and the preference table.

`deserialize()` restores the preference table via `set_preferences()`.

### Updated processor: `SurfaceProcessor._find_nearest_pipe`

Build a lookup dict at `__init__` time from `import_settings.surface_linking.sewer_type_preferences`:

```python
self.preference_by_type = {
    p.sewerage_type: p.preference
    for p in import_settings.surface_linking.sewer_type_preferences
}
```

Pass it to `_find_nearest_pipe` instead of the full `linking` object (or keep passing `linking` and look up inline). In `_find_nearest_pipe`, replace:

```python
if mapping.sewerage_type == SewerageType.STORM_DRAIN.value:
    dist -= linking.stormwater_sewer_preference
elif mapping.sewerage_type == SewerageType.SANITARY_SEWER.value:
    dist -= linking.sanitary_sewer_preference
```

with:

```python
dist -= preference_by_type.get(mapping.sewerage_type, 0.0)
```

### JSON config format

```json
"surface_linking": {
    "search_distance": 250.0,
    "sewer_type_preferences": [
        {"sewerage_type": 1, "preference": 20.0},
        {"sewerage_type": 2, "preference": 10.0}
    ],
    "surface_map_layer_name": "Surface map",
    "pipe_layer_name": "Pipe",
    "node_layer_name": "Connection node",
    "selected_pipes_only": false
}
```

Empty list = no preferences (all types treated equally), which is the default.

### Backward compatibility

Old JSON configs with `stormwater_sewer_preference` and `sanitary_sewer_preference` will load without error (pydantic ignores extra fields) but the values will be silently dropped. Users who relied on these fields need to migrate their configs to `sewer_type_preferences`.

## Affected files

- `settings_models.py` — add `SewerTypePreference`, update `SurfaceLinkingSettings`
- `wizard/settings_widgets.py` — add `SewerTypePreferenceModel`, update `SurfaceConnectionSettingsWidget`
- `processors.py` — update `SurfaceProcessor.__init__` and `_find_nearest_pipe`
- `tests/vector_data_importer/test_processors_surface.py` — update preference offset tests
- JSON configs (`import_bgt.json`, `import_surface_bgt.json`)

## Open questions

- None
