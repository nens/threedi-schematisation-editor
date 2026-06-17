# Rana Schematisation Editor Constitution

## Core Principles

### I. Stability

Code must not break. Remain consistent with existing patterns and conventions unless the current code is clearly bad and requires improvement. Changes should be predictable and safe.

### II. Test Meaningful Behavior

New code must be tested, focusing on meaningful behavior rather than coverage targets. Integration-style tests through QGIS layer/feature APIs are preferred. Bug fixes to existing untested code do not require new tests.

A test has value only if it would catch a real regression. Do not write tests that merely assert a function returns a non-empty dict, that a specific key exists, or that no exception is raised in a trivially safe code path. Before adding a test, ask: "what bug would this catch?" If the answer is "nothing realistic", skip it.

### III. Documentation

No API docs or excessive docstrings. Inline docstrings only when code is not self-explanatory. Design docs (e.g. DESIGN.md files) must be kept up to date when working on features that have them.

### IV. Focused Changes

Only touch what is needed for the task at hand. No opportunistic refactoring. Refactoring is done in dedicated tasks, not as a side effect.

### V. Follow Existing Conventions

Follow the patterns and conventions established in the codebase and documented in AGENTS.md. This includes: imports from `qgis.PyQt`, communication via `UICommunication`, domain values in `enumerators.py`, dataclass patterns in `data_models.py`, and signal management via helpers.

## Technology Stack

- Python (no type annotations)
- QGIS Plugin API via `qgis.PyQt` (QGIS 3.28-3.99)
- `threedi-schema` for data model, migrations, validation
- pydantic for settings/configuration models
- pytest (Docker-only, QGIS 3.34 container)
- ruff for formatting and import sorting (via pre-commit)

## Development Workflow

- Lint/format: `pre-commit run --all-files`
- Tests: `docker compose run qgis-desktop make test`
- CI enforces both on every PR
- No tests on the host (QGIS bindings unavailable)
- **Run `pre-commit run --all-files` before every commit.** Fix any issues before committing.

## Git Workflow

### Branch naming

- `feat_<ticket>_<short-description>` for new features
- `fix_<ticket>_<short-description>` for bug fixes
- Example: `feat_449_unify_vdi_validation`

### Branch creation rules

- **Always ask before creating a branch.**
- If a ticket number is provided and it already appears in the current branch name, assume that branch is the one to use — do not create a new one.
- Never rename an existing branch.

---

## MiniSpec Preferences

### Review Chunk Size

medium

### Documentation Review Policy

trust-ai

### Autonomy Level

always-confirm

### Design Evolution Handling

always-discuss

### Walkthrough Depth

standard

---

## Governance

Constitution supersedes default AI behavior. Principles can be adjusted through discussion. MiniSpec preferences can be changed per-session if needed.

**Version**: 1.1.0 | **Ratified**: 2026-06-16 | **Last Amended**: 2026-06-16
