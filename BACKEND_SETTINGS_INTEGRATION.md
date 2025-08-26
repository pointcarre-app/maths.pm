# Backend Settings Integration

## Overview
This document explains how backend settings from the YAML configuration are loaded and used in the JavaScript application.

## Data Flow

### 1. YAML Configuration (`products/01_sujets0.yml`)
```yaml
backend_settings:
  nagini:
    endpoint: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/"
    js_url: "https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js"
    pyodide_worker_url: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js"
```

### 2. HTML Data Attributes
The backend settings are rendered as HTML data attributes on a settings element:
```html
<div id="products-settings" 
     data-sujets0="{&quot;nagini&quot;: {&quot;endpoint&quot;: &quot;...&quot;, &quot;js_url&quot;: &quot;...&quot;, &quot;pyodide_worker_url&quot;: &quot;...&quot;}}"
     data-nagini="{...}"
     data-jupyterlite="{...}"
     data-examples="{...}">
</div>
```

### 3. JavaScript Loading (`sujets0-main.js`)

## Available Functions

### `loadBackendSettings()`
Loads settings from the `data-sujets0` attribute specifically.

**Returns**: Object with backend settings or null if not found

**Console Output**:
- ✅ Backend settings loaded successfully
- 📦 Nagini Configuration details

### `getAllProductSettings()`
Loads and parses ALL data attributes from the products-settings element.

**Returns**: Object with all parsed data attributes

**Console Output**:
- ✅ Parsed data-{attributeName} for each attribute

## Usage Examples

### In Browser Console

```javascript
// Load settings for sujets0 specifically
const settings = loadBackendSettings();
console.log(settings);

// Get all product settings
const allSettings = getAllProductSettings();
console.log(allSettings);

// Access current loaded settings
const current = getBackendSettings();
console.log(current);
```

### Expected Console Output

When the page loads, you'll see:
```
✅ Backend settings loaded successfully: {nagini: {...}}
📦 Nagini Configuration: {
    endpoint: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/",
    js_url: "https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js",
    pyodide_worker_url: "https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js"
}
🔧 Using Nagini URLs from backend settings
📥 Loading Nagini from: https://esm.sh/gh/pointcarre-app/nagini@v0.0.21/src/nagini.js?bundle
🔨 Creating Nagini manager with worker: https://cdn.jsdelivr.net/gh/pointcarre-app/nagini@v0.0.21/src/pyodide/worker/worker-dist.js
```

### Manual Testing

To test if everything is working:

1. **Check if settings element exists**:
```javascript
document.getElementById('products-settings')
```

2. **Check data attributes**:
```javascript
const el = document.getElementById('products-settings');
console.log(el.dataset.sujets0);  // Raw JSON string
```

3. **Load and verify settings**:
```javascript
const settings = loadBackendSettings();
if (settings?.nagini) {
    console.log('Nagini endpoint:', settings.nagini.endpoint);
    console.log('Nagini JS URL:', settings.nagini.js_url);
    console.log('Worker URL:', settings.nagini.pyodide_worker_url);
}
```

4. **Check all available settings**:
```javascript
const all = getAllProductSettings();
Object.keys(all).forEach(key => {
    console.log(`Available setting: data-${key}`);
});
```

## Integration Points

### Automatic Loading
The settings are automatically loaded when `loadNaginiAndInitialize()` is called during initialization:

1. Settings are loaded from data attributes
2. If found, they override default URLs
3. Nagini is loaded with the configured URLs
4. Falls back to defaults if settings are not found

### Fallback Behavior
If settings are not found or fail to parse:
- Default URLs are used (hardcoded in the JS)
- Warning messages are logged to console
- Application continues to function normally

## Debugging

### Common Issues

1. **Settings element not found**:
   - Check if `<div id="products-settings">` exists in the HTML
   - Verify the element is present when the script runs

2. **Data attribute missing**:
   - Check if `data-sujets0` attribute is present
   - Verify the backend is rendering the attribute correctly

3. **JSON parsing errors**:
   - Check for malformed JSON in the data attribute
   - HTML entities (`&quot;`) are automatically handled

### Debug Commands

```javascript
// Check what's loaded
console.log('Current settings:', getBackendSettings());

// Force reload settings
const fresh = loadBackendSettings();
console.log('Fresh load:', fresh);

// Check raw attribute
const raw = document.getElementById('products-settings')?.getAttribute('data-sujets0');
console.log('Raw attribute:', raw);

// Parse manually
try {
    const parsed = JSON.parse(raw);
    console.log('Manual parse:', parsed);
} catch (e) {
    console.error('Parse error:', e);
}
```

## Best Practices

1. **Always check for null** when using settings
2. **Provide fallback values** for critical URLs
3. **Log configuration usage** for debugging
4. **Use optional chaining** (`?.`) for safe access
5. **Keep settings structure consistent** between YAML and JS
