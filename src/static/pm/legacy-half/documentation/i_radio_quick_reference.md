---
title: i-Radio Quick Reference
description: Quick reference guide for i-radio fragments
chapter: Documentation

# Page-specific metatags
title: "I Radio Quick Reference - Interactive Radio Button Components"
description: "Guide for creating interactive radio button questions and quizzes in PM pages"
keywords: "i_radio, radio buttons, interactive, quiz, questions, PM components"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "I Radio Quick Reference"
og:description: "Guide for creating interactive radio button questions and quizzes in PM pages"
og:type: "article"
og:url: "https://maths.pm/pm/documentation/i_radio_quick_reference.md"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "I Radio Quick Reference"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "Components, Interactive, Documentation"
revised: "2025-01-15"
pagename: "I Radio Quick Reference"

---

# i-Radio Quick Reference Guide

## 🚀 Quick Start

```markdown
What is 2 + 2?

- 3{:21 | Wrong, try again}
- 4{:20 | Correct!}
- 5{:21 | Too high}
- Hint: Count on your fingers
- Solution{:29 | **Answer:** 2 + 2 = 4}
{: .i-radio}
```

## 🎯 Flag Reference

| Flag | What It Does | When to Use |
|------|-------------|-------------|
| `{:20}` | ✅ Correct (green) | Right answers |
| `{:21}` | ❌ Wrong (red) | Incorrect options |
| `{:29}` | 📚 Explanation | Shows after any click |
| None | 💬 Comment | Always visible notes |

## 📝 Syntax Patterns

### Basic
```markdown
- Answer{:flag}
```

### With Feedback
```markdown
- Answer{:flag | Your feedback here}
```

### Multi-line Feedback
```markdown
- Answer{:flag | Line 1
  Line 2
  Line 3}
```

### Always Visible
```markdown
- This text always shows
```

### Explanation Box
```markdown
- Learn More{:29 | Detailed explanation}
```

### With Pre-Click Classes (NEW!)
```markdown
- Answer{:20 .btn-secondary .pre-pulse | Feedback}
```

### DaisyUI Override
```markdown
- Answer{:20 .btn-error .btn-lg | Custom styled button}
```

## 🎨 Visual States

```
Initial:      [Button] [Button] [Button]  (soft outline)
After click:  [GREEN] [Button] [Button]   (if correct)
              [Button] [RED] [Button]     (if wrong)
              + Feedback message below
              + Explanation box (if flag 29)
```

## 💡 Common Examples

### Yes/No Question
```markdown
Is Python interpreted?

- Yes{:20 | Correct! Python is interpreted.}
- No{:21 | Actually, Python is interpreted.}
{: .i-radio}
```

### Multiple Choice
```markdown
Capital of France?

- London{:21}
- Paris{:20}
- Berlin{:21}
- Rome{:21}
{: .i-radio}
```

### With Explanation
```markdown
What is 10 ÷ 2?

- 4{:21 | No, check your math}
- 5{:20 | Perfect!}
- 6{:21 | Too high}
- How to solve{:29 | 10 ÷ 2 = 5 because 5 × 2 = 10}
{: .i-radio}
```

### Multiple Correct
```markdown
Which are even?

- 2{:20}
- 3{:21}
- 4{:20}
- 5{:21}
{: .i-radio}
```

### With LaTeX
```markdown
Solve $x + 3 = 7$

- $x = 3${:21}
- $x = 4${:20}
- $x = 5${:21}
{: .i-radio}
```

### Pre-Click Animation
```markdown
Pick your favorite color:

- Red{:20 .btn-error .pre-pulse | Fiery choice!}
- Blue{:20 .btn-info .pre-pulse | Cool choice!}
- Green{:20 .btn-success .pre-pulse | Natural choice!}
{: .i-radio}
```

## ✅ Checklist

Before using i-radio:
- [ ] At least one option with flag 20 (correct)
- [ ] All wrong answers have flag 21
- [ ] Feedback messages are helpful
- [ ] Flag 29 content adds value
- [ ] Button text is concise
- [ ] Tested all click paths
- [ ] Pre-click classes enhance UX (optional)
- [ ] Custom DaisyUI styling works as expected (if used)

## 🔧 Troubleshooting

**No buttons?** → Check flags (need 20 or 21)
**No feedback?** → Check pipe syntax `{:flag | message}`
**Flag 29 not showing?** → Must have clickable buttons
**LaTeX broken?** → Use $ for inline math
**Long text wrapping?** → Normal, buttons auto-wrap

## 📚 Test Files

1. **Basic**: `pms/examples/i_radio_example.md`
2. **Feedback**: `pms/examples/i_radio_test.md`
3. **Advanced**: `pms/examples/i_radio_advanced.md`
4. **Edge Cases**: `pms/examples/i_radio_complete_test.md`
5. **Pre-Click Classes**: `pms/examples/i_radio_pre_click_classes_test.md`

## 🎯 Pro Tips

1. **Keep buttons short** - Details go in feedback
2. **Explain wrong answers** - Help users learn
3. **Use flag 29** - For teaching moments
4. **Test everything** - Click all options
5. **Be encouraging** - Positive feedback helps
6. **Use pre-click effects** - Draw attention to interactive elements
7. **Override DaisyUI carefully** - Test custom button styling thoroughly

## 📖 Full Documentation

See `pms/documentation/i_radio_documentation.md` for complete details.
