# P0/P1 Öneriler — Uygulanan Düzenlemeler

**Purpose:** Summary of applied patches from the P0/P1 analysis and Cursor prompt package.  
**References:** P0_P1_ANALYSIS_VERDICT.md, ROOT_ALLOWLIST.txt, check_docs_root.py, BRANCH_GOVERNANCE.md, ECOSYSTEM_GATES_AND_INVARIANTS.md.

---

## 1. P0 — ROOT_ALLOWLIST formatı

- **INV-DOC-ROOT-ALLOWLIST-FMT-1** eklendi: Her non-comment satır tek path (boşluksuz).
- **ROOT_ALLOWLIST.txt:** Açıklama satırı eklendi; release artefact satırları kaldırıldı (dosyalar archive’a taşındı).
- **.github/scripts/check_docs_root.py:** `check_allowlist_format()` eklendi; satır içi whitespace varsa script fail ediyor. `main()` içinde bu kontrol ilk sırada çalışıyor.
- **docs/ECOSYSTEM_GATES_AND_INVARIANTS.md:** §5 (Docs repo structure) tablosuna INV-DOC-ROOT-ALLOWLIST-FMT-1 satırı eklendi.

---

## 2. P1 — Root’ta release body artefact’leri

- **release_dmc_v0.1.0_body.md**, **release_dmc_v0.1.1_body.md**, **release_dmc_v0.1.1_verification.txt** root’tan silindi.
- Aynı dosyalar **archive/2026-02-19/** altına kopyalandı (release kanıtı olarak saklandı).
- **ROOT_ALLOWLIST.txt** içinden bu üç satır çıkarıldı.

---

## 3. P1 — BRANCH_GOVERNANCE.md CI vs @main

- **Rationale** (satır 23): "All workflows and git fallbacks use @main" → "CI uses tag-pinned fallbacks (`@vX.Y.Z`); dev/experiments may use `@main` (non-deterministic)".
- **Migration Notes** adım 4: "Update git fallback URLs to @main" → "Keep CI fallbacks tag-pinned (`@vX.Y.Z`); do not use @main in CI. For local dev only, @main is allowed."

---

## 4. Cursor Rule (INV-TRACE-REG-1)

- **.cursor/rules/decision-ecosystem-global.mdc** oluşturuldu: Global kural (alwaysApply: true), INV-T1 yerine **INV-TRACE-REG-1** kullanıyor; trace registry, fail-closed, SemVer, CI tag pin, docs governance (INV-DOC-ROOT-ALLOWLIST-FMT-1 dahil).
- **.github/scripts/check_docs_root.py:** Root’ta `.cursor` dizinine izin vermek için ALLOWED_DIRS’e `.cursor` eklendi.

---

## 5. Doğrulama

- `python .github/scripts/check_docs_root.py` → **OK: All docs structure invariants passed.**

---

**Last updated:** 2026-02  
**Status:** Tüm öneriler uygulandı; CI/docs root check geçiyor.
