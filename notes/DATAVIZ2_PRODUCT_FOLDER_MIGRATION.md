# DataViz2 Product Folder Migration

## Summary

Successfully migrated DataViz2 assets to a centralized product folder structure without deleting any existing files.

## New Structure

```
src/static/products/dataviz2/
├── README.md
├── css/
│   ├── dataviz2.css    # NEW: Product-specific styles
│   ├── pm.css          # Copied from /static/core/css/
│   └── toc.css         # Copied from /static/core/css/
└── js/
    ├── bokeh-detector.js  # Copied from /static/js/pm/
    └── main.js            # Copied from /static/js/products/dataviz2/
```

## Files Copied (Not Deleted)

The following files were COPIED to the new location (originals remain):

1. **JavaScript Files:**
   - `src/static/js/products/dataviz2/main.js` → `src/static/products/dataviz2/js/main.js`
   - `src/static/js/pm/bokeh-detector.js` → `src/static/products/dataviz2/js/bokeh-detector.js`

2. **CSS Files:**
   - `src/static/core/css/pm.css` → `src/static/products/dataviz2/css/pm.css`
   - `src/static/core/css/toc.css` → `src/static/products/dataviz2/css/toc.css`

3. **New Files Created:**
   - `src/static/products/dataviz2/css/dataviz2.css` - Product-specific styles
   - `src/static/products/dataviz2/README.md` - Documentation

## Configuration Updates

Updated `products/04_dataviz2.yml`:

```yaml
backend_settings:
  js_dependencies:
    - "/static/products/dataviz2/js/bokeh-detector.js"  # Updated path
    - "/static/products/dataviz2/js/main.js"           # Updated path
  css_dependencies:
    - "/static/products/dataviz2/css/pm.css"           # Updated path
    - "/static/products/dataviz2/css/toc.css"          # Updated path
    - "/static/products/dataviz2/css/dataviz2.css"     # New file
```

## Benefits of This Structure

1. **Self-contained Product:** All DataViz2 assets in one folder
2. **Easy Management:** Single location for all product files
3. **Clear Organization:** Separate js/ and css/ subfolders
4. **Product Isolation:** Each product can have its own complete set of assets
5. **No Breaking Changes:** Original files remain, ensuring backward compatibility

## Verification

Confirmed working by checking rendered HTML:
```bash
curl -s "http://127.0.0.1:5001/pm/dataviz2/00_plan.md" | grep dataviz2
```

Output shows correct paths:
- `/static/products/dataviz2/css/pm.css`
- `/static/products/dataviz2/css/toc.css`
- `/static/products/dataviz2/css/dataviz2.css`
- `/static/products/dataviz2/js/bokeh-detector.js`
- `/static/products/dataviz2/js/main.js`

## Future Products

This structure can be replicated for other products:
```
src/static/products/
├── dataviz2/
│   ├── js/
│   └── css/
├── nagini/
│   ├── js/
│   └── css/
├── sujets0/
│   ├── js/
│   └── css/
└── ...
```

## Migration Date

October 1, 2025
