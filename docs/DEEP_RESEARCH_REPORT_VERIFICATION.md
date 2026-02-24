# deep-research-report.md Doğrulama Raporu

**Kaynak:** `decision-ecosystem-docs/deep-research-report.md`  
**Doğrulama:** Workspace erişimi ile satır/iddia bazında kontrol (2026-02)  
**Kapsam:** Decision Ecosystem workspace (decision-ecosystem-docs + 6 core + harness + experimental)

---

## 1. Raporun temel iddiası: "Depo URL 404"

| Rapor iddiası | Doğrulama | Veri |
|---------------|-----------|------|
| "Verilen depo URL'sine dışarıdan erişim 404" | **Kısmen doğru / bağlama bağlı** | Tek bir `decision-ecosystem` repo URL’si yok; ekosistem **çoklu repo** yapısında. Workspace’te erişilen yapı: **decision-ecosystem-docs**, **decision-schema**, **mdm-engine**, **decision-modulation-core**, **ops-health-core**, **evaluation-calibration-core**, **execution-orchestration-core**, **decision-ecosystem-integration-harness**, **explainability-audit-core** (+ root docs/tools/scripts). GitHub’da bu repolar ayrı ayrı (örn. MchtMzffr/decision-schema, MchtMzffr/decision-ecosystem-docs) mevcut; tek “decision-ecosystem” adında bir repo olmadığı için 404 beklenir. |

**Sonuç:** "Depo erişilemedi" ifadesi, **tek bir monolitik repo** varsayımına dayanıyor. Gerçekte ekosistem **çoklu repo**; workspace’te tüm bu repolara erişim var ve aşağıdaki maddeler buna göre doğrulandı.

---

## 2. İnceleme maddesi bazında durum (rapor tablosu vs gerçek veri)

| İnceleme maddesi | Rapor | Workspace doğrulama | Kanıt |
|------------------|-------|---------------------|--------|
| **Repo yapısı (tree)** | Erişilemedi | **Erişildi** | 9 repo + workspace root; her core’da `pyproject.toml`, `README.md`, `LICENSE`, `.github/workflows/ci.yml`; docs’ta `ROOT_ALLOWLIST.txt`, `tools/`, `docs/`, `archive/`. |
| **README / docs** | Erişilemedi | **Var** | Tüm core/harness/docs’ta README; docs repo’da ARCHITECTURE, ECOSYSTEM_INVARIANTS, CI_COMPLIANCE_STANDARD, REPO_REGISTRY, RELEASE_VERIFICATION_CHECKLIST, NEXT_STEPS_ROADMAP, TAG_GOVERNANCE, FORMULAS, INTEGRATION_GUIDE vb. |
| **Kaynak kod analizi** | Erişilemedi | **Yapılabildi** | Dil: **Python** (pyproject, `*.py`). Modül sınırları: decision_schema, mdm_engine, dmc_core, ops_health_core, eval_calibration_core, execution_orchestration_core, harness, explainability_audit_core. |
| **Testler / coverage** | Erişilemedi | **Var** | Her core/harness’ta `tests/`; invariant testleri (version_single_source, schema_pin_minor_2, fail_closed, guard_order_determinism, ops_health_guard); docs’ta `tools/tests/` (public_main_audit_negative). |
| **CI (GitHub Actions)** | Erişilemedi | **Var** | Her core/harness’ta `.github/workflows/ci.yml` (secret_scan, LICENSE check, Ruff, build, pytest, artifact); docs’ta `docs_structure_guard.yml` + `secret-scan.yml`. |
| **Lisans** | Erişilemedi | **Var** | Tüm repolarda root **LICENSE** (MIT metni). README’lerde "MIT License. See [LICENSE](../LICENSE)." — placeholder yok. |
| **Issues / PR’lar** | Erişilemedi | **Belirsiz** | Workspace’te issue/PR verisi yok; yalnızca yerel dosya ağacı doğrulandı. |
| **Commit geçmişi / release/tag** | Erişilemedi | **Kısmen** | Yerel git log’larda license/SPDX commit’leri görüldü; tag/release sayısı GitHub API olmadan tam sayılamadı. REPO_REGISTRY’de latest_tag: decision-schema v0.2.2, mdm v0.2.1, dmc v0.1.1, ops-health v0.1.1, eval-cal v0.1.1, exec-orch v0.1.0. |

---

## 3. Dil, modül, bağımlılık (rapor § “belirlenemedi”)

