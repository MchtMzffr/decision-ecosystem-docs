# Decision Ecosystem — Documentation

Central documentation for the Decision Ecosystem: release guides, verification checklists, and governance.

**File structure standard:** [DOCS_REPO_STRUCTURE.md](DOCS_REPO_STRUCTURE.md) — What stays at root vs what goes to archive.

---

## Current documentation (CURRENT)

### Release & verification

- [GitHub Releases Guide](GITHUB_RELEASES_GUIDE.md) — Create and publish releases
- [Release Notes Standard and Templates](docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md) — Section order, INV-REL-TAG-1/SSOT-1/SEC-1, copy-paste templates for P0 (decision-schema v0.2.2, dmc-core v0.1.0)
- [Release Verification Checklist](RELEASE_VERIFICATION_CHECKLIST.md) — INV-REL-* and INV-REL-GH (including INV-REL-4)
- [Tag Governance](TAG_GOVERNANCE.md) — Tag immutability policy
- [Ecosystem Contract Matrix](ECOSYSTEM_CONTRACT_MATRIX.md) — Dependency ranges and CI fallback tags

**Tools (docs repo):**
- `tools/get_ci_proof.py` — CI run URL + test counts for release notes (run from docs repo; requires `gh` and local core repo clone).
- `tools/check_release_alignment.py` — INV-DOC-DRIFT-1: roadmap table vs local `pyproject.version`; run with `--workspace <parent-of-docs>`.

### CI & operations

- [CI Reliability](CI_RELIABILITY.md) — Why CI may flake and what we did to reduce it

### Architecture & governance

- [Architecture](ARCHITECTURE.md) — Ecosystem overview (cores and integration)
- [Ecosystem Invariants](ECOSYSTEM_INVARIANTS.md) — Contract, CI, docs, license checklist (INV-CORE-DEP-1, INV-LIC-1, INV-DOC-DRIFT-1, etc.)
- [Branch Governance](BRANCH_GOVERNANCE.md) — Branch rules; dev vs CI fallback (INV-GOV-1, INV-GOV-2)
- [Formulas](FORMULAS.md) — Invariants and formulas
- [Integration Guide](INTEGRATION_GUIDE.md) — How to integrate cores

### Roadmap & summaries

- [Next Steps Roadmap](NEXT_STEPS_ROADMAP.md) — Planned work
- [Task Completion Summary](TASK_COMPLETION_SUMMARY.md) — Completed work

### Analysis & reports (max 2 at root — INV-DOC-ANALYSIS-LIMIT-1)

- [Academic Static Analysis Report](ACADEMIC_STATIC_ANALYSIS_REPORT.md)
- [Ecosystem QA Static Analysis Report](ECOSYSTEM_QA_STATIC_ANALYSIS_REPORT.md)
- [Static Analysis & Code Quality — 5N1K and Control](docs/STATIC_ANALYSIS_CODE_QUALITY_5N1K_AND_CONTROL.md) — 5N1K, Feynman, uygunsuzluk/eksik/öneri listesi, akademik kontrol matrisi
- [Docs Static Analysis TODO — Completion](docs/DOCS_STATIC_ANALYSIS_TODO_COMPLETE.md) — Governance/release doc alignment and summary checklist

---

## Archive (historical snapshots)

Point-in-time verification and session reports are under **archive** so CURRENT stays clear:

- [archive/2026-02-17/](archive/2026-02-17/) — Verification snapshots from 2026-02-17 (e.g. FINAL_RELEASE_VERIFICATION, RELEASE_VERIFICATION_COMPLETE)
- [archive/2026-02-19/](archive/2026-02-19/) — Session/migration/sprint summaries and reports (per DOCS_REPO_STRUCTURE §7)

For current verification always use [RELEASE_VERIFICATION_CHECKLIST.md](RELEASE_VERIFICATION_CHECKLIST.md).

---

All documents in this repository are the single source of truth for ecosystem-wide release, verification, and governance practices.

## License

MIT License. See [LICENSE](LICENSE).
