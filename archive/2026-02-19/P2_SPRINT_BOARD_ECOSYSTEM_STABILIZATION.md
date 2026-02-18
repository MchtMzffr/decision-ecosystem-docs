# P2 Sprint Board — Ecosystem Stabilization (Release-grade Gates)

**Golden paket + CIA v0.2** → ürünleştirilebilir çekirdek platform: **Stabilization → Release → Scale-out**.

---

## 1) Net tanım: Neredeyiz, “şimdi” ne?

**CIA v0.2 DONE** = entegrasyon katmanında *tek adım karar döngüsü* (propose → ops → modulate → PacketV2 → report) **kanıtlanabilir** hale geldi.

**“Şimdi”** = bunu **ekosistemin tüm repolarında standart gate’lerle kilitleme** ve **release-ready** hale getirme.

---

## 2) Varsayım

- `decision-schema` SSOT; `>=0.2,<0.3` pin korunuyor.
- Core’lar **birbirini import etmiyor** (INV2).
- Domain örnekleri **yalnızca** `docs/examples/**`.

---

## 3) Üç faz

### Faz-1 — Repo’lara gate yayılımı (P2)

Amaç: CIA v0.2’de kanıtlanan hijyeni **tüm core repo’lara** taşımak.

**Her repo için minimum gate set:**

- **CI-0** workflow hygiene (LF-only, no control/embedding Unicode, multi-line)
- **INV0** domain-agnostic public surface
- **INV2** no cross-core imports
- Repo’nun kendi smoke testleri

### Faz-2 — Release & versioning disiplini (P3)

- Her repo: `CHANGELOG.md`, `RELEASE.md`
- decision-schema: compat matrix + deprecation timeline
- **PKG-1:** `docs/examples` hiçbir core package’a girmiyor

### Faz-3 — Scale: Multi-Proposal + Arbitration (Phase-2)

- mdm-engine: `propose_many(state, context) -> list[Proposal]`
- Integration layer: arbitrator (policy + guard penalties)
- eval-calibration: “selection stability” metrikleri

---

## 4) Invariant set (hedef ölçülebilirlik)

| Kodu | Açıklama |
|------|----------|
| **CI-0** | Workflow dosyaları hijyenik (CR=0, LF≥10, blocked Unicode=0, `on:`/`jobs:` satır-adreslenebilir) |
| **INV0** | Public surface domain vocab = 0 (docs/examples hariç) |
| **INV2** | Cross-core import = 0 |
| **H1** | Schema minor gate (expected_minor=2) fail-closed |
| **H2** | Kill-switch dominance (`ops_deny_actions=True ⇒ deny + HOLD`) |
| **H3** | PacketV2 required fields completeness |
| **H4** | Exception ⇒ fail-closed (HOLD/STOP) |
| **H5** | Report metric key set deterministik |
| **PKG-1** | Wheel/sdist içinde `docs/examples/**` yok |

---

## 5) Global P2 hedefleri (her repo için)

- **CI-0:** `.github/workflows/*.yml` hijyenik (LF-only, no control/embedding Unicode, multi-line)
- **INV0:** public surface domain-agnostic (docs/examples hariç)
- **INV2:** cross-core import yok (core’lar yalnız decision-schema’ya bağımlı)
- **PKG-1:** `docs/examples/**` package içine girmiyor
- **SMOKE:** repo’nun minimum çalışır fonksiyonu testleniyor

**Global DONE metriği:** Her repoda GitHub Actions **green**, `pytest` **PASS**, “core-only” job’da **skip=0** (integration-harness’ta full-stack opsiyonel).

---

## 6) Template (tüm repolara kopyalanacak şablon işler)

### P2-T0 — CI workflow ekle/standardize et

| Öğe | Değer |
|-----|--------|
| **Dosya** | `.github/workflows/ci.yml` |
| **İçerik** | Python matrix (3.11/3.12), `pip install -U pip pytest`, `pip install -e .`, `pytest -v` |
| **Invariant** | CI-0 + test suite koşuyor |
| **Test** | GitHub Actions run + yerelde `pytest -v` |
| **DONE** | Actions yeşil + CI-0 test PASS |

### P2-T1 — CI-0 testi ekle

| Öğe | Değer |
|-----|--------|
| **Dosya** | `tests/test_invariant_ci_0_workflow_hygiene.py` |
| **Invariant** | CR=0, LF≥10, blocked Unicode=0, `on:`/`jobs:` line-addressable |
| **Test** | `pytest tests/test_invariant_ci_0_workflow_hygiene.py -v` |
| **DONE** | PASS |

### P2-T2 — INV0 testi ekle/standardize et

| Öğe | Değer |
|-----|--------|
| **Dosya** | `tests/test_invariant_0_domain_agnosticism.py` |
| **Tarama** | `README.md`, `docs/**`, package path; **exclude:** `docs/examples/**`, `tests/**` |
| **Invariant** | blocked lexeme count = 0 |
| **DONE** | PASS |

### P2-T3 — INV2 testi ekle/standardize et

| Öğe | Değer |
|-----|--------|
| **Dosya** | `tests/test_invariant_2_no_cross_core_imports.py` |
| **Invariant** | {mdm-engine, dmc, ops-health, eval-cal} birbirini import etmiyor |
| **DONE** | PASS |

