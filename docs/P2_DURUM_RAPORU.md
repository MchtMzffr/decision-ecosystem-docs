# P2 Durum Raporu — Decision Ecosystem

**Tarih:** 2026-02  
**Kapsam:** P2 adımlarının tamamı devreye alındı; kurallar (SOLID, Clean Architecture, modular, doküman–kod uyumu) göz önünde bulunduruldu.

---

## 1. Özet

| P2 Maddesi | Durum | Açıklama |
|------------|--------|----------|
| explainability-audit-core roadmap + v0.1.0 | **Devrede** | Roadmap güncellendi; RELEASE_NOTES_0.1.0.md eklendi; tag **v0.1.0** oluşturulup push edildi. |
| Harness explanation | **Devrede** | `_attach_explanation(report, packet)` eklendi; opsiyonel import ile `report.explanation` set ediliyor. |
| decision-ecosystem-cli | **Devrede** | `tools/ecosystem.py` eklendi; `install`, `test`, `check-release`, `check-sync` subcommand'ları çalışıyor. |

---

## 2. Yapılan Değişiklikler

### 2.1 explainability-audit-core

- **docs/RELEASE_NOTES_0.1.0.md:** INV-REL-TAG-1 / RELEASE_NOTES_STANDARD’a uyumlu release notları.
- **Git tag:** `v0.1.0` oluşturuldu ve `origin`’e push edildi.
- **Bağımlılık:** Sadece `decision-schema>=0.2.2,<0.3` (INV-CORE-DEP-1).

### 2.2 decision-ecosystem-integration-harness

- **harness/run_one_step.py:**
  - Report üretildikten sonra `_attach_explanation(report, packet)` çağrılıyor (normal ve fail-closed path).
  - `_attach_explanation`: `explainability_audit_core.explain_from_packet` opsiyonel import; varsa `report.explanation = artifact.to_dict()`, yoksa `report.explanation = None`.
- **Test:** Mevcut 25 harness testi geçti (explanation opsiyonel olduğu için ek test zorunlu değil).

### 2.3 decision-ecosystem-docs

- **NEXT_STEPS_ROADMAP.md:**
  - explainability-audit-core: “Minimal tamamlandı (v0.1.0)”, ilk tag v0.1.0, harness’ta opsiyonel entegrasyon.
  - decision-ecosystem-cli: “Devrede”; `tools/ecosystem.py`, subcommand’lar açıklandı.
  - Decision matrix’te her iki P2 satırı ✅ işaretlendi.
- **tools/ecosystem.py:** Yeni CLI.
  - `--workspace <path>` (opsiyonel; varsayılan: docs repo’nun parent’ı).
  - **install:** `pip install -e` ile decision-schema önce, sonra diğer repolar.
  - **test:** Her repo için `pytest tests/` (tests/ dizini varsa).
  - **check-release:** `check_release_alignment.py --workspace`.
  - **check-sync:** `check_workspace_sync.py --workspace`.
- **docs/P2_FOCUS_PLAN.md:** P2 iş listesi ve tamamlanan maddeler (checklist güncellendi).

---

## 3. Doğrulama

| Kontrol | Sonuç |
|--------|--------|
| Harness pytest (25 test) | **PASS** |
| ecosystem.py check-release | **OK** (roadmap vs pyproject uyumlu) |
| ecosystem.py check-sync | **OK** (tüm repolar clean ve origin/main ile senkron, push sonrası) |
| explainability-audit-core tag v0.1.0 | **Push edildi** |

---

## 4. Kullanım (Devreye Alma)

- **Ecosystem CLI (docs repo’dan):**
  ```bash
  cd decision-ecosystem-docs
  python tools/ecosystem.py --workspace <parent-dir> install   # core’ları kur
  python tools/ecosystem.py --workspace <parent-dir> test       # tüm testler
  python tools/ecosystem.py --workspace <parent-dir> check-release
  python tools/ecosystem.py --workspace <parent-dir> check-sync
  ```
- **Harness’ta explanation:** `explainability-audit-core` kuruluysa `run_one_step(...)` dönen report’ta `getattr(report, 'explanation', None)` ile explanation artifact (dict) alınır.
- **explainability-audit-core v0.1.0:** `pip install explainability-audit-core==0.1.0` veya mevcut tag’ten kurulum.

---

## 5. Sıradaki Adımlar (P3)

- CI/CD olgunluk: secret scan, vulnerability scan, coverage gate’leri (roadmap’te P3).
- İsteğe bağlı: REPO_REGISTRY’de explainability-audit-core için `latest_tag: v0.1.0` ve status güncellemesi.

---

**Rapor sonu.** Tüm P2 maddeleri devreye alındı; durum raporu bu dokümanla kayıt altına alındı.
