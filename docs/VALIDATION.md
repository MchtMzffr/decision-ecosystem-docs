<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Validation — Assumptions, Guarantees, Critical Scenarios (INV-VALID-1)

**Purpose:** Document **assumptions**, **intended guarantees**, and **critical scenarios** mapped to tests; optionally one **reproducible experiment**. Per INV-VALID-1 and [ACADEMIC_CRITIQUE_AND_REASONS.md](ACADEMIC_CRITIQUE_AND_REASONS.md).

**Scope:** Decision Ecosystem (harness pipeline, cores, schema). This document supports audit and regression: “what do we assume, what do we guarantee, and how do we test it?”

---

## 1. Assumptions

| Assumption | Description | Where it holds |
|------------|-------------|----------------|
| **Trusted execution** | Pipeline and cores run in a trusted environment; no process compromise or injection. | Entire codebase; see [SECURITY_SCOPE.md](SECURITY_SCOPE.md) (out-of-scope: runtime compromise). |
| **Schema compatibility** | Cores pin decision-schema to a compatible range (e.g. `>=0.2.2,<0.3`); no unsupported version mix. | CI (INV-CI-PIN-1); tests (e.g. `test_invariant_schema_pin_minor_2`, `test_schema_dependency`). |
| **No core↔core dependency** | Cores depend only on decision-schema; no direct core-to-core imports. | INV-CORE-DEP-1; pyproject; `test_invariant_2_no_cross_core_imports` per core. |
| **Caller supplies context** | Context (e.g. `now_ms`, ops state) is supplied by the caller; pipeline does not fetch external services. | Harness contract: `run_one_step(state, context, now_ms, ...)`. |
| **Single-step ordering** | Pipeline order is fixed: propose → ops → modulate → packet → report. | Harness `run_one_step.py`; no reordering in this reference implementation. |

---

## 2. Intended guarantees

| Guarantee | Short description | Evidence |
|-----------|-------------------|----------|
| **Fail-closed** | On exception or guard deny: `allowed=False`, action HOLD/STOP, fail_closed marker set. | [FORMALISATION_NOTE.md](FORMALISATION_NOTE.md); tests in §3 below. |
| **Kill-switch dominance** | Ops-health kill-switch can force deny regardless of MDM proposal. | Harness `test_invariant_h2_kill_switch_dominance.py`; ops-health `test_kill_switch.py`. |
| **Contract SSOT** | decision-schema is the single source of truth for types and packet shape; versions aligned. | `check_release_alignment.py`; schema compat tests; INV-REL-SSOT-2. |
| **Traceability** | Every key written to `PacketV2.external` is registered in trace registry. | decision-schema `test_invariant_t1_trace_key_registry.py`; harness `test_invariant_t1_harness_external_keys_registered.py`. |
| **No secrets in repo** | No secret/PII pattern in committed files. | INV-SEC-RED-1; gitleaks in CI. |

---

## 3. Critical scenarios → tests

| Scenario | What we validate | Test(s) |
|----------|------------------|---------|
| **Exception in propose** | Harness returns deny, HOLD, packet has `harness.fail_closed`. | harness `test_invariant_h4_fail_closed_propagation.py` → `test_fail_closed_on_exception_proposal` |
| **Exception in modulate** | Same: deny, HOLD, fail_closed in packet. | harness `test_invariant_h4_fail_closed_propagation.py` → `test_fail_closed_on_exception_modulate` |
| **Kill-switch active** | Final decision is deny even if proposal was ACT. | harness `test_invariant_h2_kill_switch_dominance.py`; ops-health `test_kill_switch.py` |
| **Executor exception** | Report has `fail_closed=True`; no execution. | execution-orchestration `test_invariant_exe_fail_closed.py` |
| **Executor timeout** | Report has `fail_closed=True` when exceeding max_total_time_ms. | execution-orchestration `test_invariant_exe_boundedness.py` |
| **Schema version mismatch** | Cores pin schema minor; compat checked. | Per-core `test_invariant_schema_pin_minor_2`, `test_schema_dependency` |
| **Unregistered external key** | Strict validation fails if key not in registry. | schema `test_invariant_t1_trace_key_registry`; harness `test_invariant_t1_harness_external_keys_registered` |
| **E2E smoke** | Full pipeline (propose → ops → modulate → report) runs without error on minimal input. | harness `test_end_to_end_smoke.py`, `test_fullstack_e2e_report.py` |

---

## 4. Optional: one reproducible experiment

**Experiment:** “Fail-closed latency overhead and correctness.”

**Goal:** Under a single run, (1) trigger the fail-closed path (e.g. exception in propose) and (2) assert the outputs and that latency is bounded (e.g. &lt; 5 s on a typical dev machine).

**How to run (by hand or script):**

1. From workspace root, install and run harness tests that exercise fail-closed:
   ```bash
   cd decision-ecosystem-integration-harness
   pytest tests/test_invariant_h4_fail_closed_propagation.py -v
   ```
2. Optionally, run the full ecosystem test and confirm all pass (including fail-closed tests):
   ```bash
   cd decision-ecosystem-docs
   python tools/ecosystem.py --workspace <parent-dir> test
   ```

**Expected result:** All tests pass; `FinalDecision(allowed=False, action=HOLD)` and `packet.external["harness.fail_closed"] == True` in the exception cases. No formal latency SLO is asserted; the experiment establishes that the fail-closed path is executable and observable.

**Reproducibility:** Use a snapshot (tags or SHAs) per [REPRODUCIBILITY.md](REPRODUCIBILITY.md); run on a fixed Python version (e.g. 3.11 or 3.12 as in CI).

---

## 5. What validation does not cover

- **Exhaustive state space:** We do not model-check or prove the predicate over all inputs.
- **Performance SLOs:** No formal latency or throughput guarantees; CI runs tests in a bounded time.
- **Fault injection beyond exceptions:** We do not systematically inject e.g. corrupted context or schema version mismatch at runtime in CI (only structural/compat tests).

---

**Last updated:** 2026-02  
**Invariant:** INV-VALID-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
