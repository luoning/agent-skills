---
name: "skill-governance"
description: "Use when starting any collaborative task, planning solution architectures, writing skills, or executing scenarios to route active sub-skills and enforce checkgates."
---

# Skill Governance & Router Specification

## Overview
This skill acts as the central router and pipeline orchestrator for AI Agent lifecycle management. It organizes separate developmental phases into a unified process stream, dynamically loading sub-skills on-demand and enforcing specific verification gatekeepers to maintain codebase integrity.

---

## 1. Trigger
This orchestrator must be loaded:
*   At the initiation of any task (brainstorming, decision-making, planning).
*   When a new capability or codebase modification is created and requires verification.
*   Prior to merging staged files or generating Cursor rules config.

---

## 2. Core Guidelines & Router Mapping

### The Developer Process Stream (流程化整合)
All development tasks must cycle through the following stages, dynamically calling the designated sub-skills:

```text
  [Stage 1: Ideation]  ──>  [Stage 2: Extraction]  ──>  [Stage 3: Auditing]  ──>  [Stage 4: Scenario Test]
   workflow-contract          url-extractor            static-auditor           scenario-tester
```

### Dynamic Skill Router Table (按需路由)

| Development Phase | Target Sub-skill | Enforced Gatekeeper Check |
| :--- | :--- | :--- |
| **Phase 1: Ideation & Setup** | `sub-skills/workflow-contract.md` | Evolving ideas stay inside temporary/scratch isolation. |
| **Phase 2: Knowledge Extraction** | `sub-skills/url-extractor.md` | Deduce user sharing intent and map parameters via POE. |
| **Phase 3: Static Integrity Audit** | `sub-skills/static-auditor.md` | Run `skill_integrity_auditor.py` to block absolute paths. |
| **Phase 4: Functional Verification**| `sub-skills/scenario-tester.md` | Run `pytest` executing target subclasses of `BaseScenarioTest`. |

---

## 3. Definition of Done (DoD)
- [ ] Sandbox isolation is confirmed (no unstaged active workspace changes without authorization).
- [ ] Banned marketing buzzwords are audited and removed.
- [ ] No local absolute disk paths exist in any code snippet or documentation link.
- [ ] Target scenario tests successfully complete all four stages of `BaseScenarioTest`.

---

## 4. Verification & Testing Commands
Run the complete testing and integrity suite managed by this router:
```bash
# Compile MDC rules
python scripts/generate_mdc.py
# Perform global skill files schema integrity audit
python scripts/skill_integrity_auditor.py .
# Run all scenario tests
pytest
```
*   **DoD**: All three CLI gates return exit code 0.

---

## 5. Silent Dynamic Context Routing (中枢自动静默路由协议)
To ensure a native Vibecoding experience, the user must never be asked to manually run context swapper commands. The agent must silently intercept the user's intent and execute the swapper in the background:

- **When the user shares a URL or asks to extract data**:
  - *Action*: Proactively run `python scripts/context_swapper.py url-extractor` as a background task.
- **When the user initiates a planning or planning-approval task**:
  - *Action*: Proactively run `python scripts/context_swapper.py workflow-contract` as a background task.
- **When the user requests tests or verification runs**:
  - *Action*: Proactively run `python scripts/context_swapper.py scenario-tester` as a background task.
- **When the user requests visual adjustments or styling planning**:
  - *Action*: Proactively run `python scripts/context_swapper.py web-design` as a background task.
- **When the user requests structural component coding**:
  - *Action*: Proactively run `python scripts/context_swapper.py web-autobuild` as a background task.

The agent must immediately act upon the newly swapped context without waiting for the user to confirm the command execution.

