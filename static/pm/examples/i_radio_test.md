---
title: Test Radio with Feedback
description: Testing the new feedback system
chapter: Examples
---


[TOC]


# Testing i-Radio Feedback Features

This file tests all the feedback functionality of the i-radio system.

## Test 1: Simple Feedback

What is 2 + 2?

- 3{:21 | Not quite. Remember: 2 + 2 = 4}
- 4{:20 | Excellent! You got it right.}
- 5{:21 | Too high. The answer is 4.}
{: .i-radio}

Each answer shows personalized feedback when clicked.

## Test 2: Feedback with Flag 29 Explanation

What is the capital of France?

- London{:21 | No, that's the capital of the UK.}
- Berlin{:21 | No, that's the capital of Germany.}
- Paris{:20 | Correct! Paris is the capital of France.}
- Madrid{:21 | No, that's the capital of Spain.}
- General Info{:29 | **Did you know?** Paris has been the capital of France since 987 AD, with a brief interruption during the French Revolution.}
{: .i-radio}

The Flag 29 content appears after ANY answer is selected.

## Test 3: Multi-line Feedback

Which is the largest planet?

- Earth{:21 | Earth is the 5th largest planet. 
  - Diameter: 12,742 km
  - It's the largest terrestrial planet}
- Jupiter{:20 | Correct! Jupiter is the largest planet.
  - Diameter: 139,820 km  
  - Mass: 318 times Earth's mass
  - Has 79 known moons}
- Saturn{:21 | Saturn is the 2nd largest planet.
  - Diameter: 116,460 km
  - Famous for its rings}
- Explanation{:29 | **Planet Size Comparison:**
  1. Jupiter (largest)
  2. Saturn
  3. Uranus
  4. Neptune
  5. Earth
  6. Venus
  7. Mars
  8. Mercury (smallest)}
{: .i-radio}

## Test 4: LaTeX in Feedback

Solve: $2x + 4 = 10$

- $x = 2${:21 | Close, but check your arithmetic. $2(2) + 4 = 8 \neq 10$}
- $x = 3${:20 | Perfect! $2(3) + 4 = 6 + 4 = 10$ ✓}
- $x = 4${:21 | Too high. $2(4) + 4 = 12 > 10$}
- $x = 6${:21 | Remember to solve for $x$, not $2x$. If $2x = 6$, then $x = 3$}
- Solution Steps{:29 | **How to solve:**
  1. Start with: $2x + 4 = 10$
  2. Subtract 4: $2x = 6$
  3. Divide by 2: $x = 3$}
{: .i-radio}

## Test 5: Mixed Flags

Which are programming languages?

- Python{:20 | Yes! Python is a programming language.}
- HTML{:21 | HTML is a markup language, not a programming language.}
- JavaScript{:20 | Correct! JavaScript is a programming language.}
- CSS{:21 | CSS is a style sheet language, not a programming language.}
- Note: Some items can be debated
- Learn More{:29 | **Programming vs Markup Languages:**
  - **Programming languages** have logic, conditions, and loops
  - **Markup languages** describe structure and presentation
  - **Style languages** define visual appearance}
{: .i-radio}

## Test 6: No Feedback (Basic Flags Only)

True or False: The Earth is flat.

- True{:21}
- False{:20}
{: .i-radio}

Works without feedback - just shows red/green buttons.

## Feedback System Summary

| Flag | Purpose | When Shown | Visual |
|------|---------|------------|--------|
| 20 | Correct + feedback | On click | Green button + success alert |
| 21 | Wrong + feedback | On click | Red button + error alert |
| 29 | General explanation | After any answer | Info card below |
| -1/none | Comment | Always | Italic text |

## Syntax Reference

```markdown
- Answer{:flag | Feedback message}
- Explanation{:29 | Shows after any answer}
- Comment without flag (always visible)
{: .i-radio}
```