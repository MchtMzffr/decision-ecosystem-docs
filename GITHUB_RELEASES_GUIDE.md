# GitHub Releases Guide — Quick Reference

**Purpose:** Create GitHub Releases for patch releases  
**Estimated Time:** ~10 minutes per repository

---

## Release Checklist

For each repository, create a GitHub Release:

### Step 1: Navigate to Releases Page

| Repository | Releases URL |
|------------|--------------|
| decision-schema | https://github.com/MchtMzffr/decision-schema/releases/new |
| mdm-engine | https://github.com/MchtMzffr/mdm-engine/releases/new |
| ops-health-core | https://github.com/MchtMzffr/ops-health-core/releases/new |
| evaluation-calibration-core | https://github.com/MchtMzffr/evaluation-calibration-core/releases/new |
| execution-orchestration-core | https://github.com/MchtMzffr/execution-orchestration-core/releases/new |

### Step 2: Fill Release Form

**Tag version:**
- decision-schema: `v0.2.2` (latest), or `v0.2.1`
- mdm-engine: `v0.2.1`
- ops-health-core: `v0.1.1`
- evaluation-calibration-core: `v0.1.1`
- execution-orchestration-core: `v0.1.0`

**Release title:**
- `Release 0.2.2` / `Release 0.2.1` (decision-schema)
- `Release 0.2.1` (mdm-engine)
- `Release 0.1.1` (ops-health-core, evaluation-calibration-core)
- `Release 0.1.0` (execution-orchestration-core)

**Description:**
Copy content from `docs/RELEASE_NOTES_X.Y.Z.md` (or use body templates below):
- decision-schema: `docs/RELEASE_NOTES_0.2.2.md` (v0.2.2) or `RELEASE_NOTES_0.2.1.md`
- mdm-engine: `docs/RELEASE_NOTES_0.2.1.md`
- ops-health-core: `docs/RELEASE_NOTES_0.1.1.md`
- evaluation-calibration-core: `docs/RELEASE_NOTES_0.1.1.md`
- execution-orchestration-core: `docs/RELEASE_NOTES_0.1.0.md` or body template below

**Options:**
- ✅ Check "Set as the latest release"
- ✅ Check "Create a discussion for this release" (optional)

### Step 3: Publish

Click "Publish release"

---

## Release Notes Content (Quick Copy)

### decision-schema 0.2.1

```markdown
# Release Notes — decision-schema 0.2.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

## Summary

This patch release fixes INV-T1 external key validation to support both context keys (PARAMETER_INDEX) and trace-extension keys (INV-T1), resolving validation conflicts with harness context keys.

## Changes

### ✅ F1 — INV-T1 Two-Mode Validation

**Problem:** `validate_external_dict()` only accepted dot-separated keys (`harness.fail_closed`), but harness places plain context keys (`now_ms`, `run_id`, `ops_deny_actions`) into `external_snapshot`, causing validation failures.

**Solution:** Added two-mode validation:
- **Context keys:** Plain format `^[a-z0-9_]+$` (PARAMETER_INDEX keys)
- **Trace-extension keys:** Dot-separated format `^[a-z0-9_]+(\.[a-z0-9_]+)+$` (INV-T1 keys)
- **Both mode:** Accepts either format (default)

**Files Changed:**
- `decision_schema/trace_registry.py`: Added `CONTEXT_KEY_RE`, `TRACE_KEY_RE`, `mode` parameter
- `docs/PARAMETER_INDEX.md`: Documented context vs trace-extension keys
- `tests/test_invariant_t1_trace_key_registry.py`: Updated tests (14/14 passed)

**Invariant:** INV-T1.1 (format) and INV-T1.2 (registry) now correctly handle both key types.

## Backward Compatibility

✅ **Fully backward-compatible:**
- Default `mode="both"` accepts existing usage patterns
- No API changes (only new optional parameter)
- Existing code continues to work without modification

## Upgrade Path

`pip install "decision-schema>=0.2.1,<0.3"`
```

### decision-schema 0.2.2

```markdown
## decision-schema 0.2.2

Patch release extending the SSOT trace key registry.

### Changes
- Registered `exec.*` trace keys (owner: execution-orchestration-core)
- Reserved `exec` namespace in the ecosystem registry
- Tests and registry documentation updated accordingly

### Install
pip install "decision-schema>=0.2.2,<0.3"
```

### mdm-engine 0.2.1

