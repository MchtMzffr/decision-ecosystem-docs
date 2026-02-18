# P3 Kickoff Checklist (Gate to P3)

P3’e geçmeden önce bu üç madde tamamlanmalı. Tamamlandığında trace standardizasyonu ve arbitration için temel SSOT + integration layer hazır olur.

---

## 1. decision-schema P3-S1 — PacketV2.external key registry + test

**Hedef:** Guard/eval/ops sonuçlarının PacketV2.external’a yazılacağı key’lerin SSOT tanımı.

- [ ] `docs/PARAMETER_INDEX.md` (veya ilgili schema doc): `external.dmc.guard_trace`, `external.ops.health_snapshot`, `external.eval.metrics_summary` tanımları
- [ ] Test: `test_packet_external_namespace_keys` (key formatı: namespaced)
- [ ] Test: `test_packet_external_trace_schema` (guard trace entry shape)

**DONE:** Schema doc güncel + iki test PASS.

---

## 2. harness P3-H1 — Canonical external writer + INV-T1

**Hedef:** Integration layer’ın trace/snapshot’ı PacketV2.external’a canonical key’lerle yazması.

- [ ] `harness/packet_builder.py`: `attach_dmc_trace`, `attach_ops_snapshot` (veya eşdeğer) fonksiyonları
- [ ] `docs/INTEGRATION_GUIDE.md`: canonical external key listesi
- [ ] INV-T1 test: key formatı + trace schema
- [ ] Test: `test_packet_external_keys_are_namespaced`

**DONE:** Harness canonical writer + INV-T1 testleri PASS.

---

## 3. dmc-core P3-D1 — Guard trace schema + determinism test

**Hedef:** DMC modulate çıktısında guard evaluation trace’i standart formatta.

- [ ] `dmc_core/dmc/modulator.py` (veya helper): `trace: list[dict]` üretimi — alanlar: `name`, `pass`, `reason_code`, `latency_ms`, `severity`, `ts_ms`
- [ ] Core Packet’a yazmaz; sadece trace döndürür (harness P3-H1 yazar)
- [ ] Test: `test_trace_schema_stable`
- [ ] Test: `test_trace_guard_order_matches_guard_order`

**DONE:** Guard trace schema sabit + determinism testleri PASS.

---

## Neden bu sıra?

1. **Schema (P3-S1)** — SSOT; diğer repolar buna referans verir.
2. **Harness (P3-H1)** — PacketV2’ye yazım sözleşmesi; DMC ve ops çıktılarını bu key’lerle yazar.
3. **DMC (P3-D1)** — Trace’i üretir; harness onu Packet’a yazar.

Bu üçü bittiğinde P3’ün geri kalanı (arbitration, trace metrics, release discipline) daha hızlı ilerler.
