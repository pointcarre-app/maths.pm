# LaTeX Escaping in PM Framework - Data Flow Guide

## The Problem
When you write `feedback_correct: "$19 \\times 9 \\ times 10$ $km$ $\\times 10$ $km$ = 17100"` in your markdown, the LaTeX isn't rendering correctly and shows broken text.

## Data Flow Overview

The feedback text travels through **5 major stages**, each with potential escaping issues:

```
Markdown YAML → Python Parser → JSON Serialization → HTML Attribute → JavaScript → DOM → KaTeX
```

## Detailed Flow with Escaping Points

### Stage 1: Markdown File (YAML Frontmatter)
**File:** `pms/corsica/a_troiz_geo.md`
```yaml
feedback_correct: "$19 \\times 9 \\times 10$ $km$ $\\times 10$ $km$ = 17100"
```
**Issues here:**
- YAML requires backslash escaping (so `\times` becomes `\\times`)
- But you have `\\ times` (with a space) which is wrong!

### Stage 2: Python Fragment Builder
**File:** `src/core/pm/services/fragment_builder.py`
- Reads YAML using Python yaml parser
- The string now contains literal backslashes
- Python sees: `$19 \times 9 \ times 10$` (note the broken `\ times`)

### Stage 3: JSON Serialization
**File:** `src/templates/pm/fragments/number_.html`
- Python serializes to JSON for HTML attribute
- JSON.dumps() adds ANOTHER layer of escaping
- Backslashes become double backslashes in JSON
- Result: `"$19 \\\\times 9 \\\\ times 10$"`

### Stage 4: HTML Attribute Storage
```html
<pm-number-input data-payload='{"feedback_correct": "$19 \\\\times 9 \\\\ times 10$"}'>
```
- HTML attribute needs escaping for quotes
- Special characters might be HTML-encoded

### Stage 5: JavaScript Parsing
**File:** `src/static/js/pm/components/pm-number-input.js`
```javascript
const payload = JSON.parse(this.getAttribute('data-payload'));
// Now we have the string with backslashes
```

### Stage 6: DOM Insertion
```javascript
container.innerHTML = `<div class="alert">${feedback_text}</div>`;
```
- innerHTML interprets HTML entities
- Text content is inserted as-is

### Stage 7: KaTeX Rendering
```javascript
renderMathInElement(container, {
  delimiters: [
    { left: '$', right: '$', display: false }
  ]
});
```
- KaTeX looks for `$...$` delimiters
- Expects LaTeX commands like `\times` (single backslash)
- But might receive `\\times` or `\\ times`

## The Core Issues

### Issue 1: Space in LaTeX Command
```
WRONG: \\ times  (backslash, space, "times")
RIGHT: \\times   (escaped backslash for "\times")
```

### Issue 2: Multiple Escaping Layers
Each stage adds/removes escaping:
1. YAML: `\\times` → `\times`
2. JSON: `\times` → `\\times`
3. HTML: Preserves as-is
4. JS Parse: `\\times` → `\times`
5. KaTeX: Needs exactly `\times`

### Issue 3: Mixed Content
Your string has both LaTeX (`$...$`) and regular text mixed together:
- `$19 \\times 9$` - LaTeX math
- `km` - Regular text (should it be in math mode?)
- `= 17100` - Regular text

## Safe Solution Strategy

### Option 1: Use Unicode Instead
```yaml
feedback_correct: "$19 × 9 × 10$ km × 10 km = 17100"
```
- Use actual × symbol (Unicode U+00D7)
- No escaping needed
- Works everywhere

### Option 2: Separate Math and Text
```yaml
feedback_correct: "$19 \\times 9 \\times 10 \\text{ km} \\times 10 \\text{ km} = 17100$"
```
- Keep everything in one math block
- Use `\text{}` for non-math content

### Option 3: Use HTML Entities
```yaml
feedback_correct: "$19 &times; 9 &times; 10$ km &times; 10 km = 17100"
```
- Use HTML entities for symbols outside math
- LaTeX only for complex formulas

## Recommended Safe Approach

1. **Fix the source markdown:**
   - Remove spaces after backslashes
   - Use consistent escaping

2. **Test at each stage:**
   - Log the string after Python reads it
   - Log it after JSON serialization
   - Log it in JavaScript before rendering
   - Check what KaTeX receives

3. **Consider simpler syntax:**
   - Use Unicode symbols when possible
   - Keep math and text separate
   - Use a single math block with `\text{}` for units

## Debug Checklist

- [ ] Check YAML syntax (no spaces in `\\times`)
- [ ] Verify Python reads correct string
- [ ] Check JSON in HTML attribute
- [ ] Log JavaScript parsed value
- [ ] Verify KaTeX receives proper LaTeX
- [ ] Test with simple formula first (`$2 \\times 3$`)

## Common Patterns That Work

```yaml
# Simple multiplication
feedback_correct: "$2 \\times 3 = 6$"

# With units (all in math mode)
feedback_correct: "$19 \\times 9 \\times 10 \\, \\text{km} \\times 10 \\, \\text{km} = 17100 \\, \\text{km}^2$"

# Mixed content (math + text)
feedback_correct: "Result: $19 \\times 9 \\times 100 = 17100$ km²"

# Using Unicode (no escaping needed)
feedback_correct: "19 × 9 × 10 km × 10 km = 17100 km²"
```
