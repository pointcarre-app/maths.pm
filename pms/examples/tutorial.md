---
title: PM Tutorial
chapter: Step by Step Guide
description: A comprehensive tutorial for PM features
keywords: tutorial, pm, guide, learning
---

# PM Tutorial

This tutorial will guide you through the advanced features of the PM system.

## Advanced Fragments

### Tables

| Feature | Description | Status |
|---------|------------|--------|
| Markdown | Basic text formatting | ✅ Ready |
| LaTeX | Mathematical expressions | ✅ Ready |
| Code | Syntax highlighting | ✅ Ready |
| Interactivity | User inputs | ✅ Ready |

### Interactive Elements

The PM system supports various interactive elements:

- Radio buttons for multiple choice questions
- Number inputs for mathematical exercises
- Dynamic content updates

## Layout System

PM supports responsive column layouts using special directives:

---
layout: columns
columns: 2
breakpoint: md
---

### Column 1

This content appears in the first column on medium screens and above.

### Column 2

This content appears in the second column on medium screens and above.

---

## Code Examples

### Python Example

```python
class PMRenderer:
    def __init__(self, content):
        self.content = content
    
    def render(self):
        # Process markdown
        html = markdown.render(self.content)
        return html
```

### JavaScript Example

```javascript
const pmRuntime = new PMRuntime({
    mode: 'interactive',
    debug: false
});

pmRuntime.init();
```

## Mathematical Content

PM excels at rendering mathematical content:

### Equations

The quadratic formula:
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

### Matrices

$$
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
$$

## Summary

You've learned about:
- Advanced fragments and formatting
- Interactive elements
- Layout systems
- Code highlighting
- Mathematical rendering

Continue exploring the PM system to discover more features!
