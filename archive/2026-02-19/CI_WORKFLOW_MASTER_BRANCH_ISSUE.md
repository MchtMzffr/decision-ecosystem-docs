# CI Workflow — Master Branch Issue Analysis

**Date:** 2026-02-17  
**Issue:** GitHub Actions shows CI runs on `master` branch, but workflow triggers `main` only

---

## Problem

GitHub Actions UI shows:
- ❌ All recent CI runs on `master` branch
- ❌ All CI runs failing (red X)
- ❌ CI runs triggered by commits on `master`

But:
- ✅ Local workflow file triggers on `main` only
- ✅ Local repo has no `master` branch
- ✅ Remote shows only `main` branch

---

## Root Cause Analysis

### Possible Explanations

1. **GitHub Cache:** Old workflow runs cached in UI
2. **Master Branch Still Exists:** Remote `master` branch may still exist (not visible in local fetch)
3. **Workflow File Mismatch:** Different workflow file on `master` vs `main`
4. **Historical Runs:** Old CI runs from before migration

---

## Verification Steps

### 1. Check Remote Branches (GitHub API)

```bash
curl https://api.github.com/repos/MchtMzffr/decision-ecosystem-integration-harness/branches
```

**Expected:** Only `main` branch should exist

### 2. Check Workflow File on Remote

```bash
# Check workflow on main branch
curl https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/main/.github/workflows/ci.yml

# Check if master branch exists and has different workflow
curl https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/master/.github/workflows/ci.yml
```

**Expected:** 
- `main` branch workflow should trigger on `main` only
- `master` branch should return 404 (doesn't exist)

### 3. Check Recent CI Runs

```bash
curl https://api.github.com/repos/MchtMzffr/decision-ecosystem-integration-harness/actions/runs?per_page=5
```

**Check:**
- `head_branch` field — should be `main` for recent runs
- `conclusion` field — check if failures are due to branch mismatch

---

## Solution Steps

### If `master` Branch Still Exists

1. **Delete `master` branch completely:**
   ```bash
   git push origin --delete master
   ```

2. **Verify deletion:**
   ```bash
   git fetch --prune
   git branch -r
   ```

3. **Check GitHub UI:** Wait 5-10 minutes for cache refresh

### If Workflow File Mismatch

1. **Verify workflow on `main`:**
   ```bash
   git show origin/main:.github/workflows/ci.yml | grep branches
   ```

2. **If `master` has different workflow, merge `main` → `master` or delete `master`**

### If Historical Runs

- **No action needed** — Old runs will remain in history
- **New runs should trigger on `main` only**

---

## Expected Final State

- ✅ Only `main` branch exists
- ✅ CI workflow triggers on `main` only
- ✅ New CI runs show `head_branch: main`
- ✅ No new runs on `master` branch

---

## Monitoring

After cleanup, monitor:
- New CI runs should show `main` branch
- No new runs on `master` branch
- CI workflow file matches local version

---

**Status:** 🔍 **Investigation Required**

**Next Steps:** Verify remote branch status via GitHub API
