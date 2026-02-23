<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# New Cores Research — Market Landscape and Ecosystem-Aligned Candidates

**Purpose:** Research and recommend **new cores** that can be added to the Decision Ecosystem while preserving a **coherent, compatible** architecture. Market examples inform design; the target is a **unified ecosystem** where every core depends only on decision-schema and fits the existing pipeline.

**Scope:** Cores that (1) depend only on `decision-schema`, (2) consume/produce `PacketV2` or integration context, (3) are domain-agnostic at the contract level, (4) support fail-closed semantics where applicable, and (5) extend trace keys only via the SSOT registry (PARAMETER_INDEX).

**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md, CORE_REPO_STANDARDS.md, RND_FUTURE_DIRECTIONS_AND_REASONS.md, PARAMETER_INDEX (decision-schema).

---

## 1. Executive summary

- **Market:** Policy/decision engines (OPA, Swiftward), ML fairness (SageMaker Clarify, TF Fairness Indicators), feature/experimentation (LaunchDarkly, Optimizely, Harness), regulatory audit (FINOS AI Governance, lending compliance), and cost-aware systems (BoTorch, API cost optimization) all provide **components** we can map to **guard**, **post-report**, or **context-enrichment** roles.
- **Ecosystem fit:** New cores must be **schema-only**, **no core↔core**, and use **registered context/trace keys**. They can sit as **guards** (proposal → allow/deny), **report enhancers** (packet → export/artefact), or **context producers** (caller supplies context; core logic can live in harness or a thin core).
- **Recommended candidates:** (1) **Fairness-guard core**, (2) **Cost-utility core**, (3) **Compliance-audit core**, (4) **Arbitration core**, (5) **Experimentation-context core**. Each is scoped to avoid cross-core dependencies and to use only PacketV2 + context + schema types.

---

## 2. Market landscape

### 2.1 Policy and decision engines

| System | Description | Relevance to ecosystem |
|--------|-------------|------------------------|
| **Open Policy Agent (OPA)** | CNCF policy engine; Rego rules; decision logging with `decision_id`, W3C trace-context. | **Audit/trace:** Our trace keys and PacketV2 already give a similar audit surface. A **compliance-audit core** could export PacketV2 + report to an OPA-style log format or to regulators. |
| **Swiftward** | Self-hosted policy engine for Trust & Safety; A/B testing, replay, full audit trails. | **Experimentation + audit:** “Experimentation-context” core could provide variant/experiment_id in context; harness or evaluation core consumes it. No need to replicate full A/B platform. |

### 2.2 ML fairness and bias

| System | Description | Relevance to ecosystem |
|--------|-------------|------------------------|
| **SageMaker Clarify** | Pre/post-training bias, feature attributions, bias drift in production. | **Guard:** A **fairness-guard core** could take proposal + input (or slices), compute domain-agnostic “fairness signals” (e.g. per-group metrics in `external`), and allow/deny. Metrics stay in schema/external; no ML runtime in core. |
| **TensorFlow Fairness Indicators** | Slice-based fairness metrics, confidence intervals. | Same as above: fairness core consumes proposal + context, writes to `external` with **registered** keys, and can deny. |

### 2.3 Feature flags and experimentation

| System | Description | Relevance to ecosystem |
|--------|-------------|------------------------|
| **LaunchDarkly / Optimizely / Harness** | Feature flags, A/B, gradual rollouts, stats. | **Context only:** An **experimentation-context core** (or harness step) could resolve variant/flag from external service and put `experiment_id`, `variant` in context; DMC or evaluation can use them. Core = thin adapter: context in, context out. |

### 2.4 Regulatory compliance and audit

| Source | Description | Relevance to ecosystem |
|--------|-------------|------------------------|
| **FINOS AI Governance Framework** | Tiers 0–3: from no retention to tamper-evident, real-time decision tracking, explainability. | **Compliance-audit core:** Consumes PacketV2 + report (+ optional explanation), produces **audit artefact** (e.g. JSON/PDF for regulators). No policy logic; just formatting and optional signing/checksums. |
| **Lending / CFPB** | Record retention, audit trail from initiation to disposition. | Same: compliance-audit core can export “decision packet + report” as the audit record. |

