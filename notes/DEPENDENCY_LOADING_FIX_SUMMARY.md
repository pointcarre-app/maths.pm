# Product Dependencies Loading Fix Summary

## Problem Identified

The dependency loading system had three conflicting approaches:

1. **PM metadata dependencies** - `pm.js_dependencies` and `pm.css_dependencies` loaded from individual PM markdown files
2. **Product backend_settings arrays** - `backend_settings.js_dependencies` and `backend_settings.css_dependencies` from product YAML files  
3. **Individual backend_settings items** - Expecting `setting_value.js_url` and `setting_value.css_url` properties

## Issues Fixed

### 1. main-alt.html (Lines 90-123)
**Problem:** Auto-loader expected individual `js_url/css_url` properties, not arrays
**Solution:** Updated to handle both array formats (`js_dependencies`, `css_dependencies`) and legacy individual items

### 2. pm/index.html (Lines 25-37)
**Problem:** Template loaded dependencies from PM object instead of product settings
**Solution:** Modified to load from `product_settings.product.backend_settings` first, then fall back to PM metadata

### 3. pm/index.html (Line 71)
**Problem:** Bug that printed CSS dependencies as raw text
**Solution:** Removed the erroneous `{{ pm.css_dependencies }}` line

### 4. runtime-init.html
**Problem:** Duplicate loading of JS dependencies
**Solution:** Removed dependency loading since it's now handled in the head section

## New Loading Order

Dependencies are now loaded in this priority order:

1. **Product-level dependencies** (from product YAML `backend_settings`)
   - CSS: `product_settings.product.backend_settings.css_dependencies`
   - JS: `product_settings.product.backend_settings.js_dependencies`

2. **PM-level dependencies** (from PM markdown metadata)  
   - CSS: `pm.css_dependencies`
   - JS: `pm.js_dependencies`

## Configuration Example (products/04_dataviz2.yml)

```yaml
backend_settings:
  js_dependencies:
    - "/static/js/pm/bokeh-detector.js"
    - "/static/js/products/dataviz2/main.js"
  css_dependencies:
    - "/static/css/pm.css"
    - "/static/css/toc.css"
```

## Benefits

1. **Clear hierarchy** - Product settings take precedence over PM settings
2. **No duplicates** - Dependencies are loaded once in the appropriate location
3. **Backward compatibility** - Still supports legacy `js_url/css_url` format
4. **Centralized configuration** - Product dependencies can be managed in YAML files

## Testing

Verified that dataviz2 product correctly loads:
- 2 JS dependencies: bokeh-detector.js, dataviz2/main.js
- 2 CSS dependencies: pm.css, toc.css

All dependencies are properly injected into templates and accessible via `product_settings.product.backend_settings`.
