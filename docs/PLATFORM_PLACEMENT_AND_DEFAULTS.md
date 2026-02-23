<!--
Decision Ecosystem - decision-ecosystem-docs
Copyright (c) 2026 Mucahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Platform Layer — SSOT (Placement, Invariants, API, Tests)

**Purpose:** Single-page SSOT for the Decision Center / Platform layer: file tree, invariants, minimal endpoint contract, and test plan. Platform lives inside the harness repo under `harness/platform/`; it does not change pipeline semantics (INV-PLAT-ISOLATION-1).

**References:** DECISION_CENTER_GAPS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, REPO_REGISTRY.md.

---

## 1. File tree (harness repo)

```
harness/
  run_one_step.py          # Pipeline SSOT — unchanged by platform
  packet_builder.py
  redaction.py
  __init__.py              # Re-exports run_one_step + platform (create_app, serve, catalog, control, store)
  __main__.py              # python -m harness --host ... --port ... --store memory|file|off
  platform/
    __init__.py            # Re-exports catalog, control, store
    gateway.py             # POST /decide, POST /decision (legacy), GET/POST /control, GET /health
    catalog.py             # get_context_overrides(tenant_id), get_policy_defaults(), merge_context()
    store.py               # save(packet, report?, explanation?, backend=memory|file|off)
    control.py             # get_ops_state(), set_ops_state(), set_red(), set_green(), clear_ops_override()
    adapters/
      __init__.py          # get_adapter(name), BaseAdapter, Example domain adapters
      base.py              # BaseAdapter (to_state_context, to_domain_output)
      example_domain_agent_tool_use.py
      example_domain_content_moderation.py
      example_domain_lending.py
      example_domain_ops_automation.py
      example_domain_scheduling.py
      example_domain_triage.py
      example_domain_trading.py
```

**Invariant INV-PLAT-ISOLATION-1:** Platform modules do not change pipeline semantics; they only orchestrate. Pipeline SSOT remains `harness.run_one_step` (unchanged).

---

## 2. Invariants

