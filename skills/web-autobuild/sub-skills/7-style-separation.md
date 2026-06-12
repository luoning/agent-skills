# Phase 7: Style Separation & Code Audit

## Trigger
Use when the Web Components (Phase 6) are hydrated, and you are styling the visual layout of the page. This is the final gatekeeping step.

---

## 1. Core Principles
1. **Physical Decoupling**: All styles must be divided into:
   *   `variables.css`: Holds pure CSS variables/tokens (brand colors, border-radius, font sizes, shadows).
   *   `layout.css`: Focuses purely on width, display, position, padding, margin, flex, grid. **Zero colors/borders/backgrounds/shadows**.
   *   `theme.css`: Holds interactive hover animations, fonts, cards textures. Colors must reference variables.
2. **Absolute Color Isolation**: No hardcoded color declarations (hex, rgb, rgba, hsl, hsla, keywords) are allowed in layout files or HTML inline style attributes.

---

## 2. Definition of Done (DoD)
- [ ] CSS files are physically split into `variables.css`, `layout.css`, and `theme.css`.
- [ ] Comprehensive verification script runs and reports 100% success.
- [ ] No inline style with color definition exists in HTML.
- [ ] `.pipeline_state.json` is updated with `phases["7"].status = "completed"`.

---

## 3. Fail-State Mapping & Auto-Recovery
When running verification or audit suites, map these error messages to their root causes and recovery actions:

| Logged Error / Failure Pattern | Root Cause | Self-Correction Recovery Action |
| :--- | :--- | :--- |
| `AssertionError: Error: Raw hex found in layout.css: ...` | Hex code (e.g. `#fff`) leaked into the layout file. | Move hex code to `variables.css`, declare variable, and reference via `var(--)` in the theme file. |
| `AssertionError: Error: Raw rgba found in layout.css: ...` | RGBA or HSL color declaration leaked into layout. | Convert to token in `variables.css`, use `rgba(var(--brand-color-rgb), 0.1)` or migrate visual property to `theme.css`. |
| `AssertionError: Error: Color keywords found in layout.css: ...` | Built-in colors (`white`, `transparent`) used in layout. | Re-declare using variables or remove the visual rule from layout files. |
| `AssertionError: Error: Inline style containing color found in ...` | Inline HTML color declaration (e.g., `<div style="color: #000">`). | Abstract to a CSS class in `theme.css` using theme variables. |

---

## 4. Verification Script
Save and run this script in the workspace to verify complete CSS isolation:
```python
import os
import re

def verify_phase_7():
    state_file = ".pipeline_state.json"
    assert os.path.exists(state_file), "State lock missing."
    
    layout_path = "css/layout.css"
    if not os.path.exists(layout_path):
        print("Warning: css/layout.css not found.")
        return
        
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Hex colors
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}', content)
    
    # 2. rgb, rgba, hsl, hsla
    rgb_colors = re.findall(r'\brgb\s*\([^)]*\)', content, re.IGNORECASE)
    rgba_colors = re.findall(r'\brgba\s*\([^)]*\)', content, re.IGNORECASE)
    hsl_colors = re.findall(r'\bhsl\s*\([^)]*\)', content, re.IGNORECASE)
    hsla_colors = re.findall(r'\bhsla\s*\([^)]*\)', content, re.IGNORECASE)
    
    # 3. Common color keywords
    keywords = ['black', 'white', 'red', 'green', 'blue', 'yellow', 'orange', 
                'purple', 'pink', 'brown', 'gray', 'grey', 'cyan', 'magenta', 
                'silver', 'gold', 'transparent']
    keyword_pattern = r'\b(' + '|'.join(keywords) + r')\b'
    keyword_colors = []
    
    # Strip comments from content first to avoid false positives in comments
    clean_content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    for line in clean_content.splitlines():
        if ':' in line:
            prop, val = line.split(':', 1)
            matches = re.findall(keyword_pattern, val, re.IGNORECASE)
            if matches:
                keyword_colors.extend(matches)
                
    assert len(hex_colors) == 0, f"Error: Raw hex found in layout.css: {hex_colors}"
    assert len(rgb_colors) == 0, f"Error: Raw rgb found in layout.css: {rgb_colors}"
    assert len(rgba_colors) == 0, f"Error: Raw rgba found in layout.css: {rgba_colors}"
    assert len(hsl_colors) == 0, f"Error: Raw hsl found in layout.css: {hsl_colors}"
    assert len(hsla_colors) == 0, f"Error: Raw hsla found in layout.css: {hsla_colors}"
    assert len(keyword_colors) == 0, f"Error: Color keywords found in layout.css: {keyword_colors}"
    
    # 4. Check HTML inline styles containing color attributes e.g., style=".*color.*"
    html_files = [f for f in os.listdir(".") if f.endswith(".html")]
    for hf in html_files:
        with open(hf, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        inline_colors = re.findall(r'style=["\'][^"\']*color[^"\']*["\']', html_content, re.IGNORECASE)
        assert len(inline_colors) == 0, f"Error: Inline style containing color found in {hf}: {inline_colors}"
        
    print("Phase 7 CSS isolation verification passed successfully!")

if __name__ == "__main__":
    verify_phase_7()
```
```
