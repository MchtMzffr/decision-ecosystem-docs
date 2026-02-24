# Akademik Docs Governance — Öneri Doğrulama Raporu

**Purpose:** Verify the proposed P0/P1 invariants (INV-DOC-LINK-1, INV-DOC-ACTIVE-1, INV-DOC-DOMAIN-0, INV-DOC-POLICY-SSOT-1), patch plan, Cursor rules, and cleanup algorithm against the current repo. Corrections and minimal patch notes where needed.

**Scope:** decision-ecosystem-docs; ECOSYSTEM_GATES_AND_INVARIANTS.md; .github/scripts; DOCS_REPO_STRUCTURE.md; DOCUMENTATION_STANDARDS.md.

---

## 1. Özet: Öneriler doğru mu?

**Genel cevap: Evet.** Yön (broken link gate, ACTIVE/ARCHIVE netliği, domain lexeme ban, policy SSOT, Cursor rötuş, deterministic cleanup) doğru ve “fail-closed docs governance” ile uyumlu. Aşağıdaki **düzeltmeler** repoya özgü (dosya adı, governance konumu, mevcut invariant).

---

## 2. Mevcut garanti (senin özetin) — Onay

- Root allowlist + INV-DOC-ROOT-ALLOWLIST-FMT-1 + script: **doğru**
- Release artefact’ler archive’a: **doğru**
- CI fallback (tag pin vs dev @main) dokümanda: **doğru**
- `.cursor/` ALLOWED_DIRS’te: **doğru**

---

## 3. Açık riskler (4 madde) — Onay

1. Broken link → 404: **doğru**; INV-DOC-LINK-1 zaten tanımlı (§12 L) ama **gate yok** (link checker script yok).
2. ACTIVE vs ARCHIVE net değil: **kısmen**; DOCS_REPO_STRUCTURE.md “CURRENT vs ARCHIVE” var ama README’de “CURRENT only / archive ayrı” **policy olarak** tek yerde toplanmamış.
3. Domain lexeme sızıntısı: **doğru**; ölçülebilir gate yok.
4. Policy drift (aynı konu iki yerde): **doğru**; SSOT kuralı yazılı değil.

---

## 4. Önerilen 4 invariant — Doğrulama ve düzeltmeler

### INV-DOC-LINK-1 — Broken links = 0

- **Proje durumu:** ECOSYSTEM_GATES_AND_INVARIANTS.md §12 L’de **zaten var**: “README and doc links (relative) resolve; no broken link. check_docs_root.py / **link checker**”. Ama `check_docs_root.py` sadece allowlist/archive/README/analysis limit yapıyor; **link kontrolü yok**.
- **Öneri:** Yeni script `check_docs_links.py` + CI step. **Doğru.**
- **Patch notu:** Invariant adı **değişmesin** (INV-DOC-LINK-1); sadece “CI / check” sütununu `check_docs_links.py` olarak güncelle (script eklendikten sonra).

---

### INV-DOC-ACTIVE-1 — Current index canonical

- **Formül:** README “Quick links” sadece CURRENT setine (docs/ + root allowlist); archive/ ayrı bölümde.
- **Proje durumu:** README’de zaten “Current documentation” ve “Archive (historical snapshots)” var; INV-DOC-README-CURRENT-1 README’deki linklerin allowlist’te olmasını zorunlu kılıyor. “CURRENT only” ve “archive ayrı” davranışı fiilen uygulanıyor.
- **Öneri:** Bunu resmi invariant yap (INV-DOC-ACTIVE-1). **Doğru.**
- **Patch notu:** ECOSYSTEM_GATES_AND_INVARIANTS.md §5 veya §12’ye satır ekle. Opsiyonel: `check_docs_root.py` veya link checker’da “Current section’da archive/ linki varsa fail” kuralı (çok sıkı istemezsen P2).

---

### INV-DOC-DOMAIN-0 — Domain lexeme ban (ACTIVE)

- **Formül:** `count(domain_lexemes in ACTIVE) == 0`; scope: docs/ (archive/ ve examples/ hariç); config: DOMAIN_LEXEMES.txt.
- **Öneri:** Script + config + CI. **Doğru.** Fail-closed (lexeme bulunursa error) mantıklı.
- **Patch notu:** Config dosya adı `docs/DOMAIN_LEXEMES.txt` önerinle uyumlu. İlk set: örnek lexeme’lar (örn. Sharpe, drawdown, vendor isimleri); repo domain’ine göre genişletilir.

---

### INV-DOC-POLICY-SSOT-1 — Governance single-source

