<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Evidence Summary — Claims vs Enforcement Mechanisms

**Purpose:** Separate which **claims** (fail-closed, domain-agnostic, contract-first, kill-switch) are enforced by which **mechanism** and in which **scope** (documentation, API/data, runtime). Per INV-EVIDENCE-1 and [ACADEMIC_CRITIQUE_AND_REASONS.md](ACADEMIC_CRITIQUE_AND_REASONS.md).

**Scope:** Decision Ecosystem (schema, cores, harness, docs). Keep this table updated when adding invariants or tests.

---

## 1. Summary table

| Claim | Scope | Mechanism | Where |
|-------|-------|-----------|--------|
| **Domain-agnostic (docs)** | Documentation | Lexeme scan: forbidden words (e.g. bid, auction) must not appear in README and docs (excl. examples). | Harness: `tests/test_invariant_0_domain_agnosticism.py` → `test_invariant_0_docs_domain_agnostic`; CI runs pytest. |
| **Domain-agnostic (API/data)** | API, data model | Schema and cores use generic types only (Action, Proposal, PacketV2, generic keys). No core↔core deps. | INV-CORE-DEP-1: pyproject/grep; tests in each core: `test_invariant_0_domain_agnosticism`, `test_invariant_2_no_cross_core_imports`, schema contract tests. |
| **Domain-agnostic (runtime)** | Runtime behaviour | Not asserted as a single invariant. Pipeline accepts generic input; domain logic is in caller/adapter. | By design: cores do not encode domain; no dedicated “runtime domain-agnostic” test suite. |
| **Fail-closed** | Runtime | On exception or guard failure, final action is HOLD/STOP; packet carries `harness.fail_closed` or report.fail_closed. | Harness: `tests/test_invariant_h4_fail_closed_propagation.py`; execution-orchestration: `test_invariant_exe_fail_closed.py`, `test_invariant_exe_boundedness.py`; explainability: `test_explain_denied_fail_closed`. |
| **Kill-switch dominance** | Runtime | Ops-health kill-switch can force deny regardless of proposal. | Harness: `tests/test_invariant_h2_kill_switch_dominance.py`; ops-health: `test_kill_switch.py`; execution: `test_invariant_exe_kill_switch.py`. |
| **Contract-first / SSOT** | API, CI | decision-schema is single source of truth; version compatibility (e.g. minor pin). | INV-CI-PIN-1, INV-REL-SSOT-2; `check_release_alignment.py`; schema compat tests in cores (e.g. `test_schema_dependency`, `test_invariant_schema_pin_minor_2`). |
| **No secrets in repo** | Repo content | No secret/PII pattern in committed files. | INV-SEC-RED-1: gitleaks (or equivalent) in CI; secret_scan job in every workflow. See [SECURITY_SCOPE.md](SECURITY_SCOPE.md). |
| **Version/docs alignment** | Docs vs reality | Roadmap table matches pyproject versions and Git tags. | `check_release_alignment.py`; INV-DOC-DRIFT-1. |
| **Workspace sync** | Git state | Working tree clean; not ahead of origin/main; remote owner canonical. | `check_workspace_sync.py`, `check_remote_owner.py`; INV-SYNC-1. |
| **CI compliance** | CI workflow | Required steps (secret_scan, LICENSE, Ruff, build, pytest, artifact) per repo type. | `check_ci_compliance.py`; INV-CI-COMPLY-1, INV-CI-COMPLY-2. See [CI_COMPLIANCE_STANDARD.md](CI_COMPLIANCE_STANDARD.md). |

---

## 2. Scope definitions

- **Documentation:** Human-readable docs (README, `docs/`, release notes). Evidence = lexeme scan and link/placeholder checks.
- **API/data:** Public types, packet shape, dependency graph. Evidence = schema, pyproject, and tests that assert no domain types and no core↔core imports.
- **Runtime:** Behaviour of the pipeline under execution. Evidence = tests that inject failures and assert final action and fail_closed/kill_switch behaviour.

---

## 3. What we do not claim

- **Runtime domain-agnosticism** is not enforced by a single test; we rely on “no domain types in schema/cores” and design. No formal proof.
- **Formal fail-closed** is defined as a predicate in [FORMALISATION_NOTE.md](FORMALISATION_NOTE.md); current evidence remains test-based (no proof over all reachable states).
- **Security** is scoped to “no secrets in repo” and structured errors; see [SECURITY_SCOPE.md](SECURITY_SCOPE.md).

---

**Last updated:** 2026-02  
**Invariant:** INV-EVIDENCE-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
