# Decision: Allowed methods for the `id` field

**Date**: 2026-07-07  
**Feature**: allow-custom-id-methods  
**Status**: Accepted

## Context

The `id` field previously allowed only `AUTO`. The feature requires allowing additional methods. The question was whether to allow all non-IGNORE methods (AUTO, ATTRIBUTE, EXPRESSION, DEFAULT) or only a subset controlled by per-model metadata.

## Options Considered

**Option A — All methods except IGNORE:**  
Remove the special-case rule in `get_allowed_methods_for_model_class_field` that forces `[AUTO]` for `id` fields. The existing IGNORE-removal logic (for non-optional fields) already excludes IGNORE. Result: AUTO, ATTRIBUTE, EXPRESSION, DEFAULT all allowed. AUTO remains the default (first in enum order).

- ✅ Simple — one line removed
- ✅ Consistent with how all other required fields work
- ✅ AUTO stays default without extra machinery

**Option B — Per-model `allowed_methods` metadata on the `id` field:**  
Annotate specific data model `id` fields with `allowed_methods` metadata to control the set per model.

- ✅ Fine-grained control if different models need different rules
- ❌ More boilerplate — every data model's `id` field needs annotation
- ❌ Over-engineered for a case where all models want the same behaviour

## Decision

**Option A** was chosen.

## Reasoning

There is no current requirement for different models to have different allowed methods for `id`. The simpler approach removes one special-case rule and relies on the already-correct general logic. Per-model metadata can be added later if a specific model needs tighter constraints.