| Rapor iddiası | Doğrulama | Veri |
|---------------|-----------|------|
| "Programlama dilleri, modül sınırları belirlenemedi" | **Yanlış (workspace’te belirlendi)** | **Dil:** Python (pyproject.toml + .py). **Modül grafı:** SSOT = decision-schema; core’lar sadece decision-schema’ya bağımlı (INV-CORE-DEP-1). Örnek: mdm-engine `dependencies = ["numpy>=1.24", "decision-schema>=0.2,<0.3"]`. |
| "Bağımlılık tablosu unspecified" | **Kısmen giderildi** | decision-schema: 0.2.2, bağımlılık yok. mdm-engine: decision-schema>=0.2,<0.3, numpy>=1.24. Diğer core’lar benzer; tam lockfile (SBOM) workspace’te üretilmedi. |

---

## 4. Güvenlik, lisans, CI (rapor § “unspecified”)

| Rapor iddiası | Doğrulama | Veri |
|---------------|-----------|------|
| "Depoda hangi lisans bilinmiyor" | **Yanlış** | Tüm repolarda root **LICENSE** (MIT). README’de "MIT License. See [LICENSE](../LICENSE)." SPDX pratikte uyumlu (MIT identifier). |
| "CI/workflow yokluğu bilinmediği için unspecified" | **Yanlış** | 10 workflow dosyası: 6 core + harness + explainability + docs (docs_structure_guard, secret-scan). Her core CI: checkout, LICENSE check, setup-python, Ruff check/format, decision-schema install (pin/fallback), build, pytest, artifact. |
| "no_secrets_in_repo" invariant | **Uygulanıyor** | Docs’ta gitleaks (secret-scan.yml); core’larda ci.yml içinde secret_scan job. |
| "workflow_permissions_minimized" | **Uygulanıyor** | Örnek (docs_structure_guard): `permissions` yok (default); core ci.yml’lerde `permissions: contents: read` mevcut. |
| "sbom_generated" | **Yok** | Hiçbir repoda scorecard workflow veya SBOM artefact yok (rapor P1 önerisi ile uyumlu). |

---

## 5. Minimum artefact seti (rapor tablosu P0/P1)

| Öğe | Rapor öncelik | Workspace durumu | Not |
|-----|----------------|------------------|-----|
| README.md | P0 | **Var** (tüm repolarda) | Amaç, kurulum, mimari linkleri mevcut. |
| LICENSE | P0 | **Var** (tüm repolarda) | MIT metni; CI’da `test -f LICENSE`. |
| SECURITY.md | P0 | **Kısmen** | **Var:** decision-schema, mdm-engine, decision-modulation-core, ops-health-core, evaluation-calibration-core. **Yok:** decision-ecosystem-docs, execution-orchestration-core, integration-harness, explainability-audit-core. |
| CONTRIBUTING.md | P1 | **Yok** | Hiçbir repoda CONTRIBUTING.md yok. |
| .github/workflows/ci.yml | P0 | **Var** (core/harness) | Build, test, lint, LICENSE, artifact. |
| .github/dependabot.yml | P1 | **Var** (docs) | pip + github-actions, weekly; diğer repolarda tek tek kontrol edilmedi. |
| scorecard.yml | P1 | **Yok** | Hiçbir repoda yok. |
| SBOM | P1 | **Yok** | Üretilmiyor. |
| Release tags + SemVer | P1 | **Var** | REPO_REGISTRY + NEXT_STEPS_ROADMAP’te tag/sürüm tabloları; pyproject.version ile uyum. |

---

## 6. Contract-first invariant’lar (rapor § önerilen I1–I4)

| Invariant | Rapor | Doğrulama | Veri |
|-----------|-------|-----------|------|
| **I1 — Bağımlılık yönü (core yalnızca SSOT)** | Öneri | **Uyumlu** | Core’lar sadece decision-schema’ya bağımlı; pyproject’lerde core↔core yok. |
| **I2 — SemVer uyumu** | Öneri | **Uyumlu** | decision-schema 0.2.2; tag v0.2.2; core’lar >=0.2.2,<0.3 veya >=0.2,<0.3 (mdm local’de 0.2). |
| **I3 — Fail-closed** | Öneri | **Uygulanıyor** | DMC’de fail-closed testleri (test_invariant_4_fail_closed.py); modulator’da HOLD/DENY; guard/kill-switch dokümante. |
| **I4 — Secret redaction** | Öneri | **Kısmen** | Secret scanning (gitleaks) CI’da var; log redaction ayrı kontrol edilmedi. |

---

## 7. Olgunluk ve roadmap (rapor § “sınıflandırılamaz”)

| Rapor iddiası | Doğrulama | Veri |
|---------------|-----------|------|
| "Olgunluk seviyesi unspecified" | **Kısmen giderildi** | Release/tag: 6 core released (v0.1.0–v0.2.2). CI: her PR’da çalışıyor. Test: invariant + birim testleri var. Supply-chain: SBOM/Scorecard yok. NEXT_STEPS_ROADMAP’te P0 tamamlanmış, P2–P3 ertelendi. |
| Mermaid roadmap / SSOT diyagramı | Şablon | **Uyumlu** | REPO_REGISTRY ve ECOSYSTEM_INVARIANTS ile uyumlu; SSOT = decision-schema, core’lar domain-agnostic. |

