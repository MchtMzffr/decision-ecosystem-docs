# Decision Ecosystem — Akademik QA İncelemesi (Statik Analiz)

Bu değerlendirme **yalnızca statik kod ve doküman incelemesine** dayanır (çalıştırma/test yok). Tüm core repolar ve integration harness kapsanmıştır.

**P0 kapanış durumu:** P0 (version single-source + INTEGRATION_GUIDE pin + INV-V1 + P0.5-A schema pin) DONE; drift_count=0; tüm repolarda testler geçiyor (INV-V1 + schema pin minor=2). P0.5-B (harness version): `__version__` sabit tutuldu; isteğe bağlı ileride `importlib.metadata.version(...)` ile tek kaynak yapılabilir.

---

## 1) Terminoloji Haritası (Ekosistem)

| Terim | Anlam | SSOT / Kullanım |
|-------|--------|------------------|
| **decision-schema** | Kontrat SSOT: Action, Proposal, FinalDecision, PacketV2, compat | decision_schema.types, .packet_v2, .compat |
| **Proposal** | Önerilen aksiyon + güven + gerekçeler | decision_schema.types.Proposal |
| **FinalDecision** | DMC sonrası yürütülecek nihai aksiyon | decision_schema.types.FinalDecision |
| **PacketV2** | İzleme/telemetri çıktısı (trace) | decision_schema.packet_v2.PacketV2 |
| **MDM** | Proposal üreten çekirdek motor | mdm-engine (DecisionEngine) |
| **DMC** | Risk/modülasyon katmanı (GuardPolicy, modulate) | decision-modulation-core |
| **Ops-health** | Kill-switch, cooldown, ops_deny_actions | ops-health-core |
| **Fail-closed** | Hata durumunda güvenli davranış (HOLD/STOP) | Tüm core’larda |
| **GuardPolicy** | DMC policy (domain-agnostic) | dmc_core.dmc.policy.GuardPolicy |
| **RiskPolicy** | Legacy/example isim; core’da GuardPolicy kullanılır | docs/examples, PARAMETER_INDEX (drift) |

**Terminolojik olgunluk (ekosistem):** 7.8/10 — Temel kavramlar net; doküman–kod ve repo’lar arası sürüm/kapsam drift’leri var.

---

## 2) Repo Bazlı Yapısal Skor Kartı

| Repo | Modülerlik | Kontrat-first | Doküman↔Kod | Sürüm tutarlılığı | Test/gate | Genel |
|------|------------|---------------|-------------|--------------------|-----------|--------|
| **decision-schema** | 9.0 | 9.0 | 7.5 | 6.0 (pyproject≠version.py) | 8.5 | 7.8 |
| **decision-modulation-core** | 8.5 | 8.5 | 6.0 | 8.0 | 8.0 | 7.7 |
| **ops-health-core** | 8.0 | 8.5 | 8.0 | 8.0 | 7.5 | 8.0 |
| **evaluation-calibration-core** | 8.0 | 8.5 | 8.0 | 8.0 | 8.0 | 8.1 |
| **mdm-engine** | 8.5 | 8.8 | 5.5 | 5.0 (pyproject≠__init__) | 7.5 | 7.8 |
| **integration-harness** | 8.0 | 9.0 | 7.0 | 8.0 | 8.0 | 8.0 |

**Ekosistem bileşik skor:** 7.8/10

---

## 3) Güçlü Yanlar (Ekosistem)

- **Kontrat odaklı mimari:** decision-schema SSOT; tüm core’lar `>=0.2,<0.3` pin ile uyumlu.
- **İnvariant test kültürü:** CI-0, INV0, INV2, PKG-1/2; domain-agnosticism ve cross-core import yasağı testli.
- **Harness kanıt zinciri:** core_only / full_stack job’lar, skip=0, P2_DONE_EVIDENCE ile point-in-time kanıt.
- **Güvenlik temelleri:** redaction, audit, kill-switch fail-closed, DMC guard determinism.
- **Private hook / opsiyonel core’lar:** mdm-engine private model; harness optional import ile core-only çalışabiliyor.

---

## 4) Kritik Bulgular ve Önerilen Görevler

### decision-schema

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| DS-1 | **pyproject.toml** `version = "0.1.0"`, **decision_schema/version.py** `__version__ = "0.2.0"` — tek kaynak yok. | Tekil sürüm kaynağı: pyproject’i 0.2.0 yap veya version.py’yi pyproject’ten okuyacak şekilde senkronize et. |
| DS-2 | README’de `ECOSYSTEM_CONTRACT_MATRIX.md` referansı var; matrix root dosyada ve 0.2.x pin ile uyumlu; ancak “Release block” (released versions, deprecation timeline) bölümü eksik. | P3-S2: `ECOSYSTEM_CONTRACT_MATRIX.md` (root) içine “Released versions” + deprecation timeline ekle. |

