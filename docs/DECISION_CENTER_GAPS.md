<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Decision Center Completeness — What Exists vs What Makes a “Center”

**Purpose:** Clarify that existing cores are **already global and domain-agnostic**. The gap is not “more cores like them” but **supporting structures** that turn the pipeline into a full **Decision Center** (Karar Merkezi): how it is called, where data lives, how it is configured and operated.

**Audience:** Product and architecture. Aligns with “no duplicate cores” and “decision-schema–integrated support layer”.

---

## 1. Existing cores are already universal

| Core | Role | Scope |
|------|------|--------|
| decision-schema | Contract (types, PacketV2, context/trace registry) | **Global:** any domain |
| mdm-engine | Propose (model → Proposal) | **Global:** any model, any action set |
| ops-health-core | Kill-switch, state, cooldown | **Global:** any ops policy |
| decision-modulation-core | Guards (ops, staleness, rate, circuit breaker, cooldown) | **Global:** domain-agnostic guards; domain logic via context |
| evaluation-calibration-core | Report, metrics, contract check | **Global:** any packet/report |
| execution-orchestration-core | Run actions (outside pipeline) | **Global:** any action type |
| explainability-audit-core | Reason codes, guard chain, explanation | **Global:** any decision |
| integration-harness | Single-step pipeline orchestration | **Global:** propose → ops → modulate → report |

**Conclusion:** The **decision engine** is complete and domain-agnostic. Adding “fairness core”, “cost core” as **separate repos** duplicates the same pattern (guards, context); those belong as **extensions** of DMC or as **context supplied by the caller**, not as new cores. The wrong turn is: “we need more decision-logic cores.” The right question is: **what is missing so that this engine becomes a full Decision Center?**

---

## 2. What is missing: the “center” around the engine

A **Decision Center** in the full sense is not only the pipeline but:

1. **How** external systems and users call it (API / ingress).
2. **Where** decisions, reports, and audit data are stored (persistence / audit trail).
3. **How** policies, models, and tenants are configured (catalog / registry).
4. **How** operators control and observe it (control plane / ops).
5. **How** verticals (lending, hiring, scheduling) plug in without reinventing the wheel (adapters / SDK).

Today we have:

- **Engine:** propose → ops → modulate → PacketV2 → report (and optional explanation, execution). ✓  
- **Caller:** Whoever uses the harness (e.g. a script or service) must import `run_one_step`, build `state` and `context`, and handle the return value. There is **no standard API layer** (e.g. REST/gRPC “decision service”) that the ecosystem provides.
- **Persistence:** PacketV2 and Report are returned in memory. **No ecosystem-owned store** for audit, replay, or analytics; the caller is responsible.
- **Configuration:** Policy and context are passed per call. **No central catalog** for policies, model endpoints, or tenant-specific config that the pipeline reads from.
- **Control plane:** Ops state (e.g. kill-switch) is updated by the caller. **No standard control API or UI** (e.g. “set RED”, “view last N runs”) provided by the ecosystem.
- **Verticals:** Domains use the same harness and schema; there is **no formal adapter layer** (e.g. “lending adapter” that maps domain input → state/context and FinalDecision → domain output) as part of the ecosystem.

So: **the engine is global and complete; the “center” (platform around it) is not.**

---

## 3. Decision-schema–integrated support layer (recommended direction)

What is needed is not “another set of decision cores” but a **support layer** that integrates with decision-schema and the existing pipeline:

| Layer | Purpose | Integrates with |
|-------|---------|------------------|
| **Gateway / API** | Single entry point for “request a decision”: HTTP/gRPC → build state/context → `run_one_step` → return decision/report (and optionally store). | decision-schema (types), harness (`run_one_step`). |
| **Store / audit sink** | Persist PacketV2, Report (and optional explanation) for audit, replay, analytics. Optional: tamper-evident digest. | decision-schema (PacketV2, Report); no change to pipeline logic. |
| **Catalog / registry** | Policies, model endpoints, tenant configs (and optionally feature flags). Pipeline or gateway reads from here to build context and policy. | decision-schema (policy types, context keys); harness or gateway. |
| **Control plane** | Update ops state (e.g. kill-switch, cooldown), view recent runs, health. Can be API + optional UI. | ops-health-core, decision-schema (context keys); harness. |
| **Adapter SDK / reference adapters** | Standard way to map domain input → `state`/`context` and `FinalDecision`/Report → domain output. Reference adapters (e.g. lending, scheduling) prove the center works in every domain. | decision-schema only; no new core↔core. |

These are **not** “more decision logic”; they are **platform components** that make the existing universal engine **callable, storable, configurable, operable, and reusable** across domains.

---

## 4. Do we need a “new core group” for this?

Yes — but as a **support group**, not as duplicates of the current cores.

- **Option A — Separate repos (recommended for clear boundaries):**  
  - e.g. `decision-gateway` (API), `decision-store` (persistence), `decision-catalog` (registry), `decision-control` (control plane), and optionally `decision-adapter-sdk` or reference adapters.  
  - Each depends only on **decision-schema** (and optionally harness as a library). No core↔core. They extend the **ecosystem** without changing the **engine**.

- **Option B — Fewer repos:**  
  - e.g. one “decision-platform” repo that includes gateway + store + control, and a separate “decision-adapters” repo.  
  - Same idea: support layer, schema-only dependency.

- **Option C — Harness extensions:**  
  - Gateway and store could live as optional modules inside the harness repo (e.g. `harness.gateway`, `harness.store`).  
  - Simpler for small deployments; less clear separation for multi-team or multi-tenant.

**Recommendation:** Treat “decision-schema–integrated support layer” as the **next group of repos** (gateway, store, catalog, control, adapters). That completes the **Decision Center** without adding redundant decision logic.

---

## 5. Summary

| Question | Answer |
|----------|--------|
| Are existing cores already global / domain-agnostic? | **Yes.** They are designed for use in any domain. |
| Is building “fairness core”, “cost core” as new cores the right move? | **No.** Same mechanism (guards, context); extend DMC or supply context from caller. |
| What is missing? | **The center around the engine:** API, persistence, catalog, control plane, adapters. |
| Do we need a new group of “cores” that integrate with decision-schema? | **Yes** — as **support/platform** components (gateway, store, catalog, control, adapters), not as more decision-logic cores. |
| Is the Decision Center complete today? | **Engine: yes. Center: no.** Completing it means adding the support layer above. |

---

**Last updated:** 2026-02-19  
**References:** NEW_CORES_RESEARCH.md (§7), REPO_REGISTRY.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, PROJECT_COMPLETION_STATUS.md.

**Where to add these in existing repos and how they should be default for model users:** see **PLATFORM_PLACEMENT_AND_DEFAULTS.md**.
