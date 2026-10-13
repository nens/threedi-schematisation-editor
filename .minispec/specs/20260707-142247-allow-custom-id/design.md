---
feature: allow-custom-id-methods
status: complete
created: 2026-07-07
updated: 2026-07-22
branch: feat_433_custom_id
decisions:
  - 20260707-1422-id-conflict-scope
  - 20260707-1422-id-allowed-methods
  - 20260707-1422-id-resolution-point
  - 20260707-1422-feature-manager-next-id
---

# Custom ID Methods for Vector Data Importer

## Overview

Currently the `id` field of imported features is always assigned automatically by `FeatureManager` (AUTO method only). This feature allows users to set the `id` field using ATTRIBUTE, EXPRESSION, or DEFAULT methods as well. When a non-AUTO method is chosen, the resolved ID is checked against all IDs already present in the target layer and all IDs assigned earlier in the same import batch. If the resolved ID conflicts, the feature is skipped with a `FeaturesImporterWarning`.

## User Stories

### User Story 1 — Import features preserving source IDs (Priority: P1)

A user has a source layer where features already have meaningful IDs they want to preserve in the schematisation. They select the `id` field method as ATTRIBUTE and pick the source field. Imported features receive the source IDs. If a source ID already exists in the target layer, that feature is skipped and a warning is shown.

**Why this priority**: Core use case — the feature has no value without this.

**Independent Test**: Can be fully tested by importing a small source layer with known IDs into a layer that already contains one conflicting ID and verifying the skip + warning behaviour.

**Acceptance Scenarios**:

1. **Given** a source layer with IDs [1, 2, 3] and a target layer already containing ID 2, **When** the user imports with `id` method = ATTRIBUTE pointing to the source ID field, **Then** features 1 and 3 are imported successfully and feature 2 is skipped with a `FeaturesImporterWarning`.
2. **Given** a source layer where two features have the same ID value (e.g. both have ID 5), **When** importing with `id` method = ATTRIBUTE, **Then** the first is imported and the second is skipped with a warning (intra-batch conflict).
3. **Given** a source layer with IDs [10, 20, 30] and an empty target layer, **When** importing with `id` method = ATTRIBUTE, **Then** all three features are imported with IDs 10, 20, 30 respectively.

---

### User Story 2 — Import features with a computed ID (Priority: P2)

A user wants to derive IDs via a QGIS expression (e.g. `to_int(left("code", 4))`) or set all features to the same base ID shifted by a DEFAULT value. Conflict detection still applies.

**Why this priority**: Extends the same mechanism — useful but not the primary driver.

**Independent Test**: Can be tested by configuring an EXPRESSION or DEFAULT method for the `id` field and verifying the resulting IDs match expectations, with conflict skipping working as in Story 1.

**Acceptance Scenarios**:

1. **Given** an EXPRESSION method `to_int("source_id") + 1000` for the `id` field, **When** importing, **Then** each feature's ID equals the source `source_id` value plus 1000.
2. **Given** a DEFAULT method with value `42` for the `id` field and two features to import, **When** importing, **Then** the first feature gets ID 42 and the second is skipped with a conflict warning.

---

### Edge Cases

