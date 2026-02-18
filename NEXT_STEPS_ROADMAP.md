<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Next Steps Roadmap — Decision Ecosystem

**Date:** 2026-02-19  
**Current Status:** ✅ Migration Complete, Static Analysis Fixes Applied, Releases Partially Published

---

## P0 — Release Alignment (Tags) — RECOMMENDED

**Rationale:** For each core, `pyproject.toml [project].version` MUST have a matching Git tag/release.
This makes dependency pinning and contract matrices reproducible.

| Repository | pyproject version (main) | Latest tag/release | Next action |
|---|---:|---:|---|
| decision-schema | 0.2.2 | v0.2.1 | **Publish v0.2.2** (tag + release notes) |
| mdm-engine | 0.2.1 | v0.2.1 | OK |
| ops-health-core | 0.1.1 | v0.1.1 | OK |
| evaluation-calibration-core | 0.1.1 | v0.1.1 | OK |
| execution-orchestration-core | 0.1.0 | v0.1.0 | OK |
| decision-modulation-core (dmc-core) | 0.1.0 | (none) | **Publish first release v0.1.0** |

**Source of truth:** pyproject version on `main` + Git tags. Update this table whenever you publish a tag.

**Invariant:** `tag(version) == pyproject.version` for released packages.

---

## P1 — Optional: Ops-Health Latency Windowing

**Task:** Add `latency_timestamps` to `OpsState` for proper window-based pruning.

**Current State:**
- `latency_samples` is timestamp-less
- p95 computed over all samples (not windowed)

**Implementation Sketch:**
1. Add `latency_timestamps: list[int]` to `OpsState` (default empty).
2. Update scorer to prune latency samples by timestamp within the configured window.
3. Add tests covering pruning correctness and percentile stability.

**Effort:** Medium (state-model change + tests)

---

## Completed (Recent)

### P2 — DMC-Core Dependency Cleanup (F7) — ✅ DONE
- Removed unused `numpy` and `pydantic` from `dmc-core` package.
- Reference: `decision-modulation-core/docs/DEPENDENCY_CLEANUP.md`

### P3 — Eval Invariant Extension (F8) — ✅ DONE
- Extended fail-closed invariant to cover exception path.
- Published in eval release: v0.1.1

---

## Future (P2–P3) — New Core Proposals

### explainability-audit-core (Priority: High)
**Purpose:** Explain "why" decisions were made (audit/compliance).
**Scope:** proposal explanation, guard trigger chain, domain-agnostic reason codes.

### decision-ecosystem-cli (Priority: Medium)
**Purpose:** Single-command ecosystem management.
**Scope:** install cores, local test pipeline, contract matrix validation.

**Note:** `execution-orchestration-core` already exists and is released (v0.1.0); do not list it as "new core".

---

## Decision Matrix (High Level)

| Item | Impact | Effort | Priority |
|---|---:|---:|---:|
| P0 Release alignment (tags) | Medium | Low | P0 |
| P1 Ops latency windowing | Low | Medium | P1 |
| explainability-audit-core | High | High | P2 |
| decision-ecosystem-cli | Medium | Medium | P2 |
| CI/CD maturity (secret scan, vuln scan, coverage gates) | Medium | Medium | P3 |

---

**Last Updated:** 2026-02-19  
**Status:** Ready for next phase
