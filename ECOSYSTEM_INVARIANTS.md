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
| **INV-CI-COMPLY-1** | Every repo’s CI workflow conforms to the **CI Compliance Standard** (secret_scan, LICENSE, Ruff check, Ruff format check, build, pytest, artifact per repo type). | All required steps present and passing. See **docs/CI_COMPLIANCE_STANDARD.md**. |
| **INV-CI-COMPLY-2** | CI compliance checker runs in docs repo CI (and optionally with `--workspace`); fail-closed. | compliance_checker_pass == true. See **docs/CI_COMPLIANCE_STANDARD.md** §7. |
| **INV-SYNC-1** | “Workspace’te var” ≠ “main’de var”. **DONE** = proof on GitHub `main` + CI gate passing. | Done = Gates_present ∧ Main_parity. See **docs/CI_COMPLIANCE_STANDARD.md** §6. |
| **INV-CI-SCOPE-1** | Repo-type steps may be N/A only with documented condition (e.g. Docs Ruff when no pyproject/tools/*.py). | na_steps_without_condition == 0. |
| **INV-CI-PROOF-STD-1** | Proof artifact path and name fixed (e.g. pytest-report.json, artifact name pytest-report or pytest-report-<py>). | missing_or_wrong_artifact_count == 0. |
| **INV-CI-ACT-PIN-1** | GitHub Actions `uses:` pinned (tag or sha). | unpinned_actions_count == 0. |
| **INV-CI-PERM-1** | Default `permissions: { contents: read }`. | overprivileged_workflows == 0. |
| **INV-CI-PY-1** | Core/harness CI: at least one fixed Python version (e.g. 3.11). | python_version_unspecified == 0. |
| **INV-CI-BUILD-SMOKE-1** | After build: pip install dist/*.whl + minimal import smoke. | wheel_smoke_failures == 0. |
| **INV-CI-SCHEMA-FB-1** | decision-schema fallback tag only (@vX.Y.Z); no @main. | schema_fallback_main_count == 0. |

Branch/CI policy details: **BRANCH_GOVERNANCE.md** (INV-BRANCH-1, INV-BRANCH-2, INV-GOV-1, INV-GOV-2). **CI uyum standardı:** **docs/CI_COMPLIANCE_STANDARD.md**.

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
| **INV-COMMIT-1** | Intended changes are committed and pushed; no repo left with uncommitted tracked changes or ahead of origin/main. | `git status --porcelain` empty; `git log origin/main..HEAD` empty. See **docs/CORE_REPO_STANDARDS.md** §2. |

Full gates (H–L, metrics, remediation): **docs/ECOSYSTEM_GATES_AND_INVARIANTS.md**. Details and checklist: **docs/CORE_REPO_STANDARDS.md**. Applies to every core (existing and newly added).

---

## Release notes

See **docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md** for INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1, INV-REL-PROOF-1, INV-CI-TAG-1, INV-CI-PROOF-1.

---

**Last updated:** 2026-02-19  
**Status:** Checklist for static analysis and score (contract, CI, docs, license).
