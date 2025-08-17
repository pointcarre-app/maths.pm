# Generator Levels Implementation

## Overview
This document describes the implementation of education level indicators (2DE vs 1ERE) for all exercise generators in the Sujets0 application, based on the COMPETENCES_MAPPING.md analysis.

## What Was Added

### 1. Router Changes (`src/sujets0/router.py`)

#### GENERATOR_LEVELS Dictionary
A comprehensive dictionary mapping each generator to its appropriate education level:
```python
GENERATOR_LEVELS = {
    "spe_sujet1_auto_01_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_01_question": {"level": "1ERE", "note": "probabilités conditionnelles"},
    # ... etc
}
```

#### Helper Function
```python
def get_generator_level_info(generator_name):
    """Get level information for a generator"""
```

#### Context Updates
All route handlers now pass level information to templates:
- `generator_levels`: Full dictionary of all generator levels
- `get_generator_level`: Helper function to get level info

### 2. Template Updates

#### ex_ante_generated.html
- Generator dropdown now shows level badges: `gen_name [2DE] (95/100)`
- Questions display with colored level badges

#### originals.html
- Related generators show level badges with tooltips
- Color coding: blue for 2DE, yellow for 1ERE

#### ex_ante_generated_error_analysis.html
- Error table includes level badges for each generator
- Helps identify if errors are in basic (2DE) or advanced (1ERE) questions

#### JavaScript Updates (`pre-generated-viewer.js`)
- Question cards display level badges
- Tooltips show special notes (e.g., "demanding but manageable")

### 3. Level Distribution

Based on COMPETENCES_MAPPING.md analysis:
- **2DE Level**: 59 generators (95.2%)
  - All GEN Sujet 1, 2, 3 (36 generators)
  - All SPE Sujet 1 (12 generators)
  - Most SPE Sujet 2 (11 generators)
- **1ERE Level**: 1 generator (1.6%)
  - `spe_sujet2_auto_01_question` (conditional probabilities)
- **Special Cases**: 2 generators marked "demanding but manageable" for 2DE

## Visual Design

### Color Coding
- **Blue badge** (`badge-info`): 2DE level - accessible to seconde students
- **Yellow badge** (`badge-warning`): 1ERE level - requires première knowledge

### Badge Placement
- Always appears next to generator name
- Tooltips provide additional context when available
- Consistent across all views

## Usage in Templates

```html
{# Display level badge for a generator #}
{% set level_info = get_generator_level(generator_name) %}
<span class="badge {% if level_info.level == '1ERE' %}badge-warning{% else %}badge-info{% endif %}">
  {{ level_info.level }}
</span>
```

## Benefits

1. **Educational Clarity**: Teachers immediately see which exercises are appropriate for their students' level
2. **Curriculum Alignment**: Clear mapping to official French education levels (Seconde/Première)
3. **Filtering Capability**: Can easily filter questions by difficulty level
4. **Error Analysis**: Helps identify if generation errors occur more in basic or advanced questions

## Technical Notes

- Level information is centralized in the router for maintainability
- JavaScript and templates are synchronized via the JSON data passed to frontend
- System is extensible - easy to add new levels or modify existing mappings

## Future Enhancements

Potential improvements:
1. Add level filtering in the UI (show only 2DE or 1ERE questions)
2. Create level-specific practice sets
3. Add progression tracking (2DE → 1ERE)
4. Generate difficulty reports by level
