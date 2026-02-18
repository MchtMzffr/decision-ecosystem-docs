# decision-ecosystem-docs — Static Analysis Remediation (2026-02-18)

**Scope:** SSOT for governance, release, and verification; reduce contradiction, drift, and broken references.

---

## Summary of changes

### P0 — Semantics (governance)

1. **RELEASE_VERIFICATION_CHECKLIST.md**
   - Replaced “Tag Alignment: tag commit == main commit” with **INV-REL-4**: tag commit must be **ancestor** of `main` (verify with `git merge-base --is-ancestor vX.Y.Z origin/main`).
   - Updated Git commands section accordingly.

2. **TAG_GOVERNANCE.md**
   - Related docs: removed broken link to missing file; added RELEASE_VERIFICATION_CHECKLIST and ECOSYSTEM_CONTRACT_MATRIX (see repo root or decision-schema for matrix).

3. **TAG_ALIGNMENT_COMPLETE.md**
   - Marked as **historical incident report** (not policy). Current policy: TAG_GOVERNANCE (immutability) + INV-REL-4 (reachability).

4. **BRANCH_GOVERNANCE.md**
   - Split “Git Fallback URLs” into:
     - **Dev/experiments:** `@main` allowed (documented as non-deterministic).
     - **CI / release:** tag-pinned only (**INV-GOV-1**). **INV-GOV-2**: dev may use `@main`.
   - Enforcement: INV-GOV-1, INV-GOV-2 added.

### P1 — Missing artifact

5. **ECOSYSTEM_CONTRACT_MATRIX.md** added with: repo → decision-schema range, CI fallback tag, exec.* note.

### P2 — Current vs archive

6. **archive/2026-02-17/** created; **FINAL_RELEASE_VERIFICATION.md** and **RELEASE_VERIFICATION_COMPLETE.md** moved there (with header note that they are historical).
7. **README.md** updated: “CURRENT” docs only in main quick links; “Archive” section links to `archive/2026-02-17/`. Removed “Final Release Verification” from current links.
8. **RELEASE_VERIFICATION_CHECKLIST.md** “Related Documentation” updated: no longer points to deleted FINAL_RELEASE_VERIFICATION; added ECOSYSTEM_CONTRACT_MATRIX and archive.

### P3 — Content updates

9. **ARCHITECTURE.md**: “five cores” → **six cores**; added **execution-orchestration-core**; data flow diagram updated.
10. **INTEGRATION_GUIDE.md**: Code blocks labeled as **pseudocode**; note to verify actual API in each core repo.
11. **FORMULAS.md**: Drawdown/Sharpe-like described as generic (peak-to-trough decline, risk-adjusted outcome ratio); note that domain-specific names live in examples only.
12. **GITHUB_RELEASES_GUIDE.md**: execution-orchestration-core install: added git-tag install when not on PyPI (`pip install "git+...@v0.1.0"`).

---

## Invariants referenced

- **INV-REL-4:** Tag commit is ancestor of `main` (not “tag == main HEAD”).
- **INV-GOV-1:** CI fallback ⇒ tag.
- **INV-GOV-2:** Dev install guidance may allow `@main` (non-deterministic).
- **INV-DOC-1:** README quick links ⇒ current docs only.
- **INV-DOC-2:** Historical reports ⇒ `archive/YYYY-MM-DD/`.
- **INV-DOC-3:** All referenced local docs exist (ECOSYSTEM_CONTRACT_MATRIX added).
- **INV-DOC-4:** Code blocks either verified or labeled pseudocode (INTEGRATION_GUIDE updated).

---

**Last Updated:** 2026-02-18
