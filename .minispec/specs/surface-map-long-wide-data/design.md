---
feature: surface-map-long-wide-data
status: complete
created: 2026-07-01
---

# Surface Map Long/Wide Data Support

## Overview

The vector data importer currently assumes surface mapping input is always "wide" — multiple
percentage columns where each column maps to a sewage type. This design adds support for "long"
format data (one percentage column, one optional sewage type column, one `surface_map` row per
source row) and merges the previously separate percentage-mapping and surface-linking widgets
and settings models into a single cohesive unit.

## User Stories

- As a user with wide data, I want the existing column-mapping table so that I can assign each
  sewage type to its percentage column as before.
- As a user with long data, I want to pick a single percentage column (required) and optionally
  a sewage type column so that each input row generates exactly one `surface_map` row.
- As a user with long data who has selected a sewage type column, I want to optionally use that
  column for attribute-based pipe matching so that the linking respects the sewage type in my data.

## Data Format Definitions

**Wide data** (existing behaviour):
- Multiple numeric columns, each representing a percentage for one sewage type.
- One `sewer_type_mapping` entry per column.
- One `surface_map` row created per (source row × non-zero mapping).

**Long data** (new):
- One column holds the percentage value (required).
- An optional second column holds the sewage type value.
- Exactly one `surface_map` row created per source row.
- If sewage type column is present, it drives pipe-type filtering for spatial matching and,
  optionally, attribute-based matching.

## Settings Model

Replace `SurfaceMapPercentageSettings` and `SurfaceLinkingSettings` with a single model.
Update `ImportSettings` to reference `surface_map: SurfaceMapSettings` (remove the old
`surface_map_percentage` and `surface_linking` keys — no backward compatibility required).

```python
class SurfaceMapSettings(BaseModel):
    name: ClassVar[str] = "surface_map"

    # Format selection
    data_format: Literal["long", "wide"] = "wide"

    # Long data fields
    percentage_column: Optional[str] = None
    sewage_type_column: Optional[str] = None  # optional; None means not used

    # Wide data fields
    sewer_type_mappings: list[SewerTypeMapping] = []

    # Linking (formerly SurfaceLinkingSettings)
    search_distance: float = Field(default=10.0, ge=0, le=1000000.0)
    selected_pipes_only: bool = False
    attribute_match_enabled: bool = False
    spatial_match_enabled: bool = True
    attribute_match_table: Optional[Literal["pipe", "connection_node"]] = None
    attribute_match_col: Optional[str] = None
    attribute_match_input_config: Optional[FieldMapConfig] = None

    # New: use sewage type source for attribute matching
    use_sewage_type_for_attribute_match: bool = False
```

## Widget: SurfaceMapSettingsWidget

Replaces `SurfaceMapPercentageSettingsWidget` and `SurfaceConnectionSettingsWidget`.

### Layout

```
Data format:  ● Long data  ○ Wide data

── Long data columns ──────────────────────────  [hidden when wide]
Percentage column:   [dropdown - required]
Sewage type column:  [dropdown - "None" + available columns]

── Wide data mappings ─────────────────────────  [hidden when long]
[table: sewage type ↔ percentage column]
[+ Add row]  [− Remove row]

── Linking ────────────────────────────────────
Match mode:  ○ None  ● Pipe  ○ Connection node
  [field map widget]

☐ Use sewage type for attribute matching
  [enabled only when: match mode ≠ None
                  AND sewage type source is present
                      (long: sewage_type_column set;
                       wide: ≥1 sewer_type_mapping row)]

☐ Spatial matching   Search distance: [spinbox] m
☐ Only match selected pipes
```

### Enable/Disable Rules

| Control | Enabled when |
|---|---|
| Long data section | `data_format == "long"` |
| Wide data table | `data_format == "wide"` |
| `Use sewage type for attribute matching` | match mode ≠ None AND sewage type source present |

### Validation

