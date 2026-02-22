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
| decision-schema | 0.2.2 | v0.2.2 | OK |
| mdm-engine | 0.2.1 | v0.2.1 | OK |
| ops-health-core | 0.1.1 | v0.1.1 | OK |
| evaluation-calibration-core | 0.1.1 | v0.1.1 | OK |
| execution-orchestration-core | 0.1.0 | v0.1.0 | OK |
| decision-modulation-core (dmc-core) | 0.1.1 | v0.1.1 | OK |

**Harness policy (INV-RM-SCOPE-1):** integration-harness is **non-core**; it is not in the core release alignment table above. Harness is tracked by tag for reproducibility when needed; optional "Non-core reproducibility" table can be added after first harness tag. Scope: roadmap P0 table = **core-only** (6 cores).

**Source of truth:** pyproject version on `main` + Git tags. Update this table whenever you publish a tag.

**Invariants:** `tag(version) == pyproject.version` for released packages; roadmap must match tags (INV-DOC-DRIFT-1). Full list: [ECOSYSTEM_INVARIANTS.md](ECOSYSTEM_INVARIANTS.md). To check table vs local repos: `python tools/check_release_alignment.py --workspace <parent-of-docs>`.

---

## Completed (Recent)

### P2 — DMC-Core Dependency Cleanup (F7) — ✅ DONE
- Removed unused `numpy` and `pydantic` from `dmc-core` package.
- Reference: `decision-modulation-core/docs/DEPENDENCY_CLEANUP.md`

### P3 — Eval Invariant Extension (F8) — ✅ DONE
- Extended fail-closed invariant to cover exception path.
- Published in eval release: v0.1.1

### P1 — Ops-Health Latency Windowing — ✅ DONE
- `OpsState.latency_timestamps` added; window-based pruning in `kill_switch.py`; p95 on windowed samples in `scorer.py`; CLI appends both on `latency` event.
- Tests: `tests/test_latency_window_pruning.py` (pruning, sync, window-based p95, empty-after-prune).

---

## Future (P2–P3) — New Core Proposals

**Note:** Yeni çekirdek geliştirmesi şu an **ertelendi**; öncelik mevcut core’ların stabilizasyonunda. Aşağıdaki proposal’lar ileride ele alınacak.

### explainability-audit-core (Priority: High) — ✅ Minimal tamamlandı (v0.1.0)
**Purpose:** Explain "why" decisions were made (audit/compliance).
**Scope:** proposal explanation, guard trigger chain, domain-agnostic reason codes; `explain_from_packet(PacketV2)` → ExplanationArtifact.
**Status:** v0.1.0 skeleton tamamlandı: INV-EXPL testleri, doc trio (ARCHITECTURE, FORMULAS, INTEGRATION_GUIDE), CI. İlk tag v0.1.0 yayınlandı. Harness’ta opsiyonel entegrasyon: rapora `report.explanation` eklenir.

### decision-ecosystem-cli (Priority: Medium) — ✅ Devrede
**Purpose:** Single-command ecosystem management.
**Scope:** install cores, local test pipeline, release/sync checks. CLI: `python tools/ecosystem.py` (docs repo); subcommand’lar: `install`, `test`, `check-release`, `check-sync`.

**Note:** `execution-orchestration-core` already exists and is released (v0.1.0); do not list it as "new core".

---

## Decision Matrix (High Level)

| Item | Impact | Effort | Priority |
|---|---:|---:|---:|
| P0 Release alignment (tags) | Medium | Low | P0 ✅ |
| P1 Ops latency windowing | Low | Medium | P1 ✅ |
| explainability-audit-core | High | High | P2 ✅ |
| decision-ecosystem-cli | Medium | Medium | P2 ✅ |
| CI/CD maturity (secret scan, vuln scan, coverage gates) | Medium | Medium | P3 |

---

**Last Updated:** 2026-02-19  
**Status:** Ready for next phase
