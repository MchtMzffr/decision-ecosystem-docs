<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Core Code Analysis — Structure, Inconsistencies, and Recommendations

**Purpose:** Analysis of **core codebases and harness** (not rules/roadmap): structure, consistency, and concrete gaps with recommendations.  
**Scope:** decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, explainability-audit-core, decision-ecosystem-integration-harness.  
**Date:** 2026-02

---

## 1. Executive summary

The cores are **architecturally consistent**: all depend only on decision-schema, use the same types (Action, Proposal, FinalDecision, PacketV2), and follow fail-closed where required. The main **gaps** are: (1) **decision-schema**: input mutation in `from_dict` and dead code in `types.py`; (2) **harness**: execution-orchestration is not integrated; OpsState is only partially filled from context; (3) **execution-orchestration**: `timeout_per_action_ms` is never applied to a single executor call; (4) **evaluation-calibration**: weak typing for `build_report(packets)`; (5) **explainability**: packet treated as dict-like with potential type drift. Below: per-repo summary, then **inconsistencies and gaps**, then **recommendations**.

---

## 2. Per-repo structure (one sentence)

| Repo | Architecture (one sentence) |
|------|------------------------------|
| **decision-schema** | Single shared contract package: types (Action, Proposal, FinalDecision, MismatchInfo), PacketV2, trace registry, compat. |
| **mdm-engine** | Features → Proposal via reference model + optional private hook; execution/trace/security as separate layers. |
| **decision-modulation-core** | Proposal + policy + context → fixed guard order → FinalDecision + MismatchInfo; fail-closed on exception. |
| **ops-health-core** | Window-based health score and kill-switch → OpsSignal; output merged into context (ops_deny_actions, ops_state, ops_cooldown_until_ms) for DMC/harness. |
| **evaluation-calibration-core** | List of PacketV2 → metrics + invariant checks + schema contract → Report (read-only packet consumption). |
| **execution-orchestration-core** | FinalDecision + context + policy + executor callable → ExecutionReport; bounded by max_total_time_ms and retries; fail-closed on exception/timeout. |
| **explainability-audit-core** | allowed/guard_chain or PacketV2 → reason codes + evidence → ExplanationArtifact; schema-shape only. |
| **harness** | run_one_step: propose → ops → modulate → packet → report (+ optional explanation); no execution step. |

---

## 3. Inconsistencies and gaps (code and structure)

### 3.1 decision-schema

| Issue | Where | Detail |
|-------|--------|--------|
| **Input mutation** | `packet_v2.py` `from_dict()` | `data.pop("schema_version", __version__)` mutates the caller’s dict. If the same dict is passed twice (e.g. in a loop or shared ref), the second call gets wrong/missing schema_version. |
| **Dead code** | `types.py` | `clamp_confidence()` and `ensure_non_empty_reasons()` are defined but never used anywhere in the repo or by cores. |

**Consistency:** No cross-core or schema violations; types and PacketV2 are used consistently.

---

### 3.2 mdm-engine

| Issue | Where | Detail |
|-------|--------|--------|
| **Shallow public API** | Package `__init__.py` | Only `__version__` is exported; consumers must import `mdm_engine.mdm.decision_engine.DecisionEngine` (and similar) explicitly. Acceptable but not a single entry point. |
| **Fail-closed reason standard** | Private hook / error paths | Exception path uses HOLD + `private_hook_error`; not aligned with a single documented “fail_closed reason code” set used across all cores (e.g. harness uses `fail_closed_exception`). |

**Consistency:** Proposal/Action and schema usage are correct.

---

### 3.3 decision-modulation-core

| Issue | Where | Detail |
|-------|--------|--------|
| **Silent defaults for missing context** | Guard implementations, context access | Context keys (e.g. `errors_in_window`, `steps_in_window`, `ops_deny_actions`) are read with `.get(..., 0)` or similar. Missing keys imply “no signal,” so guards may allow when the caller simply did not provide data. Behaviour is deterministic but not self-documenting. |

**Consistency:** Only decision_schema used; guard order and fail-closed behaviour are consistent.

---

### 3.4 ops-health-core

| Issue | Where | Detail |
|-------|--------|--------|
| **OpsState only partially fed from harness** | Harness `_update_ops()` | OpsState is built with `error_timestamps`, `rate_limit_timestamps`, `ops_cooldown_until_ms` from context. **latency_timestamps** and **reconnect_timestamps** are not passed; they remain empty. Health formulas that depend on latency/reconnect windows will see zeros; behaviour is partial, not wrong, but undocumented. |

