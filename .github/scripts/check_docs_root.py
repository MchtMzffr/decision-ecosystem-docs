# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
Docs repo root structure guard — INV-DOC-ROOT-*, INV-DOC-ARCHIVE-*, INV-DOC-README-*, INV-DOC-ANALYSIS-LIMIT-1.
Run from repo root: python .github/scripts/check_docs_root.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_FILE = REPO_ROOT / "ROOT_ALLOWLIST.txt"
README_FILE = REPO_ROOT / "README.md"

# Directories allowed at root (archive/ may only contain YYYY-MM-DD subdirs)
ALLOWED_DIRS = {
    ".github",
    "archive",
    "docs",
    "examples",
    ".git",
    "reports",
    "tools",
    ".ruff_cache",
    ".pytest_cache",
}

# INV-DOC-ANALYSIS-LIMIT-1: Max number of analysis/report files at root
MAX_ANALYSIS_REPORTS = 2

# Only YYYY-MM-DD subdirs allowed under archive/
ARCHIVE_SUBDIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_allowlist() -> set[str]:
    allowed = set()
    if not ALLOWLIST_FILE.exists():
        return allowed
    with open(ALLOWLIST_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                allowed.add(line)
    return allowed


def check_inv_doc_root_allow_1(allowlist: set[str]) -> tuple[bool, list[str]]:
    """INV-DOC-ROOT-ALLOW-1: Only allowlist files and allowed dirs at root."""
    errors = []
    for name in os.listdir(REPO_ROOT):
        if name == ".git" and os.path.isdir(REPO_ROOT / name):
            continue
        path = REPO_ROOT / name
        if path.is_dir():
            if name not in ALLOWED_DIRS:
                errors.append(
                    f"INV-DOC-ROOT-ALLOW-1: disallowed directory at root: {name}"
                )
        else:
            if name not in allowlist:
                errors.append(f"INV-DOC-ROOT-ALLOW-1: disallowed file at root: {name}")
    return len(errors) == 0, errors


def check_inv_doc_archive_snapshot_1() -> tuple[bool, list[str]]:
    """INV-DOC-ARCHIVE-SNAPSHOT-1: Only YYYY-MM-DD/ subdirs under archive/."""
    errors = []
    archive_dir = REPO_ROOT / "archive"
    if not archive_dir.is_dir():
        return True, []
    for name in os.listdir(archive_dir):
        if not ARCHIVE_SUBDIR_RE.match(name):
            errors.append(
                f"INV-DOC-ARCHIVE-SNAPSHOT-1: disallowed path under archive/: archive/{name}"
            )
    return len(errors) == 0, errors


def check_inv_doc_readme_current_1(allowlist: set[str]) -> tuple[bool, list[str]]:
    """INV-DOC-README-CURRENT-1: README Current section only links to root allowlist files."""
    errors = []
    if not README_FILE.exists():
        return True, []
    with open(README_FILE, encoding="utf-8") as f:
        content = f.read()
    # Collect ](link) refs in the Current documentation section
    in_current = False
    for line in content.splitlines():
        if "## Current documentation" in line or "## Current Documentation" in line:
            in_current = True
            continue
        if in_current and line.strip().startswith("## "):
            break
        if in_current:
            # ](FILENAME.md) veya ](FILENAME)
            for m in re.finditer(r"\]\(([^)]+)\)", line):
                link = m.group(1).strip()
                if (
                    link.startswith("http")
                    or link.startswith("#")
                    or link.startswith("archive/")
                ):
                    continue
                base = link.split("/")[0].split("#")[0]
                if base and base not in allowlist and base not in ALLOWED_DIRS:
                    errors.append(
                        f"INV-DOC-README-CURRENT-1: link in Current section not in allowlist: {base}"
                    )
    return len(errors) == 0, errors


def check_inv_doc_analysis_limit_1(allowlist: set[str]) -> tuple[bool, list[str]]:
    """INV-DOC-ANALYSIS-LIMIT-1: Count of *_REPORT.md or *_ANALYSIS*.md at root <= 2."""
    errors = []
    count = 0
    for name in allowlist:
        if "_REPORT.md" in name or "_ANALYSIS" in name:
            if (REPO_ROOT / name).exists():
                count += 1
    if count > MAX_ANALYSIS_REPORTS:
        errors.append(
            f"INV-DOC-ANALYSIS-LIMIT-1: analysis/report file count at root {count} > {MAX_ANALYSIS_REPORTS}"
        )
    return len(errors) == 0, errors


def main() -> int:
    os.chdir(REPO_ROOT)
    allowlist = load_allowlist()
    all_errors = []

    ok1, err1 = check_inv_doc_root_allow_1(allowlist)
    if not ok1:
        all_errors.extend(err1)

    ok2, err2 = check_inv_doc_archive_snapshot_1()
    if not ok2:
        all_errors.extend(err2)

    ok3, err3 = check_inv_doc_readme_current_1(allowlist)
    if not ok3:
        all_errors.extend(err3)

    ok4, err4 = check_inv_doc_analysis_limit_1(allowlist)
    if not ok4:
        all_errors.extend(err4)

    if all_errors:
        for e in all_errors:
            print(e)
        return 1
    print("OK: All docs structure invariants passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
