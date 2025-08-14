---
title: i-Radio Fragment Complete Documentation
description: Complete technical documentation for the i-radio fragment system
chapter: Documentation
---

# i-Radio Fragment System Documentation

## Overview

The i-radio fragment system provides interactive multiple-choice questions with immediate visual feedback, personalized messages, and explanatory content. It's designed for educational content where learners benefit from immediate feedback.

## Quick Start

### Basic Usage

```markdown
Which is correct?

- Wrong answer{:21}
- Correct answer{:20}
{: .i-radio}
```

### With Feedback

```markdown
What is 2 + 2?

- 3{:21 | No, try again.}
- 4{:20 | Perfect!}
- Explanation{:29 | Math tip: 2 + 2 = 4}
{: .i-radio}
```

## Flag System

| Flag | Purpose | Visual Result | When Shown |
|------|---------|---------------|------------|
| **20** | Correct answer | Green button (`btn-success`) | Always interactive |
| **21** | Wrong answer | Red button (`btn-error`) | Always interactive |
| **29** | Explanation | Info card below buttons | After ANY answer clicked |
| **-1** | Comment | Italic text below | Always visible |
| *none* | Comment | Same as -1 | Always visible |

## Visual Behavior

### Initial State
- All buttons appear as soft primary outline (`btn btn-primary btn-sm btn-outline`)
- Clean, professional appearance
- No feedback visible
- Flag 29 content hidden

### After Click
- Clicked button transforms:
  - Flag 20 → Green solid (`btn-success`)
  - Flag 21 → Red solid (`btn-error`)
- Other buttons reset to outline state
- Individual feedback appears if provided
- Flag 29 content becomes visible
- State persists until another option selected

## Syntax Reference

### Basic Patterns

```markdown
# Minimal (just flags)
- Option{:flag}

# With feedback
- Option{:flag | Feedback message}

# With CSS classes
- Option{:flag .class-name | Feedback}

# With pre-click classes (NEW!)
- Option{:flag .btn-secondary .pre-pulse | Feedback}

# Multi-line feedback
- Option{:flag | Line 1
  Line 2
  Line 3}

# Comment (always visible)
- This is always shown

# Explanation (shows after any answer)
- Title{:29 | Detailed explanation}
```

### Complete Example

```markdown
What causes rain?

- The sun{:21 | The sun evaporates water, but doesn't directly cause rain.}
- Water cycle{:20 | Correct! The water cycle includes evaporation, condensation, and precipitation.}
- Wind{:21 | Wind moves clouds but doesn't create rain.}
- Temperature only{:21 | Temperature is involved but not the complete answer.}
- Note: This is a simplified explanation
- Learn More{:29 | **The Water Cycle:**
  1. **Evaporation**: Sun heats water → water vapor
  2. **Condensation**: Vapor cools → forms clouds
  3. **Precipitation**: Droplets combine → fall as rain
  4. **Collection**: Water returns to rivers, lakes, oceans}
{: .i-radio}
```

## HTML Structure

### Generated HTML

```html
<div class="fragment-wrapper" data-f_type="radio_">
  <div class="fragment" data-f_type="radio_">
    <!-- Buttons -->
    <div class="flex flex-wrap gap-2 items-center">
      <button class="btn btn-primary btn-sm btn-outline" 
              data-flag="21" 
              data-feedback="...">
        Option Text
      </button>
      <!-- More buttons -->
    </div>
    
    <!-- Feedback area (hidden initially) -->
    <div id="radio-feedback-0" class="mt-3 hidden">
      <div class="alert">
        <span id="radio-feedback-text-0"></span>
      </div>
    </div>
    
    <!-- Flag 29 explanation (hidden initially) -->
    <div id="radio-explanation-0" class="mt-4 hidden">
      <div class="card bg-base-200">
        <div class="card-body">
          <div class="prose max-w-none">
            <!-- Explanation content -->
          </div>
        </div>
      </div>
    </div>
    
    <!-- Always visible comments -->
    <div class="text-sm opacity-70 italic mt-3">
      Comment text
    </div>
  </div>
</div>
```

## JavaScript Behavior

### Click Handler

```javascript
function handleRadioClick(groupIndex, flag, button) {
    // 1. Reset all buttons to outline state
    // 2. Apply success/error class to clicked button
    // 3. Show individual feedback if available
    // 4. Show flag 29 content
    // 5. Store answer in localStorage
    // 6. Dispatch custom event
}
```

### Custom Events

```javascript
// Listen for answer events
document.addEventListener('i-radio-answered', (event) => {
    console.log(event.detail);
    // { fragmentIndex, flag, isCorrect, feedback, timestamp }
});
```

## Implementation Files

### Backend (Python)

1. **`src/core/pm/services/fragment_builder.py`**
   - `capture_html_flag_feedback()` - Parses markdown syntax
   - `from_list()` - Builds fragment data structure

2. **`src/core/pm/services/i_radio_utils.py`**
   - Flag constants (20, 21, 29, -1)
   - Helper functions for validation
   - CSS class mappings

### Frontend (HTML/JS)

1. **`src/templates/pm/index.html`**
   - Fragment rendering template
   - Click handler JavaScript
   - CSS styles

## Advanced Features

### Pre-Click CSS Classes (NEW!)

You can now add CSS classes that are active only before any button is clicked. This is perfect for creating call-to-action effects that disappear once the user starts interacting.

