<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Deprecation Policy (INV-DEPREC-1)

**Purpose:** Single source of truth for how deprecated fields and APIs are documented and removed. Ensures SemVer and compatibility are predictable.

---

## 1. Rule (INV-DEPREC-1)

Every deprecated field or API must have:

| Element | Where | Requirement |
|---------|--------|-------------|
| **deprecated_in** | SSOT doc (this policy or release notes) | Version in which the item was first marked deprecated. |
| **remove_in** | SSOT doc | Version (or date) when the item will be removed. |
| **migration_note** | SSOT doc | How to migrate (e.g. use replacement X instead). |

**Metric:** `deprecated_without_timeline == 0` (no deprecated item may lack these three in the SSOT).

---

## 2. Where to document

- **Ecosystem-wide:** This doc or a table in `ECOSYSTEM_CONTRACT_MATRIX.md` / release notes.
- **Per repo:** Release notes (e.g. `docs/RELEASE_NOTES_*.md`) must have a **Deprecated** subsection when something is deprecated in that release.
- **Code:** Emit `DeprecationWarning` when deprecated API is used (with message pointing to migration note).

---

## 3. Lifecycle

1. **Deprecate:** In release N, add to SSOT: `deprecated_in: N`, `remove_in: N+2` (or next major), `migration_note: ...`. Add DeprecationWarning in code. Add **Deprecated** subsection in that release’s notes.
2. **Support window:** At least one minor (or one major) version where the deprecated item still works but warns.
3. **Remove:** In release `remove_in`, remove the field/API and update SSOT. Bump version per INV-SEMVER-1 (major if breaking).

---

## 4. Relation to SemVer (INV-SEMVER-1)

- **Breaking change** (e.g. removal of deprecated API at `remove_in`) → **major** version bump.
- **Deprecation only** (add DeprecationWarning, no removal) → **minor** version bump is acceptable; document in release notes **Compatibility** and **Deprecated**.

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md (J. SemVer / deprecation), RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
