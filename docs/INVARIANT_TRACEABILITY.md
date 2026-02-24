<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Invariant → Script / Test Mapping (INV-TRACE-MAP-1)

**Purpose:** Map each invariant (or gate) to the **script**, **CI job**, or **test file** that enforces it. Per INV-TRACE-MAP-1 and [ECOSYSTEM_GATES_AND_INVARIANTS.md](ECOSYSTEM_GATES_AND_INVARIANTS.md).

**Scope:** P0/P1 and key CI/docs invariants. Update this table when adding or changing invariants.

---

## 1. Docs repo scripts (decision-ecosystem-docs)

| Invariant ID | Script / command | Test file (if any) |
|--------------|------------------|---------------------|
| INV-DOC-DRIFT-1, version alignment | `tools/check_release_alignment.py --workspace <path>` | — |
| INV-SYNC-1 | `tools/check_workspace_sync.py --workspace <path>` | — |
| INV-REMOTE-OWNER | `tools/check_remote_owner.py --workspace <path>` | — |
| INV-CI-COMPLY-2, INV-CI-COMPLY-1 (per repo) | `tools/check_ci_compliance.py --workspace <path>` | — |
| INV-PUBLIC-MAIN-1, INV-PUBLIC-MAIN-2 | `tools/public_main_audit.py --owner <owner>` | — |
| INV-DOC-ROOT-ALLOWLIST-1, INV-DOC-ROOT-ALLOWLIST-FMT-1, docs structure | `.github/scripts/check_docs_root.py` (docs repo CI) | — |
| INV-DOC-LINK-1 | `.github/scripts/check_docs_links.py` | — |
| INV-DOC-DOMAIN-0 | `.github/scripts/check_docs_domain_lexemes.py` (config: docs/DOMAIN_LEXEMES.txt) | — |
| Local CI simulation (all docs guard steps) | `python .github/scripts/run_docs_guard_ci_steps.py` (from repo root) | — |
| **Tüm testler + guard'lar (sadece docs repo)** | `python .github/scripts/run_all_tests_and_guards.py` (docs pytest + 4 guard) | `tools/tests/` |
| **Tüm ekosistem (çekirdekler + harness + docs + guard'lar)** | `python tools/run_all_ecosystem_tests.py --workspace <parent-dir>` (tüm repolarda pytest + docs guard'lar) | Her repoda `tests/`; docs: `tools/tests/` |

---

## 2. CI jobs (all repos)

| Invariant ID | CI job / step | Test file (if any) |
|--------------|----------------|---------------------|
| INV-SEC-RED-1 | `secret_scan` (gitleaks) | — |
| INV-LIC-1 | `test -f LICENSE` (or equivalent) | — |
| INV-LINT-1 | Ruff check, Ruff format check | — |
| INV-BUILD-1 | `python -m build` | — |
| INV-CI-BUILD-SMOKE-1 | Wheel install + smoke import | — |
| INV-CI-PROOF-1, INV-CI-PROOF-STD-1 | pytest with artifact upload | (all `tests/` in repo) |
| INV-PARAM-INDEX-1 | decision-schema CI: `python tools/check_parameter_index.py` | — |
| INV-CI-PIN-1, INV-CI-SCHEMA-FB-1 | Workflow YAML + check_ci_compliance.py | — |
| INV-DOC-* (docs repo) | `.github/workflows/docs_structure_guard.yml`: check_docs_root, check_docs_links, check_docs_domain_lexemes, check_ci_compliance | — |

---

## 3. Tests by repo (invariant behaviour)

| Invariant / behaviour | Repo | Test file |
|------------------------|------|-----------|
| Domain-agnostic (docs lexeme) | harness | `tests/test_invariant_0_domain_agnosticism.py` |
| Domain-agnostic (no cross-core import) | schema, mdm-engine, dmc, ops-health, eval, exe, explainability, harness | `tests/test_invariant_0_domain_agnosticism.py`, `tests/test_invariant_2_no_cross_core_imports.py` (per repo) |
| CI workflow hygiene (LF, no control chars) | schema, mdm-engine, dmc, ops-health, eval, exe, harness | `tests/test_invariant_ci_0_workflow_hygiene.py` |
| Schema pin (minor 2) | mdm-engine, dmc, ops-health, eval, harness | `tests/test_invariant_schema_pin_minor_2.py` |
| Version single source | schema, mdm-engine, dmc, ops-health, eval, exe, explainability, harness | `tests/test_invariant_version_single_source.py` |
| Fail-closed propagation | harness | `tests/test_invariant_h4_fail_closed_propagation.py` |
| Fail-closed (external key registered) | harness | `tests/test_invariant_t1_harness_external_keys_registered.py` |
| Kill-switch dominance | harness | `tests/test_invariant_h2_kill_switch_dominance.py` |
| Fail-closed (exception / timeout) | execution-orchestration-core | `tests/test_invariant_exe_fail_closed.py`, `tests/test_invariant_exe_boundedness.py` |
| Kill-switch denies execution | execution-orchestration-core | `tests/test_invariant_exe_kill_switch.py` |
| Explainability fail-closed | explainability-audit-core | `tests/test_explain.py` (e.g. `test_explain_denied_fail_closed`) |
| Trace keys / external registry | decision-schema | `tests/test_invariant_t1_trace_key_registry.py` |
| PacketV2 / contract | schema, harness | schema: `tests/test_packet_v2_smoke.py`, `tests/test_contract_matrix.py`; harness: contract tests in e2e |

---

## 4. Manual / checklist (no automated script)

| Invariant ID | Enforcement | Where |
|--------------|-------------|--------|
| INV-REL-* (release notes) | Manual / checklist | RELEASE_NOTES_STANDARD_AND_TEMPLATES.md |
| INV-SEMVER-1 | Manual / release process | Release notes "Compatibility" |
| INV-DEPREC-1 | Doc review | docs/DEPRECATION_POLICY.md ✅ |
| INV-EVIDENCE-1 | Doc review | EVIDENCE_SUMMARY.md (this doc set) |
| INV-SEC-SCOPE-1 | Doc review | SECURITY_SCOPE.md |

---

**Last updated:** 2026-02  
**Invariant:** INV-TRACE-MAP-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