---

## 8. Patch planı (rapor § “erişim sağlanınca”)

| Rapor önerisi | Workspace durumu |
|---------------|------------------|
| README: mimari SSOT + core + adapter | **Mevcut** (ARCHITECTURE, REPO_REGISTRY, ECOSYSTEM_INVARIANTS). |
| LICENSE + NOTICE | **LICENSE var**, NOTICE yok (çoğu repo için gerekmiyor). |
| ci.yml: format/lint → build → test → compat → SBOM | **Build/test/lint/artifact var**; SBOM ve Scorecard yok. |
| dependabot.yml | **Docs’ta var** (pip + github-actions). |
| scorecard.yml | **Yok** — eklenebilir (P1). |
| Swift/SwiftUI | **Yok** — ekosistem tamamen Python. |

---

## 9. Özet tablo (rapor satırı vs gerçek)

| Rapor bölümü | “Unspecified” / “erişilemedi” iddiası | Workspace’te doğrulandı mı? | Not |
|--------------|----------------------------------------|-----------------------------|-----|
| § Erişim durumu | 404, içerik yok | **Hayır** — çoklu repo var, hepsine erişim var | Tek repo URL’si yanlış varsayım. |
| § Repo yapısı | Erişilemedi | **Evet** — tree, README, LICENSE, CI | 9 repo + root. |
| § Dil/modül/bağımlılık | Belirlenemedi | **Evet** — Python, SSOT, pyproject | Bağımlılık tablosu kısmen doldurulabilir. |
| § Kod kalitesi | Üretilemedi | **Kısmen** — test/invariant var; kompleksite metrikleri çalıştırılmadı | cloc/cyclomatic bu doğrulamada yapılmadı. |
| § Bağımlılık tablosu | Boş/unspecified | **Kısmen** — manifest’ler okundu | SBOM yok. |
| § Lisans | Bilinmiyor | **Yanlış** — MIT, tüm repolarda | INV-LIC-1 karşılanıyor. |
| § CI/güvenlik | Unspecified | **Yanlış** — CI var, secret_scan var | Scorecard/SBOM yok. |
| § Olgunluk | Sınıflandırılamaz | **Kısmen** — release/tag/CI/test var | Rubrik uygulanabilir. |
| § SECURITY.md | P0 öneri | **Kısmen** — 5 repoda var, 4’te yok | Docs, exec-orch, harness, explainability’de yok. |
| § CONTRIBUTING.md | P1 öneri | **Yok** | Hiçbir repoda yok. |
| § Scorecard/SBOM | P1 öneri | **Yok** | Eklenebilir. |

---

## 10. Net cevap: “Rapor bulguları doğru mu?”

- **“Depo 404, hiçbir şey doğrulanamaz”** → **Workspace’e göre yanlış.** Ekosistem tek repo değil; çoklu repo ve hepsine erişim var. Rapor tek bir “decision-ecosystem” URL’si varsaydığı için 404’e takılmış.
- **“Repo yapısı, README, kod, test, CI, lisans unspecified”** → **Yanlış.** Hepsi mevcut ve kontrol edildi.
- **“Lisans/güvenlik/CI bilinmiyor”** → **Yanlış.** LICENSE (MIT), CI (workflow’lar), secret_scan mevcut.
- **“Bağımlılık tablosu boş”** → **Kısmen doğru.** SBOM/lockfile yok; pyproject’lerden isim/sürüm çıkarıldı.
- **“SECURITY.md P0”** → **Kısmen.** 5 repoda var, 4’te (docs, exec-orch, harness, explainability) yok.
- **“CONTRIBUTING, Scorecard, SBOM yok”** → **Doğru.** Rapor önerisi olarak uyumlu.

**Sonuç:** Raporun **temel varsayımı** (tek repo + 404) gerçek yapıyla uyuşmuyor. **Workspace verisiyle** raporun “unspecified / erişilemedi” dediği maddelerin çoğu **doğrulanabilir ve mevcut**; eksik olanlar (SECURITY.md bazı repolarda, CONTRIBUTING, Scorecard, SBOM) raporun kendi P0/P1 öneri listesiyle uyumlu.

---

**Hazırlayan:** Workspace doğrulama (decision-ecosystem-docs + tüm repolar)  
**Tarih:** 2026-02  
**Referans:** deep-research-report.md, REPO_REGISTRY.md, ECOSYSTEM_INVARIANTS.md, CI_COMPLIANCE_STANDARD.md
