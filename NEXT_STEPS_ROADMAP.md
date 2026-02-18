# Next Steps Roadmap — Decision Ecosystem

**Date:** 2026-02-17  
**Current Status:** ✅ Migration Complete, Static Analysis Fixes Applied

---

## Immediate Next Steps (P0-P1)

### Option 1: Version Bumps (Patch Releases) — **RECOMMENDED**

**Rationale:** All fixes (F1, F2, F5, F6) are backward-compatible and qualify for patch releases.

| Repository | Current | Target | Action |
|------------|---------|--------|--------|
| **decision-schema** | 0.2.0 | **0.2.1** | Bump version, tag release |
| **mdm-engine** | 0.2.0 | **0.2.1** | Bump version, tag release |
| **evaluation-calibration-core** | 0.1.0 | **0.1.1** | Bump version, tag release |
| **ops-health-core** | 0.1.0 | **0.1.1** | Bump version, tag release |

**Benefits:**
- ✅ Formalizes fixes in release history
- ✅ Enables dependency pinning to specific patch versions
- ✅ Follows SemVer best practices

**Effort:** Low (version bump + git tag)

---

### Option 2: Remaining Optional Tasks (P1-P2)

#### P1 — Ops-Health Latency TODO

**Task:** Add `latency_timestamps` to `OpsState` for proper window-based pruning

**Current State:**
- `latency_samples` is timestamp-less
- TODO added in `scorer.py`
- p95 computed on all samples (not windowed)

**Implementation:**
1. Add `latency_timestamps: list[int]` to `OpsState`
2. Update `scorer.py` to prune latency samples by timestamp
3. Add tests for window-based latency pruning

**Effort:** Medium (requires state model change)

---

#### P2 — DMC-Core Dependency Cleanup

**Task:** Remove unused `numpy` and `pydantic` dependencies

**Current State:**
- Dependencies declared but not used in core code
- Only used in `docs/examples/` (legacy)

**Implementation:**
1. Verify no core code uses numpy/pydantic
2. Move to optional dependencies or remove
3. Update `pyproject.toml`

**Effort:** Low (dependency cleanup)

---

#### P3 — Eval Invariant Extension (F8)

**Task:** Extend invariant to cover harness exception path

**Current State:**
- Invariant: `deny_flags ⇒ allowed=False`
- Missing: `allowed=False ∧ mismatch is None ⇒ external has fail_closed marker`

**Implementation:**
1. Update `eval_calibration_core/suites/invariants.py`
2. Add test for exception path invariant
3. Document in invariant suite

**Effort:** Low (invariant extension)

---

## Medium-Term Roadmap (P2-P3)

### Option 3: New Core Development

Based on `docs/ECOSYSTEM_ROADMAP_AND_RECOMMENDATIONS.md`:

#### 3.1 execution-orchestration-core (Priority: High)

**Purpose:** Execute FinalDecision in real-world scenarios

**Scope:**
- Action execution orchestration
- Retry/backoff, timeout, idempotency
- Execution trace → PacketV2

**Effort:** Medium-High (new core + DOC TRIO)

---

#### 3.2 explainability-audit-core (Priority: High)

**Purpose:** Explain "why" decisions were made (audit/compliance)

**Scope:**
- Proposal explanation (which signals/features)
- Guard trigger chain explanation
- Domain-agnostic reason codes → human-readable

**Effort:** Medium (new core + DOC TRIO)

---

#### 3.3 decision-ecosystem-cli (Priority: Medium)

**Purpose:** Single-command ecosystem management

**Scope:**
- Install all cores: `decision-ecosystem install`
- Local test pipeline
- Contract matrix validation

**Effort:** Medium (CLI tool + integration)

---

## Long-Term Enhancements (P3-P4)

### Option 4: CI/CD Maturity

**Tasks:**
- Secret scanning (GitHub Actions)
- Test coverage metrics + thresholds
- Dependency vulnerability scanning
- Automated release workflow

**Effort:** Low-Medium (CI/CD improvements)

---

### Option 5: Documentation Sync

**Tasks:**
- Auto-generate trace registry docs from code
- CI check for doc drift
- Contract matrix auto-update

**Effort:** Medium (tooling + CI)

---

## Recommended Priority Order

### Immediate (This Week)

1. **Version Bumps** (Option 1) — Low effort, high value
   - Formalizes fixes
   - Enables proper dependency management
   - **Estimated Time:** 1-2 hours

### Short-Term (Next 2 Weeks)

2. **Remaining Optional Tasks** (Option 2) — Medium effort
   - P1: Latency TODO (if needed)
   - P2: Dependency cleanup (quick win)
   - P3: Invariant extension (quick win)
   - **Estimated Time:** 4-6 hours total

### Medium-Term (Next Month)

3. **New Core Development** (Option 3) — High effort, high value
   - execution-orchestration-core (highest priority)
   - explainability-audit-core (high priority)
   - **Estimated Time:** 1-2 weeks per core

### Long-Term (Ongoing)

4. **CI/CD Maturity** (Option 4) — Ongoing improvements
5. **Documentation Sync** (Option 5) — Tooling improvements

---

## Decision Matrix

| Option | Impact | Effort | Priority | Recommended? |
|--------|--------|--------|----------|--------------|
| **Version Bumps** | Medium | Low | P0 | ✅ **YES** |
| **P1 Latency TODO** | Low | Medium | P1 | ⚠️ Optional |
| **P2 Dependency Cleanup** | Low | Low | P2 | ✅ Quick win |
| **P3 Invariant Extension** | Low | Low | P2 | ✅ Quick win |
| **New Core (execution)** | High | High | P2 | ⚠️ Future |
| **New Core (explainability)** | High | High | P2 | ⚠️ Future |
| **CI/CD Maturity** | Medium | Medium | P3 | ⚠️ Ongoing |

---

## Recommendation

**Start with Option 1 (Version Bumps):**
- ✅ Low effort, high value
- ✅ Formalizes completed work
- ✅ Enables proper SemVer management
- ✅ Can be done in 1-2 hours

**Then Option 2 (Quick Wins):**
- ✅ P2: Dependency cleanup (15 min)
- ✅ P3: Invariant extension (30 min)
- ⚠️ P1: Latency TODO (if needed, 2-3 hours)

**Then evaluate Option 3 (New Cores):**
- Based on business needs
- Requires more planning

---

## Next Action

**Choose one:**
1. **Version bumps** — I'll prepare version bump commits for all repos
2. **Quick wins** — I'll implement P2 (dependency cleanup) and P3 (invariant extension)
3. **New core** — I'll create skeleton for execution-orchestration-core
4. **Something else** — Tell me what you'd like to focus on

---

**Last Updated:** 2026-02-17  
**Status:** Ready for next phase
