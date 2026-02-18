# Architecture Documentation

## Overview

This document describes the architecture of the Decision Ecosystem, a domain-agnostic decision stack for autonomous and AI-driven systems.

## System Architecture

### Core Components

The ecosystem consists of five independent cores:

1. **decision-schema**: Single Source of Truth (SSOT) contract
   - Defines types: `Proposal`, `FinalDecision`, `PacketV2`
   - Provides trace format specification
   - No runtime logic, pure contract definition

2. **mdm-engine**: Proposal Generation Runtime
   - Generates proposals ("what to do?")
   - Operates on context and state
   - Outputs `Proposal` objects conforming to schema

3. **decision-modulation-core**: Modulation and Safety Guards
   - Evaluates proposals ("should we do it?")
   - Applies guards and risk assessment
   - Modulates proposals based on safety constraints
   - Outputs `FinalDecision` objects

4. **ops-health-core**: Operational Safety
   - Monitors operational health signals
   - Implements kill-switch logic
   - Provides safety state to other cores via context

5. **evaluation-calibration-core**: Evidence Generation
   - Computes metrics and invariants
   - Generates evaluation reports
   - Calibrates system parameters

### Design Principles

#### Contract-First Architecture
- All cores depend only on `decision-schema`
- No cross-core dependencies
- Integration via shared types and context dictionaries

#### Domain Agnosticism
- Core vocabulary is universal: event, signal, state, context, proposal, decision
- No domain-specific assumptions in core logic
- Domain-specific implementations exist only as optional examples

#### Fail-Closed Safety
- Guards are deterministic and ordered
- Safety violations trigger fail-closed behavior
- Operational health signals can override decisions

#### Measurable Guarantees
- Invariants are testable
- Compatibility checks ensure contract compliance
- Metrics are defined with generic symbols

## Data Flow

```
Context + State
    ↓
[mdm-engine] → Proposal
    ↓
[decision-modulation-core] → FinalDecision
    ↓
[ops-health-core] → Safety Override (if needed)
    ↓
Execution + Trace (PacketV2)
    ↓
[evaluation-calibration-core] → Metrics + Reports
```

## Integration Pattern

### Via Contract Types
```typescript
// Example (language-agnostic concept)
import { Proposal, FinalDecision, PacketV2 } from 'decision-schema';

// mdm-engine generates
const proposal: Proposal = {
  action: {...},
  context: {...},
  metadata: {...}
};

// decision-modulation-core processes
const decision: FinalDecision = {
  proposal: proposal,
  guardResults: [...],
  riskScore: 0.85,
  approved: true
};

// Trace captured as PacketV2
const trace: PacketV2 = {
  timestamp: ...,
  proposal: proposal,
  decision: decision,
  execution: {...}
};
```

### Via Context Dictionaries
- Key-value pairs for cross-core communication
- No schema enforcement (flexibility)
- Documented conventions per integration

## Guard System

### Guard Ordering
Guards are applied in deterministic order:
1. Critical safety guards (fail-closed)
2. Risk assessment guards
3. Operational health guards
4. Domain-specific guards (if any, via adapters)

### Guard Types
- **Hard Guards**: Must pass, fail-closed if violated
- **Soft Guards**: Modulate risk score, may allow with warnings
- **Informational Guards**: Log only, no blocking

## Safety Mechanisms

### Kill-Switch Logic
- `ops-health-core` monitors system health
- Can override any decision if safety threshold exceeded
- Fail-closed by default

### Invariant Checking
- `evaluation-calibration-core` verifies invariants
- Reports violations for calibration
- Does not block execution (monitoring only)

## Extension Points

### Adapters
- Optional domain-specific adapters
- Must not modify core contract
- Clearly isolated and documented

### Custom Guards
- Can be added via modulation core
- Must follow guard interface
- Must be deterministic

## Performance Considerations

- Contract types are lightweight
- Context dictionaries allow lazy evaluation
- Trace packets support compression
- Guards are designed for low latency

## Testing Strategy

- Unit tests for each core independently
- Integration tests via contract types
- Invariant tests for contract compliance
- Compatibility tests for backward compatibility

## Future Considerations

- Distributed execution support
- Real-time streaming traces
- Advanced guard composition
- Multi-agent coordination patterns
