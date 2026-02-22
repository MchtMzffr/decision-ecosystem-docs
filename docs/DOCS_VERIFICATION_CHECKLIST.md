<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Documentation Verification Checklist — Gaps, Errors, Unapplied Steps

**Purpose:** Single reference list: documents are scanned against standards and actual state; **gaps**, **incorrect or inconsistent information**, and **unapplied steps** are recorded here.  
**Created:** 2026-02-19  
**Applied:** 2026-02-19 — A1–A5, Y1–Y3, U1–U4, T1–T2 fixes applied (DOCS_REPO_STRUCTURE, RELEASE_VERIFICATION_CHECKLIST, check_workspace_sync, NEXT_STEPS_ROADMAP, ECOSYSTEM_INVARIANTS, CI_COMPLIANCE_STANDARD §3, README, ECOSYSTEM_CONTRACT_MATRIX, INV-CI-BUILD-SMOKE-1 in all core/harness CI, check_ci_compliance pin/perm/proof).  
**Usage:** Add new findings to the table; note resolved items.

---

## 1. Omitted (Missing / Not in document or list)

| # | Topic | Where | Description |
|---|-------|--------|-------------|
| A1 | **ECOSYSTEM_INVARIANTS.md** not in root allowlist | DOCS_REPO_STRUCTURE.md §2.1 | README links to it under "Architecture & governance"; root allowlist table does not list it. Add it or include under "Governance" row. |
| A2 | **RELEASE_VERIFICATION_CHECKLIST** — Version Single-Source table missing 2 repos | RELEASE_VERIFICATION_CHECKLIST.md | Table has only 4 repos (decision-schema, mdm-engine, ops-health-core, evaluation-calibration-core). **decision-modulation-core** and **execution-orchestration-core** should be added (align with NEXT_STEPS_ROADMAP P0 table). |
| A3 | **RELEASE_VERIFICATION_CHECKLIST** — INV-REL-1 checklist template missing dmc-core | RELEASE_VERIFICATION_CHECKLIST.md §Checklist Template | "INV-REL-1 (Version Single-Source)" items have no row for decision-modulation-core; add it. |
| A4 | **check_workspace_sync.py** — decision-ecosystem-docs not in repo list | tools/check_workspace_sync.py REPO_DIRS | INV-SYNC-1 says "all repos"; standard counts 8 repos. Sync script has **explainability-audit-core** but not **decision-ecosystem-docs**. Add docs; document or drop explainability if optional/deferred. |
| A5 | **NEXT_STEPS_ROADMAP** — integration-harness not in P0 table | NEXT_STEPS_ROADMAP.md | P0 Release Alignment table has no harness. If harness has pyproject version + tag, it may need to be in the table for INV-DOC-DRIFT-1; otherwise document "harness version not in table" as a deliberate choice. |

---

## 2. Incorrect / Inconsistent information

| # | Topic | Where | Description |
|---|-------|--------|-------------|
| Y1 | **INV-SYNC-1 metric shorthand** | ECOSYSTEM_INVARIANTS.md | Table says "Done = Gates_present ∧ Main_parity"; CI_COMPLIANCE_STANDARD §6.1 has **Done = (Gates_present = 1) ∧ (CI_pass = 1) ∧ (Main_parity = 1)**. CI_pass is not explicit in the invariant list; either add CI_pass to ECOSYSTEM_INVARIANTS or add a note "CI_pass included" next to Main_parity. |
| Y2 | **CI Compliance Standard §3** — Script described as "optional" | docs/CI_COMPLIANCE_STANDARD.md §3 | Text says "Automated (optional): A script could grep...". With INV-CI-COMPLY-2 the script is required (runs in docs CI). §3 should be updated: automation is required, script name and §7 reference should be given. |
| Y3 | **README duplicate link** | README.md | "Analysis & reports" links to CI Compliance Standard as "INV-CI-COMPLY-1: required CI steps..."; "CI & operations" has "INV-CI-COMPLY-1/2... compliance checker". Same doc in two places; one short one long. Keep both up to date (emphasise INV-CI-COMPLY-2 and checker). |

---

## 3. Step not applied (Defined in standard / invariant, not implemented)

| # | Topic | Defined where | Status |
|---|-------|----------------|--------|
| U1 | **INV-CI-BUILD-SMOKE-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_INVARIANTS | No core/harness CI has `pip install dist/*.whl` + minimal import smoke after build. Step not added. |
| U2 | **INV-CI-ACT-PIN-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_GATES §13 | Actions `uses:` pin check is not done inside **check_ci_compliance.py**. No automated verification; manual or script extension needed. |
| U3 | **INV-CI-PERM-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_GATES §13 | `permissions: { contents: read }` not checked by checker. In practice: manual/grep for workflows; add to checker if automation desired. |
| U4 | **INV-CI-PROOF-STD-1** (path/format) | CI_COMPLIANCE_STANDARD §2.5 | Checker only looks for "pytest-report" string; artifact path is not verified as `pytest-report.json` or `artifacts/pytest-report.json`. Tighten checker for full format compliance if needed. |

---

## 4. Inconsistency (Two sources disagree)

