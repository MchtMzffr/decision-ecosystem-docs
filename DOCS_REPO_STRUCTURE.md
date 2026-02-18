# decision-ecosystem-docs — Dosya Yapısı Standardı

**Amaç:** Bu repo ekosistem genelinde **governance, release ve verification** için tek kaynak (SSOT) olsun. Her dosyayı root’a atmak yerine net bir yapı ve kural seti uygulanır.

**İlkeler:** CURRENT (güncel, tek bakışta bulunur) vs ARCHIVE (tarihsel snapshot); root sadece “yaşayan” dokümanlar; tekrarlar ve eski raporlar archive’da.

---

## 1. Repo amacı (net)

- **Governance:** Branch/tag/release kuralları (INV-REL-*, INV-GOV-*)
- **Release & verification:** Checklist, contract matrix, tag politikası
- **Mimari & entegrasyon:** Ekosistem genel bakış, formüller, entegrasyon rehberi
- **Güncel durum:** Roadmap ve tamamlanan işler için **tek** özet dosyası

Bu amaca hizmet etmeyen veya “bir oturumun çıktısı” olan dokümanlar root’ta **kalıcı** yer almaz; archive’a taşınır.

---

## 2. Kök dizin (root) kuralları

### 2.1 Root’ta bulunabilecek dosyalar (izin listesi)

Sadece aşağıdaki kategorilerde ve isimlendirmeyle dosya **root’ta** tutulur. README “Current documentation” bölümü **yalnızca** bu dosyalara link verir.

| Kategori | Dosya(lar) | Açıklama |
|----------|------------|----------|
| **Release & verification** | `GITHUB_RELEASES_GUIDE.md`, `RELEASE_VERIFICATION_CHECKLIST.md`, `TAG_GOVERNANCE.md`, `ECOSYSTEM_CONTRACT_MATRIX.md` | Release süreci ve invariant doğrulama |
| **CI & operations** | `CI_RELIABILITY.md` | CI flakiness ve çözümler |
| **Governance** | `BRANCH_GOVERNANCE.md` | Branch kuralları; dev vs CI fallback |
| **Mimari & rehber** | `ARCHITECTURE.md`, `FORMULAS.md`, `INTEGRATION_GUIDE.md` | Ekosistem mimarisi, formüller, entegrasyon (DOC TRIO referansı) |
| **Roadmap & durum** | `NEXT_STEPS_ROADMAP.md`, `TASK_COMPLETION_SUMMARY.md` | Tek “ileride ne var” + tek “ne bitti” özeti |
| **Analiz (güncel)** | En fazla **1–2** “current” analiz raporu (örn. `ACADEMIC_STATIC_ANALYSIS_REPORT.md` veya `ECOSYSTEM_QA_STATIC_ANALYSIS_REPORT.md`) | Eski raporlar archive’a taşınır |
| **Meta** | `README.md`, `DOCS_REPO_STRUCTURE.md` (bu dosya) | Repo tanımı ve bu standardın kendisi |

### 2.2 Root’ta olmaması gerekenler

- Oturum/session özetleri (örn. `SESSION_COMPLETE_SUMMARY.md`, `FINAL_SESSION_SUMMARY.md`)
- Tek seferlik migration/closure raporları (örn. `MIGRATION_SUMMARY.md`, `P0_CLOSURE_CHECKLIST.md`)
- Sprint/board dosyaları (örn. `P2_SPRINT_BOARD_*.md`, `P3_KICKOFF_CHECKLIST.md`) — tamamlandıktan sonra archive
- Tarihsel doğrulama snapshot’ları (örn. `FINAL_RELEASE_VERIFICATION.md`, `RELEASE_VERIFICATION_COMPLETE.md`) — sadece `archive/YYYY-MM-DD/` altında
- Kişisel/operasyonel notlar (örn. `TERMINAL_GITHUB_GIRIS.md`, `GIT_KIMLIK_KONTROL.md`, `REPO_YONETIMI_VE_KATKIDA_BULUNANLAR.md`) — isteğe bağlı `docs/operational/` veya archive
- Eski remediation/summary dosyaları (örn. `VERSION_BUMP_SUMMARY.md`, `EXECUTION_ORCHESTRATION_CORE_CREATED.md`) — archive

**Kural:** Yeni bir “özet” veya “rapor” yazıldığında: “Bu root’ta kalıcı mı?” sorusu sorulur. Kalıcı değilse `archive/YYYY-MM-DD/` altında açılır veya taşınır.

---

## 3. Klasör yapısı (standart)