- What if `get_field_config_value` returns NULL for the `id` field (e.g. source attribute missing)? → The feature is skipped with a `FeaturesImporterWarning` indicating the ID could not be resolved.
- What if the resolved ID is not a valid integer (e.g. a string that can't be converted)? → `convert_to_type` raises `TypeConversionError`; the feature is skipped with a warning.
- What if AUTO is selected for `id`? → Existing behaviour is unchanged; `FeatureManager` assigns and increments `next_id`.
- What if the target layer is empty? → `used_ids` starts as an empty set; the first non-conflicting custom ID is always accepted.
- Does this affect `node_manager`, `surface_map_manager`, `integrate_manager`? → No. Those managers always use AUTO and are not exposed to the user's field map.

## Requirements

### Functional Requirements

- **FR-001**: The `id` field MUST allow methods AUTO, ATTRIBUTE, and EXPRESSION only (IGNORE and DEFAULT are excluded).
- **FR-002**: AUTO MUST remain the default method for the `id` field in the UI and in new configs.
- **FR-003**: When a non-AUTO method is chosen for `id`, the system MUST resolve the ID before creating the feature.
- **FR-004**: The conflict check MUST cover both IDs already present in the target layer at import start AND IDs assigned to earlier features in the same import batch.
- **FR-005**: On a conflict, the feature MUST be skipped (not imported) and a `FeaturesImporterWarning` MUST be emitted.
- **FR-006**: On a conflict, `FeatureManager.next_id` MUST NOT advance (the conflicting ID was not used for AUTO assignment).
- **FR-007**: When a non-AUTO custom ID is successfully assigned, `FeatureManager.next_id` MUST NOT advance.
- **FR-008**: When AUTO assigns an ID, `FeatureManager.next_id` MUST advance as today and the assigned ID MUST be added to `used_ids`.

### Key Entities

- **`FeatureManager`** (`utils.py`): Tracks `next_id` for AUTO assignment and a `used_ids` set for conflict detection. `used_ids` is seeded from the target layer at construction time.
- **`FieldMapConfig`** / `get_allowed_methods_for_model_class_field` (`settings_models.py`): Controls which methods are offered for each field. The special-case rule forcing `[AUTO]` for `"id"` fields is removed.

## Design

### `settings_models.py` — remove special-case `id` rule

In `get_allowed_methods_for_model_class_field`, remove the branch:

```python
if model_field.name == "id":
    allowed_methods = [ColumnImportMethod.AUTO]
```

With this removed, `id` falls through to the default path which allows all methods except AUTO. Then the existing non-optional guard removes IGNORE (since `id` is not optional), resulting in `[ATTRIBUTE, EXPRESSION, DEFAULT]`. To also allow AUTO, add it back explicitly:

```python
if model_field.name == "id":
    allowed_methods = [
        m for m in ColumnImportMethod
        if m not in (ColumnImportMethod.IGNORE, ColumnImportMethod.DEFAULT)
    ]
```

This yields `[AUTO, ATTRIBUTE, EXPRESSION]`.

### `utils.py` — `FeatureManager` changes

```python
class FeatureManager:
    def __init__(self, next_id=1, existing_ids=None):
        self.next_id = next_id
        self.used_ids = set(existing_ids) if existing_ids else set()

    def create_new(self, geom, fields, attributes=None, explicit_id=None):
        new_feat = QgsFeature(fields)
        result = self.add_feature(new_feat, geom, attributes, explicit_id=explicit_id)
        if result is None:
            return None  # conflict — caller should return {} and skip related features
        return new_feat

    def add_feature(self, new_feat, geom=None, attributes=None, set_id=True, explicit_id=None):
        if geom:
            new_feat.setGeometry(geom)
        if attributes:
            for field_name, field_value in attributes.items():
                new_feat[field_name] = field_value
        if not set_id:
            return new_feat  # integrator split-conduit case: keep existing ID
        if explicit_id is not None:
            if explicit_id in self.used_ids:
                warnings.warn(
                    f"Feature with id {explicit_id} skipped: id already exists in "
                    f"target layer or was already assigned in this import.",
                    FeaturesImporterWarning,
                )
                return None  # signal conflict to caller
            new_feat["id"] = explicit_id
            self.used_ids.add(explicit_id)
        else:
            # AUTO: advance next_id past any already-used ids
            while self.next_id in self.used_ids:
                self.next_id += 1
            new_feat["id"] = self.next_id
            self.used_ids.add(self.next_id)
            self.next_id += 1
        return new_feat
```

The existing `set_id=True/False` parameter is kept for backward compatibility — `set_id=False` is used in the integrators (`add_feature(..., set_id=(i > 0))`) to preserve the original conduit ID for the first split segment. The three-way behaviour is:

```
set_id=True,  explicit_id=None    → AUTO (existing behaviour, next_id assigned)
set_id=False, explicit_id=None    → no ID set (existing integrator usage)
set_id=True,  explicit_id=<value> → custom ID with conflict check
```

This avoids touching any integrator call sites.

### `processors.py` — `process_feature` call sites

Extract a shared helper to avoid repeating the resolution logic across all processors:

```python
def resolve_id(fields_configuration, src_feat, target_manager, expression_context=None):
    """Resolve the id field config. Returns (explicit_id, skip) tuple.
    
    explicit_id=None means AUTO. skip=True means the feature should be skipped.
    """
    id_config = fields_configuration.get("id")
    if id_config is None:
        return None, False
    method = ColumnImportMethod(id_config["method"])
    if method == ColumnImportMethod.AUTO:
        return None, False
    resolved = get_field_config_value(id_config, src_feat, expression_context)
    if resolved == NULL or resolved is None:
        warnings.warn(
            f"Feature skipped: could not resolve id value from source feature.",
            FeaturesImporterWarning,
        )
        return None, True
    try:
        explicit_id = convert_to_type(resolved, int)
    except TypeConversionError as e:
        warnings.warn(
            f"Feature skipped: id value '{resolved}' could not be converted to int. {e}",
            FeaturesImporterWarning,
        )
        return None, True
    return explicit_id, False
```

Each `process_feature` that calls `target_manager.create_new(...)` changes to:

```python
explicit_id, skip = resolve_id(self.fields_configuration, src_feat, self.target_manager)
if skip:
    return {}
new_feat = self.target_manager.create_new(new_geom, self.target_fields, explicit_id=explicit_id)
if new_feat is None:  # conflict detected inside FeatureManager
    return {}
update_attributes(self.fields_configuration, ModelCls, src_feat, new_feat)
```

**Affected processors:**
- `ConnectionNodeProcessor.process_feature`
- `PointProcessor.process_feature`
- `LineProcessor.process_feature`
- `CrossSectionLocationProcessor.process_feature`
- `SurfaceProcessor.process_feature`

### `utils.py` — `update_attributes`

`update_attributes` already skips fields whose method is `AUTO`. However, for non-AUTO `id` methods, `update_attributes` would re-apply the `id` field config and overwrite the ID already set by the processor via `explicit_id`. Skip `id` unconditionally in `update_attributes`:

```python
if field_name == "id":
    continue
if ColumnImportMethod(field_config["method"]) == ColumnImportMethod.AUTO:
    continue
```

The `id` field is always handled before feature creation — either by `FeatureManager` (AUTO) or by `resolve_id` + `explicit_id` (non-AUTO). `update_attributes` must not touch it.

### `FeatureManager` construction — seed `used_ids`

In `SpatialProcessor.__init__`, update the construction:

```python
self.target_manager = (
    FeatureManager(
        get_next_feature_id(target_layer),
        existing_ids=get_existing_ids(target_layer),
    )
    if target_layer else None
)
```

Add a small helper in `utils.py` (or reuse `get_next_feature_id`'s logic):

```python
def get_existing_ids(layer):
    """Return set of all existing id values in the layer."""
    id_idx = layer.fields().indexFromName("id")
    return set(layer.uniqueValues(id_idx))
```

This seeds `used_ids` from the layer at import start. As AUTO and custom IDs are assigned during the import, they are added to `used_ids` in `add_feature`.

## Components Summary

| Component | File | Change |
|-----------|------|--------|
| `get_allowed_methods_for_model_class_field` | `settings_models.py` | Remove special-case `id → [AUTO]` rule |
| `FeatureManager.__init__` | `utils.py` | Add `existing_ids` param; seed `used_ids` |
| `FeatureManager.add_feature` | `utils.py` | Add `explicit_id` param; conflict check; update `used_ids` |
| `FeatureManager.create_new` | `utils.py` | Thread `explicit_id` through; return `None` on conflict |
| `SpatialProcessor.__init__` | `processors.py` | Pass `existing_ids` to `FeatureManager` |
| `resolve_id` (new helper) | `utils.py` or `processors.py` | Shared ID resolution + type conversion |
| `update_attributes` | `utils.py` | Skip `id` field unconditionally — always handled before `create_new` |
| `ConnectionNodeProcessor.process_feature` | `processors.py` | Use `resolve_id` + `explicit_id` |
| `PointProcessor.process_feature` | `processors.py` | Use `resolve_id` + `explicit_id` |
| `LineProcessor.process_feature` | `processors.py` | Use `resolve_id` + `explicit_id` |
| `CrossSectionLocationProcessor.process_feature` | `processors.py` | Use `resolve_id` + `explicit_id` |
| `SurfaceProcessor.process_feature` | `processors.py` | Use `resolve_id` + `explicit_id` |

## Constraint: `connection_node_fields` — `id` must remain AUTO

Connection nodes created during import can be shared by multiple source features (many-to-one). Allowing a custom ID for `connection_node_fields.id` would cause intra-batch conflicts and is architecturally unsound. The `fields` dict targeting a connection node as the primary model is unaffected — only `connection_node_fields` is restricted.

This is enforced at two layers:

### Layer 1 — UI: `FieldMapPage` for connection node fields

`FieldMapPage` gains an optional `restrict_id_to_auto: bool` parameter (default `False`). When `True`, the config class for the `"id"` row is overridden to allow only `[AUTO]`:

```python
if restrict_id_to_auto and field_name == "id":
    config_class = create_field_map_config([ColumnImportMethod.AUTO], field_type=int)
```

The wizard passes `restrict_id_to_auto=True` when creating the `connection_node_fields` page:

```python
FieldMapPage(model_cls=dm.ConnectionNode, name="connection_node_fields", restrict_id_to_auto=True)
```

### Layer 2 — Validation: `validate_field_map` for the processing path

`validate_field_map` gains an `allow_non_auto_id=True` parameter. When `False`, it rejects any `id` entry whose method is not AUTO (or absent):

```python
def validate_field_map(field_map, model_cls, allow_non_auto_id=True):
    if not allow_non_auto_id and "id" in field_map:
        cfg = field_map["id"]
        method = cfg.get("method") if isinstance(cfg, dict) else cfg.method
        if method not in (None, ColumnImportMethod.AUTO):
            raise ValueError(
                "The 'id' field in connection_node_fields must use AUTO method."
            )
    # ... existing logic unchanged ...
```

The processing algorithm passes `allow_non_auto_id=False` for `connection_node_fields`:

```python
validate_field_map(
    import_config.connection_node_fields,
    dm.ConnectionNode,
    allow_non_auto_id=False,
)
```

### Components added

| Component | File | Change |
|-----------|------|--------|
| `validate_field_map` | `settings_models.py` | Add `allow_non_auto_id` param |
| Processing call site | `processing/algorithms_vector_data_importer.py` | Pass `allow_non_auto_id=False` for cn fields |
| `FieldMapPage` | `wizard/pages.py` | Add `restrict_id_to_auto` param; override id row config |
| Wizard registration | `wizard/wizard.py` | Pass `restrict_id_to_auto=True` for cn fields page |

## Out of Scope

- `node_manager`, `surface_map_manager`, `integrate_manager`, `cross_section_manager` — always AUTO, not user-configurable
- UI changes beyond what flows automatically from the `allowed_methods` change
- Migrating existing saved import configs (AUTO remains default, so existing configs remain valid)

## Open Questions

- None — all decisions made during design conversation.