### 2.5 Cost and utility

| System | Description | Relevance to ecosystem |
|--------|-------------|------------------------|
| **BoTorch cost-aware utility** | Cost models, inverse-cost weighting, multi-fidelity. | **Cost-utility core:** Given proposal + context (e.g. `cost_estimate`, `budget_remaining`), can **allow/deny** or **adjust** (e.g. via a modulation-like contract: proposal in, proposal out with cost metadata in external). Domain-agnostic: “cost” is numeric; semantics in adapters. |
| **API cost optimization** | Model selection, token minimization, batching. | Same: cost core can gate or annotate decisions based on cost context. |

---

## 3. Ecosystem compatibility criteria

Any new core **must** satisfy the following (from ECOSYSTEM_GATES_AND_INVARIANTS and CORE_REPO_STANDARDS):

| Criterion | Requirement |
|-----------|-------------|
| **INV-CORE-DEP-1** | Depends **only** on `decision-schema` (no dependency on mdm-engine, DMC, ops-health, etc.). |
| **Schema contract** | Consumes/emits only types from decision-schema (e.g. Proposal, PacketV2, Report, integration context dict). |
| **Domain-agnostic** | Public API and types are not tied to a single vertical (e.g. “lending”); verticals use adapters. |
| **Context/trace keys** | New keys in `context` or `PacketV2.external` / trace registry must be documented in **PARAMETER_INDEX** (or equivalent SSOT in decision-schema). |
| **Fail-closed** | If the core can “deny” or “override”, it should follow the same fail-closed semantics as the rest of the pipeline (e.g. on error, safe default). |
| **Repo standards** | INV-GITIGNORE-1, INV-COMMIT-1, tests, release notes, as per CORE_REPO_STANDARDS. |

**Pipeline placement (reminder):** Current flow is **propose → ops (kill-switch) → modulate → PacketV2 → report**; execution is optional and invoked by the caller. New cores can:

- **Guard:** After propose (or after ops), before or inside modulation: input = proposal + context, output = allow/deny or modified proposal; denial flows into existing “deny” path.
- **Enricher:** Add keys to context before modulation (e.g. experimentation-context).
- **Post-report:** Consume PacketV2 + Report (and optional explanation), produce audit/compliance artefact.

---

## 4. Proposed new cores (candidates)

### 4.1 Fairness-guard core

| Attribute | Description |
|-----------|-------------|
| **Name** | `fairness-guard-core` (or `fairness-core`) |
| **Purpose** | Act as a **guard** that allows or denies a proposal based on configurable fairness constraints (e.g. per-group metrics, thresholds). Does not train models; consumes proposal + input/external and optionally slice/group info from context. |
| **Market parallel** | SageMaker Clarify, TensorFlow Fairness Indicators (guard slice of functionality). |
| **Pipeline place** | After propose (and optionally after ops). Input: Proposal + context (e.g. `input`, `external`). Output: allow or deny; if allow, can attach fairness metrics to context/external for trace. |
| **Schema compatibility** | Uses only Proposal, context dict, and registered keys in PARAMETER_INDEX (e.g. extend with `fairness_ok`, `fairness_metrics`). No new core↔core deps. |
| **Fail-closed** | On error or missing data, guard can be configured to deny (safe default) or allow (depending on policy). |

### 4.2 Cost-utility core

| Attribute | Description |
|-----------|-------------|
| **Name** | `cost-utility-core` |
| **Purpose** | Gate or annotate decisions by cost/utility: e.g. reject if estimated cost > budget, or attach cost metadata to context for downstream. Domain-agnostic: “cost” and “budget” are numbers or structured entries in context. |
| **Market parallel** | BoTorch cost-aware utility, API cost optimization patterns. |
| **Pipeline place** | Guard-style: proposal + context (e.g. `cost_estimate`, `budget_remaining`) → allow/deny or pass-through with cost in external. |
| **Schema compatibility** | Only schema types and registered context keys (e.g. `cost_estimate`, `budget_remaining`, `cost_utility_ok`). |
| **Fail-closed** | On error, configurable: deny or allow. |