| ID | Definition | Where enforced |
|----|------------|----------------|
| **INV-PLAT-ISOLATION-1** | Platform does not change pipeline semantics; only orchestration (call run_one_step, merge context, persist). | Design; gateway only calls run_one_step. |
| **INV-DEPS-OPTIONAL-1** | Core install is minimal; server (FastAPI/uvicorn) only with `[gateway]` or `[server]` extra. `python -m harness --serve` without extra ⇒ fail with message. | pyproject.toml optional-dependencies; gateway.py ImportError message. |
| **INV-ADAPTER-DOMAIN-LEAK-1** | Adapter names and docs carry "Example domain" label; no production domain in public API. | harness/platform/adapters/*.py docstrings and names (example_domain_*). |
| **INV-GW-FAILCLOSED-1** | Gateway exception ⇒ response with `allowed=false`, packet trace marker (e.g. `gateway_fail_closed`). | harness/platform/gateway.py _run_and_respond. |
| **INV-GW-DET-1** | Same input + policy ⇒ same PacketV2/decision (determinism). | Pipeline; tests. |
| **INV-STORE-SEC-1** | Store never writes when `packet.external["harness.redaction_applied"] != True` (fail-closed). | harness/platform/store.py save(); packet_builder sets marker when redact_input and redact_external. |
| **INV-STORE-NO-PII-1** | Store refuses write if payload matches secret/PII patterns (minimal regex set). | harness/platform/store.py _has_secret_pattern(). |
| **INV-GW-CTRL-LOCK-1** | Control mutation endpoint (GET/POST /control) default disabled; enable via DECISION_GATEWAY_ENABLE_CONTROL=1 or create_app(enable_control_endpoints=True). | harness/platform/gateway.py; 403 when disabled. |
| **INV-GW-AUTH-1** | When control enabled, X-Decision-Control-Token or Authorization: Bearer must match DECISION_CONTROL_TOKEN; else 401. | harness/platform/gateway.py _control_token_ok(). |
| **INV-CTRL-DOM-1** | Kill-switch ON ⇒ all decisions deny (ops-health dominance). | DMC ops_health_guard; control merges ops state into context. |
| **INV-ADAPTER-REG-1** | Every adapter in registry is importable and implements BaseAdapter. | harness/platform/adapters/__init__.py; test_inv_adapter_reg_det. |
| **INV-ADAPTER-DET-1** | Same domain_input ⇒ same (state, context) when serialized (order-stable JSON). | Adapters; test_inv_adapter_reg_det. |
| **INV-STORE-PATH-1** | Default store path only under allowlist (e.g. cwd or ./artifacts); absolute path only with explicit allow_absolute_path=True. | harness/platform/store.py save(); test_inv_store_sec_1. |
| **INV-GW-SIZE-1** | Request body size upper bound (default 256KB); over limit ⇒ 413. | harness/platform/gateway.py middleware; test_inv_gw_size_rl. |
| **INV-GW-RL-1** | In-memory per-IP rate limit (key: client IP; optional future: per-tenant); over limit ⇒ 429 with Retry-After, X-RateLimit-Limit/Remaining/Reset. | harness/platform/gateway.py _rate_limit; test_inv_gw_size_rl. |
| **INV-API-SURFACE-1** (P1) | Top-level harness exports minimal; platform API under harness.platform.*. | Docs; DEPRECATION_POLICY.md; future removal at 1.0. |

---

## 3. Minimal API contract

### Gateway

- **POST `/decide`** (domain-agnostic)
  - **Input:** `{ "adapter": "example_domain_lending" | "example_domain_scheduling" | "example_domain_trading" | "example_domain_content_moderation" | "example_domain_ops_automation" | "example_domain_triage" | "example_domain_agent_tool_use" | null, "input": {...}, "tenant": "...", "policy_id": "...", "idempotency_key": "...", "run_id": "...", "step": 0 }`
  - If `adapter` is set: `input` → adapter.to_state_context() → (state, context). Else: `input.state`, `input.context` (or input as state).
  - **Output:** `{ "final_decision": {...}, "packet": {...}, "report_suite": ..., "domain_output": ... (if adapter) }`
- **POST `/decision`** (legacy)
  - **Input:** `{ "state": {...}, "context": {...}, "run_id": "...", "step": 0, "tenant_id": "..." }`
  - **Output:** same shape as /decide (no domain_output).
- **GET `/control`**, **POST `/control`** (INV-GW-CTRL-LOCK-1): Default **disabled** (403). Enable with `DECISION_GATEWAY_ENABLE_CONTROL=1` or `create_app(enable_control_endpoints=True)`. When enabled (INV-GW-AUTH-1): require header `X-Decision-Control-Token` or `Authorization: Bearer <token>` matching `DECISION_CONTROL_TOKEN`; else 401.
- **Rate limit (INV-GW-RL-1):** Over limit ⇒ 429 with `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Key: per-IP (deterministic); optional future: per-tenant.
- **GET `/health`** ⇒ `{ "status": "ok" }`.

### Store

- `save(packet, report=None, explanation=None, backend="memory"|"file"|"off", path=...)`
- INV-STORE-SEC-1: Does not write when `packet.external.get("harness.redaction_applied") is not True` (fail-closed).
- INV-STORE-NO-PII-1: Does not write if payload matches secret/PII patterns (minimal regex set).
- Default: no-op when backend is `off` or not configured; caller enables persistence. File backend: flush + fsync after append.

### Control

- `get_ops_state()`, `set_ops_state(...)`, `set_red()`, `set_green()`, `clear_ops_override()`.

**Safety default:** Gateway crash/exception ⇒ fail-closed (allowed=false) + packet trace marker (INV-GW-FAILCLOSED-1).

---

## 4. Test plan (invariants)

| Invariant | Test / CI |
|-----------|-----------|
| INV-GW-FAILCLOSED-1 | Gateway exception ⇒ 500 + final_decision.allowed=false, reasons include gateway_fail_closed. |
| INV-GW-DET-1 | Same (state, context, now_ms) ⇒ same final_decision/packet (pytest). |
| INV-STORE-SEC-1 | test_inv_store_sec_1_redaction_required (no marker ⇒ no write); test_inv_store_sec_1_redaction_applied_writes. |
| INV-STORE-NO-PII-1 | test_inv_store_no_pii_1_token_pattern_fails (payload with sk-* ⇒ no write). |
| INV-GW-CTRL-LOCK-1 | test_inv_gw_ctrl_lock_1_default_disabled (GET/POST /control ⇒ 403 when disabled). |
| INV-GW-AUTH-1 | test_inv_gw_auth_1_token_required (enabled, no token ⇒ 401; valid token ⇒ 200). |
| INV-CTRL-DOM-1 | set_red(); run_one_step with context merged from get_ops_state() ⇒ allowed=false (existing kill-switch tests). |
| INV-DEPS-OPTIONAL-1 | Install without [gateway]; import harness works; create_app() or serve() raises ImportError with message. |
| INV-ADAPTER-DOMAIN-LEAK-1 | test_inv_adapter_domain_leak_1_no_bare_domain_modules (adapter modules must have example_domain_ prefix). |
| INV-ADAPTER-REG-1 | test_inv_adapter_reg_det: get_adapter(name) returns BaseAdapter for each registry name. |
| INV-ADAPTER-DET-1 | test_inv_adapter_reg_det: same domain_input ⇒ same JSON (sort_keys) for (state, context). |
| INV-STORE-PATH-1 | test_inv_store_sec_1: save(..., path=absolute, allow_absolute_path=False) ⇒ ValueError. |
| INV-GW-SIZE-1 | test_inv_gw_size_rl: body over max_body_bytes ⇒ 413. |
| INV-GW-RL-1 | test_inv_gw_size_rl: requests over DECISION_GATEWAY_RATE_MAX in window ⇒ 429. |

**CI:** `pytest tests/ -k "platform or inv_gw or inv_store or inv_ctrl"` (and existing fullstack tests). Optional: JSON artifact for PROOF-STD alignment.

---

### 4.1 Adapter PR checklist (fail-closed)

Before merging a new adapter:

- **INV-ADAPTER-DOMAIN-LEAK-1** (prefix): Adapter module name and public surface use `example_domain_*`; no production domain in public API. Test: `test_inv_adapter_domain_leak_1_*` PASS.
- **INV-ADAPTER-REG-1**: Adapter is in registry and `get_adapter(name)` returns a `BaseAdapter` instance. Test: `test_inv_adapter_reg_det` PASS.
- **INV-ADAPTER-DET-1**: Same `domain_input` ⇒ same `(state, context)` (order-stable JSON). Test: `test_inv_adapter_reg_det` PASS.
- **Store redaction gate**: Example input produces packet with `harness.redaction_applied=True` when redaction is enabled; store write path satisfies INV-STORE-SEC-1.

---

## 5. Model users (default experience)

Model users (mdm-engine + harness) get platform capabilities by default or single entry point:

- **Entry:** `python -m harness --port 8000` (with `[gateway]` installed) or `harness.serve()`.
- **Catalog/control:** Gateway merges get_context_overrides(tenant) and get_ops_state() into context.
- **Store:** Optional; enable via create_app(store_backend=...) or env DECISION_STORE_PATH for file.
- **Adapters:** Use `adapter=example_domain_lending`, `example_domain_scheduling`, `example_domain_trading`, `example_domain_content_moderation`, `example_domain_ops_automation`, `example_domain_triage`, or `example_domain_agent_tool_use` in POST /decide body for domain input/output mapping.
- **Control:** By default GET/POST /control return 403. Set `DECISION_GATEWAY_ENABLE_CONTROL=1` and `DECISION_CONTROL_TOKEN` (header `X-Decision-Control-Token` or `Authorization: Bearer <token>`) to enable.

---

## 6. Quick reference

| Item | Value |
|------|--------|
| Platform namespace | `harness.platform` |
| Pipeline SSOT | `harness.run_one_step` (unchanged) |
| Server extra | `pip install decision-ecosystem-integration-harness[gateway]` or `[server]` |
| CLI | `python -m harness --host 0.0.0.0 --port 8000 --store memory\|file\|off --store-path path` |

---

**Last updated:** 2026-02-19  
**References:** DECISION_CENTER_GAPS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, REPO_REGISTRY.md
