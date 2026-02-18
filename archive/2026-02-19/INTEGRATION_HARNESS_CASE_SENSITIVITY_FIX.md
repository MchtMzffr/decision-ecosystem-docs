# Integration Harness — Case Sensitivity Fix (Main → main)

**Date:** 2026-02-17  
**Issue:** GitHub default branch is `Main` (capital M) instead of `main` (lowercase)

---

## Current Status

### GitHub API Verification

```json
{
  "default_branch": "Main"  // ❌ Capital M
}
```

### Git Remote Status

```
HEAD branch: Main
Remote branches:
  Main tracked
  main tracked
```

**Problem:** Both `Main` and `main` branches exist, causing confusion.

---

## Root Cause

When we created the `main` branch locally and pushed it, GitHub may have created a case-insensitive duplicate or the default branch setting didn't update correctly.

---

## Solution Steps

### Step 1: Verify Branch Contents Match

```bash
cd decision-ecosystem-integration-harness
git fetch origin
git diff origin/Main origin/main --stat
```

**Expected:** No differences (branches should be identical)

### Step 2: Set Default Branch to `main` (lowercase) in GitHub

1. Go to: https://github.com/MchtMzffr/decision-ecosystem-integration-harness/settings/branches
2. Change default branch from `Main` → `main` (lowercase)
3. Confirm the change

### Step 3: Delete `Main` Branch (After Default Change)

**After default branch is changed to `main`:**

```bash
cd decision-ecosystem-integration-harness
git push origin --delete Main
```

**Note:** This will fail if `Main` is still the default branch. Change default first!

### Step 4: Verify

```bash
git remote show origin
# Should show: HEAD branch: main (lowercase)
```

---

## Verification Commands

### Check Current Default Branch

```bash
# Via GitHub API
curl https://api.github.com/repos/MchtMzffr/decision-ecosystem-integration-harness | grep default_branch

# Via git
git remote show origin | grep "HEAD branch"
```

### Check Branch Existence

```bash
git branch -r | grep -i main
# Should only show: origin/main (after cleanup)
```

---

## Expected Final State

```
HEAD branch: main (lowercase)
Remote branches:
  main tracked
```

**No `Main` branch should exist.**

---

## Notes

- **Case Sensitivity:** Git treats `Main` and `main` as different branches
- **GitHub Default:** GitHub's default branch setting is case-sensitive
- **CI Impact:** CI workflows use `main` (lowercase), so default should match

---

**Status:** ⚠️ **Requires manual GitHub settings change**

**Action Required:** Change default branch from `Main` → `main` in GitHub repository settings.
