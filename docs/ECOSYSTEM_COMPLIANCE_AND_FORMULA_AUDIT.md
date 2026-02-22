# Decision Ecosystem — Uyumsuzluk, Güvenlik, Eksiklik ve Formül Tutarlılık Raporu

**Amaç:** Workspace erişimi ile kod, dokümantasyon ve genel yapının akademik düzeyde incelenmesi; uyumsuzluk, güvenlik açığı, eksiklik ve matematik/fizik formüllerinde tutarsızlık tespiti.  
**Format:** deep-research-report.md ile uyumlu (yönetici özeti, kapsam, bulgular, tablolar, invariant, patch planı).  
**Tarih:** 2026-02.

---

## 1. Yönetici özeti

Bu rapor, Decision Ecosystem workspace’inde (decision-ecosystem-docs + 6 core + harness + experimental) **birincil kaynak (kod + doküman)** üzerinden yapılan incelemeye dayanmaktadır. Depo erişimi mevcuttur; tüm bulgular dosya/satır bazında doğrulanabilir.

**Özet sonuçlar:**

| Kategori | Durum | Özet |
|----------|--------|------|
| **Uyumsuzluk (kod↔doküman)** | Hafif | ops-health doc’ta threshold adları (yellow_threshold/red_threshold) ile kod (score_threshold_yellow/red) aynı semantiği taşıyor; tek potansiyel sayısal risk: `max_p95_latency_ms = 0` ile bölme. |
| **Güvenlik** | Orta | CI’da `permissions: contents: read` ve secret_scan var; SECURITY.md 4 repoda eksik; CONTRIBUTING.md yok; SBOM/Scorecard yok. |
| **Eksiklik** | Orta | SECURITY.md (docs, exec-orch, harness, explainability); CONTRIBUTING.md (tüm repolar); coverage threshold; ops-health’ta sıfıra bölme koruması. |
| **Matematik/fizik formülleri** | Tutarlı | ops-health ve mdm-engine formülleri doküman ile kod uyumlu; ağırlık toplamları 1; confidence [0,1] clamp; tek açık nokta: genel notasyonlarda σ=0 veya payda 0 koruması (eval FORMULAS genel notasyon). |

**Önceliklendirme (erişim mevcut):**

- **P0:** ops-health scorer’da `max_p95_latency_ms == 0` iken sıfıra bölme riski (defensive check).
- **P1:** SECURITY.md (4 repo), CONTRIBUTING.md (en azından docs + core’lar), formül dokümanlarında “payda ≠ 0” notu.
- **P2:** SBOM/Scorecard, coverage threshold, DMC/eval genel notasyon formüllerinde edge-case notları.

---

## 2. İnceleme kapsamı ve yöntem

**Kapsam:** Kaynak ağaç yapısı, bağımlılık manifestleri, CI, lint/format, **formül içeren modüller** (ops-health scorer, mdm reference model, DMC modulator, eval invariants), lisans/güvenlik dosyaları, invariant dokümanları.

**Yöntem:** Kod ve ilgili FORMULAS.md / ARCHITECTURE.md karşılaştırması; formül sembollerinin (p_err, score, σ, ağırlıklar) kod ile bire bir eşleşmesi; bölme/edge-case kontrolü; CI permissions ve secret kullanımı taraması.

**Kısıt:** Sadece workspace’teki dosyalar; GitHub Issues/PR trafiği veya canlı ortam testi yok.

---

## 3. Uyumsuzluk bulguları (kod ↔ doküman)

### 3.1 ops-health-core: Health score formülü

**Doküman (docs/FORMULAS.md):**

```
p_err = min(1, errors/max_errors_per_window)
p_429 = min(1, rate_limit_events/max_429_per_window)
p_rec = min(1, reconnects/max_reconnects_per_window)
p_lat = min(1, max(0, (p95_latency - max_p95_latency_ms) / max_p95_latency_ms))
score = 1 - (w1*p_err + w2*p_429 + w3*p_rec + w4*p_lat)
```

