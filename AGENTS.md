# AGENTS.md

## Project overview

QGIS plugin that lets users view and edit 1D/2D hydraulic model schematisations stored as GeoPackage (`.gpkg`) files. Developed by Nelen & Schuurmans under the "Rana" product brand.

- **Language:** Python (no type annotations used)
- **Framework:** QGIS Plugin API via `qgis.PyQt` (supports QGIS 3.28–3.99)
- **Entry point:** `threedi_schematisation_editor/__init__.py` exports `classFactory(iface)`
- **Main class:** `ThreediSchematisationEditorPlugin` (~470 lines)
- **Key dependency:** `threedi-schema` (data model, migrations, validation)

## Architecture

```
threedi_schematisation_editor/
  __init__.py              # classFactory(), plugin lifecycle (initGui/unload)
  data_models.py           # Dataclass definitions for all hydraulic objects (~1300 lines)
  enumerators.py           # IntEnum/StrEnum domain types
  user_layer_manager.py    # LayersManager – creates/manages QGIS vector layers (~700 lines)
  user_layer_handlers.py   # Signal-driven layer event handlers (~1460 lines)
  user_layer_forms.py      # Custom QGIS edit forms
  workspace.py             # WorkspaceContextManager – multiple open schematisations
  utils.py                 # Shared helpers (layers, type conversion, styles) (~1250 lines)
  validators.py            # Field and feature validation
  expressions.py           # Custom QGIS expressions
  communication.py         # UICommunication wrappers (message bar, dialogs)
  processing/              # QGIS Processing Framework algorithms
  forms/                   # UI form definitions
  load_schematisation/     # Load-schematisation dialog
  vector_data_importer/    # Wizard + importers/processors/integrators
  styles/                  # QML style files
tests/                     # pytest suite (mirrors plugin structure)
.github/workflows/         # CI: lint (ruff) + test (Docker)
Makefile                   # make zip | make test
Dockerfile                 # QGIS 3.34 test environment
```

### Layer management pattern

The plugin uses a signal-driven architecture for layer editing:

1. `LayersManager` creates layers grouped by type (1D, 2D, 1D2D, Settings) and maintains a `model_handlers` dict mapping model classes to handlers.
2. `UserLayerHandler` subclasses connect to QGIS signals (`editingStarted`, `beforeCommitChanges`, `featureAdded`, `featuresDeleted`, etc.).
3. **Multi-editing:** When a "1D group" layer starts editing, all related layers start editing together (multi-start, multi-commit, multi-rollback).
4. Validation runs via `VALIDATORS` on each handler with auto-fix capability.
5. `WorkspaceContextManager` tracks multiple simultaneously-loaded schematisations and the active one.

## Development workflow

**Run tests** (Docker required — QGIS bindings are not available on the host):
```bash
docker compose run qgis-desktop make test
# equivalent to: QT_QPA_PLATFORM=offscreen pytest --cov
```

**Build the zip:**
```bash
python3 zip_plugin.py
```

**Lint/format** (pre-commit, backed by ruff v0.14.4 — identical to CI):
```bash
pre-commit run --all-files
```

**Release:** Tag push triggers GitHub Actions → runs tests → `upload-artifact.sh` uploads zip to `artifacts.lizard.net`. Version is read from `metadata.txt`.

**No `pyproject.toml` or `setup.py`.** This is not a pip-installable package. It's a QGIS plugin distributed as a zip.

## Testing

- Framework: `pytest` with `pytest-cov` and `pytest-qt`
- All tests auto-use the `qgis_app_initialized` fixture (`tests/conftest.py`) which starts a headless `QgsApplication`.
- Test files mirror the plugin structure under `tests/`.
- Write tests for new business logic. Prefer integration-style tests that work through QGIS layer/feature APIs.

## Key conventions

1. **Data models** (`data_models.py`) use `dataclasses` with field metadata for display names, units, and allowed methods. Follow the existing pattern when adding new hydraulic object types.
2. **Enumerators** (`enumerators.py`) are `IntEnum` or `StrEnum`. Add new domain values here; do not hard-code magic numbers elsewhere.
3. **Communication** with users goes through `UICommunication` (`communication.py`); do not use bare `print` or `QMessageBox` outside that wrapper.
4. **Processing algorithms** must register with the QGIS processing registry pattern used in `processing/`.
5. **Styles** are QML files in `styles/`; update them when adding new layer types.
6. **Signal management:** Use the `connect_signal` / `disconnect_signal` helper utilities for safe signal connection/disconnection in handlers.

## Common pitfalls

- **Import from `qgis.PyQt`, never `PyQt5` directly.** The codebase uses `from qgis.PyQt.QtCore`, `from qgis.PyQt.QtWidgets`, etc. There are a few legacy `from PyQt5.QtCore import QVariant` usages in `vector_data_importer/processors.py` and some tests — do not propagate this pattern.
- **Version lives in two places:** `metadata.txt` (canonical, used by release tooling and QGIS) and `version.txt` (dev version string). They are not automatically kept in sync.
- **QGIS version compatibility:** The code has multiple `try/except AttributeError` blocks and `Qgis.QGIS_VERSION_INT` checks for API differences between QGIS versions. When using QGIS enums or newer API features, check how existing code handles version differences.
- **Module-level imports in `__init__.py`:** Heavy imports (e.g., `threedi_schema`, `threedi_mi_utils`) happen at module load time, after `check_dependency_loader()` runs. Be cautious adding new top-level imports that might fail if dependencies are missing.
- **`deploy.py` is Windows-only.** It hardcodes a Windows `AppData` path. On Linux, manually symlink or copy the plugin to `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`.
- **Tests cannot run on the host.** Always use `docker compose run qgis-desktop make test`. If you forget, imports of `qgis.*` will fail immediately.

## Out of scope

- Do not modify `symbology-style.db` or `user-history.db` directly.
- Do not change `version.txt` or `metadata.txt` unless explicitly asked to bump the version.
- Do not add secrets, credentials, or environment-specific paths to any committed file.
