---
feature: generic-importer
status: complete
created: 2026-07-22
branch: 20260722-071549-generic-importer-part
decisions:
  - 20260722-071549-generic-importer-design
---

# Generic Importer Design

## Overview

A simple importer/processor pair that copies features from any source layer to any
target layer using only a field map. No connection nodes, no integration logic, no
special matching. Handles both spatial and non-spatial target layers. Geometry is
coerced (linearized, flattened, single-part) and CRS-transformed if needed.

## User Stories

- As a user, I want to import features from an arbitrary source layer into any target
  layer of my schematisation, mapping source fields to target fields, without being
  forced into a predefined object type.

## Scope

**Covered by this design:**
- `GenericProcessor` in `processors.py`
- `GenericImporter` in `importers.py`
- Geometry type compatibility validation
- CRS transformation
- Field mapping via `update_attributes`
- Non-spatial (table) target layers

**NOT covered (follow-up):**
- Processing algorithm (QGIS Processing Framework)
- UI / wizard integration
- New import-settings pages

## Components

### `GenericProcessor(SpatialProcessor)` — `processors.py`

Inherits `SpatialProcessor` for the free `__init__` setup (`target_manager`,
`target_fields`, `target_name`, `transformation`, `context`).

```python
class GenericProcessor(SpatialProcessor):
    def __init__(self, target_layer, target_model_cls, import_settings):
        super().__init__(target_layer, target_model_cls)
        self.fields_configuration = import_settings.fields

    @staticmethod
    def new_geometry(src_feat):
        """Return coerced source geometry, or None for non-spatial features."""
        return get_src_geometry(src_feat, none_ok=True)

    def process_feature(self, src_feat):
        new_geom = self.new_geometry(src_feat)
        if new_geom is not None and self.transformation:
            new_geom.transform(self.transformation)
        new_feat = self.target_manager.create_new(new_geom, self.target_fields)
        update_attributes(
            self.fields_configuration, self.target_model_cls, src_feat, new_feat
        )
        return {self.target_name: [new_feat]}
```

### `GenericImporter(SpatialImporter)` — `importers.py`

Subclasses `SpatialImporter`. Adds geometry type validation in `import_features`
before delegating to `super()`.

```python
class GenericImporter(SpatialImporter):
    def __init__(
        self,
        external_source,
        target_gpkg,
        import_settings,
        target_model_cls,
        target_layer=None,
    ):
        super().__init__(
            external_source, target_gpkg, import_settings, target_model_cls, target_layer
        )
        self.processor = GenericProcessor(
            self.target_layer, target_model_cls, import_settings
        )

    def validate_geometry_compatibility(self):
        """Raise ValueError if source and target geometry types are incompatible.

        Non-spatial targets (NullGeometry) accept any source.
        Spatial targets require source geometry of the same base type.
        """
        src_geom_type = self.external_source.geometryType()
        tgt_geom_type = self.target_layer.geometryType()
        if tgt_geom_type == QgsWkbTypes.GeometryType.NullGeometry:
            return  # non-spatial target accepts anything
        if src_geom_type == QgsWkbTypes.GeometryType.NullGeometry:
            raise ValueError(
                "Source has no geometry but target layer expects geometry"
            )
        if src_geom_type != tgt_geom_type:
            raise ValueError(
                f"Geometry type mismatch: source is {src_geom_type}, "
                f"target is {tgt_geom_type}"
            )

    def import_features(self, context=None, selected_ids=None, progress_callback=None):
        self.validate_geometry_compatibility()
        super().import_features(context, selected_ids, progress_callback)
```

## Key Decisions

| # | Decision | Choice | Reason |
|---|----------|--------|--------|
| 1 | Processor class | New `GenericProcessor` | Clean, no modification of existing classes |
| 2 | Geometry check location | `GenericImporter.validate_geometry_compatibility` (public, no underscore) | Importer has both layers; fail before editing starts |
| 3 | Geometry coercion | Via `get_src_geometry(none_ok=True)` | Consistent with other importers; handles all edge cases |
| 4 | Settings model | Reuse `ImportSettings` (only `.fields` read) | No new model to maintain |
| 5 | Processor base class | `SpatialProcessor` (pragmatic) | Free init (`target_manager`, `target_fields`, etc.) |
| 6 | Non-spatial support | `new_geometry` returns `None`; `FeatureManager.create_new` accepts `None` | No geometry column → no geometry set on feature |

## Tests

### Unit tests (in `test_processors.py` or `test_importers.py`)

Test `validate_geometry_compatibility` directly on `GenericImporter`:

- **matching types** (e.g. both Line): no error raised
- **target non-spatial (NullGeometry)**: no error raised regardless of source
- **source non-spatial, target spatial**: raises `ValueError`
- **type mismatch** (e.g. source Point, target Line): raises `ValueError`

These tests can use lightweight mock layers with just `.geometryType()` set, no real
gpkg needed.

### Integration test (in `test_conversion.py`)

Use `schematisation_channel.gpkg` as source (table: `channel`, Line geometry) and
`empty.gpkg` as target, importing into the `channel` table. Field map copies `code`
and `display_name` via `ATTRIBUTE` method.

Assert:
- The correct number of features was imported into the target channel layer
- Geometry of imported features matches source geometry (within tolerance)
- Mapped attribute values are correct

## Open Questions

- None at this stage. Processing algorithm and UI are explicitly deferred.
