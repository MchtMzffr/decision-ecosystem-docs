# P0/P1 Analysis & Cursor Prompt Package — Verdict

**Purpose:** Evaluate the user-submitted (A) P0/P1 docs-repo analysis and (B) Cursor Rules + Subagents + Commands package for correctness and alignment with the current codebase.

**Scope:** decision-ecosystem-docs (workspace state); ECOSYSTEM_GATES_AND_INVARIANTS.md, check_docs_root.py, ROOT_ALLOWLIST.txt, ECOSYSTEM_INVARIANTS.md, BRANCH_GOVERNANCE.md.

---

## A) P0/P1 Öneri Değerlendirmesi

### A.1 P0 — ROOT_ALLOWLIST formatı

**Öneri:** "ROOT_ALLOWLIST.txt tek satırda çoklu isim içeriyor"; script satır bazında okuyor, whitespace split yok → tüm satır tek item → root dosyaları disallowed sayılabilir.

**Workspace durumu:** `ROOT_ALLOWLIST.txt` şu an **zaten satır bazlı** (her satırda tek dosya adı). `check_docs_root.py` şöyle okuyor:

```python
for line in f:
    line = line.strip()
    if line and not line.startswith("#"):
        allowed.add(line)
```

Yani şu anki dosyada format bozuk değil; script de satır bazlı. **Ancak:**

- Eğer bir satıra yanlışlıkla `"FILE1.md FILE2.md"` yazılırsa, script bunu tek bir allowlist elemanı yapar ve `os.listdir()` ile eşleşmez → o dosyalar "disallowed" sayılır. Önerilen **INV-DOC-ROOT-ALLOWLIST-FMT-1** (her satır tek path, boşluksuz) ve script’te satır içi whitespace varsa **error** vermek mantıklı ve **doğru** bir sertleştirme.
- Sonuç: **Öneri doğru** (risk gerçek; mevcut dosya şans eseri doğru). Format invariant’ı + script’te whitespace kontrolü eklenmeli.

---

### A.2 P0 — Doc path drift (yanlış link hedefleri)

**Öneri:** ECOSYSTEM_INVARIANTS.md içinde REPO_REGISTRY.md, CI_COMPLIANCE_STANDARD.md gibi referanslar root path ile geçiyor; içerikler docs/ altında → 404 riski.

**Workspace durumu:** `ECOSYSTEM_INVARIANTS.md` içinde referanslar **zaten `docs/` prefix’li**: `docs/REPO_REGISTRY.md`, `docs/CI_COMPLIANCE_STANDARD.md`, `docs/CORE_REPO_STANDARDS.md`, `docs/ECOSYSTEM_GATES_AND_INVARIANTS.md`. README’deki linkler de `docs/...` kullanıyor. Yani **mevcut repoda bu P0 maddesi zaten sağlanmış**.

- Öneri genel kural olarak **doğru** (relative link’lerin çözülür olması, INV-DOC-LINK-1).
- "ECOSYSTEM_INVARIANTS.md’de root path" iddiası **bu workspace için yanlış**; başka commit/ fork’ta varsa düzeltmek doğru.

---

### A.3 P1 — Root’ta release body artefact’leri

**Öneri:** `release_dmc_v0.1.0_body.md`, `release_dmc_v0.1.1_body.md`, `release_dmc_v0.1.1_verification.txt` policy/doc değil; template ise docs/templates/, kanıt ise archive/YYYY-MM-DD/; ROOT_ALLOWLIST’ten çıkar.

**Workspace durumu:** Bu üç dosya şu an ROOT_ALLOWLIST.txt’te ve root’ta. Bunlar release **kanıt/body** artefact’i; kalıcı policy değil. INV-DOC-ROOT-ALLOWLIST-1 ile uyum için root’u sadece entrypoint + governance + checklist tutmak doğru.

- Öneri **doğru**. Patch: release_dmc_* → `archive/2026-02-XX/` (veya template ise `docs/templates/`), ROOT_ALLOWLIST’ten çıkar.

---

### A.4 P1 — BRANCH_GOVERNANCE.md “@main vs tag” dili

**Öneri:** "CI/CD Alignment: All workflows and git fallbacks use @main" eski/yanlış; aynı dokümanda CI için tag pin savunuluyor → çelişki.

