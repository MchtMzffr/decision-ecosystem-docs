<!--
Decision Ecosystem — decision-ecosystem-docs
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Subagents vs Project Alignment Report

**Purpose:** Compare the four User subagents (Formal Methods Reviewer, Security & Ops Safety Auditor, Release & Governance Steward, Docs Editor ADS-1) with the Decision Ecosystem project. Gaps, errors, and incompatibilities are listed with remediation.

**Scope:** decision-ecosystem-docs; subagents in `~/.cursor/agents/`. SSOT for invariants: ECOSYSTEM_GATES_AND_INVARIANTS.md; for release: RELEASE_NOTES_STANDARD_AND_TEMPLATES.md, RELEASE_VERIFICATION_CHECKLIST.md.

---

## 1. Summary

| Subagent | Uyumluluk | Eksik / Hatalı / Uyumsuz |
|----------|------------|---------------------------|
| Formal Methods Reviewer | Genel uyumlu | Invariant ID formatı (INV-*) ve trace registry path referansı eksik |
| Security & Ops Safety Auditor | Uyumlu | Proje spesifik invariant (INV-SEC-RED-1, INV-ERR-SURFACE-1) opsiyonel referans |
| Release & Governance Steward | Uyumlu | INV-REL-4, ECOSYSTEM_CONTRACT_MATRIX, RELEASE_VERIFICATION_CHECKLIST referansı eklendi |
| Docs Editor (ADS-1) | Uyumlu | Doc naming (SCREAMING_SNAKE_CASE), root allowlist, INV-DOC-* referansı eklendi |

---

## 2. Formal Methods Reviewer

### Proje ile uyumlu olanlar
- decision-schema SSOT, cores only depend on decision-schema (INV-CORE-DEP-1).
- Trace keys registered in decision-schema (INV-TRACE-REG-1).
- Fail-closed, kill-switch, boundedness (max_*) — VALIDATION.md, ECOSYSTEM_GATES_AND_INVARIANTS.md, execution-orchestration invarians (INV-EXE-2, INV-EXE-4).
- Deterministic tests; exception paths (e.g. test_invariant_h4_fail_closed_propagation.py, test_invariant_exe_fail_closed.py).

### Eksik / düzeltme
- **Invariant ID formatı:** Projede tüm invariant’lar `INV-<Kategori>-<No>` (örn. INV-TRACE-REG-1, INV-EXE-2, INV-CORE-DEP-1). Subagent’ta “id (e.g. INV-BOUND-QUEUE-1)” gibi proje convention’ı belirtilmeli; yeni invariant önerirken ECOSYSTEM_GATES_AND_INVARIANTS.md ve INVARIANT_TRACEABILITY.md ile uyumlu isimlendirme.
- **Trace registry konumu:** Projede SSOT: `decision-schema` repoda `decision_schema/trace_registry.py` (EXTERNAL_KEY_REGISTRY); doküman: `decision-schema/docs/TRACE_KEY_REGISTRY.md`, `PARAMETER_INDEX.md` (INV-PARAM-INDEX-1, INV-TRACE-REG-1). Subagent “decision-schema trace registry” diyor; path açık değil. Subagent’a “Register in decision_schema/trace_registry.py and document in TRACE_KEY_REGISTRY.md” notu eklendi.

---

## 3. Security & Ops Safety Auditor

### Proje ile uyumlu olanlar
- INV-SEC-RED-1 (gitleaks), INV-ERR-SURFACE-1 (redacted error surfaces), fail-closed, kill-switch (INV-CTRL-DOM-1, harness/exec tests), boundedness (max_429_per_window, max_rate_limit_events_per_window — ops-health FORMULAS).
- SECURITY_SCOPE.md; risk alanları proje ile uyumlu.

### Eksik / düzeltme
- **Opsiyonel:** Risk register’da “detection” için proje invariant’ları referans verilebilir (INV-SEC-RED-1, INV-ERR-SURFACE-1). Subagent genel bırakıldı; proje kullanırken bu ID’ler hatırlatılabilir.

---

## 4. Release & Governance Steward

### Proje ile uyumlu olanlar
- INV-CI-NONDET-0 (no @main fallback), INV-CI-SCHEMA-FB-1, INV-CI-PIN-1; tag immutability (TAG_GOVERNANCE.md); INV-REL-TAG-1, INV-REL-SSOT-1, INV-REL-SEC-1, INV-REL-PROOF-1, INV-REL-NO-TBD-1.
- **INV-REL-GH** projede tanımlı: RELEASE_VERIFICATION_CHECKLIST.md § “GitHub Release Artefacts (INV-REL-GH)” — INV-REL-GH-1..4.
- INV-REL-4: tag commit must be ancestor of main (`git merge-base --is-ancestor`).
- ECOSYSTEM_CONTRACT_MATRIX.md (repo root): dependency ranges, CI fallback tags.
- Single-source version: test_invariant_version_single_source.py; INV-REL-1 (version single-source) arşiv dokümanlarında.

