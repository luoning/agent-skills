import os
import sys
import json
import pytest
import shutil
import tempfile

# Add scripts directory to sys.path to import validate_pipeline
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts"))
from pipeline_validator import validate_pipeline

@pytest.fixture
def temp_workspace():
    """Creates a temporary workspace with standard configuration."""
    temp_dir = tempfile.mkdtemp()
    
    # Initialize basic pipeline state
    state = {
        "current_phase": 3,
        "schema_version": "1.0.0",
        "src_dir": "."
    }
    with open(os.path.join(temp_dir, ".pipeline_state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f)
        
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_unsupported_schema_version(temp_workspace):
    # Set unsupported version
    state = {
        "current_phase": 1,
        "schema_version": "2.0.0"
    }
    with open(os.path.join(temp_workspace, ".pipeline_state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f)
        
    with pytest.raises(SystemExit) as excinfo:
        validate_pipeline(temp_workspace)
    assert excinfo.value.code == 1

def test_bilingual_fluffy_terms(temp_workspace):
    # Set current phase to 2
    with open(os.path.join(temp_workspace, ".pipeline_state.json"), "w", encoding="utf-8") as f:
        json.dump({"current_phase": 2, "schema_version": "1.0.0"}, f)
        
    # Test English fluffy term
    with open(os.path.join(temp_workspace, ".narrative_copy.md"), "w", encoding="utf-8") as f:
        f.write("Our service is world-class and revolutionary.")
        
    with pytest.raises(SystemExit) as excinfo:
        validate_pipeline(temp_workspace)
    assert excinfo.value.code == 1

def test_fact_enforcement_and_lineage(temp_workspace):
    # Establish facts
    facts = {
        "rates": {
            "drayage": {
                "base_rate": "850"
            }
        }
    }
    with open(os.path.join(temp_workspace, ".extracted_facts.json"), "w", encoding="utf-8") as f:
        json.dump(facts, f)
        
    # Write HTML with correct fact and data lineage
    html_content = """
    <html>
      <head>
        <script type="application/ld+json">{}</script>
      </head>
      <body>
        <div data-fact-source="rates.drayage.base_rate">850</div>
      </body>
    </html>
    """
    with open(os.path.join(temp_workspace, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # Validate - should pass without exit
    validate_pipeline(temp_workspace)

def test_broken_data_lineage_intercepts(temp_workspace):
    facts = {
        "rates": {"base_rate": "850"}
    }
    with open(os.path.join(temp_workspace, ".extracted_facts.json"), "w", encoding="utf-8") as f:
        json.dump(facts, f)
        
    # HTML contains invalid path in data-fact-source
    html_content = """
    <html>
      <head>
        <script type="application/ld+json">{}</script>
      </head>
      <body>
        <div data-fact-source="rates.invalid_path.rate">850</div>
      </body>
    </html>
    """
    with open(os.path.join(temp_workspace, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    with pytest.raises(SystemExit) as excinfo:
        validate_pipeline(temp_workspace)
    assert excinfo.value.code == 1
    
    # Check if recovery loop json was generated
    fix_file = os.path.join(temp_workspace, ".pipeline_fix_suggestions.json")
    assert os.path.exists(fix_file)
    with open(fix_file, "r", encoding="utf-8") as f:
        suggestions = json.load(f)
    assert suggestions["fix_type"] == "broken_lineage"

def test_reverse_hallucination_check(temp_workspace):
    facts = {
        "specs": {"ram": "16"}
    }
    with open(os.path.join(temp_workspace, ".extracted_facts.json"), "w", encoding="utf-8") as f:
        json.dump(facts, f)
        
    # HTML contains unregistered numeric value $999 USD
    html_content = """
    <html>
      <head>
        <script type="application/ld+json">{}</script>
      </head>
      <body>
        <div>Product spec: 16GB RAM</div>
        <div>Price: $999 USD</div>
      </body>
    </html>
    """
    with open(os.path.join(temp_workspace, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    with pytest.raises(SystemExit) as excinfo:
        validate_pipeline(temp_workspace)
    assert excinfo.value.code == 1
    
    # Verify recommendations
    fix_file = os.path.join(temp_workspace, ".pipeline_fix_suggestions.json")
    with open(fix_file, "r", encoding="utf-8") as f:
        suggestions = json.load(f)
    assert suggestions["fix_type"] == "hallucinated_fact"
