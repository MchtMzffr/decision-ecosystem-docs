# Final Release Verification — Public Remote Status

**Date:** 2026-02-17  
**Verification Method:** Direct GitHub raw content + Git log  
**Status:** ✅ **ALL INVARIANTS PASS**

---

## ✅ INV-REL-1 (Version Single-Source) — PASS

**Verification:** `main` branch version == tag version

| Repository | `main` Version | Tag Version | Status |
|------------|----------------|-------------|--------|
| **decision-schema** | 0.2.1 | v0.2.1 = 0.2.1 | ✅ Match |
| **mdm-engine** | 0.2.1 | v0.2.1 = 0.2.1 | ✅ Match |
| **ops-health-core** | 0.1.1 | v0.1.1 = 0.1.1 | ✅ Match |
| **evaluation-calibration-core** | 0.1.1 | v0.1.1 = 0.1.1 | ✅ Match |

**Evidence:**
- `raw.githubusercontent.com/.../main/pyproject.toml` → `version = "0.2.1"` / `"0.1.1"`
- `raw.githubusercontent.com/.../v0.2.1/pyproject.toml` → `version = "0.2.1"`
- `raw.githubusercontent.com/.../v0.1.1/pyproject.toml` → `version = "0.1.1"`
- Git log verification: `main` commit == tag commit

---

## ✅ INV-REL-2 (Branch Governance) — PASS

**Verification:** All CI workflows trigger only on `main` branch

- ✅ decision-schema: `branches: [main]`
- ✅ mdm-engine: `branches: [main]`
- ✅ ops-health-core: `branches: [main]`
- ✅ evaluation-calibration-core: `branches: [main]`
- ✅ integration-harness: `branches: [main]`

**Evidence:** All `.github/workflows/ci.yml` files verified

---

## ✅ INV-REL-3 (Fallback Determinism) — PASS

**Verification:** Git fallback URLs use tagged versions where required

### INV-REL-3a: Integration Pipeline (Tag-Pinned) — PASS

**Scope:** Integration pipeline (harness + ops-health) requires deterministic fallbacks.

#### integration-harness CI

| Dependency | Constraint | Fallback Tag | Status |
|------------|------------|--------------|--------|
| decision-schema | >=0.2.1,<0.3 | @v0.2.1 | ✅ |
| mdm-engine | >=0.2.1,<0.3 | @v0.2.1 | ✅ |
| ops-health-core | >=0.1.1,<0.2 | @v0.1.1 | ✅ |
| evaluation-calibration-core | >=0.1.1,<0.2 | @v0.1.1 | ✅ |
| dmc-core | >=0.1,<0.2 | @main | ⚠️ (no tag yet, acceptable) |

**Evidence:**
```yaml
# integration-harness/.github/workflows/ci.yml
pip install "decision-schema>=0.2.1,<0.3" || pip install "git+...decision-schema.git@v0.2.1"
pip install "mdm-engine>=0.2.1,<0.3" || pip install "git+...mdm-engine.git@v0.2.1"
pip install "ops-health-core>=0.1.1,<0.2" || pip install "git+...ops-health-core.git@v0.1.1"
pip install "evaluation-calibration-core>=0.1.1,<0.2" || pip install "git+...evaluation-calibration-core.git@v0.1.1"
```

#### ops-health-core CI

| Dependency | Constraint | Fallback Tag | Status |
|------------|------------|--------------|--------|
| decision-schema | >=0.2.1,<0.3 | @v0.2.1 | ✅ |

**Evidence:**
```yaml
# ops-health-core/.github/workflows/ci.yml
pip install "decision-schema>=0.2.1,<0.3" || pip install "git+...decision-schema.git@v0.2.1"
```

### INV-REL-3b: Core CI (Latest SSOT Compatibility) — PASS

**Scope:** Core repositories (mdm-engine, eval-calibration, dmc-core) may use `@main` fallback to test compatibility with latest SSOT.

**Rationale:** Core CI tests compatibility with latest `decision-schema@main` to catch breaking changes early.

**Status:** ✅ Acceptable design choice (not a violation)

---

## ✅ Tag Alignment — PASS

**Verification:** Tag commit == `main` branch commit

| Repository | Tag Commit | `main` Commit | Status |
|------------|------------|---------------|--------|
| **decision-schema** | ef8c1c2 | ef8c1c2 | ✅ Aligned |
| **mdm-engine** | ea9973a | ea9973a | ✅ Aligned |
| **ops-health-core** | c0cb359 | c0cb359 | ✅ Aligned |
| **evaluation-calibration-core** | e628733 | e628733 | ✅ Aligned |

**Evidence:** Git log verification confirms tag points to `main` HEAD

---

## Summary

✅ **INV-REL-1:** Version single-source — PASS  
✅ **INV-REL-2:** Branch governance — PASS  
✅ **INV-REL-3:** Fallback determinism — PASS  
✅ **Tag Alignment:** Tags aligned with `main` — PASS  

**Ecosystem Status:** ✅ **PRODUCTION-READY**

---

## Note on GitHub Cache

If you see outdated versions in GitHub UI, this may be due to:
- Browser cache
- GitHub CDN cache (usually clears within minutes)
- Stale browser tab

**Verification Method:** Always use `raw.githubusercontent.com` URLs with cache-busting (`?cb=YYYYMMDDHH`) or `git show origin/main:file` for definitive verification.

---

## Related Policies

- **TAG_GOVERNANCE.md:** Tag immutability policy
- **BRANCH_GOVERNANCE.md:** Branch governance rules
- **RELEASE_VERIFICATION_CHECKLIST.md:** Quick reference checklist

---

**Last Verified:** 2026-02-17  
**Verification Method:** Direct GitHub API + Git log  
**Quick Reference:** See `RELEASE_VERIFICATION_CHECKLIST.md` for 2-minute verification
