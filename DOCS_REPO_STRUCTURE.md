<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# decision-ecosystem-docs — File Structure Standard

**Purpose:** This repo is the single source of truth (SSOT) for ecosystem-wide **governance, release, and verification**. A clear structure and rule set is applied instead of placing every file at root.

**Principles:** CURRENT (live, at-a-glance) vs ARCHIVE (historical snapshot); root holds only "living" documents; duplicates and old reports go to archive.

---

## 1. Repo purpose (clear)

- **Governance:** Branch/tag/release rules (INV-REL-*, INV-GOV-*)
- **Release & verification:** Checklist, contract matrix, tag policy
- **Architecture & integration:** Ecosystem overview, formulas, integration guide
- **Current status:** A **single** summary file for roadmap and completed work

Documents that do not serve this purpose or are "one-off session output" do **not** live permanently at root; they are moved to archive.

---

## 2. Root directory rules

### 2.1 Files allowed at root (allowlist)

Only files in the categories below (with the given names) may live at **root**. The README "Current documentation" section links **only** to these files.

| Category | File(s) | Description |
|----------|---------|-------------|
| **Release & verification** | `GITHUB_RELEASES_GUIDE.md`, `RELEASE_VERIFICATION_CHECKLIST.md`, `TAG_GOVERNANCE.md`, `ECOSYSTEM_CONTRACT_MATRIX.md` | Release process and invariant verification |
| **CI & operations** | `CI_RELIABILITY.md` | CI flakiness and mitigations |
| **Governance** | `BRANCH_GOVERNANCE.md` | Branch rules; dev vs CI fallback |
| **Architecture & guide** | `ARCHITECTURE.md`, `FORMULAS.md`, `INTEGRATION_GUIDE.md` | Ecosystem architecture, formulas, integration (DOC TRIO reference) |
| **Roadmap & status** | `NEXT_STEPS_ROADMAP.md`, `TASK_COMPLETION_SUMMARY.md` | Single "what's next" + single "what's done" summary |
| **Analysis (current)** | At most **1–2** current analysis reports (e.g. `ACADEMIC_STATIC_ANALYSIS_REPORT.md`, `ECOSYSTEM_QA_STATIC_ANALYSIS_REPORT.md`) | Older reports are moved to archive |
| **Meta** | `README.md`, `DOCS_REPO_STRUCTURE.md` (this file) | Repo description and this standard itself |

### 2.2 What must not stay at root

- Session/summary outputs (e.g. `SESSION_COMPLETE_SUMMARY.md`, `FINAL_SESSION_SUMMARY.md`)
- One-off migration/closure reports (e.g. `MIGRATION_SUMMARY.md`, `P0_CLOSURE_CHECKLIST.md`)
- Sprint/board files (e.g. `P2_SPRINT_BOARD_*.md`, `P3_KICKOFF_CHECKLIST.md`) — move to archive when done
- Historical verification snapshots (e.g. `FINAL_RELEASE_VERIFICATION.md`, `RELEASE_VERIFICATION_COMPLETE.md`) — only under `archive/YYYY-MM-DD/`
- Personal/operational notes (e.g. terminal or repo management guides) — optional `docs/operational/` or archive
- Old remediation/summary files (e.g. `VERSION_BUMP_SUMMARY.md`, `EXECUTION_ORCHESTRATION_CORE_CREATED.md`) — archive

**Rule:** When adding a new "summary" or "report", ask: "Is this permanent at root?" If not, create or move it under `archive/YYYY-MM-DD/`.

---

## 3. Folder structure (standard)

```
decision-ecosystem-docs/
├── README.md                          # Entry; CURRENT + Archive links only
├── DOCS_REPO_STRUCTURE.md             # This standard (meta)
├── ARCHITECTURE.md                    # Ecosystem architecture
├── FORMULAS.md                        # Formulas / invariant reference
├── INTEGRATION_GUIDE.md               # Integration guide
├── GITHUB_RELEASES_GUIDE.md
├── RELEASE_VERIFICATION_CHECKLIST.md
├── TAG_GOVERNANCE.md
├── ECOSYSTEM_CONTRACT_MATRIX.md
├── BRANCH_GOVERNANCE.md
├── CI_RELIABILITY.md
├── NEXT_STEPS_ROADMAP.md
├── TASK_COMPLETION_SUMMARY.md
├── [at most 1–2 current analysis reports]
│
├── archive/                           # Historical snapshots
│   └── YYYY-MM-DD/                    # Date-based (e.g. 2026-02-17)
│       ├── README.md                  # Content summary for that date
│       └── *.md                       # Reports/summaries for that date
│
├── docs/                              # Optional: extra technical docs
│   └── [e.g. STATIC_ANALYSIS_REMEDIATION_*.md]
│
└── examples/                          # Domain examples guide (if any)
    └── README.md
```

### 3.1 Archive rule (INV-DOC-2)

