---
name: web-autobuild
description: Use when building, expanding, or modifying web pages and interfaces. This coordinates Phase 1 to Phase 7 and manages the physical state lock (.pipeline_state.json).
---

# Web Auto-Build Master Skill Router

## Overview
This is the master coordinator for the **7-Step Web Automatic Creation & Evolution Pipeline**. Loading this skill automatically equips the agent with capabilities spanning from content extraction to decoupled CSS skinning.

All pipeline processes are strictly tracked using a physical state lock file `.pipeline_state.json` to ensure stage-by-stage execution and prevent skipping.

### 🔌 Execution Paths (Modular Workflows)
Depending on project requirements, you can invoke these skills in two ways:
1. **Direct Build Mode**: If the user wants a standard functional page layout directly, execute **`web-autobuild`** directly.
2. **Premium Design-Build Mode**: If the user requires a highly styled, premium visual brand system, execute **`web-design`** first to configure design tokens, colors, and layout aesthetics, and then proceed with **`web-autobuild`**.

---

## 1. Multi-Agent & Tool Compatibility
This skill and its sub-skills are fully portable across modern AI agent environments:
*   **Antigravity 2.0**: Load globally via `~/.gemini/config/skills/` or locally via `.agents/skills/` directory.
*   **Claude Code**: Symlink this directory into `.claude/skills/`.
*   **Cursor**: Add this directory or copy rules into `.cursor/rules/`.
*   **Copilot / Windsurf**: Reference via `.github/copilot-instructions.md` or `.windsurfrules`.

---

## 2. Progressive Loading Protocol (Token-Saving Rules)
To reduce token consumption and prevent context window fatigue, **DO NOT** read all sub-skills at once.
1.  Read `.pipeline_state.json` first to identify `current_phase = N`.
2.  **Only load** the sub-skill markdown file corresponding to Phase $N$ (e.g. `sub-skills/N-*.md`).
3.  Upon completing Phase $N$ and running its DoD, unload Phase $N$'s instructions and load Phase $N+1$'s.

---

## 3. Subagent Dispatch & Guarding Protocol

When dispatching parallel or nested Subagents, follow these strict execution boundaries:

### ⚠️ Subagent Execution Mode Selection
Before spawning any subagent, you **MUST** evaluate the mode selection.

1.  **Manual Mode (Interactive Prompting)**:
    *   **Action**: Present the options, state locks, and risks clearly to the human partner. Ask them to confirm.
2.  **Auto-Process Mode (Autonomous Task Pipeline)**:
    *   **Action**: If executing via an automated script/CI pipeline (e.g. *Auto-Pilot*, *Auto-Process*), **DO NOT** block on prompting. **YOU MUST DEFAULT TO the Recommended Mode** below to protect workspace integrity.

### 🛡️ Recommended Mode: sandbox isolation (`workspace = branch` or `share`)
*   **Rationale**: Parallel subagents working in the same branch will cause Git merge conflicts and corrupt the single `.pipeline_state.json` file.
*   **Rules**:
    *   **Always spawn** subagents in an isolated workspace branch (e.g., `git worktree` or MCP sandbox isolation).
    *   **Never allow** multiple subagents to write to the same `.pipeline_state.json` concurrently.
    *   **Commitment Gate**: The parent Agent acts as the *Gatekeeper*. Before merging a subagent's branch, you **MUST** run the verification suite (`pipeline_validator.py`) against their output files. If the validator fails, reject the merge and feed the errors back to the subagent.

---

## 4. Directory Structure

```text
web-autobuild/
├── SKILL.md                          <-- (This file) Master Coordinator & Entrypoint
└── sub-skills/
    ├── 1-content-extraction.md       <-- Phase 1: Raw content extraction & validation
    ├── 2-narrative-alignment.md      <-- Phase 2: Buyer mental model & narrative alignment
    ├── 3-data-structuring.md         <-- Phase 3: Data structuring & Schema JSON-LD
    ├── 4-geo-anchors.md              <-- Phase 4: GEO anchor mapping & navigation ID injection
    ├── 5-skeleton-html.md            <-- Phase 5: Semantic HTML5 skeleton creation
    ├── 6-web-components.md           <-- Phase 6: Component imports & custom elements hydration
    ├── 7-style-separation.md         <-- Phase 7: Three-tier CSS style separation & verification
    └── 8-merging-gatekeeper.md       <-- Phase 8: Merging gatekeeper & CI/CD sandbox integration
```


---

## 5. Whitepaper Reference
The pipeline is designed to conform to the high-extensibility CSS separation standard. Reference the global design whitepaper for detailed guidelines:
*   Relative URI: [webcss_design_whitepaper.md](../../docs/webcss_design_whitepaper.md)

---

## 6. Physical State Lock Protocol (`.pipeline_state.json`)
... [remaining content truncated for mapping] ...
### [Phase 1: Content Extraction](sub-skills/1-content-extraction.md)
*   **Trigger**: Ready to begin webpage creation. Extract parameters, specifications, locations, and copy points.
*   **Action**: Follow `1-content-extraction.md`.

### [Phase 2: Narrative Alignment](sub-skills/2-narrative-alignment.md)
*   **Trigger**: Content extracted. Convert specifications to customer value maps.
*   **Action**: Follow `2-narrative-alignment.md`.

### [Phase 3: Data Structuring](sub-skills/3-data-structuring.md)
*   **Trigger**: Narrative copy drafted. Generate Schema.org JSON-LD structured data.
*   **Action**: Follow `3-data-structuring.md`.

### [Phase 4: GEO Anchors](sub-skills/4-geo-anchors.md)
*   **Trigger**: Data structure ready. Inject unique LLM-scannable ID anchors.
*   **Action**: Follow `4-geo-anchors.md`.

### [Phase 5: Skeleton HTML](sub-skills/5-skeleton-html.md)
*   **Trigger**: ID mapping finalized. Build semantic HTML grid and block templates.
*   **Action**: Follow `5-skeleton-html.md`.

### [Phase 6: Web Components](sub-skills/6-web-components.md)
*   **Trigger**: Semantic HTML built. Inject custom elements and hydrate templates.
*   **Action**: Follow `6-web-components.md`.

### [Phase 7: Style Separation & Visual Design](sub-skills/7-style-separation.md)
*   **Trigger**: HTML fully hydrated. Consult [web-design](../web-design/SKILL.md) for global design tokens, color philosophy, and interactive card transitions. Then, apply styles into `variables.css`, `layout.css`, and `theme.css`. Run the test harness.
*   **Action**: Follow `7-style-separation.md`.

### [Phase 8: Merging Gatekeeper](sub-skills/8-merging-gatekeeper.md)
*   **Trigger**: Subagent request PR merge. Run static checker and merge state locks.
*   **Action**: Follow `8-merging-gatekeeper.md`.


