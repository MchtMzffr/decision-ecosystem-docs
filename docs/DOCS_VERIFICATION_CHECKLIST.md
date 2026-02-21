<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Documentation Verification Checklist — Gaps, Errors, Unapplied Steps

**Purpose:** Tek referans listesi: dökümanlar taranıp standartlara ve gerçek duruma göre tespit edilen **atlamalar**, **yanlış/uyumsuz bilgiler** ve **uygulanmamış adımlar**.  
**Oluşturulma:** 2026-02-19  
**Uygulandı:** 2026-02-19 — A1–A5, Y1–Y3, U1–U4, T1–T2 düzeltmeleri yapıldı (DOCS_REPO_STRUCTURE, RELEASE_VERIFICATION_CHECKLIST, check_workspace_sync, NEXT_STEPS_ROADMAP, ECOSYSTEM_INVARIANTS, CI_COMPLIANCE_STANDARD §3, README, ECOSYSTEM_CONTRACT_MATRIX, tüm core/harness CI’da INV-CI-BUILD-SMOKE-1, check_ci_compliance pin/perm/proof).  
**Kullanım:** Yeni tespitleri tabloya ekleyin; giderilen maddeleri not edin.

---

## 1. Atlandı (Eksik / Dokümanda veya listede yok)

| # | Konu | Nerede | Açıklama |
|---|------|--------|----------|
| A1 | Root allowlist’te **ECOSYSTEM_INVARIANTS.md** yok | DOCS_REPO_STRUCTURE.md §2.1 | README "Architecture & governance" altında bu dosyaya link var; root allowlist tablosunda adı geçmiyor. Eklenmeli veya "Governance" satırına dahil edilmeli. |
| A2 | **RELEASE_VERIFICATION_CHECKLIST** — Version Single-Source tablosunda 2 repo eksik | RELEASE_VERIFICATION_CHECKLIST.md | "Version Single-Source (INV-REL-1)" tablosunda yalnızca 4 repo var (decision-schema, mdm-engine, ops-health-core, evaluation-calibration-core). **decision-modulation-core** ve **execution-orchestration-core** eklenmeli (NEXT_STEPS_ROADMAP P0 tablosu ile uyum). |
| A3 | **RELEASE_VERIFICATION_CHECKLIST** — INV-REL-1 checklist şablonunda dmc-core eksik | RELEASE_VERIFICATION_CHECKLIST.md §Checklist Template | "INV-REL-1 (Version Single-Source)" maddelerinde decision-modulation-core için satır yok; eklenmeli. |
| A4 | **check_workspace_sync.py** — decision-ecosystem-docs repoda yok | tools/check_workspace_sync.py REPO_DIRS | INV-SYNC-1 "tüm repolar" der; standart 8 repo sayıyor. Sync script’te **decision-ecosystem-docs** yok, **explainability-audit-core** var. Docs eklenmeli; explainability (opsiyonel/ertelenmiş) ise dokümante edilmeli veya listeden çıkarılmalı. |
| A5 | **NEXT_STEPS_ROADMAP** — integration-harness P0 tabloda yok | NEXT_STEPS_ROADMAP.md | P0 Release Alignment tablosunda harness yok. Harness’ın pyproject version + tag’i varsa INV-DOC-DRIFT-1 için tabloya eklenmesi gerekebilir; yoksa "harness version tabloda değil" bilinçli karar olarak dokümante edilmeli. |

---

## 2. Yanlış / Uyumsuz Bilgi

