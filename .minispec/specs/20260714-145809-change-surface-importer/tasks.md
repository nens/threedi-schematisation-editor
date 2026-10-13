---
feature: change-surface-importer
status: complete
created: 2026-07-14
chunk_size: medium
total_tasks: 4
estimated_lines: 150
---

# Change Surface Importer — Replace attribute_match_col with attribute_match_target_config

## Overview

Replace the plain string `attribute_match_col` in `SurfaceLinkingSettings` with a `FieldMapConfig` (`attribute_match_target_config`) supporting ATTRIBUTE and EXPRESSION methods. Mirrors the `CrossSectionLocationSettings` pattern. Includes extracting shared processor logic into a utility function.

## Task List

### Foundation

#### Task 1: Extract `build_feature_mapping` utility
- **Estimate:** ~25 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Add a module-level function `build_feature_mapping(layer, field_config_dict)` that builds a `{value: feature}` dict from a layer using a `FieldMapConfig` dict. Supports ATTRIBUTE and EXPRESSION methods; returns `{}` on invalid/missing config.
- **Depends on:** None
- **Acceptance:** Function exists and handles both methods correctly
- **Evidence:** Unit tests for `build_feature_mapping` pass (add to `test_processors_surface.py` or a shared test)

### Core Implementation

#### Task 2: Update model + processors + processor tests
- **Estimate:** ~50 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/settings_models.py`, `threedi_schematisation_editor/vector_data_importer/processors.py`, `tests/vector_data_importer/test_processors_surface.py`
- **Description:**
  - `settings_models.py`: Remove `attribute_match_col: Optional[str] = None`, add `attribute_match_target_config: Optional[FieldMapConfig] = None`
  - `processors.py` — `CrossSectionLocationProcessor.channel_mapping`: Refactor to call `build_feature_mapping(self.channel_layer, self.join_field_tgt)`
  - `processors.py` — `SurfaceProcessor.get_attribute_match`: Replace `f[linking.attribute_match_col]` lookup with `build_feature_mapping` on the appropriate layer, then look up `input_val` in the resulting dict
  - `test_processors_surface.py`: Replace `attribute_match_col="code"` with `attribute_match_target_config=FieldMapConfig(method="attribute", attribute="code")`
- **Depends on:** Task 1
- **Acceptance:** Attribute-based surface linking works end-to-end; cross-section location processor unaffected
- **Evidence:** `pytest tests/vector_data_importer/test_processors_surface.py -q --tb=short` passes; `pytest tests/vector_data_importer/test_cross_section_location_processor.py -q --tb=short` passes

#### Task 3: Update widget
- **Estimate:** ~60 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/wizard/settings_widgets.py`
- **Description:**
  - Remove `match_table_col` QComboBox and its `_repopulate_match_col` / `_on_match_col_changed` logic
  - Add a target `FieldMapWidget` row for `attribute_match_target_config` (allowed methods: ATTRIBUTE, EXPRESSION)
  - Call `set_fixed_source_attributes_from_data_model` with `dm.Pipe` or `dm.ConnectionNode` when the table radio changes; update the row label dynamically ("Match field in pipe" / "Match field in connection_node")
  - Update `_on_match_table_changed`, `_sync_match_input_config`, `_update_model`, `deserialize`, `is_valid` to use the new widget
- **Depends on:** Task 2
- **Acceptance:** UI shows target FieldMapWidget with correct label for each table selection; config round-trips correctly via `deserialize`
- **Evidence:** Manual smoke test in QGIS; `pytest tests/vector_data_importer/ -q --tb=short` passes

### Fixtures

#### Task 4: Update config fixtures & dev scripts
- **Estimate:** ~15 lines
- **Files:** `tests/vector_data_importer/data/config/import_surfaces_long.json`, `tests/vector_data_importer/data/config/import_surfaces_wide.json`, `generate_surface_refs.py`
- **Description:**
  - Replace `"attribute_match_col": "code"` with `"attribute_match_target_config": {"method": "attribute", "attribute": "code"}` in `import_surfaces_long.json`
  - Set `"attribute_match_target_config": null` in `import_surfaces_wide.json` (was `null` for `attribute_match_col`)
  - Update `generate_surface_refs.py` to use `attribute_match_target_config=FieldMapConfig(method="attribute", attribute="code")`
- **Depends on:** Task 2
- **Acceptance:** Config files deserialize correctly into `SurfaceLinkingSettings`
- **Evidence:** `pytest tests/vector_data_importer/ -q --tb=short` passes with updated fixtures

## Notes

- Tasks 3 and 4 can run in parallel after Task 2 is done.
- No backward compatibility required for saved JSON configs.
- `generate_surface_refs.py` is a developer utility for regenerating integration test reference GPKGs — update it but no need to run it as part of this feature unless reference files need regenerating.
- The open question about where to place `build_feature_mapping` is resolved: keep it in `processors.py` near existing usage.

## Progress
- [x] Task 1: Extract `build_feature_mapping` utility
- [x] Task 2: Update model + processors + processor tests
- [x] Task 3: Update widget
- [x] Task 4: Update config fixtures & dev scripts
