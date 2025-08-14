---
title: number_input – PM Fragment Guide
description: Authoring and rendering guide for the number_input (number_) fragment using NumberInputPCA YAML.
chapter: Documentation
---

# number_input – PM Fragment Guide

The `number_input` fragment (f_type: `number_`) lets you define numeric questions with bounds, step, units, tolerance, and feedback using a YAML block embedded in Markdown. The backend parses it into a `number_` fragment; the frontend renders it with a Lit component.

## Authoring (YAML)

Use a fenced code block with `yaml`:

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

## Fields

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `NumberInputPCA` | string | yes | Version tag (e.g., `v0.0.1`) |
| `id` | string | recommended | Unique identifier |
| `type` | string | yes | Must be `number` |
| `label` | string | recommended | Prompt shown above input |
| `min` | number | optional | Minimum allowed value |
| `max` | number | optional | Maximum allowed value |
| `step` | number | optional | UI increment/decrement step |
| `unit` | string | optional | Displayed next to the input |
| `correct` | number | optional | Expected answer |
| `tolerance` | number | optional | ± margin around `correct` |
| `correct_values` | array | optional | List of `{ value, tolerance }` accepted ranges |
| `flag` | number | optional | i‑radio compatibility (20=correct, 21=wrong, 29=explain) |
| `feedback_correct` | string | optional | Message shown on success |
| `feedback_incorrect` | string | optional | Message shown on failure |
| `hint` | string | optional | Always-visible hint below input |

Notes:
- Use either `correct` (+ `tolerance`) or `correct_values`.
- All numeric values may be integers or floats.

## Quick Examples

Integer exact:
```yaml
NumberInputPCA: v0.0.1
id: apples_count
type: number
label: "How many apples are in the basket?"
min: 0
max: 20
step: 1
correct: 12
tolerance: 0
feedback_correct: "✅ Yes — there are exactly 12 apples."
feedback_incorrect: "❌ Not correct — count them again."
hint: "They are arranged in 3 rows of 4 apples."
```

Decimal with unit + tolerance:
```yaml
NumberInputPCA: v0.0.1
id: tank_volume
type: number
label: "Enter the volume of the tank"
min: 0.0
max: 1000.0
step: 0.1
unit: "liters"
correct: 523.6
tolerance: 0.5
feedback_correct: "✅ Perfect, rounded to one decimal place."
feedback_incorrect: "❌ Check the π and rounding steps."
hint: "The shape is a cylinder with r = 10 cm and h = 166.4 cm."
```

Multiple acceptable ranges:
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

## Rendering behavior

- Server parses YAML → `number_` fragment.
- Template renders `<pm-number-input>` and injects the data.
- Component shows:
  - A parameter table (id, min, max, step, unit, correct, tolerance, etc.)
  - A numeric input with unit
  - A live value preview (KaTeX font for aesthetic alignment with math)
  - A Check button and feedback region

## Styling

The `pm-number-input` component inherits theme colors from the PM container.

- Text size: larger (approx. `text-lg`) for input value
- Font stack includes KaTeX_Main for a math-friendly look
- Success/Error colors flow from CSS variables exposed on `.pm-container`

Relevant CSS (already shipped in `@core/css/pm.css`):

```css
.fragment-wrapper[data-f_type="number_"] { margin: 1.25rem 0 1.5rem; }
pm-number-input { --ok: var(--pm-ok); --err: var(--pm-err); }
```

## Live Examples

- PM route: `/pm/examples/number_input_example.md?format=html`
- Standalone component demo: `/static/js/examples/pm-number-input-example.html`

## See Also

- `pms/documentation/interactive_fragments_guide.md` (section: NumberInputPCA)
- `pms/documentation/fragments_quick_reference.md`
- `pms/examples/number_input_example.md`


