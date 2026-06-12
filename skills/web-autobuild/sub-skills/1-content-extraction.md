# Phase 1: Content Extraction, Fact Lock & Decision Scoping

## Trigger
Use when beginning a new webpage creation task, before planning navigation or skeleton structure. This phase establishes the absolute baseline of business truth and user-decision guardrails.

---

## 1. Core Principles for Vibe Coding

Vibe Coding requires strict boundaries to prevent LLM hallucinations from corrupting business facts while lowering the cognitive load of decision-making for junior operators.

### 🔒 Fact Enforcement Lock (事实一致性锁)
*   **Facts Decoupled from Prompting**: Only extract and lock down concrete parameters (pricing tables, port codes, SLA times, hardware specs) explicitly defined in the initial input.
*   **Consistency Bound**: The parsed data is saved in `.extracted_facts.json`. In subsequent phases, any code generated (HTML/JS) **MUST** match these values exactly. Any missing or added parameter is treated as a hallucination error and will fail the DoD validator.

### ⚖️ LLM Recommendation & Human Gate (人机协作决策降噪)
LLM intelligence should simplify decisions, not bypass human judgment. 
1.  **AI Proposes**: For missing layout details or functional suggestions, the AI must output a `.decision_pending.json` mapping:
    *   `proposal_id`: A unique suggestion index.
    *   `context`: Why the AI suggests this (e.g. "Add tooltip to explain USLAX port fee calculation").
    *   `complexity`: Cognitive impact (`low`/`medium`/`high`).
    *   `human_approved`: Must default to `false`.
2.  **Human Decides**: The human operator must manually review the proposals, toggling `human_approved` to `true` or `false`.
3.  **Engine Executes**: The pipeline will block any code execution for a proposal unless it has been explicitly approved by the human operator.

---

## 2. Definition of Done (DoD)
- [ ] A structured `.extracted_facts.json` is generated containing locked business facts.
- [ ] A `.decision_pending.json` is generated listing all AI design recommendations with default approval states set to `false`.
- [ ] The `.pipeline_state.json` phase 1 status is marked as `completed`.
