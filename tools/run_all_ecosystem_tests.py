#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Run all ecosystem tests (cores + harness + docs) and docs guards; report total passed.

Repos: decision-schema, mdm-engine, decision-modulation-core, ops-health-core,
evaluation-calibration-core, execution-orchestration-core, explainability-audit-core,
decision-ecosystem-integration-harness, decision-ecosystem-docs.

Usage (from workspace root or docs repo):
  # Once: install deps so cores can import decision_schema
  python decision-ecosystem-docs/tools/ecosystem.py --workspace <parent-dir> install
  # Then: run all tests
  python decision-ecosystem-docs/tools/run_all_ecosystem_tests.py --workspace <parent-dir>
  python tools/run_all_ecosystem_tests.py --workspace ..   # from decision-ecosystem-docs
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Same as ecosystem.py
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

DOCS_REPO_NAME = "decision-ecosystem-docs"


def get_workspace(workspace_arg: Path | None) -> Path:
    if workspace_arg and workspace_arg.is_dir():
        return workspace_arg.resolve()
    # Default: parent of this file's repo (decision-ecosystem-docs)
    tools_dir = Path(__file__).resolve().parent
    docs_repo = tools_dir.parent
    if docs_repo.name == DOCS_REPO_NAME:
        return docs_repo.parent
    return Path.cwd()


def run_pytest_in_repo(workspace: Path, repo_name: str) -> tuple[int, int, bool]:
    """Run pytest in repo. Returns (passed, failed, ok). For docs repo uses tools/tests/."""
    repo = workspace / repo_name
    if not repo.is_dir():
        return (0, 0, True)
    if repo_name == DOCS_REPO_NAME:
        test_path = "tools/tests"
        if not (repo / test_path).is_dir():
            return (0, 0, True)
    else:
        test_path = "tests"
        if not (repo / test_path).is_dir():
            return (0, 0, True)

    r = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-v", "--tb=no", "-q"],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=300,
    )
    out = (r.stdout or "") + (r.stderr or "")
    passed = out.count(" PASSED")
    failed = out.count(" FAILED")
    if passed == 0 and failed == 0 and " passed" in out:
        for part in out.replace("\n", " ").split():
            if part.isdigit():
                idx = out.find(part + " passed")
                if idx >= 0:
                    passed = int(part)
                    break
    if r.returncode != 0 and failed == 0 and passed == 0:
        failed = 1
    return (passed, failed, r.returncode == 0)


def run_docs_guard(docs_repo: Path, script_name: str, workspace: Path) -> bool:
    if script_name == "check_ci_compliance.py":
        r = subprocess.run(
            [
                sys.executable,
                "tools/check_ci_compliance.py",
                "--workspace",
                str(workspace),
            ],
            cwd=docs_repo,
            capture_output=True,
            text=True,
            timeout=60,
        )
    else:
        script = docs_repo / ".github" / "scripts" / script_name
        if not script.exists():
            return True
        r = subprocess.run(
            [sys.executable, str(script)],
            cwd=docs_repo,
            capture_output=True,
            text=True,
            timeout=60,
        )
    return r.returncode == 0


def main() -> int:
    ap = __import__("argparse").ArgumentParser(
        description="Run all ecosystem tests + docs guards."
    )
    ap.add_argument(
        "--workspace", type=Path, default=None, help="Parent dir containing repo dirs"
    )
    args = ap.parse_args()
    workspace = get_workspace(args.workspace)
    docs_repo = workspace / DOCS_REPO_NAME
    if not workspace.is_dir():
        print(f"[FAIL] workspace not found: {workspace}", file=sys.stderr)
        return 1

    total_passed = 0
    total_failed = 0
    results = []

    # 1. Pytest in each repo
    for repo_name in REPO_DIRS:
        passed, failed, ok = run_pytest_in_repo(workspace, repo_name)
        if passed == 0 and failed == 0:
            continue
        total_passed += passed
        total_failed += failed
        status = "OK" if ok else "FAIL"
        results.append((f"pytest {repo_name}", passed, failed, status))
        if not ok:
            print(f"[FAIL] pytest in {repo_name}: {failed} failed", file=sys.stderr)

    # 2. Docs guards (only if docs repo exists)
    if docs_repo.is_dir():
        guards = [
            (".github/scripts/check_docs_root.py", "check_docs_root (INV-DOC-ROOT-*)"),
            (
                ".github/scripts/check_docs_links.py",
                "check_docs_links (INV-DOC-LINK-1)",
            ),
            (
                ".github/scripts/check_docs_domain_lexemes.py",
                "check_docs_domain_lexemes (INV-DOC-DOMAIN-0)",
            ),
        ]
        for script_rel, label in guards:
            script_path = docs_repo / script_rel
            if script_path.exists():
                ok = run_docs_guard(docs_repo, Path(script_rel).name, workspace)
                total_passed += 1 if ok else 0
                total_failed += 0 if ok else 1
                results.append(
                    (label, 1 if ok else 0, 0 if ok else 1, "OK" if ok else "FAIL")
                )

        ok = run_docs_guard(docs_repo, "check_ci_compliance.py", workspace)
        total_passed += 1 if ok else 0
        total_failed += 0 if ok else 1
        results.append(
            (
                "check_ci_compliance (INV-CI-COMPLY-2)",
                1 if ok else 0,
                0 if ok else 1,
                "OK" if ok else "FAIL",
            )
        )

    # Report
    print("--- Results ---")
    for name, p, f, status in results:
        print(f"  {name}: {p} passed, {f} failed [{status}]")
    print("---")
    print(f"TOPLAM: {total_passed} gecti, {total_failed} kaldi")
    if total_failed > 0:
        print(
            "Not: Core/harness pytest icin once: python decision-ecosystem-docs/tools/ecosystem.py --workspace <dir> install",
            file=sys.stderr,
        )
        return 1
    print("Tum testler ve guard'lar gecti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