**Consistency:** Schema (Action, compat) and context contract (ops_deny_actions, ops_state, ops_cooldown_until_ms) are aligned with DMC and harness.

---

### 3.5 evaluation-calibration-core

| Issue | Where | Detail |
|-------|--------|--------|
| **Weak typing for packets** | `report/builder.py` `build_report(packets, ...)` | Parameter is `list`; not `list[PacketV2]` or a Protocol. Duck-typing works today but is fragile if a different “packet-like” type is passed later. |

**Consistency:** PacketV2 fields used (run_id, step, input, external, mdm, final_action, latency_ms, mismatch, schema_version) match schema; expected_schema_minor=2 is consistent.

---

### 3.6 execution-orchestration-core

| Issue | Where | Detail |
|-------|--------|--------|
| **timeout_per_action_ms not enforced** | `orchestrator.py` execution loop | `TimeoutPolicy` has `timeout_per_action_ms` and it is stored in `ExecutionPlan`, but the loop only checks **max_total_time_ms**. Each `executor(action, context)` call is **not** limited by `timeout_per_action_ms`; the orchestrator does not interrupt or time out a single action. So “per-action timeout” exists in the model but not in behaviour. |

**Consistency:** Action/FinalDecision from schema; exec.* trace keys in registry; fail-closed and boundedness (max_total_time_ms, retries) are implemented.

---

### 3.7 explainability-audit-core

| Issue | Where | Detail |
|-------|--------|--------|
| **Packet as dict-like** | `explain_from_packet(packet)` | Uses `getattr(packet, "run_id", "")` and `.get("reason_codes")` on mismatch; works for both PacketV2 and dict. If PacketV2 or harness serialization changes (e.g. mismatch shape), behaviour can drift without type errors. |
| **Namespaced reason_codes** | Mapping to ReasonCode enum | DMC and other cores may emit namespaced or custom reason_codes; explainer maps known ones and falls back to UNKNOWN. Not wrong but worth documenting so that new reason_codes are explicitly handled or left as UNKNOWN. |

**Consistency:** Only schema shape is assumed; no direct schema import at runtime (TYPE_CHECKING only).

---

### 3.8 decision-ecosystem-integration-harness

| Issue | Where | Detail |
|-------|--------|--------|
| **Execution not integrated** | `run_one_step()` | Pipeline is propose → ops → modulate → packet → report. **Execution-orchestration-core is never called.** There is no “execute final_decision” step and no execution exception path in the harness. Full “decision + execution” E2E is only possible outside the harness (e.g. caller runs executor separately). |
| **OpsState partially filled** | `_update_ops()` | As in §3.4: latency_timestamps and reconnect_timestamps are not taken from context, so ops-health sees them empty. |
| **Report type** | Return type and Report model | Return is `tuple[FinalDecision, PacketV2, Report | None]`. Report is from eval_calibration_core; `explanation` is attached via `setattr(report, "explanation", ...)`. The Report type does not declare `explanation`; usage is optional and type-weak. |

**Consistency:** Core wiring (mdm, ops-health, DMC, eval, explainability) and packet building match schema and contracts.

---

## 4. Recommendations (concrete)

### 4.1 decision-schema

- **from_dict mutation:** Use `schema_version = data.get("schema_version", __version__)` and do not mutate `data`. If you need to strip keys for `**data`, use a copy: `data_copy = {k: v for k, v in data.items() if k != "schema_version"}` and pass `schema_version` and `data_copy` (or equivalent) so the caller’s dict is unchanged.
- **Dead code:** Remove `clamp_confidence` and `ensure_non_empty_reasons` from `types.py`, or use them (e.g. in Proposal construction / validation) and document. Prefer removal if there is no use case.

### 4.2 mdm-engine

- **Public API:** Optionally add a thin facade in `mdm_engine/__init__.py`, e.g. `propose(features) -> Proposal` that delegates to DecisionEngine, so that “single entry point” is clear.
- **Fail-closed reason:** Document the set of reason strings used on error (e.g. `private_hook_error`, `fail_closed_exception`) in a short doc or PARAMETER_INDEX so all cores align.

### 4.3 decision-modulation-core

- **Context defaults:** Document in integration/release notes which context keys each guard expects and what default is used when missing (e.g. “errors_in_window missing → 0”). Optionally add a “required context keys” list per guard for clarity.

### 4.4 ops-health-core and harness

- **OpsState completeness:** Document that when the harness builds OpsState, only `error_timestamps`, `rate_limit_timestamps`, and `ops_cooldown_until_ms` are taken from context; latency and reconnect windows are left empty unless the caller merges them into context before `run_one_step`. If you want full health behaviour in the harness, extend `_update_ops` to pass `context.get("latency_timestamps", [])` and `context.get("reconnect_timestamps", [])` into OpsState (and document the context contract).

