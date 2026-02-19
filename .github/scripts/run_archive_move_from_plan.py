# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
Option B: Run git mv from archive_move_plan_YYYY-MM-DD.txt.
Run from repo root: python .github/scripts/run_archive_move_from_plan.py archive_move_plan_2026-02-19.txt
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: python run_archive_move_from_plan.py <archive_move_plan_2026-02-19.txt>",
            file=sys.stderr,
        )
        return 1
    plan_file = REPO_ROOT / sys.argv[1]
    if not plan_file.exists():
        print(f"Plan file not found: {plan_file}", file=sys.stderr)
        return 1
    os.chdir(REPO_ROOT)
    with open(plan_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if " -> " not in line:
                continue
            src, _, dst = line.partition(" -> ")
            src, dst = src.strip(), dst.strip()
            if not src or not dst:
                continue
            src_path = REPO_ROOT / src
            dst_path = REPO_ROOT / dst
            if not src_path.exists():
                print(f"Skip (missing): {src}")
                continue
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "mv", src, dst], check=True, cwd=REPO_ROOT)
            print(f"mv {src} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
