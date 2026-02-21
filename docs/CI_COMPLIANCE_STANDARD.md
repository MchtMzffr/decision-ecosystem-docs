<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# CI Compliance Standard (INV-CI-COMPLY-1)

**Purpose:** Define the minimum set of CI steps and jobs that every repo must have so that **CI uyumu** (CI compliance) is measurable and enforceable. New cores and the docs repo must follow this standard.

**Scope:** Repo list and types are SSOT in **docs/REPO_REGISTRY.md** (INV-REPO-REG-1). Current set: 6 core + harness + docs; optional 9th = explainability-audit-core (experimental/unreleased).

**Hard prerequisite (INV-SYNC-1, INV-PUBLIC-MAIN-1, INV-CI-PASS-1):** Policy = **main’de kanıt** + CI pass. “Done” only when gates are present on **public** GitHub `main` and CI is green. Verify via `raw.githubusercontent.com` or `python tools/public_main_audit.py`; workspace-only state does not count. See §6.

---

## 1. Rule (INV-CI-COMPLY-1)

Every repo’s default CI workflow (e.g. `.github/workflows/ci.yml` or `docs_structure_guard.yml`) must include the steps listed below for its **repo type**. No step may be omitted without a documented exception or N/A condition (§2.4). Compliance is **enforced** by `tools/check_ci_compliance.py` (INV-CI-COMPLY-2).

**Metric:** For each repo, `ci_compliance_failures == 0` (all required steps present and passing). Produced by the compliance checker; see §7.

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
| 8b | INV-CI-BUILD-SMOKE-1 | INV-CI-BUILD-SMOKE-1a | Wheel smoke: `pip install dist/*.whl` then import smoke. **SMOKE_IMPORT SSOT:** per repo, set `env.SMOKE_IMPORT` to canonical import (see **docs/REPO_REGISTRY.md**) or use `tools/smoke_import.py`; step: `python -c "import importlib, os; importlib.import_module(os.environ['SMOKE_IMPORT'])"`. |
| 9 | Run tests | — | `pytest tests/ ...` with proof format per INV-CI-PROOF-STD-1. |
| 10 | Upload pytest report | INV-CI-PROOF-1, INV-CI-PROOF-STD-1 | Artifact name `pytest-report` or `pytest-report-<py>`; path/format per §2.5. |

Cores that depend on decision-schema must install it (e.g. pin `>=0.2.2,<0.3` + fallback **tag only**, no `@main`) before installing the package. See INV-CI-PIN-1, INV-CI-SCHEMA-FB-1.

### 2.2 Integration harness (decision-ecosystem-integration-harness)

Same as **2.1** (secret_scan, LICENSE, Ruff check, Ruff format check, Install harness, INV-BUILD-1, pytest with artifact). No PARAMETER_INDEX step. May have separate jobs (e.g. core_only + full_stack); each test job must run Ruff check and Ruff format check.

### 2.3 Docs repo (decision-ecosystem-docs)

| Order | Step / job | Description |
|-------|------------|-------------|
| 1 | **secret_scan** job | gitleaks/gitleaks-action@v2. |
| 2 | Ruff check | `ruff check .` — **conditional (INV-CI-SCOPE-1):** required only if `pyproject.toml` exists OR `tools/*.py` exists; else N/A. |
| 3 | Ruff format check | `ruff format --check .` — same condition as Ruff check. |
| 4 | Docs structure guard | `python .github/scripts/check_docs_root.py` (INV-DOC-*). |

No `python -m build` or pytest (docs repo is not a Python package).

### 2.4 N/A conditions (INV-CI-SCOPE-1) — mandatory unless N/A

All steps in §2.1–2.3 are **mandatory** for their repo type unless an **N/A condition** is documented and satisfied. No step may be omitted as "optional". **N/A rules:** (1) Docs repo Ruff check/format: N/A only when there is no `pyproject.toml` and no `tools/*.py` in the repo. (2) Any other N/A must be listed here with condition. **Metric:** `na_steps_without_condition == 0` (N/A only with explicit condition).

### 2.5 Proof artifact standard (INV-CI-PROOF-STD-1)

Single format to avoid drift and enable audit:

- **Command:** `pytest ... --json-report --json-report-file=pytest-report.json` (or `artifacts/pytest-report.json`). Alternative: `--junitxml=artifacts/junit.xml`.
- **Upload artifact name:** `pytest-report` or `pytest-report-<py>` (e.g. `pytest-report-3.11`). Path must be consistent (e.g. `pytest-report.json`).
- **Metric:** `missing_or_wrong_artifact_count == 0`.

### 2.6 SMOKE_IMPORT SSOT (INV-CI-BUILD-SMOKE-1a)

Per-repo wheel smoke import is defined in one place so CI does not hardcode module names and drift.

- **Option A (recommended):** In workflow, set `env: SMOKE_IMPORT: "<canonical_import>"` (e.g. `decision_schema`) at job or step level; smoke step: `pip install dist/*.whl && python -c "import importlib, os; importlib.import_module(os.environ['SMOKE_IMPORT'])"`.
- **Option B:** Repo has `tools/smoke_import.py` that performs the single import; CI runs `python tools/smoke_import.py` after `pip install dist/*.whl`.
- **Registry:** **docs/REPO_REGISTRY.md** lists `canonical_import` per repo; checker can validate workflow uses it. **Metric:** `missing_smoke_import == 0`.

---

## 3. Verification

- **Per repo:** Open the default workflow YAML and confirm each step in §2 is present. Run the workflow; all jobs must succeed.
- **Automated (mandatory for docs repo):** `tools/check_ci_compliance.py` runs in docs CI (INV-CI-COMPLY-2). For all repos locally: `python tools/check_ci_compliance.py --workspace <parent-of-all-repos>`. See §7.

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

### 5.1 Additional CI invariants (determinism, security, smoke)

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-CI-ACT-PIN-1** | GitHub Actions `uses:` must be pinned (tag or sha). No floating `@main` or unpinned. | `unpinned_actions_count == 0` |
| **INV-CI-PERM-1** | Default `permissions: { contents: read }`; widen only when necessary. | `overprivileged_workflows == 0` |
| **INV-CI-PY-1** | Core/harness CI: at least one fixed Python version (e.g. 3.11); matrix optional. | `python_version_unspecified == 0` |
| **INV-CI-BUILD-SMOKE-1** | After `python -m build`, smoke test: `pip install dist/*.whl` + minimal import. | `wheel_smoke_failures == 0` |
| **INV-CI-SCHEMA-FB-1** | decision-schema fallback **tag only** (`@vX.Y.Z`); no `@main`. | `schema_fallback_main_count == 0` |

**INV-CI-COMPLY-1:** Every repo’s CI workflow conforms to this standard (all required steps present and passing).

**INV-CI-COMPLY-2:** CI compliance checker runs in docs repo CI (and optionally locally with `--workspace`); fail-closed. **Metric:** `compliance_checker_pass == true`. See §7.

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

## 7. Compliance checker (INV-CI-COMPLY-2)

**Script:** `decision-ecosystem-docs/tools/check_ci_compliance.py`

- **Local (all repos):** `python tools/check_ci_compliance.py --workspace <parent-of-all-repos>` — checks each repo’s workflow(s) against required steps for its type; exit 1 if any missing.
- **Docs CI:** Run the same script (e.g. with `--workspace .` to check only docs repo, or with workspace root when multiple repos are checked out). Must pass for PR/merge.
- **Metric:** `compliance_checker_pass == true` (script exit 0).

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_INVARIANTS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, CORE_REPO_STANDARDS.md
