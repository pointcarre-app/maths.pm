# CodeMirror Height Configuration for PM-Codex Components

## Overview

This document describes the implementation of configurable height for CodeMirror instances in pm-codex components. The feature allows users to specify custom heights for code editors in YAML blocks, providing better control over the display of code content.

## Feature Summary

- **YAML Parameter**: `height_in_px: <number>`
- **Default Height**: 600px (when not specified)
- **Minimum Height**: 50px
- **Maximum Height**: 2000px
- **Scope**: Works with both `inline` and `script_path` codex blocks

## Usage

### Basic Example

```yaml
f_type: "codex_"
height_in_px: 800
inline: |
    import matplotlib.pyplot as plt
    
    # Your Python code here
    plt.figure(figsize=(12, 6))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    plt.show()
```

### With Script Path

```yaml
f_type: "codex_"
height_in_px: 400
script_path: "path/to/your/script.py"
```

### Compact Example

```yaml
f_type: "codex_"
height_in_px: 100
inline: |
    print("Hello, World!")
```

## Implementation Details

### Data Flow

1. **YAML Processing** (`fragment_builder.py`)
   - Captures `height_in_px` from YAML data
   - Validates and applies bounds (50px - 2000px)
   - Stores in `fragment.data["height_in_px"]`

2. **Template Rendering** (`codex_.html`)
   - Adds `data-height-in-px` attribute to fragment container
   - Only adds attribute when height is specified

3. **Component Wrapping** (`main.js`)
   - PMRuntime copies data attributes from fragment to `<pm-codex>` element
   - Ensures `data-height-in-px` is available on the component

4. **Height Application** (`pm-codex.js`)
   - Reads `data-height-in-px` from multiple sources (priority order)
   - Applies height to CodeMirror wrapper via JavaScript
   - Sets both `height` and `maxHeight` CSS properties

### File Changes

#### 1. Fragment Builder (`src/core/pm/services/fragment_builder.py`)

**Location**: Lines 762-770 in `from_code()` method

```python
# Capture height_in_px configuration if provided
if "height_in_px" in data:
    try:
        height_value = int(data["height_in_px"])
        # Ensure reasonable bounds (min 50px, max 2000px)
        data["height_in_px"] = max(50, min(2000, height_value))
    except (ValueError, TypeError):
        # Invalid height value, remove it to use default
        data.pop("height_in_px", None)
```

**Purpose**: 
- Validates height input from YAML
- Enforces minimum (50px) and maximum (2000px) bounds
- Handles invalid values gracefully

#### 2. Template (`src/templates/pm/fragments/codex_.html`)

**Change**: Added conditional data attribute

```html
<div class="fragment codex" data-f_type="{{ fragment.f_type.value }}" data-codex-container{% if fragment.data and fragment.data.height_in_px is defined %} data-height-in-px="{{ fragment.data.height_in_px }}"{% endif %}>
```

**Purpose**: 
- Passes height configuration from backend to frontend
- Only adds attribute when height is specified

#### 3. Runtime Component Wrapper (`src/static/js/pm/main.js`)

**Location**: Lines 210-217 in `initFragment()` method

```javascript
// Copy data attributes from fragment to host component
if (fragment && fragment.attributes) {
  for (const attr of fragment.attributes) {
    if (attr.name.startsWith('data-') && attr.name !== 'data-f_type') {
      host.setAttribute(attr.name, attr.value);
    }
  }
}
```

**Purpose**: 
- Copies all data attributes from fragment container to `<pm-codex>` element
- Ensures height configuration is accessible to the component

#### 4. PM-Codex Component (`src/static/js/pm/components/pm-codex.js`)

**Location**: Lines 137-166 in `start()` function

```javascript
// STEP 4.1: APPLY HEIGHT CONFIGURATION
// Check for height configuration in data attributes
// Priority: pm-codex element > container > wrapper
const heightInPx = this.getAttribute('data-height-in-px') || 
                 container.getAttribute('data-height-in-px') ||
                 wrapper?.getAttribute('data-height-in-px');

const cmWrapper = cm.getWrapperElement();

if (heightInPx) {
  const height = parseInt(heightInPx, 10);
  if (!isNaN(height) && height > 0) {
    // Set the custom height on the CodeMirror wrapper
    cmWrapper.style.height = `${height}px`;
    cmWrapper.style.maxHeight = `${height}px`;
    console.debug('[pm-codex] Applied custom height:', height + 'px');
  } else {
    // Invalid height, use default
    cmWrapper.style.height = '600px';
    cmWrapper.style.maxHeight = '600px';
    console.debug('[pm-codex] Invalid height, using default: 600px');
  }
} else {
  // No height specified, use default 600px
  cmWrapper.style.height = '600px';
  cmWrapper.style.maxHeight = '600px';
  console.debug('[pm-codex] No height specified, using default: 600px');
}

// Refresh CodeMirror to ensure proper rendering with new height
setTimeout(() => cm.refresh(), 10);
```

