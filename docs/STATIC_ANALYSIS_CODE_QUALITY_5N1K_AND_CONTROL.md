<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Static Analysis & Code Quality — 5N1K ve Akademik Seviye Kontrol

**Tarih:** 2026-02-19  
**Kapsam:** Tüm çekirdek repolar + integration-harness + decision-ecosystem-docs  
**Metodoloji:** 5N1K (Ne, Neden, Nerede, Ne zaman, Nasıl, Kim), Feynman tekniği (basit açıklama + uygunsuzluk/eksik listesi), akademik kontrol matrisi

---

## 1. Feynman Özeti (Tek Cümleyle “Ne”)

**Statik analiz**, kodu çalıştırmadan sadece metin/yapı üzerinden inceleyerek hata, tutarsızlık ve standart ihlallerini bulmak; **kod kalitesi** ise okunabilirlik, bakım kolaylığı, güvenlik ve test edilebilirlikle ilgili kuralların karşılanmasıdır. Bu rapor, ekosistemde **neyin eksik olduğunu**, **nerede uyumsuzluk bulunduğunu** ve **nasıl düzeltileceğini** 5N1K ile netleştirir.

---

## 2. 5N1K Çerçevesi

### 2.1 Ne (What)

| Soru | Cevap |
|------|--------|
| **Ne inceleniyor?** | Python kaynak kodu (.py), testler, CLI, dokümantasyon referansları, CI yapılandırması. |
| **Hangi araçlar?** | Ruff (lint + format), pyproject.toml [tool.ruff], hedef Python 3.11. |
| **Hangi standartlar?** | SOLID, Clean Architecture, INV-* invariant’ları, REPO_SIGNATURE, SECURITY.md, schema pin. |

### 2.2 Neden (Why)

- **Kalite:** Tekrarlanabilir derleme, okunabilir kod, az hata.
- **Güvenlik:** Gizli bilgi sızması (secret scanning), redaction, fail-closed.
- **Uyumluluk:** decision-schema SSOT, domain-agnostic, sürüm tek kaynağı (INV-V1).
- **Akademik kontrol:** Her öneri ve uygunsuzluk “neden” ile gerekçelendirilir; ölçülebilir kriterler vardır.

### 2.3 Nerede (Where)

| Seviye | Kapsam |
|--------|--------|
| **Dosya** | Her .py (ve hedeflenen .md/.sh) — imza, import, syntax, format. |
| **Repo** | decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core, execution-orchestration-core, decision-ecosystem-integration-harness, decision-ecosystem-docs. |
| **Ekosistem** | CI ortak davranışı, contract matrix, doc-drift. |

### 2.4 Ne Zaman (When)

- **Geliştirici:** Commit öncesi (pre-commit hook önerilir; şu an yok).
- **CI:** Her push/PR’da test + (öneri) lint + format check.
- **Release:** Tag öncesi INV-REL-4, sürüm tek kaynağı, release checklist.

### 2.5 Nasıl (How)