#### How It Works
- **Pre-click classes**: Any CSS class starting with `pre-` is applied initially
- **On first click**: All `pre-` classes are removed from ALL buttons in the group
- **DaisyUI override**: If custom classes contain `btn-` variants, they override default styling
- **Backward compatibility**: Existing i-radio fragments work unchanged

#### Basic Pre-Click Example

```markdown
What is 2 + 2?

- 3{:21 .pre-pulse .pre-glow | Wrong, but nice try!}
- 4{:20 .pre-pulse .pre-glow | Perfect!}
- 5{:21 .pre-pulse .pre-glow | Too high!}
{: .i-radio}
```

All buttons will pulse and glow until the user clicks any button.

#### DaisyUI Button Override

```markdown
Choose your favorite:

- Red{:20 .btn-error .btn-lg .pre-animate-bounce | Fiery!}
- Blue{:20 .btn-info .btn-lg .pre-animate-bounce | Cool!}
- Green{:20 .btn-success .btn-lg .pre-animate-bounce | Natural!}
{: .i-radio}
```

This creates large colored buttons that bounce initially, completely overriding the default primary outline styling.

#### Available Pre-Click Classes

- `.pre-pulse` - Pulsing animation
- `.pre-bounce` - Bouncing animation  
- `.pre-glow` - Blue glow effect
- `.pre-animate-spin` - Spinning animation
- `.pre-bg-warning` - Warning background color
- `.pre-shadow-lg` - Large shadow
- `.pre-ring` - Ring effect
- And more...

### Multi-line Feedback

```markdown
- Answer{:21 | This is wrong because:
  - Reason 1
  - Reason 2
  - Reason 3}
{: .i-radio}
```

### LaTeX Support

```markdown
- $x = 2${:21 | Try again: $x^2 = 4$ has two solutions}
- $x = \pm 2${:20 | Perfect! Both $x = 2$ and $x = -2$ work}
{: .i-radio}
```

### Code in Feedback

```markdown
- Option{:20 | Here's the code:
  ```python
  def example():
      return "Hello"
  ```}
{: .i-radio}
```

### Nested Markdown

```markdown
- Answer{:29 | **Bold**, *italic*, `code`
  
  1. Ordered list
  2. With items
  
  - Unordered too
  - Works great}
{: .i-radio}
```

## Best Practices

### Do's ✅

- **Provide feedback** for wrong answers explaining why
- **Use flag 29** for detailed explanations
- **Keep buttons concise** - put details in feedback
- **Test all paths** - click each option
- **Use LaTeX** for math expressions
- **Add comments** for instructions
- **Use pre-click classes** for call-to-action effects
- **Override DaisyUI classes** when you need custom styling

### Don'ts ❌

- Don't make button text too long
- Don't use flag 29 alone (needs interactive options)
- Don't mix unrelated questions in one fragment
- Don't forget to mark at least one answer correct
- Don't use complex HTML in button text

## Common Patterns

### Single Correct Answer

```markdown
- Wrong 1{:21 | Explanation why wrong}
- Wrong 2{:21 | Explanation why wrong}
- Correct{:20 | Explanation why right}
- Wrong 3{:21 | Explanation why wrong}
{: .i-radio}
```

### Multiple Correct Answers

```markdown
Which are fruits?

- Apple{:20 | Yes, a fruit}
- Carrot{:21 | No, a vegetable}
- Banana{:20 | Yes, a fruit}
- Potato{:21 | No, a vegetable}
{: .i-radio}
```

### Progressive Hints

```markdown
- Wrong{:21 | Hint: Think about...}
- Also wrong{:21 | Closer! Consider...}
- Correct{:20 | Exactly right!}
- Still wrong{:21 | Remember that...}
- Explanation{:29 | Full solution here}
{: .i-radio}
```

## Troubleshooting

### Issue: Buttons don't appear
**Cause:** No flags or all items have flag -1
**Solution:** Add flag 20 or 21 to create buttons

### Issue: Feedback doesn't show
**Cause:** Missing or malformed pipe syntax
**Solution:** Check syntax: `{:flag | message}`

### Issue: Flag 29 always visible
**Cause:** Implementation error
**Solution:** Flag 29 should be hidden until any answer clicked

### Issue: Special characters break display
**Cause:** Unescaped HTML characters
**Solution:** Characters are auto-escaped, check template

## Testing

Comprehensive test files available:
- `pms/examples/i_radio_example.md` - Basic examples
- `pms/examples/i_radio_test.md` - Feedback testing
- `pms/examples/i_radio_advanced.md` - Advanced features
- `pms/examples/i_radio_complete_test.md` - Edge cases

## Version History

- **v1.0** - Basic flags (20, 21, -1)
- **v2.0** - Added feedback with pipe syntax
- **v3.0** - Added flag 29 for explanations
- **Current** - Full feature set with multi-line support

## Future Enhancements

Potential additions:
- [ ] Timer for timed quizzes
- [ ] Score tracking across fragments
- [ ] Hint system with progressive reveals
- [ ] Audio feedback support
- [ ] Animation transitions
- [ ] Export answer history
- [ ] Accessibility improvements

## Support

For issues or questions:
1. Check test files for examples
2. Review this documentation
3. Verify flag values (20, 21, 29, -1)
4. Check browser console for errors
5. Ensure markdown syntax is correct
