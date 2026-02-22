<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Security Scope — In-Scope and Out-of-Scope

**Purpose:** Define which **security threats** are in scope for this project and which invariants address them. Out-of-scope threats are explicitly listed so that “secure” is not overclaimed. Per INV-SEC-SCOPE-1 and [ACADEMIC_CRITIQUE_AND_REASONS.md](ACADEMIC_CRITIQUE_AND_REASONS.md).

**Scope:** Decision Ecosystem (all repos). This document is normative for security-related claims.

---

## 1. In-scope threats and mitigations

| Threat | In scope? | Mitigation / invariant | How enforced |
|--------|-----------|------------------------|--------------|
| **Secrets and PII committed to repo** | Yes | No secret/PII pattern in committed files. | INV-SEC-RED-1: gitleaks (or equivalent) in CI; `secret_scan` job in every workflow. |
| **Raw error messages exposing internals** | Yes | Runtime error surfaces are redacted and structured (`error_type`, `error_code`); raw `error_message` not exposed to callers. | INV-ERR-SURFACE-1: lint/grep + unit tests; use structured error types. |
| **Known vulnerable dependencies** | Yes | Python deps scanned for known CVEs; CI fails on findings. | CI: pip-audit (after pip upgrade to ≥26); coverage in P3. |
| **CI/workflow supply-chain (unpinned actions)** | Yes | Actions pinned to tag or SHA; minimal permissions. | INV-CI-ACT-PIN-1, INV-CI-PERM-1; check_ci_compliance.py. |

---

## 2. Out-of-scope (not addressed by this project)

| Threat / area | Out of scope? | Reason |
|---------------|----------------|--------|
| **Side-channel attacks** (timing, power, etc.) | Yes | No countermeasures; not in design scope. |
| **Runtime compromise** (e.g. process injection, host compromise) | Yes | Assumes trusted execution environment. |
| **Supply-chain beyond deps** (e.g. build tool compromise, repo takeover) | Partially | We pin actions and deps; we do not implement SLSA/attestation or signed builds. |
| **Authentication / authorization** (who may call the pipeline) | Yes | Pipeline is a library/integration layer; caller is responsible for authn/authz. |
| **Secrets at runtime** (e.g. env vars, vault) | Yes | No runtime secret management in scope; callers provide config. |
| **Data in transit / at rest encryption** | Yes | Not provided by this codebase; deployer responsibility. |
| **Security of dependent services** (e.g. GitHub, PyPI) | Yes | We rely on their security; no additional hardening. |

---

## 3. Invariant → threat mapping

| Invariant | Addressed threat |
|-----------|-------------------|
| INV-SEC-RED-1 | Committed secrets / PII in repo |
| INV-ERR-SURFACE-1 | Information leakage via raw error messages |
| CI pip-audit step | Known vulnerabilities in Python dependencies |
| INV-CI-ACT-PIN-1 | Malicious or tampered GitHub Actions |
| INV-CI-PERM-1 | Overprivileged CI jobs |

---

## 4. What we do not claim

- We do **not** claim that the system is “secure” in an unbounded sense.
- We do **not** claim protection against side-channel, runtime compromise, or advanced supply-chain attacks.
- We **do** claim: no committed secrets (by policy and CI), structured/redacted errors, dependency vulnerability scanning, and pinned CI actions with minimal permissions.

---

**Last updated:** 2026-02  
**Invariant:** INV-SEC-SCOPE-1 (docs/ECOSYSTEM_GATES_AND_INVARIANTS.md §15)
