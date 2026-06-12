import os
import sys
import json
import re

def fail_with_suggestions(workspace_dir, error_msg, fix_type, suggestions):
    """
    Saves an automated recovery/fix patch into .pipeline_fix_suggestions.json
    to lower Vibe Coder debugging friction, and exits.
    """
    print(error_msg)
    fix_file = os.path.join(workspace_dir, ".pipeline_fix_suggestions.json")
    payload = {
        "status": "blocked",
        "error_message": error_msg,
        "fix_type": fix_type,
        "suggested_actions": suggestions
    }
    with open(fix_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    sys.exit(1)

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
        
    # Schema version checks for backward compatibility
    schema_version = state.get("schema_version", "1.0.0")
    supported_versions = ["1.0.0"]
    if schema_version not in supported_versions:
        print(f"Error: Unsupported state schema version '{schema_version}'. Supported: {supported_versions}")
        sys.exit(1)
        
    current_phase = state.get("current_phase", 1)
    
    # Dynamically resolve src_dir config
    src_dir_val = state.get("src_dir")
    if src_dir_val:
        src_dir = os.path.join(workspace_dir, src_dir_val)
    else:
        # Default directly to workspace root for generic environments
        src_dir = workspace_dir
            
    print(f"Checking project state in {workspace_dir}. Current phase: {current_phase}, Src directory: {src_dir}")
    
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

        # Check for Decision Pending approved status
        pending_file = os.path.join(workspace_dir, ".decision_pending.json")
        if os.path.exists(pending_file):
            try:
                with open(pending_file, "r", encoding="utf-8") as f:
                    decisions = json.load(f)
                unapproved = [d for d in decisions if not d.get("human_approved", False)]
                if unapproved:
                    unapproved_ids = [u.get('proposal_id') for u in unapproved]
                    err_msg = f"DoD Verification Failed: There are unapproved AI recommendations in .decision_pending.json: {unapproved_ids}"
                    fail_with_suggestions(
                        workspace_dir,
                        err_msg,
                        "unapproved_decision",
                        [
                            {
                                "action": "approve_decision",
                                "instruction": f"Open '.decision_pending.json' and change 'human_approved' to true for proposals: {unapproved_ids}"
                            },
                            {
                                "action": "rollback_code",
                                "instruction": f"Remove the implemented code block corresponding to proposals {unapproved_ids} from files if you reject them."
                            }
                        ]
                    )
            except json.JSONDecodeError:
                print("DoD Verification Failed: .decision_pending.json contains invalid JSON syntax.")
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
            # Prevent lazy/fluffy marketing terms (Bilingual support)
            fluffy_terms = [
                '最快', '最好', '顶级', '革命性', '无敌',
                'revolutionary', 'unmatched', 'game-changing', 
                'world-class', 'best-in-class', 'innovative'
            ]
            found_fluff = [term for term in fluffy_terms if re.search(r'\b' + re.escape(term) + r'\b', copy_content, re.IGNORECASE) or (term in copy_content and ord(term[0]) > 127)]
            if found_fluff:
                print(f"DoD Verification Failed: .narrative_copy.md contains fluffy marketing terms: {found_fluff}")
                sys.exit(1)

    # ------------------------------------------------------------------------
    # Phase 3 & 4 Checks: Structured Schema JSON-LD & GEO Anchors in HTML
    # ------------------------------------------------------------------------
    if current_phase >= 3:
        # Search HTML files inside the resolved src_dir
        html_files = []
        if os.path.exists(src_dir):
            if os.path.isdir(src_dir):
                html_files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith(".html")]
            elif src_dir.endswith(".html"):
                html_files = [src_dir]
        # Verify that all facts locked in .extracted_facts.json are physically present in HTML content to block hallucinations
        facts_file = os.path.join(workspace_dir, ".extracted_facts.json")
        has_facts = os.path.exists(facts_file)
        if has_facts:
            with open(facts_file, "r", encoding="utf-8") as f:
                facts_data = json.load(f)
            # Flatten dict values to verify
            def get_flat_values(d):
                vals = []
                for k, v in d.items():
                    if isinstance(v, dict):
                        vals.extend(get_flat_values(v))
                    elif isinstance(v, list):
                        for item in v:
                            if isinstance(item, dict):
                                vals.extend(get_flat_values(item))
                            else:
                                vals.append(str(item))
                    else:
                        vals.append(str(v))
                return vals
            flat_facts = get_flat_values(facts_data)

        for hf in html_files:
            with open(hf, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # Check fact enforcement lock
            if has_facts:
                for fact in flat_facts:
                    # Ignore short string noises (less than 3 chars)
                    if len(fact) >= 3 and fact not in html_content:
                        err_msg = f"DoD Verification Failed: Locked business fact '{fact}' is missing in generated webpage {os.path.basename(hf)}."
                        fail_with_suggestions(
                            workspace_dir,
                            err_msg,
                            "missing_fact",
                            [
                                {
                                    "action": "insert_fact",
                                    "instruction": f"Open '{os.path.basename(hf)}' and render the missing fact string: '{fact}'."
                                }
                            ]
                        )
                
                # Reverse Anti-Hallucination check: Detect arbitrary numerical values/specifications in HTML
                # (e.g. 1500, $250, 99.9%, 40HQ) and ensure they are backed by the facts list.
                # Exclude common visual/HTML attribute values (like 100%, 1px, 2026 for copyright) to prevent false positives.
                num_pattern = r'\b(?:\$|￥|€)?\d+(?:\.\d+)?(?:%|px|vh|vw|s|ms|deg)?\b'
                found_numbers = re.findall(num_pattern, html_content)
                
                # Extract numbers from flat facts for fast comparison
                flat_fact_numbers = set()
                for fact in flat_facts:
                    nums = re.findall(r'\d+(?:\.\d+)?', fact)
                    flat_fact_numbers.update(nums)
                
                # Common web layout and system numerical values to ignore
                system_ignore_list = {'100', '0', '1', '2', '3', '4', '8', '12', '24', '2026', '2025', '365', '16', '32', '64'}
                
                for num_str in found_numbers:
                    # Strip symbols to get the raw numeric component
                    raw_num = re.sub(r'[^\d.]', '', num_str)
                    if not raw_num or raw_num in system_ignore_list:
                        continue
                    
                    # Verify if this numerical fact exists in our locked facts
                    if raw_num not in flat_fact_numbers:
                        # Allow standard CSS unit styles like 1px, 100% but block potential business specification hallucinations
                        if not any(unit in num_str for unit in ['px', 'vh', 'vw', 'ms', 'deg']):
                            err_msg = f"DoD Verification Failed: Unregistered business numerical fact '{num_str}' detected in {os.path.basename(hf)}. This value is not declared in .extracted_facts.json!"
                            fail_with_suggestions(
                                workspace_dir,
                                err_msg,
                                "hallucinated_fact",
                                [
                                    {
                                        "action": "declare_fact",
                                        "instruction": f"Open '.extracted_facts.json' and add the missing specification/price/numerical value containing '{raw_num}'."
                                    },
                                    {
                                        "action": "remove_fact",
                                        "instruction": f"Open '{os.path.basename(hf)}' and delete/correct the unregistered number '{num_str}'."
                                    }
                                ]
                            )
                
                # Data Lineage Check: Verify all data-fact-source attributes resolve to valid keys in .extracted_facts.json
                lineage_sources = re.findall(r'data-fact-source=["\']([^"\']+)["\']', html_content)
                for src in lineage_sources:
                    # Resolve JSON dot notation path inside facts_data
                    parts = src.split('.')
                    current_node = facts_data
                    resolved = True
                    for part in parts:
                        if isinstance(current_node, dict) and part in current_node:
                            current_node = current_node[part]
                        elif isinstance(current_node, list):
                            try:
                                idx = int(part)
                                if 0 <= idx < len(current_node):
                                    current_node = current_node[idx]
                                else:
                                    resolved = False
                                    break
                            except ValueError:
                                resolved = False
                                break
                        else:
                            resolved = False
                            break
                    
                    if not resolved:
                        err_msg = f"DoD Verification Failed: Broken data lineage in {os.path.basename(hf)}. The data-fact-source '{src}' does not resolve to a valid fact key in .extracted_facts.json!"
                        fail_with_suggestions(
                            workspace_dir,
                            err_msg,
                            "broken_lineage",
                            [
                                {
                                    "action": "correct_data_source",
                                    "instruction": f"Inspect '{os.path.basename(hf)}' and correct the path '{src}' to point to a valid field inside '.extracted_facts.json'."
                                }
                            ]
                        )
            
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
        layout_path = os.path.join(src_dir, "css/layout.css")
        if current_phase == 5 and not os.path.exists(layout_path):
            print("DoD Verification Failed: layout.css must be initialized in Phase 5.")
            sys.exit(1)

    if current_phase >= 6:
        # Check Web Components modules
        comp_dir = os.path.join(src_dir, "components")
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
    layout_path = os.path.join(src_dir, "css/layout.css")
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

