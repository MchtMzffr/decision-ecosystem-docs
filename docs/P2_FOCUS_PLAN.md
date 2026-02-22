# P2 Focus Plan — Decision Ecosystem

**Date:** 2026-02  
**Context:** P0 ve P1 check’ler tamamlandı; sırada P2 işleri.

---

## P0 / P1 Check Sonuçları (Doğrulandı)

| Check | Tool / Test | Sonuç |
|-------|------------|--------|
| **INV-DOC-DRIFT-1** | `check_release_alignment.py --workspace <parent>` | OK — roadmap tablosu ile pyproject version’lar uyumlu |
| **INV-SYNC-1** | `check_workspace_sync.py --workspace <parent>` | OK — tüm repolar clean, origin/main ile senkron |
| **P0 Remote owner** | `check_remote_owner.py --workspace <parent>` | OK — canonical owner kullanılıyor |
| **P1 Ops-Health latency** | `pytest tests/test_latency_window_pruning.py test_health_score test_kill_switch` | OK — 12 passed |

**Özet:** P0 ve P1 blokaj yok; P2’ye geçilebilir.

---

## P2 İş Listesi (Öncelik Sırası)

### 1. explainability-audit-core — Roadmap + Release (P2-High)

**Mevcut durum:** Repo var; `explain_from_packet`, INV-EXPL testleri, doc trio (ARCHITECTURE, FORMULAS, INTEGRATION_GUIDE) tamamlandı. CI mevcut.

**P2 yapılacaklar:**
- [x] **Roadmap güncellemesi:** NEXT_STEPS_ROADMAP.md içinde “explainability-audit-core” satırını güncelle: “Minimal tamamlandı (v0.1.0 skeleton, INV-EXPL testleri, doc trio); ilk tag v0.1.0 yayınlanabilir.”
- [x] **İlk release:** SemVer 0.1.0 için GitHub tag + release notes (RELEASE_NOTES_STANDARD_AND_TEMPLATES’e uyumlu).
- [x] **Opsiyonel:** Roadmap P0 tablosuna 7. core olarak eklemek (scope “6 core” ise eklenmez; “Future” bölümünde kalır).

### 2. Harness’ta explanation (P2-Medium, opsiyonel)

**Amaç:** Integration harness’ta PacketV2 üretildikten sonra `explain_from_packet(packet)` ile rapora explanation artifact eklemek.

**Yapılacaklar:**
- [ ] Harness’ta `explainability-audit-core` opsiyonel dependency (try/import).
- [x] PacketV2 sonrası `explain_from_packet(packet)` çağrısı; çıktıyı report’a (örn. `report["explanation"]`) yazmak.
- [ ] INTEGRATION_GUIDE’da bu adımı dokümante etmek (zaten explainability-audit-core/docs/INTEGRATION_GUIDE.md’de taslak var).

### 3. decision-ecosystem-cli (P2-Medium)

**Amaç:** Tek komutla ecosystem yönetimi: core’ları kurma, yerel test pipeline, contract matrix doğrulama.

**Kapsam (önerilen):**
- [ ] Yeni repo veya `decision-ecosystem-docs/tools` altında `ecosystem` CLI script’i.
- [ ] Subcommand’lar: `install` (pip install -e her core), `test` (workspace’te pytest), `check-release` (check_release_alignment), `check-sync` (check_workspace_sync).
- [ ] Bağımlılık: docs repo’daki mevcut tools ile uyum; çalışma dizini `--workspace` ile verilir.

### 4. CI/CD olgunluk (P3 — P2 sonrası)

Roadmap’te P3: secret scan, vulnerability scan, coverage gate’leri. P2 tamamlandıktan sonra ele alınır.

---

## Önerilen P2 Sırası

1. **explainability-audit-core roadmap + v0.1.0 release** — Kısa sürede tamamlanabilir; audit-ready skorunu netleştirir.
2. **Harness explanation (opsiyonel)** — explainability’yi gerçek pipeline’a bağlar.
3. **decision-ecosystem-cli** — Tek komut deneyimi; tools script’lerini sarmalayan ince CLI.

Bu doküman P2 odaklı çalışma için referans olarak kullanılabilir; ilerleme durumu checklist üzerinden güncellenebilir.
