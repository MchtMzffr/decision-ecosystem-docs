# P3 Sprint Board — Core Integration Architecture (CIA) v0.3

P2 ile kapılar (CI-0/INV0/INV2/PKG) ve temel güvenlik davranışı oturdu. **P3 hedefi:** ekosistemi ürünleşebilir hale getirmek için **trace standardizasyonu, deterministik arbitration ve release disiplinini** tamamlamak. Domain-agnostic, contract-first; core'lar sadece `decision-schema`'ya bağımlı.

---

## P3 Hedef Tanımı

- **Trace standardizasyonu:** Guard/eval/ops sonuçlarının PacketV2'ye namespaced key'lerle yazılması (SSOT).
- **Deterministik arbitration:** Çoklu proposal → tek seçim (domain-free, testli).
- **Release disiplini:** CHANGELOG, tag, ECOSYSTEM_CONTRACT_MATRIX release bölümü.

---

## P3 Varsayımlar

- Sözleşme aralığı: `decision-schema>=0.2,<0.3` (minor=2 pin).
- CIA adımı: propose → ops gate → modulate → packet → report (harness kanıtlıyor).
- Domain örnekleri yalnız `docs/examples/` altında (PKG-1/2 ile kilitli).

---

## P3 Çekirdek Formüller (Contract-level)

### 1) Trace standardı (guard değerlendirme kaydı)

Her guard için:

- Giriş: $(p_t, c_t, \pi)$
- Çıkış: $g_i = (\text{pass}_i \in \{0,1\}, \text{code}_i, \text{latency}_i, \text{severity}_i)$

PacketV2'ye yazım:

$$\text{PacketV2.external}[\texttt{dmc.guard_trace}] := [g_1, g_2, \ldots, g_n]$$

Namespacing invariant: external key'ler `[a-z0-9]+(\.[a-z0-9]+)+` formatında olmalı.

### 2) Multi-proposal + arbitration

MDM çoklu öneri üretebilir: $P_t = \{p_t^{(1)}, \ldots, p_t^{(K)}\}$.

Arbitration (domain-free) seçer:

$$p_t^* = \arg\max_{p \in P_t} U(p, c_t) \quad \text{s.t. } \text{feasible}(p, c_t)$$

Sonra DMC modulate eder: $(d_t, m_t) = \mathrm{DMC}(p_t^*, \pi, c'_t)$.

---

## P3 Global Invariant Set (yeni)

P2 gate'lerine ek:

| ID | Açıklama |
|----|----------|
| **INV-T1** | Trace namespacing & shape: PacketV2.external trace anahtarları namespaced; guard trace entry schema sabit (field set + types). |
| **INV-T2** | Deterministic arbitration: aynı input → aynı seçilen proposal; tie-break rule explicit ve testli. |
| **INV-R1** | Release consistency: her repo `__version__`, CHANGELOG.md, tag'lenebilir release notu; matrix dokümanı minor pin ile tutarlı. |

---

## P3 Sprint Board (Repo Bazlı)

### A) decision-schema (SSOT) — P3-S*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-S1** | PacketV2 trace extension (domain-free): guard/eval/ops sonuçları için SSOT key registry. | `PARAMETER_INDEX.md`: `external.dmc.guard_trace`, `external.ops.health_snapshot`, `external.eval.metrics_summary`. Test: `test_packet_external_namespace_keys`, `test_packet_external_trace_schema`. |
| **P3-S2** | ECOSYSTEM_CONTRACT_MATRIX "Release block". | Matrix'e released versions + expected_minor + deprecation timeline. DONE: schema doc + test minor gate pass. |

### B) decision-modulation-core (dmc-core) — P3-D*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-D1** | Guard trace writer: DMC modulate içinde guard evaluation trace'i standart formatta üret. | `modulator.py`: `trace: list[dict]` — `{name, pass, reason_code, latency_ms, severity, ts_ms}`. Core Packet'a yazmaz; integration layer yazar. Test: `test_trace_schema_stable`, `test_trace_guard_order_matches_guard_order`. |
| **P3-D2** | Multi-proposal arbitration API (opsiyonel). | `dmc_core/dmc/arbitration.py`: `modulate_many(proposals, policy, context)`. Tie-break: `(confidence, action_priority, stable_hash(reasons/params))`. Test: INV-T2, property-based reorder → same result. |

### C) mdm-engine — P3-M*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-M1** | Multi-proposal generation: `DecisionEngine.propose_many(features) -> list[Proposal]`. | `decision_engine.py` + `reference_model_generic`: top-K, candidate actions (HOLD/ACT/EXIT/CANCEL) + score. Test: deterministic ordering, len≤K, confidence in [0,1]. |
| **P3-M2** | Proposal param hygiene: Proposal.params anahtarları `mdm.*` namespace (PARAMETER_INDEX). | Test: `test_params_namespace_mdm`. |

### D) ops-health-core — P3-O*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-O1** | Health snapshot standard output: OpsSignal → standard snapshot dict. | `ops_health_core/snapshot.py`: `build_snapshot(...)`. Integration: `external.ops.health_snapshot`. Test: snapshot field set stable, fail-closed path snapshot present. |
| **P3-O2** | Cooldown semantics formalization. | docs/FORMULAS.md: cooldown window + RED dominance. Test: time boundary (now_ms == cooldown_until_ms). |

### E) evaluation-calibration-core — P3-E*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-E1** | Packet trace consumption: `dmc.guard_trace`, `ops.health_snapshot` okuyan metrics. | `eval_calibration_core/metrics/trace_metrics.py`: `guard_trigger_rates`, `guard_latency_p95`, `ops_red_rate`. INVARIANT-5 key set + backward-compat. |
| **P3-E2** | Report schema stabilization. | Report JSON schema + markdown sections stable. Test: golden file (small packet set → stable report). |

### F) integration-harness — P3-H*

| ID | Tanım | Patch / Test |
|----|--------|--------------|
| **P3-H1** | Packet external writer (canonical): trace/snapshot/metrics → PacketV2.external canonical key'lerle. | `harness/packet_builder.py`: `attach_dmc_trace`, `attach_ops_snapshot`. INTEGRATION_GUIDE: canonical external key list. Test: INV-T1, `test_packet_external_keys_are_namespaced`. |
| **P3-H2** | Full-stack E2E golden pipeline. | Fixed seed state/context → deterministic Packet+Report. Test: `tests/golden/` JSON fixtures, checksum verify. DONE: CI full_stack passes golden. |

---

## P3 Release Plan (SemVer + timeline)

- **decision-schema:** 0.2.x → trace ekleri backward-compatible ise 0.2.(x+1).
- **Cores:** Yeni API'ler (propose_many / modulate_many) → her core kendi SemVer'inde 0.(minor+1).0 (pre-1.0 disiplinli).
- **Deprecation:** Eski trace key yoksa "none"; yeni ek kırma yok.

---

## P3 "Hemen yapılacaklar" (en kritik 5 iş)

1. **decision-schema P3-S1:** PacketV2.external key registry + tests.
2. **harness P3-H1:** canonical external writer + INV-T1 tests.
3. **dmc-core P3-D1:** guard trace schema + determinism test.
4. **mdm-engine P3-M1:** propose_many + deterministic ordering.
5. **eval-cal P3-E1:** trace_metrics + metrics key set governance (INVARIANT-5 update rule).
