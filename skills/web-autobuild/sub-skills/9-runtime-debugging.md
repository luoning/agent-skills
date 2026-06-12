# Phase 9: Runtime Debugging & Self-Healing Protocol

## Trigger
Use when a page, script, or component fails runtime execution (e.g., console errors, failed unit tests, or broken script loading in the sandbox).

---

## 1. The Self-Healing Loop

When a runtime error is encountered (e.g., during Jest/Vitest/Playwright tests or Python script execution), you **MUST NOT** ask the user for help immediately. Execute the three-stage self-healing cycle:

```text
Detect Error (Capture Stacktrace/Log)
  ├── [Stage 1] Isolate root cause (Identify broken file, line, and syntax/runtime failure)
  ├── [Stage 2] Apply surgical fix (Edit the exact lines, preserving surrounding code)
  └── [Stage 3] Validate again (Rerun the failing validator/test suite)
```

Repeat this loop up to **3 times**. If the suite still fails after 3 attempts, halt execution, generate a diagnostic report, and request human intervention.

---

## 2. Common Runtime Error Matrix & Recovery Actions

| Error / Log Pattern | Typical Root Cause | Surgical Recovery Action |
| :--- | :--- | :--- |
| `TypeError: Cannot read properties of null (reading 'addEventListener')` | Web Component hydrated before DOM element loaded. | Wrap initialization inside `DOMContentLoaded` event listener or use standard custom element `connectedCallback()`. |
| `ReferenceError: customElements is not defined` | Script executed in non-browser environment (Node / JSDOM) without mock. | Add guard: `if (typeof window !== 'undefined' && 'customElements' in window)`. |
| `CSSStyleSheet.replaceSync is not defined` | Shadow DOM styling loaded on outdated browser mock. | Fallback to standard `<style>` tag insertion inside Shadow Root. |

---

## 3. Telemetry Tracking (.agent_trajectory.json)

To maintain high observability, write all runtime correction steps to `.agent_trajectory.json` in the target workspace root:

```json
{
  "timestamp": "2026-06-12T10:55:00Z",
  "errors_encountered": [
    {
      "phase": "Phase 6: Web Components",
      "error_message": "customElements is not defined",
      "attempts_to_fix": 1,
      "outcome": "resolved"
    }
  ]
}
```

---

## 4. Definition of Done (DoD)
- [ ] No uncaught console exceptions are generated during execution.
- [ ] The self-healing loop has been run (up to 3 iterations) and succeeded, or halted with a diagnostic log.
- [ ] `.agent_trajectory.json` logs the diagnostic path.
