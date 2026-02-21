#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
INV-CI-COMPLY-2: CI compliance checker. Fail-closed.
Checks each repo's workflow(s) against required steps per repo type (CI_COMPLIANCE_STANDARD).
Repo list and types: optional SSOT from docs/REPO_REGISTRY.md (INV-REPO-REG-1).
Usage:
  python tools/check_ci_compliance.py --workspace <parent-of-all-repos>   # check all repos
  python tools/check_ci_compliance.py --workspace .                        # check only current dir (single repo)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Fallback when registry not found
REPO_DIRS_FALLBACK = [
    "decision-schema",
    "mdm-engine",
    "decision-modulation-core",
    "ops-health-core",
    "evaluation-calibration-core",
    "execution-orchestration-core",
    "decision-ecosystem-integration-harness",
    "decision-ecosystem-docs",
]


def load_registry(workspace: Path) -> tuple[list[str], dict[str, str]] | None:
    """Load REPO_REGISTRY.md from docs repo. Returns (repo_names, name -> type) or None."""
    for docs_path in [
        workspace / "decision-ecosystem-docs" / "docs" / "REPO_REGISTRY.md",
        workspace / "docs" / "REPO_REGISTRY.md",
        Path(__file__).resolve().parent.parent / "docs" / "REPO_REGISTRY.md",
    ]:
        if docs_path.exists():
            break
    else:
        return None
    text = docs_path.read_text(encoding="utf-8", errors="replace")
    rows: list[tuple[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if "| repo_name |" in line or "| repo_name |" in line:
            in_table = True
            continue
        if not in_table or not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2 and parts[0] != "---" and not parts[0].startswith("repo_name"):
            name, typ = parts[0], parts[1]
            if name and typ:
                rows.append((name, typ))
    if not rows:
        return None
    repo_list = [r[0] for r in rows]
    type_map = {r[0]: r[1] for r in rows}
    return (repo_list, type_map)


def repo_type(name: str, type_map: dict[str, str] | None = None) -> str:
    if type_map and name in type_map:
        t = type_map[name]
        if t == "docs":
            return "docs"
        if t == "harness":
            return "harness"
        if t == "core":
            return "core_schema" if name == "decision-schema" else "core"
        if t == "experimental":
            return "core"  # checklist as core
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


def _check_action_pins(content: str) -> list[str]:
    """INV-CI-ACT-PIN-1: every uses: must have @tag or @sha; @main/@master/@HEAD forbidden."""
    missing = []
    for line in content.splitlines():
        if "uses:" not in line or line.strip().startswith("#"):
            continue
        ref = line.split("uses:")[-1].split("#")[0].strip()
        if "@" not in ref:
            missing.append("INV-CI-ACT-PIN-1: action without pin (uses: ...@vX or @sha)")
            break
        if "@main" in ref or "@master" in ref or "@HEAD" in ref:
            missing.append("INV-CI-ACT-PIN-1: action must not use @main/@master/@HEAD (use @vX or sha)")
            break
    return missing


def _check_permissions(content: str) -> list[str]:
    """INV-CI-PERM-1: workflow should set permissions (e.g. contents: read)."""
    if "permissions:" not in content:
        return ["INV-CI-PERM-1: no permissions block (prefer contents: read)"]
    if "contents: read" not in content and "contents: write" not in content:
        return ["INV-CI-PERM-1: permissions block should include contents: read"]
    return []


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
    has_smoke = (
        "INV-CI-BUILD-SMOKE-1" in content
        or "wheel smoke" in content.lower()
        or ("SMOKE_IMPORT" in content and "import_module" in content)
    )
    if not has_smoke:
        missing.append("INV-CI-BUILD-SMOKE-1 / SMOKE_IMPORT (wheel smoke after build)")
    if "pytest" not in content:
        missing.append("pytest")
    if "pytest-report" not in content and "pytest_report" not in content:
        missing.append("pytest report artifact (INV-CI-PROOF-STD-1)")
    if "json-report-file=" not in content:
        missing.append("INV-CI-PROOF-STD-1: pytest --json-report-file= (e.g. pytest-report.json or artifacts/pytest-report.json)")
    if typ == "core_schema":
        if "check_parameter_index" not in content:
            missing.append("INV-PARAM-INDEX-1 (check_parameter_index.py)")
    if typ in ("core", "core_schema"):
        if "decision-schema" in content and "@main" in content and "v0.2.2" not in content:
            missing.append("INV-CI-SCHEMA-FB-1: schema fallback must be tag (e.g. @v0.2.2), not @main")
    missing.extend(_check_action_pins(content))
    missing.extend(_check_permissions(content))
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


def check_repo(workspace: Path, repo_name: str, type_map: dict[str, str] | None = None) -> list[str]:
    repo_path = workspace / repo_name
    if not repo_path.is_dir():
        if workspace.name == repo_name and (workspace / ".github").is_dir():
            repo_path = workspace  # single-repo mode: workspace is repo root
        else:
            return [f"Repo dir not found: {repo_name}"]
    typ = repo_type(repo_name, type_map)
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

    registry = load_registry(workspace)
    if registry:
        repo_list, type_map = registry
        # CI scope: core, harness, docs (optional: include experimental)
        repo_list_in_scope = [r for r in repo_list if type_map.get(r, "") in ("core", "harness", "docs")]
    else:
        repo_list_in_scope = REPO_DIRS_FALLBACK
        type_map = None

    if args.repos:
        repo_names = [r for r in args.repos if r in repo_list_in_scope or not registry]
        if not repo_names and args.repos:
            repo_names = args.repos  # allow ad-hoc names
    else:
        repo_names = [d for d in repo_list_in_scope if (workspace / d).is_dir()]
        if not repo_names:
            name = workspace.name
            if name in repo_list_in_scope or name in (REPO_DIRS_FALLBACK if not registry else []):
                repo_names = [name]
            else:
                print("check_ci_compliance: no known repo dirs under workspace; specify --repos?", file=sys.stderr)
                return 1

    errors: list[tuple[str, list[str]]] = []
    for repo_name in repo_names:
        miss = check_repo(workspace, repo_name, type_map)
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
