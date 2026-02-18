# Integration Guide

This guide explains how to integrate the Decision Ecosystem cores and build domain-specific decision systems.

## Prerequisites

- Understanding of `decision-schema` contract types
- Familiarity with your domain's decision requirements
- Access to core repositories

## Core Integration Pattern

### Step 1: Understand the Contract

Start with `decision-schema` to understand:
- `Proposal` type structure
- `FinalDecision` type structure
- `PacketV2` trace format
- Context dictionary conventions

### Step 2: Choose Your Cores

Select which cores you need:
- **mdm-engine**: If you need proposal generation
- **decision-modulation-core**: If you need guards and risk assessment
- **ops-health-core**: If you need operational safety monitoring
- **evaluation-calibration-core**: If you need metrics and evaluation

### Step 3: Implement Domain Adapter (Optional)

If you need domain-specific logic:
1. Create adapter in separate module
2. Map domain concepts to contract types
3. Keep adapter isolated from cores
4. Document in `docs/examples/[your-domain]/`

## Integration Examples

### Minimal Integration (Single Core)

```python
# Example: Using only mdm-engine
from decision_schema import Proposal
from mdm_engine import generate_proposal

context = {
    "state": {...},
    "signals": {...}
}

proposal = generate_proposal(context)
# proposal is a Proposal type from decision-schema
```

### Full Stack Integration

```python
# Example: Using all cores
from decision_schema import Proposal, FinalDecision, PacketV2
from mdm_engine import generate_proposal
from decision_modulation_core import evaluate_proposal
from ops_health_core import check_health, apply_kill_switch
from evaluation_calibration_core import record_trace, compute_metrics

# 1. Generate proposal
context = {...}
proposal = generate_proposal(context)

# 2. Evaluate with guards
decision = evaluate_proposal(proposal, context)

# 3. Check operational health
health_signal = check_health(context)
if health_signal < critical_threshold:
    decision = apply_kill_switch(decision)

# 4. Execute (your domain logic)
if decision.approved:
    result = execute_action(decision.proposal.action)

# 5. Record trace
trace = PacketV2(
    timestamp=now(),
    proposal=proposal,
    decision=decision,
    execution=result
)
record_trace(trace)

# 6. Compute metrics (async/background)
metrics = compute_metrics([trace])
```

## Context Dictionary Conventions

### Standard Keys (Optional but Recommended)
- `state`: Current system state
- `signals`: Current signals/observations
- `history`: Historical data (compressed)
- `metadata`: Domain-specific metadata

### Domain-Specific Keys
- Use namespaced keys: `domain:key` (e.g., `robotics:position`)
- Document in your adapter
- Keep core logic domain-agnostic

## Guard Integration

### Adding Custom Guards

```python
from decision_modulation_core import Guard, GuardResult

class CustomGuard(Guard):
    def evaluate(self, proposal: Proposal, context: dict) -> GuardResult:
        # Your guard logic
        passes = self.check_condition(proposal, context)
        return GuardResult(
            guard_id="custom_guard",
            passed=passes,
            score=0.0 if passes else 1.0,
            message="Custom guard evaluation"
        )

# Register guard
register_guard(CustomGuard(), priority=100)
```

### Guard Priority
- Lower priority = evaluated first
- Hard guards should have priority < 50
- Soft guards should have priority >= 50

## Health Signal Integration

### Providing Health Signals

```python
from ops_health_core import HealthSignal, register_health_provider

class CustomHealthProvider:
    def get_health(self, context: dict) -> HealthSignal:
        # Compute health from your domain
        health_value = self.compute_health(context)
        return HealthSignal(
            value=health_value,
            critical_threshold=0.2,
            source="custom_provider"
        )

register_health_provider(CustomHealthProvider())
```

## Evaluation Integration

### Custom Metrics

```python
from evaluation_calibration_core import Metric, register_metric

class CustomMetric(Metric):
    def compute(self, traces: List[PacketV2]) -> float:
        # Your metric computation
        return self.calculate_metric(traces)

register_metric(CustomMetric())
```

## Domain Adapter Pattern

### Adapter Structure

```
your-domain-adapter/
├── README.md              # Domain-specific documentation
├── adapter.py             # Main adapter code
├── domain_types.py        # Domain type mappings
├── examples/              # Domain examples
└── tests/                 # Adapter tests
```

### Adapter Example

```python
# adapter.py
from decision_schema import Proposal, FinalDecision

class DomainAdapter:
    """Adapter for [Your Domain]"""
    
    def domain_to_proposal(self, domain_action) -> Proposal:
        """Convert domain action to Proposal"""
        return Proposal(
            action=self._map_action(domain_action),
            context=self._build_context(domain_action),
            metadata={"domain": "your_domain"}
        )
    
    def decision_to_domain(self, decision: FinalDecision):
        """Convert FinalDecision to domain format"""
        if decision.approved:
            return self._map_to_domain_action(decision.proposal)
        return None
```

## Testing Integration

### Unit Tests
- Test each core independently
- Mock contract types
- Verify contract compliance

### Integration Tests
- Test full decision flow
- Verify trace generation
- Check guard application

### Compatibility Tests
- Test with different schema versions
- Verify backward compatibility
- Check parameter validation

## Performance Considerations

### Async Processing
- Evaluation and metrics can be async
- Proposal generation should be synchronous for real-time decisions
- Traces can be batched

### Caching
- Cache proposal generation results if context unchanged
- Cache guard evaluations for repeated proposals
- Cache health signals with TTL

### Optimization
- Minimize context dictionary size
- Compress historical data
- Use efficient trace storage

## Error Handling

### Contract Violations
```python
from decision_schema import SchemaValidationError

try:
    proposal = generate_proposal(context)
except SchemaValidationError as e:
    # Handle contract violation
    log_error(e)
    return safe_default_proposal()
```

### Guard Failures
```python
decision = evaluate_proposal(proposal, context)
if not decision.approved:
    # Handle guard failure
    log_guard_failure(decision.guard_results)
    return safe_default_decision()
```

## Deployment Considerations

### Core Deployment
- Deploy cores as independent services (optional)
- Or integrate as libraries
- Ensure `decision-schema` version compatibility

### Monitoring
- Monitor proposal generation latency
- Track guard failure rates
- Monitor health signals
- Alert on kill-switch activations

## Migration Guide

### From Domain-Specific to Ecosystem

1. Identify decision points in your system
2. Map to `Proposal` and `FinalDecision` types
3. Extract guards and risk logic
4. Implement health monitoring
5. Add trace recording
6. Gradually migrate decision logic

### Version Upgrades

- Check `decision-schema` version compatibility
- Update core dependencies
- Run compatibility tests
- Update adapters if contract changed

## Best Practices

1. **Start Small**: Begin with one core, add others gradually
2. **Keep Adapters Thin**: Domain logic in adapters, not cores
3. **Test Contracts**: Always validate contract compliance
4. **Monitor Health**: Set up health signal monitoring early
5. **Document Domain Mappings**: Clearly document how domain concepts map to contract types

## Getting Help

- Review `docs/ARCHITECTURE.md` for system design
- Check `docs/FORMULAS.md` for metric definitions
- See `docs/examples/` for domain-specific examples
- Consult core repository documentation
