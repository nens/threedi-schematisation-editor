# Decision: ID conflict scope includes in-batch assignments

**Date**: 2026-07-07  
**Feature**: allow-custom-id-methods  
**Status**: Accepted

## Context

When a user imports features with a non-AUTO `id` method, the system must detect conflicts with existing IDs. The question was whether to check only IDs already in the target layer at import start, or also IDs assigned to earlier features in the same import batch.

## Options Considered

**Option A — Narrow:** Check only IDs present in the target layer at import start.

- ✅ Simple — just read `layer.uniqueValues(id_idx)` once
- ❌ Two source features with the same ID would both be "accepted" and one would silently overwrite the other in the layer

**Option B — Broad:** Check IDs in the target layer at start *plus* IDs already assigned during the current import pass.

- ✅ Prevents intra-batch duplicates (two source features with the same custom ID)
- ✅ Consistent — the final layer will never contain duplicate IDs
- ✅ Implemented naturally by maintaining a `used_ids` set in `FeatureManager` that grows as IDs are assigned

## Decision

**Option B (broad)** was chosen.

## Reasoning

The goal of conflict detection is to ensure the final imported layer has no duplicate `id` values. Checking only the pre-import state would miss the case where two source features share the same custom ID. The `FeatureManager` already owns ID state, making it the natural place to track both pre-existing and newly assigned IDs via a `used_ids` set seeded at construction.
