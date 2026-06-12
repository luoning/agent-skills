#!/bin/bash
set -e

echo "========================================================"
echo "⚡ AI Agent Skills - One-Click Installer & Rule Compiler ⚡"
echo "========================================================"

# 1. Download scripts and skills structure from repository
REPO_RAW_URL="https://raw.githubusercontent.com/luoning/agent-skills/master"

echo "📥 Creating target directories..."
mkdir -p scripts skills/common-checks skills/web-autobuild/sub-skills skills/web-design .cursor/rules

echo "📥 Fetching helper scripts..."
curl -fsSL "$REPO_RAW_URL/scripts/pipeline_validator.py" -o scripts/pipeline_validator.py
curl -fsSL "$REPO_RAW_URL/scripts/skill_integrity_auditor.py" -o scripts/skill_integrity_auditor.py
curl -fsSL "$REPO_RAW_URL/scripts/generate_mdc.py" -o scripts/generate_mdc.py

echo "📥 Fetching core skills specifications..."
curl -fsSL "$REPO_RAW_URL/skills/common-checks/SKILL.md" -o skills/common-checks/SKILL.md
curl -fsSL "$REPO_RAW_URL/skills/web-design/SKILL.md" -o skills/web-design/SKILL.md
curl -fsSL "$REPO_RAW_URL/skills/web-autobuild/SKILL.md" -o skills/web-autobuild/SKILL.md

# Fetch web-autobuild sub-skills
for phase in 1-content-extraction 2-narrative-alignment 3-data-structuring 4-geo-anchors 5-skeleton-html 6-web-components 7-style-separation 8-merging-gatekeeper 9-runtime-debugging 10-vibecoding-defense; do
  curl -fsSL "$REPO_RAW_URL/skills/web-autobuild/sub-skills/$phase.md" -o "skills/web-autobuild/sub-skills/$phase.md"
done

# 2. Run the MDC rules compiler
if command -v python3 &>/dev/null; then
  echo "⚙️ Compiling Cursor MDC rules..."
  python3 scripts/generate_mdc.py
elif command -v python &>/dev/null; then
  echo "⚙️ Compiling Cursor MDC rules..."
  python scripts/generate_mdc.py
else
  echo "⚠️ Warning: Python not found. Please run 'python scripts/generate_mdc.py' manually to compile Cursor MDC rules."
fi

echo "========================================================"
echo "🚀 Installation completed successfully! "
echo "Your AI coding agents are now fully sandboxed and governed."
echo "========================================================"