**Kod (ops_health_core/scorer.py):**

- `p_err`, `p_429`, `p_rec`: `max_*_per_window > 0` ise bölme, else `0.0` — **dokümanla uyumlu ve sıfıra bölme korumalı.**
- `p_lat`: Yalnızca `p95_latency > policy.max_p95_latency_ms` iken hesaplanıyor; formül: `(p95_latency - max_p95_latency_ms) / max_p95_latency_ms`. **Eğer `max_p95_latency_ms == 0` ise payda sıfır → sıfıra bölme.**

**Varsayılan (model.py):** `max_p95_latency_ms: int = 1000`; normal kullanımda risk yok. Ancak politika programatik olarak 0 verilirse (örn. “latency kapalı”) hata oluşur.

**Sonuç:** **Uyumsuzluk değil, eksik savunma.** Doküman matematiksel formülü doğru yazıyor; kodda `max_p95_latency_ms == 0` için açık guard yok. Öneri: `if policy.max_p95_latency_ms <= 0: p_lat = 0.0` (veya dokümanda “max_p95_latency_ms > 0 olmalı” kısıtı).

### 3.2 mdm-engine: Reference model (generic numeric scorer)

**Doküman (mdm-engine/docs/FORMULAS.md):**

- `scale_score = min(1, scale_a/100)`; `signal_score = |s1|`; `width_penalty = min(1, max(0, 1 − scale_b/1000))`
- `raw_score = 0.4·scale_score + 0.4·signal_score + 0.2·width_penalty`
- `confidence = σ(5·(raw_score − 0.5))`, σ(x) = 1/(1+e^(-x))
- ACT ⇔ confidence ≥ threshold and |s1| ≥ signal_threshold

**Kod (reference_model_generic.py):**

- `scale_score = min(1.0, scale_a / 100.0) if scale_a else 0.0`
- `signal_score = abs(s1)`
- `width_penalty = min(1.0, max(0.0, 1.0 - (scale_b or 0) / 1000.0))`
- `raw_score = scale_score * 0.4 + signal_score * 0.4 + width_penalty * 0.2`
- `confidence = 1.0 / (1.0 + math.exp(-5.0 * (raw_score - 0.5)))`

**Sonuç:** **Tam uyumlu.** Ağırlıklar 0.4+0.4+0.2=1; sigmoid doğru; ACT koşulu kod ile aynı.

### 3.3 Ops-health ağırlık toplamı

**Kod (model.py):** `weight_errors=0.4`, `weight_429=0.3`, `weight_reconnects=0.2`, `weight_latency=0.1` → toplam 1.0.  
**Doküman:** “Weights: weight_errors, weight_429, weight_reconnects, weight_latency” — sayısal değer dokümanda yok; kod varsayılanları tutarlı. **Tutarsızlık yok.**

### 3.4 decision-schema: confidence clamp

**Kod (types.py):** `clamp_confidence(c) = max(0.0, min(1.0, c))`.  
**Invariant:** Tüm Proposal/FinalDecision confidence ∈ [0,1]. **Tutarlı.**

### 3.5 DMC: risk = Σ w·g ve modulation = 1 − risk

**Doküman (FORMULAS.md, decision-ecosystem-docs ve dmc-core):** “risk(d) = Σᵢ wᵢ·gᵢ(d) … **not the current implementation**; the core uses **ordered hard guards** only.”  
**Kod (modulator.py):** Sıralı guard’lar; ilk başarısız guard → fail-closed; ağırlıklı toplam yok. **Dokümanla uyumlu; tutarsızlık yok.**

---

## 4. Matematik ve fizik formülleri — akademik tutarlılık

### 4.1 Normalize edilmiş ceza ve skor (ops-health)