### 4.3 Compliance-audit core

| Attribute | Description |
|-----------|-------------|
| **Name** | `compliance-audit-core` |
| **Purpose** | Produce **audit artefacts** from PacketV2 + Report (+ optional explanation): e.g. JSON for regulators, PDF summary, or tamper-evident digest. No policy logic; pure export/format. |
| **Market parallel** | FINOS AI Governance (audit trail), lending record retention. |
| **Pipeline place** | **Post-report:** consumes PacketV2, Report, optional explanation; outputs file or structured payload. Can be invoked from harness after report. |
| **Schema compatibility** | Consumes only PacketV2, Report, and optional explanation type from schema (or explainability-audit). No new core↔core: explanation can be passed as a string or schema-defined type. |
| **Fail-closed** | If export fails, caller can retry or log; core does not change the decision path. |

### 4.4 Arbitration core

| Attribute | Description |
|-----------|-------------|
| **Name** | `arbitration-core` (or `multi-objective-arbitration-core`) |
| **Purpose** | When multiple objectives or signals exist (e.g. from multiple proposals or from DMC + fairness + cost), **arbitrate** into a single final decision. Domain-agnostic: inputs are proposals or scores; output is one chosen or merged decision. |
| **Market parallel** | Multi-criteria decision-making (MCDM), ensemble/arbitration in ML. |
| **Pipeline place** | Could sit **after** modulation: multiple candidate outcomes → arbitration → single Proposal or FinalDecision. Or used only in verticals that need multi-objective resolution. |
| **Schema compatibility** | Input: list of Proposal or similar; output: Proposal or FinalDecision. All from schema. |
| **Fail-closed** | On error, e.g. return first candidate or a configured default. |

### 4.5 Experimentation-context core

| Attribute | Description |
|-----------|-------------|
| **Name** | `experimentation-context-core` |
| **Purpose** | Resolve **experiment/variant** from external feature-flag or A/B service and put result into integration context (e.g. `experiment_id`, `variant`). Downstream cores (DMC, evaluation) use context only; no A/B logic inside other cores. |
| **Market parallel** | LaunchDarkly, Optimizely, Harness feature/experimentation. |
| **Pipeline place** | **Enricher:** before or at start of pipeline; caller or harness calls this core to get context fragment, then passes full context to propose/modulate. |
| **Schema compatibility** | Only context keys; extend PARAMETER_INDEX with `experiment_id`, `variant`, etc. No Proposal/PacketV2 change required. |
| **Fail-closed** | If experiment service fails, core returns default variant or “control”; context always gets some value. |

---

## 5. Trace and context keys (SSOT)

New cores **must** register any new **context** or **PacketV2.external** / **trace** keys in the SSOT (PARAMETER_INDEX in decision-schema). Suggested keys (to be added when cores are implemented):

| Key | Type | Meaning | Producer | Consumer |
|-----|------|---------|----------|----------|
| fairness_ok | bool | Fairness guard passed | fairness-guard-core | harness, evaluation |
| fairness_metrics | dict | Per-slice/metric snapshot (redactable) | fairness-guard-core | evaluation, compliance-audit |
| cost_estimate | number | Estimated cost for this decision | caller / cost-utility-core | cost-utility-core |
| budget_remaining | number | Remaining budget | caller | cost-utility-core |
| cost_utility_ok | bool | Cost guard passed | cost-utility-core | harness |
| experiment_id | string | Experiment identifier | experimentation-context-core | DMC, evaluation |
| variant | string | Assigned variant (e.g. control, treatment) | experimentation-context-core | DMC, evaluation |

Compliance-audit core typically does not add new context keys; it **consumes** existing PacketV2 and report fields.

---

## 6. Onboarding checklist for a new core

Before adding a new core to REPO_REGISTRY and the pipeline:

