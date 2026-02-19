<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Release Notes Standard and Templates

**Purpose:** Single standard for ecosystem release notes; copy-paste templates for P0 release alignment.  
**Invariants:** INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1 (see below).

**Link style:** When referencing this document from elsewhere in the docs repo, use the relative path `docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md` (branch/rename drift reduction; aligns with INV-DOC-LINK-1). In the templates below, the full GitHub URL is used so the link works from the published Release page.

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

### Verification section (proof-link standard)

Where applicable, use evidence-style lines so releases are auditable:

- `✅ Tests: PASS (CI run link: <url>)` — use the CI run URL for the tag (see §4). **REQUIRED** for publish: no TBD in release body (INV-REL-PROOF-1).
- `✅ Contract gate: PASS (expected schema minor: 2)` — or equivalent for the repo.

### Changes section (optional subheadings)

Without changing section order, you may structure **Changes** with: **Added** / **Changed** / **Fixed** / **Deprecated**. This speeds SemVer and deprecation reading.

### INV-REL-SEC-1 — Never in release notes

Release notes MUST NOT contain:

- Secrets, tokens, API keys
- Internal endpoints or non-public URLs
- Real user data, logs, or PII

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
- ✅ Unit tests: PASS (CI run link: TBD)
- ✅ Contract gate: PASS (expected schema minor: 2)

## Links
- Repository: https://github.com/MchtMzffr/decision-schema
- Tags: https://github.com/MchtMzffr/decision-schema/tags
- Ecosystem contract matrix: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/ECOSYSTEM_CONTRACT_MATRIX.md
- Release notes standard: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
```

---

### B) decision-modulation-core — v0.1.0 (first release needed)

```markdown
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
- ✅ Unit tests: PASS (CI run link: TBD)
- ✅ Guard order determinism: PASS
- ✅ Fail-closed invariant: PASS
- ✅ Contract gate: PASS (expected schema minor: 2)

## Links
- Repository: https://github.com/MchtMzffr/decision-modulation-core
- Dependency cleanup note: https://github.com/MchtMzffr/decision-modulation-core/blob/main/docs/DEPENDENCY_CLEANUP.md
- Tags: https://github.com/MchtMzffr/decision-modulation-core/tags
- Release notes standard: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
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
- ✅ Tests: PASS (CI run link: TBD)

## Links
- Repo: <repo URL>
- Tags: <tags URL>
- Release notes standard: https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/docs/RELEASE_NOTES_STANDARD_AND_TEMPLATES.md
```

---

## 3. Tag/release procedure (fail-closed, minimum risk)

### 3.1 Local validation (each repo)

```bash
git fetch origin
git checkout main
git pull --ff-only

# Working tree must be clean (fail-closed)
test -z "$(git status --porcelain)" || { echo "Working tree not clean"; exit 1; }

# Version check (Python 3.11+ has tomllib; else use: pip install tomli and tomli.load)
python -c "
import sys
try:
    import tomllib
except ImportError:
    import tomli as tomllib
print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])
"

# Tests
python -m pytest -q
```

**Note:** Version check requires Python 3.11+ (stdlib `tomllib`) or Python 3.10 with `pip install tomli` (use `import tomli as tomllib`). The snippet above tries tomllib first, then tomli.

### 3.2 Create tag (annotated recommended)

**decision-schema (v0.2.2):**

```bash
# Fail if tag already exists (avoid accidental re-publish)
git rev-parse "v0.2.2" >/dev/null 2>&1 && { echo "Tag v0.2.2 already exists"; exit 1; }
git tag -a v0.2.2 -m "v0.2.2"
git push origin v0.2.2
```

**decision-modulation-core (v0.1.0):**

```bash
# Fail if tag already exists
git rev-parse "v0.1.0" >/dev/null 2>&1 && { echo "Tag v0.1.0 already exists"; exit 1; }
git tag -a v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

### 3.3 GitHub Release (web UI)

- **Releases** → **Draft a new release**
- Choose tag (**v0.2.2** or **v0.1.0**)
- Paste the matching template from section 2 (A or B)
- Replace `TBD` with commit/PR or CI run links when known
- **Publish release**

### 3.4 Docs repo update (INV-RM-REL-1)

- In `NEXT_STEPS_ROADMAP.md` release alignment table:
  - decision-schema: latest tag = **v0.2.2**, next action = **OK**
  - decision-modulation-core: latest tag = **v0.1.0**, next action = **OK**

**Check:** INV-RM-REL-1 and INV-REL-TAG-1 both satisfied.

---

### 3.5 Release checklist (manual, fill before opening a release)

Use this before drafting a release (no CI requirement; discipline only):

| Step | decision-schema v0.2.2 | dmc-core v0.1.0 |
|------|-------------------------|------------------|
| main clean, tests PASS | ☐ | ☐ |
| pyproject version = target | ☐ 0.2.2 | ☐ 0.1.0 |
| Tag created and pushed | ☐ v0.2.2 | ☐ v0.1.0 |
| Release notes pasted (no secrets) | ☐ | ☐ |
| NEXT_STEPS_ROADMAP table updated | ☐ | ☐ |

---

## 4. Deterministic CI proof capture

To remove TBD from release notes in a deterministic way, CI must run on **tag push** and produce a **machine-readable proof artifact**. Use the script below to obtain the CI run URL and test counts from the tag’s workflow run.

### Invariants

| Invariant | Rule | Metric |
|-----------|------|--------|
| **INV-CI-TAG-1** | Tag push triggers CI | `on.push.tags: ["v*"]` in workflow; run count ≥ 1 after tag push |
| **INV-CI-PROOF-1** | CI produces machine-readable proof | Artifact `pytest-report-<py>` with `pytest-report.json`; JSON parseable |
| **INV-REL-PROOF-1** | Release notes contain no TBD for proof | CI run link and Tests lines must not contain TBD; TBD count = 0 in release body |

### Formula

- **CI run:** `sha_tag = git rev-list -n 1 <tag>` → latest successful `push` run for that SHA → `run.htmlUrl`.
- **Test counts:** From artifact `pytest-report.json` → `summary`: `{ passed, failed, skipped, total }`.

### Script: `tools/get_ci_proof.py`

From the **docs repo** root, with `gh` authenticated and the **core repo** cloned (e.g. `../decision-schema`):

```bash
# decision-schema
python tools/get_ci_proof.py --repo MchtMzffr/decision-schema --tag v0.2.2 --cwd ../decision-schema

# decision-modulation-core
python tools/get_ci_proof.py --repo MchtMzffr/decision-modulation-core --tag v0.1.0 --cwd ../decision-modulation-core
```

Output is Markdown you can paste into the **Verification** section of the release notes (CI run link + test counts). No secrets or tokens are written; `gh` uses local auth (INV-REL-SEC-1).

---

## 5. P3 automation (design only)

For now the “update table when you publish” rule is sufficient. In P3, a small script in the docs repo could:

- Read `pyproject.version` from each core repo (workspace or raw URL),
- Parse the release alignment table in NEXT_STEPS_ROADMAP.md,
- Fail CI if any row is inconsistent (e.g. pyproject says 0.2.2 but table says v0.2.1 as latest).

This would drive human error toward zero for INV-RM-REL-1.

---

**Last updated:** 2026-02-19  
**Status:** Standard and templates adopted for P0 release alignment.
