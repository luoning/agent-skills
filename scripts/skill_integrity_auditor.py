import os
import sys
import re
import yaml



def check_markdown_links(content, skill_md_path):
    links = re.findall(r'\[([^\]]*)\]\((file:///|(?!\w+://))([^)]*)\)', content)
    base_dir = os.path.dirname(skill_md_path)
    
    for text, protocol, path in links:
        if path.startswith("http") or path.startswith("mailto"):
            continue
            
        import urllib.parse
        clean_path = urllib.parse.unquote(path.split("#")[0].replace("file:///", ""))
        target_abs_path = os.path.abspath(os.path.join(base_dir, clean_path)) if not os.path.isabs(clean_path) else os.path.abspath(clean_path)

        
        if "石頭和碼" in target_abs_path or "石头和码" in target_abs_path:
            resolved = False
            for root, dirs, files in os.walk(os.path.dirname(target_abs_path)):
                for file in files:
                    if os.path.basename(target_abs_path).lower() == file.lower():
                        resolved = True
                        break
            if resolved:
                continue

        if not os.path.exists(target_abs_path):
            if not os.path.exists(os.path.join(workspace_root(skill_md_path), clean_path)):
                print(f"Error: Broken link found in SKILL.md -> [{text}]({path}). Resolved path: {target_abs_path}")
                return False
    print(f"Links verification successful for non-entrypoint file: {os.path.basename(skill_md_path)}")
    return True

def audit_single_skill(skill_md_path):
    """
    Audits a single SKILL.md file for compliance with best practices.
    """
    print(f"Auditing Skill file: {skill_md_path}")
    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} does not exist.")
        return False

    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Frontmatter check
    is_main_skill = os.path.basename(skill_md_path).lower() == "skill.md"
    if not is_main_skill:
        if not content.startswith("---"):
            print(f"Skipping frontmatter validation for non-entrypoint file: {os.path.basename(skill_md_path)}")
            # Check for hardcoded absolute paths / drive letters (e.g. F:/, E:/, C:/, D:/ or file:///C:, file:///D:, file:///E:, file:///F:)
            hardcoded_drive_paths = re.findall(r'(?i)\b(?:[c-z]:[\\/]|file:\/\/\/[c-z]:)', content)
            if hardcoded_drive_paths:
                print(f"Error: Hardcoded absolute drive paths found in {os.path.basename(skill_md_path)}: {hardcoded_drive_paths}")
                return False
            return check_markdown_links(content, skill_md_path)

    if not content.startswith("---"):
        print("Error: SKILL.md must start with YAML frontmatter delimiters '---'.")
        return False
        
    parts = content.split("---", 2)
    if len(parts) < 3:
        print("Error: Invalid frontmatter formatting. Missing closing '---'.")
        return False

    try:
        frontmatter = yaml.safe_load(parts[1])
    except Exception as e:
        print(f"Error parsing YAML frontmatter: {e}")
        return False

    # Frontmatter rules
    name = frontmatter.get("name")
    description = frontmatter.get("description", "")

    if not name or not re.match(r'^[a-z0-9-]+$', name):
        print(f"Error: 'name' field ({name}) must use lowercase letters, numbers, and hyphens only.")
        return False

    if not description.strip().startswith("Use when"):
        print("Error: 'description' must start with standard trigger keyword 'Use when...'.")
        return False

    # Check for process summary violation in description
    if any(keyword in description.lower() for keyword in ["then do", "steps:", "first", "next", "finally"]):
        print("Warning: 'description' should describe triggering symptoms, NOT summarize the workflow steps.")

    # 2. Check for hardcoded absolute paths / drive letters (e.g. F:/, E:/, C:/, D:/ or file:///C:, file:///D:, file:///E:, file:///F:)
    hardcoded_drive_paths = re.findall(r'(?i)\b(?:[c-z]:[\\/]|file:\/\/\/[c-z]:)', content)
    if hardcoded_drive_paths:
        print(f"Error: Hardcoded absolute drive paths found in {os.path.basename(skill_md_path)}: {hardcoded_drive_paths}")
        return False

    # 3. Check for markdown link targets availability
    return check_markdown_links(content, skill_md_path)


def workspace_root(file_path):
    # Crawl up to find config.json or README.md
    curr = os.path.abspath(file_path)
    while True:
        parent = os.path.dirname(curr)
        if parent == curr:
            return "."
        if os.path.exists(os.path.join(parent, "config.json")) or os.path.exists(os.path.join(parent, "README.md")):
            return parent
        curr = parent

def audit_repository(repo_path):
    # Audit README.md if exists
    readme_path = os.path.join(repo_path, "README.md")
    if os.path.exists(readme_path):
        print(f"Auditing repository README: {readme_path}")
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        hardcoded_drive_paths = re.findall(r'(?i)\b(?:[c-z]:[\\/]|file:\/\/\/[c-z]:)', readme_content)
        if hardcoded_drive_paths:
            print(f"Error: Hardcoded absolute drive paths found in README.md: {hardcoded_drive_paths}")
            sys.exit(1)

    skills_dir = os.path.join(repo_path, "skills")
    if not os.path.exists(skills_dir):
        print(f"Error: skills folder not found under {repo_path}")
        sys.exit(1)

    all_passed = True
    for root, dirs, files in os.walk(skills_dir):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                if not audit_single_skill(md_path):
                    all_passed = False
                    
    if not all_passed:
        print("\nRepository Audit FAILED!")
        sys.exit(1)
    else:
        print("\nAll Skills and README in Repository are fully compliant (AUDIT PASSED)!")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if os.path.isdir(target):
        audit_repository(target)
    else:
        success = audit_single_skill(target)
        sys.exit(0 if success else 1)