```
decision-ecosystem-docs/
├── README.md                          # Giriş; sadece CURRENT + Archive linki
├── DOCS_REPO_STRUCTURE.md             # Bu standard (meta)
├── ARCHITECTURE.md                    # Ekosistem mimarisi
├── FORMULAS.md                        # Formüller / invariant referansı
├── INTEGRATION_GUIDE.md               # Entegrasyon rehberi
├── GITHUB_RELEASES_GUIDE.md
├── RELEASE_VERIFICATION_CHECKLIST.md
├── TAG_GOVERNANCE.md
├── ECOSYSTEM_CONTRACT_MATRIX.md
├── BRANCH_GOVERNANCE.md
├── CI_RELIABILITY.md
├── NEXT_STEPS_ROADMAP.md
├── TASK_COMPLETION_SUMMARY.md
├── [en fazla 1–2 güncel analiz raporu]
│
├── archive/                           # Tarihsel snapshot’lar
│   └── YYYY-MM-DD/                    # Tarih bazlı (örn. 2026-02-17)
│       ├── README.md                  # O tarih için içerik özeti
│       └── *.md                       # O güne ait raporlar/özetler
│
├── docs/                              # Opsiyonel: ek teknik doküman
│   └── [ör. STATIC_ANALYSIS_REMEDIATION_*.md]
│
└── examples/                          # Domain örnekleri rehberi (varsa)
    └── README.md
```

### 3.1 Archive kuralı (INV-DOC-2)

