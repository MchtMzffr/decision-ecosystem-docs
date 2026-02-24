# Decision Ecosystem — decision-ecosystem-docs
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
#!/usr/bin/env python3
"""
INV-DOC-DOMAIN-0: ACTIVE docs (docs/ excluding archive/ and examples/) must not contain domain lexemes.
Config: docs/DOMAIN_LEXEMES.txt (one lexeme per line; # comment).
Run from repo root: python .github/scripts/check_docs_domain_lexemes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
LEXEMES_FILE = DOCS_DIR / "DOMAIN_LEXEMES.txt"


def load_lexemes() -> list[str]:
    if not LEXEMES_FILE.exists():
        return []
    lexemes = []
    for line in LEXEMES_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            lexemes.append(s)
    return lexemes


def iter_active_md(root: Path) -> list[Path]:
    """ACTIVE = docs/ but not archive/ or examples/."""
    out = []
    if not root.is_dir():
        return out
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if "archive" in rel.parts or "examples" in rel.parts:
            continue
        out.append(path)
    return out


def check_domain_lexemes() -> list[tuple[Path, int, str]]:
    """Return (file, line_no, lexeme) for each occurrence."""
    lexemes = load_lexemes()
    if not lexemes:
        return []
    # Case-insensitive; match whole word or as substring (fail on any occurrence)
    found = []
    docs_root = REPO_ROOT / "docs"
    for md_path in iter_active_md(docs_root):
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            lower = line.lower()
            for lex in lexemes:
                if lex.lower() in lower:
                    found.append((md_path, line_no, lex))
    return found


def main() -> int:
    if not LEXEMES_FILE.exists():
        print("OK: INV-DOC-DOMAIN-0 skipped (no docs/DOMAIN_LEXEMES.txt).")
        return 0
    found = check_domain_lexemes()
    if found:
        for path, line_no, lex in found:
            rel = path.relative_to(REPO_ROOT)
            print(f"INV-DOC-DOMAIN-0: domain lexeme '{lex}' in {rel}:{line_no}")
        return 1
    print("OK: INV-DOC-DOMAIN-0 passed (no domain lexemes in ACTIVE docs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
