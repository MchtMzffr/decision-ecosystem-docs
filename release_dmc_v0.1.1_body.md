## Summary
Patch release **v0.1.1**: test collection fix (f-string SyntaxError) and version single-source sync (INV-V1).

## Compatibility
- Depends only on `decision-schema` (core dependency rule). Pin: `decision-schema>=0.2.2,<0.3`.
- Designed for schema minor **0.2.x**.

## Security
- Fail-closed behavior on exceptions: `allowed=false`.
- Domain-agnostic public surface.

## Changes
- Fixed test collection: `test_invariant_ci_0_workflow_hygiene.py` f-string SyntaxError (backslash in expression).
- Synced `dmc_core.version.__version__` with `pyproject.toml` (0.1.1) for INV-V1.

## Verification
- ✅ Tests: PASS (CI run link: https://github.com/MchtMzffr/decision-modulation-core/actions/runs/22164074830)
- ✅ Test counts: py3.11: total=31 passed=31 failed=0 skipped=0; py3.12: total=31 passed=31 failed=0 skipped=0
- ✅ Guard order determinism: PASS
- ✅ Fail-closed invariant: PASS
- ✅ Contract gate: PASS (expected schema minor: 2)

## Links
- Repository: https://github.com/MchtMzffr/decision-modulation-core
- Tags: https://github.com/MchtMzffr/decision-modulation-core/tags
- Release notes standard: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
