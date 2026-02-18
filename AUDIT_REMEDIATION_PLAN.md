# Audit Remediation Plan — Domain-Agnosticism & Contract Purity

**Kaynak:** Public surface audit (commit SHA'lar üzerinden).  
**Sonuç:** "100% compliant" iddiası repo gerçekliğiyle uyuşmuyor. Contract ve core kod yüzeyinde ciddi domain sızıntısı var.

---

## Tanımlar (SSOT)

- **Public surface:** `README.md` + `docs/**` (docs/examples hariç) + paketlenen Python modülleri + exported type/identifier'lar.
- **INVARIANT 0 (Domain-agnosticism):** Public surface içinde domain-spesifik lexeme/identifier **0 adet**. Domain örnekleri yalnızca `docs/examples/**` altında.
- **Contract purity (decision-schema):** `decision_schema.types.*` ve PacketV2 alan/alias isimleri domain vocabulary içermez.

---

## Bulgu Özeti

| Repo | Durum | Ana ihlaller |
|------|--------|---------------|
| decision-schema | Contract domain vocabulary | QUOTE/FLATTEN/CANCEL_ALL, bid_quote/ask_quote/size_usd/post_only, TradeProposal alias, docstring'de "trading" |
| decision-modulation-core | INVARIANT 0 + cross-core | spread/liquidity/inventory/pnl/adverse_selection, dmc_core.schema re-export |
| mdm-engine | INVARIANT 0 + cross-core import | PositionManager, order_manager, bid_quote/pnl, run_loop'ta dmc_core import |
| ops-health-core | Genel olarak OK | Docs'ta DMC import örneği "core depends on core" algısı |
| evaluation-calibration-core | Metric key tutarsızlığı | compute: `guard_trigger_rate` vs docs: `guard_trigger_rates` |

---

## Invariant Seti (Test Olarak Eklenecek)

1. **INVARIANT 0:** Hard-term regex; public surface'de 0 match (exclude: docs/examples, examples).
2. **INVARIANT 1 (Contract purity):** Action whitelist {HOLD, ACT, EXIT, CANCEL, STOP}; Proposal/FinalDecision field whitelist (domain field yok).
3. **INVARIANT 2 (No cross-core imports):** AST scan; core paketlerinde yalnız `decision_schema` import.
4. **INVARIANT 3 (DMC):** Deterministic guard ordering.
5. **INVARIANT 4:** Fail-closed (exception → allowed=False, action in {HOLD, STOP}).
6. **INVARIANT 5 (Eval):** Metric output key set sabit ve docs ile aynı.

---

## Patch Planı (Kısa Referans)

### A) decision-schema 0.2.0 (breaking)
- types.py: QUOTE/FLATTEN/CANCEL_ALL, bid_quote/ask_quote/size_usd/post_only, TradeProposal/FinalAction alias KALDIR.
- Sadece params dict; domain key'ler namespaced.
- DEPRECATION/INTEGRATION örnekleri → docs/examples/example_domain_legacy_migration.md.
- PARAMETER_INDEX: PacketV2'de context yok, "Integration Context Dictionary" olarak düzelt.

### B) decision-modulation-core
- modulator/guards: domain guard'ları kaldır; generic set: ops_health, staleness, rate_limit, error_budget, latency, cooldown, budget.
- dmc_core.schema kaldır; doğrudan decision_schema.
- pnl_metrics + finance guard'lar → docs/examples/example_domain_finance_like/.

### C) mdm-engine
- order_manager, position_manager, run_loop (dmc import + pnl) → docs/examples.
- Core: sadece propose(event, features, context) → Proposal; DMC import 0.

### D) ops-health-core
- INTEGRATION_GUIDE: DMC örneğini "integration layer" olarak etiketle.
- Test: fail-closed, score ∈ [0,1].

### E) evaluation-calibration-core
- Canonical key: guard_trigger_rates (compute + docs aynı).
- Test: output key set assert (INVARIANT 5).

---

## SemVer

- decision-schema: 0.1.x → **0.2.0**
- Tüm core'lar: `decision-schema>=0.2,<0.3`
- ECOSYSTEM_CONTRACT_MATRIX güncelle.

---

Bu dosya, audit bulgularına göre remediation'ın tek referansıdır. Uygulama sırası: A → B, C (paralel), D, E.

---

## Preflight Reality Check (main vs local)

**Değerlendirme:** MeetlyTR/main (raw) üzerinden yapıldığında A/D/E değişiklikleri main'de görünmüyor; local workspace'ta uygulanmış durumda.

| Ne | MeetlyTR/main (raw) | Bu workspace (local) |
|----|----------------------|------------------------|
| decision-schema | version 0.1.0; types legacy alias | 0.2.0; types domain-agnostic |
| evaluation-calibration | guard_trigger_rate; writer aynı | guard_trigger_rates; writer + INV5 test |
| ops-health | DMC import algısı; pin 0.1 | "integration layer only"; pin 0.2; fail-closed test |

**Sonuç:** B/C patch'leri **local branch** (bu workspace) üzerine uygulanır. Main'e push/merge sonrası preflight main ile aynı hizaya gelir.
