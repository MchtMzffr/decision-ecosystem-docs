#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
P0.1 Remote/owner verification gate.
Ensures each repo's git remote origin URL uses the canonical owner (e.g. MchtMzffr).
Run from docs repo: python tools/check_remote_owner.py --workspace <parent-of-docs> [--owner MchtMzffr]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

REPOS = [
    "decision-schema",
    "mdm-engine",
    "decision-modulation-core",
    "ops-health-core",
    "evaluation-calibration-core",
    "execution-orchestration-core",
    "decision-ecosystem-integration-harness",
    "decision-ecosystem-docs",
]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="P0.1: Verify git remote origin uses canonical owner."
    )
    ap.add_argument(
        "--workspace", required=True, help="Parent dir containing repo dirs"
    )
    ap.add_argument("--owner", default="MchtMzffr", help="Canonical GitHub owner")
    args = ap.parse_args()
    workspace = os.path.abspath(args.workspace)
    owner = args.owner
    errors: list[str] = []

    for repo in REPOS:
        repo_path = os.path.join(workspace, repo)
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            continue
        try:
            out = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            url = (out.stdout or "").strip()
            if not url:
                errors.append(f"{repo}: no origin URL")
                continue
            # Expect github.com/<owner>/<repo>.git or github.com/<owner>/<repo>
            if owner.lower() not in url.lower() or "github.com" not in url:
                errors.append(
                    f"{repo}: origin URL should contain github.com/{owner}/... (got {url})"
                )
        except Exception as e:
            errors.append(f"{repo}: {e}")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print("INV-REMOTE-OWNER: FAIL (remote/owner mismatch)", file=sys.stderr)
        return 1
    print("INV-REMOTE-OWNER: OK (all remotes use canonical owner)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