- **p_* ∈ [0, 1]:** `min(1, x/max_x)` ve `max(0, …)` kullanımı ile sağlanıyor; matematiksel tanım ile uyumlu.
- **score = 1 − (w1·p_err + … + w4·p_lat):** w toplamı 1 olduğu için skor teorik olarak [0, 1] aralığında; kod ek olarak `score = max(0.0, min(1.0, score))` ile sınırlıyor. **Bounded invariant karşılanıyor.**
- **Determinism:** Aynı state/policy/now_ms → aynı score; kodda rastgelelik yok. **Tutarlı.**

### 4.2 Sigmoid (mdm-engine)

- **σ(x) = 1/(1+e^(-x)):** Kod `1.0/(1.0+math.exp(-5.0*(raw_score-0.5)))` — doğru. σ ∈ (0,1). **Tutarlı.**
- **Sayısal kararlılık:** `raw_score` [0,1]’den geliyor; `5*(raw_score-0.5)` [-2.5, 2.5]; exp overflow/underflow riski pratikte yok. **Kabul edilebilir.**

### 4.3 Genel notasyon (eval / docs FORMULAS)

- **σ = √(E[(r_t - R̄)²]), SR = R̄/σ:** Dokümanda “general notation” ve “not computed by the core” deniyor. İleride uygulanırsa **σ=0 veya payda 0** durumu için tanım gerekir (örn. σ=0 iken SR tanımsız veya sabit kural). **Şu an kodda yok; dokümana edge-case notu eklenebilir.**
- **DD_t = max(0, peak_t - current_t):** Matematiksel olarak tutarlı; fiziksel bir birim zorunluluğu yok (domain-agnostic). **Tutarsızlık yok.**

### 4.4 Özet (formül)

| Konu | Doküman | Kod | Tutarlılık |
|------|---------|-----|------------|
| ops-health p_err, p_429, p_rec | min(1, x/max) | + sıfır payda guard | Evet |
| ops-health p_lat | max(0, (p95−max)/max) | max_p95==0 için guard yok | Eksik savunma |
| ops-health score, ağırlıklar | w1+…+w4, [0,1] | Toplam 1, clamp | Evet |
| mdm raw_score, σ | 0.4·scale+0.4·signal+0.2·width, σ(5·(r−0.5)) | Aynı | Evet |
| DMC ordered guards | “First failure → fail-closed” | modulator sıra + _fail_closed | Evet |
| Eval σ, SR (genel notasyon) | Formül verilmiş | Core hesaplamıyor | Edge-case notu önerilir |

---

## 5. Güvenlik bulguları

### 5.1 CI permissions

- **Kontrol edilen workflow’lar:** Tüm core’lar + harness + docs ci/docs_structure_guard.  
- **Bulgu:** `permissions: contents: read` (ör. mdm-engine/.github/workflows/ci.yml) — **INV-CI-PERM-1 ile uyumlu.** Varsayılan geniş yetki kullanılmıyor.

### 5.2 Secret kullanımı

- **GITHUB_TOKEN:** Sadece `secrets.GITHUB_TOKEN` (GitHub’ın sağladığı kısa ömürlü token); repo’da sabit secret veya credential yok. **Kabul edilebilir.**
- **Secret tarama:** gitleaks ile secret_scan job’ları mevcut. **Uygulanıyor.**

### 5.3 Eksik güvenlik dokümanları

| Repo | SECURITY.md | CONTRIBUTING.md |
|------|-------------|------------------|
| decision-schema | Var | Yok |
| mdm-engine | Var | Yok |
| decision-modulation-core | Var | Yok |
| ops-health-core | Var | Yok |
| evaluation-calibration-core | Var | Yok |
| execution-orchestration-core | **Yok** | Yok |
| decision-ecosystem-integration-harness | **Yok** | Yok |
| decision-ecosystem-docs | **Yok** | Yok |
| explainability-audit-core | **Yok** | Yok |

**Sonuç:** 4 repoda SECURITY.md eksik; tüm repolarda CONTRIBUTING.md yok. Raporun P0/P1 “minimum artefact” listesi ile uyumlu eksiklik.

