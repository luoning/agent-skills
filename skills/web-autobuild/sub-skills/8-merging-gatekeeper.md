# Phase 8: Merging Gatekeeper & CI Integration

## Trigger
Use when a Subagent has completed development in an isolated branch/sandbox and requests a merge (Pull Request) into the master branch.

---

## 1. Merging Processing Unit Flow
The merging unit must process the integration via a **Three-Stage Gatekeeper**:

```text
Subagent Branch (PR)
  ├── [Stage 1] File Boundary Check (Block if E:/Skills/docs or css/layout.css mutated without permission)
  ├── [Stage 2] Run pipeline_validator.py (Verify 100% color isolation and GEO anchors)
  └── [Stage 3] State Lock Merge Protocol (Safely merge branch artifact states into .pipeline_state.json)
```

---

## 2. Gatekeeper Verification Commands

### 1. Verification Command for CI
The parent agent or CI Runner **MUST** execute the check before performing a git merge:
```bash
python scripts/pipeline_validator.py [subagent_workspace_root]
```

### 2. Evasion & Failure Handling
If Stage 2 validation fails with `exit code 1`:
*   **DO NOT** force merge.
*   Extract the validation failure output.
*   Post the error logs to the subagent's feedback loop and issue the retry command:
    ```text
    CR FAILED: Merging blocked due to CSS color isolation leak or non-semantic GEO ID.
    Error Details: [Insert pipeline_validator.py stdout logs]
    Please fix and request merge again.
    ```

---

## 3. Lock Fusion Schema (Stage 3)
Upon successful validation, merge the local artifacts metadata:

```json
"phases": {
  "7": {
    "name": "style-separation",
    "status": "completed",
    "artifacts": {
      "drayage.html": "completed",
      "fba.html": "completed"
    }
  }
}
```
*   Only when all parallel artifacts in Phase $N$ are marked as `completed`, advance the global `current_phase` to $N+1$.