### P2-T4 — PKG-1 packaging guard

| Öğe | Değer |
|-----|--------|
| **Dosya** | `tests/test_pkg_1_no_examples_packaged.py` |
| **Invariant** | wheel/sdist içinde `docs/examples/**` yok |
| **Test** | `python -m build` + wheel/sdist tarama |
| **DONE** | PASS |

---

## 7) Repo bazlı görev listesi

### A) decision-schema (SSOT)

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-S1 | CI + CI-0 (T0, T1) | `.github/workflows/ci.yml`, `tests/test_invariant_ci_0_workflow_hygiene.py` | Actions green |
| P2-S2 | INV0 (docs/README) | `tests/test_invariant_0_domain_agnosticism.py`; `docs/PARAMETER_INDEX.md` taranmalı | INV0 PASS |
| P2-S3 | PKG-1 | `tests/test_pkg_1_no_examples_packaged.py` | wheel’da docs/examples yok |
| P2-S4 | Compat gate smoke | Mevcut compat testler (minor=2) CI gate olarak | CI’da koşuyor |
| — | Release docs | `docs/RELEASE.md`, `CHANGELOG.md` | Var |

### B) decision-modulation-core (DMC)

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-D1 | CI + CI-0 (T0, T1) | `.github/workflows/ci.yml`, CI-0 testi | |
| P2-D2 | INV0 / INV2 (T2, T3) | `docs/examples/**` exclude doğru | INV0+INV2 PASS |
| P2-D3 | SMOKE: guard order + fail-closed | `test_invariant_3_guard_order_determinism`, `test_invariant_4_fail_closed` required | CI’da PASS |
| P2-D4 | PKG-1 (T4) | examples paketlenmiyor | PASS |

### C) ops-health-core

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-O1 | CI + CI-0 (T0, T1) | | |
| P2-O2 | INV0 / INV2 (T2, T3) | | |
| P2-O3 | SMOKE: kill-switch + fail-closed | `test_fail_closed_on_exception` + dominance; `deny_actions=True ⇒ HOLD` | CI’da PASS |
| P2-O4 | PKG-1 (T4) | | |

### D) evaluation-calibration-core

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-E1 | CI + CI-0 (T0, T1) | | |
| P2-E2 | INV0 / INV2 (T2, T3) | | |
| P2-E3 | INVARIANT 5 metric key set | `tests/test_invariant_5_metric_key_set.py` (veya smoke); report metrics anahtar seti sabit | CI’da PASS |
| P2-E4 | PKG-1 (T4) | | |

### E) mdm-engine

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-M1 | CI + CI-0 (T0, T1) | | |
| P2-M2 | INV0 core scan + “0 exclude” | **M2.1:** position_manager ya `docs/examples` quarantine ya domain-free rewrite; **M2.2:** INV0 exclude listesi boş | exclude=0, INV0 PASS |
| P2-M3 | INV2 (T3) | | |
| P2-M4 | test_loop_smoke (skip) | Seçenek A: legacy loop examples’a taşınır, core testten çıkar → core-only skip=0 | skip=0 |
| P2-M5 | PKG-1 (T4) | | |

### F) decision-ecosystem-integration-harness (Golden)

| ID | Görev | Dosyalar / not | DONE |
|----|--------|----------------|------|
| P2-H1 | CI job split | **Job 1:** `core-only` (decision-schema + harness) → skip=0; **Job 2:** `full-stack` (mdm+dmc+ops+eval) | core-only green; full-stack when deps var |
| P2-H2 | Evidence gate | `tests/test_end_to_end_smoke.py`; FinalDecision + PacketV2 + Report | PASS |
| P2-H3 | Docs closure record | `docs/P0_CLOSURE_CHECKLIST.md` tek paragraf closure + raw evidence linkleri | INV0+CI-0 kanıtlı |

---

## 8) Sprint output (beklenen somut çıktı)

6 repo (5 core + harness) için:

- `.github/workflows/ci.yml` **var ve CI-0 uyumlu**
- `tests/test_invariant_ci_0_workflow_hygiene.py` **PASS**
- `tests/test_invariant_0_domain_agnosticism.py` **PASS**
- `tests/test_invariant_2_no_cross_core_imports.py` **PASS**
- `tests/test_pkg_1_no_examples_packaged.py` **PASS**

Özel:

- **mdm-engine:** skip=0 (`test_loop_smoke` ve position_manager exclude kapanmış)
- **integration-harness:** core-only job green; full-stack opsiyonel

---

## 9) İcra: Issue paketi ve otomasyon

- **Copy-paste / SSOT:** [P2_GITHUB_ISSUE_PACK.md](P2_GITHUB_ISSUE_PACK.md) — repo başına issue metinleri, acceptance criteria, komutlar, invariant linki.
- **Otomasyon:** `tools/create_p2_issues.sh` — `gh` CLI ile tek komutta P2 milestone + issue'ları açar (isteğe bağlı).
- **P2 DONE (tek satır):** 6 repo'nun hepsinde Actions green + (CI-0, INV0, INV2, PKG-1) PASS + mdm-engine skip=0 + harness core-only skip=0.