- **Long data:** `percentage_column` must be set (not None).
- **Wide data:** at least one `SewerTypeMapping` must be configured (existing rule).
- Both: if `attribute_match_enabled`, the field map widget must be complete.

## Processor Changes

**File:** `processors.py` — `SurfaceProcessor._create_surface_map_features`

Add a top-level branch on `settings.data_format`:

### Sewage type matching rules (both paths)

These rules apply consistently across long and wide data:

**Spatial matching:**
- If a sewage type is available (long: `sewage_type_column` value; wide: `mapping.sewage_type`),
  spatial search always filters candidates to pipes of that sewage type.
- If no sewage type is available, fall back to nearest pipe regardless of type.
- This behaviour is independent of `use_sewage_type_for_attribute_match`.

**Attribute matching** (`use_sewage_type_for_attribute_match = True`):
- First perform the normal attribute match (field map lookup on pipe or connection node).
- Then verify the matched pipe's sewage type equals the expected sewage type.
- If the sewage type check fails, the match is rejected (treated as no match found).
- Only available when a sewage type source is present.

### Long data path

```python
if settings.data_format == "long":
    pct = float(src_feat[settings.percentage_column])
    if pct <= 0:
        return []

    sewage_type = None
    if settings.sewerage_type_column:
        sewage_type = src_feat[settings.sewerage_type_column]

    if attribute_match_enabled:
        # Attribute match first, then verify sewage type if requested
        matched_pipe = _find_pipe_by_attribute(src_feat, linking)
        if matched_pipe and settings.use_sewerage_type_for_attribute_match:
            if matched_pipe["sewage_type"] != sewage_type:
                matched_pipe = None  # reject mismatch
        nearest_pipe = matched_pipe

    if spatial_match_enabled and nearest_pipe is None:
        # Spatial search, always filtering by sewage_type when available
        nearest_pipe = _find_nearest_pipe(
            surface_geom, self.pipe_features, pipe_ids,
            sewage_type_filter=sewage_type,  # None if not set → no filter
            linking=linking,
        )

    # Create exactly one surface_map row
    sm_feat["percentage"] = pct
    return [sm_feat] if nearest_pipe else []
```

### Wide data path

Largely unchanged: iterate `sewer_type_mappings`, one row per non-zero mapping entry.
The sewage type for each iteration comes from `mapping.sewage_type`.

Apply the same matching rules as long data, substituting `mapping.sewage_type` for `sewage_type`:
- Spatial search filters by `mapping.sewage_type` when set.
- If `use_sewage_type_for_attribute_match`, attribute match result is verified against
  `mapping.sewage_type` before accepting.

## Files Touched

| File | Change |
|---|---|
| `vector_data_importer/settings_models.py` | Add `SurfaceMapSettings`; remove `SurfaceMapPercentageSettings` and `SurfaceLinkingSettings`; update `ImportSettings` |
| `vector_data_importer/wizard/settings_widgets.py` | Add `SurfaceMapSettingsWidget`; remove `SurfaceMapPercentageSettingsWidget` and `SurfaceConnectionSettingsWidget` |
| `vector_data_importer/processors.py` | Branch `_create_surface_map_features` on `data_format`; add long-data logic |
| Wizard step registration (wherever widgets are wired into pages) | Replace two widget references with one `SurfaceMapSettingsWidget` |

## Resolved Questions

1. **Sewage type column dropdown**: show all columns (can be refined later to filter by type).
2. **Wide data + attribute matching**: `use_sewage_type_for_attribute_match` is global — all
   mapping rows use the same behaviour. The intent is: first do attribute match, then verify
   the matched pipe's sewage type matches the mapping's sewage type.
3. **Spatial matching + sewage type**: spatial matching always filters by sewage type when it
   is available (long: `sewage_type_column` set; wide: per-mapping sewage type). If no sewage
   type is available, fall back to nearest pipe regardless of type.
