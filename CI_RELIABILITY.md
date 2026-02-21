<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# CI Reliability Guide

**Purpose:** Why CI may occasionally fail and what we did to reduce it.

---

## Is "occasional failure" normal?

Partly **yes**. The following can cause one-off or transient failures; we cannot eliminate them entirely, but we can **reduce** them.

---

## Possible causes

| Cause | Description | Mitigation |
|-------|-------------|------------|
| **Network / PyPI / GitHub** | `pip install` or `git clone` timeout, transient outage | **Single retry** on pip steps (wait and retry once, then git fallback) |
| **Job hang** | Step stops responding and the run runs for hours | **timeout-minutes** on every job (15–25 min) |
| **Concurrency cancel** | When a new push is made, the previous run is **cancelled** | This is not a "failure" but **cancelled**; appears as "Cancelled" in the UI |
| **Single matrix fail** | With default `fail-fast: true`, one Python version failing cancels the other | **fail-fast: false** so 3.11 and 3.12 finish separately and it is clear which environment failed |
| **Ruff / lint** | CI runs `ruff check` and `ruff format --check` (no auto-fix). If you push without running lint locally, CI fails. | **Run before push:** `pre-commit run --all-files` or `ruff check . && ruff format .`. CI pins Ruff to match `.pre-commit-config.yaml` (v0.8.x). |

---

## Improvements applied (all repos)

1. **Job timeout**
   - `timeout-minutes: 15` (single-job workflows)
   - `timeout-minutes: 20` (integration-harness core_only)
   - `timeout-minutes: 25` (integration-harness full_stack)

2. **Pip retry**
   - Test runner: `pip install ... \|\| (sleep 15 && pip install ...)`
   - Dependencies: `pip install pkg... \|\| (sleep 20 && pip install pkg...) \|\| pip install git+...`
   - So a transient network error does not fail on the first attempt.

3. **fail-fast: false**
   - In the matrix (e.g. 3.11, 3.12), if one cell fails the other still runs; reporting is clearer.

4. **decision-schema pin (cores)**
   - All cores use `>=0.2.2` and fallback `@v0.2.2`; consistent with a single SSOT version.

---

## What you see in the UI

- **Failed (red):** At least one step actually failed. Check the log; the cause is often on the "pip" or "pytest" line.
- **Cancelled (grey):** A new push cancelled this run. Not a code bug; you can "Re-run all jobs" to run the same commit again.
- **Success (green):** All steps passed.

---

## Can we guarantee no failures?

**We cannot guarantee 100%** (network, GitHub/PyPI outages, runner issues are outside our control). With the above:

- Transient network errors are largely **recovered** by retry.
- Hanging jobs are **stopped** by timeout, so we avoid runs that wait forever.
- **fail-fast: false** makes it clear which Python/environment failed.

Optional extras: for flaky tests, pytest `--flake-finder` or `@pytest.mark.flaky(retries=2)` on specific tests; currently workflow-level mitigations are in place.

---

## Repos updated

- decision-schema  
- mdm-engine  
- ops-health-core  
- evaluation-calibration-core  
- decision-modulation-core  
- execution-orchestration-core  
- decision-ecosystem-integration-harness  

All use the same pattern: `timeout-minutes`, `fail-fast: false`, pip retry.

---

**Last updated:** 2026-02-18
