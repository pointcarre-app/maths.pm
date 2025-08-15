---
title: Interactive Radio Example
description: Basic i-radio fragment with correct/wrong flag system
chapter: Examples

# Page-specific metatags
title: "I Radio Example - Interactive Radio Button Components"
description: "Guide for creating interactive radio button questions and quizzes in PM pages"
keywords: "i_radio, radio buttons, interactive, quiz, questions, PM components"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "I Radio Example"
og:description: "Guide for creating interactive radio button questions and quizzes in PM pages"
og:type: "article"
og:url: "https://maths.pm/pm/examples/i_radio_example.md"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "I Radio Example"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "Components, Interactive, Documentation"
revised: "2025-01-15"
pagename: "I Radio Example"

---


[TOC]

# Basic i-Radio Button Questions

This demonstrates the basic i-radio fragment system with flag-based answer validation.

## Visual Behavior

- **Initial state**: All buttons appear as soft primary outline buttons
- **On click**: Button turns green (correct) or red (wrong)
- **Other buttons**: Reset to soft outline state when a new answer is selected

## Example 1: Simple Binary Choice

Which programming language are we learning?

- JavaScript{:21}
- Python{:20}
- Java{:21}
- C++{:21}
{: .i-radio}

## Example 2: With Always-Visible Comment

What is 2 + 2?

- 3{:21}
- 4{:20}
- 5{:21}
- Note: This is a basic arithmetic question
{: .i-radio}

The last item without a flag is always visible as a comment.

## Example 3: Multiple Correct Answers

Which of these are even numbers?

- 2{:20}
- 3{:21}
- 4{:20}
- 5{:21}
- 6{:20}
- 7{:21}
- 8{:20}
{: .i-radio}

Multiple answers can be marked as correct (flag 20).

## Example 4: With LaTeX Math

Solve: $x^2 - 4 = 0$

- $x = 2${:21}
- $x = \pm 2${:20}
- $x = 4${:21}
- $x = -2${:21}
{: .i-radio}

LaTeX expressions work seamlessly in radio buttons.

## Example 5: French Question

Quelle est la capitale de la France?

- Lyon{:21}
- Marseille{:21}
- Paris{:20}
- Nice{:21}
- Toulouse{:21}
{: .i-radio}

## Flag System Reference

| Flag | Meaning | Visual Result |
|------|---------|---------------|
| 20 | Correct answer | Green button (btn-success) |
| 21 | Wrong answer | Red button (btn-error) |
| -1 or none | Comment | Always visible text below buttons |

## Markdown Syntax

```markdown
- Answer text{:flag}
{: .i-radio}
```

Where `flag` is 20 (correct) or 21 (wrong).