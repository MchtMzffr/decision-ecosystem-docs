# Release Notes Standard and Templates

**Purpose:** Single standard for ecosystem release notes; copy-paste templates for P0 release alignment.  
**Invariants:** INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1 (see below).

---

## 1. Global release notes standard

Every core repo release MUST use the same section order.

### Release title

- Use tag as title: **vX.Y.Z**

### Sections (mandatory order)

1. **Summary**
2. **Compatibility**
3. **Security**
4. **Changes**
5. **Verification**
6. **Links**

### Release-level invariants

| Invariant | Rule |
|-----------|------|
| **INV-REL-TAG-1** | `tag == pyproject.version` (tag string matches `[project].version` on main) |
| **INV-REL-SSOT-1** | Core repos depend only on `decision-schema` (no core↔core dependencies) |
| **INV-REL-SEC-1** | No secrets in release; redaction / kill-switch / fail-closed preserved (per repo scope) |

---

## 2. Repo-specific templates (copy-paste)

Use these for the two P0 actions in NEXT_STEPS_ROADMAP: publish **decision-schema v0.2.2** and **decision-modulation-core v0.1.0** (first release). Replace `TBD` with commit/PR references when known.

---

### A) decision-schema — v0.2.2 (publish needed)

```markdown
## Summary
This release publishes `decision-schema` version **0.2.2** as the canonical SSOT contract for the Decision Ecosystem.

## Compatibility
- Contract-first SSOT. All cores should pin `decision-schema>=0.2.2,<0.3`.
- **Invariant:** tag version equals `pyproject.toml [project].version`.

## Security
- No secrets. Public-safe contract surfaces only.

## Changes
- Contract/trace registry updates and validation improvements (see commits/PRs: TBD).

## Verification
- ✅ Unit tests: (TBD count; should match CI)
- ✅ Schema compatibility gates: PASS

## Links
- Repository: https://github.com/MchtMzffr/decision-schema
- Tags: https://github.com/MchtMzffr/decision-schema/tags
- Ecosystem contract matrix: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/ECOSYSTEM_CONTRACT_MATRIX.md
```

---

### B) decision-modulation-core — v0.1.0 (first release needed)

```markdown
## Summary
First public release of `decision-modulation-core` (**v0.1.0**). Implements deterministic guard/modulation pipeline converting `Proposal` → `FinalDecision`.

## Compatibility
- Depends only on `decision-schema` (core dependency rule).
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
- ✅ Unit tests: PASS
- ✅ Guard order determinism: PASS
- ✅ Fail-closed invariant: PASS

## Links
- Repository: https://github.com/MchtMzffr/decision-modulation-core
- Dependency cleanup note: https://github.com/MchtMzffr/decision-modulation-core/blob/main/docs/DEPENDENCY_CLEANUP.md
- Tags: https://github.com/MchtMzffr/decision-modulation-core/tags
```

---

### C) Micro-template (already-tagged repos)

For mdm-engine, ops-health-core, evaluation-calibration-core, execution-orchestration-core when publishing a new patch/minor and tag is already aligned:

```markdown
## Summary
Release vX.Y.Z. See CHANGELOG/commits for details.

## Compatibility
- tag == pyproject.version
- schema minor: 0.2.x (expected)

## Security
- No secrets; fail-closed preserved.

## Verification
- ✅ Tests: PASS

## Links
- Repo: <repo URL>
- Tags: <tags URL>
```

---

## 3. Tag/release procedure (fail-closed, minimum risk)

Same steps for every repo:

1. **main** clean; all tests PASS.
2. **pyproject.toml** `version` = target (e.g. `0.2.2`).
3. `git tag vX.Y.Z`
4. `git push origin vX.Y.Z`
5. On GitHub: **Releases** → **Draft a new release** → choose tag → paste release notes from section 2 (or 2.C) → Publish.
6. **Docs repo:** Update `NEXT_STEPS_ROADMAP.md` release alignment table (“Latest tag/release” column and “Next action” if needed). Optionally refresh contract matrix / verification checklist links.

**Check:** INV-RM-REL-1 and INV-REL-TAG-1 both satisfied.

---

## 4. P3 automation (design only)

For now the “update table when you publish” rule is sufficient. In P3, a small script in the docs repo could:

- Read `pyproject.version` from each core repo (workspace or raw URL),
- Parse the release alignment table in NEXT_STEPS_ROADMAP.md,
- Fail CI if any row is inconsistent (e.g. pyproject says 0.2.2 but table says v0.2.1 as latest).

This would drive human error toward zero for INV-RM-REL-1.

---

**Last updated:** 2026-02-19  
**Status:** Standard and templates adopted for P0 release alignment.
