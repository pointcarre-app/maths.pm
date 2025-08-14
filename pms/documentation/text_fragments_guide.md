---
title: Text Fragments Guide
description: Complete guide to text-based fragment types
chapter: Documentation
---

# 📝 Text Fragments Guide

Text fragments are the foundation of pedagogical messages. They handle all text-based content from headings to paragraphs to quotes.

## Fragment Types

### 1. Headings (h1_, h2_, h3_, h4_)

Headings create document structure and are automatically numbered in some contexts.

```markdown
# Main Title (h1_)
## Section Title (h2_)
### Subsection (h3_)
#### Sub-subsection (h4_)
```

**Features:**
- Auto-generated IDs for navigation
- Automatic numbering (Roman for h2, letters for h3, numbers for h4)
- Used for TOC generation

### 2. Paragraphs (p_)

The most common fragment type. Any regular text becomes a paragraph.

```markdown
This is a simple paragraph.

This paragraph has **bold**, *italic*, `code`, and $LaTeX$ content.
```

**Styled Paragraphs:**

```markdown
This has a colored background.
{: .bg-primary}

This is a lead paragraph - larger and emphasized.
{: .lead}

Multiple classes can be combined.
{: .bg-white .text-center .font-bold}
```

### 3. Blockquotes (q_)

Used for quotes, highlights, or important notes.

```markdown
> This is a blockquote.
> It can span multiple lines.
> 
> And have multiple paragraphs.
```

**Nested Content:**
```markdown
> **Important:** Blockquotes can contain:
> - Lists
> - *Formatting*
> - Even `code`
```

### 4. Lists (ul_, ol_, lbl_)

#### Unordered Lists
```markdown
- Item 1
- Item 2
  - Nested 2.1
  - Nested 2.2
- Item 3
```

#### Ordered Lists
```markdown
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
```

#### Labeled Lists
```markdown
- Special item 1
- Special item 2
{: .lbl}
```

### 5. Horizontal Rule (hr_)

Creates a visual separator between sections.

```markdown
Content above

---

Content below
```

## Styling with Attributes

The PM system supports markdown attribute lists for adding CSS classes:

```markdown
This paragraph has custom styling.
{: .class-name}

Multiple classes can be applied.
{: .class1 .class2 .class3}
```

### Common Style Classes

| Class | Effect |
|-------|--------|
| `.lead` | Larger, emphasized text |
| `.bg-primary` | Primary background color |
| `.bg-secondary` | Secondary background color |
| `.bg-white` | White background |
| `.text-center` | Center-aligned text |
| `.font-bold` | Bold text |
| `.nm` | No margin |
| `.mx-auto` | Center horizontally |

## Text Fragment Data Structure

Each text fragment has:
- `f_type`: The fragment type enum value
- `html`: The rendered HTML content
- `data`: Additional metadata (empty for most text fragments)
- `class_list`: CSS classes to apply

## Best Practices

### 1. Use Semantic Headings
- Start with h1 for the main title
- Use h2 for major sections
- Don't skip heading levels

### 2. Keep Paragraphs Focused
- One idea per paragraph
- Use blockquotes for emphasis
- Apply styling sparingly

### 3. Choose Appropriate Lists
- Unordered for non-sequential items
- Ordered for steps or rankings
- Labeled for special formatting

### 4. Use Dividers Sparingly
- Only between major sections
- Not between every fragment

## Examples in Context

### Academic Content
```markdown
# Introduction to Calculus

Calculus is the mathematical study of continuous change.
{: .lead}

## Key Concepts

### Derivatives

The derivative represents the rate of change of a function.

> **Definition:** The derivative of f(x) at point a is:
> $$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

### Applications

Derivatives are used in:
- Physics (velocity, acceleration)
- Economics (marginal cost)
- Engineering (optimization)
```

### Tutorial Content
```markdown
## Python Variables

Variables store data for later use.
{: .bg-primary}

### Creating Variables

Follow these steps:

1. Choose a descriptive name
2. Use the assignment operator (=)
3. Assign a value

```python
age = 25
name = "Alice"
```

> **Tip:** Variable names should be lowercase with underscores for spaces.

---

### Practice Exercise

Try creating your own variables below.
```

## Fragment Processing

The fragment builder:
1. Parses markdown to HTML
2. Identifies tag types
3. Extracts content and attributes
4. Creates fragment objects
5. Validates structure
6. Applies styling

## Advanced Features

### Dynamic IDs
Headings automatically get IDs for linking:
```markdown
## My Section
<!-- Creates id="my-section" -->
```

### TOC Generation
The `[TOC]` marker creates a table of contents from all headings.

### Inline Math
LaTeX math works in all text fragments:
```markdown
The equation $E = mc^2$ shows energy-mass equivalence.
```

## Validation Rules

Text fragments are validated for:
- Proper HTML structure
- Valid attribute syntax
- Appropriate nesting
- Character encoding

## Tips for Educators

1. **Structure First**: Plan your heading hierarchy
2. **Visual Hierarchy**: Use styling to guide attention
3. **Consistency**: Apply styles consistently
4. **Accessibility**: Ensure good contrast and readability
5. **Progressive Disclosure**: Start simple, add complexity

---

This guide covers all text-based fragment types. For interactive fragments, see the Interactive Fragments Guide.