```markdown
# Release Notes — mdm-engine 0.2.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

## Summary

This patch release adds batch flush support to `TraceLogger` for improved IO performance in high-throughput scenarios, while maintaining backward-compatible default behavior.

## Changes

### ✅ F5 — TraceLogger Batch Flush

**Problem:** `TraceLogger.write()` performed `flush()` on every write, creating an IO bottleneck for high-throughput scenarios.

**Solution:** Added configurable batch flush:
- `flush_every_n` parameter (default: 1, backward-compatible)
- Context manager pattern (`__enter__`/`__exit__`)
- Explicit `flush()` method
- Automatic flush on `close()`

**Files Changed:**
- `mdm_engine/trace/trace_logger.py`: Added batch flush support

**Performance:** For high-throughput scenarios, set `flush_every_n=100` or higher to reduce IO operations.

## Backward Compatibility

✅ **Fully backward-compatible:**
- Default `flush_every_n=1` maintains existing behavior
- No API changes (only new optional parameter)
- Existing code continues to work without modification

## Upgrade Path

`pip install "mdm-engine>=0.2.1,<0.3"`
```

### ops-health-core 0.1.1

```markdown
# Release Notes — ops-health-core 0.1.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

## Summary

This patch release fixes unbounded growth in timestamp lists by implementing in-place pruning, ensuring memory usage remains bounded over time.

## Changes

### ✅ F2 — Unbounded Growth Fix

**Problem:** `count_in_window()` pruned timestamps but didn't mutate state, causing `error_timestamps`, `rate_limit_timestamps`, and `reconnect_timestamps` to grow unbounded.

**Solution:** Added in-place pruning:
- `prune_timestamps_inplace()` function
- Called in `update_kill_switch()` before `compute_health_score()`
- Ensures timestamp lists remain bounded within window

**Files Changed:**
- `ops_health_core/windows.py`: Added `prune_timestamps_inplace()`
- `ops_health_core/kill_switch.py`: Call in-place prune before health score computation
- `ops_health_core/scorer.py`: Added TODO for latency_timestamps (future enhancement)

**Invariant:** `∀ts∈timestamps: ts ≥ now_ms - window_ms` (window bounded)

## Backward Compatibility

✅ **Fully backward-compatible:**
- No API changes
- Behavior improvement (memory efficiency)
- Existing code continues to work without modification

## Upgrade Path

`pip install "ops-health-core>=0.1.1,<0.2"`
```

### evaluation-calibration-core 0.1.1

```markdown
# Release Notes — evaluation-calibration-core 0.1.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

## Summary

This patch release documents the percentile calculation method (nearest-rank) for clarity and deterministic behavior understanding.

## Changes

### ✅ F6 — Percentile Documentation

**Problem:** `latency_percentiles()` used nearest-rank method but wasn't documented, leading to potential confusion about behavior (especially for small datasets).

**Solution:** Added comprehensive documentation:
- Method explanation: nearest-rank (`idx = floor((k/100) * n)`)
- Small n behavior note: "For small n, p95 and p99 may equal max value (expected behavior)"
- Alternative methods mentioned (linear interpolation)

**Files Changed:**
- `eval_calibration_core/metrics/definitions.py`: Enhanced docstring for `latency_percentiles()`

**Clarity:** Users now understand:
- How percentiles are calculated (deterministic nearest-rank)
- Why small datasets may show p95=p99=max (expected behavior)
- That the method is deterministic and simple

## Backward Compatibility

✅ **Fully backward-compatible:**
- No code changes (documentation only)
- No API changes
- Existing behavior unchanged

## Upgrade Path

`pip install "evaluation-calibration-core>=0.1.1,<0.2"`
```

### execution-orchestration-core 0.1.0

```markdown
## execution-orchestration-core 0.1.0

Initial release of the domain-agnostic execution orchestration core.

### Highlights
- Deterministic execution orchestration for FinalDecision actions (retries/timeouts/idempotency policies)
- Fail-closed behavior on exceptions + kill-switch gating
- Secret hygiene via structured redaction
- PacketV2 execution trace keys under the `exec.*` namespace

### Invariants
- INV-EXE-2: boundedness (max retries / max total time)
- INV-EXE-3: fail-closed on exception
- INV-EXE-4: kill-switch compliance
- INV-EXE-5: secret hygiene (redaction)
- INV-T1: trace key format compliance

### Compatibility
- Requires: decision-schema >= 0.2.2, < 0.3

### Install
If published to PyPI: `pip install "execution-orchestration-core==0.1.0"`
Otherwise install from GitHub tag: `pip install "git+https://github.com/MchtMzffr/execution-orchestration-core.git@v0.1.0"`
```

---

## Verification

After creating releases, verify:

1. **Release appears on repository's Releases page**
2. **Tag is marked as "Latest release"**
3. **Release notes are visible and formatted correctly**

---

**Last Updated:** 2026-02-18
