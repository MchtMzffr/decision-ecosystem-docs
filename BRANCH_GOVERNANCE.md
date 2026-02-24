# Branch Governance — Decision Ecosystem

## Source of Truth Branch

**All repositories use `main` as the source of truth branch.**

### Repositories

| Repository | Source of Truth | Notes |
|------------|----------------|-------|
| **decision-schema** | `main` | SSOT contract |
| **mdm-engine** | `main` | Proposal generation |
| **decision-modulation-core** | `main` | Guards/risk |
| **ops-health-core** | `main` | Safety signals |
| **evaluation-calibration-core** | `main` | Metrics/reports |
| **execution-orchestration-core** | `main` | Execution orchestration |
| **integration-harness** | `main` | Integration layer |

### Rationale

1. **Ecosystem Consistency**: All cores use `main` for uniformity
2. **Modern Standard**: GitHub's default branch naming (2020+)
3. **CI/CD Alignment**: CI uses tag-pinned fallbacks (`@vX.Y.Z`); dev/experiments may use `@main` (non-deterministic)

## Branch Naming Convention

- **`main`**: Source of truth, production-ready code
- **`develop`**: (Optional) Development branch for features
- **`release/*`**: (Optional) Release candidate branches
- **`hotfix/*`**: (Optional) Critical fixes

## Git Fallback URLs — Two Policies

### Dev / experiments (non-deterministic)

For local development or one-off experiments you may use `@main` to get the latest code. This is **explicitly non-deterministic**: main moves over time.

```bash
pip install "git+https://github.com/MchtMzffr/repo-name.git@main"
```

Examples: `decision-schema`, `mdm-engine`, `evaluation-calibration-core` — use `@main` only when you accept non-deterministic builds.

### CI / release verification (deterministic)

For CI pipelines and release verification, **always use tag-pinned fallbacks** so builds are reproducible:

- **INV-GOV-1:** CI fallback ⇒ tag (e.g. `@v0.2.2`, `@v0.2.1`, `@v0.1.1`).
- See **RELEASE_VERIFICATION_CHECKLIST.md** for the exact tags each repo’s CI must use.

Do **not** use `@main` in CI fallbacks when a release tag exists.

## CI/CD Workflows

All GitHub Actions workflows:
- Trigger on `main` branch pushes only
- Use **tag-pinned** git fallbacks in CI (e.g. `@v0.2.2` for decision-schema); `@main` is for dev only
- Do not reference `master` branch (deprecated)

## Migration Notes

If any repository still has `master` branch:
1. Merge `master` → `main` (if needed)
2. Update default branch in GitHub settings
3. Update CI workflows to trigger on `main` only (remove `master` triggers)
4. Keep CI fallbacks tag-pinned (`@vX.Y.Z`); do not use `@main` in CI. For local dev only, `@main` is allowed.
5. Delete `master` branch (after migration complete)

## Enforcement

- **INV-BRANCH-1:** All repos must use `main` as source of truth
- **INV-BRANCH-2:** CI workflows must trigger on `main` only
- **INV-GOV-1:** CI fallback URLs must use tags (`@vX.Y.Z`), not `@main`
- **INV-GOV-2:** Dev/experiment install guidance may allow `@main` (documented as non-deterministic)

---

**Last Updated**: 2026-02-17  
**Status**: ✅ All repos standardized on `main`