- **Formül:** Branch/Tag/Release politikası yalnız belirlenmiş governance dokümanlarında tanımlı; diğerleri sadece link verir.
- **Proje durumu:** Bu repoda governance dosyaları **root’ta**: BRANCH_GOVERNANCE.md, TAG_GOVERNANCE.md, RELEASE_VERIFICATION_CHECKLIST.md; **docs/** altında: CI_COMPLIANCE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md. Yani “docs/*GOVERNANCE*.md” ifadesi **yanlış** — root’ta *GOVERNANCE*.md var.
- **Düzeltme:** Invariant metninde konum: “Policy is defined only in designated governance docs (**root**: BRANCH_GOVERNANCE.md, TAG_GOVERNANCE.md, RELEASE_VERIFICATION_CHECKLIST.md; **docs/**: CI_COMPLIANCE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md). Other docs **link**, do not duplicate policy text.”
- **Öneri:** SSOT kuralı + opsiyonel check_policy_duplicates.py (P2). **Doğru.**

---

## 5. Patch plan doğrulama ve düzeltmeler

### P0 — Broken link gate (INV-DOC-LINK-1)

- **Yeni dosya:** `.github/scripts/check_docs_links.py` — **doğru.** Relative `[text](path)` parse; ilk aşamada sadece dosya varlığı (anchor opsiyonel).
- **CI:** Bu repoda `ci.yml` yok; workflow **`.github/workflows/docs_structure_guard.yml`**. Step ekle: `python .github/scripts/check_docs_links.py`. **Düzeltme:** “ci.yml” değil, **docs_structure_guard.yml**.
- **Metrik:** broken_links == 0. **Doğru.**

---

### P0 — ACTIVE vs ARCHIVE standardını netleştir

- **Öneri:** “Yeni/Update: docs/DOCUMENTATION_STANDARD.md”.
- **Düzeltme:** Repoda zaten **docs/DOCUMENTATION_STANDARDS.md** (sonunda **S**) var; naming ve doc naming standardı orada. **Yeni “DOCUMENTATION_STANDARD.md” (tekil) eklemeyin** — isim çakışması ve SCREAMING_SNAKE_CASE ile uyumsuzluk riski.
- **Doğru yaklaşım:** ACTIVE/ARCHIVE/CURRENT policy’yi ya **DOCUMENTATION_STANDARDS.md**’e yeni bölüm olarak ekleyin (örn. §4 “CURRENT vs ARCHIVE”) ya da **DOCS_REPO_STRUCTURE.md**’e (zaten “CURRENT vs ARCHIVE” ve root kuralları var) kısa “Policy: CURRENT only in main index; archive immutable snapshot” cümlesiyle güçlendirin. README’de “Quick links (CURRENT)” / “Archive (historical)” etiketleri zaten var; gerekirse bir cümle ile “CURRENT only” vurgulanabilir.

---

### P1 — Domain lexeme gate (INV-DOC-DOMAIN-0)

- **Yeni dosya:** `.github/scripts/check_docs_domain_lexemes.py`; exclude `docs/examples/`, `archive/`; config `docs/DOMAIN_LEXEMES.txt`. **Doğru.**
- **CI:** docs_structure_guard.yml’e step. **Doğru.**

---

### P1 — Governance SSOT

- **Update:** Cross-reference standardı: checklist “how to verify”; governance dosyaları policy SSOT; diğerleri tekrarlamaz, link verir.
- **Düzeltme:** “docs/BRANCH_GOVERNANCE.md”, “docs/TAG_GOVERNANCE.md” **yanlış** — bu repoda bunlar **root’ta**: BRANCH_GOVERNANCE.md, TAG_GOVERNANCE.md. RELEASE_VERIFICATION_CHECKLIST.md da root’ta. Güncelleme yapılacak dosyalar: **root** BRANCH_GOVERNANCE.md, TAG_GOVERNANCE.md, RELEASE_VERIFICATION_CHECKLIST.md ve **docs/** CI_COMPLIANCE_STANDARD.md, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md (hepsi “policy SSOT; others link” ifadesiyle uyumlu olacak şekilde).

---

## 6. Cursor Rule / Skills — Onay ve rötuş

- **INV-TRACE-REG-1** ve **INV-DOC-*** kullanımı: **Doğru.**
- **Docs repo scope kuralı:** “Bu repo’da core API dokümanı yazma; core’a link ver.” ve “Yeni doc eklemeden önce: hangi invariant bunu gerektiriyor?” — **Doğru** ve decision-ecosystem-global.mdc veya docs-scope’lu ayrı bir rule ile eklenebilir.

---

## 7. Cleanup algoritması — Onay

- “Policy/guides/checklist dışında summary/report → archive/DATE”; “template → docs/templates/”; “domain lexeme: policy → rewrite, örnek → docs/examples/”. **Doğru** ve önceki release artefact taşıma ile tutarlı. Tek prompt ile Cursor’a yaptırmak uyumlu.

---

## 8. Yapılacaklar özeti (senin önerin + düzeltmeler)

| Öğe | Durum | Düzeltme / not |
|-----|--------|------------------|
| INV-DOC-LINK-1 | Zaten tanımlı | Script eksik; check_docs_links.py ekle; CI’da docs_structure_guard.yml’e step |
| INV-DOC-ACTIVE-1 | Yeni | ECOSYSTEM_GATES_AND_INVARIANTS.md’e ekle; README policy’yi DOCS_REPO_STRUCTURE veya DOCUMENTATION_STANDARDS’ta netleştir |
| INV-DOC-DOMAIN-0 | Yeni | Script + DOMAIN_LEXEMES.txt + CI step |
| INV-DOC-POLICY-SSOT-1 | Yeni | Metinde governance konumu: root + docs/ (docs/*GOVERNANCE* değil); cross-ref standardı root + docs dosyalarına uygula |
| DOCUMENTATION_STANDARD.md | Kullanma | Yeni dosya açma; DOCUMENTATION_STANDARDS.md veya DOCS_REPO_STRUCTURE.md’i güncelle |
| CI | Workflow adı | ci.yml değil **docs_structure_guard.yml** |
| Governance dosya yolları | Düzelt | BRANCH_GOVERNANCE, TAG_GOVERNANCE, RELEASE_VERIFICATION_CHECKLIST **root’ta** |

---

**Sonuç:** Öneriler doğru yönde ve akademik “devamlı tutarlılık” için uygun. Yukarıdaki düzeltmelerle (dosya adı, governance konumu, mevcut invariant’a referans) patch plan doğrudan uygulanabilir.

**Last updated:** 2026-02  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md, DOCS_REPO_STRUCTURE.md, DOCUMENTATION_STANDARDS.md, .github/workflows/docs_structure_guard.yml
