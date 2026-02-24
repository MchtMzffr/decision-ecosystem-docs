<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Documentation Standards — Naming and Format

**Purpose:** Single standard for documentation file naming so that tooling and humans can rely on a consistent format. Per ECOSYSTEM_GATES_AND_INVARIANTS.md §4 (Doc naming) and P1 patch plan.

---

## 1. File naming (normative)

**Rule:** Documentation filenames (e.g. in `docs/`, root, or any repo) use **SCREAMING_SNAKE_CASE** with **ASCII-only** characters and the `.md` extension.

| Requirement | Example | Not allowed |
|-------------|---------|-------------|
| Uppercase letters, digits, single underscore | `RELEASE_NOTES_0_2_2.md`, `ECOSYSTEM_GATES_AND_INVARIANTS.md` | `release-notes.md`, `ReleaseNotes.md` |
| ASCII only | `P2_STATUS_REPORT.md` | `Durum_Raporu.md` (non-ASCII), `P2-Durum.md` (hyphen) |
| Extension `.md` | `README.md` (root README may stay) | `.mdx` unless explicitly allowlisted |

**Metric:** `nonconforming_doc_filenames == 0`. Enforcement: CI script or manual checklist; new docs must follow this format.

**Exceptions:** Root `README.md` is kept as-is. Files under `archive/` may retain their original name when moved. Allowlist for other exceptions (e.g. `CHANGELOG.md`) may be defined in CI.

---

## 2. Language and content

- **Language:** All documentation content is in **English** (INV-DOC-LANG-2). See .cursor/rules/documentation-english.mdc.
- **Headers:** Each doc should have a short purpose line and, when relevant, "Last updated" and "References".

---

## 3. Relation to other invariants

| Invariant | Reference |
|-----------|-----------|
| INV-DOC-LANG-2 | All docs in English |
| Doc naming (SCREAMING_SNAKE_CASE) | This doc |
| INV-DOC-ROOT-ALLOWLIST-1 | Root allowlist in check_docs_root.py |

---

## 4. CURRENT vs ARCHIVE (INV-DOC-ACTIVE-1)

- **CURRENT docs** live under `docs/` (and root allowlist files). These are the live policy, guides, and checklists.
- **archive/YYYY-MM-DD/** is an immutable snapshot; do not edit archived files. Historical reports and one-off session output go here.
- **README link policy:** The main index ("Current documentation" / "Quick links") must link only to CURRENT set (root allowlist + `docs/`). Links to `archive/` belong in a separate **Archive (historical)** section so readers know what is current vs historical.

---

**Last updated:** 2026-02  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md §4, §14 P1
