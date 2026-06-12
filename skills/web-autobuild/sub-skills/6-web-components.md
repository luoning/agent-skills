# Phase 6: Component Hydration

## Trigger
Use when semantic HTML is built (Phase 5), to mount reusable page elements.

---

## 1. Modular Assembly Protocol
*   Common page fragments (headers, footers, widget inputs) must be loaded dynamically as custom Custom Elements.
*   **Zero inline styling**: Do not inject CSS styling attributes directly inside JavaScript string templates.

---

## 2. Definition of Done (DoD)
*   [ ] Reusable JS modules (`navbar.js`, `footer.js`) are integrated and run without errors.
*   [ ] The `.pipeline_state.json` phase 6 status is marked as `completed`.
