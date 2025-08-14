---
title: Interactive Fragments Guide
description: Guide to all interactive fragment types for engaging learning
chapter: Documentation
---

# 🎯 Interactive Fragments Guide

Interactive fragments make pedagogical messages engaging by allowing students to interact with content, answer questions, and receive feedback.

## Fragment Types

### 1. Radio Buttons (radio_) 

Multiple choice questions with immediate feedback.

#### Basic Syntax

```markdown
What is 2 + 2?

- 3{:21}
- 4{:20}
- 5{:21}
{: .i-radio}
```

#### Flag System

| Flag | Meaning | Visual Feedback |
|------|---------|----------------|
| `{:20}` | ✅ Correct answer | Green highlight |
| `{:21}` | ❌ Wrong answer | Red highlight |
| No flag | 💬 Comment/hint | Italic, non-clickable |

#### Advanced Examples

**With Multiple Correct Answers:**
```markdown
Which are even numbers?

- 2{:20}
- 3{:21}
- 4{:20}
- 5{:21}
- Hint: Even numbers are divisible by 2
{: .i-radio}
```

**With Custom Styling:**
```markdown
Select the capital of France:

- London{:21 .text-error}
- Paris{:20 .text-success .font-bold}
- Berlin{:21 .text-error}
{: .i-radio}
```

**With LaTeX Math:**
```markdown
Solve: $x^2 = 4$

- $x = 2${:21}
- $x = -2${:21}
- $x = \pm 2${:20}
- Remember: Consider both roots!
{: .i-radio}
```

### 2. Math Input (maths_)

Text input for mathematical answers with validation.

#### Basic Syntax

```yaml
mathPCAVersion: 1
question: "Calculate: $\int_0^1 x^2 dx$"
answer: "1/3"
tolerance: 0.001
unit: ""
```

#### Features
- Accepts numeric answers
- Tolerance for approximate answers
- Optional units
- LaTeX rendering in questions

#### Advanced Example

```yaml
mathPCAVersion: 1
question: "A car travels 120 km in 2 hours. What is its average speed?"
answer: "60"
tolerance: 0.1
unit: "km/h"
hint: "Speed = Distance / Time"
```

### 3. Interactive Graphs (graph_)

Dynamic, interactive mathematical graphs.

#### Basic Syntax

```yaml
graphPCAVersion: 1
xmin: -10
xmax: 10
ymin: -10
ymax: 10
grid: true
axes: true
functions:
  - expression: "x^2"
    color: "blue"
    label: "f(x) = x²"
```

#### Multiple Functions

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
    label: "Parabola"
  - expression: "2*x + 1"
    color: "red"
    label: "Line"
  - expression: "sin(x)"
    color: "green"
    label: "Sine"
```

#### Interactive Features
- Zoom and pan
- Trace function values
- Show coordinates on hover
- Toggle functions on/off

### 4. Interactive Code (codex_)

Executable code environments for programming education.

#### Basic Syntax

```yaml
codexPCAVersion: 1
script_path: "intro/hello_world.py"
```

#### Features
- Live code execution
- Syntax highlighting
- Error feedback
- Test cases
- Hidden test validation

#### Example with Inline Code

```yaml
codexPCAVersion: 1
language: python
starter_code: |
  # Calculate the area of a circle
  radius = 5
  # Your code here
  area = 
  print(f"Area: {area}")
solution: |
  import math
  radius = 5
  area = math.pi * radius ** 2
  print(f"Area: {area}")
tests:
  - input: ""
    expected: "Area: 78.53981633974483"
```

## JavaScript Integration

Interactive fragments dispatch events for tracking:

```javascript
// Listen for radio button answers
document.addEventListener('i-radio-answered', (e) => {
    console.log('Answer:', e.detail);
    // e.detail contains: {fragmentIndex, flag, isCorrect, timestamp}
});

// Listen for math input
document.addEventListener('i-maths-answered', (e) => {
    console.log('Math answer:', e.detail);
    // e.detail contains: {fragmentIndex, answer, isCorrect, timestamp}
});
```

## Data Storage

Answers are stored in localStorage:

```javascript
// Retrieve all answers
const answers = JSON.parse(localStorage.getItem('pm-answers')) || {};

// Clear answers
localStorage.removeItem('pm-answers');
```

## Best Practices

### For Radio Questions

1. **Always include a correct answer** (flag 20)
2. **Provide hints** as non-flagged items
3. **Use clear, unambiguous wording**
4. **Test all options** for clarity
5. **Consider partial credit** with custom flags

### For Math Input

1. **Set appropriate tolerance** for decimal answers
2. **Specify units** when needed
3. **Provide hints** for complex problems
4. **Accept equivalent forms** (e.g., 0.5 and 1/2)

### For Graphs

1. **Choose appropriate scale** for the content
2. **Use contrasting colors** for multiple functions
3. **Label axes and functions** clearly
4. **Enable grid** for coordinate reading

### For Code Exercises

1. **Provide starter code** when helpful
2. **Include clear instructions** in comments
3. **Test edge cases** in validation
4. **Give helpful error messages**
5. **Build complexity gradually**

## Combining Interactive Elements

Create rich learning experiences by combining fragments:

```markdown
## Example: Quadratic Functions

