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
| **INV-REPO-REG-1** | Repo list and type are SSOT in **docs/REPO_REGISTRY.md**. | repo_registry_count == expected; unknown_repo_in_ci == 0 | check_ci_compliance (reads registry) | Update REPO_REGISTRY.md; align checker/sync |
| **INV-REPO-REG-SSOT-1** | check_workspace_sync and checker use repo list from registry when present (no hardcode drift). | sync_repos_from_registry == true when registry exists | check_workspace_sync / check_ci_compliance | Load REPO_DIRS from REPO_REGISTRY.md |
| **Repo list** | Registry defines: core, harness, docs, experimental (e.g. explainability-audit-core as 9th). | — | REPO_REGISTRY.md | Add row when new repo joins ecosystem |
| **Workspace paths** | Workspace root may also contain folders `docs`, `scripts` (not standalone repos but paths under a monorepo/workspace). Script COMPONENT_MAP uses these for **signature component name** only. | — | — | Keep COMPONENT_MAP in sync with repo names + workspace path names for header attribution |
| **INV-CORE-DEP-1** | Core repos depend only on decision-schema (no core↔core). | core_to_core_dep_count == 0 | pyproject / grep | Remove cross-core dependency; use schema only |
| **INV-REL-SSOT-2** | Version in docs = pyproject + Git tag; docs do not override reality. | version_mismatch_rows == 0 | check_release_alignment; ECOSYSTEM_CONTRACT_MATRIX | Set matrix/roadmap to actual versions |

### 3.1 COMPONENT_MAP vs repo list (P0)

**Repo list (sync/CI):** The ecosystem has **9 repositories** (SSOT: REPO_REGISTRY.md / tools REPO_DIRS): decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, explainability-audit-core, decision-ecosystem-integration-harness, decision-ecosystem-docs.

**COMPONENT_MAP** (in `scripts/add_repo_signature.py`): Used **only for signature header attribution** when adding or verifying file headers. It lists **repo names** that exist as directories (e.g. decision-schema, mdm-engine, …) plus **workspace paths** that are not standalone repos: `docs`, `scripts`. So COMPONENT_MAP may have 8 repo names + `docs` + `scripts` (order and count depend on script version). When a new repo is added to the ecosystem, add it to REPO_REGISTRY / REPO_DIRS for sync and CI; add it to COMPONENT_MAP only if the signature script should attribute files under that path to a component name. **Do not** confuse COMPONENT_MAP with the canonical repo count: the canonical list for release/sync is REPO_REGISTRY / check_workspace_sync REPO_DIRS.

---

## 4. D. License / docs

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-LIC-1** | Every repo root has `LICENSE` (MIT text). | license_missing_count == 0 | `test -f LICENSE` | Add LICENSE file |
| **INV-README-LIC-1** | README has no placeholder like `[Add your license]`. | count(placeholder) == 0 | grep | Replace placeholder |
| **INV-LIC-SPDX-2** | Repo-level: LICENSE exists + README no license placeholder; CI enforces both. | license_missing == 0, license_placeholder_found == 0 | CI step + optional grep README | Add LICENSE; fix README |
| **INV-LANG-1** | All documentation and file/dir names in **English**. | non_english_doc_or_filename == 0 | grep Turkish chars/words | Rename or translate to English |
| **INV-DOC-LANG-2** | **All documentation in English** (standards, invariants, release notes, verification checklists, status reports, operational docs). No Turkish allowlist. | non_english_doc_count == 0 | Policy; .cursor/rules/documentation-english.mdc | Translate to English |
| **Doc naming** | Documentation filenames: **single format** `SCREAMING_SNAKE_CASE.md` (ASCII-only). | nonconforming_doc_filenames == 0 | CI / script | See **docs/DOCUMENTATION_STANDARDS.md**; rename to SCREAMING_SNAKE_CASE |

---