- **archive/YYYY-MM-DD/** = Snapshots for a given date (release verification, session summary, migration report, etc.).
- The README "Archive" section links only to subdirs under `archive/`; old single files like "Final Release Verification" do **not** stay at root.
- For a new dated snapshot, create a new folder: e.g. `archive/2026-02-19/`.

### 3.2 "Analysis & reports" at root

- The "Analysis & reports" listed in the README should be **at most 1–2** current reports.
- When a new analysis report is added, the previous one is moved under `archive/YYYY-MM-DD/` (or the README link is removed and the file is moved to archive).

---

## 4. Naming conventions

| Type | Rule | Example |
|------|------|---------|
| Governance / process | `UPPER_SNAKE_CASE.md` | `RELEASE_VERIFICATION_CHECKLIST.md` |
| Single-date snapshot | Under `archive/YYYY-MM-DD/`, meaningful name | `FINAL_RELEASE_VERIFICATION.md` |
| Analysis report | Descriptive, consistent | `ACADEMIC_STATIC_ANALYSIS_REPORT.md` |
| When adding new report | Prefer archive; avoid inflating root | `archive/2026-02-19/STATIC_ANALYSIS_P0_P1_APPLIED.md` |

---

## 5. README alignment (INV-DOC-1)

- The README "Current documentation" section lists **only** root files that comply with this standard.
- The "Archive" section links only to directories like `archive/YYYY-MM-DD/`.
- Obsolete or duplicate documents are removed from the README (the file may remain in archive).

---

## 6. Summary (one sentence)

**Root = only living, single-source documents; session summaries, migration reports, and historical snapshots live under `archive/YYYY-MM-DD/`.**

---

## 7. Current file classification (implementation guide)

Per this standard, below is what **stays at root** and what **moves to archive**. Use `archive/2026-02-19/` (or the relevant date) when performing the move.

### Keep at root (CURRENT)

| File | Reason |
|------|--------|
| `README.md` | Meta |
| `DOCS_REPO_STRUCTURE.md` | This standard |
| `ARCHITECTURE.md`, `FORMULAS.md`, `INTEGRATION_GUIDE.md` | DOC TRIO reference |
| `GITHUB_RELEASES_GUIDE.md`, `RELEASE_VERIFICATION_CHECKLIST.md`, `TAG_GOVERNANCE.md`, `ECOSYSTEM_CONTRACT_MATRIX.md` | Release & verification |
| `BRANCH_GOVERNANCE.md` | Governance |
| `CI_RELIABILITY.md` | CI & operations |
| `NEXT_STEPS_ROADMAP.md`, `TASK_COMPLETION_SUMMARY.md` | Roadmap & status |
| `ACADEMIC_STATIC_ANALYSIS_REPORT.md`, `ECOSYSTEM_QA_STATIC_ANALYSIS_REPORT.md` | At most 2 analysis (current) |
| `TAG_ALIGNMENT_COMPLETE.md` | Aligns with historical note; optionally move to archive |

### Move to archive (archive/2026-02-19 or appropriate date)

| File | Suggested destination |
|------|------------------------|
| Session/complete summaries, migration/branch migration reports | archive/YYYY-MM-DD/ |
| P0/P2/P3 closure, sprint board, issue pack | archive/ |
| Version bump, execution core created, workflow, CI legacy docs | archive/ |
| Remote verification, integration harness fixes | archive/ |
| Static analysis fixes, audit remediation | archive/ or docs/ |
| Terminal/Git/repo management guides | archive/ or docs/operational/ |
| Ecosystem roadmap (older version) | Merge into NEXT_STEPS_ROADMAP; old version to archive |

After the move, remove links to moved files from the README "Current documentation" section and add the relevant `archive/YYYY-MM-DD/` link to the Archive section. The temporary move plan file `archive_move_plan_2026-02-19.txt` is deleted or moved to archive when done (it is not on the allowlist).

---

## 8. Invariant gates (CI-verifiable)

Root and README rules are enforced in CI. Single source: `ROOT_ALLOWLIST.txt` (CI script reads this list).

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-DOC-ROOT-ALLOW-1** | Only allowlist files + `.github/`, `archive/`, `docs/`, `examples/` at root | root_non_allowed_count == 0 |
| **INV-DOC-ARCHIVE-SNAPSHOT-1** | Only `YYYY-MM-DD/` format dirs under `archive/` | count of non-matching dirs == 0 |
| **INV-DOC-README-CURRENT-1** | README "Current documentation" links only to root allowlist files | root-external link count == 0 |
| **INV-DOC-ANALYSIS-LIMIT-1** | At most 2 analysis/report files at root (`*_REPORT.md`, `*_ANALYSIS*.md`) | analysis_report_count ≤ 2 |

- **Workflow:** `.github/workflows/docs_structure_guard.yml` (on push/PR to `main`).
- **Script:** `.github/scripts/check_docs_root.py` (allowlist, archive path, README links, analysis count).
- When updating the allowlist, edit `ROOT_ALLOWLIST.txt`; the script treats it as the single source.

---

## 9. Archive move operation

The table (§7) is the single source. The move can be done in two ways:

- **Option A (manual):** `git checkout -b chore/archive-YYYY-MM-DD`, `mkdir -p archive/YYYY-MM-DD`, then `git mv <file> archive/YYYY-MM-DD/` for each file.
- **Option B (plan file):** In `archive_move_plan_YYYY-MM-DD.txt`, line format `SOURCE -> archive/YYYY-MM-DD/SOURCE`. Then:
  - `python .github/scripts/run_archive_move_from_plan.py archive_move_plan_2026-02-19.txt`
  - When the move is done, delete the plan file or move it to archive (it is not on the root allowlist).

After the move, run `python .github/scripts/check_docs_root.py` to verify invariants; CI should be green.
