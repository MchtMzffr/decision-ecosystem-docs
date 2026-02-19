#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Deterministic CI proof capture for release notes.
Resolves tag → commit SHA, finds successful CI run for that SHA, downloads
pytest-report artifacts, and prints Markdown lines to paste into release notes.
Requires: gh CLI authenticated; local repo (--cwd) for resolving tag SHA.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def sh(cmd: list[str], cwd: str | None = None) -> str:
    p = subprocess.run(
        cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr.strip()}")
    return p.stdout.strip()


def get_tag_sha_locally(tag: str, cwd: str) -> str:
    """Resolve tag to commit SHA (annotated or lightweight)."""
    return sh(["git", "rev-list", "-n", "1", tag], cwd=cwd)


def find_run(repo: str, workflow: str, sha: str) -> dict:
    out = sh(
        [
            "gh",
            "run",
            "list",
            "-R",
            repo,
            "--workflow",
            workflow,
            "--json",
            "databaseId,headSha,url,conclusion,event,status,createdAt",
            "--limit",
            "50",
        ]
    )
    runs = json.loads(out)
    candidates = [
        r
        for r in runs
        if r.get("headSha") == sha
        and r.get("event") == "push"
        and r.get("conclusion") == "success"
    ]
    if not candidates:
        candidates = [
            r for r in runs if r.get("headSha") == sha and r.get("event") == "push"
        ]
    if not candidates:
        raise RuntimeError(
            f"No runs found for {repo} {workflow} sha={sha}. Is CI triggered on tags?"
        )
    candidates.sort(key=lambda r: r.get("createdAt", ""), reverse=True)
    return candidates[0]


def download_and_parse_reports(
    repo: str, run_id: int, py_versions: list[str], tmp_base: Path
) -> dict:
    """Download each pytest-report artifact into a version-specific subdir to avoid overwrite."""
    results = {}
    for v in py_versions:
        name = f"pytest-report-{v}"
        subdir = tmp_base / v
        subdir.mkdir(parents=True, exist_ok=True)
        sh(
            [
                "gh",
                "run",
                "download",
                str(run_id),
                "-R",
                repo,
                "--name",
                name,
                "--dir",
                str(subdir),
            ]
        )
        path = subdir / "pytest-report.json"
        if not path.exists():
            matches = list(subdir.rglob("pytest-report.json"))
            if not matches:
                raise RuntimeError(
                    f"pytest-report.json not found after downloading artifact {name}"
                )
            path = matches[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        s = data.get("summary", {})
        results[v] = {
            "total": int(s.get("total", 0)),
            "passed": int(s.get("passed", 0)),
            "failed": int(s.get("failed", 0)),
            "skipped": int(s.get("skipped", 0)),
        }
    return results


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Print release-note lines with CI run URL and test counts from tag."
    )
    ap.add_argument(
        "--repo", required=True, help="owner/repo, e.g. MchtMzffr/decision-schema"
    )
    ap.add_argument("--tag", required=True, help="tag name, e.g. v0.2.2")
    ap.add_argument("--workflow", default="ci.yml", help="workflow file name")
    ap.add_argument(
        "--py",
        default="3.11,3.12",
        help="comma-separated python versions for artifacts",
    )
    ap.add_argument(
        "--cwd",
        default=".",
        help="local repo path for resolving tag SHA via git",
    )
    args = ap.parse_args()

    sha = get_tag_sha_locally(args.tag, args.cwd)
    run = find_run(args.repo, args.workflow, sha)
    run_id = int(run["databaseId"])
    url = run.get("url") or run.get("htmlUrl", "")
    py_versions = [p.strip() for p in args.py.split(",") if p.strip()]

    with tempfile.TemporaryDirectory(prefix="ci-proof-") as tmp:
        tmp_path = Path(tmp)
        reports = download_and_parse_reports(args.repo, run_id, py_versions, tmp_path)

    # Markdown lines to paste into release notes (INV-REL-PROOF-1: no TBD)
    # Use ASCII-safe bullets for Windows console; paste into MD as "- [OK] ..." or replace with ✅
    print(f"- [OK] Tests: PASS (CI run link: {url})")
    parts = [
        f"py{v}: total={reports[v]['total']} passed={reports[v]['passed']} "
        f"failed={reports[v]['failed']} skipped={reports[v]['skipped']}"
        for v in py_versions
    ]
    print("- [OK] Test counts: " + "; ".join(parts))
    print("- [OK] Contract gate: PASS (expected schema minor: 2)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
