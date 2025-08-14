# Safe LaTeX Practices for PM Framework

## Quick Fix for Your Current Issue

Your problem: `feedback_correct: "$19 \\times 9 \\ times 10$ $km$ $\\times 10$ $km$ = 17100"`

### What's Wrong:
- `\\ times` has a SPACE between `\\` and `times` - this breaks LaTeX!
- Multiple separate `$...$` blocks make parsing complex

### Immediate Fix:
```yaml
# Option 1: Fix the spaces
feedback_correct: "$19 \\times 9 \\times 10$ km $\\times 10$ km = 17100"

# Option 2: Use one math block
feedback_correct: "$19 \\times 9 \\times 10 \\, \\text{km} \\times 10 \\, \\text{km} = 17100$"

# Option 3: Use Unicode (SAFEST!)
feedback_correct: "19 × 9 × 10 km × 10 km = 17100"
```

## The Escaping Chain - What Actually Happens

| Stage | Your Broken Version | What It Should Be |
|-------|-------------------|-------------------|
| **1. YAML** | `\\times` and `\\ times` | `\\times` (no space!) |
| **2. Python reads** | `\times` and `\ times` | `\times` |
| **3. JSON dumps** | `\\times` and `\\ times` | `\\times` |
| **4. HTML attribute** | Same as JSON | Same as JSON |
| **5. JS parses** | `\times` and `\ times` | `\times` |
| **6. KaTeX sees** | `\times` and `\ times` ❌ | `\times` ✅ |

## Safe Patterns to Use

### 🟢 ALWAYS SAFE: Unicode Characters
```yaml
feedback_correct: "19 × 9 × 10 = 1710 km²"
```
- No escaping needed
- Works everywhere
- Easy to read

### 🟡 SAFE: Simple LaTeX in One Block
```yaml
feedback_correct: "$19 \\times 9 \\times 10 = 1710$"
```
- Double backslash in YAML
- Single math block
- No mixed content

### 🔴 RISKY: Mixed LaTeX and Text
```yaml
feedback_correct: "$19 \\times 9$ times $10$ km"  # Multiple math blocks
```
- Hard to debug
- Multiple escape points
- Prone to errors

## Testing Strategy

### 1. Start Simple
First test with:
```yaml
feedback_correct: "$2 \\times 3 = 6$"
```

### 2. Add Complexity Gradually
Then try:
```yaml
feedback_correct: "$2 \\times 3 = 6$ km"
```

### 3. Use Browser Console
```javascript
// Check what JavaScript receives
console.log(this.data.feedback_correct);
// Should show: "$2 \times 3 = 6$" (single backslash)
```

### 4. Check KaTeX Input
```javascript
// Before KaTeX rendering
console.log("KaTeX will render:", element.textContent);
```

## Common Mistakes to Avoid

| ❌ Don't Do This | ✅ Do This Instead |
|-----------------|-------------------|
| `\\ times` (space!) | `\\times` (no space) |
| `$km$` (units in math) | `km` or `\\text{km}` |
| `\\\\times` (too many) | `\\times` (exactly 2) |
| Mixing HTML & LaTeX | Pick one format |

## Emergency Fallback

If LaTeX keeps breaking, use HTML entities:
```yaml
feedback_correct: "19 &times; 9 &times; 10 = 1710 km&sup2;"
```

This will always work and never break!