### Eksik / düzeltme
- Subagent’ta “INV-REL-GH” vardı; proje ile uyumlu. **Eklendi:** INV-REL-4 (tag reachability), RELEASE_VERIFICATION_CHECKLIST.md, ECOSYSTEM_CONTRACT_MATRIX, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md referansı — checklist’in nerede olduğu netleştirildi.

---

## 5. Docs Editor (ADS-1)

### Proje ile uyumlu olanlar
- ACTIVE = ecosystem-level docs (projede literal “ACTIVE” klasörü yok; docs/ altındaki güncel politikalar).
- archive/YYYY-MM-DD (INV-DOC-2); README index only; INV-DOC-LANG-2 (English); domain lexemes only in examples.
- .cursor/skills/docs_triage_ads1 ile kavramsal örtüşme.

### Eksik / düzeltme
- **Doc naming:** DOCUMENTATION_STANDARDS.md: dosya adları SCREAMING_SNAKE_CASE, ASCII-only, .md. Subagent’ta “ACTIVE” dışında doc naming kuralı yoktu. **Eklendi:** Doc filenames SCREAMING_SNAKE_CASE; INV-DOC-ROOT-ALLOWLIST-1 (root allowlist), check_docs_root.py, DOCS_REPO_STRUCTURE.
- **Root allowlist:** Projede root’ta sadece allowlist dosyaları; README sadece bunlara link (RELEASE_VERIFICATION_CHECKLIST.md, ECOSYSTEM_CONTRACT_MATRIX.md, TAG_GOVERNANCE.md, vb.). Subagent “README indexes CURRENT only” diyor; “root allowlist” ve “check_docs_root.py” ile uyum için not eklendi.

---

## 6. Skills vs Subagents Çakışması

Projede .cursor/skills altında benzer işlere odaklanan skill’ler var:

| Skill | Subagent | İlişki |
|-------|----------|--------|
| contract_gatekeeper | Formal Methods Reviewer, Release Steward | Skill schema/trace/contract; subagent invariant+test+release. Birlikte kullanılabilir; skill diff/implementation, subagent spec/checklist. |
| invariant_test_builder | Formal Methods Reviewer | Skill test/invariant; subagent daha geniş (invariant table + failure modes). Örtüşme kabul edilebilir. |
| security_redaction_audit | Security & Ops Safety Auditor | Skill audit odaklı; subagent risk register + patch plan. Tamamlayıcı. |
| release_engineer | Release & Governance Steward | Skill release süreci; subagent governance + checklist. Tamamlayıcı. |
| docs_triage_ads1 | Docs Editor (ADS-1) | Aynı hedef (ADS-1, archive, README). Subagent daha detaylı deliverable; skill kısa triage. Çakışma yok. |
| execution_orchestration_spec | Formal Methods Reviewer | Skill orchestration spec; subagent genel invariant/tests. Örtüşme yok. |

**Sonuç:** Çakışma yok; skill’ler tek adım/odak, subagent’lar tam iş akışı ve deliverable üretiyor.

---

## 7. Yapılan Subagent Güncellemeleri

Aşağıdaki güncellemeler `~/.cursor/agents/` dosyalarına uygulandı:

1. **formal-methods-reviewer.md:** Invariant ID’lerin INV-* convention’ı (ECOSYSTEM_GATES_AND_INVARIANTS.md); trace key’ler için `decision_schema/trace_registry.py` ve TRACE_KEY_REGISTRY.md referansı.
2. **release-governance-steward.md:** INV-REL-4, RELEASE_VERIFICATION_CHECKLIST.md, ECOSYSTEM_CONTRACT_MATRIX, RELEASE_NOTES_STANDARD_AND_TEMPLATES.md referansı.
3. **docs-editor-ads1.md:** Doc naming (SCREAMING_SNAKE_CASE), root allowlist (INV-DOC-ROOT-ALLOWLIST-1), check_docs_root.py, INV-DOC-*.

---

## 8. Doğrulama

- Subagent’lar proje SSOT’una (decision-schema, ECOSYSTEM_GATES_AND_INVARIANTS, RELEASE_NOTES_STANDARD, RELEASE_VERIFICATION_CHECKLIST, DOCUMENTATION_STANDARDS) referans veriyor.
- Domain-agnostic, fail-closed, kill-switch, boundedness, trace registry kuralları proje ile uyumlu.
- Invariant ID’ler (INV-REL-GH, INV-REL-4, INV-DOC-*, INV-TRACE-REG-1, vb.) projede mevcut; subagent metinleri güncellendi.

**Last updated:** 2026-02  
**References:** ECOSYSTEM_GATES_AND_INVARIANTS.md, INVARIANT_TRACEABILITY.md, RELEASE_VERIFICATION_CHECKLIST.md, DOCUMENTATION_STANDARDS.md, .cursor/agents/*.md
