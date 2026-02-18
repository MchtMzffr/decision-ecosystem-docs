# Formulas and Metrics

This document defines the mathematical formulas and metrics used in the Decision Ecosystem using generic, domain-agnostic symbols.

## Notation

### Generic Symbols
- `x_t`: State at time `t`
- `a_t`: Action/proposal at time `t`
- `r_t`: Reward/outcome at time `t`
- `c_t`: Context at time `t`
- `s_t`: Signal at time `t`
- `DD_t`: Peak-to-trough decline at time `t` (generic; see “Example domain metrics” for naming notes)
- `σ_t`: Volatility/uncertainty at time `t`
- `θ`: Parameters/configuration
- `P(·)`: Probability
- `E[·]`: Expectation

### Decision Types
- `p`: Proposal (from mdm-engine)
- `d`: Final Decision (from decision-modulation-core)
- `g`: Guard result
- `h`: Health signal (from ops-health-core)

## Proposal Generation (mdm-engine)

### Proposal Score (abstract)
```
score(p, c_t) = f(x_t, c_t, θ)
```

Where:
- `p` is the generated proposal
- `c_t` is the current context
- `x_t` is the current state
- `θ` are model parameters
- `f` is the proposal generation function

Concrete reference formulas (moral scores W,J,H,C, Score, confidence, CUS) and the generic numeric scorer (e.g. 0.4·scale + 0.4·signal + 0.2·width, sigmoid confidence) are in **mdm-engine** `docs/FORMULAS.md`.

### Context Encoding
```
c_t = encode(events, signals, history)
```

Context is encoded from:
- Recent events
- Current signals
- Historical patterns

## Risk Assessment (decision-modulation-core)

**Current implementation: ordered hard guards.** Guards run in a fixed order; the **first** guard that fails yields fail-closed and evaluation stops. There is no weighted sum of guard outputs in the core.

### Guard order (deterministic)

1. Ops-health: `context["ops_deny_actions"] == True` → deny (HOLD/STOP)
2. Staleness: `(now_ms - last_event_ts_ms) > policy.staleness_ms` → HOLD
3. Error-rate, rate-limit, circuit-breaker, cooldown (policy thresholds) → HOLD on first failure

### Fail-closed

- Any guard returns fail → `FinalDecision(allowed=False, action=policy.fail_closed_action)` (e.g. HOLD or STOP)
- Any exception during guard evaluation → same fail-closed outcome

### Optional future model (risk score)

A possible future extension could define a risk score and modulation factor as:

- `risk(d) = Σᵢ wᵢ · gᵢ(d)` with `gᵢ ∈ {0,1}` or [0,1], and `modulation(d) = 1 - risk(d)` with a threshold for fail-closed. This is **not** the current implementation; the core uses ordered hard guards only.

## Operational Health (ops-health-core)

### Health Signal
```
h_t = health_monitor(x_t, history, thresholds)
```

Where:
- `h_t ∈ [0, 1]` (0 = critical, 1 = healthy)
- Thresholds define safety boundaries

### Kill-Switch Condition
```
kill_switch(d) = true if h_t < critical_threshold
kill_switch(d) = false otherwise
```

### Override Decision
```
d_final = {
  d if kill_switch(d) == false
  SAFE_DEFAULT if kill_switch(d) == true
}
```

## Evaluation Metrics (evaluation-calibration-core)

**Implemented in the core:** `action_distribution`, `guard_trigger_rates`, `safety_invariant_pass_rate`, `latency_percentiles` (and related confidence stats). See `evaluation-calibration-core/docs/FORMULAS.md`.

**General notation (optional / not computed by the core):** The following are domain-agnostic formulas for outcome/reward aggregates; the core does not currently compute them.

### Cumulative Outcome (general notation)
```
R_T = Σₜ₌₁ᵀ r_t
```

### Average Outcome (general notation)
```
R̄ = (1/T) · R_T
```

### Volatility (general notation)
```
σ = √(E[(r_t - R̄)²])
```

### Peak-to-trough decline (generic)
```
DD_t = max(0, peak_t - current_t)
peak_t = max(x₀, x₁, ..., x_t)
```
Interpretation: decline from running maximum; domain-agnostic.

### Maximum decline over horizon
```
MDD = max(DD_t for t ∈ [0, T])
```

### Risk-adjusted outcome ratio (generic)
```
SR = R̄ / σ
```
Interpretation: mean outcome per unit variability; domain-agnostic. (In some domains this is known as a Sharpe-like ratio; we keep the formula and core vocabulary generic. Domain-specific names are for illustration only.)

### Guard Compliance Rate
```
compliance_rate = (guards_passed / total_guards) × 100%
```

### Proposal Acceptance Rate
```
acceptance_rate = (decisions_approved / total_proposals) × 100%
```

## Invariants

### Invariant 1: Fail-Closed Behavior
```
∀d: (any guard fails in order) → d.approved == false
```
(In the current implementation, the first failing guard yields fail-closed; no risk-score threshold.)

### Invariant 2: Guard Ordering Determinism
```
guard_order(d₁) == guard_order(d₂) if d₁.context == d₂.context
```

### Invariant 3: Contract Compliance
```
∀p: p ∈ Proposal → schema.validate(p) == true
∀d: d ∈ FinalDecision → schema.validate(d) == true
```

### Invariant 4: Health Override
```
∀d: h_t < critical_threshold → d_final == SAFE_DEFAULT
```

## Calibration Formulas

### Parameter Update (Gradient-based)
```
θ_{t+1} = θ_t - α · ∇_θ loss(θ_t, data_t)
```

Where:
- `α` is learning rate
- `loss` is the calibration loss function
- `data_t` is the training data at time `t`

### Loss Function (Example)
```
loss(θ) = E[(predicted_outcome - actual_outcome)²] + λ · regularization(θ)
```

Where:
- `λ` is regularization weight
- `regularization` prevents overfitting

## Confidence Intervals

### Outcome Prediction Interval
```
CI_α = [μ - z_α/2 · σ/√n, μ + z_α/2 · σ/√n]
```

Where:
- `μ` is mean outcome
- `σ` is standard deviation
- `n` is sample size
- `z_α/2` is critical value for confidence level `α`

## Time-Decay Functions

### Exponential Decay (for historical weighting)
```
w_t = exp(-λ · (T - t))
```

Where:
- `λ` is decay rate
- `T` is current time
- `t` is historical time point

## Aggregation Functions

### Weighted Average
```
x̄_weighted = Σᵢ wᵢ · xᵢ / Σᵢ wᵢ
```

### Moving Average
```
MA_t = (1/n) · Σᵢ₌ₜ₋ₙ⁺¹ᵗ xᵢ
```

## Notes

- All formulas use generic symbols suitable for any domain
- Domain-specific interpretations (e.g. finance-origin names like “drawdown”, “Sharpe”) are only in `docs/examples/` or in adapter layers; core vocabulary stays domain-agnostic
- Symbols follow mathematical conventions
- Formulas are testable and verifiable
