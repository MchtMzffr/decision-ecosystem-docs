#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-SYNC-1 (Workspace–Main Parity): Fail-closed check that all repos have
clean working tree and are not ahead of origin/main.
Run from docs repo: python tools/check_workspace_sync.py --workspace <parent-dir>
"""

import argparse
import subprocess
import sys
from pathlib import Path


# 8 repos per CI_COMPLIANCE_STANDARD: 6 cores + harness + docs. explainability-audit-core deferred.
REPO_DIRS = [
    "decision-schema",
    "mdm-engine",
    "decision-modulation-core",
    "ops-health-core",
    "evaluation-calibration-core",
    "execution-orchestration-core",
    "decision-ecosystem-integration-harness",
    "decision-ecosystem-docs",
]


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    out = (p.stdout or "").strip() + (p.stderr or "").strip()
    return p.returncode, out


def main() -> int:
    ap = argparse.ArgumentParser(description="INV-SYNC-1: workspace vs origin/main parity check.")
    ap.add_argument("--workspace", type=Path, required=True, help="Parent dir containing repo dirs")
    args = ap.parse_args()
    workspace = args.workspace.resolve()
    errors = []
    for name in REPO_DIRS:
        repo = workspace / name
        if not repo.is_dir():
            errors.append(f"{name}: directory not found")
            continue
        if not (repo / ".git").is_dir():
            errors.append(f"{name}: not a git repo")
            continue
        # working tree clean
        code, out = run(["git", "status", "--porcelain"], repo)
        if code != 0:
            errors.append(f"{name}: git status failed: {out}")
            continue
        if out:
            errors.append(f"{name}: working tree not clean (uncommitted changes)")
        # ahead of origin/main
        code, count_out = run(
            ["git", "rev-list", "--count", "origin/main..HEAD"],
            repo,
        )
        if code != 0:
            # branch might not exist or no remote
            try:
                code2, _ = run(["git", "rev-parse", "origin/main"], repo)
                if code2 != 0:
                    errors.append(f"{name}: origin/main not found")
            except Exception:
                pass
            continue
        try:
            ahead = int((count_out or "0").strip().split()[0])
        except (ValueError, IndexError):
            ahead = 0
        if ahead > 0:
            errors.append(f"{name}: {ahead} commit(s) ahead of origin/main (push required)")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print("INV-SYNC-1: FAIL (workspace not in parity with origin/main)", file=sys.stderr)
        return 1
    print("INV-SYNC-1: OK (all repos clean and in sync with origin/main)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
