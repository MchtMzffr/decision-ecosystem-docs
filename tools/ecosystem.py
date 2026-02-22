#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Decision Ecosystem CLI: single-command install, test, release/sync checks.
Usage: python tools/ecosystem.py --workspace <parent-dir> <command>
Commands: install | test | check-release | check-sync
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Same repo list as check_workspace_sync (core + harness + docs)
REPO_DIRS = [
    "decision-schema",
    "mdm-engine",
    "decision-modulation-core",
    "ops-health-core",
    "evaluation-calibration-core",
    "execution-orchestration-core",
    "explainability-audit-core",
    "decision-ecosystem-integration-harness",
    "decision-ecosystem-docs",
]


def get_workspace(args: argparse.Namespace, tools_dir: Path) -> Path:
    """Resolve workspace; default to parent of docs repo when run from docs."""
    if getattr(args, "workspace", None):
        return Path(args.workspace).resolve()
    # Default: parent of decision-ecosystem-docs
    docs = tools_dir.parent
    if docs.name == "decision-ecosystem-docs":
        return docs.parent
    return Path.cwd()


def cmd_install(workspace: Path) -> int:
    """pip install -e for each repo (decision-schema first)."""
    order = ["decision-schema"] + [r for r in REPO_DIRS if r != "decision-schema"]
    for name in order:
        repo = workspace / name
        if not repo.is_dir() or not (repo / "pyproject.toml").exists():
            continue
        print(f"[install] {name}...")
        code = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", str(repo), "-q"],
            cwd=workspace,
        ).returncode
        if code != 0:
            print(f"[FAIL] pip install -e {name}", file=sys.stderr)
            return code
    print("[OK] install done")
    return 0


def cmd_test(workspace: Path) -> int:
    """Run pytest in each repo that has tests/."""
    for name in REPO_DIRS:
        repo = workspace / name
        tests_dir = repo / "tests"
        if not tests_dir.is_dir():
            continue
        print(f"[test] {name}...")
        code = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-q"],
            cwd=repo,
        ).returncode
        if code != 0:
            print(f"[FAIL] pytest in {name}", file=sys.stderr)
            return code
    print("[OK] test done")
    return 0


def cmd_check_release(workspace: Path, tools_dir: Path) -> int:
    """Run check_release_alignment.py."""
    script = tools_dir / "check_release_alignment.py"
    if not script.exists():
        print("[FAIL] check_release_alignment.py not found", file=sys.stderr)
        return 1
    return subprocess.run(
        [sys.executable, str(script), "--workspace", str(workspace)],
        cwd=tools_dir.parent,
    ).returncode


def cmd_check_sync(workspace: Path, tools_dir: Path) -> int:
    """Run check_workspace_sync.py."""
    script = tools_dir / "check_workspace_sync.py"
    if not script.exists():
        print("[FAIL] check_workspace_sync.py not found", file=sys.stderr)
        return 1
    return subprocess.run(
        [sys.executable, str(script), "--workspace", str(workspace)],
        cwd=tools_dir.parent,
    ).returncode


def main() -> int:
    tools_dir = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(
        description="Decision Ecosystem CLI: install, test, check-release, check-sync."
    )
    ap.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Parent dir containing repo dirs (default: parent of docs repo)",
    )
    ap.add_argument(
        "command",
        choices=["install", "test", "check-release", "check-sync"],
        help="Command to run",
    )
    args = ap.parse_args()
    workspace = get_workspace(args, tools_dir)
    if not workspace.is_dir():
        print(f"[FAIL] workspace not found: {workspace}", file=sys.stderr)
        return 1

    if args.command == "install":
        return cmd_install(workspace)
    if args.command == "test":
        return cmd_test(workspace)
    if args.command == "check-release":
        return cmd_check_release(workspace, tools_dir)
    if args.command == "check-sync":
        return cmd_check_sync(workspace, tools_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
