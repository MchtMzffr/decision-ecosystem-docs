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

## 2. INV-COMMIT-1: No File or Repo Skipped on Commit/Push

**Rule:** When doing commit and push (batch or per release), **no intended file and no repo may be skipped**. Every repo that has uncommitted or unpushed changes must be committed and pushed. Newly added cores and every relevant file must be included.

### 2.1 What “no skip” means

| Must be included | Must not be skipped |
|------------------|----------------------|
| Every core repo that has local changes | A repo left with uncommitted or unpushed work |
| New cores and new files (source, config, docs) | Any source/config/doc file that should be in version control |
| All modified/added files under target paths | Leaving a file out “by mistake” when it should be committed |

### 2.2 What is intentionally excluded

Files and directories listed in **INV-GITIGNORE-1** (§1.1) are **not** intended to be in the repo: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `build/`, `dist/`, `.venv/`, secrets/env. These must remain untracked and are not “skipped” — they are excluded by rule.

### 2.3 Checklist before “done” (commit/push completeness)

1. Run `git status -sb` (or equivalent) in **every** core repo and in the docs repo.
2. For each repo with changes: stage all **intended** files (respecting `.gitignore`), commit, then push.
3. Confirm no repo is left **ahead** of `origin/main` (all pushed).
4. New cores: same process; every file that belongs in the repo must be committed and pushed, no file skipped.

**Invariant INV-COMMIT-1:** After a batch commit/push, no repo has uncommitted or unpushed changes for intended files; no file that should be in version control is left out.

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
