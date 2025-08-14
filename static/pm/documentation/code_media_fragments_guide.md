---
title: Code & Media Fragments Guide
description: Guide for code blocks, images, and visual content fragments
chapter: Documentation
---

# 💻 Code & Media Fragments Guide

This guide covers fragments for displaying code, images, and other visual content in pedagogical messages.

## Code Fragments

### 1. Static Code Blocks (code_)

Display syntax-highlighted code without execution.

#### Basic Syntax

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

#### Supported Languages

````markdown
```javascript
const sum = (a, b) => a + b;
```

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

```html
<div class="container">
    <h1>Title</h1>
</div>
```

```css
.container {
    display: flex;
    justify-content: center;
}
```

```sql
SELECT * FROM users 
WHERE age > 18
ORDER BY name;
```
````

#### Features
- Syntax highlighting
- Line numbers (optional)
- Copy button
- Language detection

### 2. Interactive Code (codex_)

Executable code environments with validation.

#### External Script Reference

```yaml
codexPCAVersion: 1
script_path: "intro/variables_intro.py"
```

#### Inline Code Definition

```yaml
codexPCAVersion: 1
language: python
starter_code: |
  # Calculate factorial
  def factorial(n):
      # Your code here
      pass
  
  print(factorial(5))
solution: |
  def factorial(n):
      if n <= 1:
          return 1
      return n * factorial(n-1)
  
  print(factorial(5))
tests:
  - input: "5"
    expected: "120"
  - input: "0"
    expected: "1"
```

#### Advanced Features

```yaml
codexPCAVersion: 1
language: python
title: "List Comprehension Exercise"
instructions: |
  Create a list of squares of even numbers from 0 to 10
starter_code: |
  # Create list of squares of even numbers
  squares = 
  print(squares)
solution: |
  squares = [x**2 for x in range(11) if x % 2 == 0]
  print(squares)
hidden_tests: |
  assert squares == [0, 4, 16, 36, 64, 100]
  assert type(squares) == list
visible_tests:
  - input: ""
    expected: "[0, 4, 16, 36, 64, 100]"
hints:
  - "Use list comprehension syntax: [expression for item in iterable if condition]"
  - "Remember range(11) gives 0 to 10"
```

## Media Fragments

### 1. Images (image_)

Display static images with optional styling.

#### Basic Syntax

```markdown
![Alt text for accessibility](/path/to/image.jpg)
```

#### With Styling

```markdown
![Computer setup](/images/computer-desk-old-169.jpg)
{: .mx-auto .max-w-lg}
```

#### Features
- Automatic lazy loading
- Responsive sizing
- Alt text for accessibility
- Click to zoom (optional)

### 2. SVG Graphics (svg_)

Vector graphics with inline or external sources.

#### External SVG

```markdown
![Corsica Map](/static/pm/corsica/files/corsica_grid_with_labels.svg)
{: .mx-auto}
```

#### Inline SVG Benefits
- CSS styling control
- Interactive elements
- No additional HTTP requests
- Dynamic manipulation

#### Sized SVG

```markdown
![Grid diagram](/static/pm/corsica/files/corsica_grid.svg)
{: .max-w-[340px] .mx-auto}
```



## Tables & Data Visualization

### 1. Data Tables (table_)

Display structured data in tables.

#### Basic Table

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Value A  | Value B  | Value C  |
```

#### Aligned Columns

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
```

#### Complex Table with Math

```markdown
| Function | Derivative | Integral |
|----------|------------|----------|
| $x^n$ | $nx^{n-1}$ | $\frac{x^{n+1}}{n+1}$ |
| $e^x$ | $e^x$ | $e^x$ |
| $\sin(x)$ | $\cos(x)$ | $-\cos(x)$ |
| $\cos(x)$ | $-\sin(x)$ | $\sin(x)$ |
```

### 2. Table of Variations (tabvar_)

Specialized tables for function analysis.

```yaml
class: table-variations
function: "f(x) = x³ - 3x"
x_values: ["-∞", -1, 0, 1, "+∞"]
f_prime: ["+", 0, "-", 0, "+"]
f_variations: ["↗", "max", "↘", "min", "↗"]
f_values: ["-∞", 2, 0, -2, "+∞"]
```

## Mathematical Visualizations

### 1. Function Graphs (graph_)

