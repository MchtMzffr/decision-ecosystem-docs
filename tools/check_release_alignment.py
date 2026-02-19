#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Release alignment drift guard (INV-DOC-DRIFT-1).
Parses NEXT_STEPS_ROADMAP.md P0 table and optionally checks that local repos'
pyproject.toml [project].version matches the table. Exit 1 if any mismatch.
"""

import argparse
import re
import sys
from pathlib import Path


# Table repo name (first column) -> directory name under workspace
REPO_DIRS = {
    "decision-schema": "decision-schema",
    "mdm-engine": "mdm-engine",
    "ops-health-core": "ops-health-core",
    "evaluation-calibration-core": "evaluation-calibration-core",
    "execution-orchestration-core": "execution-orchestration-core",
    "decision-modulation-core (dmc-core)": "decision-modulation-core",
}


def parse_roadmap_table(roadmap_path: Path) -> list[tuple[str, str, str, str]]:
    """Return list of (repo_name, pyproject_version, latest_tag, action)."""
    text = roadmap_path.read_text(encoding="utf-8")
    rows = []
    in_table = False
    for line in text.splitlines():
        if "| decision-schema |" in line or "| decision-schema |" in line:
            in_table = True
        if not in_table:
            continue
        m = re.match(
            r"\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(.+)\s*\|", line
        )
        if not m:
            if line.strip().startswith("|") and "---" in line:
                continue
            break
        repo, pyver, tag, action = (s.strip() for s in m.groups())
        if repo and not repo.startswith("---"):
            rows.append((repo, pyver, tag, action))
    return rows


def get_pyproject_version(repo_dir: Path) -> str | None:
    """Read [project].version from pyproject.toml. Returns None if file missing."""
    pyproject = repo_dir / "pyproject.toml"
    if not pyproject.exists():
        return None
    try:
        content = pyproject.read_text(encoding="utf-8")
    except Exception:
        return None
    # Minimal TOML parse for [project] version = "x.y.z"
    in_project = False
    for line in content.splitlines():
        line = line.strip()
        if line == "[project]":
            in_project = True
            continue
        if in_project and line.startswith("version"):
            # version = "0.2.2" or version = '0.2.2'
            m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                return m.group(1)
        if in_project and line.startswith("[") and "[project]" not in line:
            break
    return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check NEXT_STEPS_ROADMAP.md P0 table vs local pyproject versions (INV-DOC-DRIFT-1)."
    )
    ap.add_argument(
        "--roadmap",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "NEXT_STEPS_ROADMAP.md",
        help="Path to NEXT_STEPS_ROADMAP.md",
    )
    ap.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Parent dir containing repo dirs (e.g. parent of decision-ecosystem-docs). If omitted, only table parse is checked.",
    )
    args = ap.parse_args()

    if not args.roadmap.exists():
        print(f"Error: Roadmap not found: {args.roadmap}", file=sys.stderr)
        return 1

    rows = parse_roadmap_table(args.roadmap)
    if not rows:
        print("Error: No P0 table rows parsed.", file=sys.stderr)
        return 1

    mismatches = []
    for repo_name, expected_ver, tag, action in rows:
        dir_name = REPO_DIRS.get(repo_name)
        if not dir_name:
            continue
        if not args.workspace:
            continue
        repo_dir = args.workspace / dir_name
        actual = get_pyproject_version(repo_dir)
        if actual is None:
            mismatches.append(
                (
                    repo_name,
                    expected_ver,
                    "<no pyproject or version>",
                    "file missing or unreadable",
                )
            )
        elif actual != expected_ver:
            mismatches.append((repo_name, expected_ver, actual, "version mismatch"))

    if mismatches:
        print(
            "INV-DOC-DRIFT-1: Roadmap table vs local pyproject.version mismatch:",
            file=sys.stderr,
        )
        for repo, expected, actual, reason in mismatches:
            print(
                f"  {repo}: table={expected} actual={actual} ({reason})",
                file=sys.stderr,
            )
        return 1

    if args.workspace:
        print("OK: All repo pyproject versions match roadmap table.")
    else:
        print(
            "OK: Roadmap table parsed (run with --workspace <parent> to check repo versions)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
