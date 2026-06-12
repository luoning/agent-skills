import os
import sys
import yaml

def parse_skill_file(filepath):
    """
    Parses a SKILL.md file and extracts name, description, and markdown contents.
    """
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    if not content.startswith("---"):
        return None
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
        
    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return {
            "name": frontmatter.get("name"),
            "description": frontmatter.get("description"),
            "body": body
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def generate_cursor_rules():
    """
    Scans the skills/ directory and outputs Cursor MDC rules in .cursor/rules/
    """
    skills_dir = "skills"
    output_dir = os.path.join(".cursor", "rules")
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(skills_dir):
        print(f"Error: {skills_dir} folder not found.")
        sys.exit(1)
        
    # Standard glob bindings for matching rules
    glob_bindings = {
        "skills-auditor": ["skills/**/*.md", "README.md"],
        "web-autobuild": ["SofreightWorkspace/oversea/track/**/*.html", "SofreightWorkspace/oversea/track/**/*.css", "SofreightWorkspace/oversea/track/**/*.js"],
        "web-design": ["SofreightWorkspace/oversea/track/**/*.css", "SofreightWorkspace/oversea/track/css/variables.css"]
    }
    
    generated_count = 0
    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            if file.lower() == "skill.md":
                skill_path = os.path.join(root, file)
                skill_data = parse_skill_file(skill_path)
                if skill_data:
                    name = skill_data["name"]
                    description = skill_data["description"]
                    body = skill_data["body"]
                    
                    globs = glob_bindings.get(name, ["*"])
                    
                    # Generate MDC content with yaml frontmatter
                    mdc_content = f"""---
description: {description}
globs: {globs}
alwaysApply: false
---

{body}
"""
                    output_file = os.path.join(output_dir, f"{name}.mdc")
                    with open(output_file, "w", encoding="utf-8") as out_f:
                        out_f.write(mdc_content)
                    print(f"Generated Cursor Rule: {output_file}")
                    generated_count += 1
                    
    print(f"\nSuccessfully generated {generated_count} Cursor rules (*.mdc) in .cursor/rules/")

if __name__ == "__main__":
    generate_cursor_rules()
