#!/usr/bin/env python3
# Decision Ecosystem — decision-ecosystem-docs
# SPDX-License-Identifier: MIT
"""
INV-AUDIT-NEG-1: Negative test for public_main_audit. Invalid owner or missing path must yield exit != 0.
Run: pytest tools/tests/test_public_main_audit_negative.py -v
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_audit_fails_for_invalid_owner() -> None:
    """With --owner DefinitelyNotAnOwner, audit must exit with non-zero (FAIL)."""
    script = Path(__file__).resolve().parent.parent / "public_main_audit.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--owner", "DefinitelyNotAnOwner"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode != 0, (
        f"Expected FAIL for invalid owner; got exit 0. stderr: {proc.stderr}"
    )
    assert "FAIL" in proc.stderr or "not 200" in proc.stderr or "404" in proc.stderr
