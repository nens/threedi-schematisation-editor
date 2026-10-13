# Project Constitution

**Version**: 1.0.0  
**Created**: 2026-06-22  
**Project**: threedi-schematisation-editor (Rana QGIS Plugin)

---

## Principles

### 1. Stability — MUST
Do not break existing functionality. Changes must be minimal and close to the
existing code. When in doubt, match the current implementation rather than
improving it.

### 2. Consistency — MUST
New code must be consistent with the current state of the codebase: same patterns,
same idioms, same style. Readability, simplicity, and test coverage improvements
are welcome but must not diverge from existing conventions.

---

## MiniSpec Preferences

### Chunk Size
**Medium** — 40–80 lines per review chunk. Matches the existing file sizes in
this codebase.

### Autonomy
**Always confirm** — Pause after every chunk for explicit approval before
continuing to the next step.

### Documentation Review
**Trust-AI** — Update minispec knowledge files (patterns, modules, conventions)
silently. Flag architectural decisions for review before saving.

### Design Evolution
**Flag and continue** — For minor deviations, flag and continue. For major
deviations from the design, stop and discuss.

---

## Complexity Tolerance

### Change Size
**Minimal first** — Show the smallest change that satisfies the task's acceptance
criteria. Offer the thorough version after. Do not add error handling, tests, or
configurability beyond what the task asks for.

### Abstraction Threshold
**Conservative** — Only extract a helper, module, or utility when the pattern
already exists in the codebase or the code is duplicated 3+ times. Do not
introduce new abstractions for cleanliness alone.

### Review Findings
**Triage first** — When a code review tool flags an issue, present it with three
options (fix / decline / defer) before writing any code.

### Deletion Permission
**Only if related** — Propose removing code only when directly related to the
current task (e.g. an import that becomes unused by this change). Do not flag
unrelated dead code during feature work.
