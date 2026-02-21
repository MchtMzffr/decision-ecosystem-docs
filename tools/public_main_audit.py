#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-PUBLIC-MAIN-1 / INV-PUBLIC-MAIN-2: Public main audit. Fail-closed, deterministic.
Verifies that key invariants hold on **public** GitHub main (raw.githubusercontent.com).
DONE is only valid when this audit passes for the configured owner.
Usage:
  python tools/public_main_audit.py [--owner MchtMzffr]
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request

BASE = "https://raw.githubusercontent.com"

# All core/harness repos must have LICENSE (INV-LIC-1)
LICENSE_REPOS = [
    "decision-schema",
    "mdm-engine",
    "decision-modulation-core",
    "ops-health-core",
    "evaluation-calibration-core",
    "execution-orchestration-core",
    "decision-ecosystem-integration-harness",
]
README_PLACEHOLDER_REPOS = [
    "ops-health-core",
    "evaluation-calibration-core",
    "mdm-engine",
    "decision-ecosystem-integration-harness",
]
# ops-health doc/code drift
OPS_FORMULAS_REPO = "ops-health-core"
OPS_FORMULAS_PATH = "docs/FORMULAS.md"
OPS_README_PATH = "README.md"
# CI: must have tag trigger, no @main fallback
CI_REPOS = ["decision-schema", "mdm-engine", "decision-ecosystem-integration-harness"]
CI_PATH = ".github/workflows/ci.yml"
# SSOT: decision-schema version and CI compliance
SCHEMA_REPO = "decision-schema"
SCHEMA_PYPROJECT = "pyproject.toml"
SCHEMA_VERSION_EXPECTED = "0.2.2"
# Docs repo: audit script must be present (INV-SSOT-REALITY-1)
DOCS_REPO = "decision-ecosystem-docs"
DOCS_AUDIT_PATH = "tools/public_main_audit.py"
# INV-OWNER-REF-1: canonical owner; wrong owner = fail
WRONG_OWNER_PATTERN = re.compile(r"github\.com/(?:MeetlyTR|meetlytr)/", re.I)


def fetch(owner: str, repo: str, path: str) -> tuple[int, str]:
    """Return (status_code or -1 on error, body or error message)."""
    url = f"{BASE}/{owner}/{repo}/main/{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DecisionEcosystem-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return (r.status, r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        return (e.code, str(e))
    except Exception as e:
        return (-1, str(e))


