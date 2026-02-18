<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Tag Governance — Immutability Policy

**Date:** 2026-02-17  
**Status:** Active Policy

---

## Core Principle

**Tags are immutable.** Once a tag is created and pushed, it must never be moved, deleted, or force-updated.

---

## Rationale

### Supply-Chain Security

Moving tags creates supply-chain risks:
- Consumers may have cached the tag → different content on re-fetch
- Build reproducibility breaks
- Security audits become unreliable

### SemVer Best Practice

If additional commits are needed after a tag:
- Create a **new patch release**: `v0.2.2` / `v0.1.2`
- Do NOT retag `v0.2.1` / `v0.1.1`

---

## Policy Rules

### ✅ Allowed

1. **Create new tags** for new releases
2. **Delete tags** before first push (local only)
3. **Create patch releases** (`v0.2.1` → `v0.2.2`) for fixes

### ❌ Forbidden

1. **Force-update tags** (`git tag -f`)
2. **Delete and recreate** tags after push
3. **Move tags** to different commits
4. **Retag** existing releases

---

## Exception: Pre-Release (Before First Push)

Tags can be deleted/recreated **only before first push**:
```bash
# ✅ OK: Delete local tag before push
git tag -d v0.2.1
git tag -a v0.2.1 -m "Release 0.2.1"
git push origin v0.2.1

# ❌ FORBIDDEN: Delete remote tag after push
git push origin :refs/tags/v0.2.1  # Only if tag was never consumed
```

---

## Enforcement

**INV-TAG-1:** Tag immutability
- Once pushed, tags must never change
- Violations require new patch release

**Verification:**
- CI checks: Tag commit hash must match release commit
- Release notes: Tag commit must be documented

---

## Examples

### ✅ Correct: New Patch Release

```bash
# v0.2.1 already released
# New fix needed → create v0.2.2
git commit -m "fix: Additional fix"
git tag -a v0.2.2 -m "Release 0.2.2"
git push origin v0.2.2
```

### ❌ Incorrect: Retagging

```bash
# v0.2.1 already released
# New fix needed → DO NOT retag
git tag -d v0.2.1  # ❌ FORBIDDEN
git tag -a v0.2.1 -m "Release 0.2.1 (updated)"
git push origin :refs/tags/v0.2.1  # ❌ FORBIDDEN
git push origin v0.2.1  # ❌ FORBIDDEN
```

---

## Related Policies

- **BRANCH_GOVERNANCE.md:** `main` as source of truth; dev vs CI fallback policy
- **RELEASE_VERIFICATION_CHECKLIST.md:** INV-REL-* and INV-REL-GH checks (including INV-REL-4: tag reachability)
- **ECOSYSTEM_CONTRACT_MATRIX.md:** SemVer and dependency ranges (see repo root or decision-schema repo)

---

**Last Updated:** 2026-02-17
