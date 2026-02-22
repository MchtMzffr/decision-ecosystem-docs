# Public Main Audit — Verification and Test Vectors

**Goal:** Clarify that `public_main_audit.py` reads **only raw public** content (`raw.githubusercontent.com/<owner>/<repo>/main/...`), does not use the local workspace, and that "OK" means the current public main complies with the rules.

---

## 1) What does the script do?

- **Source:** HTTP GET only to `https://raw.githubusercontent.com/{owner}/{repo}/main/{path}`. It does not read local files and does not take `--workspace`.
- **Fail-closed network (INV-PUBLIC-MAIN-2):** Any URL fetch failure (HTTP != 200, timeout, exception) ⇒ exit != 0. Cache-bust: `?t=<unix>` and headers `Cache-Control: no-cache`, `Pragma: no-cache`.
- **Fail:** 404, README placeholder, ops-health param drift, schema != 0.2.2, CI using `decision-schema.git@main`, audit script missing in docs, MeetlyTR → exit 1.
- **OK:** Exit 0 when all checks pass. Optional: `--proof-json <path>` for machine-readable proof (url, status, ok per check).
- **INV-AUDIT-NEG-1:** Negative test: when run with `--owner DefinitelyNotAnOwner`, exit != 0 (tools/tests/test_public_main_audit_negative.py).

---

## 2) Test vectors (manual verification)

Open the URLs below in a browser or with `curl`. If the audit reports "OK", these contents **currently** should be as described (or better).

| Check | URL | Expected (strict) |
|-------|-----|-------------------|
| INV-LIC-1 (ops-health) | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/LICENSE` | HTTP 200, body "MIT License" |
| INV-LIC-1 (eval-cal) | `https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/main/LICENSE` | HTTP 200, body "MIT License" |
| INV-LIC-1 (exec-orch) | `https://raw.githubusercontent.com/MchtMzffr/execution-orchestration-core/main/LICENSE` | HTTP 200 |
| README placeholder (ops) | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/README.md` | No "Add your license"; "max_429_per_window" **present** |
| README placeholder (mdm) | `https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/README.md` | No "Add your license"; ">=0.2.2" **present** |
| README placeholder (harness) | `https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/main/README.md` | No "Add your license"; ">=0.2.2" **present** |
| Ops FORMULAS drift | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/docs/FORMULAS.md` | "max_429_per_window" **present**; "max_rate_limit_events" **absent** |
| INV-SSOT-REALITY-1 (schema version) | `https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/pyproject.toml` | `version = "0.2.2"` |
| INV-CI-NONDET-0 (mdm CI) | `https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/.github/workflows/ci.yml` | "decision-schema" + "@v0.2.2" **present**; "@main" **absent** (for schema fallback) |
| Docs audit script present | `https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-docs/main/tools/public_main_audit.py` | HTTP 200 |

---

## 3) "Audit says OK but I still see old content" — what does it mean?

1. **Timing:** If the review was done **before** pushes, public main was actually broken at that time; **after** pushes, the script and raw URLs reflect the current state. Audit OK = raw-public is **currently** compliant.
2. **Cache:** Browser or CDN may serve stale content. Check with `curl -s "https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/pyproject.toml" | findstr version` (Windows) or incognito.
3. **Branch/owner:** The script uses `--owner MchtMzffr` and `/main/`. A different owner or branch will yield different results.

---

## 4) Conclusion

- **Agreed:** "DONE = evidence on public main" and the audit’s **raw-public-only** verification is the right approach.
- **Verification (this session):** The same raw URLs are currently (as of fetch date) compliant: decision-schema 0.2.2, mdm CI @v0.2.2, LICENSEs 200, no README placeholder, ops FORMULAS max_429_per_window. So the script’s "OK" is **consistent**.
- **If you still see 404/placeholder at those URLs:** Confirm that pushes reached main and that cache is bypassed; run the script again. If needed, fill the test-vector table row by row to identify which URL fails.

**Last updated:** 2026-02-19
