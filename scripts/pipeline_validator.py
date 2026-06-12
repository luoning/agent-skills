import os
import sys
import json
import re

def validate_pipeline(workspace_dir):
    """
    Performs automated DoD checkgates for Phase 1 to Phase 7.
    """
    state_file = os.path.join(workspace_dir, ".pipeline_state.json")
    if not os.path.exists(state_file):
        print(f"Error: Physical pipeline state file {state_file} does not exist.")
        sys.exit(1)
        
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
        
    current_phase = state.get("current_phase", 1)
    print(f"Checking project state in {workspace_dir}. Current phase: {current_phase}")
    
    # ------------------------------------------------------------------------
    # Phase 1 Check: Fact Extraction File
    # ------------------------------------------------------------------------
    if current_phase >= 1:
        facts_file = os.path.join(workspace_dir, ".extracted_facts.json")
        if current_phase == 1 and not os.path.exists(facts_file):
            print("DoD Verification Failed: .extracted_facts.json must exist in Phase 1.")
            sys.exit(1)
        if os.path.exists(facts_file):
            try:
                with open(facts_file, "r", encoding="utf-8") as f:
                    facts = json.load(f)
                if not isinstance(facts, dict) or len(facts) == 0:
                    print("DoD Verification Failed: .extracted_facts.json is empty or invalid.")
                    sys.exit(1)
            except json.JSONDecodeError:
                print("DoD Verification Failed: .extracted_facts.json contains invalid JSON syntax.")
                sys.exit(1)

    # ------------------------------------------------------------------------
    # Phase 2 Check: Narrative Copy
    # ------------------------------------------------------------------------
    if current_phase >= 2:
        copy_file = os.path.join(workspace_dir, ".narrative_copy.md")
        if current_phase == 2 and not os.path.exists(copy_file):
            print("DoD Verification Failed: .narrative_copy.md must exist in Phase 2.")
            sys.exit(1)
        if os.path.exists(copy_file):
            with open(copy_file, "r", encoding="utf-8") as f:
                copy_content = f.read()
            # Prevent lazy/fluffy marketing terms
            fluffy_terms = ['最快', '最好', '顶级', '革命性', '无敌']
            found_fluff = [term for term in fluffy_terms if term in copy_content]
            if found_fluff:
                print(f"DoD Verification Failed: .narrative_copy.md contains fluffy marketing terms: {found_fluff}")
                sys.exit(1)

    # ------------------------------------------------------------------------
    # Phase 3 & 4 Checks: Structured Schema JSON-LD & GEO Anchors in HTML
    # ------------------------------------------------------------------------
    if current_phase >= 3:
        html_files = [f for f in os.listdir(workspace_dir) if f.endswith(".html")]
        # Fallback to search recursively if in track/ subdirectory
        if not html_files:
            track_dir = os.path.join(workspace_dir, "SofreightWorkspace/oversea/track")
            if os.path.exists(track_dir):
                html_files = [os.path.join(track_dir, f) for f in os.listdir(track_dir) if f.endswith(".html")]
        else:
            html_files = [os.path.join(workspace_dir, f) for f in html_files]

        for hf in html_files:
            with open(hf, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # Phase 3: Check Schema JSON-LD exists in head
            if current_phase == 3 and "application/ld+json" not in html_content:
                print(f"DoD Verification Failed: Schema JSON-LD metadata block missing in {os.path.basename(hf)}.")
                sys.exit(1)
                
            # Phase 4: Check GEO Anchors - ensure table rows or details have descriptive IDs, prevent id="faq-1" or id="row-2"
            if current_phase == 4:
                invalid_ids = re.findall(r'id=["\'](faq-\d+|row-\d+|tr-\d+|table-\d+)["\']', html_content, re.IGNORECASE)
                if invalid_ids:
                    print(f"DoD Verification Failed: {os.path.basename(hf)} contains non-semantic sequential IDs: {invalid_ids}")
                    sys.exit(1)

    # ------------------------------------------------------------------------
    # Phase 5 & 6 Checks: HTML Grid Classes & Component Shadow/Inline Styles
    # ------------------------------------------------------------------------
    if current_phase >= 5:
        # Check layout CSS file exists
        layout_path = os.path.join(workspace_dir, "SofreightWorkspace/oversea/track/css/layout.css")
        if current_phase == 5 and not os.path.exists(layout_path):
            print("DoD Verification Failed: layout.css must be initialized in Phase 5.")
            sys.exit(1)

    if current_phase >= 6:
        # Check Web Components modules
        comp_dir = os.path.join(workspace_dir, "SofreightWorkspace/oversea/track/components")
        if os.path.exists(comp_dir):
            js_components = [os.path.join(comp_dir, f) for f in os.listdir(comp_dir) if f.endswith(".js")]
            for jsc in js_components:
                with open(jsc, "r", encoding="utf-8") as f:
                    js_content = f.read()
                # Check for inline HTML styles pollution inside components JS
                if re.search(r'style=["\'][^"\']*color|style=["\'][^"\']*display|style=["\'][^"\']*padding', js_content, re.IGNORECASE):
                    print(f"DoD Verification Failed: Web Component {os.path.basename(jsc)} contains forbidden inline CSS style declarations.")
                    sys.exit(1)

    # ------------------------------------------------------------------------
    # Phase 7 Check: Style Separation
    # ------------------------------------------------------------------------
    layout_path = os.path.join(workspace_dir, "SofreightWorkspace/oversea/track/css/layout.css")
    if current_phase == 7 and os.path.exists(layout_path):
        with open(layout_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verify color keywords, hex and rgb/rgba/hsl/hsla
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}', content)
        rgb_colors = re.findall(r'\brgb\s*\([^)]*\)', content, re.IGNORECASE)
        rgba_colors = re.findall(r'\brgba\s*\([^)]*\)', content, re.IGNORECASE)
        hsl_colors = re.findall(r'\bhsl\s*\([^)]*\)', content, re.IGNORECASE)
        hsla_colors = re.findall(r'\bhsla\s*\([^)]*\)', content, re.IGNORECASE)
        
        keywords = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 
                    'purple', 'pink', 'brown', 'gray', 'grey', 'cyan', 'magenta', 
                    'transparent']
        keyword_pattern = r'\b(' + '|'.join(keywords) + r')\b'
        keyword_colors = []
        
        # Strip comments
        clean_content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        for line in clean_content.splitlines():
            if ':' in line:
                prop, val = line.split(':', 1)
                matches = re.findall(keyword_pattern, val, re.IGNORECASE)
                if matches:
                    keyword_colors.extend(matches)
        
        if len(hex_colors) > 0 or len(rgb_colors) > 0 or len(rgba_colors) > 0 or len(hsl_colors) > 0 or len(hsla_colors) > 0 or len(keyword_colors) > 0:
            print("CSS Verification Failed: layout.css contains raw color declarations!")
            print(f"Hex: {hex_colors}")
            print(f"RGB/RGBA: {rgb_colors} {rgba_colors}")
            print(f"HSL/HSLA: {hsl_colors} {hsla_colors}")
            print(f"Keywords: {keyword_colors}")
            sys.exit(1)
            
    print("Static verification completed successfully!")

if __name__ == "__main__":
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    validate_pipeline(workspace)

