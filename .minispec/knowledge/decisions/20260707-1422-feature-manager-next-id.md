# Decision: `FeatureManager.next_id` only advances for AUTO assignments

**Date**: 2026-07-07  
**Feature**: allow-custom-id-methods  
**Status**: Accepted

## Context

`FeatureManager` maintains a `next_id` counter used for AUTO ID assignment. When a custom (non-AUTO) ID is used, the question was whether `next_id` should still advance.

## Decision

`next_id` advances **only** when the manager performs an AUTO assignment. Custom IDs do not advance `next_id`.

## Reasoning

`next_id` represents the next available ID for AUTO assignment. Custom IDs are chosen by the user/expression and are independent of the AUTO counter. Advancing `next_id` for custom IDs would waste ID space unnecessarily and could cause confusing gaps. The `used_ids` set already handles collision avoidance for both AUTO and custom IDs: when AUTO eventually runs, it skips any IDs already in `used_ids` (including any custom IDs assigned earlier in the batch).