Consider the function $f(x) = x^2 - 4x + 3$

### Visualization

```yaml
graphPCAVersion: 1
xmin: -1
xmax: 5
ymin: -2
ymax: 4
functions:
  - expression: "x^2 - 4*x + 3"
    color: "blue"
```

### Question 1

Where does the function cross the x-axis?

- At x = 1 and x = 3{:20}
- At x = 0 and x = 4{:21}
- At x = 2 only{:21}
- Hint: Set f(x) = 0 and solve
{: .i-radio}

### Question 2

Find the vertex of the parabola.

```yaml
mathPCAVersion: 1
question: "What is the x-coordinate of the vertex?"
answer: "2"
tolerance: 0.01
```

### Practice Code

```yaml
codexPCAVersion: 1
language: python
starter_code: |
  # Find the roots of f(x) = x^2 - 4x + 3
  import math
  
  # Quadratic formula: x = (-b ± √(b²-4ac)) / 2a
  a = 1
  b = -4
  c = 3
  
  # Calculate discriminant
  discriminant = 
  
  # Calculate roots
  root1 = 
  root2 = 
  
  print(f"Roots: {root1} and {root2}")
```
```

## Validation & Feedback

### Immediate Feedback
- Radio buttons show color changes
- Math inputs validate on submit
- Code runs with test results

### Progress Tracking
- Answers saved automatically
- Score calculation available
- Time tracking included

### Custom Validation
Create custom validators for complex scenarios:

```python
def validate_answer(student_answer, correct_answer, tolerance=0.01):
    """Custom validation logic"""
    return abs(student_answer - correct_answer) <= tolerance
```

## Accessibility

Interactive fragments support:
- Keyboard navigation
- Screen reader announcements
- High contrast modes
- Focus indicators
- Error descriptions

## Performance Considerations

1. **Lazy Loading**: Interactive components load on demand
2. **Debouncing**: Input validation is debounced
3. **Caching**: Answers cached locally
4. **Optimization**: Graphs render efficiently

## Advanced Features

### Conditional Rendering
Show/hide content based on answers:

```javascript
if (userAnswer.isCorrect) {
    showElement('.success-message');
} else {
    showElement('.hint-message');
}
```

### Adaptive Learning
Track performance and adjust difficulty:

```javascript
const performance = calculatePerformance();
if (performance < 0.6) {
    loadEasierQuestions();
} else {
    loadHarderQuestions();
}
```

### Analytics Integration
Send interaction data to analytics:

```javascript
document.addEventListener('i-radio-answered', (e) => {
    analytics.track('QuestionAnswered', {
        type: 'radio',
        correct: e.detail.isCorrect,
        question: e.detail.fragmentIndex
    });
});
```

---

Interactive fragments transform static content into engaging learning experiences. Combine them thoughtfully to create effective pedagogical messages.

## NumberInputPCA (number_)

A versioned numeric input fragment designed for simple numeric answers with bounds, step, units, and tolerance.

Author with a YAML code block:

```yaml
NumberInputPCA: v0.0.1
id: circle_area_q1
type: number
label: "Enter the radius of the circle"
min: 0
max: 100
step: 0.5
unit: "cm"
correct: 7.5
tolerance: 0.1
feedback_correct: "✅ Well done — that's the correct radius."
feedback_incorrect: "❌ Incorrect. Check your calculation."
hint: "The diameter is 15 cm — radius is half."
```

- Use `correct_values` to define multiple acceptable values, each with its tolerance:

```yaml
NumberInputPCA: v0.0.1
id: boiling_point_water
type: number
label: "Quelle est la température d'ébullition de l'eau ?"
min: 90
max: 110
step: 0.1
unit: "°C"
correct_values:
  - { value: 100, tolerance: 0.5 }
  - { value: 99, tolerance: 0.5 }
feedback_correct: "✅ Correct — that matches standard boiling point."
feedback_incorrect: "❌ Incorrect — consider atmospheric pressure."
```

Rendering
- Server parses the YAML into a `number_` fragment.
- The template renders a `pm-number-input` component.
- The component displays:
  - a table of parameters
  - a numeric input with optional unit
  - a live value preview and hint
  - a Check button and feedback

Styling
- The input uses the KaTeX font stack to harmonize with math content.
- Colors are theme-driven via CSS vars (`--pm-ok`, `--pm-err`).

Examples
- See `pms/examples/number_input_example.md` for ready-to-copy snippets.
