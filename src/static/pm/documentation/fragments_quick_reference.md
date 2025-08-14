---
title: Fragments Quick Reference
description: Quick reference for all PM fragment types
chapter: Documentation
---

# ⚡ Fragments Quick Reference

Quick lookup for all fragment types in the PM system.

## 📝 Text Fragments

| Fragment | Markdown | Description |
|----------|----------|-------------|
| **h1_** | `# Title` | Main heading |
| **h2_** | `## Section` | Section heading (Roman numerals) |
| **h3_** | `### Subsection` | Subsection (letters) |
| **h4_** | `#### Sub-subsection` | Sub-subsection (numbers) |
| **p_** | Plain text | Regular paragraph |
| **q_** | `> Quote` | Blockquote |
| **hr_** | `---` | Horizontal divider |
| **toc_** | `[TOC]` | Table of contents |

## 📋 List Fragments

| Fragment | Markdown | Description |
|----------|----------|-------------|
| **ul_** | `- Item` | Unordered list |
| **ol_** | `1. Item` | Ordered list |
| **lbl_** | `- Item`<br>`{: .lbl}` | Labeled list |

## 🎯 Interactive Fragments

| Fragment | Markdown | Description |
|----------|----------|-------------|
| **radio_** | `- Option{:20}`<br>`- Wrong{:21}`<br>`{: .i-radio}` | Multiple choice |
| **maths_** | `\`\`\`yaml`<br>`mathPCAVersion: 1`<br>`\`\`\`` | Math input field |
| **graph_** | `\`\`\`yaml`<br>`graphPCAVersion: 1`<br>`\`\`\`` | Interactive graph |
| **codex_** | `\`\`\`yaml`<br>`codexPCAVersion: 1`<br>`\`\`\`` | Executable code |
| **number_** | `\`\`\`yaml`<br>`NumberInputPCA: v0.0.1`<br>`type: number`<br>`label: "..."`<br>`min: 0`<br>`max: 100`<br>`step: 0.5`<br>`unit: "cm"`<br>`correct: 7.5`<br>`tolerance: 0.1`<br>`\`\`\`` | Numeric input with tolerance |

## 🖼️ Media Fragments

| Fragment | Markdown | Description |
|----------|----------|-------------|
| **image_** | `![Alt](/path.jpg)` | Static image |
| **svg_** | `![Alt](/path.svg)` | SVG graphic |

## 📊 Data Fragments

| Fragment | Markdown | Description |
|----------|----------|-------------|
| **table_** | `\| A \| B \|`<br>`\|---\|---\|` | Data table |
| **tabvar_** | `\`\`\`yaml`<br>`class: table-variations`<br>`\`\`\`` | Variation table |
| **code_** | `\`\`\`language`<br>`code`<br>`\`\`\`` | Code block |

## 🎨 Styling with Attributes

Add CSS classes to most fragments:

```markdown
Text with custom styling.
{: .class1 .class2}
```

### Common Classes

| Class | Effect |
|-------|--------|
| `.lead` | Emphasized intro text |
| `.bg-primary` | Primary background |
| `.bg-secondary` | Secondary background |
| `.bg-white` | White background |
| `.text-center` | Center text |
| `.font-bold` | Bold text |
| `.mx-auto` | Center horizontally |
| `.max-w-[size]` | Maximum width |
| `.nm` | No margin |

## 🔧 Fragment Data Structure

```python
Fragment = {
    "f_type": FType,        # Enum value
    "html": str,            # Rendered content
    "data": dict,           # Type-specific data
    "class_list": list,     # CSS classes
    "classes": str,         # Computed from class_list
}
```

## 🚀 Quick Examples

### Radio Question
```markdown
What is 2+2?

- 3{:21}
- 4{:20}
- 5{:21}
{: .i-radio}
```

### Code Block
````markdown
```python
def hello():
    print("Hello!")
```
````

### Math Input
```yaml
mathPCAVersion: 1
question: "Solve: x + 5 = 12"
answer: "7"
```

### Interactive Graph
```yaml
graphPCAVersion: 1
xmin: -5
xmax: 5
functions:
  - expression: "x^2"
    color: "blue"
```

### Styled Paragraph
```markdown
Important information here.
{: .lead .bg-primary}
```

### Table
```markdown
| Name | Score |
|------|-------|
| Alice | 95 |
| Bob | 87 |
```

### Image with Styling
```markdown
![Description](/image.jpg)
{: .mx-auto .max-w-lg}
```

## 🎮 Interactive Fragment Flags

### Radio Button Flags
- `{:20}` - ✅ Correct answer
- `{:21}` - ❌ Wrong answer
- `{:-1}` or none - 💬 Comment

## 📁 File Structure

```
pms/
├── documentation/      # Guides and references
├── examples/          # Example PMs
├── corsica/          # Corsica project
│   └── files/        # Assets (SVG, images)
└── pyly/             # Python lessons
    └── files/        # Code examples
```

## 🔗 Related Documentation

- [All Fragments Showcase](all_fragments_showcase.md) - Complete examples
- [Text Fragments Guide](text_fragments_guide.md) - Text formatting
- [Interactive Fragments Guide](interactive_fragments_guide.md) - Interactions
- [Code & Media Guide](code_media_fragments_guide.md) - Visual content
- [i-Radio Guide](i_radio_fragment_guide.md) - Radio buttons

## 💡 Tips

1. **Start simple** - Use basic text fragments first
2. **Add interactivity** - Enhance with radio/math questions
3. **Include visuals** - Break up text with images/code
4. **Test rendering** - Preview your markdown
5. **Validate structure** - Check fragment validation
6. **Use attributes** - Style with CSS classes
7. **Combine fragments** - Create rich content

---

*This quick reference covers all fragment types. See individual guides for detailed documentation.*
