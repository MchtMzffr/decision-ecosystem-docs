# P2 GitHub Issue Pack (Copy-Paste / Automation SSOT)

P2 Sprint Board’ı icra aracına çevirir: her repoda **P2 milestone + issue seti**, her issue’da **acceptance criteria + komutlar + invariant linki**.

**P2 DONE (tek satır):** 6 repo’nun hepsinde Actions green + (CI-0, INV0, INV2, PKG-1) PASS + mdm-engine skip=0 + harness core-only skip=0.

---

## Ortak etiket seti (tüm repolar)

- `p2`
- `invariant`
- `ci`
- `docs`
- `packaging`

**Milestone:** P2 Ecosystem Stabilization

---

## 1) decision-schema

### [P2-S1] Add GitHub Actions CI (pytest matrix) + CI-0 hygiene gate

**Acceptance**
- `.github/workflows/ci.yml` eklendi (3.11/3.12, pytest)
- `tests/test_invariant_ci_0_workflow_hygiene.py` PASS
- GitHub Actions green

**Commands**
```bash
pytest -v
pytest tests/test_invariant_ci_0_workflow_hygiene.py -v
```

**Invariants:** CI-0

---

### [P2-S2] Standardize INV0 domain-agnostic public surface scan (README+docs+public code)

**Acceptance**
- `tests/test_invariant_0_domain_agnosticism.py` PASS
- `docs/examples/**` ve `tests/**` exclude

**Commands**
```bash
pytest tests/test_invariant_0_domain_agnosticism.py -v
```

**Invariants:** INV0

---

### [P2-S3] Add PKG-1: Ensure docs/examples is not packaged

**Acceptance**
- `tests/test_pkg_1_no_examples_packaged.py` PASS
- wheel/sdist içinde `docs/examples/**` yok

**Commands**
```bash
python -m build
pytest tests/test_pkg_1_no_examples_packaged.py -v
```

**Invariants:** PKG-1

---

### [P2-S4] Release hygiene: add CHANGELOG.md + RELEASE.md (SemVer + compat policy)

**Acceptance**
- `CHANGELOG.md` mevcut
- `docs/RELEASE.md` mevcut: SemVer, deprecation timeline, compat gating

---

## 2) decision-modulation-core

### [P2-D1] Add GitHub Actions CI + CI-0 hygiene gate

(Acceptance/commands: P2-S1 ile aynı)

---

### [P2-D2] Standardize INV0 + INV2 gates

**Acceptance**
- INV0 PASS (examples excluded)
- INV2 PASS (no mdm/ops/eval imports)

**Commands**
```bash
pytest tests/test_invariant_0_domain_agnosticism.py -v
pytest tests/test_invariant_2_no_cross_core_imports.py -v
```

---

### [P2-D3] Promote determinism + fail-closed tests to required gates

**Acceptance**
- `test_invariant_3_guard_order_determinism.py` PASS
- `test_invariant_4_fail_closed.py` PASS

**Commands**
```bash
pytest tests/test_invariant_3_guard_order_determinism.py -v
pytest tests/test_invariant_4_fail_closed.py -v
```

---

### [P2-D4] PKG-1 packaging guard

(P2-S3 ile aynı)

---

## 3) ops-health-core

### [P2-O1] Add GitHub Actions CI + CI-0 hygiene gate

(P2-S1 ile aynı)

---

### [P2-O2] Standardize INV0 + INV2 gates

(P2-D2 ile aynı)

---

### [P2-O3] Promote kill-switch dominance + fail-closed exception tests to required gates

**Acceptance**
- dominance test PASS: `ops_deny_actions=True ⇒ deny_actions=True & recommended_action=HOLD`
- exception path test PASS

**Commands**
```bash
pytest -k "dominance or fail_closed" -v
```

---

### [P2-O4] PKG-1 packaging guard

(P2-S3 ile aynı)

---

## 4) evaluation-calibration-core

### [P2-E1] Add GitHub Actions CI + CI-0 hygiene gate

(P2-S1 ile aynı)

---

### [P2-E2] Standardize INV0 + INV2 gates

(P2-D2 ile aynı)

---

### [P2-E3] Promote INVARIANT 5 metric key set to required gate

**Acceptance**
- `test_invariant_5_metric_key_set` PASS (veya mevcut smoke)
- report metrics keys sabit set ile uyumlu

**Commands**
```bash
pytest -k "invariant_5 or metric_key_set" -v
```

---

### [P2-E4] PKG-1 packaging guard

(P2-S3 ile aynı)

---

## 5) mdm-engine

### [P2-M1] Add GitHub Actions CI + CI-0 hygiene gate

(P2-S1 ile aynı)

---

### [P2-M2] INV0 “0 exclude” — eliminate position_manager.py exclusion

**Acceptance**
- `tests/test_invariant_0_domain_agnosticism.py` core scan exclude list = empty
- `position_manager.py` ya **docs/examples** altına quarantine ya da domain-free rewrite

**Commands**
```bash
pytest tests/test_invariant_0_domain_agnosticism.py -v
```

**Invariants:** INV0

---

### [P2-M3] INV2 cross-core imports gate

(P2-D2 ile aynı)

---

### [P2-M4] Remove skip: replace legacy loop smoke with example-only test or delete

**Acceptance**
- `pytest -q` sonucu skip=0
- legacy loop varsa `docs/examples/**` altında

---

### [P2-M5] PKG-1 packaging guard

(P2-S3 ile aynı)

---

## 6) decision-ecosystem-integration-harness

### [P2-H1] CI split: core-only + full-stack jobs

**Acceptance**
- Job `core-only`: decision-schema + harness, skip=0
- Job `full-stack`: mdm+dmc+ops+eval kurulu, E2E smoke çalışıyor

---

### [P2-H2] E2E smoke required

**Acceptance**
- `tests/test_end_to_end_smoke.py` PASS (full-stack job’da)

---

### [P2-H3] Add P0 closure paragraph + evidence links to docs/P0_CLOSURE_CHECKLIST.md

**Acceptance**
- tek paragraf closure
- raw evidence linkleri (ci.yml, CI-0 test, INV0 test, checklist)

---

## Kanıt zinciri (P2 DONE sonrası)

- Her repo: **Actions** → Son run linki (green)
- Her repo: **pytest** → CI log’da PASS özeti
- mdm-engine: **skip=0** log kanıtı
- harness: **core-only** job green + **full-stack** (opsiyonel) özeti
