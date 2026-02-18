# Release Verification Checklist — Quick Reference

**Purpose:** 2-minute verification of release invariants  
**Use:** After each release, verify all invariants pass

---

## Quick Verification URLs

### Version Single-Source (INV-REL-1)

**Check:** `main` version == tag version

| Repository | `main` URL | Tag URL |
|------------|------------|---------|
| decision-schema | [main/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/pyproject.toml) | [v0.2.2/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/decision-schema/v0.2.2/pyproject.toml) |
| mdm-engine | [main/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/pyproject.toml) | [v0.2.1/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/mdm-engine/v0.2.1/pyproject.toml) |
| ops-health-core | [main/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/pyproject.toml) | [v0.1.1/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/ops-health-core/v0.1.1/pyproject.toml) |
| evaluation-calibration-core | [main/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/main/pyproject.toml) | [v0.1.1/pyproject.toml](https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/v0.1.1/pyproject.toml) |

**Expected:** Both show same `version = "X.Y.Z"`

---

### Branch Governance (INV-REL-2)

**Check:** CI workflows trigger only on `main`

| Repository | CI Workflow URL |
|------------|-----------------|
| decision-schema | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/.github/workflows/ci.yml) |
| mdm-engine | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/.github/workflows/ci.yml) |
| ops-health-core | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/.github/workflows/ci.yml) |
| evaluation-calibration-core | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/main/.github/workflows/ci.yml) |
| integration-harness | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/main/.github/workflows/ci.yml) |

**Expected:** `branches: [main]` (no `master`)

---

### Fallback Determinism (INV-REL-3a)

**Check:** Integration pipeline fallbacks use tags

| Repository | CI Workflow URL | Check For |
|------------|-----------------|-----------|
| integration-harness | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/main/.github/workflows/ci.yml) | decision-schema `@v0.2.2`, mdm `@v0.2.1`, ops/eval `@v0.1.1` |
| ops-health-core | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/.github/workflows/ci.yml) | `@v0.2.2` |
| execution-orchestration-core | [main/.github/workflows/ci.yml](https://raw.githubusercontent.com/MchtMzffr/execution-orchestration-core/main/.github/workflows/ci.yml) | `@v0.2.2` |

**Expected:** Fallback URLs contain `@vX.Y.Z` (not `@main`)

---

### GitHub Release Artefacts (INV-REL-GH)

**Check:** Each required tag has a published GitHub Release (UI); Latest is correct; notes match repo.

| Repo | Tag (Latest) | Release notes source | Releases URL |
|------|--------------|----------------------|--------------|
| decision-schema | `v0.2.2` | `docs/RELEASE_NOTES_0.2.2.md` | [releases](https://github.com/MchtMzffr/decision-schema/releases) |
| mdm-engine | `v0.2.1` | `docs/RELEASE_NOTES_0.2.1.md` | [releases](https://github.com/MchtMzffr/mdm-engine/releases) |
| ops-health-core | `v0.1.1` | `docs/RELEASE_NOTES_0.1.1.md` | [releases](https://github.com/MchtMzffr/ops-health-core/releases) |
| evaluation-calibration-core | `v0.1.1` | `docs/RELEASE_NOTES_0.1.1.md` | [releases](https://github.com/MchtMzffr/evaluation-calibration-core/releases) |
| execution-orchestration-core | `v0.1.0` | `docs/RELEASE_NOTES_0.1.0.md` or body template below | [releases](https://github.com/MchtMzffr/execution-orchestration-core/releases) |

**INV-REL-GH-1:** Tag → Release exists.  
**INV-REL-GH-2:** Latest release = max SemVer for that repo.  
**INV-REL-GH-3:** Release body ≈ `docs/RELEASE_NOTES_X.Y.Z.md` (or approved template).  
**INV-REL-GH-4:** No secrets; description English, domain-agnostic.

---

## Checklist Template

Copy this for each release:

```markdown
## Release Verification — vX.Y.Z

**Date:** YYYY-MM-DD  
**Release:** vX.Y.Z

### INV-REL-1 (Version Single-Source)
- [ ] decision-schema: main == tag
- [ ] mdm-engine: main == tag
- [ ] ops-health-core: main == tag
- [ ] evaluation-calibration-core: main == tag

### INV-REL-2 (Branch Governance)
- [ ] All CI workflows: `branches: [main]`
- [ ] No `master` references

### INV-REL-3a (Integration Pipeline Fallbacks)
- [ ] integration-harness: decision-schema `@v0.2.2`, others per table
- [ ] ops-health-core: Fallback uses `@v0.2.2`
- [ ] execution-orchestration-core: Fallback uses `@v0.2.2`

### INV-REL-GH (GitHub Release Artefacts)
- [ ] decision-schema: Release for v0.2.2, set Latest
- [ ] mdm-engine: Release for v0.2.1, set Latest
- [ ] ops-health-core: Release for v0.1.1, set Latest
- [ ] evaluation-calibration-core: Release for v0.1.1, set Latest
- [ ] execution-orchestration-core: Release for v0.1.0, set Latest

### Tag Alignment
- [ ] Tag commit == main commit (git log verification)

**Status:** ✅ PASS / ❌ FAIL
```

---

## Git Commands for Verification

```bash
# Check version in main
git fetch origin
git show origin/main:pyproject.toml | grep "version ="

# Check version in tag
git show vX.Y.Z:pyproject.toml | grep "version ="

# Verify tag alignment
git log --oneline origin/main -1
git log --oneline vX.Y.Z -1
# Should show same commit hash

# Check CI fallback
git show origin/main:.github/workflows/ci.yml | grep -A 2 "fallback"
```

---

## Cache-Busting URLs

If GitHub shows stale content, add `?cb=YYYYMMDDHH` to URLs:

```
https://raw.githubusercontent.com/.../main/pyproject.toml?cb=20260218
```

---

## Related Documentation

- **FINAL_RELEASE_VERIFICATION.md:** Detailed verification report
- **TAG_GOVERNANCE.md:** Tag immutability policy
- **BRANCH_GOVERNANCE.md:** Branch governance rules

---

**Last Updated:** 2026-02-18
