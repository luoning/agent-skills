---
name: "architecture-piercing"
description: "Use when the agent generates complex code modifications or new structural blocks to force architectural disclosure and prevent blind human merging."
---

# Architecture-Piercing & Structural Auditing Skill

## Overview
This skill forces the coding agent to disclose the underlying design decisions, trade-offs, and failure boundaries of its generated code. It aims to bridge the "expert knowledge gap" by forcing the human developer to act as a critical system auditor.

---

## 1. Trigger
This skill must be triggered when:
*   Generating a new module, file, or class exceeding 50 lines of code.
*   Conducting major database schema designs or API contract refactorings.
*   Encountering complex algorithms (e.g. custom tree traversals, state machines).

---

## 2. Core Guidelines & Engineering Rules

### Design Trade-offs Disclosure (舍弃与抉择)
*   **Rule**: The agent must accompany code blocks with a brief "Design Decisions & Trade-offs" summary.
*   **Action**: List what alternative design was considered and *why* it was discarded (e.g., "Chose SQLite over PostgreSQL because of zero-dependency deployment requirements, sacrificing concurrent write performance").

### Explicit Boundary Declaration (边界与限额)
*   **Rule**: The agent must explicitly declare where the generated system will break or slow down.
*   **Action**: Detail the input scale limits (e.g., "Fails when JSON payloads exceed 50MB due to in-memory buffering").

### Red-Teaming Self-Critique (自曝漏洞)
*   **Rule**: The agent must self-report the most fragile part of its implementation.
*   **Action**: State the exact functions or logic gates that are most vulnerable to runtime exceptions or state drift.

---

## 3. Definition of Done (DoD)
Before completing any major code generation:
- [ ] Code blocks are followed by a "Design Decisions & Trade-offs" summary.
- [ ] Explicit boundary limits (CPU, memory, scale) are documented.
- [ ] The "Red-Teaming Self-Critique" lists at least one potential logical weakness.
- [ ] All conversational text explaining this audit remains concise and neutral.