- **Lint:** `ruff check .` — F401 (unused import), F841 (unused variable), syntax.
- **Format:** `ruff format --check .` — satır uzunluğu, tırnak stilı.
- **Syntax:** Python 3.11 hedefi; f-string içinde `\` escape (Python 3.12+) kullanılmamalı 3.11’de.
- **Argparse:** `--in` gibi keyword isimleri `dest="input_path"` ile kullanılmalı; `args.in` yerine `getattr(args, 'in')` veya `args.input_path`.

### 2.6 Kim (Who)

- **Geliştirici:** Yerel ruff/mypy çalıştırır, imza ekler.
- **CI:** Otomatik test + (öneri) ruff check/format.
- **Bakımcı:** Secret scanning, Dependabot, release checklist.

---

## 3. Uygunsuzluklar (Non-Conformities) — Ruff + Mevcut Raporlar

Aşağıdaki liste **2026-02-19** ruff çıktıları ve mevcut akademik rapora göre derlenmiştir. “Uygun değil” = şu anki durum standarda aykırı.

### 3.1 Kritik (Syntax / Çalışmayan Kod) — ✅ P0 uygulandı (2026-02-19)

| # | Repo | Dosya | Sorun | Durum |
|---|------|--------|--------|--------|
| NC-1 | decision-schema | tests/test_invariant_ci_0_workflow_hygiene.py | f-string içinde `b'\r'` escape | ✅ `cr_count` ayrı değişkene alındı |
| NC-2 | mdm-engine | tests/test_invariant_ci_0_workflow_hygiene.py | Aynı | ✅ Düzeltildi |
| NC-3 | ops-health-core | tests/test_invariant_ci_0_workflow_hygiene.py | Aynı | ✅ Düzeltildi |
| NC-4 | evaluation-calibration-core | eval_calibration_core/cli.py | `args.in` keyword | ✅ `dest="input_path"`, `getattr(args, "input_path", None)` |
| NC-5 | decision-ecosystem-integration-harness | tools/rewrite_ci_yml.py | f-string escape | ✅ `cr_val` / `lf_val` ayrı değişkenler |

### 3.2 Yüksek (Kod Kalitesi) — ✅ P1 uygulandı (ruff check --fix + format)

| # | Repo | Kategori | Durum |
|---|------|----------|--------|
| NC-6 … NC-13 | Tüm core + harness + docs | F401 / F841 / F541 | ✅ Her repoda `ruff check . --fix` ve `ruff format .` uygulandı; kalan tekiller (örn. dmc `__all__`, mdm `_s0`, ops `update_kill_switch` atamasız) elle düzeltildi. |

### 3.3 Process / CI Uyumsuzlukları — ✅ P1/P2 uygulandı

| # | Konu | Durum |
|----|------|--------|
| NC-14 | Linting CI’da yok | ✅ Tüm core + harness + docs CI’da “Ruff check” ve “Ruff format check” adımı eklendi. |
| NC-15 | Secret scanning yok | ✅ decision-ecosystem-docs’ta `.github/workflows/secret-scan.yml` (Gitleaks) eklendi. |
| NC-16 | Coverage raporu yok | ✅ Tüm core + harness CI’da pytest-cov kurulumu ve `--cov=. --cov-report=term-missing` eklendi. |
| NC-17 | Dependabot yok | ✅ Tüm repolarda `.github/dependabot.yml` (pip haftalık; docs’ta + github-actions) eklendi. |

---

## 4. Eksik Listesi (Gaps)

Bunlar “henüz yapılmamış” iyileştirmeler; uygunsuzluk değil, eksiklik.

### 4.1 Araç / Konfigürasyon

- **Pre-commit:** pre-commit hook (ruff, repo-signature check) yok.
- **mypy:** pyproject.toml’da [tool.mypy] yok; tip kontrolü sadece manuel/IDE.
- **Karmaşıklık metrikleri:** radon/mccabe ile cyclomatic complexity CI’da yok (akademik raporda önerilmiş).
- **Lock file:** poetry.lock veya pip-tools lock yok; tekrarlanabilir kurulum zayıf.

### 4.2 CI / Release

- **Lint/format adımı:** CI’da `ruff check .` ve `ruff format --check .` yok.
- **Secret scanning:** gitleaks veya trufflehog job’ı yok.
- **Coverage:** pytest-cov ve “min %80” benzeri threshold yok.
- **Changelog / sürüm zorunluluğu:** Otomatik changelog üretimi ve semver zorunluluğu yok.

### 4.3 Dokümantasyon / Governance

- **Doc–kod senkronu:** README/INTEGRATION_GUIDE ile kod sürümü drift’i (P1); senkron script önerilmiş.
- **Structured logging:** JSON logging standardı tanımlı değil.

### 4.4 Güvenlik

- **Runtime input validation:** Hafif decorator veya pydantic benzeri doğrulama yok (öneri).
- **Dependency CVE taraması:** Dependabot veya benzeri açık değil.

---

## 5. Öneri Listesi (Öncelikli)

### P0 — Hemen (Bloker / Syntax)

1. **NC-1, NC-2, NC-3, NC-5:** f-string içinde `b'\r'` / `b'\n'` kullanımını kaldır; örn. `count_cr = b.count(b'\r')` ayrı satırda hesapla, f-string’de sadece `{count_cr}` kullan.
2. **NC-4:** evaluation-calibration-core `cli.py`: `--in` için `dest="input_path"` ekle; tüm `args.in` kullanımlarını `args.input_path` yap.

### P1 — Kısa Vade (Kalite)

3. **NC-6 … NC-13:** Her repoda `ruff check . --fix` ve (gerekiyorsa) `ruff format .` uygula; unused import/variable ve gereksiz f-string’leri temizle.
4. **NC-14:** Tüm core + harness + docs CI’larına “Ruff check” ve “Ruff format check” adımı ekle (pyproject.toml [tool.ruff] ile uyumlu).
5. **Secret scanning (NC-15):** CI’a gitleaks veya trufflehog job’ı ekle (örn. docs repo veya ortak workflow).

### P2 — Orta Vade

6. **Coverage (NC-16):** pytest-cov ekle; CI’da raporla ve (isteğe bağlı) threshold koy.
7. **Dependabot (NC-17):** .github/dependabot.yml ile enable et.
8. **Pre-commit:** .pre-commit-config.yaml ile ruff + imza doğrulama.

### P3 — Uzun Vade

9. **mypy:** Seçili paketlerde [tool.mypy] aç; strict’e kademeli geç.
10. **Karmaşıklık:** radon veya ruff extend ile complexity uyarıları.
11. **Lock file:** pip-tools veya poetry ile lock; CI’da lock’tan kurulum.

---

## 6. Akademik Kontrol Matrisi

Her satır “kontrol edilen şey” ve “nasıl doğrulanacağı”nı özetler.

| Kontrol | Ne | Nasıl Doğrulanır | Hedef |
|--------|-----|-------------------|--------|
| **Imza** | Tüm hedef dosyalarda repo imzası | `scripts/add_repo_signature.py --verify` | Exit 0, “Verify OK” |
| **Syntax** | Python 3.11 geçerli sözdizimi | `ruff check .` (syntax hataları) | 0 error |
| **Lint** | Kullanılmayan import/değişken, stil | `ruff check .` | 0 error |
| **Format** | Satır uzunluğu, tırnak | `ruff format --check .` | 0 change |
| **Test** | Birim + invariant testleri | `pytest tests/` | Tümü geçer |
| **Schema pin** | decision-schema minor sürüm uyumu | INV-Schema testleri | Geçer |
| **Sürüm tek kaynağı** | pyproject.toml = __version__ / version.py | INV-V1 testi | Geçer |
| **Secret** | Commit’te gizli yok | gitleaks/trufflehog (öneri) | 0 finding |
| **CI lint** | PR’da lint/format çalışıyor | workflow’da ruff adımı (öneri) | Var |

---

## 7. Sonuç ve Bir Sonraki Adım

- **Uygunsuzluklar:** 17 madde (5 kritik/syntax, 8 yüksek kalite, 4 process/CI).
- **Eksikler:** Pre-commit, mypy, CI lint/format, secret scanning, coverage, Dependabot, lock file, doc-sync, structured logging.
- **Öncelik:** P0 (syntax + CLI keyword) hemen; P1 (ruff fix + CI lint) kısa vade; P2/P3 plana alınabilir.

**Tek cümle (Feynman):** “Kodu çalıştırmadan, kurallara göre tarıyoruz; şu an bazı syntax ve lint hataları ile CI’da lint/secret/coverage eksik — önce P0/P1 düzeltmeleri yapılırsa akademik seviye kontrol kriterleri karşılanır.”

---

**Son güncelleme:** 2026-02-19  
**Referanslar:** ACADEMIC_STATIC_ANALYSIS_REPORT.md, STATIC_ANALYSIS_REMEDIATION_2026-02-18.md, ECOSYSTEM_INVARIANTS.md, Ruff 2026.x
