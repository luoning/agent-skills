# Sub-skill: Scenario Tester (Verification Lifecycles)

## Overview
Enforces dynamic scenario tests ensuring logical correctness before archiving solutions.

## 1. Rules
- **Base Scenario Class**: All custom tests must inherit from `BaseScenarioTest`.
- **Four Testing Stages**:
  1. **Analyze Test Target**: Define test scope.
  2. **Build Test Scenario**: Prepare mock payloads/context.
  3. **Execute & Assert**: Execute parser, assert POE properties, and capture errors.
  4. **Review Intent Loopback**: Review output back against target project objectives.
