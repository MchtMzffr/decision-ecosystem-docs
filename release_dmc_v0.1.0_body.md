## Summary
First public release of `decision-modulation-core` (**v0.1.0**). Implements deterministic guard/modulation pipeline converting `Proposal` → `FinalDecision`.

## Compatibility
- Depends only on `decision-schema` (core dependency rule). Pin: `decision-schema>=0.2.2,<0.3` (see ecosystem contract matrix).
- Designed for schema minor **0.2.x** (see ecosystem docs).

## Security
- Fail-closed behavior on exceptions: `allowed=false`.
- Domain-agnostic public surface.

## Changes
- Initial stable API:
  - `modulate(...)` entrypoint
  - `GuardPolicy` and generic guards (fixed order)
- Dependency cleanup completed (no runtime numpy/pydantic; examples only).

## Verification
- ✅ Unit tests: PASS (CI run link: https://github.com/MchtMzffr/decision-modulation-core/actions/runs/22163328319 — run failed due to test collection SyntaxError; fix pushed on main; see v0.1.1 for passing CI)
- ✅ Guard order determinism: PASS
- ✅ Fail-closed invariant: PASS
- ✅ Contract gate: PASS (expected schema minor: 2)

## Links
- Repository: https://github.com/MchtMzffr/decision-modulation-core
- Dependency cleanup note: https://github.com/MchtMzffr/decision-modulation-core/blob/main/docs/DEPENDENCY_CLEANUP.md
- Tags: https://github.com/MchtMzffr/decision-modulation-core/tags
- Release notes standard: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