Interactive mathematical function plots.

```yaml
graphPCAVersion: 1
title: "Trigonometric Functions"
xmin: -6.28
xmax: 6.28
ymin: -2
ymax: 2
grid: true
gridStep: 1.57
functions:
  - expression: "sin(x)"
    color: "blue"
    label: "sin(x)"
    lineWidth: 2
  - expression: "cos(x)"
    color: "red"
    label: "cos(x)"
    lineStyle: "dashed"
points:
  - x: 0
    y: 0
    label: "Origin"
  - x: 3.14
    y: 0
    label: "π"
```

### 2. Geometric Diagrams

Using SVG for precise geometric constructions:

```html
<svg width="400" height="400" class="mx-auto">
  <!-- Triangle -->
  <polygon points="200,50 350,350 50,350" 
           fill="none" 
           stroke="blue" 
           stroke-width="2"/>
  
  <!-- Labels -->
  <text x="200" y="40" text-anchor="middle">A</text>
  <text x="360" y="355" text-anchor="middle">B</text>
  <text x="40" y="355" text-anchor="middle">C</text>
  
  <!-- Angle marking -->
  <path d="M 80,350 Q 50,350 65,320" 
        fill="none" 
        stroke="red" 
        stroke-width="1"/>
</svg>
```

## Best Practices

### For Code Blocks

1. **Choose appropriate language** for syntax highlighting
2. **Include comments** to explain complex parts
3. **Keep examples concise** and focused
4. **Show both input and output** when relevant
5. **Use consistent formatting** and style

### For Images

1. **Provide meaningful alt text** for accessibility
2. **Optimize file sizes** for web delivery
3. **Use appropriate formats** (JPEG for photos, PNG for diagrams, SVG for vectors)
4. **Consider responsive sizing** with CSS classes
5. **Place images near related text**

### For Tables

1. **Keep headers clear and concise**
2. **Align numerical data** appropriately
3. **Use consistent formatting** within columns
4. **Don't overcrowd** - split large tables
5. **Consider mobile viewing** - use responsive tables

### For Mathematical Visualizations

1. **Label axes clearly** with units
2. **Use contrasting colors** for multiple plots
3. **Include grid lines** for reading values
4. **Add interactive features** thoughtfully
5. **Provide context** with titles and descriptions

## Combining Code and Media

Create rich educational content by combining different fragment types:

```markdown
## Physics Simulation

Here's how we model projectile motion:

```python
import numpy as np
import matplotlib.pyplot as plt

# Initial conditions
v0 = 20  # m/s
angle = 45  # degrees
g = 9.81  # m/s²

# Calculate trajectory
t = np.linspace(0, 3, 100)
x = v0 * np.cos(np.radians(angle)) * t
y = v0 * np.sin(np.radians(angle)) * t - 0.5 * g * t**2

plt.plot(x, y)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile Trajectory')
plt.grid(True)
plt.show()
```

### Visualization

```yaml
graphPCAVersion: 1
xmin: 0
xmax: 45
ymin: 0
ymax: 12
functions:
  - expression: "20*sin(pi/4)*x/14.14 - 0.5*9.81*(x/14.14)^2"
    color: "blue"
    label: "Trajectory"
```

### Results Table

| Time (s) | Distance (m) | Height (m) |
|----------|-------------|------------|
| 0.0      | 0.0         | 0.0        |
| 0.5      | 7.1         | 8.3        |
| 1.0      | 14.1        | 11.8       |
| 1.5      | 21.2        | 10.4       |
| 2.0      | 28.3        | 4.1        |
```

## Performance Optimization

### Images
- Use lazy loading for below-fold images
- Provide multiple resolutions with srcset
- Compress images appropriately
- Use CDN for faster delivery

### Code
- Syntax highlighting on demand
- Virtual scrolling for long code
- Code splitting for large examples
- Cache parsed results

### SVG
- Optimize SVG files (remove metadata)
- Use CSS for styling when possible
- Implement viewport culling for complex graphics
- Consider canvas for many elements

## Accessibility Features

1. **Alt text** for all images
2. **ARIA labels** for interactive elements
3. **Keyboard navigation** for code blocks
4. **High contrast** mode support
5. **Screen reader** compatibility

---

Code and media fragments bring content to life through visualization and interactivity. Use them strategically to enhance understanding and engagement.