| # | Topic | Source 1 | Source 2 | Recommendation |
|---|-------|----------|-----------|----------------|
| T1 | **Repo list: 8 vs 7 + explainability** | CI_COMPLIANCE_STANDARD, ECOSYSTEM_GATES: "8 repos" (6 core + harness + docs) | check_workspace_sync: 7 dirs (6 core + harness + explainability; **no docs**) | Single SSOT: either "8 repo = 6 core + harness + docs" and add docs to sync, document explainability as optional; or update repo definition. |
| T2 | **decision-schema version range** | CI standard: cores ">=0.2.2,<0.3" | ECOSYSTEM_CONTRACT_MATRIX: mdm-engine ">=0.2.1,<0.3" | If intentional (mdm 0.2.1 accepted) add note in contract matrix; otherwise update to 0.2.2. |

---

## 5. Summary (To do)

- **Omitted (resolved):** ECOSYSTEM_INVARIANTS in DOCS_REPO_STRUCTURE allowlist; dmc+exec-orch in RELEASE_VERIFICATION; check_workspace_sync reads REPO_REGISTRY; harness policy (INV-RM-SCOPE-1) in roadmap.
- **Incorrect/inconsistent (resolved):** INV-SYNC-1 = git only; INV-CI-PASS-1 separate; §2.4 mandatory+N/A; README INV-CI-COMPLY-2 fail-closed.
- **Not applied:** INV-CI-BUILD-SMOKE-1 (smoke step in workflows), INV-CI-ACT-PIN-1 / INV-CI-PERM-1 (in checker or separate script), INV-CI-PROOF-STD-1 (path/format in checker).
- **Inconsistency:** decision-schema 0.2.1/0.2.2 = SSOT public main (audit expects 0.2.2); keep contract matrix up to date.

---

## 6. External review (GitHub main) — 2026-02

**Source:** Review was done over files on GitHub main branch; some standard files could not be fetched and were marked "not verified".

**Workspace vs public main:** "Correct in workspace" is valuable; **DONE = evidence on public main** (INV-PUBLIC-MAIN-1). If public main differs (push missing or different remote), the claim should not be updated.

| P0 item | Review (public main) | Workspace state | To close on public main |
|---------|----------------------|-----------------|--------------------------|
| P0.1 Matrix vs tag | decision-schema main 0.2.1, tag v0.2.1 | Some clones 0.2.2; matrix @v0.2.2. | Create and push v0.2.2 tag in decision-schema **or** lower matrix to v0.2.1. |
| P0.2 LICENSE + placeholder | LICENSE 404; README [Add your license] | In this workspace LICENSE exists, README fine. | Push all changes to **origin main**; verify with `python tools/public_main_audit.py`. |
| P0.3 ops-health doc↔code | FORMULAS/README max_rate_limit_events | In this workspace max_429_per_window. | Push ops-health-core main; confirm with audit script. |
| P0.4 CI minimal | CI has no tag/ruff/build/proof/artifact; @main fallback | In this workspace full CI + tag fallback. | Push all repo CI changes; check ci.yml with audit. |

**New rules (review recommendation → applied):**

- **INV-LIC-SPDX-2:** Repo-level LICENSE + README placeholder; CI verifies both. (ECOSYSTEM_INVARIANTS, ECOSYSTEM_GATES.)
- **INV-REL-NO-TBD-1:** No TBD in release body at publish time. (RELEASE_NOTES_STANDARD_AND_TEMPLATES.md.)
- **INV-DOC-LANG-2:** Normative docs in English; meta/operational (e.g. CI_RELIABILITY) may be in Turkish per allowlist. (ECOSYSTEM_GATES.) **Update:** All documentation is English (see .cursor/rules/documentation-english.mdc).

**2.1 / 2.2 (PARAMETER_INDEX, trace registry):** In workspace, PARAMETER_INDEX context keys are flat, trace keys dotted; exec.* registered in trace_registry. No extra patch applied.

**INV-PUBLIC-MAIN-1:** Public main verification is required before DONE. `python tools/public_main_audit.py --owner MchtMzffr` (or relevant owner) must exit 0. Script checks: LICENSE, README placeholder, ops-health FORMULAS/README drift, CI tag trigger and @main fallback.

**P0 Patch Plan (fail-closed, deterministic):** (1) **P0.1** Remote/owner: `git remote -v` → `github.com/MchtMzffr/<repo>.git`; `python tools/check_remote_owner.py --workspace <parent>`. (2) **P0.2** LICENSE + README placeholder: root LICENSE in all core/harness, no placeholder in README; INV-OWNER-REF-1 (MeetlyTR → MchtMzffr). (3) **P0.3** SSOT: decision-schema 0.2.2 + tag v0.2.2; pin >=0.2.2,<0.3; CI fallback @v0.2.2 (no @main). (4) **P0.4** CI_COMPLIANCE_STANDARD: decision-schema CI has PARAMETER_INDEX, ruff, build, artifact. New invariants: INV-PUBLIC-MAIN-2, INV-README-NO-PLACEHOLDER-1, INV-OWNER-REF-1, INV-SSOT-REALITY-1.

---

**Last updated:** 2026-02-19  
**References:** CI_COMPLIANCE_STANDARD.md, ECOSYSTEM_INVARIANTS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, DOCS_REPO_STRUCTURE.md, RELEASE_VERIFICATION_CHECKLIST.md, NEXT_STEPS_ROADMAP.md
