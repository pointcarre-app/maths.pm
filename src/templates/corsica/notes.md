# Firefox Fragment Order Fix - Notes

## Issue Fixed
In Firefox, the "Corrigé Enseignant" (teacher correction table) was appearing ABOVE the print button instead of below it, unlike Chrome/other browsers.

## Root Cause
The Firefox-specific code path was creating a **combined fragment** that included both:
1. Parameters table 
2. Teacher correction table with collapsible `<details>` element

This combined fragment was injected as the **first fragment**, but the print button gets added AFTER the first fragment in `injectFragmentsIntoPM()`. So the order was:
1. ✅ Combined fragment (parameters + teacher table) 
2. ✅ Print button added

Instead of the intended:
1. ✅ Parameters table
2. ✅ Print button  
3. ✅ Teacher correction table

## Solution Applied
Changed Firefox to use the **same fragment structure as Chrome** but with Firefox-specific CSS classes for print compatibility:

### Code Changes Made:

1. **Fragment Structure (lines 1760-1913)**:
   - Firefox now creates **two separate fragments** like Chrome
   - First fragment: Parameters table only (with `firefox-parameters-*` classes)
   - Second fragment: Teacher table only (with `firefox-teacher-*` classes)
   - Removed the combined fragment approach entirely

2. **Print CSS Updates (lines 973-998)**:
   - Added new Firefox-specific CSS classes to existing print rules:
     - `.firefox-teacher-section`
     - `.firefox-parameters-section` 
     - `.firefox-parameters-wrapper`
     - `.firefox-parameters-table`
   - Updated fragment selectors for better print compatibility

3. **TOC Navigation Fix (lines 1242-1248)**:
   - Enhanced selector to find teacher details element more reliably
   - Added fallback selector and debug logging
   - Uses `document.querySelector(".teacher-answer-details.screen-only") || document.querySelector(".teacher-answer-details")`

## Result
Firefox now shows the same order as Chrome:
1. ✅ Parameters table
2. ✅ Print button + TOC
3. ✅ Teacher correction table (collapsible)

## Files Modified
- `files/sujets0/sujets0_question_generator_v1.js`
  - Lines 1760-1913: Firefox fragment structure 
  - Lines 973-998: Print CSS updates
  - Lines 1242-1248: TOC navigation enhancement

## Additional Fix: Firefox Title Separation Issue

### Problem
When content doesn't fit on one page, Firefox was separating the "Corrigé Enseignant" title from its table, showing:
- Page N: "Corrigé Enseignant" title alone
- Page N+1: The actual table

### Solution
**Removed the print title entirely for Firefox** (lines 1906-1909):
- Firefox print version now shows table directly without title
- Screen version still shows collapsible details with title
- Chrome/other browsers unchanged (still show title in print)

### Additional CSS (lines 1000-1017):
- `.firefox-print .print-only-teacher-table`: Remove margins/padding
- Force table to start immediately without gaps
- Ensure table stays together as one unit

## Additional Fix: Firefox Table Page Separation

### Problem
Firefox was forcing the parameters table and teacher correction table onto separate pages even when they could fit together, wasting space and creating unnecessary page breaks.

### Solution
**Updated Firefox print CSS** (lines 973-994):
- Changed from `page-break-inside: avoid` to `page-break-inside: auto` for teacher table
- Kept `page-break-before: avoid` between the two tables to encourage them to stay together
- Reduced margin between tables to 0.25rem
- Allow teacher table to break internally if absolutely necessary

## Testing Notes
- Firefox-specific print compatibility maintained through CSS classes
- TOC "Corrigé Enseignant" link should now properly open details and scroll
- **Firefox print: No title, just table** (prevents page break issues)
- **Firefox print: Tables try to fit together when possible**
- **Chrome print: Still shows title** (no change)
- No changes to screen display behavior

## Safety Measures
- Kept all existing Firefox print CSS rules
- Added new classes instead of replacing existing ones
- Enhanced TOC selector with fallback instead of replacing
- No changes to Chrome code path
- **Title removal only affects Firefox print mode**
- **Page break changes only affect Firefox print mode**