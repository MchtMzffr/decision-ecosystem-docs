#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""
Run all tests and invariant guards; report total passed.
  - pytest: tools/tests/
  - Docs guards: check_docs_root, check_docs_links, check_docs_domain_lexemes
  - CI compliance: check_ci_compliance.py --workspace .
Run from repo root: python .github/scripts/run_all_tests_and_guards.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_pytest() -> tuple[int, int]:
    """Run pytest tools/tests/; return (passed, failed)."""
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tools/tests/", "-v", "--tb=no", "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = (r.stdout or "") + (r.stderr or "")
    passed = out.count(" PASSED")
    failed = out.count(" FAILED")
    # Parse "X passed" summary line
    if " passed" in out and passed == 0 and failed == 0:
        for part in out.replace("\n", " ").split():
            if part.isdigit():
                idx = out.find(part + " passed")
                if idx >= 0:
                    passed = int(part)
                    break
    if r.returncode != 0 and failed == 0 and passed == 0:
        failed = 1
    return (passed, failed)


def run_script(script_path: str) -> bool:
    """Run a Python script; return True if exit 0."""
    r = subprocess.run(
        [sys.executable, script_path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return r.returncode == 0


def main() -> int:
    total_passed = 0
    total_failed = 0
    results = []

    # 1. Pytest
    passed, failed = run_pytest()
    total_passed += passed
    total_failed += failed
    results.append(("pytest tools/tests/", passed, failed))
    if failed > 0:
        subprocess.run(
            [sys.executable, "-m", "pytest", "tools/tests/", "-v", "--tb=short"],
            cwd=REPO_ROOT,
        )

    # 2. Docs root
    ok = run_script(".github/scripts/check_docs_root.py")
    total_passed += 1 if ok else 0
    total_failed += 0 if ok else 1
    results.append(
        ("check_docs_root.py (INV-DOC-ROOT-*)", 1 if ok else 0, 0 if ok else 1)
    )

    # 3. Links
    ok = run_script(".github/scripts/check_docs_links.py")
    total_passed += 1 if ok else 0
    total_failed += 0 if ok else 1
    results.append(
        ("check_docs_links.py (INV-DOC-LINK-1)", 1 if ok else 0, 0 if ok else 1)
    )

    # 4. Domain lexemes
    ok = run_script(".github/scripts/check_docs_domain_lexemes.py")
    total_passed += 1 if ok else 0
    total_failed += 0 if ok else 1
    results.append(
        (
            "check_docs_domain_lexemes.py (INV-DOC-DOMAIN-0)",
            1 if ok else 0,
            0 if ok else 1,
        )
    )

    # 5. CI compliance
    r = subprocess.run(
        [sys.executable, "tools/check_ci_compliance.py", "--workspace", "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    ok = r.returncode == 0
    total_passed += 1 if ok else 0
    total_failed += 0 if ok else 1
    results.append(
        ("check_ci_compliance.py (INV-CI-COMPLY-2)", 1 if ok else 0, 0 if ok else 1)
    )

    # Report
    print("--- Results ---")
    for name, p, f in results:
        print(f"  {name}: {p} passed, {f} failed")
    print("---")
    print(f"TOPLAM: {total_passed} geçti, {total_failed} kaldı")
    if total_failed > 0:
        return 1
    print("Tüm testler ve guard'lar geçti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
