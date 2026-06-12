import os
import sys
import json
import shutil

def swap_active_context(target_skill: str, workspace_dir: str = "."):
    """
    Reads config.json routing rules, resolves the dependency chain for the target skill,
    and dynamically compiles a singular .cursor/rules/active-context.mdc rule containing
    ONLY the active skill and its direct pre-requisites.
    
    This physical swapper prevents instruction drift and saves agent token contexts.
    """
    config_path = os.path.join(workspace_dir, "config.json")
    if not os.path.exists(config_path):
        print(f"Error: config.json not found at {os.path.abspath(config_path)}.")
        sys.exit(1)
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    rules = config.get("routing_rules", {})
    if target_skill not in rules:
        print(f"Error: Target skill '{target_skill}' is not registered in routing_rules.")
        print(f"Available rules: {list(rules.keys())}")
        sys.exit(1)
        
    # Resolve dependency list (DFS)
    visited = []
    def resolve(name):
        if name in visited:
            return
        if name not in rules:
            return
        for dep in rules[name].get("dependencies", []):
            resolve(dep)
        visited.append(name)
        
    resolve(target_skill)
    print(f"Resolved context stack: {visited}")
    
    # Compile singular MDC rule file
    mdc_content = f"""---
description: "Active context rule loaded dynamically. Currently focused on stage: {target_skill}."
globs: "*"
---

# ACTIVE WORKFLOW CONTEXT: {target_skill.upper()}

> [!NOTE]
> This rule was compiled dynamically by the context swapper.
> Only the rules for the current active development phase are loaded below.

"""

    for skill_name in visited:
        skill_path = os.path.join(workspace_dir, rules[skill_name]["path"])
        if not os.path.exists(skill_path):
            print(f"Warning: Skill file not found: {skill_path}")
            continue
            
        with open(skill_path, "r", encoding="utf-8") as sf:
            raw_text = sf.read()
            
        # Strip frontmatter
        cleaned_text = raw_text
        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                cleaned_text = parts[2].strip()
                
        mdc_content += f"\n---\n\n## [{skill_name.upper()} MODULE]\n\n{cleaned_text}\n"

    # Ensure .cursor/rules/ exists
    rules_dir = os.path.join(workspace_dir, ".cursor", "rules")
    os.makedirs(rules_dir, exist_ok=True)
    
    active_mdc_path = os.path.join(rules_dir, "active-context.mdc")
    with open(active_mdc_path, "w", encoding="utf-8") as f:
        f.write(mdc_content)
        
    print(f"Successfully compiled dynamic context: {active_mdc_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/context_swapper.py <target_skill>")
        sys.exit(1)
    swap_active_context(sys.argv[1])