### decision-modulation-core (dmc-core)

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| DMC-1 | **PARAMETER_INDEX.md** ve **docs/examples** `RiskPolicy` / `dmc_core.dmc.risk_policy.RiskPolicy` referans veriyor; core API **GuardPolicy** (dmc_core.dmc.policy). | PARAMETER_INDEX ve ilgili dokümanları GuardPolicy ile hizala; RiskPolicy’yi “legacy/example only” olarak işaretle. |
| DMC-2 | README “MeetlyTR” git URL; ekosistem **MchtMzffr** kullanıyor olabilir. | README’deki git URL’leri ekosistemle (ve varsayılan remote) uyumlu hale getir. |
| DMC-3 | DOC TRIO drift: `docs/FORMULAS.md` eksik veya bulunamıyor; README de core API yerine legacy terimlere kayabiliyor. | `docs/FORMULAS.md` ekle (domain-free guard/composition formülleri) ve README’yi GuardPolicy/modulate ile hizala. |

### ops-health-core

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| OPS-1 | README “MeetlyTR” git URL. | Git URL’leri ekosistemle uyumlu hale getir. |

### evaluation-calibration-core

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| EVAL-1 | README “from eval_calibration_core.report import build_report” — doğru; fakat “report.save_json” / “report.save_markdown” kullanımı: API’de `write_report(report, path)` var. | README örneğini `write_report(report, Path("output"))` ile hizala (save_* yerine). |
| EVAL-2 | README “MeetlyTR” git URL. | Git URL’leri ekosistemle uyumlu hale getir. |

### mdm-engine

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| MDM-1 | **docs/INTEGRATION_GUIDE.md** `decision-schema>=0.1,<0.2` ve `min_minor=1,max_minor=1`; repo **0.2,<0.3** kullanıyor. | INTEGRATION_GUIDE’ı decision-schema 0.2 kontratıyla hizala (>=0.2,<0.3, min_minor=2, max_minor=2). |
| MDM-2 | **README** `mdm_engine/features/feature_builder.py` ve event-loop referansları; features/loop paketten çıkarıldı (docs/examples/.../mdm_engine_legacy). | README’deki kaldırılmış/taşınmış modül referanslarını temizle; Quick Start’ı features olmadan (state→features passthrough) güncelle. |
| MDM-3 | **pyproject.toml** `version = "0.2.0"`, **mdm_engine/__init__.py** `__version__ = "0.1.0"`. | Tekil sürüm kaynağı oluştur; __version__’ı 0.2.0 ile senkronize et. |
| MDM-4 | **redaction.py**: `redact_dict` içinde her anahtar için normalize key set yeniden üretiliyor; büyük payload’ta gereksiz maliyet. | Normalize edilmiş anahtar kümesini döngü dışında bir kez hesapla / önbellekle. |
| MDM-5 | **RateLimiter** `tokens` varsayılan 0.0; ilk çağrıda beklenmedik deny riski. Çoğu token-bucket impl başlangıçta capacity dolu. | RateLimiter başlangıç token politikasını açıkla ve (isteğe bağlı) capacity ile başlatma seçeneği ekle veya dokümante et. |

### decision-ecosystem-integration-harness

| # | Bulgu | Önerilen görev |
|---|--------|-----------------|
| H-1 | README “H4: Fail-closed propagation” listeleniyor; testlerde **H4** yok (H1, H2, H3 + fullstack e2e var). | README invariant listesini mevcut testlerle eşleştir (H4’ü kaldır veya H4 testi ekle). |
| H-2 | **Nested redaction riski:** `redaction` mantığı iç içe yapılarda sızıntı üretebilir (statik inceleme bulgusu). | `harness/redaction.py` nested yapıları deterministik şekilde redakte edecek biçimde düzelt + test ekle (`nested dict` içinde secret key redacted). |
| H-3 | README “H4: Fail-closed propagation” listeleniyor; fakat test seti / uygulama buna birebir karşılık gelmeyebilir (H1/H2/H3 + fullstack E2E var). | Ya README’de H4’ü “planned” diye işaretle **ya da** H4’ü gerçek bir invariant testiyle uygula (exception → FinalDecision deny + HOLD + Packet işareti). |

---

## 5) Özet Tablo — Sürüm ve Kontrat Drift

| Repo | pyproject version | Paket __version__ | decision-schema pin | Doküman schema örneği |
|------|-------------------|-------------------|----------------------|------------------------|
| decision-schema | 0.1.0 | 0.2.0 (version.py) | — | 0.2.x (README) |
| dmc-core | 0.1.0 | 0.1.0 | >=0.2,<0.3 | GuardPolicy ok |
| ops-health-core | 0.1.0 | 0.1.0 | >=0.2,<0.3 | — |
| eval-calibration-core | 0.1.0 | 0.1.0 | >=0.2,<0.3 | >=0.2,<0.3 ok |
| mdm-engine | 0.2.0 | 0.1.0 | >=0.2,<0.3 | 0.1,<0.2 (INTEGRATION_GUIDE) |
| harness | 0.1.0 | — | >=0.2,<0.3 | 0.2.x ok |

