# Ecosystem Invariants — Decision Ecosystem

**Purpose:** Single checklist for repo-surface static analysis. Source of truth: GitHub `main`.  
**Use:** Verify these before release; drift = roadmap/CI/license mismatches.

---

## Contract & dependencies

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-CORE-DEP-1** | Core repos depend **only** on `decision-schema` (no core↔core). | `core_to_core_dep_count == 0` (pyproject) |

---

## CI determinism

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-CI-PIN-1** | CI installs `decision-schema` with range `>=0.2.2,<0.3` and fallback tag `@v0.2.2`. | Workflow files match per repo. |
| **INV-CI-NONDET-0** | CI fallback must not use `@main` when a release tag exists. | `@main` only in allowlist (e.g. unreleased dmc until v0.1.0). |
| **INV-CI-TAG-1** | Tag push triggers CI (`on.push.tags: ["v*"]`). | Run count ≥ 1 after tag push. |
| **INV-CI-PROOF-1** | CI produces machine-readable proof artifact (`pytest-report-<py>` with JSON). | Artifact downloadable, JSON parseable. |

Branch/CI policy details: **BRANCH_GOVERNANCE.md** (INV-BRANCH-1, INV-BRANCH-2, INV-GOV-1, INV-GOV-2).

---

## Docs & drift

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-DOC-DRIFT-1** | Docs roadmap table matches `pyproject.version` and Git tags. | `roadmap_mismatch_rows == 0` in NEXT_STEPS_ROADMAP.md. Run: `python tools/check_release_alignment.py --workspace <parent-of-docs>` from docs repo. |

---

## License / IP

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-LIC-1** | Every repo root has a `LICENSE` file (MIT text). | `license_missing_count == 0`. |
| **INV-README-LIC-1** | README has no placeholder like `[Add your license]`. | `count(placeholder) == 0`. |

CI can enforce INV-LIC-1 with a step: `test -f LICENSE`.

---

## Repo hygiene (all cores, including new)

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-GITIGNORE-1** | `.gitignore` must include `__pycache__/`, `.pytest_cache/`, build/dist, venv, secrets/env; no such file may be tracked. | No `__pycache__/` or `.pytest_cache/` in `git status` as tracked; run `git rm --cached` if ever committed. |

Details and required patterns: **docs/CORE_REPO_STANDARDS.md**. Applies to every core (existing and newly added).

---

## Release notes

See **docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md** for INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1, INV-REL-PROOF-1, INV-CI-TAG-1, INV-CI-PROOF-1.

---

**Last updated:** 2026-02-19  
**Status:** Checklist for static analysis and score (contract, CI, docs, license).