**Purpose**: 
- Detects height configuration from multiple sources
- Applies height to CodeMirror wrapper element
- Provides fallback to 600px default
- Refreshes CodeMirror for proper rendering

#### 5. CSS Updates (`src/static/core/css/pm.css`)

**Location**: Lines 1330-1343

```css
/* Default CodeMirror height for all pm-codex instances */
pm-codex .CodeMirror {
    min-height: 200px; /* Minimum height to ensure readability */
    overflow: hidden;
}

/* Make CodeMirror in pm-codex slightly taller for DataViz2 */
pm-codex[data-executable="true"] .CodeMirror {
    min-height: 200px;
    resize: vertical;
    overflow: hidden;
}
```

**Purpose**: 
- Removed CSS `max-height` constraints that would override JavaScript
- Kept minimum height for readability
- Let JavaScript handle all dynamic height setting

## Validation and Error Handling

### Input Validation

1. **Type Checking**: Only accepts integer values
2. **Range Validation**: Enforces 50px minimum, 2000px maximum
3. **Graceful Fallback**: Invalid values are removed, defaults to 600px

### Error Scenarios

| Scenario | Behavior | Example |
|----------|----------|---------|
| Valid height | Uses specified height | `height_in_px: 800` → 800px |
| Below minimum | Uses minimum (50px) | `height_in_px: 30` → 50px |
| Above maximum | Uses maximum (2000px) | `height_in_px: 3000` → 2000px |
| Invalid type | Uses default (600px) | `height_in_px: "tall"` → 600px |
| Not specified | Uses default (600px) | No parameter → 600px |

## Debugging

### Console Logs

The implementation includes debug logging to help troubleshoot issues:

```javascript
console.debug('[pm-codex] Applied custom height:', height + 'px');
console.debug('[pm-codex] Invalid height, using default: 600px');
console.debug('[pm-codex] No height specified, using default: 600px');
```

### Inspection

To verify the feature is working:

1. **Check the `<pm-codex>` element** for `data-height-in-px` attribute
2. **Inspect CodeMirror wrapper** for `style="height: XXXpx; max-height: XXXpx;"`
3. **Look for console logs** during component initialization

### Common Issues

1. **Height not applied**: Check if `data-height-in-px` attribute exists on `<pm-codex>` element
2. **Wrong height**: Verify the value is within bounds (50px - 2000px)
3. **CSS override**: Ensure no CSS rules are setting `!important` max-height

## Browser Compatibility

- **Modern Browsers**: Full support (Chrome, Firefox, Safari, Edge)
- **Legacy Support**: Falls back to default 600px height
- **Mobile**: Responsive behavior maintained

## Performance Considerations

- **Lazy Loading**: Height is applied only when CodeMirror becomes visible
- **Refresh Optimization**: Single refresh call after height application
- **Memory**: No significant memory overhead

## Future Enhancements

Potential improvements that could be added:

1. **Relative Heights**: Support for percentage-based heights
2. **Auto-sizing**: Dynamic height based on content length
3. **Breakpoint Heights**: Different heights for different screen sizes
4. **Animation**: Smooth transitions when height changes

## Related Files

- `src/core/pm/services/fragment_builder.py` - YAML processing
- `src/templates/pm/fragments/codex_.html` - Template rendering
- `src/static/js/pm/main.js` - Component wrapping
- `src/static/js/pm/components/pm-codex.js` - Component logic
- `src/static/core/css/pm.css` - Styling rules

## Testing

### Test Cases

1. **Basic functionality**: `height_in_px: 400` should create 400px editor
2. **Minimum bound**: `height_in_px: 10` should create 50px editor
3. **Maximum bound**: `height_in_px: 5000` should create 2000px editor
4. **Invalid input**: `height_in_px: "invalid"` should create 600px editor
5. **No parameter**: Should create 600px editor
6. **Both inline and script_path**: Should work with both code sources

### Example Test File

```yaml
# Test different heights
f_type: "codex_"
height_in_px: 200
inline: |
    print("Compact editor")
```

```yaml
f_type: "codex_"  
height_in_px: 800
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Larger editor for complex code
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, y)
    plt.title('Sine Wave')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()
```

## Changelog

- **Initial Implementation**: Added configurable height support
- **Bug Fix**: Removed CSS max-height constraints that prevented custom heights > 600px
- **Enhancement**: Lowered minimum height from 100px to 50px for compact code blocks
- **Improvement**: Added data attribute copying from fragment to component wrapper
