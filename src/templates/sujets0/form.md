# Sujets0 Form Implementation Documentation

## Overview
The Sujets0 form is a mathematics exercise generator for French high school students preparing for their "Baccalauréat" exam. It generates randomized questions with consistent formatting and includes teacher correction tables.

## Table of Contents
1. [Form Structure](#form-structure)
2. [Tab System](#tab-system)
3. [Form Validation](#form-validation)
4. [Question Generation](#question-generation)
5. [Print Functionality](#print-functionality)
6. [Known Issues & Solutions](#known-issues--solutions)
7. [Technical Architecture](#technical-architecture)

---

## Form Structure

### Main Components
- **form.html**: Main form template with tabs and input fields
- **tabs.html**: Tab navigation component (Generate, Documentation, Subjects)
- **sujets0_question_generator_v1.js**: Core JavaScript for question generation

### Form Fields
```html
<!-- Number of copies (1-50) -->
<input type="number" id="nb-eleves" min="1" max="50" value="2" required>

<!-- Curriculum selection (radio buttons) -->
<input type="radio" name="sujets0" value="spe">    <!-- Spécialité -->
<input type="radio" name="sujets0" value="gen">    <!-- Non-Spécialité -->
<input type="radio" name="sujets0" value="techno"> <!-- Technologique (disabled) -->

<!-- Questions per copy (1-12) -->
<input type="number" id="nb-questions" min="1" max="12" value="12" required>

<!-- Random seed (1-100) -->
<input type="number" id="seed" min="1" max="100" value="9" required>
```

---

## Tab System

### Implementation (tabs.html)
The tab system uses DaisyUI button groups with dynamic style switching:

```javascript
// Tab switching with opacity for inactive tabs
tabButtons.forEach(btn => {
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-outline');
    btn.style.opacity = '0.7';        // 70% opacity for inactive
    btn.style.fontWeight = '400';      // Normal font weight
});

// Active tab gets full opacity
this.classList.add('btn-primary');
this.style.opacity = '1';
this.style.fontWeight = '400';
```

### Styling Features
- **Active tab**: `btn-primary` class, full opacity
- **Inactive tabs**: `btn-outline` class, 70% opacity
- **Font weight**: Always 400 (normal) for all states
- **Responsive text**: Different labels for mobile/desktop

---

## Form Validation

### Current Implementation
Basic HTML5 validation with manual checks:

```javascript
function generateFromForm() {
    const config = extractFormConfig();
    
    // Validate number ranges
    if (isNaN(nbStudents) || nbStudents < 1 || nbStudents > 50) {
        alert("⚠️ Le nombre de copies doit être entre 1 et 50");
        return;
    }
    
    if (isNaN(nbQuestions) || nbQuestions < 1 || nbQuestions > 12) {
        alert("⚠️ Le nombre de questions doit être entre 1 et 12");
        return;
    }
    
    // Check curriculum selection
    if (!curriculumRadio) {
        throw new Error("Curriculum not selected");
    }
}
```

### DaisyUI Validator Enhancement (Proposed)
To improve UX, implement DaisyUI's validator classes:

```html
<!-- Number input with validator -->
<input type="number" 
       class="input input-bordered validator" 
       id="nb-eleves" 
       min="1" max="50" 
       required>
<p class="validator-hint">Doit être entre 1 et 50</p>

<!-- Radio validation with hidden input -->
<input type="hidden" 
       id="sujets0-validator" 
       class="validator" 
       required 
       pattern="spe|gen|techno">
<p class="validator-hint">Veuillez sélectionner une filière</p>
```

With JavaScript sync:
```javascript
function syncRadioValidator() {
    const radios = document.querySelectorAll('input[name="sujets0"]');
    const hiddenValidator = document.getElementById('sujets0-validator');
    
    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.checked) {
                hiddenValidator.value = radio.value;
                hiddenValidator.dispatchEvent(new Event('input'));
            }
        });
    });
}
```

---

## Question Generation

### Process Flow
1. **Configuration extraction** from form fields
2. **URL construction** with query parameters
3. **Navigation** to generation page: `/pm/sujets0/a_generate.md`
4. **Generator execution** using Nagini Python engine
5. **PDF-ready output** with KaTeX math rendering

### URL Parameters
```javascript
const targetUrl = `${baseUrl}${targetPath}?format=html
    &nbStudents=${config.nbStudents}
    &nbQuestions=${config.nbQuestions}
    &seed=${config.seed}
    &curriculum-slug=${encodeURIComponent(config.curriculumSlug)}
    &curriculum=${encodeURIComponent(config.curriculum)}`;
```

### Generator Selection
Generators are filtered by curriculum:
```javascript
const selectedGenerators = CONFIG.generators
    .filter(generator => generator.startsWith(CONFIG.curriculumSlug))
    .slice(0, CONFIG.nbQuestions);
```

---

## Print Functionality

### The Teacher Correction Table Problem
**Issue**: The teacher correction table wasn't visible when printing if the `<details>` element was closed.

**Root Cause**: Browsers don't render closed `<details>` content during print, even with CSS overrides.

### Solution: Dual Table Approach
Create two versions of the table - one for screen, one for print:

```javascript
let tableHtml = `
    <div id="teacher-answer-table" class="mb-6">
        <!-- Screen version with collapsible details -->
        <details class="teacher-answer-details screen-only">
            <summary class="teacher-summary">
                Corrigé Enseignant
            </summary>
            <div>
                ${tableContent}
            </div>
        </details>
        
        <!-- Print version that's always visible during print -->
        <div class="print-only-teacher-table">
            <h3>Corrigé Enseignant</h3>
            ${tableContent}
        </div>
    </div>
`;
```

### CSS Implementation
```css
/* Screen styles */
@media screen {
    .print-only-teacher-table {
        display: none !important;
    }
}

/* Print styles */
@media print {
    .screen-only {
        display: none !important;
    }
    
    .print-only-teacher-table {
        display: block !important;
    }
}
```

### Print Button Handler (Simplified)
```javascript
function handlePrint() {
    addPrintStyles();
    
    const pmContainer = document.querySelector(".pm-container .max-w-\\[640px\\]");
    if (pmContainer) {
        pmContainer.classList.add("print-target");
    }
    
    setTimeout(() => {
        window.print();
        
        setTimeout(() => {
            if (pmContainer) {
                pmContainer.classList.remove("print-target");
            }
        }, 1000);
    }, 50);
}
```

---

## Known Issues & Solutions

### 1. Safari Print Support
- **Issue**: Print functionality doesn't work properly on Safari
- **Status**: Known limitation, users advised to use Firefox/Chrome
- **Workaround**: None available

### 2. Theme Enforcement
- **Issue**: Printing requires "anchor" theme for proper rendering
- **Solution**: Theme is automatically forced during generation
```javascript
if (currentTheme !== "anchor") {
    document.documentElement.setAttribute("data-theme", "anchor");
    localStorage.setItem("theme", "anchor");
    showToast("⚡ Le thème anchor est obligatoire pour l'impression", "info");
}
```

### 3. Background Graphics
- **Issue**: Browser print dialogs may not include background colors/graphics by default
- **Solution**: Users must manually enable "Background graphics" in print settings

---

## Technical Architecture

### Dependencies
- **Nagini**: Python execution engine for question generation
- **KaTeX**: LaTeX math rendering
- **DaisyUI**: UI component framework
- **Tailwind CSS**: Utility-first CSS framework
- **PCAGraphLoader**: SVG graph generation for mathematical functions

### File Structure
```
src/templates/sujets0/
├── form.html                  # Main form template
├── tabs.html                  # Tab navigation component
├── documentation.html         # Documentation content
├── header.html               # Page header
└── modal-info-content.html   # Modal information

files/sujets0/
└── sujets0_question_generator_v1.js  # Core generation logic

src/sujets0/generators/
├── gen_sujet2_auto_*.py     # Non-specialty generators
└── spe_sujet1_auto_*.py     # Specialty generators
```

### Key Functions

#### Form Configuration Extraction
```javascript
function extractFormConfig() {
    return {
        nbStudents: document.getElementById("nb-eleves")?.value || 2,
        nbQuestions: document.getElementById("nb-questions")?.value || 12,
        seed: document.getElementById("seed")?.value || 9,
        curriculum: curriculumMapping[curriculumRadio.value],
        curriculumSlug: curriculumRadio.value
    };
}
```

#### Question Generation Pipeline
```javascript
async function executeAllGenerators() {
    const selectedGenerators = CONFIG.generators
        .filter(g => g.startsWith(CONFIG.curriculumSlug))
        .slice(0, CONFIG.nbQuestions);
    
    for (let studentNum = 1; studentNum <= CONFIG.nbStudents; studentNum++) {
        const seed = CONFIG.rootSeed + studentNum * Math.floor(Math.random() * 137);
        
        for (const generator of selectedGenerators) {
            const result = await executeGeneratorWithSeed(generator, seed);
            // Process and store results
        }
    }
}
```

---

## Best Practices

### 1. Form Validation
- Use HTML5 validation attributes (`min`, `max`, `required`)
- Implement DaisyUI validator classes for better UX
- Provide clear error messages in French

### 2. Print Optimization
- Always test print functionality in multiple browsers
- Use duplicate content approach for critical print elements
- Minimize JavaScript manipulation during print events

### 3. Accessibility
- Maintain keyboard navigation support
- Use proper ARIA labels for screen readers
- Ensure sufficient color contrast (especially in print)

### 4. Performance
- Use parallel tool calls when possible
- Cache generated content to avoid regeneration
- Minimize DOM manipulation during runtime

---

## Future Enhancements

### Planned Features
1. **Techno curriculum support** (currently disabled)
2. **Save/load configurations** for repeated use
3. **Batch export** to multiple PDF files
4. **Question difficulty levels** customization
5. **Custom question pools** per teacher

### Proposed Improvements
1. Replace alert() with toast notifications
2. Add progress indicators during generation
3. Implement auto-save for form state
4. Add preview before final generation
5. Support for custom LaTeX templates

---

## Maintenance Notes

### Testing Checklist
- [ ] Form validation works for all input ranges
- [ ] Tab switching maintains proper styling
- [ ] Print output includes teacher correction table
- [ ] Questions generate with correct numbering
- [ ] Graphs render properly in print
- [ ] Theme enforcement doesn't break UI
- [ ] Mobile responsiveness maintained

### Common Debugging Steps
1. Check browser console for JavaScript errors
2. Verify Nagini engine is loaded properly
3. Ensure KaTeX CSS is included
4. Test with different seed values
5. Validate generator file paths

---

## Contact & Support

For issues or questions about the Sujets0 form implementation:
- Review this documentation first
- Check browser compatibility (Chrome/Firefox preferred)
- Ensure all dependencies are loaded
- Test with default values before customization

Last Updated: December 2024
