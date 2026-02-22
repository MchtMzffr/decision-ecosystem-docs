<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Repository Registry (INV-REPO-REG-1) — SSOT

**Purpose:** Single source of truth for which repos belong to the ecosystem and how they are classified. Stops "8 vs 9 repo" drift; CI and docs read from here.

**Invariant:** INV-REPO-REG-1 — Ecosystem repo list and types are defined only in this registry. Metric: `repo_registry_count == expected`, `unknown_repo_in_ci == 0`.

---

## Registry table

| repo_name | repo_type | status | canonical_import | latest_tag |
|-----------|-----------|--------|------------------|------------|
| decision-schema | core | released | decision_schema | v0.2.2 |
| mdm-engine | core | released | mdm_engine | v0.2.1 |
| decision-modulation-core | core | released | dmc_core | v0.1.1 |
| ops-health-core | core | released | ops_health_core | v0.1.1 |
| evaluation-calibration-core | core | released | eval_calibration_core | v0.1.1 |
| execution-orchestration-core | core | released | execution_orchestration_core | v0.1.0 |
| decision-ecosystem-integration-harness | harness | released | harness | — |
| decision-ecosystem-docs | docs | released | — | — |
| explainability-audit-core | experimental | released | explainability_audit_core | v0.1.0 |

- **repo_type:** `core` | `harness` | `docs` | `experimental`. "6 core" narrative = first 6 rows with type=core.
- **status:** `released` (has tag/release) | `unreleased`.
- **canonical_import:** Top-level Python import for INV-CI-BUILD-SMOKE-1 (wheel smoke). `—` = not a Python package or N/A.
- **latest_tag:** Git tag for released; `—` if not applicable.

---

## Usage

- **CI compliance checker:** Repo list and types may be read from this file when present (fallback: built-in list).
- **Version truth:** Per INV-REL-SSOT-2, version in docs = `pyproject.toml` + Git tag; this table’s `latest_tag` must match that.
- **New repo:** Add a row; set type and status. **INV-REPO-REG-SSOT-1:** `check_workspace_sync` and `check_ci_compliance` read repo list from this file when present (no separate REPO_DIRS to maintain).

---

**Last updated:** 2026-02-19  
**References:** CI_COMPLIANCE_STANDARD.md, ECOSYSTEM_INVARIANTS.md
