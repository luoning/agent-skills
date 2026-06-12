import os
import sys
import json
import pytest
import shutil
import tempfile

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))
from context_swapper import swap_active_context

def test_context_swapper_resolves_dag():
    """Verify that context swapper resolves dependencies using DFS and outputs clean MDC rule."""
    temp_dir = tempfile.mkdtemp()
    
    # 1. Build Mock config.json containing DAG routing dependencies
    mock_config = {
        "routing_rules": {
            "workflow-contract": {
                "path": "skills/workflow-contract.md",
                "dependencies": []
            },
            "url-extractor": {
                "path": "skills/url-extractor.md",
                "dependencies": ["workflow-contract"]
            }
        }
    }
    
    with open(os.path.join(temp_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(mock_config, f)
        
    # 2. Write Mock Skills
    skills_dir = os.path.join(temp_dir, "skills")
    os.makedirs(skills_dir, exist_ok=True)
    
    with open(os.path.join(skills_dir, "workflow-contract.md"), "w", encoding="utf-8") as f:
        f.write("---\nname: workflow-contract\n---\nRule: Do not pollute workspace.")
        
    with open(os.path.join(skills_dir, "url-extractor.md"), "w", encoding="utf-8") as f:
        f.write("---\nname: url-extractor\n---\nRule: Extract POE assets.")
        
    # 3. Execute Swapper focusing on url-extractor
    swap_active_context("url-extractor", workspace_dir=temp_dir)
    
    # 4. Assert singular MDC output is generated inside .cursor/rules/
    active_mdc = os.path.join(temp_dir, ".cursor", "rules", "active-context.mdc")
    assert os.path.exists(active_mdc)
    
    with open(active_mdc, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Order verification (DFS resolves dependencies first)
    assert "WORKFLOW-CONTRACT MODULE" in content
    assert "URL-EXTRACTOR MODULE" in content
    assert content.index("WORKFLOW-CONTRACT MODULE") < content.index("URL-EXTRACTOR MODULE")
    
    shutil.rmtree(temp_dir)
