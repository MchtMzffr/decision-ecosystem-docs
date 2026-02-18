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
| **integration-harness** | `main` | Integration layer |

### Rationale

1. **Ecosystem Consistency**: All cores use `main` for uniformity
2. **Modern Standard**: GitHub's default branch naming (2020+)
3. **CI/CD Alignment**: All workflows and git fallbacks use `@main`

## Branch Naming Convention

- **`main`**: Source of truth, production-ready code
- **`develop`**: (Optional) Development branch for features
- **`release/*`**: (Optional) Release candidate branches
- **`hotfix/*`**: (Optional) Critical fixes

## Git Fallback URLs

When installing from git (fallback for PyPI), always use `@main`:

```bash
pip install "git+https://github.com/MchtMzffr/repo-name.git@main"
```

Examples:
- `decision-schema`: `git+https://github.com/MchtMzffr/decision-schema.git@main`
- `mdm-engine`: `git+https://github.com/MchtMzffr/mdm-engine.git@main`
- `evaluation-calibration-core`: `git+https://github.com/MchtMzffr/evaluation-calibration-core.git@main`

## CI/CD Workflows

All GitHub Actions workflows:
- Trigger on `main` branch pushes
- Use `@main` for git fallback installs
- Do not reference `master` branch (deprecated)

## Migration Notes

If any repository still has `master` branch:
1. Merge `master` → `main` (if needed)
2. Update default branch in GitHub settings
3. Update CI workflows to remove `master` triggers
4. Update git fallback URLs to `@main`
5. Delete `master` branch (after migration complete)

## Enforcement

- **INV-BRANCH-1**: All repos must use `main` as source of truth
- **INV-BRANCH-2**: CI workflows must trigger on `main` only
- **INV-BRANCH-3**: Git fallback URLs must use `@main`

---

**Last Updated**: 2026-02-17  
**Status**: ✅ All repos standardized on `main`