def main() -> int:
    ap = argparse.ArgumentParser(description="INV-PUBLIC-MAIN-1: Audit public GitHub main.")
    ap.add_argument("--owner", default="MchtMzffr", help="GitHub org/user")
    args = ap.parse_args()
    owner = args.owner
    errors: list[str] = []

    # LICENSE exists (INV-LIC-1)
    for repo in LICENSE_REPOS:
        code, _ = fetch(owner, repo, "LICENSE")
        if code != 200:
            errors.append(f"{repo}/LICENSE: missing or not 200 (got {code})")

    # README no placeholder (INV-README-LIC-1, INV-LIC-SPDX-2)
    for repo in README_PLACEHOLDER_REPOS:
        code, body = fetch(owner, repo, "README.md")
        if code != 200:
            errors.append(f"{repo}/README.md: not 200 (got {code})")
        elif "[Add your license]" in body or "Add your license" in body:
            errors.append(f"{repo}/README.md: contains license placeholder")

    # ops-health FORMULAS + README param name (INV-DOC-DRIFT-1)
    code, body = fetch(owner, OPS_FORMULAS_REPO, OPS_FORMULAS_PATH)
    if code != 200:
        errors.append(f"{OPS_FORMULAS_REPO}/{OPS_FORMULAS_PATH}: not 200 (got {code})")
    else:
        if "max_rate_limit_events" in body or "max_rate_limit_events_per_window" in body:
            errors.append(f"{OPS_FORMULAS_REPO}/FORMULAS.md: still uses max_rate_limit_events (doc/code drift)")
        if "max_429_per_window" not in body:
            errors.append(f"{OPS_FORMULAS_REPO}/FORMULAS.md: missing max_429_per_window")
    code, body = fetch(owner, OPS_FORMULAS_REPO, OPS_README_PATH)
    if code == 200 and "max_rate_limit_events_per_window" in body:
        errors.append(f"{OPS_FORMULAS_REPO}/README.md: example still uses max_rate_limit_events_per_window")

    # CI: tag trigger, no @main fallback (INV-CI-TAG-1, INV-CI-NONDET-0)
    for repo in CI_REPOS:
        code, body = fetch(owner, repo, CI_PATH)
        if code != 200:
            errors.append(f"{repo}/ci.yml: not 200 (got {code})")
            continue
        if 'tags: ["v*"]' not in body and "tags: [\"v*\"]" not in body:
            errors.append(f"{repo}/ci.yml: missing on.push.tags v* (INV-CI-TAG-1)")
        # Fallback: must not use @main when tag exists (allow @v0.2.2 etc.)
        if "github.com" in body and "@main" in body:
            if "decision-schema" in body and "@main" in body and "@v0.2.2" not in body and "@v0.2.1" not in body:
                errors.append(f"{repo}/ci.yml: decision-schema fallback uses @main (INV-CI-NONDET-0)")
        if repo == "decision-ecosystem-integration-harness" and "decision-modulation-core" in body and "@main" in body:
            if "@v0.1.1" not in body and "@v0.1.0" not in body:
                errors.append(f"{repo}/ci.yml: dmc fallback uses @main (INV-CI-NONDET-0)")

    # INV-SSOT-REALITY-1: decision-schema version 0.2.2 on public main
    code, body = fetch(owner, SCHEMA_REPO, SCHEMA_PYPROJECT)
    if code != 200:
        errors.append(f"{SCHEMA_REPO}/pyproject.toml: not 200 (got {code})")
    else:
        if f'version = "{SCHEMA_VERSION_EXPECTED}"' not in body and f"version = '{SCHEMA_VERSION_EXPECTED}'" not in body:
            errors.append(f"{SCHEMA_REPO}/pyproject.toml: expected version {SCHEMA_VERSION_EXPECTED} (INV-SSOT-REALITY-1)")

    # INV-CI-COMPLY-1: decision-schema CI has required steps (PARAMETER_INDEX, ruff, artifact)
    code, body = fetch(owner, SCHEMA_REPO, CI_PATH)
    if code == 200:
        if "PARAMETER_INDEX" not in body and "check_parameter_index" not in body:
            errors.append(f"{SCHEMA_REPO}/ci.yml: missing PARAMETER_INDEX / check_parameter_index step")
        if "upload-artifact" not in body:
            errors.append(f"{SCHEMA_REPO}/ci.yml: missing upload-artifact (proof)")
    else:
        errors.append(f"{SCHEMA_REPO}/ci.yml: not 200 (got {code})")

    # Docs repo: public_main_audit.py must be present (deterministic proof)
    code, _ = fetch(owner, DOCS_REPO, DOCS_AUDIT_PATH)
    if code != 200:
        errors.append(f"{DOCS_REPO}/{DOCS_AUDIT_PATH}: not 200 (got {code}) — audit script must be on public main")

    # INV-OWNER-REF-1: no wrong-owner links (e.g. MeetlyTR) in READMEs
    for repo in README_PLACEHOLDER_REPOS + [SCHEMA_REPO, "decision-modulation-core", "execution-orchestration-core"]:
        code, body = fetch(owner, repo, "README.md")
        if code == 200 and WRONG_OWNER_PATTERN.search(body):
            errors.append(f"{repo}/README.md: contains wrong owner link (INV-OWNER-REF-1)")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print("INV-PUBLIC-MAIN-1: FAIL (public main drift)", file=sys.stderr)
        return 1
    print("INV-PUBLIC-MAIN-1: OK (public main audit passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
