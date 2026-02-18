# Decision Ecosystem Docs — Static Analysis TODO Completion

**Date:** 2026-02-18  
**Scope:** decision-ecosystem-docs repo as SSOT for governance, release, and verification.  
**Language:** All new/updated docs in English (conversation language remains at user preference).

---

## 1. Objectives (from static analysis)

- **Governance:** Single clear policy for branch/tag/release (no drift between docs).
- **Release & verification:** INV-REL-* and INV-REL-GH applied consistently; tag semantics correct.
- **Information architecture:** Clear split between CURRENT docs and historical snapshots (archive).

---

## 2. What was already in place (no change needed)

| Item | Status |
|------|--------|
| **INV-REL-4 (tag reachability)** | RELEASE_VERIFICATION_CHECKLIST already states: tag commit must be *ancestor* of main; verify with `git merge-base --is-ancestor vX.Y.Z origin/main`. |
| **BRANCH_GOVERNANCE (dev vs CI)** | Already split: dev/experiments may use `@main` (non-deterministic); CI/release must use tag `@vX.Y.Z` (INV-GOV-1, INV-GOV-2). |
| **TAG_ALIGNMENT_COMPLETE** | Already labeled "Historical incident report (not current policy)" and points to TAG_GOVERNANCE + INV-REL-4. |
| **ECOSYSTEM_CONTRACT_MATRIX.md** | Present at repo root; TAG_GOVERNANCE and README link to it. |
| **README CURRENT vs archive** | README links only to CURRENT docs; archive/2026-02-17 and archive/2026-02-19 linked under "Archive". |
| **ARCHITECTURE** | Already describes six cores including execution-orchestration-core. |
| **GITHUB_RELEASES_GUIDE** | execution-orchestration-core install: "If published to PyPI … Otherwise install from GitHub tag". |

---

## 3. Changes applied in this pass

| Priority | File | Change |
|----------|------|--------|
| **P0** | BRANCH_GOVERNANCE.md | Added **execution-orchestration-core** to the repository table (source of truth = main). |
| **P3** | INTEGRATION_GUIDE.md | Added upfront note: code blocks are either (a) verified against real API or (b) explicitly labeled pseudocode (INV-DOC-4). |
| **P3** | FORMULAS.md | Clarified that domain-specific names (e.g. Sharpe-like) are for illustration only; core vocabulary stays domain-agnostic. |
| **Roadmap** | NEXT_STEPS_ROADMAP.md | Marked P2 (DMC dependency cleanup) and P3 (F8 invariant extension) as ✅ DONE with short status text. |

---

## 4. Invariants (documented policy)

- **INV-GOV-1:** CI fallback URLs use tags (`@vX.Y.Z`), not `@main`.
- **INV-GOV-2:** Dev/experiment install guidance may allow `@main` (documented as non-deterministic).
- **INV-REL-4:** Tag commit must be ancestor of `main` (not necessarily main HEAD).
- **INV-DOC-1:** README quick links point only to CURRENT docs.
- **INV-DOC-2:** Historical reports live under `archive/YYYY-MM-DD/`.
- **INV-DOC-3:** All referenced local docs exist (ECOSYSTEM_CONTRACT_MATRIX present).
- **INV-DOC-4:** Integration code blocks either verified against real API or labeled pseudocode.
- **INV-DOC-LINK-1:** README internal doc links resolve on `main` (relative paths only; target files must exist). Metric: broken link count = 0. Optional CI guard: fail if any README-referenced relative doc path is missing.

---

## 5. Summary list (checklist)

- [x] Tag semantics: INV-REL-4 (ancestor) documented; no "tag == main HEAD" requirement.
- [x] Branch governance: Dev vs CI fallback split; execution-orchestration-core in repo table.
- [x] TAG_ALIGNMENT_COMPLETE: Historical only; no conflict with tag immutability.
- [x] ECOSYSTEM_CONTRACT_MATRIX: Present and linked.
- [x] CURRENT vs archive: README points to CURRENT; archive links explicit.
- [x] ARCHITECTURE: Six cores including execution-orchestration-core.
- [x] INTEGRATION_GUIDE: Code-block policy (verified API or pseudocode) stated.
- [x] FORMULAS: Domain-agnostic wording for generic metrics (DD, SR, etc.).
- [x] GITHUB_RELEASES_GUIDE: execution-orchestration-core install covers PyPI or git tag.
- [x] NEXT_STEPS_ROADMAP: P2 and P3 marked complete.
- [x] INV-DOC-LINK-1: README uses relative paths for doc links (e.g. `docs/DOCS_STATIC_ANALYSIS_TODO_COMPLETE.md`); CI may enforce broken-link check.

---

**Last updated:** 2026-02-18  
**Status:** Static analysis TODO list completed; docs aligned with governance and verification policy.
