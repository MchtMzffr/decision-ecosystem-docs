# Tag Alignment Complete — Final Verification

**Date:** 2026-02-17  
**Status:** Historical incident report (not current policy)

**Note:** This document describes a one-time correction (2026-02-17) where tags were moved to match `main` HEAD. Current policy is **TAG_GOVERNANCE.md**: tags are immutable; we do not move tags. For release verification we use **INV-REL-4**: tag commit must be an *ancestor* of `main` (see RELEASE_VERIFICATION_CHECKLIST.md).

---

## Issue Identified (historical)

Tag commit'leri `main` branch'in son commit'leriyle uyumsuzdu:
- Tag'ler oluşturulduktan sonra `main`'e yeni commit'ler push edilmiş
- Bu durum "source-of-truth = main" prensibini bozuyordu

---

## Resolution

Tag'ler `main` branch'in son commit'lerine taşındı:

### mdm-engine
- **Old tag commit:** `bf089ee` (version bump)
- **New tag commit:** `ea9973a` (includes test_rate_limit.py)
- **Status:** ✅ Aligned

### ops-health-core
- **Old tag commit:** `7b366b3` (version bump)
- **New tag commit:** `c0cb359` (includes CI fallback fix)
- **Status:** ✅ Aligned

### evaluation-calibration-core
- **Old tag commit:** `0c5b881` (version bump)
- **New tag commit:** `e628733` (includes F8 invariant extension)
- **Status:** ✅ Aligned

### decision-schema
- **Tag commit:** `ef8c1c2` (already aligned with `main`)
- **Status:** ✅ Already aligned

---

## Verification

**INV-REL-1 (Version Single-Source):** ✅
- `main` branch version == tag version
- All repositories verified

**INV-REL-3 (Fallback Determinism):** ✅
- All CI fallbacks use tagged versions (`@v0.2.1`, `@v0.1.1`)
- Integration harness CI pinned to tags
- ops-health-core CI pinned to tags

---

## Final Status

✅ **All tags aligned with `main` branch**  
✅ **All CI fallbacks use tagged versions**  
✅ **Source-of-truth = main principle maintained**

**Ecosystem Status:** ✅ **Production-Ready**

---

**Last Updated:** 2026-02-17
