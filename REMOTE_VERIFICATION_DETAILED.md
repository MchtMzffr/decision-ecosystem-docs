# Remote Verification — Detailed Report

**Date:** 2026-02-17  
**Method:** Git remote inspection + raw.githubusercontent.com fetch

---

## Verification Method

1. ✅ **Git remote log inspection** — Check commit history
2. ✅ **Git show origin/main** — Verify file contents in remote
3. ✅ **raw.githubusercontent.com fetch** — Cross-check with GitHub raw URLs

---

## F5 — TraceLogger Batch Flush (mdm-engine)

### Remote Commit History

```
32b7a8d perf(F5): Add batch flush support to TraceLogger
```

**Status:** ✅ **COMMIT EXISTS in origin/main**

### Remote File Contents (git show origin/main)

```python
class TraceLogger:
    """
    Append PacketV2 as JSONL (input/external must be pre-redacted).
    
    Performance: Flushes every N writes (default: every write for safety, set flush_every_n for batch).
    """

    def __init__(self, run_dir: Path, flush_every_n: int = 1):
        """
        Initialize trace logger.
        
        Args:
            run_dir: Directory for traces.jsonl
            flush_every_n: Flush every N writes (1 = flush every write, higher = batch flush)
        """
        # ... flush_every_n, _write_count initialized ...

    def write(self, packet: PacketV2) -> None:
        """Write packet to JSONL (flush based on flush_every_n)."""
        line = json.dumps(packet.to_dict(), default=str) + "\n"
        self._file.write(line)
        self._write_count += 1
        if self._write_count >= self._flush_every_n:
            self._file.flush()
            self._write_count = 0

    def flush(self) -> None:
        """Force flush buffer."""
        self._file.flush()

    def close(self) -> None:
        """Close file (flushes before closing)."""
        self.flush()
        self._file.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit (ensures flush and close)."""
        self.close()
```

**Status:** ✅ **CODE VERIFIED in origin/main**

### raw.githubusercontent.com Fetch

**URL:** https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/mdm_engine/trace/trace_logger.py

**Result:** ✅ **Batch flush code present** (flush_every_n, counter, context manager)

---

## F6 — Percentile Documentation (evaluation-calibration-core)

### Remote Commit History

```
d43753a docs(F6): Document percentile calculation method
```

**Status:** ✅ **COMMIT EXISTS in origin/main**

### Remote File Contents (git show origin/main)

```python
@staticmethod
def latency_percentiles(packets: list[Any]) -> dict[str, float]:
    """
    Compute latency percentiles using nearest-rank method.
    
    Formula (nearest-rank):
        p_k = value at index = floor((k/100) * n)
        For k=95, n=100: index = 95 (0-indexed: 94)
    
    Method: Nearest-rank (deterministic, simple)
    - Alternative: Linear interpolation (smoother but more complex)
    - For small n, p95 and p99 may equal max value (expected behavior)
    
    Args:
        packets: List of PacketV2 packets
    
    Returns:
        Dict with p50, p95, p99 keys (milliseconds)
    """
    # ... implementation ...
    
    def percentile(p: float) -> float:
        """Nearest-rank percentile: index = floor((p/100) * n)."""
        idx = int((p / 100.0) * n)
        return sorted_latencies[min(idx, n - 1)]
```

**Status:** ✅ **DOCUMENTATION VERIFIED in origin/main**

### raw.githubusercontent.com Fetch

**URL:** https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/main/eval_calibration_core/metrics/definitions.py

**Result:** ✅ **Nearest-rank documentation present** (method explanation + small n behavior note)

---

## Possible Discrepancy Explanations

### 1. GitHub Cache/CDN Delay

**Issue:** raw.githubusercontent.com may serve cached content  
**Solution:** Wait 5-10 minutes, or use `?v=<timestamp>` query parameter

### 2. Browser Cache

**Issue:** Browser may cache old version  
**Solution:** Hard refresh (Ctrl+F5) or use incognito mode

### 3. Different Commit Hash

**Issue:** User may be viewing different commit  
**Solution:** Verify commit hash matches `32b7a8d` (mdm-engine) and `d43753a` (eval-calibration-core)

### 4. Branch Mismatch

**Issue:** User may be viewing `master` instead of `main`  
**Solution:** Verify URL uses `/main/` not `/master/`

---

## Verification Commands (For User)

### mdm-engine

```bash
cd mdm-engine
git fetch origin
git log origin/main --oneline -5
git show origin/main:mdm_engine/trace/trace_logger.py | grep -A 5 "flush_every_n"
```

**Expected:** `flush_every_n`, `_write_count`, `flush()`, `__enter__`, `__exit__`

### evaluation-calibration-core

```bash
cd evaluation-calibration-core
git fetch origin
git log origin/main --oneline -5
git show origin/main:eval_calibration_core/metrics/definitions.py | grep -A 10 "nearest-rank"
```

**Expected:** "nearest-rank method", "floor((k/100) * n)", "small n" note

---

## Conclusion

✅ **F5 commit verified:** `32b7a8d` in origin/main  
✅ **F6 commit verified:** `d43753a` in origin/main  
✅ **Code verified:** Both fixes present in remote `main` branch  
✅ **raw.githubusercontent.com verified:** Both fixes fetchable

**If user still sees old code:**
1. Check browser cache (hard refresh)
2. Verify URL uses `/main/` not `/master/`
3. Wait 5-10 minutes for CDN cache refresh
4. Use git commands above for definitive verification

---

**Last Updated:** 2026-02-17  
**Verification Method:** Git remote inspection + raw.githubusercontent.com fetch
