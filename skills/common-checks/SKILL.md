---
name: skills-auditor
description: Use when creating a new agent skill, editing existing skills, or running a pull request (PR) audit on a repository of skills.
---

# Skills Lifecycle & Integrity Auditor (Meta-Skill)

## Overview
This meta-skill governs the creation, review, and verification of AI Agent Skills. It ensures that skills are not vague, contain no broken markdown links, and resist agent evasion under pressure.

---

## 1. Trigger
Run this audit:
*   Immediately after creating a new `SKILL.md` or a sub-skill markdown file.
*   Prior to submitting a Pull Request (PR) containing skills modification.

---

## 2. Core Compliance Standards
Every skill file must pass the following checkgates:

### YAML Frontmatter Compliance
*   `name`: Must use lowercase letters, numbers, and hyphens only (e.g. `web-autobuild`).
*   `description`: Must start with **"Use when..."** and specify only trigger symptoms, **NOT** process workflow summaries.

### Markdown Links Completeness
*   All relative and absolute links (e.g., `file:///`) pointing to白皮书 documents or scripts must be valid and exist in the filesystem.

### Evasion Prevention
*   Every skill must have a **DoD (Definition of Done)** section outlining concrete checkable items.

---

## 3. Modular Sub-skills
*   **[Skill Generator & Registrar](sub-skills/skill-generator.md)**: Guidelines for learning boilerplate, creating new skills dynamically, and auto-registering them.

---

## 4. DoD Verification Script
To verify the integrity of the repository, execute:
```bash
python scripts/skill_integrity_auditor.py .
```
*   **DoD**: The console prints `All Skills in Repository are fully compliant (AUDIT PASSED)!.`.
