<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Core Repo Standards — All Cores (Including Newly Added)

**Purpose:** Single set of rules that apply to **every** core repo in the Decision Ecosystem. New cores must follow the same standards from day one.

**Scope:** decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, decision-ecosystem-integration-harness, and any future core.

---

## 1. INV-GITIGNORE-1: Never Commit Build/Cache/Secrets

**Rule:** Every core repo **must** have a root `.gitignore` that includes the following patterns so these paths are **never** committed or pushed.

### 1.1 Required patterns (minimum)

| Category | Patterns | Reason |
|----------|----------|--------|
| Bytecode / cache | `__pycache__/`, `*.py[cod]`, `*.pyo`, `.pytest_cache/`, `.ruff_cache/` | Generated; not source; platform-dependent. |
| Build / dist | `build/`, `dist/`, `*.egg-info/`, `*.egg` | Build artifacts. |
| Virtual env | `.venv/`, `venv/`, `env/` | Local environment. |
| IDE / OS | `.idea/`, `.vscode/`, `*.swp`, `.DS_Store` | Local/editor. |
| Secrets / env | `.env`, `.env.*`, `*.secrets*`, `*.key`, `*.pem` | Security (INV-SEC-1). |

**Invariant INV-GITIGNORE-1:** No file under any of the above patterns may be tracked by git. If such a file was ever committed, it must be removed from the index (`git rm --cached <path>`) and a commit pushed so the repo no longer tracks it.

### 1.2 Verification

- **New core:** Before first release, confirm root `.gitignore` contains at least `__pycache__/` and `.pytest_cache/`.
- **Existing cores:** `git status` must not show `__pycache__/` or `.pytest_cache/` as modified/untracked in a way that suggests they were previously tracked. If they appear as "modified", run `git rm --cached -r <dir>` and commit.

### 1.3 Same rules for new cores

When adding a **new** core to the ecosystem:

1. Copy or adapt `.gitignore` from an existing core (e.g. decision-schema or execution-orchestration-core) so it includes §1.1.
2. Do **not** commit `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, or secret/env files.
3. CI and pre-commit (ruff, pytest) apply the same as in other cores; see ECOSYSTEM_INVARIANTS and repo CI workflows.

---

## 2. INV-COMMIT-1: Intended Changes Committed and Pushed (revised)

**Rule:** If a repo has **intended** (designed) changes, those changes are committed and pushed. If there are no intended changes, the repo remains clean. No repo may be left with uncommitted **tracked** changes or with commits **ahead** of `origin/main`. Intentionally excluded paths (see INV-GITIGNORE-1) are not “intended” and must not be committed.

### 2.1 What “intended” means

- **Intended:** Source, config, or doc files that are part of the designed change (e.g. feature, fix, release).
- **Not intended:** Files under INV-GITIGNORE-1 (§1.1); large datasets, local caches, or temporary exports that are deliberately not in version control. Omitting these is **not** a rule violation.

### 2.2 What is intentionally excluded

Paths in **INV-GITIGNORE-1** (§1.1): `__pycache__/`, `*.pyc`, `.pytest_cache/`, `build/`, `dist/`, `.venv/`, secrets/env. These remain untracked.

### 2.3 Deterministic checks (commit/push completeness)

| Check | Command | Pass condition |
|-------|--------|-----------------|
| No uncommitted tracked changes | `test -z "$(git status --porcelain)"` | Exit 0 |
| No commits ahead of origin/main | `git log --oneline origin/main..HEAD \| wc -l` | 0 |

Run in **every** core repo and docs repo after a batch. **Metric:** `uncommitted_tracked_changes == 0`, `ahead_of_origin_main == 0`.

**Invariant INV-COMMIT-1 (revised):** After batch commit/push, every repo with intended changes has those changes committed and pushed; no repo is left with uncommitted tracked changes or ahead of origin/main.

---

## 3. Alignment With Other Standards

| Standard | Applies to | Reference |
|----------|------------|-----------|
| Repo signature (SPDX, copyright) | All source files in all cores | REPO_SIGNATURE_STANDARD.md; script `add_repo_signature.py` |
| Denylist (never touch) | Signature script + mental model | `__pycache__/`, `.pytest_cache/`, `build/`, `dist/`, `.venv/`, etc. in REPO_SIGNATURE_STANDARD §3.2 |
| CI (lint, test, secret scan) | All cores | Each repo `.github/workflows/ci.yml` |
| Dependabot / pre-commit | All cores | `.github/dependabot.yml`, `.pre-commit-config.yaml` |

New cores must satisfy the same invariants (INV-LIC-1, INV-GITIGNORE-1, INV-COMMIT-1, INV-SAFE-1, etc.) as existing cores.

---

## 4. Summary

- **INV-GITIGNORE-1:** `.gitignore` in every core must include `__pycache__/`, `.pytest_cache/`, build/dist, venv, and secrets/env patterns; no such file may remain tracked. (`__pycache__` and `.pyc` are **intentionally** not committed.)
- **INV-COMMIT-1:** On commit/push, no repo and no intended file may be skipped; every new core and every file that belongs in the repo must be committed and pushed. Use the §2.3 checklist.
- **New cores:** Same rules; use an existing core’s `.gitignore` as template; ensure every relevant file is committed and pushed with no file left out.

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_INVARIANTS.md, REPO_SIGNATURE_STANDARD.md, BRANCH_GOVERNANCE.md