## 5. E. Docs repo structure (decision-ecosystem-docs)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **Root allowlist** | Only allowlist files at root; README links only to these. | — | check_docs_root.py | Move non-allowlist to archive or docs/ |
| **INV-DOC-ROOT-ALLOWLIST-FMT-1** | Each non-comment line in ROOT_ALLOWLIST.txt contains a single path (no spaces). | allowlist_parse_errors == 0 | check_docs_root.py | One path per line; fix or remove whitespace |
| **INV-DOC-ROOT-ALLOWLIST-1** | ECOSYSTEM_INVARIANTS.md (and governance docs) in root allowlist; check_docs_root.py enforces. | allowlist_contains_invariants == true | check_docs_root.py | Add to DOCS_REPO_STRUCTURE allowlist |
| **No root clutter** | No session/summary, one-off migration, sprint board, old verification at root. | — | check_docs_root.py | Move to archive/YYYY-MM-DD/ |
| **INV-DOC-2** | Dated snapshots under `archive/YYYY-MM-DD/`. | — | — | Create dated archive dir; move file |
| **INV-DOC-ACTIVE-1** | README "Current" section links only to CURRENT set (root allowlist + docs/); archive/ links only in Archive section. | current_section_archive_links == 0 | check_docs_root.py / policy | Keep CURRENT vs Archive sections separate; link checker can enforce |
| **Analysis limit** | At most 1–2 current analysis reports at root. | current_analysis_count <= 2 | check_docs_root.py | Move older to archive |

---

## 6. F. CI / release

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-CI-PIN-1** | CI installs decision-schema `>=0.2.2,<0.3` with fallback tag `@v0.2.2`. **Lifecycle:** When schema minor is bumped, update range and fallback in all cores (procedural). | Workflow matches per repo | workflow YAML | Update workflow + ECOSYSTEM_CONTRACT_MATRIX; document procedure |
| **INV-CI-NONDET-0** | CI fallback must not use `@main` when a release tag exists. Allowlist SSOT (e.g. first-release-only temporary @main). | @main only in allowlist | grep workflow | Use tag fallback; document allowlist |
| **INV-CI-TAG-1** | Tag push triggers CI. **Scope:** core + harness (docs optional). | on.push.tags: ["v*"] | workflow | Add tags trigger |
| **INV-CI-PROOF-1** | CI produces machine-readable proof artifact. **Scope:** pytest repos → pytest-report JSON; docs → e.g. broken-link check. | Artifact present, parseable | upload-artifact / job | Add pytest-report or docs artifact step |
| **INV-SYNC-1** | Git state only: working tree clean, not ahead/behind origin/main, remote owner canonical. **CI run result is separate.** | working_tree_clean ∧ ahead_of_origin_main==0 ∧ behind==0 ∧ remote_owner | check_workspace_sync + check_remote_owner | Commit/push; fix remote URL |
| **INV-CI-PASS-1** | CI workflow run outcome = PASS (green). Separate from sync. | workflow_run_success == true | GitHub Actions / API | Fix failing steps; re-run |
| **INV-PUBLIC-MAIN-1** | Standards not DONE until verified on **public** main (`raw.githubusercontent.com/.../main/...`). | public_main_drift_count == 0 | public_main_audit.py | Push to origin main; run `python tools/public_main_audit.py --owner <owner>` |
| **INV-PUBLIC-MAIN-2** | Public main raw content satisfies same invariants (deterministic proof; hard-fail). | Same as INV-PUBLIC-MAIN-1 | public_main_audit.py | Fix drift; push to origin; re-run audit |
| **INV-README-NO-PLACEHOLDER-1** | README/docs have no `[Add your license]` placeholder. | placeholder_hits == 0 | grep / public_main_audit | Remove placeholder; add license link |
| **INV-OWNER-REF-1** | All github.com/owner/... links use canonical owner (e.g. MchtMzffr). | wrong_owner_link_count == 0 | public_main_audit | Replace wrong owner with canonical |
| **INV-SSOT-REALITY-1** | Docs pin/tag/version verifiable from public main. | docs_claim_mismatches == 0 | public_main_audit + check_release_alignment | Align pyproject/tag/CI on public main |
| **INV-DOC-DRIFT-1** | Roadmap table matches pyproject.version and Git tags. | roadmap_mismatch_rows == 0 | check_release_alignment.py | Update NEXT_STEPS_ROADMAP or version/tag |
| **INV-RM-SCOPE-1** | Roadmap P0 table scope is defined (e.g. core-only); repos not in table have written reason (e.g. harness non-core). | scope_documented == true | NEXT_STEPS_ROADMAP | Add harness policy / scope note |

