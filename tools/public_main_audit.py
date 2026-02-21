#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-PUBLIC-MAIN-1 / INV-PUBLIC-MAIN-2: Public main audit. Fail-closed, deterministic.
Verifies that key invariants hold on **public** GitHub main (raw.githubusercontent.com).
Any fetch error (HTTP != 200, timeout, exception) => FAIL (INV-PUBLIC-MAIN-2 fail-closed network).
Usage:
  python tools/public_main_audit.py [--owner MchtMzffr] [--proof-json path]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com"
CACHE_BUST = True  # append ?t=unix to reduce CDN cache hits

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


def fetch(owner: str, repo: str, path: str) -> tuple[int, str, str]:
    """Return (status_code or -1 on error, body or error message, url_used). Fail-closed: non-200 or exception = error."""
    url = f"{BASE}/{owner}/{repo}/main/{path}"
    if CACHE_BUST:
        url = f"{url}?t={int(time.time())}"
    headers = {
        "User-Agent": "DecisionEcosystem-Audit/1.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode("utf-8", errors="replace")
            return (r.status, body, url)
    except urllib.error.HTTPError as e:
        return (e.code, str(e), url)
    except Exception as e:
        return (-1, str(e), url)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="INV-PUBLIC-MAIN-1/2: Audit public GitHub main (fail-closed)."
    )
    ap.add_argument("--owner", default="MchtMzffr", help="GitHub org/user")
    ap.add_argument(
        "--proof-json",
        default="",
        help="Write machine-readable proof to this path (optional)",
    )
    args = ap.parse_args()
    owner = args.owner
    errors: list[str] = []
    proof_checks: list[dict] = []

    def _proof(name: str, url: str, code: int, ok: bool) -> None:
        proof_checks.append(
            {"name": name, "url": url, "status": code, "ok": ok and code == 200}
        )

    # LICENSE exists (INV-LIC-1)
    for repo in LICENSE_REPOS:
        code, _, url = fetch(owner, repo, "LICENSE")
        if code != 200:
            errors.append(f"{repo}/LICENSE: missing or not 200 (got {code})")
        _proof(f"{repo}/LICENSE", url, code, code == 200)

    # README no placeholder (INV-README-LIC-1, INV-LIC-SPDX-2)
    for repo in README_PLACEHOLDER_REPOS:
        code, body, url = fetch(owner, repo, "README.md")
        no_placeholder = (
            code == 200
            and "[Add your license]" not in body
            and "Add your license" not in body
        )
        if code != 200:
            errors.append(f"{repo}/README.md: not 200 (got {code})")
        elif not no_placeholder:
            errors.append(f"{repo}/README.md: contains license placeholder")
        _proof(f"{repo}/README.md", url, code, no_placeholder)

    # ops-health FORMULAS + README param name (INV-DOC-DRIFT-1)
    code, body, url = fetch(owner, OPS_FORMULAS_REPO, OPS_FORMULAS_PATH)
    if code != 200:
        errors.append(f"{OPS_FORMULAS_REPO}/{OPS_FORMULAS_PATH}: not 200 (got {code})")
    else:
        if (
            "max_rate_limit_events" in body
            or "max_rate_limit_events_per_window" in body
        ):
            errors.append(
                f"{OPS_FORMULAS_REPO}/FORMULAS.md: still uses max_rate_limit_events (doc/code drift)"
            )
        if "max_429_per_window" not in body:
            errors.append(
                f"{OPS_FORMULAS_REPO}/FORMULAS.md: missing max_429_per_window"
            )
    _proof(
        OPS_FORMULAS_PATH,
        url,
        code,
        code == 200
        and "max_429_per_window" in body
        and "max_rate_limit_events_per_window" not in body,
    )
    code, body, _ = fetch(owner, OPS_FORMULAS_REPO, OPS_README_PATH)
    if code == 200 and "max_rate_limit_events_per_window" in body:
        errors.append(
            f"{OPS_FORMULAS_REPO}/README.md: example still uses max_rate_limit_events_per_window"
        )

    # CI: tag trigger, no @main fallback (INV-CI-TAG-1, INV-CI-NONDET-0)
    for repo in CI_REPOS:
        code, body, url = fetch(owner, repo, CI_PATH)
        if code != 200:
            errors.append(f"{repo}/ci.yml: not 200 (got {code})")
            _proof(f"{repo}/ci.yml", url, code, False)
            continue
        no_main = (
            "decision-schema.git@main" not in body
            and "decision-schema.git@main " not in body
        )
        if 'tags: ["v*"]' not in body and 'tags: ["v*"]' not in body:
            errors.append(f"{repo}/ci.yml: missing on.push.tags v* (INV-CI-TAG-1)")
        if not no_main:
            errors.append(
                f"{repo}/ci.yml: decision-schema fallback uses @main (INV-CI-NONDET-0)"
            )
        if (
            repo == "decision-ecosystem-integration-harness"
            and "decision-modulation-core" in body
            and "@main" in body
        ):
            if "@v0.1.1" not in body and "@v0.1.0" not in body:
                errors.append(
                    f"{repo}/ci.yml: dmc fallback uses @main (INV-CI-NONDET-0)"
                )
        _proof(
            f"{repo}/ci.yml",
            url,
            code,
            no_main and ("@v0.2.2" in body or "@v0.2.1" in body),
        )

    # INV-SSOT-REALITY-1: decision-schema version 0.2.2 on public main
    code, body, url = fetch(owner, SCHEMA_REPO, SCHEMA_PYPROJECT)
    if code != 200:
        errors.append(f"{SCHEMA_REPO}/pyproject.toml: not 200 (got {code})")
    else:
        if (
            f'version = "{SCHEMA_VERSION_EXPECTED}"' not in body
            and f"version = '{SCHEMA_VERSION_EXPECTED}'" not in body
        ):
            errors.append(
                f"{SCHEMA_REPO}/pyproject.toml: expected version {SCHEMA_VERSION_EXPECTED} (INV-SSOT-REALITY-1)"
            )
    _proof(
        f"{SCHEMA_REPO}/pyproject.toml",
        url,
        code,
        code == 200 and SCHEMA_VERSION_EXPECTED in body,
    )

    # INV-CI-COMPLY-1: decision-schema CI has required steps
    code, body, url = fetch(owner, SCHEMA_REPO, CI_PATH)
    if code == 200:
        if "PARAMETER_INDEX" not in body and "check_parameter_index" not in body:
            errors.append(
                f"{SCHEMA_REPO}/ci.yml: missing PARAMETER_INDEX / check_parameter_index step"
            )
        if "upload-artifact" not in body:
            errors.append(f"{SCHEMA_REPO}/ci.yml: missing upload-artifact (proof)")
    else:
        errors.append(f"{SCHEMA_REPO}/ci.yml: not 200 (got {code})")
    _proof(
        f"{SCHEMA_REPO}/ci.yml", url, code, code == 200 and "upload-artifact" in body
    )

    # Docs repo: public_main_audit.py must be present (deterministic proof)
    code, _, url = fetch(owner, DOCS_REPO, DOCS_AUDIT_PATH)
    if code != 200:
        errors.append(
            f"{DOCS_REPO}/{DOCS_AUDIT_PATH}: not 200 (got {code}) — audit script must be on public main"
        )
    _proof(DOCS_AUDIT_PATH, url, code, code == 200)

    # INV-OWNER-REF-1: no wrong-owner links in READMEs
    for repo in README_PLACEHOLDER_REPOS + [
        SCHEMA_REPO,
        "decision-modulation-core",
        "execution-orchestration-core",
    ]:
        code, body, url = fetch(owner, repo, "README.md")
        if code == 200 and WRONG_OWNER_PATTERN.search(body):
            errors.append(
                f"{repo}/README.md: contains wrong owner link (INV-OWNER-REF-1)"
            )
        _proof(
            f"{repo}/README owner",
            url,
            code,
            code == 200
            and not (WRONG_OWNER_PATTERN.search(body) if code == 200 else False),
        )

    if args.proof_json:
        out = {"owner": owner, "checks": proof_checks, "ok": len(errors) == 0}
        Path(args.proof_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.proof_json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print("INV-PUBLIC-MAIN-1: FAIL (public main drift)", file=sys.stderr)
        return 1
    print("INV-PUBLIC-MAIN-1: OK (public main audit passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
