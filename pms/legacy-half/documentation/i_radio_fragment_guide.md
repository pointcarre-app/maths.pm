---
title: i-Radio Fragment Documentation
description: Complete guide for using interactive radio button fragments
chapter: Documentation

# Page-specific metatags
title: "I Radio Fragment Guide - Interactive Radio Button Components"
description: "Guide for creating interactive radio button questions and quizzes in PM pages"
keywords: "i_radio, radio buttons, interactive, quiz, questions, PM components"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "I Radio Fragment Guide"
og:description: "Guide for creating interactive radio button questions and quizzes in PM pages"
og:type: "article"
og:url: "https://maths.pm/pm/documentation/i_radio_fragment_guide.md"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "I Radio Fragment Guide"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "Components, Interactive, Documentation"
revised: "2025-01-15"
pagename: "I Radio Fragment Guide"

---

# i-Radio Fragment System Documentation

## Overview

The i-radio fragment system allows you to create interactive multiple-choice questions in your pedagogical messages. It uses a flag-based system to distinguish between correct answers, wrong answers, and non-interactive comments.

## Flag Convention

The system uses numeric flags to indicate the nature of each option:

| Flag | Meaning | Visual Feedback |
|------|---------|-----------------|
| **{:20}** | ✅ Correct answer | Green text, success badge |
| **{:21}** | ❌ Wrong answer | Red text, error badge |
| **{:-1}** or no flag | 💬 Comment/explanation | Italic, grayed out, non-clickable |

## Markdown Syntax

### Basic Structure

```markdown
- Option Text{:flag}
- Another Option{:flag}
- Comment without flag
{: .i-radio}
```

### With CSS Classes

You can add CSS classes after the flag for additional styling:

```markdown
- Correct Answer{:20 .text-success .font-bold}
- Wrong Answer{:21 .text-error}
{: .i-radio}
```

## Examples

### Simple Question

```markdown
What is the capital of France?

- London{:21}
- Paris{:20}
- Berlin{:21}
- Madrid{:21}
{: .i-radio}
```

### With Explanatory Comment

```markdown
Which Python keyword is used to define a function?

- func{:21}
- def{:20}
- function{:21}
- Remember: Python uses 'def' keyword
{: .i-radio}
```

### Multiple Correct Answers

```markdown
Which of these are prime numbers?

- 2{:20}
- 3{:20}
- 4{:21}
- 5{:20}
- 6{:21}
{: .i-radio}
```

### With LaTeX Math

```markdown
Solve: $\int_0^1 x^2 dx = ?$

- $\frac{1}{2}${:21}
- $\frac{1}{3}${:20}
- $\frac{1}{4}${:21}
- $1${:21}
{: .i-radio}
```

## How It Works

### 1. Markdown Processing
When the markdown is processed:
- Lists with `class="i-radio"` are detected
- Each `<li>` item is parsed for the flag pattern `{:number}`
- The fragment builder creates a `radio_` fragment type

### 2. Data Structure
The fragment stores radio data as:
```python
{
    "radios": [
        {
            "pos": 0,
            "name": "option-slug",
            "flag": 20,  # or 21, -1, etc.
            "html": "Option Text",
            "classes": "additional-css-classes"
        },
        ...
    ],
    "comment": "Optional comment text"
}
```

### 3. Template Rendering
The template:
- Renders interactive radio buttons for items with flag != -1
- Shows comments as non-interactive italic text
- Applies hover effects and visual feedback

### 4. JavaScript Interaction
The i-radio-handler.js:
- Listens for radio button changes
- Provides immediate visual feedback (green for correct, red for wrong)
- Stores answers in localStorage
- Calculates and displays scores
- Dispatches custom events for integration with other components

## API Functions

### Python Utilities (`i_radio_utils.py`)

```python
from src.core.pm.services.i_radio_utils import *

# Check answer types
is_correct_answer(radio_item)  # Returns True if flag == 20
is_wrong_answer(radio_item)    # Returns True if flag == 21
is_interactive(radio_item)     # Returns True if flag != -1

# Get answers from fragment
get_correct_answers(fragment)  # Returns list of correct options

# Validation
validate_radio_fragment(fragment)  # Returns (is_valid, error_message)

# Create radio items programmatically
create_radio_item(html="Answer", flag=20, pos=0, classes="")
```

### JavaScript API

```javascript
// Access the handler
const handler = iRadioHandler;

// Get all stored answers for current page
const answers = handler.getStoredAnswers();

// Calculate score
const score = handler.calculateScore();
// Returns: { total: 5, answered: 3, correct: 2, percentage: 40 }

// Clear all answers
handler.clearAnswers();

// Listen for answer events
document.addEventListener('i-radio-answered', (event) => {
    console.log('Answer selected:', event.detail);
    // event.detail contains: { fragmentIndex, flag, isCorrect, timestamp }
});
```

## Best Practices

### 1. Always Mark Correct Answers
Every radio fragment should have at least one correct answer (flag 20).

### 2. Use Comments Wisely
Add explanatory comments without flags to guide learners:
```markdown
- Hint: Think about the formula for area
```
(Include in a list with `{: .i-radio}` attribute)

### 3. Consistent Flag Usage
- Use 20 for correct answers
- Use 21 for wrong answers
- Use -1 or no flag for comments

### 4. Provide Clear Questions
Always include a clear question before the radio options, either as a heading or paragraph.

### 5. Test Interactivity
Verify that:
- Correct answers show green feedback
- Wrong answers show red feedback
- Comments are not clickable
- Answers are stored and can be retrieved

## Integration with Other Systems

The i-radio fragment integrates with:
- **Fragment validation system**: Ensures proper structure
- **PM builder**: Processes markdown into fragments
- **Storage system**: Saves user progress
- **Analytics**: Tracks learning progress (via custom events)

## Troubleshooting

### Radio buttons not appearing
- Check that the list has `{: .i-radio}` attribute at the end
- Verify flag syntax is correct `{:number}`

### No visual feedback
- Ensure i-radio-handler.js is loaded
- Check browser console for errors
- Verify flag values are 20 or 21

### Comments appearing as buttons
- Use no flag or {:−1} for comments
- Don't use {:20} or {:21} for non-interactive text