- **archive/YYYY-MM-DD/** = Belirli bir tarihe ait snapshot’lar (release verification, session summary, migration raporu vb.).
- README’de “Archive” bölümü sadece `archive/` alt dizinlerine link verir; root’ta “Final Release Verification” gibi eski tek dosya **kalmaz**.
- Yeni tarihli snapshot için yeni klasör: `archive/2026-02-19/` gibi.

### 3.2 Root’ta “Analysis & reports”

- README’de listelenen “Analysis & reports” **en fazla 1–2** güncel rapor olsun.
- Yeni analiz raporu eklendiğinde, eski olan `archive/YYYY-MM-DD/` altına taşınır (veya silinmez, sadece README linki kaldırılır ve dosya archive’a taşınır).

---

## 4. İsimlendirme kuralları

| Tür | Kural | Örnek |
|-----|--------|--------|
| Governance / süreç | `BÜYÜK_HARF_SNAKE_CASE.md` | `RELEASE_VERIFICATION_CHECKLIST.md` |
| Tek tarihli snapshot | `archive/YYYY-MM-DD/` içinde, anlamlı isim | `FINAL_RELEASE_VERIFICATION.md` |
| Analiz raporu | Açıklayıcı, tek tip | `ACADEMIC_STATIC_ANALYSIS_REPORT.md` |
| Yeni rapor eklerken | Root’u şişirmemek; mümkünse archive | `archive/2026-02-19/STATIC_ANALYSIS_P0_P1_APPLIED.md` |

---

## 5. README ile uyum (INV-DOC-1)

- README “Current documentation” bölümü **sadece** bu standarda uyan root dosyalarını listeler.
- “Archive” bölümü sadece `archive/YYYY-MM-DD/` gibi dizinlere link verir.
- Eski veya tekrarlayan dokümanlar README’den çıkarılır (dosya archive’da kalabilir).

---

## 6. Özet (tek cümle)

**Root = sadece yaşayan, tek kaynak dokümanlar; oturum özetleri, migration raporları ve tarihsel snapshot’lar `archive/YYYY-MM-DD/` altında.**

---

## 7. Mevcut dosyaların sınıflandırması (uygulama rehberi)

Standarda göre root’ta **kalması gerekenler** ve **archive’a taşınacaklar** aşağıda. Taşıma yapılırken `archive/2026-02-19/` (veya ilgili tarih) kullanılabilir.

### Root’ta kalsın (CURRENT)

| Dosya | Sebep |
|-------|--------|
| `README.md` | Meta |
| `DOCS_REPO_STRUCTURE.md` | Bu standard |
| `ARCHITECTURE.md`, `FORMULAS.md`, `INTEGRATION_GUIDE.md` | DOC TRIO referansı |
| `GITHUB_RELEASES_GUIDE.md`, `RELEASE_VERIFICATION_CHECKLIST.md`, `TAG_GOVERNANCE.md`, `ECOSYSTEM_CONTRACT_MATRIX.md` | Release & verification |
| `BRANCH_GOVERNANCE.md` | Governance |
| `CI_RELIABILITY.md` | CI & operations |
| `NEXT_STEPS_ROADMAP.md`, `TASK_COMPLETION_SUMMARY.md` | Roadmap & durum |
| `ACADEMIC_STATIC_ANALYSIS_REPORT.md`, `ECOSYSTEM_QA_STATIC_ANALYSIS_REPORT.md` | En fazla 2 analiz (güncel) |
| `TAG_ALIGNMENT_COMPLETE.md` | Tarihsel not ile uyumlu; isteğe bağlı archive’a taşınabilir |

### Archive’a taşınsın (archive/2026-02-19 veya uygun tarih)

| Dosya | Önerilen hedef |
|-------|-----------------|
| `SESSION_COMPLETE_SUMMARY.md`, `FINAL_SESSION_SUMMARY.md`, `RELEASE_COMPLETE_SUMMARY.md` | archive/YYYY-MM-DD/ |
| `MIGRATION_SUMMARY.md`, `FINAL_MIGRATION_STATUS.md`, `BRANCH_MIGRATION_COMPLETE.md`, `BRANCH_MIGRATION_FINAL_STATUS.md`, `INTEGRATION_HARNESS_BRANCH_MIGRATION.md` | archive/ |
| `P0_CLOSURE_CHECKLIST.md`, `P2_SPRINT_BOARD_*.md`, `P3_*.md`, `P2_GITHUB_ISSUE_PACK.md` | archive/ |
| `VERSION_BUMP_SUMMARY.md`, `EXECUTION_ORCHESTRATION_CORE_CREATED.md`, `WORKFLOW_RUN_DELETION_SAFE.md`, `CI_MASTER_BRANCH_LEGACY_RUNS.md`, `CI_WORKFLOW_MASTER_BRANCH_ISSUE.md` | archive/ |
| `REMOTE_VERIFICATION_*.md`, `INTEGRATION_HARNESS_CASE_SENSITIVITY_FIX.md` | archive/ |
| `STATIC_ANALYSIS_FIXES_REPORT.md` | archive/ (veya docs/; güncel analiz 2 tane kalınca üçüncüsü archive) |
| `AUDIT_REMEDIATION_PLAN.md` | archive/ veya docs/ |
| `TERMINAL_GITHUB_GIRIS.md`, `GIT_KIMLIK_KONTROL.md`, `REPO_YONETIMI_VE_KATKIDA_BULUNANLAR.md` | archive/ veya docs/operational/ |
| `ECOSYSTEM_ROADMAP_AND_RECOMMENDATIONS.md` | İçerik NEXT_STEPS_ROADMAP ile birleştirilip tek roadmap kalabilir; eski sürüm archive’a |

Taşıma sonrası README “Current documentation” bölümünden kaldırılan dosyaların linkleri silinir; Archive bölümüne ilgili `archive/YYYY-MM-DD/` linki eklenir. Geçici taşıma planı `archive_move_plan_2026-02-19.txt` taşıma tamamlanınca silinir veya archive’a alınır (allowlist’te değildir).

---

## 8. Invariant kapıları (CI’da kanıtlanabilir)

Root ve README kuralları CI ile zorunlu tutulur. Tek kaynak: `ROOT_ALLOWLIST.txt` (CI script bu listeyi okur).

| Invariant | Kural | Metrik |
|-----------|--------|--------|
| **INV-DOC-ROOT-ALLOW-1** | Root’ta yalnız allowlist dosyaları + `.github/`, `archive/`, `docs/`, `examples/` | root_non_allowed_count == 0 |
| **INV-DOC-ARCHIVE-SNAPSHOT-1** | `archive/` altında sadece `YYYY-MM-DD/` formatında dizin | regex dışı klasör sayısı 0 |
| **INV-DOC-README-CURRENT-1** | README “Current documentation” yalnız root allowlist’teki dosyalara link verir | root dışı link 0 |
| **INV-DOC-ANALYSIS-LIMIT-1** | Root’ta en fazla 2 analiz/rapor dosyası (`*_REPORT.md`, `*_ANALYSIS*.md`) | analysis_report_count ≤ 2 |

- **Workflow:** `.github/workflows/docs_structure_guard.yml` (push/PR to `main`).
- **Script:** `.github/scripts/check_docs_root.py` (allowlist, archive path, README linkler, analiz sayısı).
- Allowlist’i güncellerken `ROOT_ALLOWLIST.txt` düzenlenir; script bu dosyayı tek kaynak kabul eder.

---

## 9. Arşiv taşıma operasyonu

Tablo (§7) tek kaynaktır. Taşıma iki şekilde yapılabilir:

- **Seçenek A (elle):** `git checkout -b chore/archive-YYYY-MM-DD`, `mkdir -p archive/YYYY-MM-DD`, sonra her dosya için `git mv <dosya> archive/YYYY-MM-DD/`.
- **Seçenek B (plan dosyası):** `archive_move_plan_YYYY-MM-DD.txt` içinde satır formatı `SOURCE -> archive/YYYY-MM-DD/SOURCE`. Sonra:
  - `python .github/scripts/run_archive_move_from_plan.py archive_move_plan_2026-02-19.txt`
  - Taşıma bitince plan dosyası silinir veya archive’a alınır (root allowlist’te değildir).

Taşıma sonrası `python .github/scripts/check_docs_root.py` ile invariant’lar doğrulanır; CI yeşil olmalıdır.
