# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
INV-DOC-LINK-1: Relative links in .md files must resolve (no broken links).
Run from repo root: python .github/scripts/check_docs_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Match ](path) or ](path#anchor) — capture path only
LINK_RE = re.compile(r"\]\s*\(\s*([^)#\s]+)(?:#[\w-]*)?\s*\)")


def iter_md_files(root: Path):
    """Yield .md files under root, excluding .git and common noise."""
    for path in root.rglob("*.md"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        yield path


def is_external(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:") or url.startswith("#")


def strip_code_for_link_scan(line: str) -> str:
    """Remove inline code `...` so ](path) in examples is not treated as a link."""
    return re.sub(r"`[^`]*`", " ", line)


def check_links() -> list[tuple[Path, int, str, Path]]:
    """Return list of (md_file, line_no, link_text, resolved_path) for broken links."""
    broken = []
    for md_path in iter_md_files(REPO_ROOT):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        base_dir = md_path.parent
        for line_no, line in enumerate(text.splitlines(), 1):
            scan_line = strip_code_for_link_scan(line)
            for m in LINK_RE.finditer(scan_line):
                url = m.group(1).strip()
                if is_external(url):
                    continue
                # Relative path: resolve from current file's directory
                target = (base_dir / url).resolve()
                if not target.exists():
                    broken.append((md_path, line_no, url, target))
    return broken


def main() -> int:
    broken = check_links()
    if broken:
        for md_path, line_no, url, resolved in broken:
            rel = md_path.relative_to(REPO_ROOT)
            print(f"INV-DOC-LINK-1: broken link in {rel}:{line_no} -> {url} (resolved: {resolved})")
        return 1
    print("OK: INV-DOC-LINK-1 passed (no broken relative links).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
