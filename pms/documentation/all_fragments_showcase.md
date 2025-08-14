---
title: Complete Fragment Showcase
description: Comprehensive demonstration of all fragment types in the PM system
chapter: Documentation
---

[TOC]

# 📚 Complete Fragment Types Showcase

This document demonstrates all available fragment types in the Pedagogical Message (PM) system. Each fragment type is shown with its markdown syntax and rendered output.
{: .lead}

---

## 📝 Text Fragments

### Headings (h1_, h2_, h3_, h4_)

# This is an H1 Heading
## This is an H2 Heading  
### This is an H3 Heading
#### This is an H4 Heading

### Paragraphs (p_)

This is a regular paragraph. It can contain **bold text**, *italic text*, and even `inline code`. Paragraphs are the most basic fragment type and are created automatically from regular text.

Here's another paragraph with a link to [example.com](https://example.com) and some mathematical notation like $x^2 + y^2 = z^2$.

### Blockquotes (q_)

> This is a blockquote fragment. It's perfect for highlighting important information or quotes.
> 
> Blockquotes can span multiple lines and contain other markdown elements.

### Lead Paragraphs

This paragraph has a special lead class that makes it stand out as an introduction or summary.
{: .lead}

### Styled Paragraphs

This paragraph has a secondary background color.
{: .bg-secondary}

This paragraph has a white background and no margin.
{: .bg-white .nm}

---

## 📋 List Fragments

### Unordered Lists (ul_)

- First item
- Second item
  - Nested item 2.1
  - Nested item 2.2
- Third item

### Ordered Lists (ol_)

1. First step
2. Second step
   1. Sub-step 2.1
   2. Sub-step 2.2
3. Third step

### Line-by-line (lbl_) — progressive reveal

A special list that reveals items one-by-one with buttons. You can pre-reveal the first N items using an attribute.

Example A (default: start hidden):

- Première ligne
- Deuxième ligne
- Troisième ligne
{: .lbl}

Example B (reveal first 1):

- Ligne A
- Ligne B
- Ligne C
{: .lbl data-reveal-first="1"}

Example C (reveal first 2 using `reveal-first`):

- Étape 1
- Étape 2
- Étape 3
{: .lbl reveal-first="2"}

---

## 🎯 Interactive Fragments

### Radio Buttons (radio_)

Which programming language are we learning?

- JavaScript{:21}
- Python{:20}
- Java{:21}
- C++{:21}
- Hint: It's named after a snake!
{: .i-radio}

### Multiple Correct Answers

Which of these are prime numbers?

- 2{:20}
- 3{:20}
- 4{:21}
- 5{:20}
- 6{:21}
- Remember: Prime numbers are only divisible by 1 and themselves
{: .i-radio}

### Math Input (maths_)

```yaml
mathPCAVersion: 1
question: "Solve for x: $2x + 5 = 13$"
answer: "4"
tolerance: 0.01
unit: ""
```

### Interactive Graph (graph_)

```yaml
graphPCAVersion: 1
xmin: -5
xmax: 5
ymin: -5
ymax: 5
grid: true
functions:
  - expression: "x^2"
    color: "blue"
  - expression: "2*x + 1"
    color: "red"
```

---

## 📊 Data & Visual Fragments

### Tables (table_)

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Value A  | Value B  | Value C  |
| Item X   | Item Y   | Item Z  |

### Complex Table

| Student | Math | Physics | Chemistry | Average |
|---------|------|---------|-----------|---------|
| Alice   | 95   | 88      | 92        | 91.7    |
| Bob     | 87   | 91      | 85        | 87.7    |
| Charlie | 92   | 95      | 90        | 92.3    |

---

## 🖼️ Media Fragments

### Images (image_)

![Computer desk with old monitor](/images/computer-desk-old-169.jpg)

### SVG Graphics (svg_)

![Corsica Grid Map](/static/pm/corsica/files/corsica_grid_with_labels.svg)
{: .mx-auto}

### Inline SVG with Custom Classes

![Corsica No Grid](/static/pm/corsica/files/corsica_no_grid.svg)
{: .max-w-[340px] .mx-auto}

---

## 💻 Code Fragments

### Code Blocks (code_)

```python
# Python code example
def calculate_area(width, height):
    """Calculate the area of a rectangle."""
    return width * height

# Using the function
area = calculate_area(10, 5)
print(f"The area is: {area}")
```

```javascript
// JavaScript example
const greet = (name) => {
    return `Hello, ${name}!`;
};

console.log(greet("World"));
```

### Interactive Code (codex_)

```yaml
codexPCAVersion: 1
script_path: "pyly/premiers-pas-affichages-strings.py"
```

```yaml
codexPCAVersion: 1
script_path: "intro/variables_intro.py"
```

---

## 📈 Mathematical Fragments

### Table of Variations (tabvar_)

```yaml
class: table-variations
x_values: ["-∞", -2, 0, 2, "+∞"]
f_variations: ["↗", "max", "↘", "min", "↗"]
f_values: ["-∞", 4, 0, -4, "+∞"]
function: "f(x) = x³ - 3x"
```

---

## 🎨 Special Fragments

### Horizontal Rule / Divider (hr_)

Content before the divider.

---

Content after the divider.

### Layout directive (columns)

--- {: .pm-cols-sm-2 gap-4 }

This paragraph will appear next to the SVG on small screens and up.

![Corsica Grid Map](/static/pm/corsica/files/corsica_grid_with_grid.svg)
{: .max-w-[340px] .mx-auto}

### Table of Contents (toc_)

The `[TOC]` marker at the beginning of this document generates an automatic table of contents based on all headings.

---

## 🔧 Fragment Attributes

### Custom CSS Classes

You can add custom CSS classes to most fragments using the attribute syntax:

This paragraph has multiple custom classes applied.
{: .text-center .font-bold .text-primary}

### Nested Content

> This blockquote contains **bold text**, *italic text*, and even math: $e^{i\pi} + 1 = 0$
> 
> It also has a list inside:
> - Item 1
> - Item 2

---

## 📋 Combining Fragments

Fragments can work together to create rich educational content:

### Example Problem

Calculate the area of a rectangle with width 8 and height 5.

```python
width = 8
height = 5
area = width * height
print(f"Area = {area}")
```

What is the result?

- 13{:21}
- 40{:20}
- 45{:21}
- 35{:21}
{: .i-radio}

> **Solution:** The area of a rectangle is width × height = 8 × 5 = 40

---

## 📝 Notes

- All fragments are automatically validated when the PM is built
- Fragment types are defined in the `FType` enum
- Each fragment can have associated data and CSS classes
- Interactive fragments track user responses and can provide feedback
- The system supports both HTML and markdown input formats

---

**This showcase demonstrates the flexibility and power of the PM fragment system for creating rich, interactive educational content.**
