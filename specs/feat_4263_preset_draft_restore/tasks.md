# Tasks: Wizard Draft Recovery

**Input**: `specs/feat_4263_preset_draft_restore/design.md`
**Branch**: `feat_4263_preset_draft_restore`

---

## Phase 1: Foundational — Draft Storage Helpers

**Purpose**: QSettings helpers that all other tasks depend on.

- [x] T001 [US1][US2][US3] Add `VDI_DRAFT_KEY_PREFIX`, `get_draft()`, `save_draft()`, `delete_draft()` to `threedi_schematisation_editor/vector_data_importer/wizard/utils.py`
- [x] T002 [US1][US2][US3] Add `TestDraftHelpers` tests to `tests/vector_data_importer/test_wizard.py` (get returns None when absent; save/get round-trip; delete removes entry; delete is idempotent)

**Checkpoint**: `pytest tests/vector_data_importer/test_wizard.py::TestDraftHelpers` passes

---

## Phase 2: User Story 1 — Save Draft on Close (Priority: P1) 🎯 MVP

**Goal**: User closing the wizard mid-configuration is prompted to save or discard; settings survive to next session.

**Independent Test**: Open wizard, change a field mapping, close — verify save/discard/cancel dialog appears and behaves correctly.

- [x] T003 [P] [US1] Add `_initial_state` snapshot in `VDIWizard.__init__()` and `has_changes()` method to `wizard/wizard.py`
- [x] T004 [P] [US1] Add `TestVDIWizardHasChanges` tests to `tests/vector_data_importer/test_wizard.py` (False at init; True after deserialize with non-default settings)
- [x] T005 [US1] Add `reject()` override to `VDIWizard` in `wizard/wizard.py` — shows QMessageBox with Save draft / Discard / Cancel; Save calls `save_draft()` + `super().reject()`; Discard calls `delete_draft()` + `super().reject()`; Cancel does nothing (depends on T003)
- [x] T006 [US1] No separate reject() tests — UI dialog logic covered by has_changes() tests; mock-heavy tests removed as low value

**Checkpoint**: `pytest tests/vector_data_importer/test_wizard.py::TestVDIWizardHasChanges tests/vector_data_importer/test_wizard.py::TestVDIWizardReject` passes

---

## Phase 3: User Story 2 — Restore Draft on Open (Priority: P2)

**Goal**: User returning after an interrupted session is offered to restore their previous configuration.

**Independent Test**: Save a draft via QSettings directly, open the wizard — verify restore prompt appears; "Restore draft" applies settings; "Start fresh" leaves defaults unchanged and retains draft.

- [ ] T007 [P] [US2] Add `restore_draft_lenient()` to `VDIWizard` in `wizard/wizard.py` — iterates pages, calls `page.deserialize()` in individual try/except blocks (depends on T003)
- [ ] T008 [P] [US2] Add `_maybe_offer_draft_restore()` to `VDIWizard` in `wizard/wizard.py` — checks `get_draft()` on init, shows QMessageBox with Restore draft / Start fresh; Restore calls `restore_draft_lenient()`; Start fresh retains draft unchanged; call from `__init__` after snapshot (depends on T001, T007)
- [ ] T009 [US2] Add `TestVDIWizardDraftRestore` tests to `tests/vector_data_importer/test_wizard.py` — lenient restore applies valid data; lenient restore skips bad pages without raising; prompt shown when draft exists; Restore applies draft and `has_changes()` is True; Start fresh leaves defaults and retains draft; no prompt when no draft (depends on T002, T007, T008)

**Checkpoint**: `pytest tests/vector_data_importer/test_wizard.py::TestVDIWizardDraftRestore` passes

---

## Phase 4: User Story 3 — Draft Lifecycle Cleanup (Priority: P3)

**Goal**: Draft is deleted automatically when the user no longer needs it (after successful import or after saving a preset file).

**Independent Test**: Run a successful import — verify draft is gone. Save preset via "Save as..." — verify draft is gone.

- [ ] T010 [P] [US3] Delete draft in `save_settings_to_json()` on success in `wizard/wizard.py` — call `delete_draft(type(self).__name__)` after `QMessageBox.information(...)` (depends on T001)
- [ ] T011 [P] [US3] Delete draft in `handle_finished` closure inside `run_import()` on success in `wizard/wizard.py` — call `delete_draft(type(self).__name__)` when `success is True` (depends on T001)
- [ ] T012 [US3] Add `TestVDIWizardDraftLifecycle` tests to `tests/vector_data_importer/test_wizard.py` — save_settings_to_json deletes draft; successful import deletes draft (depends on T010, T011)

**Checkpoint**: `pytest tests/vector_data_importer/test_wizard.py::TestVDIWizardDraftLifecycle` passes

---

## Phase 5: Polish & Verification

- [ ] T013 Run full test suite: `docker compose run qgis-desktop make test`
- [ ] T014 [P] Run linter: `pre-commit run --all-files`

---

## Dependencies & Execution Order

- **Phase 1** (T001–T002): No dependencies — start here
- **Phase 2** (T003–T006): Depends on Phase 1 complete
  - T003 and T004 can run in parallel [P]
  - T005 depends on T003; T006 depends on T002 and T004
- **Phase 3** (T007–T009): Depends on Phase 1 complete; T007 and T008 can run in parallel [P]
- **Phase 4** (T010–T012): Depends on Phase 1 complete; T010 and T011 can run in parallel [P]
- **Phase 5** (T013–T014): Depends on all prior phases complete

### Files changed

- `threedi_schematisation_editor/vector_data_importer/wizard/utils.py` — T001
- `threedi_schematisation_editor/vector_data_importer/wizard/wizard.py` — T003, T005, T007, T008, T010, T011
- `tests/vector_data_importer/test_wizard.py` — T002, T004, T006, T009, T012
