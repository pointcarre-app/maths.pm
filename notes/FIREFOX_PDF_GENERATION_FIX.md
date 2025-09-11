# Firefox PDF Generation Fix for Sujets0

## Problem Description

When generating PDFs in Firefox, the document structure breaks with multiple issues:

### Initial Symptoms:
1. "Corrigé enseignant" title appears alone on a new page
2. The teacher correction table appears on yet another new page
3. The parameters table and teacher correction section are not kept together

### After First Fix Attempt:
1. "Bac 1ère Maths - Génération de copies" appears alone on a page
2. Empty page follows
3. Parameters table on separate page
4. Teacher correction on another separate page

## Root Cause

Firefox interprets CSS page-break rules more strictly than Chrome and has different default behaviors for:
- `break-inside` properties
- Fragment boundaries between elements
- Table element page-break handling

## Solution Implementation (Simplified Approach)

After testing, a simpler conditional approach works better:

### 1. Firefox Detection in Fragment Generation
Detect Firefox at the fragment generation level and conditionally render:

```javascript
const isFirefox = navigator.userAgent.includes('Firefox');
```

### 2. Conditional Rendering
For Firefox, remove titles that cause page breaks:
- No "Paramètres de la génération" title in print view
- No "Corrigé Enseignant" title in print view for Firefox
- Keep tables only, letting them flow naturally

### 3. Browser Detection for CSS
Still add the Firefox class for CSS targeting:

```javascript
if (navigator.userAgent.includes('Firefox')) {
    document.body.classList.add('firefox-print');
}
```

### 2. Enhanced CSS Rules

#### A. Multiple Fallback Properties
Use all available page-break properties for maximum compatibility:

```css
page-break-inside: avoid !important;
break-inside: avoid !important;
-moz-column-break-inside: avoid !important; /* Firefox specific */
break-inside: avoid-page !important; /* More explicit */
```

#### B. Firefox-Specific Rules
Target Firefox with specific print styles:

```css
/* Firefox-specific adjustments */
.firefox-print .fragment-wrapper:has(#teacher-answer-table),
.firefox-print .print-only-teacher-table {
    display: table !important;
    width: 100% !important;
    page-break-inside: avoid !important;
    break-inside: avoid-page !important;
}

.firefox-print .fragment-wrapper[data-f_type="p_"]:has(table) {
    break-inside: avoid-page !important;
    page-break-inside: avoid !important;
}
```

#### C. Keep Content Together
Force the parameters table and teacher correction to stay together:

```css
/* Keep parameters table and teacher correction together */
.fragment-wrapper:has(.parameters-table),
.fragment-wrapper:has(.parameters-table) + .fragment-wrapper {
    page-break-after: avoid !important;
    break-after: avoid !important;
}

/* Ensure teacher table title and content stay together */
.print-only-teacher-table > div:first-child {
    page-break-after: avoid !important;
    break-after: avoid !important;
    margin-bottom: 0.5rem !important; /* Reduce spacing to help fit */
}
```

#### D. Orphans and Widows Control
Prevent single lines from being isolated:

```css
.print-only-teacher-table {
    orphans: 4;
    widows: 4;
}
```

### 3. Structural Improvements

#### A. Wrapper Container
Consider wrapping related content in a single container:

```html
<div class="teacher-section-wrapper" style="break-inside: avoid;">
    <!-- Parameters table -->
    <!-- Teacher correction title and table -->
</div>
```

#### B. Display Table Hack
Firefox respects `display: table` better for page breaks:

```css
.teacher-section-wrapper {
    display: table;
    width: 100%;
    break-inside: avoid;
}
```

## Testing Checklist

- [ ] Test in Firefox: Verify "Corrigé enseignant" stays with its table
- [ ] Test in Firefox: Verify parameters table stays with teacher correction
- [ ] Test in Chrome: Ensure no regression
- [ ] Test in Edge: Verify compatibility
- [ ] Test with different numbers of questions/students
- [ ] Test with long question content that might force page breaks

## Browser Compatibility Notes

- **Chrome**: Handles page-break rules flexibly, generally works without special handling
- **Firefox**: Requires explicit and redundant page-break rules, benefits from `display: table`
- **Safari**: Has known issues with print preview (documented separately)
- **Edge**: Generally follows Chrome's behavior

## Implementation Details

### Final Solution: Combined Fragment Approach

The key insight is that Firefox treats fragment boundaries as potential page break points. The solution combines both tables into a single fragment for Firefox while keeping them separate for Chrome.

### Changes Made:

1. **Print Button Position** (line 622-629)
   - Moved print button outside of details section to prevent it appearing in summary

2. **Firefox Detection** (lines 715-718, 1702)
   - Added `firefox-print` class to body in `addPrintStyles()`
   - Added `const isFirefox = navigator.userAgent.includes('Firefox');` in fragment generation

3. **Shared Table Content Generation** (lines 1704-1761)
   - Moved teacher table content generation before the conditional logic
   - This content is used by both Firefox and Chrome branches

4. **Firefox: Single Combined Fragment** (lines 1766-1865)
   - Both parameters table and teacher correction table in ONE fragment
   - No titles in print view (they cause page breaks)
   - Single `PMFragmentGenerator.createParagraph()` call with class `firefox-combined-teacher-section`

5. **Chrome: Separate Fragments** (lines 1867-2081)
   - Parameters table in first fragment with title
   - Teacher correction table in second fragment with title
   - Original structure preserved

6. **CSS Firefox-specific Rules** (lines 980-1002)
   - Added styles for `.firefox-combined-tables` and `.firefox-combined-teacher-section`
   - Multiple fallback properties for page-break control
   - `display: table` hack for better Firefox handling

## Implementation Location

File: `/files/sujets0/sujets0_question_generator_v1.js`
- Firefox detection in `addPrintStyles()`: lines 715-718
- Firefox detection in `generateFragmentsFromResults()`: line 1679
- Conditional rendering: lines 1687, 1884-1920
- CSS modifications: lines 966-1020, 841-852

## Fallback Strategy

If the CSS-only approach doesn't fully resolve the issue:
1. Use JavaScript to measure content height
2. Dynamically add page breaks where appropriate
3. Consider restructuring the DOM to have fewer fragment boundaries
