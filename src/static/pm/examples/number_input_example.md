---
# Page-specific metatags
title: "Number Input Example - Number Input Components"
description: "Interactive number input fields for mathematical exercises"
keywords: "number input, forms, interactive, mathematics, components"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "Number Input Example"
og:description: "Interactive number input fields for mathematical exercises"
og:type: "article"
og:url: "https://maths.pm/pm/examples/number_input_example.md"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "Number Input Example"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "Components, Forms, Documentation"
revised: "2025-01-15"
pagename: "Number Input Example"
---
# NumberInputPCA – Example Snippets

This file contains ready-to-copy YAML blocks for the upcoming NumberInputPCA fragment. Paste a block into your Markdown (inside a fenced code block) to describe a numeric question. Rendering will be handled by the frontend later.

## 1) Integer exact

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

## 2) Decimal with unit and tolerance

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

## 3) Physics (FR)

```yaml
NumberInputPCA: v0.0.1
id: vitesse_train
type: number
label: "Quelle est la vitesse moyenne du train ?"
min: 0
max: 500
step: 0.1
unit: "km/h"
correct: 120.5
tolerance: 0.2
feedback_correct: "✅ Parfait, c'est bien 120,5 km/h."
feedback_incorrect: "❌ Non, vérifiez la formule v = d / t."
hint: "Le train parcourt 241 km en 2 heures."
```

## 4) Multiple correct ranges

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
hint: "Réponse attendue au niveau de la mer."
```

## 5) Integer only

```yaml
NumberInputPCA: v0.0.1
id: classroom_tables
type: number
label: "How many tables are in the room?"
min: 0
max: 50
step: 1
correct: 18
tolerance: 0
feedback_correct: "✅ Exactly! There are 18 tables."
feedback_incorrect: "❌ Count them from the front row to the back."
```

## 6) With flag (compat)

```yaml
NumberInputPCA: v0.0.1
id: gravity_accel
type: number
label: "Value of g on Earth"
min: 0
max: 20
step: 0.01
unit: "m/s²"
correct: 9.81
tolerance: 0.01
flag: 20
feedback_correct: "✅ Correct, g ≈ 9.81 m/s²."
feedback_incorrect: "❌ Wrong, try considering Earth's mass and radius."
```

---

For full specification details, see `pms/documentation/number_input.md`.
