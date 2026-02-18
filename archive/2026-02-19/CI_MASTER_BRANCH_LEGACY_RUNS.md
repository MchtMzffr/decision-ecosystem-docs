# CI Master Branch — Legacy Runs Analysis

**Date:** 2026-02-17  
**Issue:** GitHub UI shows failed CI runs on `master` branch

---

## Situation

GitHub Actions UI shows:
- ❌ Failed CI runs on `master` branch (runs #6, #7, #8)
- ✅ Successful CI run on `main` branch (run #21)

---

## Root Cause

### Historical Context

1. **Before Migration:**
   - `master` branch was the default branch
   - CI workflow triggered on `master` branch
   - Some CI runs failed (runs #6, #7, #8)

2. **After Migration:**
   - Default branch changed to `main`
   - CI workflow updated to trigger on `main` only
   - `master` branch deleted from remote
   - New CI runs trigger on `main` branch only

### Why Master Branch Runs Still Appear

**GitHub Actions UI shows historical runs:**
- Old CI runs remain in history (even after branch deletion)
- These runs are from **before migration**
- They cannot be re-triggered because:
  1. `master` branch no longer exists
  2. Workflow file only triggers on `main`

---

## Verification

### Current State (GitHub API)

**`main` branch runs:**
- ✅ Run #21: `head_branch: "main"`, `conclusion: "success"`
- ✅ All 4 jobs successful (core_only 3.11, core_only 3.12, full_stack 3.11, full_stack 3.12)

**`master` branch runs:**
- ⚠️ Historical runs exist (runs #6, #7, #8, #20, etc.)
- ⚠️ These are from before migration
- ⚠️ Cannot be re-run because `master` branch doesn't exist

### Branch Status

```bash
# Remote branches
origin/HEAD -> origin/main
origin/main

# No origin/master exists
```

**Status:** ✅ Only `main` branch exists

---

## Solution

### Option 1: Ignore Legacy Runs (Recommended)

**Action:** No action needed

**Reasoning:**
- Legacy runs are historical data
- They cannot be re-triggered
- New runs only happen on `main` branch
- Migration is complete

### Option 2: Archive Legacy Runs (If Needed)

If you want to clean up the UI:

1. **GitHub doesn't provide API to delete workflow runs**
2. **Legacy runs will remain in history**
3. **They don't affect new CI runs**

---

## Expected Behavior Going Forward

### New CI Runs

- ✅ Trigger only on `main` branch pushes
- ✅ Workflow file: `.github/workflows/ci.yml` triggers `main` only
- ✅ No new runs on `master` (branch doesn't exist)

### Legacy Runs

- ⚠️ Old `master` branch runs remain in history
- ⚠️ They show as failed (historical state)
- ⚠️ Cannot be re-run or fixed (branch doesn't exist)

---

## Verification Commands

### Check Current CI Status

```bash
# Latest run on main branch
curl https://api.github.com/repos/MchtMzffr/decision-ecosystem-integration-harness/actions/runs?branch=main&per_page=1

# Should show: head_branch: "main", conclusion: "success"
```

### Check Branch Existence

```bash
curl https://api.github.com/repos/MchtMzffr/decision-ecosystem-integration-harness/branches

# Should show: Only "main" branch exists
```

---

## Conclusion

✅ **Migration Complete:**
- Only `main` branch exists
- CI workflow triggers on `main` only
- Latest CI run (#21) successful on `main`

⚠️ **Legacy Runs:**
- Old `master` branch runs remain in history
- They cannot be re-run (branch doesn't exist)
- They don't affect new CI runs

**Recommendation:** Ignore legacy `master` branch runs. Focus on `main` branch CI runs going forward.

---

**Status:** ✅ **Migration Complete** — Legacy runs are historical only
