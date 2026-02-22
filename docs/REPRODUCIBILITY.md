<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Reproducibility — Versioned Snapshots for Releases and Publications

**Purpose:** Define how to document a **versioned snapshot** for major releases or publications so that “this report or paper refers to this exact version” is citable. Per INV-REPRO-1 and [ACADEMIC_CRITIQUE_AND_REASONS.md](ACADEMIC_CRITIQUE_AND_REASONS.md).

**Scope:** Decision Ecosystem (all repos). Apply for each **major release** or when citing the ecosystem in a **publication** (paper, report, audit).

---

## 1. When to document a snapshot

- **Major release:** When publishing a new minor or major version of the ecosystem (e.g. schema 0.3.0, or “CIA v0.3” harness release).
- **Publication:** When citing the Decision Ecosystem in a paper, technical report, or external audit.
- **Compliance / audit:** When an auditor or regulator requires a fixed reference version.

---

## 2. Minimum snapshot content

For each snapshot, record **at least one** of the following so that the exact state can be recovered:

| Method | What to record | Where to record |
|--------|----------------|------------------|
| **Git tags** | For each repo: repo name + tag (e.g. `decision-schema@v0.2.2`, `mdm-engine@v0.2.1`, …). | Release notes (e.g. RELEASE_NOTES_0.3.0 in docs or schema); or a **Snapshot** section in the release notes. |
| **Commit SHAs** | For each repo: repo name + full commit SHA on `main` (or the branch used for the release). | Same as above; or a dedicated `docs/snapshots/YYYY-MM-DD_<release-label>.md` file. |
| **DOI (Zenodo / other)** | Upload a bundle (e.g. zip of all repos at the tagged commits) and obtain a DOI. Document the DOI and the list of tags/SHAs it contains. | Release notes + REPRODUCIBILITY.md (e.g. “Release vX.Y.Z → DOI: 10.5281/zenodo.…”). |

---

## 3. Recommended process (per release)

1. **Before release:** Ensure all repos are tagged (or at least have the commit SHAs to be released).
2. **At release:** In the release notes or in this doc (e.g. “Recorded snapshots” table), add one row:
   - **Label** (e.g. “Ecosystem 0.2.2”, “CIA v0.3”),
   - **Date** (YYYY-MM-DD),
   - **Repos + tags or SHAs** (e.g. `decision-schema:v0.2.2`, `mdm-engine:v0.2.1`, …),
   - **Optional:** DOI if a bundle was deposited.
3. **For publications:** In the paper or report, cite the snapshot (e.g. “Decision Ecosystem, snapshot 2026-02-19, tags: …” or “DOI: …”).

---

## 4. Example: snapshot table (to be updated at release)

| Snapshot label | Date | Repos and versions (tags) | DOI (optional) |
|----------------|------|---------------------------|----------------|
| Ecosystem 0.2.2 (current) | 2026-02 | decision-schema@v0.2.2, mdm-engine@v0.2.1, decision-modulation-core@v0.1.1, ops-health-core@v0.1.1, evaluation-calibration-core@v0.1.1, execution-orchestration-core@v0.1.0, explainability-audit-core@v0.1.0, harness (see NEXT_STEPS_ROADMAP), decision-ecosystem-docs@main | — |

*Update this table (or the linked release notes) whenever a new snapshot is recorded.*

---

## 5. Public accessibility

- Repositories must be **public** (or a stated mirror must be) for independent reproduction from tags/SHAs.
- If the ecosystem is **private by design**, state that in this doc and define who may access the snapshot (e.g. “on request”, “internal only”).

---

**Last updated:** 2026-02  
**Invariant:** INV-REPRO-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
