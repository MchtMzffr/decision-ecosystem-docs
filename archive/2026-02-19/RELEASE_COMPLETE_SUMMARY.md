# Release Complete Summary — Patch Releases + P3 Extension

**Date:** 2026-02-17  
**Status:** ✅ All Tasks Completed

---

## ✅ Completed Tasks

### P0 — CI Governance Drift Closure

**ops-health-core:**
- ✅ Added `@main` to decision-schema git fallback URL
- ✅ Committed & pushed

**mdm-engine:**
- ✅ Already configured correctly (only `main` trigger, `@main` fallback)

---

### Version Bumps (4 Repositories)

| Repository | Version | Fix ID | Status |
|------------|---------|--------|--------|
| **decision-schema** | 0.2.0 → **0.2.1** | F1 (INV-T1 two-mode) | ✅ Tagged & Pushed |
| **mdm-engine** | 0.2.0 → **0.2.1** | F5 (TraceLogger batch flush) | ✅ Tagged & Pushed |
| **ops-health-core** | 0.1.0 → **0.1.1** | F2 (Unbounded growth fix) | ✅ Tagged & Pushed |
| **evaluation-calibration-core** | 0.1.0 → **0.1.1** | F6 (Percentile doc) | ✅ Tagged & Pushed |

**Git Tags Created:**
- `decision-schema`: `v0.2.1`
- `mdm-engine`: `v0.2.1`
- `ops-health-core`: `v0.1.1`
- `evaluation-calibration-core`: `v0.1.1`

**Release Notes Created:**
- `decision-schema/docs/RELEASE_NOTES_0.2.1.md`
- `mdm-engine/docs/RELEASE_NOTES_0.2.1.md`
- `ops-health-core/docs/RELEASE_NOTES_0.1.1.md`
- `evaluation-calibration-core/docs/RELEASE_NOTES_0.1.1.md`

---

### Integration Harness CI Update

**Updated CI to use tagged versions:**
- ✅ `decision-schema`: `>=0.2.1`, fallback `@v0.2.1`
- ✅ `mdm-engine`: `>=0.2.1`, fallback `@v0.2.1`
- ✅ `ops-health-core`: `>=0.1.1`, fallback `@v0.1.1`
- ✅ `evaluation-calibration-core`: `>=0.1.1`, fallback `@v0.1.1`

**Benefits:**
- Deterministic fallback to tagged releases
- Ensures reproducible CI builds
- Aligns with SemVer best practices

---

### P3 — Eval Invariant Extension (F8)

**Task:** Extend fail-closed invariant to cover harness exception path

**Implementation:**
- ✅ Extended `_check_fail_closed()` in `eval_calibration_core/suites/invariants.py`
- ✅ Added invariant: `allowed=False ∧ mismatch=None => external has fail_closed marker`
- ✅ Added test: `test_invariant_fail_closed_exception_path()`
- ✅ All tests passing (5/5)

**Invariant Logic:**
```python
# Invariant 1: deny_flags => allowed=False (existing)
# Invariant 2 (F8): allowed=False ∧ mismatch=None => external has fail_closed marker (new)
```

**Coverage:**
- ✅ Harness exception path (`harness.fail_closed`)
- ✅ Other exception paths (`ops.fail_closed`, etc.)
- ✅ Invalid cases (missing marker) correctly fail

**Files Changed:**
- `eval_calibration_core/suites/invariants.py`: Extended `_check_fail_closed()`
- `tests/test_invariants.py`: Added `test_invariant_fail_closed_exception_path()`

---

## Verified Invariants

### INV-REL-1 (Version Single-Source) ✅
- `pyproject.toml:version` == `<package>/version.py:__version__` (or `__init__.py:__version__`)

### INV-REL-2 (Branch Governance) ✅
- All CI workflows trigger only on `main` branch
- No `master` references

### INV-REL-3 (Fallback Determinism) ✅
- All git fallback URLs use tagged versions (`@v0.2.1`, `@v0.1.1`)

### INV-F8 (Exception Path Fail-Closed) ✅
- `allowed=False ∧ mismatch=None => external has fail_closed marker`
- Covers harness exception path

---

## Summary

✅ **P0 CI Governance:** Closed  
✅ **Version Bumps:** All 4 repositories bumped, tagged, and pushed  
✅ **Release Notes:** All 4 repositories documented  
✅ **Integration Harness CI:** Updated to use tagged versions  
✅ **P3 F8 Extension:** Implemented and tested  

**Status:** Ready for GitHub Releases (optional, manual step)

---

## Next Steps (Optional)

### GitHub Releases (Manual)

Create GitHub Releases with release notes:
1. Go to each repository's "Releases" page
2. Click "Draft a new release"
3. Tag: `v0.2.1` / `v0.1.1`
4. Title: "Release 0.2.1" / "Release 0.1.1"
5. Description: Copy content from `docs/RELEASE_NOTES_X.Y.Z.md`
6. Mark as "Latest release"

**Repositories:**
- `decision-schema`: https://github.com/MchtMzffr/decision-schema/releases/new
- `mdm-engine`: https://github.com/MchtMzffr/mdm-engine/releases/new
- `ops-health-core`: https://github.com/MchtMzffr/ops-health-core/releases/new
- `evaluation-calibration-core`: https://github.com/MchtMzffr/evaluation-calibration-core/releases/new

---

## Upgrade Paths

```bash
pip install "decision-schema>=0.2.1,<0.3"
pip install "mdm-engine>=0.2.1,<0.3"
pip install "ops-health-core>=0.1.1,<0.2"
pip install "evaluation-calibration-core>=0.1.1,<0.2"
```

---

**All tasks completed successfully!** 🎉