---

## 6) Sonuç (Akademik Değerlendirme)

Ekosistem **kontrat-merkezli ve domain-agnostic** hedefte olgun bir yönelime sahip. En büyük kalite açığı **doküman–kod senkronizasyonu** ve **sürüm tek kaynağı** eksikliği:

- **Sürüm:** decision-schema ve mdm-engine’de pyproject ↔ __version__ uyumsuzluğu.
- **Doküman:** mdm-engine INTEGRATION_GUIDE eski kontrat; README taşınan modüllere referans; DMC’de RiskPolicy vs GuardPolicy; harness README H4.
- **Kod:** mdm-engine redaction önbellek, RateLimiter başlangıç politikası (küçük iyileştirmeler).

Bu gap’ler kapatıldığında akademik tutarlılık ve release güvenilirliği belirgin biçimde artar.

---

## 7) Yapılacaklar Listesi (Öncelik Sırasıyla)

Aşağıdaki liste, bulguların **ölçülebilir, tek commit’e uygun** görevlere dönüştürülmüş halidir.

### P0 — Release güveni ve tekil sürüm kaynağı (hemen)

1. **decision-schema:** `pyproject.toml` `version` değerini `decision_schema/version.py` ile aynı olacak şekilde senkronize et (tek kaynak).
2. **mdm-engine:** `mdm_engine/__init__.py` içindeki `__version__` değerini `pyproject.toml` ile senkronize et (tek kaynak).
3. **mdm-engine:** `docs/INTEGRATION_GUIDE.md` — dependency `decision-schema>=0.2,<0.3`, compat `min_minor=2, max_minor=2` olacak şekilde güncelle; taşınmış modül referanslarını kaldır (state→features passthrough örneği).
4. **(Yeni, ekosistemsel kilit) INV-V1:** Tüm repolara “version single-source” invariant testi ekle: `pyproject version == package __version__` (varsa `version.py` dahil). Drift tekrar oluşursa CI kırmızı.

### P1 — Doküman–kod senkronizasyonu (public narrative)

5. **mdm-engine:** `README.md` — taşınan/kaldırılan modüllere (`features/`, loop, legacy) referansları kaldır; core API (DecisionEngine + domain-free features dict) ile Quick Start’ı güncelle.
6. **decision-modulation-core:**
   - README’yi **GuardPolicy + modulate** eksenine çek; `RiskPolicy` sadece “legacy/example only” olarak işaretlensin.
   - `docs/INTEGRATION_GUIDE.md` dilini “integration layer records trace into PacketV2.external/context” şeklinde netleştir (core Packet yazmaz).
   - `docs/FORMULAS.md` ekle (DOC TRIO kapanışı; domain-free formüller).
7. **ops-health-core:** README’deki install/git URL’lerini ekosistemle uyumlu hale getir (owner/remote drift).
8. **evaluation-calibration-core:** README’de report örneğini gerçek API ile hizala (örn. `build_report` + `write_report`); install/git URL drift’i düzelt.
9. **integration-harness:** README’de “invariant listesi”ni mevcut test setiyle birebir eşleştir: H4 ya “planned” olarak işaretlensin ya da P2’deki H4 testi eklensin.

### P2 — Güvenlik + küçük ama kritik kod hijyeni

10. **integration-harness:** `harness/redaction.py` — nested redaction davranışını deterministik hale getir + unit test ekle (nested dict içinde secret key her durumda redacted).
11. **integration-harness (H4):** Fail-closed propagation’ı gerçek invariant yap: `run_one_step` içinde exception → `FinalDecision(allowed=False, action=HOLD)` + Packet’ta fail-closed işareti; `tests/test_invariant_h4_fail_closed_propagation.py` ekle (monkeypatch ile exception üret).
12. **mdm-engine:** `redaction.py` — normalize key set’i döngü dışında hesapla/önbellekle (büyük payload maliyeti düşür).
13. **mdm-engine:** `rate_limit.py` — RateLimiter başlangıç token semantiğini dokümante et; opsiyonel olarak “initial_tokens”/“start_full” gibi açık bir politika ekle veya default’u netleştir.

### P3 — Release/matrix disiplini (ekosistem uzun vadeli)

14. **decision-schema:** `ECOSYSTEM_CONTRACT_MATRIX.md` (root) içine “Released versions” + deprecation timeline bloğu ekle (P3-S2).

---

**Toplam:** 14 net görev.
P0 (1–4) tamamlanınca sürüm drift’i CI ile kilitlenir; P1 (5–9) public narrative’ı kodla hizalar; P2 (10–13) güvenlik ve runtime hijyenini güçlendirir; P3 (14) release disiplinini tamamlar.