| # | Konu | Nerede | Açıklama |
|---|------|--------|----------|
| Y1 | **INV-SYNC-1 metrik kısaltması** | ECOSYSTEM_INVARIANTS.md | Tabloda "Done = Gates_present ∧ Main_parity" yazıyor; CI_COMPLIANCE_STANDARD §6.1’de **Done = (Gates_present = 1) ∧ (CI_pass = 1) ∧ (Main_parity = 1)**. CI_pass invariant listesinde açık yok; ya ECOSYSTEM_INVARIANTS’a CI_pass eklenmeli ya da "Main_parity" ile "CI_pass dahil" notu konmalı. |
| Y2 | **CI Compliance Standard §3** — Script "optional" deniyor | docs/CI_COMPLIANCE_STANDARD.md §3 | "Automated (optional): A script could grep..." ifadesi var. Oysa INV-CI-COMPLY-2 ile script zorunlu (docs CI’da çalışıyor). §3 güncellenmeli: otomasyon artık zorunlu, script adı ve §7 referansı verilmeli. |
| Y3 | **README tekrarlayan link** | README.md | "Analysis & reports" bölümünde CI Compliance Standard linki "INV-CI-COMPLY-1: required CI steps..." diyor; "CI & operations" bölümünde ise "INV-CI-COMPLY-1/2... compliance checker" deniyor. Aynı doküman iki yerde; biri kısa biri uzun. İkisi de güncel tutulmalı (INV-CI-COMPLY-2 ve checker vurgulanmalı). |

---

## 3. Adım Uygulanmadı (Standard’da / invariant’ta yazıyor, uygulama yok)

| # | Konu | Nerede tanımlı | Durum |
|---|------|----------------|--------|
| U1 | **INV-CI-BUILD-SMOKE-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_INVARIANTS | Build sonrası `pip install dist/*.whl` + minimal import smoke hiçbir core/harness CI’da yok. Adım eklenmemiş. |
| U2 | **INV-CI-ACT-PIN-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_GATES §13 | Actions `uses:` pin kontrolü **check_ci_compliance.py** içinde yapılmıyor. Otomatik doğrulama yok; manuel veya script genişletmesi gerekir. |
| U3 | **INV-CI-PERM-1** | CI_COMPLIANCE_STANDARD §5.1, ECOSYSTEM_GATES §13 | `permissions: { contents: read }` kontrolü checker’da yok. Uygulama: workflow’larda var mı manuel/grep; otomasyon istenirse checker’a eklenir. |
| U4 | **INV-CI-PROOF-STD-1** (path/format) | CI_COMPLIANCE_STANDARD §2.5 | Checker sadece "pytest-report" string’ini arıyor; artifact path’in `pytest-report.json` veya `artifacts/pytest-report.json` olduğu doğrulanmıyor. Tam format uyumu için checker sıkılaştırılabilir. |

---

## 4. Tutarsızlık (İki kaynak farklı diyor)

| # | Konu | Kaynak 1 | Kaynak 2 | Öneri |
|---|------|----------|----------|--------|
| T1 | **Repo listesi: 8 vs 7 + explainability** | CI_COMPLIANCE_STANDARD, ECOSYSTEM_GATES: "8 repos" (6 core + harness + docs) | check_workspace_sync: 7 dir (6 core + harness + explainability; **docs yok**) | Tek SSOT: Ya "8 repo = 6 core + harness + docs" ve sync’e docs eklenir, explainability opsiyonel açıklanır; ya da repo tanımı güncellenir. |
| T2 | **decision-schema version aralığı** | CI standard: cores ">=0.2.2,<0.3" | ECOSYSTEM_CONTRACT_MATRIX: mdm-engine ">=0.2.1,<0.3" | Kasıtlı ise (mdm 0.2.1 kabul) contract matrix’te not; değilse 0.2.2 olarak güncellenmeli. |

---

## 5. Özet (Yapılacaklar)

- **Atlandı:** DOCS_REPO_STRUCTURE allowlist (ECOSYSTEM_INVARIANTS), RELEASE_VERIFICATION_CHECKLIST version tablosu ve INV-REL-1 şablonu (dmc, exec-orch), check_workspace_sync REPO_DIRS (docs ekle / explainability netleştir), roadmap harness (bilinçli karar veya tabloya ekle).
- **Yanlış/uyumsuz:** INV-SYNC-1 metrik (CI_pass), CI standard §3 (optional→mandatory), README CI Compliance açıklamaları (INV-CI-COMPLY-2).
- **Uygulanmadı:** INV-CI-BUILD-SMOKE-1 (workflow’lara smoke adımı), INV-CI-ACT-PIN-1 / INV-CI-PERM-1 (checker’da veya ayrı script), INV-CI-PROOF-STD-1 (checker’da path/format).
- **Tutarsızlık:** Repo listesi (sync vs standard), decision-schema minor (0.2.1 vs 0.2.2) contract matrix ile netleştirilmeli.