**Workspace durumu:** `BRANCH_GOVERNANCE.md` satır 23: *"3. **CI/CD Alignment**: All workflows and git fallbacks use `@main`"* — bu **CI bağlamında yanlış**: proje politikası CI’da tag (`@vX.Y.Z`), dev’de opsiyonel `@main`. Aynı dosyada satır 46–51 ve 73–74’te CI ⇒ tag açık. Sonuç: satır 23 okuyucuda “CI da @main kullanıyor” izlenimi veriyor.

- Öneri **doğru**. Patch: "CI/CD Alignment" maddesini “CI: tag-pinned fallbacks; dev/experiments: @main allowed (non-deterministic)” şeklinde netleştir; Migration Notes’taki “Update git fallback URLs to @main”ı **CI bağlamından çıkar** veya “dev only” olarak işaretle.

---

## B) Cursor Prompt Paketi Değerlendirmesi

### B.1 Cursor Rule (global)

- decision-schema SSOT, INV-CORE-DEP-1, trace registry, domain-agnostic, fail-closed, kill-switch, boundedness, SemVer, CI tag pin, tag immutability, docs root allowlist, SCREAMING_SNAKE_CASE, INV-DOC-LINK-1 — **proje ile uyumlu ve doğru**.
- "INV-T1 registry level" ifadesi: projede trace için **INV-TRACE-REG-1** kullanılıyor; kuralda INV-T1 yerine INV-TRACE-REG-1 yazmak terminoloji tutarlılığı için daha iyi.

### B.2 Subagent prompt’ları (4 adet)

- **Formal Methods Reviewer:** INV-*, SSOT, trace registry, boundedness, fail-closed — doğru. Mevcut `~/.cursor/agents/formal-methods-reviewer.md` ile örtüşüyor; bu paket daha kısa/özet.
- **Security & Ops Safety Auditor:** Secret hygiene, redaction, kill-switch, rate-limit, risk register — doğru. Proje INV-SEC-RED-1, INV-ERR-SURFACE-1 ile uyumlu.
- **Release & Governance Steward:** SemVer, tag immutability, CI determinism, proof artifacts — doğru. INV-REL-GH, RELEASE_VERIFICATION_CHECKLIST, ECOSYSTEM_CONTRACT_MATRIX ile uyumlu.
- **Docs Editor (ADS-1):** Minimal docs, root allowlist, link integrity, archive — doğru. INV-DOC-* ve docs_triage_ads1 skill ile uyumlu.

### B.3 Cursor Commands

- `/docs-triage`, `/release-verify`, `/trace-key-add`, `/security-audit` — tanımlar proje terminolojisi ve invariant’larıyla uyumlu. INV-T1 → INV-TRACE-REG-1 olarak düzeltilirse daha tutarlı.

---

## Özet Tablo

| Madde | Öneri | Durum |
|--------|--------|--------|
| P0 ROOT_ALLOWLIST format | Format invariant + script’te whitespace = error | **Doğru**; mevcut dosya şu an OK, sertleştirme gerekli |
| P0 Doc path drift | ECOSYSTEM_INVARIANTS.md → docs/ path | **Bu workspace’te zaten doğru**; genel kural geçerli |
| P1 Release body root’ta | release_dmc_* → archive veya docs/templates; allowlist’ten çıkar | **Doğru** |
| P1 BRANCH_GOVERNANCE | CI için “tag pin” dilini netleştir; @main’i CI’dan ayır | **Doğru** |
| B Cursor Rule | — | **Doğru**; INV-T1 → INV-TRACE-REG-1 önerilir |
| B Subagents | — | **Doğru**, proje ile uyumlu |
| B Commands | — | **Doğru**; trace key kısmında INV-TRACE-REG-1 kullan |

---

## Net Öneri

- **Uygula:** P0 format invariant (INV-DOC-ROOT-ALLOWLIST-FMT-1) + check_docs_root.py’de satır içi whitespace kontrolü; P1 release_dmc_* taşıma + ROOT_ALLOWLIST güncellemesi; P1 BRANCH_GOVERNANCE.md CI/@main dil düzeltmesi.
- **Opsiyonel:** ECOSYSTEM_INVARIANTS.md’de ek broken-link taraması (genel INV-DOC-LINK-1 için); mevcut workspace’te kritik 404 yok.
- **Cursor paketi:** Doğrudan kullanılabilir; Rule’da “INV-T1” → “INV-TRACE-REG-1” yapılması önerilir.

**Last updated:** 2026-02  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md, ROOT_ALLOWLIST.txt, check_docs_root.py, BRANCH_GOVERNANCE.md, ECOSYSTEM_INVARIANTS.md
