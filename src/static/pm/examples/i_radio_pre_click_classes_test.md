---
title: i-Radio Pre-Click Classes Test
description: Testing the new pre-click CSS class functionality for i-radio fragments
chapter: Examples
---

[TOC]

# i-Radio Pre-Click Classes Test Suite

This document tests the new pre-click class functionality that allows custom styling before any button is clicked.

## How It Works

- **Pre-click classes**: Any CSS class starting with `pre-` is applied initially
- **On first click**: All `pre-` classes are removed from ALL buttons in the group
- **DaisyUI override**: If custom classes contain `btn-` variants, they override the default button styling
- **Backward compatibility**: Existing i-radio fragments work unchanged

---

## 🧪 Test 1: Basic Pre-Click Classes

What is 2 + 2?

- 3{:21 .pre-pulse .pre-bg-warning | Wrong answer}
- 4{:20 .pre-pulse .pre-bg-warning | Correct!}
- 5{:21 .pre-pulse .pre-bg-warning | Try again}
{: .i-radio}

**Expected**: All buttons pulse and have warning background initially. After first click, pulsing and warning background disappear.

---

## 🧪 Test 2: DaisyUI Button Override

Which is the capital of France?

- London{:21 .btn-secondary .btn-lg .pre-animate-bounce | Wrong - that's UK}
- Paris{:20 .btn-secondary .btn-lg .pre-animate-bounce | Correct!}
- Berlin{:21 .btn-secondary .btn-lg .pre-animate-bounce | Wrong - that's Germany}
{: .i-radio}

**Expected**: Large secondary buttons that bounce initially. Default primary styling is completely overridden.

---

## 🧪 Test 3: Mixed Pre-Click and Permanent Classes

Select the programming language:

- HTML{:21 .btn-outline .btn-accent .pre-glow .permanent-border | Markup language}
- Python{:20 .btn-outline .btn-accent .pre-glow .permanent-border | Programming language!}
- CSS{:21 .btn-outline .btn-accent .pre-glow .permanent-border | Styling language}
{: .i-radio}

**Expected**: Accent outline buttons with permanent border and initial glow. Glow disappears on click, border remains.

---

## 🧪 Test 4: Extreme Customization

Choose your favorite color:

- Red{:20 .btn-error .btn-wide .pre-animate-pulse .pre-shadow-lg | Fiery choice!}
- Blue{:20 .btn-info .btn-wide .pre-animate-pulse .pre-shadow-lg | Cool choice!}
- Green{:20 .btn-success .btn-wide .pre-animate-pulse .pre-shadow-lg | Natural choice!}
{: .i-radio}

**Expected**: Wide colored buttons with pulse animation and large shadow initially. All effects disappear after first click.

---

## 🧪 Test 5: No Pre-Click Classes (Backward Compatibility)

Traditional i-radio (should work exactly as before):

- Wrong{:21 | This is wrong}
- Correct{:20 | This is right}
- Also wrong{:21 | This is also wrong}
{: .i-radio}

**Expected**: Standard primary outline buttons, no special pre-click behavior.

---

## 🧪 Test 6: Only Pre-Click Classes (No Button Override)

Math question with utility classes only:

- 2 + 2 = 3{:21 .pre-animate-bounce .text-lg | Incorrect}
- 2 + 2 = 4{:20 .pre-animate-bounce .text-lg | Correct!}
- 2 + 2 = 5{:21 .pre-animate-bounce .text-lg | Incorrect}
{: .i-radio}

**Expected**: Default button styling with bounce animation and large text initially. Bounce disappears, text size remains.

---

## 🧪 Test 7: Complex Pre-Click Animation

Interactive demo with multiple effects:

- Option A{:21 .btn-ghost .pre-animate-spin .pre-bg-gradient-to-r .pre-from-purple-500 .pre-to-pink-500 | Spinning gradient}
- Option B{:20 .btn-ghost .pre-animate-spin .pre-bg-gradient-to-r .pre-from-purple-500 .pre-to-pink-500 | Correct spinning gradient!}
- Option C{:21 .btn-ghost .pre-animate-spin .pre-bg-gradient-to-r .pre-from-purple-500 .pre-to-pink-500 | Another spinning gradient}
{: .i-radio}

**Expected**: Ghost buttons with spinning gradient background initially. All pre-effects disappear on first click.

---

## 🧪 Test 8: LaTeX with Pre-Click Classes

Solve: $x^2 = 4$

- $x = 2${:21 .btn-outline .btn-primary .pre-ring .pre-ring-blue-300 | Partial solution}
- $x = \pm 2${:20 .btn-outline .btn-primary .pre-ring .pre-ring-blue-300 | Complete solution!}
- $x = 4${:21 .btn-outline .btn-primary .pre-ring .pre-ring-blue-300 | Incorrect}
{: .i-radio}

**Expected**: Outlined buttons with blue ring initially. Ring disappears after first click, LaTeX renders correctly.

---

## 🧪 Test 9: Accessibility Test

Screen reader friendly with pre-click effects:

- First option{:21 .btn-lg .pre-animate-pulse | This is the first option}
- Second option{:20 .btn-lg .pre-animate-pulse | This is the correct option}
- Third option{:21 .btn-lg .pre-animate-pulse | This is the third option}
{: .i-radio}

**Expected**: Large buttons with pulse animation initially. Animation stops on first click, accessibility attributes remain intact.

---

## 🧪 Test 10: Performance Test (Many Buttons)

Select any number:

- 1{:21 .btn-sm .pre-bounce}
- 2{:21 .btn-sm .pre-bounce}
- 3{:21 .btn-sm .pre-bounce}
- 4{:21 .btn-sm .pre-bounce}
- 5{:21 .btn-sm .pre-bounce}
- 6{:21 .btn-sm .pre-bounce}
- 7{:20 .btn-sm .pre-bounce | Lucky number!}
- 8{:21 .btn-sm .pre-bounce}
- 9{:21 .btn-sm .pre-bounce}
- 10{:21 .btn-sm .pre-bounce}
{: .i-radio}

**Expected**: All small buttons bounce initially. All bouncing stops on first click, performance remains smooth.

---

## CSS Classes for Testing

Add these to your CSS to see the pre-click effects:

```css
/* Pre-click animation classes */
.pre-pulse {
  animation: pulse 2s infinite;
}

.pre-bounce {
  animation: bounce 1s infinite;
}

.pre-glow {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
}

.pre-animate-spin {
  animation: spin 2s linear infinite;
}

.pre-animate-bounce {
  animation: bounce 1s infinite;
}

.pre-animate-pulse {
  animation: pulse 2s infinite;
}

.pre-bg-warning {
  background-color: hsl(var(--wa));
  color: hsl(var(--wac));
}

.pre-shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.pre-ring {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.pre-ring-blue-300 {
  box-shadow: 0 0 0 3px rgba(147, 197, 253, 0.5);
}

/* Gradient classes */
.pre-bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

.pre-from-purple-500 {
  --tw-gradient-from: #8b5cf6;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(139, 92, 246, 0));
}

.pre-to-pink-500 {
  --tw-gradient-to: #ec4899;
}

.permanent-border {
  border: 2px solid hsl(var(--bc));
}
```

## Implementation Notes

### Template Logic

The template now uses smart class detection:

```jinja2
{% if custom_classes and (custom_classes.find('btn-') != -1 or custom_classes.find('pre-') != -1) %}
  {# Custom styling detected - use minimal base + custom classes #}
  {% set button_classes = "btn min-w-[50px] px-3 text-base font-normal " + custom_classes %}
{% else %}
  {# No custom btn styling - use defaults + any custom utility classes #}
  {% set button_classes = default_classes + (" " + custom_classes if custom_classes else "") %}
{% endif %}
```

### JavaScript Logic

The JavaScript removes pre-click classes on first interaction:

```javascript
_removePreClickClasses(buttons) {
  buttons.forEach((btn) => {
    const classList = Array.from(btn.classList);
    classList.forEach((className) => {
      if (className.startsWith('pre-')) {
        btn.classList.remove(className);
      }
    });
  });
}
```

## Syntax Reference

### Basic Pre-Click Classes
```markdown
- Answer{:20 .pre-pulse | Feedback}
```

### DaisyUI Button Override
```markdown
- Answer{:20 .btn-secondary .btn-lg | Feedback}
```

### Mixed Pre-Click and Permanent
```markdown
- Answer{:20 .btn-outline .pre-glow .permanent-style | Feedback}
```

### Complex Animations
```markdown
- Answer{:20 .btn-ghost .pre-animate-spin .pre-bg-gradient-to-r | Feedback}
```

## Test Results Expected

1. ✅ **Pre-click classes work** - Classes starting with `pre-` are applied initially
2. ✅ **First click removes pre-classes** - All `pre-` classes removed from all buttons in group
3. ✅ **DaisyUI override works** - Custom `btn-` classes override defaults completely
4. ✅ **Backward compatibility** - Existing i-radio fragments unchanged
5. ✅ **Performance** - No noticeable impact with many buttons
6. ✅ **Accessibility** - Screen readers and keyboard navigation unaffected
7. ✅ **LaTeX compatibility** - Math expressions render correctly with custom classes

All features implemented and ready for testing! 🎉
