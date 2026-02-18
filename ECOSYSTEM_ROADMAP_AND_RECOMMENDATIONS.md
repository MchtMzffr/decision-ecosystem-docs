# Decision Ecosystem — Geliştirme Önerileri ve Yol Haritası

Bu belge, ekosistemi geliştirmek için **yeni çekirdek önerileri**, **mevcut çekirdeklerde iyileştirmeler** ve **altyapı/tooling** fikirlerini içerir. Hepsi domain-agnostic ve contract-first prensiplere uygun olacak şekilde tasarlanmıştır.

---

## 1. Yeni Çekirdek Önerileri

### 1.1 **execution-orchestration-core** (Öncelik: Yüksek)

**Amaç:** FinalDecision’ı gerçek dünyada “çalıştırma” katmanı.

- **Girdi:** `FinalDecision`, execution context
- **Çıktı:** Execution result, PacketV2 güncellemesi (latency, outcome)
- **Sorumluluklar:**
  - Action’ı domain-agnostic bir executor arayüzüne yönlendirme
  - Retry/backoff, timeout, idempotency (generic)
  - Execution trace’i PacketV2’ye ekleme
- **Neden:** Şu an “execute” kısmı her domain’de ayrı yazılıyor; ortak bir orchestration katmanı tekrarı azaltır ve trace bütünlüğünü garanti eder.

**Contract genişlemesi:** `decision-schema`’ya (opsiyonel) `ExecutionResult` veya PacketV2’ye `execution` alanı eklenebilir.

---

### 1.2 **explainability-audit-core** (Öncelik: Orta)

**Amaç:** Kararların “neden”ini audit ve compliance için açıklanabilir hale getirmek.

- **Girdi:** PacketV2 trace’leri, opsiyonel olarak Proposal/FinalDecision + context
- **Çıktı:** Açıklama artefaktları (metin, yapısal nedenler, guard chain)
- **Sorumluluklar:**
  - Proposal’ın hangi sinyaller/özelliklerle üretildiğinin özeti
  - Hangi guard’ların tetiklendiği / geçtiği
  - Domain-agnostic “reason codes” → insan okunabilir cümleler (template tabanlı)
- **Neden:** Regülasyon ve insan-in-the-loop senaryolarında “neden bu karar?” sorusuna tek yerden cevap verir.

**Contract:** Sadece PacketV2 ve mevcut `reasons`/`mismatch` kullanılır; yeni tip gerekmez.

---

### 1.3 **policy-config-core** (Öncelik: Orta)

**Amaç:** Guard eşikleri, risk politikaları ve ops-health parametrelerinin merkezi, versiyonlu yönetimi.

- **Girdi:** Policy tanımları (JSON/YAML), ortam etiketleri (env, region, tenant)
- **Çıktı:** Cores’a verilecek policy objeleri (RiskPolicy, OpsPolicy vb.)
- **Sorumluluklar:**
  - Policy versioning, rollback
  - Ortama göre farklı policy setleri (canary, production)
  - Validation: decision-schema ile uyumlu parametre isimleri
- **Neden:** Politikalar dağılmak yerine tek yerden yönetilir; deney ve kalibrasyon ile uyumlu olur.

**Contract:** decision-schema’da sadece tipler var; policy şeması bu çekirdekte tanımlanır ve schema’daki isimlerle uyumlu tutulur.

---

### 1.4 **drift-detection-core** (Öncelik: Orta–Düşük)

**Amaç:** Zaman içinde input dağılımı veya model/guard davranışındaki kaymayı tespit.

- **Girdi:** PacketV2 akışı veya periyodik özetler
- **Çıktı:** Drift sinyalleri (feature drift, outcome drift, guard trigger rate drift)
- **Sorumluluklar:**
  - Basit istatistiksel drift (ör. dağılım farkı, oran değişimi)
  - Alarm/event üretimi (ops-health veya monitoring’e beslenebilir)
- **Neden:** Model ve politika zamanla eskiyor; erken drift tespiti kalibrasyon ve güvenlik için kritik.

**Contract:** Sadece PacketV2; ek alan gerekmez.

---

### 1.5 **human-in-the-loop-core** (Öncelik: Orta)

**Amaç:** Belirli koşullarda kararı insana devretme ve insan cevabını tekrar sisteme işleme.

- **Girdi:** FinalDecision, context, escalation policy (örn. confidence < X → escalate)
- **Çıktı:** Onaylanmış/reddedilmiş karar, gecikme süresi, PacketV2’ye human_override alanı
- **Sorumluluklar:**
  - Escalation kuralları (domain-agnostic: confidence, guard flags, custom rules)
  - İnsan arayüzü ile entegrasyon için event/API (generic)
  - Timeout’ta fail-closed (örn. HOLD)
- **Neden:** Yüksek riskli domain’lerde (tıbbi triage, moderasyon) “machine suggests, human confirms” pattern’i için standart katman sağlar.

**Contract:** PacketV2’ye opsiyonel `human_override`, `escalation_reason` gibi alanlar eklenebilir (minor, geriye dönük uyumlu).

---

