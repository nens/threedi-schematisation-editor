# Decision: ID resolution happens before feature creation (fail fast)

**Date**: 2026-07-07  
**Feature**: allow-custom-id-methods  
**Status**: Accepted

## Context

When a non-AUTO method is used for `id`, the resolved value must be checked for conflicts. The question was *when* in the processing pipeline to do this check.

## Options Considered

**Option A — Resolve before `create_new` (fail fast):**  
Resolve the `id` value via `get_field_config_value`, check against `used_ids`, and only then call `target_manager.create_new(...)`. If there is a conflict, `return {}` before the feature object is ever built.

- ✅ No wasted work — the feature is never created if it will be discarded
- ✅ Clean call site — `create_new` returns a feature or `None`
- ✅ The conflict check naturally lives in `FeatureManager` close to the ID assignment

**Option B — Resolve inside `update_attributes`, check after feature is built:**  
Let `update_attributes` set the `id` like any other field, then check for conflicts afterwards and discard the feature.

- ❌ Feature object is fully built and then thrown away
- ❌ `update_attributes` currently has no mechanism to signal "skip this feature"
- ❌ Separation of concerns is muddier

## Decision

**Option A** was chosen.

## Reasoning

Failing fast before creating the feature is cleaner and avoids any side effects from building a feature that will be discarded. A small shared helper (`resolve_id`) is extracted to avoid repeating the resolution + conversion + null-check logic across all five processor call sites.
