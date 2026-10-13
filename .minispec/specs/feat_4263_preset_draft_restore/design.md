# Wizard Draft Recovery Design

**Date:** 2026-06-17
**Status:** Approved

## Overview

When a user closes the vector data importer wizard mid-configuration, their settings are lost. This design adds two things: (1) a **"Save draft" path** so the user can explicitly save before leaving, and (2) an **unsaved-changes confirmation dialog** when closing without saving, matching the familiar "unsaved document" UX pattern. On next open of the same wizard type, the system offers to restore the draft.

The existing explicit "Load preset" / "Save as..." mechanism is not changed. Draft recovery is a separate, more lenient path.

---

## User Stories

- As a user who is interrupted while configuring an import, I want to be prompted to save my settings when I close the wizard, so I don't lose my work.
- As a user returning to the wizard after a previous interrupted session, I want to be offered the option to restore my previous configuration, so I can continue where I left off.
- As a user who deliberately discards settings, I want to be able to start fresh without being forced to restore a draft.

---

## Components

### 1. Close Confirmation Dialog

When the user clicks "Close" (or presses Escape, or clicks the window X) **and the current state differs from the initial defaults**, a dialog appears:

> **"You have unsaved import settings."**
> [Save draft] [Discard] [Cancel]

- **Save draft** -- serializes current state to `QSettings` and closes the wizard.
- **Discard** -- closes without saving. Any existing draft for this wizard type is **deleted**.
- **Cancel** -- returns the user to the wizard unchanged.

"Has changes" is detected by comparing the serialized state at close time against a snapshot taken when the wizard first opened (i.e., the default/empty state).

The dialog is shown by overriding `reject()` on `VDIWizard`.

### 2. Draft Storage

Drafts are stored as **JSON files** in a dedicated folder inside the active QGIS profile directory:

```
<qgisSettingsDirPath()>/threedi_vdi_drafts/ImportConnectionNodesWizard.json
<qgisSettingsDirPath()>/threedi_vdi_drafts/ImportConduitWizard.json
<qgisSettingsDirPath()>/threedi_vdi_drafts/ImportStructureWizard.json
...
```

`qgisSettingsDirPath()` is `QgsApplication.qgisSettingsDirPath()` — the root of the active QGIS user profile (e.g. `~/.local/share/QGIS/QGIS3/profiles/default/` on Linux). One JSON file per wizard type; saving a draft overwrites the previous file for that type.

Rationale for a profile folder over `QSettings`:
- Keeps the `QGIS3.ini` file clean — embedding multiple JSON blobs in an INI file is messy and hard to read.
- Files are individually visible, human-readable, and recoverable outside QGIS.
- Consistent with how the sister plugin (`threedi_models_and_simulations`) stores its log file under `qgisSettingsDirPath()`.
- Survives QGIS restarts, which is precisely the recovery scenario.

The folder is created on first write if it does not exist.

New helpers added to `vector_data_importer/wizard/utils.py` (alongside `get_last_config_dir` / `update_last_config_dir`):

```python
def get_draft(wizard_class_name: str) -> Optional[dict]
def save_draft(wizard_class_name: str, data: dict) -> None
def delete_draft(wizard_class_name: str) -> None
```

Internally these helpers use `QgsApplication.qgisSettingsDirPath()` to locate the `threedi_vdi_drafts/` folder.

### 3. Draft Restore on Open

When a wizard opens and a draft exists for its class name, it shows a prompt (before the wizard pages are shown, or on the StartPage):

> **"A previous draft was found for this import type."**
> [Restore draft] [Start fresh]

- **Restore draft** -- applies the draft via the lenient deserialization path (see Section 4).
- **Start fresh** -- ignores the draft. The draft is **not deleted** at this point; it can be restored later in the same session if the user changes their mind.

### 4. Two Deserialization Paths

| | Explicit "Load preset" | Draft restore |
|---|---|---|
| Entry point | "Choose file..." button on StartPage | "Restore draft" prompt on wizard open |
| Validation | Strict: `ImportSettings(**data)` -- rejects on any pydantic error | Lenient: per-page `try/except`, apply what works |
| Incomplete data | Error dialog shown, nothing applied | Normal -- missing pages filled with defaults |
| On failure | Nothing applied, error dialog shown | Partially applied, no error dialog |
| Source attribute mismatch | Caught by pydantic or silent fallback | Silent fallback via existing `update_layer()` |

A new method `restore_draft_lenient(data: dict)` is added to `VDIWizard`. It iterates all pages and calls each page's `deserialize()` inside an individual `try/except`, so one failing page does not block others. The existing `load_settings_from_json()` and `deserialize()` methods are unchanged.

### 5. Draft Lifecycle

| Event | Effect on draft |
|---|---|
| User clicks "Save draft" in close dialog | Draft saved for this wizard type; wizard closes |
| User clicks "Discard" in close dialog | Draft deleted for this wizard type; wizard closes |
| User clicks "Cancel" in close dialog | Wizard stays open; no change to draft |
| User opens wizard, chooses "Start fresh" | Draft retained (can be restored later in same session) |
| User opens wizard, chooses "Restore draft" | Draft applied; draft retained until cleared |
| User completes successful import **and closes the wizard** | Draft deleted for this wizard type |
| User saves preset via "Save as..." | Draft deleted for this wizard type (they have a proper file now) |

---

## Data Model

The draft file contains the JSON-serialised output of `VDIWizard.get_settings().model_dump()`, identical in schema to the existing preset JSON files saved via "Save as...". No new schema is introduced.

---

## Out of Scope

- No draft scoping by source layer or schematisation (per wizard type only).
- No draft expiry or age limit.
- No "recent drafts" list or draft management UI.
- Scenarios 2 (re-run with tweaked settings) and 3 (preset reuse) remain served by the existing JSON save/load mechanism, which is not changed.

---

## Open Questions

None. All decisions were made during design.