---

## 7. G. Release notes

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-REL-*** | Release notes standard: INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1, INV-REL-PROOF-1. | Per RELEASE_NOTES_STANDARD | Manual / checklist | Follow RELEASE_NOTES_STANDARD_AND_TEMPLATES.md |

---

## 8. H. SSOT / PARAMETER_INDEX / trace registry (P0)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-PARAM-INDEX-1** | PacketV2 / external trace key format changes require **decision-schema/docs/PARAMETER_INDEX.md** (or SSOT doc) updated before merge. | param_index_drift == 0 | decision-schema CI: `python tools/check_parameter_index.py` | Update PARAMETER_INDEX; cores do not edit (SSOT in schema) ✅ |
| **INV-TRACE-REG-1** | Every key written to `PacketV2.external` by a core/harness must be **registered** in trace registry. | unregistered_external_key_count == 0 | Harness: tests/test_invariant_t1_harness_external_keys_registered.py (validate_external_dict strict) | Register key in decision-schema trace_registry; or stop writing key ✅ |

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
| **INV-DOC-LINK-1** | README and doc links (relative) resolve; no broken link. | broken_link_count == 0 | check_docs_links.py | Fix or remove link; add target file |
| **INV-DOC-DOMAIN-0** | ACTIVE docs (docs/ excluding archive/ and examples/) contain no domain lexemes from config. | domain_lexeme_count == 0 | check_docs_domain_lexemes.py | Remove lexeme or move to examples/; update docs/DOMAIN_LEXEMES.txt |
| **INV-DOC-POLICY-SSOT-1** | Branch/tag/release policy is defined only in designated governance docs (root: BRANCH_GOVERNANCE.md, TAG_GOVERNANCE.md, RELEASE_VERIFICATION_CHECKLIST.md; docs/: CI_COMPLIANCE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md). Other docs link; do not duplicate policy text. | policy_duplicate_undefined | Manual / optional check_policy_duplicates.py | Move policy text to governance doc; replace with link |

---

## 13. M. CI compliance (INV-CI-COMPLY-1, INV-CI-COMPLY-2)

