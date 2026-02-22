# P3 — CI/CD Maturity Checklist

**Date:** 2026-02  
**Scope:** Secret scan, vulnerability scan (pip audit), and coverage gate applied across core repos, harness, and explainability-audit-core.

---

## 1. Summary

| Gate | Status | Where |
|------|--------|--------|
| **Secret scan** | In place | All repos: `secret_scan` job with gitleaks/gitleaks-action@v2 (INV-SEC-RED-1). explainability-audit-core had no secret_scan; added. |
| **Vulnerability scan** | In place | All Python repos: step "Vulnerability scan (pip audit)" after Install package; `pip install -U 'pip>=26.0'` then `pip install pip-audit && pip-audit`. Pip upgrade avoids CVE in runner pip; pip-audit fails CI if known vulnerabilities in dependencies. |
| **Coverage gate** | In place | All test jobs: `pytest ... --cov=. --cov-fail-under=30 --no-cov-on-fail`. Minimum 30% line coverage required; can be raised per repo later. |

---

## 2. Repos updated

- **decision-schema:** pip audit step, `--cov-fail-under=30`.
- **mdm-engine:** pip audit step, `--cov-fail-under=30`.
- **decision-modulation-core:** pip audit step, `--cov-fail-under=30`.
- **ops-health-core:** pip audit step, `--cov-fail-under=30`.
- **evaluation-calibration-core:** pip audit step, `--cov-fail-under=30`.
- **execution-orchestration-core:** pip audit step, `--cov-fail-under=30`.
- **decision-ecosystem-integration-harness:** pip audit in both core_only and full_stack jobs; `--cov-fail-under=30` on both pytest steps.
- **explainability-audit-core:** Full CI alignment: added `secret_scan` job, Ruff check/format, INV-BUILD-1, pip audit, pytest with coverage and `--cov-fail-under=30`, json report artifact.

---

## 3. Verification

- Run locally (from each repo): `pytest tests/ -v --cov=. --cov-fail-under=30` and `pip install pip-audit && pip-audit`.
- After push, confirm CI workflow runs and all jobs pass (secret_scan, test with pip audit and coverage gate).

---

## 4. Optional next steps

- Raise `--cov-fail-under` per repo (e.g. 50 or 80) where coverage is already high.
- Add Dependabot or similar for dependency update PRs (GitHub-native).
- Document pip-audit and coverage threshold in CI_COMPLIANCE_STANDARD (e.g. new subsection P3 gates).

---

**End of checklist.** P3 CI/CD maturity items are implemented; verify via CI runs after push.
