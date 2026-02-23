<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Decision Ecosystem — Görselleştirme (Architecture & Data Flow)

**Amaç:** Yapının ve veri akışının tek sayfada görsel karşılığı. Diyagramlar Mermaid ile; GitHub, GitLab ve Mermaid-destekleyen her yerde render edilir.

**Referanslar:** PLATFORM_PLACEMENT_AND_DEFAULTS.md, DECISION_CENTER_GAPS.md, ECOSYSTEM_GATES_AND_INVARIANTS.md.

---

## 1. Ekosistem genel görünüm

Tüm core’lar yalnızca **decision-schema**’ya bağımlı; core’lar birbirine bağımlı değil. Harness pipeline’ı orkestre eder ve platform katmanını sunar.

```mermaid
flowchart TB
    subgraph SSOT["SSOT: decision-schema"]
        schema[Types, PacketV2, PARAMETER_INDEX]
    end

    subgraph cores["Cores (schema-only, no core↔core)"]
        mdm[mdm-engine\nProposal]
        ops[ops-health-core\nKill-switch]
        dmc[decision-modulation-core\nGuards, modulate]
        eval[evaluation-calibration-core\nReport, metrics]
        exe[execution-orchestration-core\nRun actions]
        expl[explainability-audit-core\nReason codes]
    end

    subgraph harness["integration-harness (orchestration + platform)"]
        run[run_one_step\nPipeline SSOT]
        gw[gateway]
        store[store]
        catalog[catalog]
        ctrl[control]
        adapt[adapters]
    end

    schema --> mdm & ops & dmc & eval & exe & expl
    mdm & ops & dmc & eval --> run
    run --> gw & store
    catalog & ctrl --> gw
    adapt --> gw
```

---

## 2. Pipeline veri akışı (tek adım)

`run_one_step(state, context)` içinde sıra: propose → ops → modulate → PacketV2 → report. Fail-closed: exception durumunda güvenli karar + packet.

```mermaid
flowchart LR
    subgraph input["Girdi"]
        S[state]
        C[context]
    end

    subgraph pipeline["Pipeline (harness.run_one_step)"]
        P[1. Propose\nmdm-engine]
        O[2. Ops signal\nops-health-core]
        M[3. Modulate\nDMC]
        PK[4. PacketV2\nbuild]
        R[5. Report\neval-calibration]
    end

    subgraph output["Çıktı"]
        FD[FinalDecision]
        Pkt[PacketV2]
        Rep[Report]
    end

    S --> P
    C --> P
    P --> O
    O --> M
    C --> M
    M --> PK
    PK --> R
    PK --> FD & Pkt & Rep
```

---

## 3. Decision Center (platform katmanı)

Gateway isteği alır; adapter ile domain → (state, context) dönüşümü yapılabilir; catalog/control context’e eklenir; pipeline çalışır; store ile kayıt; yanıt döner.

```mermaid
flowchart TB
    subgraph client["Çağıran"]
        req[POST /decide veya /decision]
    end

    subgraph gateway["Gateway"]
        mw[Middleware\nsize, rate-limit]
        adj[Adapter?\ndomain → state, context]
        merge[Catalog + Control\ncontext merge]
        call[run_one_step]
        save[Store.save\noptional]
        resp[Response\npacket, final_decision]
    end

    subgraph platform["Platform bileşenleri"]
        cat[catalog]
        ctrl[control]
        st[store]
    end

    req --> mw --> adj --> merge --> call
    cat --> merge
    ctrl --> merge
    call --> save --> resp
    st --> save
```

---

## 4. Adapter katmanı (domain ↔ pipeline)

Adapter’lar yalnızca eşleme yapar: domain girdisi → (state, context); FinalDecision/Report → domain çıktısı. Tüm örnek adapter’lar `example_domain_*` prefix’i taşır (INV-ADAPTER-DOMAIN-LEAK-1).

```mermaid
flowchart LR
    subgraph domain["Domain tarafı"]
        DI[domain_input]
        DO[domain_output]
    end

    subgraph adapter["Adapter (BaseAdapter)"]
        to_sc[to_state_context]
        to_out[to_domain_output]
    end

    subgraph pipeline["Pipeline"]
        state[state]
        context[context]
        FD[FinalDecision]
        Report[Report]
    end

    DI --> to_sc --> state & context
    state & context --> pipeline
    FD & Report --> to_out --> DO
```

---

## 5. Nasıl görüntülenir?

- **GitHub/GitLab:** Bu dosyayı açın; Mermaid blokları otomatik render edilir.
- **VS Code:** Markdown Preview Enhanced veya “Markdown: Open Preview” ile önizleme.
- **Çevrimiçi:** [Mermaid Live Editor](https://mermaid.live) — kodu yapıştırıp PNG/SVG dışa aktarabilirsiniz.
- **CLI:** `@mermaid-js/mermaid-cli` ile `mmdc -i ARCHITECTURE_VISUALIZATION.md -o out/` (blokları ayrı görsellere çıkarır).

---

**Son güncelleme:** 2026-02  
**Referanslar:** PLATFORM_PLACEMENT_AND_DEFAULTS.md, DECISION_CENTER_GAPS.md, REPO_REGISTRY.md
