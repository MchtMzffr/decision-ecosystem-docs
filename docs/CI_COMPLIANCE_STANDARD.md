<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# CI Compliance Standard (INV-CI-COMPLY-1)

**Purpose:** Define the minimum set of CI steps and jobs that every repo must have so that **CI uyumu** (CI compliance) is measurable and enforceable. New cores and the docs repo must follow this standard.

**Scope:** All 8 repos (decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, decision-ecosystem-integration-harness, decision-ecosystem-docs).

---

## 1. Rule (INV-CI-COMPLY-1)

Every repo’s default CI workflow (e.g. `.github/workflows/ci.yml` or `docs_structure_guard.yml`) must include the steps listed below for its **repo type**. No step may be omitted without a documented exception (e.g. docs repo has no `python -m build`).

**Metric:** For each repo, `ci_compliance_failures == 0` (all required steps present and passing).

---

## 2. Required CI steps by repo type

### 2.1 Core repos (decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core)

| Order | Step / job | Invariant / gate | Description |
|-------|------------|------------------|--------------|
| 1 | **secret_scan** job | INV-SEC-RED-1 | gitleaks/gitleaks-action@v2; `fetch-depth: 0`. |
| 2 | Check LICENSE | INV-LIC-1 | `test -f LICENSE` (or equivalent). |
| 3 | Set up Python | — | Matrix: 3.11, 3.12 (or current supported). |
| 4 | Ruff check | INV-LINT-1 | `ruff check .` (exit 0). |
| 5 | Ruff format check | INV-LINT-1 | `ruff format --check .` (exit 0). |
| 6 | Install package | — | `pip install -e .` or `pip install -e ".[dev]"`. |
| 7 | **(decision-schema only)** INV-PARAM-INDEX-1 | INV-PARAM-INDEX-1 | `python tools/check_parameter_index.py` (exit 0). |
| 8 | INV-BUILD-1 | INV-BUILD-1 | `python -m build` (exit 0). |
| 9 | Run tests | — | `pytest tests/ ...` with `--json-report` (INV-CI-PROOF-1). |
| 10 | Upload pytest report | INV-CI-PROOF-1 | Artifact `pytest-report-<py>`. |

Cores that depend on decision-schema must install it (e.g. pin `>=0.2.2,<0.3` + fallback tag) before installing the package. See INV-CI-PIN-1.

### 2.2 Integration harness (decision-ecosystem-integration-harness)

Same as **2.1** (secret_scan, LICENSE, Ruff check, Ruff format check, Install harness, INV-BUILD-1, pytest with artifact). No PARAMETER_INDEX step. May have separate jobs (e.g. core_only + full_stack); each test job must run Ruff check and Ruff format check.

### 2.3 Docs repo (decision-ecosystem-docs)

| Order | Step / job | Description |
|-------|------------|-------------|
| 1 | **secret_scan** job | gitleaks/gitleaks-action@v2. |
| 2 | Ruff check | `ruff check .`. |
| 3 | Ruff format check | `ruff format --check .`. |
| 4 | Docs structure guard | `python .github/scripts/check_docs_root.py` (INV-DOC-*). |

No `python -m build` or pytest (docs repo is not a Python package).

---

## 3. Verification

- **Per repo:** Open the default workflow YAML and confirm each step in §2 is present. Run the workflow; all jobs must succeed.
- **Automated (optional):** A script could grep for `ruff check`, `ruff format --check`, `gitleaks`, `python -m build`, `pytest` in `.github/workflows/*.yml` and report missing steps per repo.

---

## 4. New cores

When adding a **new** core repo, copy the CI workflow from an existing core (e.g. decision-schema or execution-orchestration-core) and adjust only: package name, install command, and (if needed) decision-schema fallback. Do **not** remove secret_scan, Ruff, build, or pytest steps.

---

## 5. Relation to other invariants

| Invariant | CI compliance |
|-----------|----------------|
| INV-LIC-1 | Enforced by “Check LICENSE” step. |
| INV-SEC-RED-1 | Enforced by secret_scan job. |
| INV-LINT-1 | Enforced by Ruff check + Ruff format check. |
| INV-BUILD-1 | Enforced by `python -m build` step. |
| INV-CI-PROOF-1 | Enforced by pytest + upload artifact. |
| INV-PARAM-INDEX-1 | Enforced by check_parameter_index.py (decision-schema only). |

**INV-CI-COMPLY-1:** Every repo’s CI workflow conforms to this standard (all required steps present and passing).

---

## 6. Fail-closed verification: “Done” only with proof on main (INV-SYNC-1)

**INV-SYNC-1:** “Workspace’te var” ≠ “main’de var”. For governance, **DONE** = proof on **GitHub `main`** + CI gate passing. Local or unmerged changes do not count.

### 6.1 Done formula (single metric)

A task is **done** only when all three hold:

| Symbol | Meaning | How to verify |
|--------|--------|----------------|
| **Gates_present** | Required CI steps exist in the workflow file on **main**. | Grep/inspect `origin/main` (e.g. `raw.githubusercontent.com/.../main/.github/workflows/ci.yml`) for step names. |
| **CI_pass** | Latest CI run on **main** for that workflow is **PASS**. | GitHub Actions: last run green. |
| **Main_parity** | No uncommitted or unpushed changes; repo not ahead of `origin/main`. | `git status --porcelain` empty; `git log origin/main..HEAD` empty. |

**Done = (Gates_present = 1) ∧ (CI_pass = 1) ∧ (Main_parity = 1)**

### 6.2 Hard checklist (fail-closed)

Before claiming “CI gates are in place”:

- **(A) Gate present on main:** decision-schema CI shows `check_parameter_index` and `python -m build`; every core/harness CI shows `python -m build`. Verify by fetching the workflow file from **main** (e.g. raw GitHub URL).
- **(B) Nondeterminism 0:** No `@main` in decision-schema fallback; use tag (e.g. `@v0.2.2`).
- **(C) Tag CI:** Workflows have `on.push.tags: ["v*"]` (INV-CI-TAG-1).

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_INVARIANTS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, CORE_REPO_STANDARDS.md
