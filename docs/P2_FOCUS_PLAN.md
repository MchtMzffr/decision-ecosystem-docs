# P2 Focus Plan — Decision Ecosystem

**Date:** 2026-02  
**Context:** P0 and P1 checks are done; P2 work is next.

---

## P0 / P1 Check Results (Verified)

| Check | Tool / Test | Result |
|-------|-------------|--------|
| **INV-DOC-DRIFT-1** | `check_release_alignment.py --workspace <parent>` | OK — roadmap table matches pyproject versions |
| **INV-SYNC-1** | `check_workspace_sync.py --workspace <parent>` | OK — all repos clean, in sync with origin/main |
| **P0 Remote owner** | `check_remote_owner.py --workspace <parent>` | OK — canonical owner in use |
| **P1 Ops-Health latency** | `pytest tests/test_latency_window_pruning.py test_health_score test_kill_switch` | OK — 12 passed |

**Summary:** No P0/P1 blockers; ready to proceed with P2.

---

## P2 Work List (Priority Order)

### 1. explainability-audit-core — Roadmap + Release (P2-High)

**Current state:** Repo exists; `explain_from_packet`, INV-EXPL tests, doc trio (ARCHITECTURE, FORMULAS, INTEGRATION_GUIDE) complete. CI in place.

**P2 tasks:**
- [x] **Roadmap update:** Update "explainability-audit-core" in NEXT_STEPS_ROADMAP.md: "Minimal complete (v0.1.0 skeleton, INV-EXPL tests, doc trio); first tag v0.1.0 publishable."
- [x] **First release:** GitHub tag + release notes for SemVer 0.1.0 (aligned with RELEASE_NOTES_STANDARD_AND_TEMPLATES).
- [x] **Optional:** Add as 7th core to roadmap P0 table (if scope remains "6 core", keep in "Future" only).

### 2. Harness explanation (P2-Medium, optional)

**Goal:** After PacketV2 is produced in the integration harness, add an explanation artifact to the report via `explain_from_packet(packet)`.

**Tasks:**
- [x] Optional dependency on `explainability-audit-core` in harness (try/import).
- [x] Call `explain_from_packet(packet)` after PacketV2; write output to report (e.g. `report.explanation`).
- [x] Document this step in INTEGRATION_GUIDE (explainability-audit-core/docs/INTEGRATION_GUIDE.md already has a draft).

### 3. decision-ecosystem-cli (P2-Medium)

**Goal:** Single-command ecosystem management: install cores, local test pipeline, contract matrix validation.

**Scope (recommended):**
- [x] `ecosystem` CLI script under `decision-ecosystem-docs/tools`.
- [x] Subcommands: `install` (pip install -e each core), `test` (pytest in workspace), `check-release` (check_release_alignment), `check-sync` (check_workspace_sync).
- [x] Compatible with existing tools in docs repo; working directory via `--workspace`.

### 4. CI/CD maturity (P3 — after P2)

P3 on roadmap: secret scan, vulnerability scan, coverage gates. To be addressed after P2 is complete.

---

## Recommended P2 Order

1. **explainability-audit-core roadmap + v0.1.0 release** — Quick to complete; clarifies audit-ready score.
2. **Harness explanation (optional)** — Connects explainability to the real pipeline.
3. **decision-ecosystem-cli** — Single-command experience; thin CLI wrapping existing tools.

This document can be used as a reference for P2-focused work; progress can be tracked via the checklist above.
