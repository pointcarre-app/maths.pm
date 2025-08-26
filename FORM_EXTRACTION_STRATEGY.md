# Form Extraction Strategy & Naming Conventions

## Overview
This document outlines the standardized approach for extracting form values from the Arpege generator form, including idiomatic naming conventions and validation strategies.

## Form Element Naming Conventions

### Number Inputs

| Element ID | Semantic Name | Description | Range |
|------------|--------------|-------------|--------|
| `nb-eleves` | `studentCount` / `copies.count` | Number of exam copies to generate | 1-50 |
| `nb-questions` | `questionCount` / `questions.perCopy` | Number of questions per copy | 1-12 |

### Radio Button Groups

| Input Name | Semantic Name | Values | Description |
|------------|--------------|---------|------------|
| `options` | `programLevel` / `program.level` | `"2nde"`, `"2nde & 1ère"` | Academic program coverage |
| `sujets0` | `specialization` / `track.type` | `"Spé."`, `"Non Spé."`, `"Techno"` | Mathematics track/specialization |

## Form Data Structure

```javascript
{
    // Student/Copy configuration
    copies: {
        count: number,          // 1-50
        isValid: boolean
    },
    
    // Question configuration  
    questions: {
        perCopy: number,        // 1-12
        isValid: boolean
    },
    
    // Program level selection
    program: {
        level: string,          // "2nde" or "2nde & 1ère"
        includesFirstYear: boolean,
        isValid: boolean
    },
    
    // Specialization selection
    track: {
        type: string,           // "Spé." or "Non Spé." or "Techno"
        isSpeciality: boolean,
        isValid: boolean
    },
    
    // Global validation
    isComplete: boolean,
    errors: Array<{
        field: string,
        message: string
    }>
}
```

## Extraction Functions

### 1. Main Extraction Function

```javascript
extractFormValues()
```

**Purpose**: Extracts all form values with automatic validation and type conversion.

**Returns**: Complete form data object with validation state.

**Usage**:
```javascript
const formData = extractFormValues();
if (formData.isComplete) {
    // Process valid form data
} else {
    // Handle validation errors
    console.error(formData.errors);
}
```

### 2. Validation Function

```javascript
validateFormData(formData)
```

**Purpose**: Validates all form fields and populates error messages.

**Side Effects**: Modifies `formData.errors` and `formData.isComplete`.

### 3. Configuration Generator

```javascript
getGeneratorConfig()
```

**Purpose**: Transforms validated form data into generator-ready configuration.

**Returns**: Simplified configuration object or `null` if validation fails.

**Output Structure**:
```javascript
{
    nbStudents: number,
    nbQuestions: number,
    programLevel: 'seconde' | 'both',
    track: 'speciality' | 'common',
    timestamp: number,
    sessionId: string
}
```

## Extraction Strategy

### 1. Number Input Extraction
```javascript
// Safe extraction with defaults
const value = parseInt(element?.value || defaultValue, 10);
```

### 2. Radio Button Extraction
```javascript
// Using aria-label for value extraction
const selected = document.querySelector('input[name="groupName"]:checked');
const value = selected?.getAttribute('aria-label') || null;
```

### 3. Validation Pattern
- Range validation for numbers
- Required field validation for radio groups
- Special case handling (disabled options)

## Error Handling

### Error Structure
```javascript
{
    field: string,      // Field identifier
    message: string     // Localized error message
}
```

### Error Messages
- `copies`: "Le nombre de copies doit être entre 1 et 50"
- `questions`: "Le nombre de questions doit être entre 1 et 12"
- `program`: "Veuillez sélectionner un niveau de programme"
- `track`: "Veuillez sélectionner une filière" or "La filière technologique n'est pas encore disponible"

## Usage Examples

### Basic Form Extraction
```javascript
// Extract form values
const formData = extractFormValues();

// Check if form is complete
if (formData.isComplete) {
    console.log(`Generating ${formData.copies.count} copies`);
    console.log(`With ${formData.questions.perCopy} questions each`);
}
```

### With Error Handling
```javascript
const config = getGeneratorConfig();

if (!config) {
    const formData = extractFormValues();
    const errorMessages = formData.errors
        .map(e => e.message)
        .join('\n');
    
    alert(`Please correct:\n${errorMessages}`);
    return;
}

// Process valid configuration
processGeneration(config);
```

### Direct Access Pattern
```javascript
// Quick extraction for specific needs
const formData = extractFormValues();

// Access specific values
const studentCount = formData.copies.count;
const isSpeciality = formData.track.isSpeciality;
const includesPremiere = formData.program.includesFirstYear;
```

## Best Practices

1. **Always validate** before using form data
2. **Use semantic names** in business logic (not HTML IDs)
3. **Handle null/undefined** with optional chaining (`?.`)
4. **Provide defaults** for missing values
5. **Type convert** immediately (string → number)
6. **Centralize validation** logic
7. **Use structured objects** over flat values

## Integration Points

### Global Access (Debugging)
```javascript
// Available in browser console
window.extractFormValues()
window.getGeneratorConfig()
```

### Module Exports
```javascript
import { 
    extractFormValues,
    validateFormData,
    getGeneratorConfig 
} from './sujets0-main.js';
```

## Future Enhancements

- [ ] Add form state persistence (localStorage)
- [ ] Add field-level validation feedback
- [ ] Add dynamic validation rules
- [ ] Add form reset functionality
- [ ] Add configuration presets
- [ ] Add validation debouncing

## Technical Notes

- Uses ES6+ features (optional chaining, nullish coalescing)
- No external dependencies
- Pure functions where possible
- Side effects isolated to validation
- Browser-compatible (no Node.js specific code)
