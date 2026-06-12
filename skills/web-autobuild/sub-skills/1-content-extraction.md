# Phase 1: Content Extraction & Fact Verification

## Trigger
Use when beginning a new web page creation task, before planning navigation or layout.

---

## 1. Core Principles
*   **Facts Over Speculation**: Only extract facts explicitly provided in inputs (numbers, locations, SLAs, terms).
*   **Structure Entity Mapping**: Identify all domain-specific entities (e.g., standard airport/seaport codes, pricing tiers, hardware specs).
*   **Aesthetic Theme Alignment**: Identify the required design theme inputs (e.g., brand colors, typography tone, visual style rules) and align them with the `web-design` system guidelines to prepare variable scoping.

---

## 2. Definition of Done (DoD)
*   [ ] A structured `.extracted_facts.json` file is generated containing all parsed entities and core parameters.
*   [ ] The `.pipeline_state.json` phase 1 status is marked as `completed`.
