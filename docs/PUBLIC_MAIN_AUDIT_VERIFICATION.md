# Public Main Audit — Doğrulama ve Test Vektörleri

**Amaç:** `public_main_audit.py`'nin **sadece raw-public** (`raw.githubusercontent.com/<owner>/<repo>/main/...`) okuyup lokal workspace kullanmadığını ve "OK" = o anki public main'in kurallara uyduğunu netleştirmek.

---

## 1) Script ne yapıyor?

- **Kaynak:** Sadece HTTP GET ile `https://raw.githubusercontent.com/{owner}/{repo}/main/{path}`. Lokal dosya okumaz, `--workspace` almaz.
- **Fail-closed network (INV-PUBLIC-MAIN-2):** Herhangi bir URL fetch hatası (HTTP != 200, timeout, exception) ⇒ exit != 0. Cache-bust: `?t=<unix>` ve header `Cache-Control: no-cache`, `Pragma: no-cache`.
- **Fail:** 404, README placeholder, ops-health param drift, schema != 0.2.2, CI'da `decision-schema.git@main`, docs'ta audit script yok, MeetlyTR → exit 1.
- **OK:** Tüm kontroller geçerse exit 0. Opsiyonel: `--proof-json <path>` ile makine-okunur kanıt (url, status, ok per check).
- **INV-AUDIT-NEG-1:** Negatif test: `--owner DefinitelyNotAnOwner` ile çalıştırıldığında exit != 0 (tools/tests/test_public_main_audit_negative.py).

---

## 2) Test vektörleri (manuel doğrulama)

Aşağıdaki URL'leri tarayıcı veya `curl` ile aç. Audit "OK" diyorsa bu içerikler **şu an** böyle olmalı (veya daha iyi).

| Kontrol | URL | Beklenen (strict) |
|--------|-----|-------------------|
| INV-LIC-1 (ops-health) | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/LICENSE` | HTTP 200, body "MIT License" |
| INV-LIC-1 (eval-cal) | `https://raw.githubusercontent.com/MchtMzffr/evaluation-calibration-core/main/LICENSE` | HTTP 200, body "MIT License" |
| INV-LIC-1 (exec-orch) | `https://raw.githubusercontent.com/MchtMzffr/execution-orchestration-core/main/LICENSE` | HTTP 200 |
| README placeholder (ops) | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/README.md` | "Add your license" **yok**, "max_429_per_window" **var** |
| README placeholder (mdm) | `https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/README.md` | "Add your license" **yok**, ">=0.2.2" **var** |
| README placeholder (harness) | `https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-integration-harness/main/README.md` | "Add your license" **yok**, ">=0.2.2" **var** |
| Ops FORMULAS drift | `https://raw.githubusercontent.com/MchtMzffr/ops-health-core/main/docs/FORMULAS.md` | "max_429_per_window" **var**, "max_rate_limit_events" **yok** |
| INV-SSOT-REALITY-1 (schema version) | `https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/pyproject.toml` | `version = "0.2.2"` |
| INV-CI-NONDET-0 (mdm CI) | `https://raw.githubusercontent.com/MchtMzffr/mdm-engine/main/.github/workflows/ci.yml` | "decision-schema" + "@v0.2.2" **var**, "@main" **yok** (schema fallback için) |
| Docs audit script present | `https://raw.githubusercontent.com/MchtMzffr/decision-ecosystem-docs/main/tools/public_main_audit.py` | HTTP 200 |

---

## 3) "Audit OK ama ben hâlâ eski görüyorum" ne demek?

1. **Zaman farkı:** İnceleme push’lardan **önce** yapıldıysa, public main o anda gerçekten bozuktu; push’lardan **sonra** script ve raw URL’ler güncel state’i gösterir. Audit OK = **şu an** raw-public uyumlu.
2. **Cache:** Tarayıcı veya CDN eski içerik verebilir. Kontrol: `curl -s "https://raw.githubusercontent.com/MchtMzffr/decision-schema/main/pyproject.toml" | findstr version` (Windows) veya incognito.
3. **Branch/owner:** Script `--owner MchtMzffr` ve `/main/` kullanıyor. Farklı owner veya branch kullanıyorsan sonuç farklı olur.

---

## 4) Sonuç

- **Katılıyorum:** "DONE = public main’de kanıt" ve audit’in **sadece raw-public** doğrulaması doğru yaklaşım.
- **Doğrulama (bu oturumda):** Aynı raw URL’ler şu an (fetch tarihi itibarıyla) uyumlu: decision-schema 0.2.2, mdm CI @v0.2.2, LICENSE’lar 200, README’lerde placeholder yok, ops FORMULAS max_429_per_window. Bu yüzden script’in "OK" demesi **tutarlı**.
- **Eğer sen aynı URL’lerde hâlâ 404/placeholder görüyorsan:** Push’ların main’e gittiğini ve cache’i bypass ettiğini kontrol et; script’i tekrar çalıştır. Gerekirse test vektörleri tablosunu tek tek doldurup hangi URL’nin fail ettiğini tespit edebilirsin.

**Last updated:** 2026-02-19
