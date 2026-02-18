# Ecosystem Contract Matrix

**Purpose:** Single reference for decision-schema version ranges and CI fallback tags across the ecosystem.

---

## decision-schema dependency (required range)

| Repository | decision-schema range | CI fallback tag | Notes |
|------------|------------------------|-----------------|--------|
| decision-schema | — | — | SSOT |
| mdm-engine | >=0.2.1,<0.3 | @v0.2.2 | |
| decision-modulation-core | >=0.2,<0.3 | @v0.2.2 | |
| ops-health-core | >=0.2.1,<0.3 | @v0.2.2 | |
| evaluation-calibration-core | >=0.2,<0.3 | @v0.2.2 | |
| execution-orchestration-core | >=0.2.2,<0.3 | @v0.2.2 | Uses `exec.*` trace keys |
| integration-harness | >=0.2.1,<0.3 (decision-schema); others per table | @v0.2.2, @v0.2.1, @v0.1.1 | Tag-pinned for determinism |

---

## Policy

- **CI / release:** Fallbacks must use tags (`@vX.Y.Z`). See **RELEASE_VERIFICATION_CHECKLIST.md**.
- **SemVer:** decision-schema is SSOT; breaking changes = major bump. Cores pin minor range.
- **Trace keys:** execution-orchestration-core owns `exec.*` namespace (registered in decision-schema 0.2.2).

---

**Last Updated:** 2026-02-18
