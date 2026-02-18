# Version Bump Summary — Patch Releases

**Date:** 2026-02-17  
**Type:** Patch Releases (backward-compatible)

---

## ✅ Completed Tasks

### P0 — CI Governance Drift Closure

**ops-health-core:**
- ✅ Added `@main` to decision-schema git fallback URL
- ✅ Ensures deterministic fallback behavior
- ✅ Aligns with BRANCH_GOVERNANCE.md

**mdm-engine:**
- ✅ Already configured correctly (only `main` trigger, `@main` fallback)

---

## Version Bumps

### decision-schema: 0.2.0 → **0.2.1**

**Files Changed:**
- `pyproject.toml`: `version = "0.2.1"`
- `decision_schema/version.py`: `__version__ = "0.2.1"`
- `docs/RELEASE_NOTES_0.2.1.md`: Created

**Changes:**
- F1 fix: INV-T1 two-mode validation (context + trace keys)
- Backward-compatible patch release

**Invariant:** INV-REL-1 (version sync) ✅

---

### mdm-engine: 0.2.0 → **0.2.1**

**Files Changed:**
- `pyproject.toml`: `version = "0.2.1"`
- `mdm_engine/__init__.py`: `__version__ = "0.2.1"`
- `docs/RELEASE_NOTES_0.2.1.md`: Created

**Changes:**
- F5 fix: TraceLogger batch flush support
- Backward-compatible patch release

**Invariant:** INV-REL-1 (version sync) ✅

---

### ops-health-core: 0.1.0 → **0.1.1**

**Files Changed:**
- `pyproject.toml`: `version = "0.1.1"`
- `ops_health_core/version.py`: `__version__ = "0.1.1"`
- `docs/RELEASE_NOTES_0.1.1.md`: Created

**Changes:**
- F2 fix: Unbounded growth fix (in-place timestamp pruning)
- Backward-compatible patch release

**Invariant:** INV-REL-1 (version sync) ✅

---

### evaluation-calibration-core: 0.1.0 → **0.1.1**

**Files Changed:**
- `pyproject.toml`: `version = "0.1.1"`
- `eval_calibration_core/version.py`: `__version__ = "0.1.1"`
- `docs/RELEASE_NOTES_0.1.1.md`: Created

**Changes:**
- F6 fix: Percentile documentation (nearest-rank method)
- Backward-compatible patch release

**Invariant:** INV-REL-1 (version sync) ✅

---

## Verified Invariants

### INV-REL-1 (Version Single-Source) ✅

All repositories now have synchronized versions:
- `pyproject.toml:version` == `<package>/version.py:__version__` (or `__init__.py:__version__`)

**Verification:**
```bash
# decision-schema
python -c "from decision_schema.version import __version__; print(__version__)"
# Output: 0.2.1

# mdm-engine
python -c "from mdm_engine import __version__; print(__version__)"
# Output: 0.2.1

# ops-health-core
python -c "from ops_health_core.version import __version__; print(__version__)"
# Output: 0.1.1

# evaluation-calibration-core
python -c "from eval_calibration_core.version import __version__; print(__version__)"
# Output: 0.1.1
```

### INV-REL-2 (Branch Governance) ✅

All CI workflows now:
- Trigger only on `main` branch
- Use `@main` in git fallback URLs
- No `master` references

**Verification:**
- ✅ mdm-engine: `.github/workflows/ci.yml` → `branches: [main]`, `@main` fallback
- ✅ ops-health-core: `.github/workflows/ci.yml` → `branches: [main]`, `@main` fallback
- ✅ evaluation-calibration-core: `.github/workflows/ci.yml` → `branches: [main]`, `@main` fallback
- ✅ decision-schema: `.github/workflows/ci.yml` → `branches: [main]`
- ✅ integration-harness: `.github/workflows/ci.yml` → `branches: [main]`, `@main` fallback

### INV-REL-3 (Fallback Determinism) ✅

All git fallback URLs now use `@main`:
- ✅ mdm-engine: `git+...decision-schema.git@main`
- ✅ ops-health-core: `git+...decision-schema.git@main`
- ✅ evaluation-calibration-core: `git+...decision-schema.git@main`
- ✅ integration-harness: All fallbacks use `@main`

---

## Release Notes

All repositories include comprehensive release notes:
- `decision-schema/docs/RELEASE_NOTES_0.2.1.md`
- `mdm-engine/docs/RELEASE_NOTES_0.2.1.md`
- `ops-health-core/docs/RELEASE_NOTES_0.1.1.md`
- `evaluation-calibration-core/docs/RELEASE_NOTES_0.1.1.md`

Each release note includes:
- Summary
- Changes (with fix IDs)
- Backward compatibility guarantee
- Migration guide (if needed)
- Testing status
- References

---

## Next Steps (Optional)

### Git Tags (Recommended)

After pushing commits, create git tags for each release:

```bash
# decision-schema
cd decision-schema
git tag -a v0.2.1 -m "Release 0.2.1: INV-T1 two-mode validation"
git push origin v0.2.1

# mdm-engine
cd mdm-engine
git tag -a v0.2.1 -m "Release 0.2.1: TraceLogger batch flush"
git push origin v0.2.1

# ops-health-core
cd ops-health-core
git tag -a v0.1.1 -m "Release 0.1.1: Unbounded growth fix"
git push origin v0.1.1

# evaluation-calibration-core
cd evaluation-calibration-core
git tag -a v0.1.1 -m "Release 0.1.1: Percentile documentation"
git push origin v0.1.1
```

### GitHub Releases (Optional)

Create GitHub Releases with release notes:
- Copy content from `docs/RELEASE_NOTES_X.Y.Z.md`
- Tag: `v0.2.1` / `v0.1.1`
- Mark as "Latest release"

### Update Integration Harness Pins (After Tags)

After tags are created, update `integration-harness` CI to use tagged versions:

```yaml
# .github/workflows/ci.yml
pip install "decision-schema>=0.2.1,<0.3" || pip install "git+https://github.com/MchtMzffr/decision-schema.git@v0.2.1"
```

---

## Summary

✅ **P0 CI Governance:** Closed (ops-health-core fallback fixed)  
✅ **Version Bumps:** All 4 repositories bumped  
✅ **Release Notes:** All 4 repositories documented  
✅ **Invariants:** INV-REL-1, INV-REL-2, INV-REL-3 verified  

**Status:** Ready for git tags and GitHub releases.

---

**Upgrade Paths:**
- `pip install "decision-schema>=0.2.1,<0.3"`
- `pip install "mdm-engine>=0.2.1,<0.3"`
- `pip install "ops-health-core>=0.1.1,<0.2"`
- `pip install "evaluation-calibration-core>=0.1.1,<0.2"`
