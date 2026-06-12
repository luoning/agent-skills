---
name: "opinion-driven-construction"
description: "Use when collaborating with Luoning to enforce extreme constraint-driven engineering and prevent agent alignment deception (sycophancy)."
---

# Opinion-Driven Construction & Anti-Sycophancy Rule

## Overview
This skill governs the behavior, communication, and layout constraints of coding agents collaborating within Luoning's digital ecosystem. It prevents agents from writing redundant documentation, over-explaining concepts, or inserting self-definitions.

---

## 1. Trigger
This skill must be loaded immediately when:
*   The agent is analyzing high-level architecture designs, future timetables, or systemic opinions.
*   The agent is editing public-facing documentation (such as profile `README.md` files).
*   The agent begins writing conversational responses.

---

## 2. Core Guidelines & Engineering Rules

### Factual-Only Documentation (Fact over Spec)
*   **Rule**: Never explain abstract methodologies, cognitive models, or personal parameters (e.g. MBTI, roles) in public repositories.
*   **Action**: Restrict repository documents (like READMEs) to strictly runnable code, installation guides, concrete project objectives (Why, Solution), and tags. Keep it neutral and objective.

### Sub-surface Architecture (Logs in the Dark)
*   **Rule**: High-level system architectures and cognitive models must be kept local (e.g. inside the local workspace or appDataDir).
*   **Action**: Do not expose design templates to remote repositories unless explicitly asked.

### Finger-Extension Protocol (Agile Execution)
*   **Rule**: Respond to short, rapid user commands with minimal conversational overhead.
*   **Action**: Drop polite fluff, greetings, and long post-execution summaries. Complete the file edit or terminal run, stage/commit to Git, and report only the physical output.

---

## 3. Definition of Done (DoD)
Before finalizing any step, the agent must check:
- [ ] No abstract labels (e.g. "INTJ-T", "Product Director") exist in public readme files.
- [ ] All public-facing project descriptions are written in neutral, system-spec English.
- [ ] High-level methodology maps are saved in local design docs, not in remote READMEs.
- [ ] Conversational responses are concise, plain-spoken, and free of commercial buzzwords.