### 4.5 evaluation-calibration-core

- **Typing:** Change `build_report(packets: list, ...)` to `build_report(packets: list[PacketV2], ...)` (or a Protocol that has the required attributes). Add the appropriate import (e.g. from decision_schema) so that type checkers and callers have a clear contract.

### 4.6 execution-orchestration-core

- **Per-action timeout:** Either (a) implement per-action timeout (e.g. run `executor(action, context)` in a thread/process with a timeout and enforce `timeout_per_action_ms`), or (b) document that `timeout_per_action_ms` is advisory and only `max_total_time_ms` is enforced by the orchestrator, and rename or annotate the field to avoid confusion.

### 4.7 explainability-audit-core

- **Packet contract:** Document the expected shape of `packet` (and nested `mismatch`) for `explain_from_packet` (e.g. in INTEGRATION_GUIDE or docstring). Prefer a minimal Protocol or TypedDict if you want static checks without hard dependency on PacketV2.
- **Reason code mapping:** Document which reason_codes map to which ReasonCode and that any unknown/namespaced code maps to UNKNOWN.

### 4.8 harness

- **Execution step:** If “decision + execution” in one pipeline is a goal, add an optional execution phase after modulate: e.g. when execution-orchestration-core is installed and a policy/executor are provided, call the orchestrator with `final_decision` and context, then attach execution report to packet or report. Define behaviour when execution fails (e.g. report.fail_closed and optional packet key).
- **Report.explanation:** If the Report type is owned by eval_calibration_core, add an optional `explanation: dict | None = None` (or a small typed structure) so that the harness does not rely on setattr and type checkers are happy.

---

## 5. Summary table

| Repo | Structural consistency | Main gap / risk | Priority fix |
|------|------------------------|-----------------|--------------|
| decision-schema | Good | from_dict mutates input; dead code in types | Fix from_dict; remove or use dead code |
| mdm-engine | Good | Shallow __init__; fail-closed reason not standardized | Optional facade; document reason codes |
| decision-modulation-core | Good | Missing context keys default silently | Document required/default context |
| ops-health-core | Good | OpsState in harness missing latency/reconnect | Document or extend harness context → OpsState |
| evaluation-calibration-core | Good | build_report(packets) untyped | Add list[PacketV2] or Protocol |
| execution-orchestration-core | Good | timeout_per_action_ms unused in loop | Implement or document as advisory |
| explainability-audit-core | Good | Packet dict-like; reason_codes → UNKNOWN | Document contract and mapping |
| harness | Good | No execution step; OpsState partial; Report.explanation untyped | Optional execute phase; document OpsState; type explanation |

---

---

## 6. Applied changes (recommendations implemented)

| Repo | Change |
|------|--------|
| **decision-schema** | `from_dict()` no longer mutates input (use `data.get` + copy). Removed unused `clamp_confidence` and `ensure_non_empty_reasons` from types.py. |
| **mdm-engine** | Added `propose(features, confidence_threshold=0.5)` facade in `__init__.py`; docstring notes fail-closed reason codes. |
| **evaluation-calibration-core** | Report model: added `explanation: dict \| None = None` and included in `to_dict()`. build_report: parameter typed as `list[PacketV2]` (TYPE_CHECKING). |
| **execution-orchestration-core** | TimeoutPolicy docstring: `timeout_per_action_ms` is advisory (not enforced per executor call); `max_total_time_ms` is enforced. |
| **explainability-audit-core** | explain_from_packet docstring: expected packet shape and reason code mapping (unknown → UNKNOWN). |
| **decision-modulation-core** | modulate() docstring: context keys and "missing keys use default per guard". |
| **harness** | _update_ops: OpsState now receives `latency_timestamps` and `reconnect_timestamps` from context. _attach_explanation: use `report.explanation =` (Report has the field). run_one_step docstring: execution not in pipeline; caller may run execute() separately. |
| **docs** | ECOSYSTEM_COMPLIANCE_AND_FORMULA_AUDIT: confidence bounds described via Proposal.__post_init__, not clamp_confidence. |

**Not implemented (by design):** Optional execution step inside run_one_step (would require API change: executor callable + policy). Documented in run_one_step docstring instead.

---

**Last updated:** 2026-02  
**References:** Subagent exploration (core structure); ECOSYSTEM_GATES_AND_INVARIANTS.md, EVIDENCE_SUMMARY.md, FORMALISATION_NOTE.md