---

## 6. Eksiklik özeti

| Öğe | Nerede | Öncelik |
|-----|--------|---------|
| ops-health: max_p95_latency_ms == 0 guard | scorer.py | P0 (savunma) |
| SECURITY.md | docs, exec-orch, harness, explainability | P1 |
| CONTRIBUTING.md | Tüm repolar (en az docs + core) | P1 |
| Formül dokümanları: payda/σ=0 notu | FORMULAS.md (eval genel notasyon) | P1 |
| Coverage threshold (pytest-cov, CI) | Tüm test repoları | P2 |
| SBOM / Scorecard workflow | — | P2 |

---

## 7. Invariant ve test (mevcut durum)

- **Fail-closed:** DMC modulator exception path’te `_fail_closed(policy)`; ops_health kill_switch; mdm private hook exception → HOLD. **Kod ile doküman uyumlu.**
- **Bounded score [0,1]:** ops-health scorer clamp; decision_schema clamp_confidence. **Karşılanıyor.**
- **Determinism:** Formül kodlarında rastgelelik yok; guard sırası sabit. **Karşılanıyor.**
- **Contract (schema):** Proposal/FinalDecision tipleri decision_schema’da; eval invariant’ları confidence_clamp vb. **Tutarlı.**

---

## 8. Patch planı (ölçülebilir adımlar)

1. **ops_health_core/scorer.py:** `p_lat` hesaplamadan önce `if policy.max_p95_latency_ms <= 0: p_lat = 0.0` (ve ilgili blokta bölme yapma) veya model dokümanında “max_p95_latency_ms > 0” kısıtı.
2. **SECURITY.md:** decision-ecosystem-docs, execution-orchestration-core, decision-ecosystem-integration-harness, explainability-audit-core köküne şablon SECURITY.md ekle (iletişim, desteklenen sürümler).
3. **CONTRIBUTING.md:** En azından docs ve bir core’da örnek CONTRIBUTING (PR koşulları, test/lint) ekle.
4. **FORMULAS.md (genel notasyon):** Eval/outcome bölümünde “σ=0 veya payda 0 ise SR/benzeri oranlar tanımsız; uygulama yapılırsa guard gerekir” notu.
5. **P2:** Coverage threshold (pytest-cov), SBOM/Scorecard — ayrı plan.

---

## 9. Sonuç tablosu

| Soru | Cevap |
|------|--------|
| Uyumsuzluk görüyor musun? | **Hafif:** Sadece ops-health’ta max_p95_latency_ms=0 edge-case’i (eksik savunma). |
| Güvenlik açığı? | **Açık zafiyet yok;** CI permissions ve secret tarama uygun. **Eksik:** SECURITY.md (4 repo), CONTRIBUTING. |
| Eksiklik? | SECURITY.md, CONTRIBUTING.md, ops-health sıfıra bölme guard, (P2) coverage/SBOM/Scorecard. |
| Matematik/fizik formülleri tutarlı mı? | **Evet.** ops-health ve mdm formülleri doküman ile kod uyumlu; ağırlık toplamları 1; clamp’ler doğru. Tek nokta: genel notasyonlarda σ=0/payda 0 için doküman notu. |
| Akademik tutarlılık (formüller)? | Normalize ceza [0,1], skor [0,1], sigmoid tanımı, determinism ve bounded invariant’lar karşılanıyor; sayısal edge-case’ler (sıfıra bölme) tek yerde (ops-health p_lat) ve düzeltilebilir. |

---

**Referanslar:** deep-research-report.md, DEEP_RESEARCH_REPORT_VERIFICATION.md, ops_health_core/scorer.py, ops_health_core/model.py, mdm_engine/mdm/reference_model_generic.py, dmc_core/dmc/modulator.py, docs/FORMULAS.md (ops-health, mdm-engine, decision-ecosystem-docs), ECOSYSTEM_INVARIANTS.md.
