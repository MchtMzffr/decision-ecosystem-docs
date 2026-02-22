<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Formalisation Note — Fail-Closed and Pipeline (INV-FORMAL-1)

**Purpose:** Give **precise, checkable** definitions for **fail-closed** and the **pipeline** so that implementation can be verified and compared to literature. Per INV-FORMAL-1 and [ACADEMIC_CRITIQUE_AND_REASONS.md](ACADEMIC_CRITIQUE_AND_REASONS.md).

**Scope:** Integration harness single-step pipeline (propose → ops → modulate → PacketV2 → report) and components that contribute to the final decision. This note is normative for what “fail-closed” means in this project.

---

## 1. Pipeline state and steps

**Pipeline (single step):**

1. **Propose** — MDM (mdm-engine) produces a `Proposal` (action, confidence, reasons, params).
2. **Ops** — ops-health-core updates kill-switch and returns ops signal (e.g. `ops_deny_actions`, `ops_state`); context is updated.
3. **Modulate** — decision-modulation-core (DMC) takes proposal + context and returns `FinalDecision` (action, allowed, reasons, mismatch).
4. **Packet** — Build `PacketV2` (run_id, step, input, external, mdm, final_action, latency_ms, mismatch).
5. **Report** — evaluation-calibration-core builds report from packet(s); optional explainability attaches explanation.

**Observable state (outputs):**

- `FinalDecision`: `action` ∈ { HOLD, ACT, EXIT, CANCEL, STOP }, `allowed` ∈ { True, False }, `reasons`, `mismatch`.
- `PacketV2`: includes `final_action`, `external` (e.g. `harness.fail_closed`, `ops_state`).
- Report: may include `fail_closed` (execution-orchestration) or equivalent.

**Types:** SSOT in decision-schema: `Action`, `Proposal`, `FinalDecision`, `MismatchInfo`, `PacketV2`. See decision-schema `docs/ARCHITECTURE.md`.

---

## 2. Fail-closed (predicate)

**Definition (operational):**  
Whenever an **exception** occurs in the pipeline or a **guard/kill-switch** forces a deny, the system shall produce a **safe** outcome: no irreversible action is taken, and the observable outputs indicate that the decision was not allowed.

**Predicate (postcondition):**

- Let \( \mathit{exception} \) = “an exception was raised during propose, ops, modulate, or packet/report build”.
- Let \( \mathit{guard\_deny} \) = “ops kill-switch or DMC guard set allowed to False (e.g. ops_deny_actions, mismatch)”.
- **Fail-closed predicate:**  
  \( \mathit{exception} \lor \mathit{guard\_deny} \;\Rightarrow\; \mathit{safe\_output} \)

Where **safe_output** is:

1. **FinalDecision:** `allowed == False` and `action` ∈ { `HOLD`, `STOP` } (no ACT/EXIT when in fail-closed path).
2. **Packet:** `packet.external` contains a registered fail-closed marker (e.g. `harness.fail_closed == True`) when the failure occurred in the harness; execution-core may set `report.fail_closed`.
3. **No silent success:** The caller can distinguish “deny because of policy” from “deny because of failure” via reasons and the fail_closed marker.

**Components in scope:**

- **Harness** `run_one_step`: on any exception → `FinalDecision(allowed=False, action=HOLD)`, `packet.external["harness.fail_closed"] = True`. See harness `run_one_step.py` and [EVIDENCE_SUMMARY.md](EVIDENCE_SUMMARY.md).
- **DMC:** When ops_deny_actions or guard logic denies → `FinalDecision(allowed=False, …)`.
- **Execution-orchestration:** On exception or timeout → `report.fail_closed = True`; no execution performed.

---

## 3. Tests that verify the predicate

| Condition | Test (file) | What is checked |
|-----------|-------------|------------------|
| Exception in propose or modulate (harness) | harness `tests/test_invariant_h4_fail_closed_propagation.py` | `FinalDecision(allowed=False, action=HOLD)`, `reasons` contain fail_closed, `packet.external["harness.fail_closed"] == True` |
| Kill-switch denies | harness `tests/test_invariant_h2_kill_switch_dominance.py`; ops-health `test_kill_switch.py` | Ops signal forces deny regardless of proposal |
| Exception / timeout in executor | execution-orchestration `tests/test_invariant_exe_fail_closed.py`, `test_invariant_exe_boundedness.py` | `report.fail_closed is True`; no execution |
| Fail-closed key registered | decision-schema `tests/test_invariant_t1_trace_key_registry.py`; harness `tests/test_invariant_t1_harness_external_keys_registered.py` | `harness.fail_closed` and `exec.fail_closed` in registry; strict validation |

These tests are the **evidence** that the implementation satisfies the fail-closed predicate under the tested scenarios. They do not constitute a proof over all reachable states; they are regression and specification tests.

---

## 4. Domain-agnostic (brief)

**Definition:**  
- **Schema/API:** No domain-specific vocabulary in public types (Action, Proposal, PacketV2 use generic names).  
- **Docs (INV0):** Forbidden lexemes must not appear in README and docs (excl. examples).  

**Not formalised here:** Runtime “no domain logic” is by design and structure (no core↔core, generic keys); no state-machine formalisation in this note.

---

## 5. References

- **Types and contracts:** decision-schema `docs/ARCHITECTURE.md`, `decision_schema/types.py`, `decision_schema/packet_v2.py`
- **Pipeline flow:** harness `harness/run_one_step.py`
- **Evidence and tests:** [EVIDENCE_SUMMARY.md](EVIDENCE_SUMMARY.md), [INVARIANT_TRACEABILITY.md](INVARIANT_TRACEABILITY.md)

---

**Last updated:** 2026-02  
**Invariant:** INV-FORMAL-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
