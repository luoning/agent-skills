# 🛡️ AI Agent Skills Framework

> **The Physical Sandbox & Aesthetic Governance Suite for Coding Agents**  
> Stop letting AI "vibe code." A contract-driven development, anti-style-leak, and runtime self-healing agent skill library for Cursor, Claude Code, Windsurf, and Copilot.

[简体中文](./README_zh.md)

<p align="center">
  <img src="https://img.shields.io/badge/Cursor-MDC%20Ready-0ea5e9?style=for-the-badge&logo=cursor" alt="Cursor MDC Ready">
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-6366f1?style=for-the-badge&logo=anthropic" alt="Claude Code Compatible">
  <img src="https://img.shields.io/badge/Windsurf-Supported-10b981?style=for-the-badge&logo=windsurf" alt="Windsurf Supported">
  <img src="https://img.shields.io/badge/Autopilot-Sandboxed-f43f5e?style=for-the-badge" alt="Autopilot Sandboxed">
</p>

---

## 💡 Why Do You Need It?

Under large contexts or complex coding workflows, AI coding agents often suffer from **"Instruction Drift"**, resulting in:
*   **Evasion & Laziness**: AI hardcodes inline styles (e.g. `style="color: #fff"`) or pollutes structure layout files with raw hex/rgb constants.
*   **Coupled Styling**: Skeleton layout structures (`layout.css`) and dynamic themes (`theme.css`) get combined, preventing easy rebranding.
*   **Runtime Exceptions**: Generated web components crash due to improper lifecycle mounting.

### 🚨 Anti-Evasion Matrix

| Scenario | Traditional Approach (Soft Rules) | This Framework (Hard Sandboxing) | Outcome |
| :--- | :--- | :--- | :--- |
| **Absolute Path Leak** | Prompts asking to "use relative links" | **Skill Auditor Gate**: `skill_integrity_auditor.py` blocks any skill containing absolute drive paths or local protocol links. | **Enforced Portability** |
| **Hardcoded Inline Colors** | Prompts asking to "use CSS variables" | **DoD Gatekeeper**: `pipeline_validator.py` scans and blocks any inline color styling in HTML or Web Components. | **Strict Separated CSS** |
| **Fact Hallucination** | Standard AI hallucinations in copywriting | **Bidirectional Fact Lock**: Cross-validates all page parameters against `.extracted_facts.json` and flags unmapped numbers. | **Pure Fact Consistency** |
| **Broken Data Lineage** | Hardcoded numbers without data trace | **Data Lineage Validator**: Blocks page integration if numerical facts lack explicit trace tags (`data-fact-source`). | **100% Traceability** |
| **Skipping Pipeline Stages** | Agent decides flow dynamically | **Physical State Lock**: Code changes are blocked unless the preceding stage in `.pipeline_state.json` is completed. | **Step-by-Step Delivery** |
| **Subagent Concurrency** | Race conditions and git conflicts | **Sandbox Isolation Gate**: Enforces `workspace = branch` isolation. Parent Agent acts as merge reviewer. | **Safe Autopilot Merge** |

---

## 📂 Repository Structure

```text
agent-skills/
├── README.md                      <-- Global English documentation
├── README_zh.md                   <-- Chinese documentation
├── config.json                    <-- Skills configurations
├── scripts/
│   ├── install.sh                 <-- One-click curl installer script
│   ├── pipeline_validator.py      <-- Static checkgate validator
│   ├── skill_integrity_auditor.py <-- Meta-skill compliance checker
│   └── generate_mdc.py            <-- MDC rules compiler
└── skills/
    ├── web-autobuild/
    │   ├── SKILL.md               <-- [Master] 10-Phase Web industrial pipeline
    │   └── sub-skills/
    │       ├── 1-content-extraction.md
    │       ├── 2-narrative-alignment.md
    │       ├── 3-data-structuring.md
    │       ├── 4-geo-anchors.md
    │       ├── 5-skeleton-html.md
    │       ├── 6-web-components.md
    │       ├── 7-style-separation.md
    │       ├── 8-merging-gatekeeper.md <-- Phase 8: Concurrency merging gateway
    │       ├── 9-runtime-debugging.md  <-- Phase 9: Runtime self-healing loop
    │       └── 10-vibecoding-defense.md <-- Phase 10: Vibe Coding facts lock and decision gateway
    ├── web-design/
    │   └── SKILL.md               <-- [Aesthetics] B2B visual design system and contrast token schema
    └── common-checks/
        └── SKILL.md               <-- Meta-skill auditor & broken links blocker
```

---

## ⚡ Quick Start (1-Minute Setup)

### Option 1: One-click Installer (Recommended)
Run the following command in the **root of your target project** to fetch the skills, deploy the checking scripts, and **automatically compile local Cursor MDC rules**:

```bash
curl -fsSL https://raw.githubusercontent.com/username/agent-skills/main/scripts/install.sh | bash
```

### Option 2: Compile MDC Rules Locally
If you cloned this repository, compile the relative skills into Cursor native rules `.cursor/rules/*.mdc`:
```bash
python scripts/generate_mdc.py
```
Cursor will now dynamically load corresponding phase rules on-demand based on the files you modify, minimizing token consumption.

---

## 🔌 Core Developer Workflows

### Flow 1: Direct Build Mode
Invoke `web-autobuild` directly. The agent scaffolds functional layouts, hooks custom components, runs static validation, and merges the pipeline.

### Flow 2: Premium Design-Build Mode
1. Run `web-design` first. The Agent plans variables, typography letter-spacing, and transition curves.
2. Trigger `web-autobuild` afterwards. Visual properties are inherited as Phase 1 input variables, delivering a polished, high-fidelity landing page.

---

## 🔬 Core Gates Mechanisms

### Gate 1: Project-level `pipeline_validator.py`
Fails integration pipeline if styling variables leak or facts mismatch:
*   **Block**: Hex/RGB/HSL declarations or color keywords inside `layout.css`.
*   **Block**: Colors declared inside inline HTML style attributes.
*   **Block**: Unregistered business numerical fact or broken data lineage (`data-fact-source`).
*   **Self-Healing recovery**: Automatically compiles a `.pipeline_fix_suggestions.json` mapping out actionable correction guidelines (such as `approve_decision` or `correct_data_source`) on failure.

### Gate 2: Skill-level `skill_integrity_auditor.py`
Ensures portability of the skills repository:
*   **Block**: Any local absolute path or disk drive prefixes (e.g. windows/unix absolute paths).
*   **Block**: Syntax error in YAML frontmatter or missing trigger description.
