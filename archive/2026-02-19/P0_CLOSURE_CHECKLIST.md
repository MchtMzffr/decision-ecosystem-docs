# P0 Closure Checklist — CIA v0.2 DONE

Her madde için: **Dosya → Beklenen durum → Çalıştırılacak test → Beklenen çıktı**.

---

## P0-A — integration-harness: CI YAML

| Öğe | Değer |
|-----|--------|
| **Dosya** | `decision-ecosystem-integration-harness/.github/workflows/ci.yml` |
| **Beklenen** | Çok satırlı, geçerli YAML; `name: CI`, `jobs.test.steps` her biri ayrı satır; "Install test tooling" + "Install decision-schema" + "Install harness" + "Run tests". |
| **Test** | GitHub Actions’ta workflow tetikle (push/PR) veya `actionlint` / `yamllint .github/workflows/ci.yml`. |
| **Çıktı** | Workflow parse edilir; job’lar yeşil (veya decision-schema kurulumu skip değilse testler geçer). |

---

## P0-B — integration-harness: INV0 docs

| Öğe | Değer |
|-----|--------|
| **Dosyalar** | `docs/INTEGRATION_GUIDE.md`, `README.md` |
| **Beklenen** | INTEGRATION_GUIDE örnek state: `signal_0`, `signal_1`, `state_scalar_a`, `state_scalar_b` (mid/imbalance/depth yok). README’de "mdm-engine" only (ami-engine yok). |
| **Test** | `pytest decision-ecosystem-integration-harness/tests/test_invariant_0_domain_agnosticism.py -v` |
| **Çıktı** | `test_invariant_0_docs_domain_agnostic` PASSED. |

---

## P0-C — mdm-engine: branch / secrets.py

| Öğe | Değer |
|-----|--------|
| **Problem** | Default branch’ta `mdm_engine/security/secrets.py` olmalı; main’de 404 ise branch drift var. |
| **Beklenen** | Varsayılan branch (tercihen `main`) üzerinde `mdm_engine/security/secrets.py` mevcut; `from mdm_engine.security import EnvSecretsProvider` çalışır. |
| **Patch** | GitHub’da default branch = main; `master` varsa main’e merge veya master’ı sil; `secrets.py` .gitignore’da allow (`!mdm_engine/security/secrets.py`). |
| **Test** | `python -c "from mdm_engine.security import EnvSecretsProvider; print('ok')"` (mdm-engine root’ta). |
| **Çıktı** | `ok`. |

---

## P0-D — mdm-engine: reference model domain-free

| Öğe | Değer |
|-----|--------|
| **Dosyalar** | `mdm_engine/mdm/reference_model_generic.py` (domain-free), `docs/examples/example_domain_legacy_v0/reference_model_legacy.py` (quarantined), `mdm_engine/mdm/reference_model.py` (compat shim). |
| **Beklenen** | Core proposal path generic key’ler kullanır (signal_0, signal_1, state_scalar_a/b). INV0 code scan sadece `mdm_engine/mdm/` (reference_model.py, position_manager.py hariç). |
| **Test** | `pytest mdm-engine/tests/test_invariant_0_domain_agnosticism.py -v` |
| **Çıktı** | `test_invariant_0_docs_domain_agnostic` ve `test_invariant_0_core_code_domain_agnostic` PASSED. |

---

## DONE kriterleri (hepsi sağlanınca CIA v0.2 DONE)

- [ ] P0-A: Harness CI parse + run.
- [ ] P0-B: Harness INV0 docs PASSED.
- [ ] P0-C: mdm-engine default branch’ta secrets.py var.
- [ ] P0-D: mdm-engine proposal core domain-free; INV0 code PASSED.
- [ ] Tüm repolarda ilgili testler yeşil (skip hariç full-core job istersen ayrı).

Bu koşullar sağlandığında bir sonraki faz: **Multi-Proposal + Arbitration** (entegrasyon katmanı genişlemesi).