## 2. Mevcut Çekirdeklerde İyileştirmeler

### 2.1 decision-schema

- **PacketV2 genişletmesi:** `execution` (execution-orchestration), `explainability` (explainability-audit), `human_override` (human-in-the-loop) için opsiyonel alanlar; hepsi backward-compatible (yoksa yok say).
- **PARAMETER_INDEX:** Yeni çekirdekler eklendikçe güncellenmeli.
- **ECOSYSTEM_CONTRACT_MATRIX:** Her yeni core için min/max schema sürümü ve “known-good” kombinasyonları eklenmeli.

### 2.2 mdm-engine

- **propose() API:** Zaten var; tüm dokümantasyon ve örneklerin `propose()` + PacketV2 odaklı olduğundan emin ol.
- **Profil/preset:** Farklı güvenlik seviyeleri için (low/medium/high) hazır parametre setleri (policy-config-core ile uyumlu).

### 2.3 decision-modulation-core

- **Guard registry:** Yeni guard’ların plug-in şeklinde eklenebilmesi; sıra determinism korunmalı.
- **Policy-config-core:** RiskPolicy’nin bu çekirdekten dışarı alınıp policy-config-core’dan beslenmesi (opsiyonel refactor).

### 2.4 ops-health-core

- **Sinyal çeşitliliği:** Latency, error rate dışında generic “saturation”, “backpressure” gibi sinyaller (formüller FORMULAS.md’de).
- **drift-detection-core:** Drift alarmları ops-health context’ine beslenerek kill-switch veya throttle tetiklenebilir.

### 2.5 evaluation-calibration-core

- **Calibration loop:** Metrikler + drift sinyalleri ile policy parametrelerinin otomatik önerisi (policy-config ile entegre).
- **Report şablonları:** JSON/MD dışında SLA/regülasyon odaklı rapor şablonları (domain-agnostic alanlarla).

---

## 3. Altyapı ve Tooling

### 3.1 **decision-ecosystem-cli** (monore veya ayrı repo)

- Tüm çekirdeklerin tek komutla kurulması (`decision-ecosystem install`).
- Lokal test pipeline: schema uyumluluğu, invariant testleri, örnek trace ile uçtan uca koşum.
- Contract matrix doğrulama: Pin’lenen schema sürümleri ile core’ların uyumluluğunu kontrol.

### 3.2 **Trace storage ve replay**

- PacketV2 JSONL’ı için ortak bir “trace store” arayüzü (dosya, S3, blob vb. backend’ler plug-in).
- Replay: Aynı trace’i farklı policy/guard seti ile tekrar çalıştırma (evaluation-calibration ve A/B test için).

### 3.3 **Compliance ve test**

- **INVARIANT 0 testi:** Tüm repo’larda domain-terim taraması (decision-schema’daki test örnek alınabilir).
- **Compat gate:** Her core’un başlangıçta `decision_schema.compat.is_compatible` çağırdığından emin olma; CI’da farklı schema sürümleri ile test.

---

## 4. Öncelik Sıralaması (Kısa Vadeli)

| Sıra | Öneri | Etki | Effort |
|------|--------|------|--------|
| 1 | execution-orchestration-core (skeleton + doc trio) | Yüksek | Orta |
| 2 | explainability-audit-core (skeleton + doc trio) | Yüksek | Orta |
| 3 | decision-ecosystem-cli (install + smoke test) | Orta | Düşük |
| 4 | policy-config-core (skeleton + doc trio) | Orta | Orta |
| 5 | human-in-the-loop-core (skeleton + doc trio) | Orta | Orta |
| 6 | drift-detection-core (skeleton + doc trio) | Orta | Orta |

---

## 5. Yeni Çekirdek Eklerken Uyulacak Kurallar

1. **Sadece decision-schema’ya bağımlılık;** diğer core’lara import yok.
2. **DOC TRIO:** Her yeni repo’da `docs/ARCHITECTURE.md`, `docs/FORMULAS.md`, `docs/INTEGRATION_GUIDE.md` zorunlu.
3. **Domain-agnostic:** İsimler ve ana anlatı tek bir endüstriye (örn. trading) bağlı olmamalı.
4. **Fail-closed:** Hata durumunda güvenli varsayılan (HOLD/STOP veya boş rapor).
5. **SemVer + ECOSYSTEM_CONTRACT_MATRIX:** Yeni core için min/max schema sürümü dokümante edilmeli.

---

## 6. Özet

- **Yeni çekirdekler:** execution-orchestration, explainability-audit, policy-config, drift-detection, human-in-the-loop — hepsi contract-first ve domain-agnostic.
- **Mevcut çekirdekler:** Guard registry, policy dışarı alma, calibration loop, PARAMETER_INDEX ve contract matrix güncellemeleri ile güçlendirilebilir.
- **Tooling:** CLI (install + smoke), trace store arayüzü, invariant ve compat testleri ekosistemi production’a taşımak için önemli.

İstersen bir sonraki adımda **execution-orchestration-core** veya **explainability-audit-core** için doğrudan README + doc trio stub’ları ve repo iskeletini çıkaracak bir plan da yazabilirim.
