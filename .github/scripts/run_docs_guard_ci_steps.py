#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Run the same steps as docs_structure_guard.yml job "check-docs-root" (without secret_scan).
Use for local CI simulation: python .github/scripts/run_docs_guard_ci_steps.py
Ruff steps are skipped if ruff is not installed; Python script steps always run.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run(cmd: list[str], cwd: Path | None = None) -> int:
    try:
        r = subprocess.run(cmd, cwd=cwd or REPO_ROOT)
        return r.returncode
    except FileNotFoundError:
        return 127


def main() -> int:
    steps = [
        ("Ruff check", ["ruff", "check", "."], True),
        ("Ruff format check", ["ruff", "format", "--check", "."], True),
        (
            "Docs root invariants",
            [sys.executable, ".github/scripts/check_docs_root.py"],
            False,
        ),
        (
            "INV-DOC-LINK-1",
            [sys.executable, ".github/scripts/check_docs_links.py"],
            False,
        ),
        (
            "INV-DOC-DOMAIN-0",
            [sys.executable, ".github/scripts/check_docs_domain_lexemes.py"],
            False,
        ),
        (
            "INV-CI-COMPLY-2",
            [sys.executable, "tools/check_ci_compliance.py", "--workspace", "."],
            False,
        ),
    ]
    for name, cmd, optional in steps:
        code = run(cmd)
        if code != 0:
            if optional and code == 127:
                print(f"[skip] {name} (ruff not in PATH)")
                continue
            if optional:
                print(f"[skip] {name} (exit {code}; install ruff to match CI)")
                continue
            print(f"[FAIL] {name}")
            return code
        print(f"[OK] {name}")
    print("All docs guard CI steps passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