---

---

## 6. External review (GitHub main) — 2026-02

**Kaynak:** İnceleme GitHub main branch’teki dosyalar üzerinden yapıldı; bazı standart dosyaları fetch edilemediği için “doğrulanamadı” işaretlenmişti.

**Workspace vs public main:** "Workspace'ta doğru" değerli; **DONE = public main'de kanıt** (INV-PUBLIC-MAIN-1). Public main farklıysa (push eksik veya farklı remote) iddia güncellenmemeli.

| P0 madde | İnceleme (public main) | Workspace durumu | Public main'i kapatmak için |
|----------|------------------------|------------------|-----------------------------|
| P0.1 Matrix vs tag | decision-schema main 0.2.1, tag v0.2.1 | Bazı clone'larda 0.2.2; matrix @v0.2.2. | decision-schema'da v0.2.2 tag'i oluşturup push et **veya** matrix'i v0.2.1'e indir. |
| P0.2 LICENSE + placeholder | LICENSE 404; README [Add your license] | Bu workspace'te LICENSE var, README düzgün. | Tüm değişiklikleri **origin main**'e push et; `python tools/public_main_audit.py` ile doğrula. |
| P0.3 ops-health doc↔code | FORMULAS/README max_rate_limit_events | Bu workspace'te max_429_per_window. | Push ops-health-core main; audit script ile teyit. |
| P0.4 CI minimal | CI’da tag/ruff/build/proof/artifact yok; @main fallback | Bu workspace’te tam CI + tag fallback. | Tüm repo CI değişikliklerini push et; audit ile ci.yml kontrolü. |

**Yeni kurallar (inceleme önerisi → uygulandı):**

- **INV-LIC-SPDX-2:** Repo-level LICENSE + README placeholder; CI her ikisini de doğrulasın. (ECOSYSTEM_INVARIANTS, ECOSYSTEM_GATES.)
- **INV-REL-NO-TBD-1:** Publish anında release body’de TBD olmasın. (RELEASE_NOTES_STANDARD_AND_TEMPLATES.md.)
- **INV-DOC-LANG-2:** Normatif dokümanlar İngilizce; meta/operasyonel (örn. CI_RELIABILITY) Türkçe allowlist ile. (ECOSYSTEM_GATES.)

**2.1 / 2.2 (PARAMETER_INDEX, trace registry):** Workspace’te PARAMETER_INDEX context key’leri düz format, trace key’ler noktalı; trace_registry’de exec.* kayıtlı. Ek patch uygulanmadı.

**INV-PUBLIC-MAIN-1:** DONE öncesi public main doğrulaması zorunludur. `python tools/public_main_audit.py --owner MchtMzffr` (veya ilgili owner) exit 0 olmalı. Script: LICENSE, README placeholder, ops-health FORMULAS/README drift, CI tag trigger ve @main fallback kontrolleri.

**P0 Patch Plan (fail-closed, deterministik):** (1) **P0.1** Remote/owner: `git remote -v` → `github.com/MchtMzffr/<repo>.git`; `python tools/check_remote_owner.py --workspace <parent>`. (2) **P0.2** LICENSE + README placeholder: tüm core/harness’ta root LICENSE, README’de placeholder yok; INV-OWNER-REF-1 (MeetlyTR → MchtMzffr). (3) **P0.3** SSOT: decision-schema 0.2.2 + tag v0.2.2; pin >=0.2.2,<0.3; CI fallback @v0.2.2 (no @main). (4) **P0.4** CI_COMPLIANCE_STANDARD: decision-schema CI’da PARAMETER_INDEX, ruff, build, artifact. Yeni invariant’lar: INV-PUBLIC-MAIN-2, INV-README-NO-PLACEHOLDER-1, INV-OWNER-REF-1, INV-SSOT-REALITY-1.

---

**Last updated:** 2026-02-19  
**References:** CI_COMPLIANCE_STANDARD.md, ECOSYSTEM_INVARIANTS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, DOCS_REPO_STRUCTURE.md, RELEASE_VERIFICATION_CHECKLIST.md, NEXT_STEPS_ROADMAP.md