| ID | Definition | Metric | CI / check | Remediation |
|----|------------|--------|------------|-------------|
| **INV-CI-COMPLY-1** | Every repo’s CI workflow conforms to the **CI Compliance Standard**: required steps (secret_scan, LICENSE, Ruff check, Ruff format check, build, pytest, artifact) present and passing per repo type. | ci_compliance_failures == 0 | check_ci_compliance.py (INV-CI-COMPLY-2) | Add missing job/step; fix failing step. See **docs/CI_COMPLIANCE_STANDARD.md**. |
| **INV-CI-COMPLY-2** | Compliance checker runs in docs CI; fail-closed. | compliance_checker_pass == true | docs workflow: `python tools/check_ci_compliance.py --workspace .` | Fix workflow or checker. |
| **INV-CI-SCOPE-1** | N/A steps only with documented condition (e.g. Docs Ruff when no pyproject/tools/*.py). | na_steps_without_condition == 0 | check_ci_compliance.py | Document condition or add step. |
| **INV-CI-PROOF-STD-1** | Proof artifact path/name fixed (pytest-report.json, artifact pytest-report or pytest-report-<py>). | missing_or_wrong_artifact_count == 0 | CI / checklist | Align pytest and upload-artifact with standard. |
| **INV-CI-ACT-PIN-1** | Actions `uses:` pinned (tag/sha). | unpinned_actions_count == 0 | grep / script | Pin to @vX or @sha. |
| **INV-CI-PERM-1** | Default permissions: contents read; widen only if needed. | overprivileged_workflows == 0 | workflow YAML | Set permissions explicitly. |
| **INV-CI-PY-1** | Core/harness: at least one fixed Python (e.g. 3.11). | python_version_unspecified == 0 | workflow YAML | Add setup-python with version. |
| **INV-CI-BUILD-SMOKE-1** | After build: pip install wheel + minimal import. | wheel_smoke_failures == 0 | CI step | Add smoke step. |
| **INV-CI-SCHEMA-FB-1** | decision-schema fallback tag only; no @main. | schema_fallback_main_count == 0 | check_ci_compliance.py / grep | Use @vX.Y.Z. |

**SSOT for required steps and N/A conditions:** **docs/CI_COMPLIANCE_STANDARD.md** (§2: core, harness, docs; §2.4 N/A, §2.5 proof artifact, §5.1 additional invariants, §7 checker).

---

## 14. Patch plan (fail-closed order)

**P0**

- INV-COMMIT-1 wording revision (intended changes; deterministic git checks). **Done:** Definition in §2 and **docs/CORE_REPO_STANDARDS.md** §2; checks: `git status --porcelain` empty, no commits ahead of origin/main. ✅
- COMPONENT_MAP vs repo list: document repo list vs workspace paths (docs, scripts) for signature component. **§3.1** ✅
- INV-PARAM-INDEX-1: CI gate in decision-schema (check_parameter_index.py in ci.yml). **Done.** ✅
- INV-TRACE-REG-1: Harness tests enforce validate_external_dict(strict=True); see test_invariant_t1_harness_external_keys_registered.py. **Done.** ✅
- INV-SEC-RED-1: secret_scan (gitleaks) job required in all repos per CI_COMPLIANCE_STANDARD; check_ci_compliance.py verifies. **Verified.** ✅

**P1**

- Doc naming: single standard SCREAMING_SNAKE_CASE. **Done:** **docs/DOCUMENTATION_STANDARDS.md** ✅
- INV-BUILD-1, INV-LINT-1: ensure build + lint in each core CI. **Done:** check_ci_compliance.py requires ruff check, ruff format, python -m build for core/harness; all repos comply. ✅
- INV-DEPREC-1: add DEPRECATION_POLICY.md and timeline requirement. **Done:** **docs/DEPRECATION_POLICY.md** (deprecated_in, remove_in, migration_note). ✅
- **Academic & R&D (from ACADEMIC_CRITIQUE_AND_REASONS.md, RND_FUTURE_DIRECTIONS_AND_REASONS.md):**
  - INV-EVIDENCE-1: Evidence summary doc — which claims (fail-closed, domain-agnostic) are enforced by which mechanism (test, CI, manual); separate (a) docs lexeme, (b) API/data, (c) runtime. See **docs/EVIDENCE_SUMMARY.md**. **Phase: P1.** ✅
  - INV-TRACE-MAP-1: Invariant → CI/test mapping table in docs (Invariant ID → script/job → test file). See **docs/INVARIANT_TRACEABILITY.md**. **Phase: P1.** ✅
  - INV-SEC-SCOPE-1: Security scope doc — in-scope vs out-of-scope threats; which invariants address which. See **docs/SECURITY_SCOPE.md**. **Phase: P1.** ✅
  - INV-REPRO-1: For major releases or publications, document a versioned snapshot (e.g. Zenodo DOI or list of commit SHAs/tags) in docs repo. See **docs/REPRODUCIBILITY.md**. **Phase: P1 (process).** ✅

**P2**

- **Academic & R&D (continued):**
  - INV-FORMAL-1: Formalisation note — fail-closed as predicate over pipeline state/outputs; list components in scope; reference tests linked to predicates. See **docs/FORMALISATION_NOTE.md**. **Phase: P2.** ✅
  - INV-VALID-1: Validation section — list assumptions and intended guarantees; map critical scenarios (e.g. kill-switch, schema mismatch) to tests; optional one reproducible experiment. See **docs/VALIDATION.md**. **Phase: P2.** ✅
  - R&D directions (roadmap): formalisation report, new vertical cores, explainability extension (counterfactuals/audit export), benchmarks/experiments, tooling (schema diff, trace viewer), community (CONTRIBUTING, interchange format). See **docs/RND_FUTURE_DIRECTIONS_AND_REASONS.md**. **Phase: P2/P3.**

---

## 15. Academic and R&D standards (normative)

These entries stem from **docs/ACADEMIC_CRITIQUE_AND_REASONS.md** and **docs/RND_FUTURE_DIRECTIONS_AND_REASONS.md**. They are added as project rules so that gaps and improvements are tracked and phased.

| ID | Definition | Metric | CI / check | Remediation | Phase |
|----|------------|--------|------------|-------------|-------|
| **INV-EVIDENCE-1** | Claims (fail-closed, domain-agnostic) have an evidence summary: which claim is enforced by which mechanism (lexeme scan, test, CI, manual). Docs vs API vs runtime separated. | evidence_summary_doc_exists == true; three categories present | Doc review; optional link check | Add **docs/EVIDENCE_SUMMARY.md**; keep table up to date | P1 |
| **INV-TRACE-MAP-1** | Every invariant (or each P0/P1 gate) has a mapping to the script/job and test file that enforces it. | mapping_rows >= key_invariants_count | Doc review; checklist | Add mapping table to gates doc or **docs/INVARIANT_TRACEABILITY.md** | P1 |
| **INV-SEC-SCOPE-1** | Security scope is documented: in-scope threats, out-of-scope, and which invariants (e.g. INV-SEC-RED-1, INV-ERR-SURFACE-1) address which. | security_scope_doc_exists == true | Doc review | Add **docs/SECURITY_SCOPE.md** | P1 |
| **INV-REPRO-1** | For each major release or publication, a versioned snapshot (DOI or commit/tag list) is documented so that “this report refers to this version” is citable. | snapshot_documented_for_release == true when release is published | Checklist / release process | Document in release notes or **docs/REPRODUCIBILITY.md** | P1 |
| **INV-FORMAL-1** | Fail-closed (and optionally pipeline) have a short formalisation: predicate over state/outputs; components in scope; tests referenced. | formalisation_note_exists == true | Doc review | **docs/FORMALISATION_NOTE.md** ✅ | P2 ✅ |
| **INV-VALID-1** | Validation section exists: assumptions, intended guarantees, critical scenarios mapped to tests; optional one reproducible experiment. | validation_section_exists == true | Doc review | **docs/VALIDATION.md** ✅ | P2 ✅ |

**Cursor rule:** When editing docs or invariants related to academic/R&D standards, follow **.cursor/rules/academic-rnd-standards.mdc** (evidence vs claim separation, traceability, formalisation when defining terms, reproducibility).

---

## 16. Last full-structure and CI verification (per rules)

**Date:** 2026-02-18

| Check | Script / command | Result |
|-------|------------------|--------|
| Release alignment | `check_release_alignment.py` | OK |
| Remote owner | `check_remote_owner.py` | OK |
| CI compliance | `check_ci_compliance.py` | OK (all repos) |
| Workspace sync (INV-SYNC-1) | `check_workspace_sync.py` | FAIL until local changes committed (ops-health-core, harness, docs) |
| Pytest + coverage | `ecosystem.py test` (all 8 repos with tests) | OK (197 tests total) |
| INV0 docs (harness) | `test_invariant_0_domain_agnosticism` | OK (P0_CLOSURE_CHECKLIST: "forbidden" → "prohibited" to avoid lexeme "bid") |

CI workflows (secret scan, Ruff, build, pip-audit, coverage) are configured per P3; pip upgraded to ≥26 in CI before pip-audit to satisfy CVE requirements.

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_INVARIANTS.md, CORE_REPO_STANDARDS.md, REPO_SIGNATURE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md, ACADEMIC_CRITIQUE_AND_REASONS.md, RND_FUTURE_DIRECTIONS_AND_REASONS.md
