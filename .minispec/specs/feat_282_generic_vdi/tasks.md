---
feature: feat_282_generic_vdi
status: complete
created: 2026-07-22
chunk_size: medium
total_tasks: 4
estimated_lines: 175
---

# Generic Importer Tasks

## Overview
Add a generic importer/processor pair to the vector data importer that copies features
from any source layer to any target layer using only a field map. No connection nodes,
no integration logic. Supports both spatial and non-spatial targets.

## Task List

### Foundation

#### Task 1: GenericProcessor
- **Estimate:** ~40 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/processors.py`
- **Description:** Add `GenericProcessor(SpatialProcessor)` with `__init__`,
  `new_geometry` (wraps `get_src_geometry(none_ok=True)`), and `process_feature`
  (coerce geometry, transform, create feature, update_attributes).
- **Depends on:** None
- **Evidence:** Class exists and is importable

#### Task 2: GenericImporter + geometry validation
- **Estimate:** ~35 lines
- **Files:** `threedi_schematisation_editor/vector_data_importer/importers.py`
- **Description:** Add `GenericImporter(SpatialImporter)` with `__init__` (sets
  `self.processor = GenericProcessor(...)`), `validate_geometry_compatibility`
  (raises `ValueError` on mismatch; non-spatial target accepts anything), and
  `import_features` (calls validate then `super()`).
- **Depends on:** Task 1
- **Evidence:** Class exists and is importable

### Core Implementation

#### Task 3: Unit tests for geometry validation
- **Estimate:** ~50 lines
- **Files:** `tests/vector_data_importer/test_importers.py`
- **Description:** Test `validate_geometry_compatibility` with mock layers:
  matching types (no error), non-spatial target (no error), non-spatial source +
  spatial target (ValueError), type mismatch Point vs Line (ValueError).
- **Depends on:** Task 2
- **Parallel:** Can run with Task 4
- **Evidence:** `pytest tests/vector_data_importer/test_importers.py -q` passes

#### Task 4: Integration test
- **Estimate:** ~50 lines
- **Files:** `tests/vector_data_importer/test_conversion.py`
- **Description:** Import `channel` features from `schematisation_channel.gpkg`
  into `empty.gpkg` using `GenericImporter`, field-mapping `code` and
  `display_name` via ATTRIBUTE method. Assert feature count, geometry match, and
  attribute values on the target layer.
- **Depends on:** Task 2
- **Parallel:** Can run with Task 3
- **Evidence:** `pytest tests/vector_data_importer/test_conversion.py -q` passes

## Notes
- `validate_geometry_compatibility` is a public method (no underscore prefix)
- Processing algorithm and UI are explicitly out of scope

## Progress
- [x] Task 1: GenericProcessor
- [x] Task 2: GenericImporter + geometry validation
- [x] Task 3: Unit tests for geometry validation
- [x] Task 4: Integration test
