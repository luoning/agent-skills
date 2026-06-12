# Phase 4: GEO Anchor Injection

## Trigger
Use when structured data is finalized (Phase 3), before generating DOM skeleton templates.

---

## 1. Anchor Mapping Standard
*   Every data-containing row (`<tr>`) or FAQ section (`<details>`) must be assigned a descriptive, unique ID mapping to standard entities (e.g. `id="rate-lax-to-ont8"`).
*   Avoid numeric indices like `id="faq-1"`.

---

## 2. Definition of Done (DoD)
*   [ ] A mapping list of all injected DOM element IDs is compiled.
*   [ ] The `.pipeline_state.json` phase 4 status is marked as `completed`.