1. **Dependency:** Repo depends only on `decision-schema` (no other core).
2. **Contract:** Public API uses only schema types (Proposal, PacketV2, Report, context dict).
3. **Keys:** All new context/trace/external keys documented in PARAMETER_INDEX (or schema docs) and follow naming rules.
4. **Fail-closed:** Behaviour on error documented; default is safe where applicable.
5. **Tests:** Unit tests and, if applicable, integration test with harness (optional import).
6. **Standards:** INV-GITIGNORE-1, INV-COMMIT-1; release notes and version in pyproject + tag.
7. **Harness:** If integrated into harness, use optional import so harness runs without the new core installed.
8. **Docs:** Short README, architecture note if needed, and update REPO_REGISTRY + ECOSYSTEM_CONTRACT_MATRIX if applicable.

---

## 7. Overlap with existing cores (when to extend vs new repo)

**Short answer:** Most of the “new core” ideas are **the same mechanism** that existing cores already provide. You can implement them as **extensions of current cores** and only add a new repo if you have a strong reason (e.g. separate ownership, release cycle, or research isolation).

| Proposed “new core” | What already exists | Recommendation |
|---------------------|---------------------|-----------------|
| **Fairness-guard** | **DMC** already has a guard pattern: `(context, policy) → (ok, code)`. Caller (or adapter) computes fairness metrics and sets e.g. `fairness_ok` / `fairness_metrics` in context; DMC gets a **fairness_guard** that reads those keys. Same as ops_health, rate_limit, circuit_breaker. | **Extend DMC:** Add `fairness_guard` (and optional context keys in PARAMETER_INDEX). No new repo unless you want fairness in a separate package. |
| **Cost-utility** | **DMC** example (e.g. `docs/examples/example_domain_legacy_v0/guards.py`) already has a **cost_guard** pattern. Generic DMC could add a **cost_guard** that reads `cost_estimate`, `budget_remaining` from context. | **Extend DMC:** Add generic cost_guard; register context keys. No new repo needed. |
| **Compliance-audit** | **Explainability-audit-core** already produces explanations and guard-chain reason codes. “Export for regulators” (JSON/PDF/digest) is just a **formatting step** on top of PacketV2 + Report + Explanation. | **Extend explainability-audit-core:** e.g. `export_audit_artifact(packet, report, explanation, format="json"|"pdf")`. No new repo needed. |
| **Arbitration** | Pipeline today is **one proposal → one decision**. We do **not** have “multiple proposals → pick one”. | **Only real new capability** if you need multi-source/multi-objective decisions. Then either: a new small core (arbitration) or a harness step that calls a single “arbitrate(proposals)” function. New repo only if you want it fully isolated. |
| **Experimentation-context** | Context is a dict; **caller** or **harness** can set `experiment_id`, `variant` from any feature-flag or A/B service. No decision logic required. | **No new core.** Document `experiment_id` / `variant` in PARAMETER_INDEX; implement resolution in harness or caller. |

**Conclusion:** The ecosystem already covers **guards** (DMC), **explanation and audit trail** (explainability-audit), and **context-driven behaviour**. “New cores” in §4 are mostly **new domains of the same building blocks** (more guards, more export formats). Prefer **extending existing cores**; introduce a **new repo** only when you need separate versioning, ownership, or a genuinely new capability (e.g. arbitration with multiple proposals).

---

## 8. Summary table

| Core | Role | Pipeline position | Main output |
|------|------|-------------------|-------------|
| fairness-guard-core | Guard | After propose/ops | allow/deny + optional fairness_metrics in context |
| cost-utility-core | Guard | After propose/ops | allow/deny or pass-through + cost in context |
| compliance-audit-core | Post-report | After report | Audit artefact (JSON/PDF/digest) |
| arbitration-core | Resolver | After modulation (or vertical-specific) | Single Proposal/FinalDecision |
| experimentation-context-core | Context enricher | Before propose | context + experiment_id, variant |

This research aligns with RND_FUTURE_DIRECTIONS_AND_REASONS.md (§3) and keeps the ecosystem **coherent and compatible**: one SSOT (decision-schema), no core-to-core dependencies, and clear pipeline roles for each new core.

---

**Last updated:** 2026-02-19  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md, RND_FUTURE_DIRECTIONS_AND_REASONS.md, PARAMETER_INDEX (decision-schema), CORE_REPO_STANDARDS.md

---

*See §7 for overlap with existing cores and when to extend vs add a new repo.*
