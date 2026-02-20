#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-CI-COMPLY-2: CI compliance checker. Fail-closed.
Checks each repo's workflow(s) against required steps per repo type (CI_COMPLIANCE_STANDARD).
Usage:
  python tools/check_ci_compliance.py --workspace <parent-of-all-repos>   # check all repos
  python tools/check_ci_compliance.py --workspace .                      # check only current dir (single repo)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

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


def repo_type(name: str) -> str:
    if name == "decision-ecosystem-docs":
        return "docs"
    if name == "decision-schema":
        return "core_schema"
    if name == "decision-ecosystem-integration-harness":
        return "harness"
    return "core"


def workflow_content(repo_path: Path, workflow_name: str) -> str:
    p = repo_path / ".github" / "workflows" / workflow_name
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def all_workflows_content(repo_path: Path) -> str:
    wdir = repo_path / ".github" / "workflows"
    if not wdir.exists():
        return ""
    parts = []
    for f in sorted(wdir.glob("*.yml")) + list(wdir.glob("*.yaml")):
        parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def check_core_or_harness(repo_path: Path, typ: str) -> list[str]:
    content = workflow_content(repo_path, "ci.yml")
    missing = []
    if not content:
        return [f"Missing .github/workflows/ci.yml"]
    if "gitleaks" not in content.lower():
        missing.append("gitleaks (secret_scan)")
    if "LICENSE" not in content and "test -f LICENSE" not in content:
        missing.append("LICENSE check")
    if "ruff check" not in content:
        missing.append("ruff check")
    if "ruff format" not in content:
        missing.append("ruff format check")
    if "python -m build" not in content:
        missing.append("INV-BUILD-1 (python -m build)")
    if "pytest" not in content:
        missing.append("pytest")
    if "pytest-report" not in content and "pytest_report" not in content:
        missing.append("pytest report artifact (INV-CI-PROOF-STD-1)")
    if typ == "core_schema":
        if "check_parameter_index" not in content:
            missing.append("INV-PARAM-INDEX-1 (check_parameter_index.py)")
    if typ in ("core", "core_schema"):
        if "decision-schema" in content and "@main" in content and "v0.2.2" not in content:
            missing.append("INV-CI-SCHEMA-FB-1: schema fallback must be tag (e.g. @v0.2.2), not @main")
    return missing


def check_docs(repo_path: Path) -> list[str]:
    content = workflow_content(repo_path, "docs_structure_guard.yml")
    all_content = all_workflows_content(repo_path)
    missing = []
    if not content:
        return [f"Missing .github/workflows/docs_structure_guard.yml"]
    if "gitleaks" not in all_content.lower():
        missing.append("gitleaks (secret_scan)")
    if "check_docs_root" not in content:
        missing.append("docs structure guard (check_docs_root.py)")
    has_py = (repo_path / "pyproject.toml").exists() or any(
        (repo_path / "tools").glob("*.py") if (repo_path / "tools").is_dir() else []
    )
    if has_py:
        if "ruff check" not in content:
            missing.append("ruff check (INV-CI-SCOPE-1: required when pyproject or tools/*.py exist)")
        if "ruff format" not in content:
            missing.append("ruff format check (INV-CI-SCOPE-1)")
    return missing


def check_repo(workspace: Path, repo_name: str) -> list[str]:
    repo_path = workspace / repo_name
    if not repo_path.is_dir():
        if workspace.name == repo_name and (workspace / ".github").is_dir():
            repo_path = workspace  # single-repo mode: workspace is repo root
        else:
            return [f"Repo dir not found: {repo_name}"]
    typ = repo_type(repo_name)
    if typ in ("core", "core_schema", "harness"):
        return check_core_or_harness(repo_path, typ)
    return check_docs(repo_path)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="INV-CI-COMPLY-2: Check CI workflows against CI Compliance Standard."
    )
    ap.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Parent dir containing repo dirs (default: current dir = single repo)",
    )
    ap.add_argument(
        "--repos",
        nargs="*",
        default=None,
        help="Limit to these repo dir names (default: all known repos under workspace)",
    )
    args = ap.parse_args()
    workspace = args.workspace.resolve()

    if args.repos:
        repo_names = [r for r in args.repos if r in REPO_DIRS]
        if not repo_names and args.repos:
            repo_names = args.repos  # allow ad-hoc names
    else:
        repo_names = [d for d in REPO_DIRS if (workspace / d).is_dir()]
        if not repo_names:
            name = workspace.name
            if name in REPO_DIRS:
                repo_names = [name]
            else:
                print("check_ci_compliance: no known repo dirs under workspace; specify --repos?", file=sys.stderr)
                return 1

    errors: list[tuple[str, list[str]]] = []
    for repo_name in repo_names:
        miss = check_repo(workspace, repo_name)
        if miss:
            errors.append((repo_name, miss))

    if errors:
        for repo_name, miss in errors:
            print(f"{repo_name}: missing or invalid: {', '.join(miss)}", file=sys.stderr)
        print("INV-CI-COMPLY-2: FAIL (CI compliance check)", file=sys.stderr)
        return 1
    print("INV-CI-COMPLY-2: OK (all checked repos comply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
