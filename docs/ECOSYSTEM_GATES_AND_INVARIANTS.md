<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Ecosystem Gates and Invariants — SSOT

**Purpose:** Single source of truth for all measurable gates and invariants. Each entry: **definition → metric → CI check (if any) → failure remediation**. Supports contract-first, SSOT (decision-schema), fail-closed, ops kill-switch, SemVer, and doc-drift guard.

**Scope:** All core repos, integration-harness, decision-ecosystem-docs. New cores must satisfy the same gates.

---

## 1. A. File / signature (imza)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **Target types** | Signature applied only to: `.py`, `.sh`, `.ps1`; optionally `.js`, `.ts`, `.jsx`, `.tsx`; `.md`, `.mdx`. | Target files under non-denylist paths | `add_repo_signature.py --verify` | Add signature to missing target files |
| **Deny dirs** | Never touch: `archive/`, `dist/`, `build/`, `.venv/`, `venv/`, `.git/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `third_party/`, `vendor/`. | denylist_hits == 0 | Script hard-fails (INV-SAFE-1) | Remove path from scope or from denylist (fail-closed: do not touch) |
| **Deny suffixes** | Never add header to: `.json`, `.toml`, `.yml`, `.yaml`, `.lock`; binaries. | — | Script hard-fails | Do not add signature to config/data files |
| **@generated** | Files with `@generated` in first ~500 chars are skipped. | — | Script skip | N/A (by design) |
| **INV-SAFE-1** | No file in exclude set is ever touched. | denylist_hits == 0 | `add_repo_signature.py --verify` | Fix path or script; no silent skip |
| **INV-SPDX-1** | Every target source file has `SPDX-License-Identifier: MIT` in the **first 20 lines** (SSOT N=20). | spdx_missing_count == 0 | `add_repo_signature.py --verify` | Add 3-line header to missing files |
| **INV-SIGN-1** | Signature script idempotent; second run no diff. | touched_after_second_run == 0 | Manual / CI verify | Fix script or file content |

---

## 2. B. Git / commit

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-GITIGNORE-1** | `.gitignore` includes `__pycache__/`, `.pytest_cache/`, build/dist, venv, secrets/env; no such file tracked. | No `__pycache__/` or `.pytest_cache/` tracked | Manual / pre-commit | `git rm --cached <path>`; add pattern to `.gitignore` |
| **INV-COMMIT-1 (rev)** | Repo has **intended** (designed) changes → commit and push; no intended changes → repo clean. No repo left with uncommitted **tracked** changes or ahead of origin/main. | uncommitted_tracked_changes == 0, ahead_of_origin_main == 0 | `test -z "$(git status --porcelain)"`; `git log --oneline origin/main..HEAD \| wc -l` → 0 | Stage, commit, push intended files; or discard if not intended |
| **Checklist** | Deterministic checks: `git status --porcelain` empty; no commits ahead of `origin/main`. | — | CI or release checklist | Complete commit/push for each repo with changes |

---

## 3. C. Repo / scope

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **Repo list (8)** | **Repos** (GitHub repos): decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, decision-ecosystem-integration-harness, decision-ecosystem-docs. | component_list_length == 8 (for repo count) | — | Add new repo to list when new core is created |
| **Workspace paths** | Workspace root may also contain folders `docs`, `scripts` (not standalone repos but paths under a monorepo/workspace). Script COMPONENT_MAP uses these for **signature component name** only; repo list remains 8. | — | — | Keep COMPONENT_MAP in sync with repo names + workspace path names for header attribution |
| **INV-CORE-DEP-1** | Core repos depend only on decision-schema (no core↔core). | core_to_core_dep_count == 0 | pyproject / grep | Remove cross-core dependency; use schema only |

---

## 4. D. License / docs

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-LIC-1** | Every repo root has `LICENSE` (MIT text). | license_missing_count == 0 | `test -f LICENSE` | Add LICENSE file |
| **INV-README-LIC-1** | README has no placeholder like `[Add your license]`. | count(placeholder) == 0 | grep | Replace placeholder |
| **INV-LANG-1** | All documentation and file/dir names in **English**. | non_english_doc_or_filename == 0 | grep Turkish chars/words | Rename or translate to English |
| **Doc naming** | Documentation filenames: **single format** `SCREAMING_SNAKE_CASE.md` (ASCII-only). | nonconforming_doc_filenames == 0 | CI / script | Rename to SCREAMING_SNAKE_CASE |

---

## 5. E. Docs repo structure (decision-ecosystem-docs)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **Root allowlist** | Only allowlist files at root; README links only to these. | — | check_docs_root.py | Move non-allowlist to archive or docs/ |
| **No root clutter** | No session/summary, one-off migration, sprint board, old verification at root. | — | check_docs_root.py | Move to archive/YYYY-MM-DD/ |
| **INV-DOC-2** | Dated snapshots under `archive/YYYY-MM-DD/`. | — | — | Create dated archive dir; move file |
| **Analysis limit** | At most 1–2 current analysis reports at root. | current_analysis_count <= 2 | check_docs_root.py | Move older to archive |

---

## 6. F. CI / release

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-CI-PIN-1** | CI installs decision-schema `>=0.2.2,<0.3` with fallback tag `@v0.2.2`. **Lifecycle:** When schema minor is bumped, update range and fallback in all cores (procedural). | Workflow matches per repo | workflow YAML | Update workflow + ECOSYSTEM_CONTRACT_MATRIX; document procedure |
| **INV-CI-NONDET-0** | CI fallback must not use `@main` when a release tag exists. Allowlist SSOT (e.g. first-release-only temporary @main). | @main only in allowlist | grep workflow | Use tag fallback; document allowlist |
| **INV-CI-TAG-1** | Tag push triggers CI. **Scope:** core + harness (docs optional). | on.push.tags: ["v*"] | workflow | Add tags trigger |
| **INV-CI-PROOF-1** | CI produces machine-readable proof artifact. **Scope:** pytest repos → pytest-report JSON; docs → e.g. broken-link check. | Artifact present, parseable | upload-artifact / job | Add pytest-report or docs artifact step |
| **INV-DOC-DRIFT-1** | Roadmap table matches pyproject.version and Git tags. | roadmap_mismatch_rows == 0 | check_release_alignment.py | Update NEXT_STEPS_ROADMAP or version/tag |

---

## 7. G. Release notes

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-REL-*** | Release notes standard: INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1, INV-REL-PROOF-1. | Per RELEASE_NOTES_STANDARD | Manual / checklist | Follow RELEASE_NOTES_STANDARD_AND_TEMPLATES.md |

---

## 8. H. SSOT / PARAMETER_INDEX / trace registry (P0)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-PARAM-INDEX-1** | PacketV2 / external trace key format changes require **decision-schema/docs/PARAMETER_INDEX.md** (or SSOT doc) updated before merge. | param_index_drift == 0 | decision-schema CI: check_parameter_index.py (to add) | Update PARAMETER_INDEX; cores do not edit (SSOT in schema) |
| **INV-TRACE-REG-1** | Every key written to `PacketV2.external` by a core/harness must be **registered** in trace registry. | unregistered_external_key_count == 0 | Harness e2e: validate_external_dict(strict=True) | Register key in decision-schema trace_registry; or stop writing key |

---

## 9. I. Security / redaction (P0)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-SEC-RED-1** | No secret/PII pattern in repo; CI fails if detected. | secret_findings == 0 | gitleaks/gitleaks-action (or trufflehog) | Remove secret; rotate if leaked |
| **INV-ERR-SURFACE-1** | Runtime error surfaces redacted and structured (`error_type`, `error_code`); raw `error_message` not exposed. | raw_error_message_set_count == 0 | Lint/grep + unit test | Use structured error; redact messages |

---

## 10. J. SemVer / deprecation (P1)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-SEMVER-1** | Public API breaking change → major bump; else minor/patch. Release notes "Compatibility" states breaking. | Breaking flag in release notes when API breaks | Manual / checklist | Bump major; document in release notes |
| **INV-DEPREC-1** | Every deprecated field has SSOT: deprecated_in, remove_in, migration_note. | deprecated_without_timeline == 0 | Doc review / DEPRECATION_POLICY.md | Add timeline to docs; emit DeprecationWarning; release notes "Deprecated" |

---

## 11. K. CI quality (P1)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-BUILD-1** | Every core repo builds: `python -m build` succeeds. | build_failures == 0 | CI step: `python -m build` | Fix packaging (pyproject.toml, manifests) |
| **INV-LINT-1** | Ruff (and optionally mypy) pass in CI. | lint_failures == 0 | ruff check .; ruff format --check | Fix lint/format |

---

## 12. L. Docs quality (P1)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-DOC-LINK-1** | README and doc links (relative) resolve; no broken link. | broken_link_count == 0 | check_docs_root.py / link checker | Fix or remove link; add target file |

---

## 13. M. CI compliance (INV-CI-COMPLY-1)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-CI-COMPLY-1** | Every repo’s CI workflow conforms to the **CI Compliance Standard**: required steps (secret_scan, LICENSE, Ruff check, Ruff format check, build, pytest, artifact) present and passing per repo type. | ci_compliance_failures == 0 | Manual or script: verify workflow YAML contains required steps; run workflow and confirm green | Add missing job/step; fix failing step. See **docs/CI_COMPLIANCE_STANDARD.md**. |

**SSOT for required steps:** **docs/CI_COMPLIANCE_STANDARD.md** (§2: core, harness, docs).

---

## 14. Patch plan (fail-closed order)

**P0**

- INV-COMMIT-1 wording revision (intended changes; deterministic git checks).
- COMPONENT_MAP vs repo list: document repo list (8) vs workspace paths (docs, scripts) for signature component.
- INV-PARAM-INDEX-1, INV-TRACE-REG-1: add CI gates (decision-schema + harness).
- INV-SEC-RED-1: already in place (gitleaks job); verify all repos.

**P1**

- Doc naming: single standard SCREAMING_SNAKE_CASE (DOCUMENTATION_STANDARDS).
- INV-BUILD-1, INV-LINT-1: ensure build + lint in each core CI.
- INV-DEPREC-1: add DEPRECATION_POLICY.md and timeline requirement.

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_INVARIANTS.md, CORE_REPO_STANDARDS.md, REPO_SIGNATURE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
