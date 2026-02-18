# Formulas and Metrics

This document defines the mathematical formulas and metrics used in the Decision Ecosystem using generic, domain-agnostic symbols.

## Notation

### Generic Symbols
- `x_t`: State at time `t`
- `a_t`: Action/proposal at time `t`
- `r_t`: Reward/outcome at time `t`
- `c_t`: Context at time `t`
- `s_t`: Signal at time `t`
- `DD_t`: Drawdown at time `t`
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

### Proposal Score
```
score(p, c_t) = f(x_t, c_t, θ)
```

Where:
- `p` is the generated proposal
- `c_t` is the current context
- `x_t` is the current state
- `θ` are model parameters
- `f` is the proposal generation function

### Context Encoding
```
c_t = encode(events, signals, history)
```

Context is encoded from:
- Recent events
- Current signals
- Historical patterns

## Risk Assessment (decision-modulation-core)

### Risk Score
```
risk(d) = Σᵢ wᵢ · gᵢ(d)
```

Where:
- `d` is the final decision
- `gᵢ` are guard functions
- `wᵢ` are guard weights

### Guard Evaluation
```
gᵢ(d) = {
  0 if guard passes
  1 if guard fails (hard guard)
  [0, 1] if guard modulates (soft guard)
}
```

### Modulation Factor
```
modulation(d) = 1 - risk(d) if risk(d) < threshold
modulation(d) = 0 if risk(d) ≥ threshold (fail-closed)
```

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

### Cumulative Outcome
```
R_T = Σₜ₌₁ᵀ r_t
```

### Average Outcome
```
R̄ = (1/T) · R_T
```

### Volatility
```
σ = √(E[(r_t - R̄)²])
```

### Drawdown
```
DD_t = max(0, peak_t - current_t)
peak_t = max(x₀, x₁, ..., x_t)
```

### Maximum Drawdown
```
MDD = max(DD_t for t ∈ [0, T])
```

### Sharpe-like Ratio (Risk-Adjusted Performance)
```
SR = R̄ / σ
```

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
∀d: risk(d) ≥ threshold → d.approved == false
```

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
- Domain-specific interpretations are provided only in `docs/examples/`
- Symbols follow mathematical conventions
- Formulas are testable and verifiable
