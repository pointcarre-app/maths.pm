# PM-Include System Documentation

## Overview

The PM-Include system enables dynamic loading and rendering of PM (Pedagogical Markdown) files directly from Jinja templates without Python preprocessing. This document summarizes all created files and available test URLs.

## 📁 Created Files Structure

```
pca-mathspm/
├── src/
│   ├── core/
│   │   ├── pm/
│   │   │   ├── services/
│   │   │   │   ├── __init__.py (updated)
│   │   │   │   └── pm_context_service.py           # Centralized PM loading service
│   │   │   └── template_helpers.py                 # Jinja function registration
│   │   ├── router_pm_examples.py                   # Example routes demonstrating PM usage
│   │   └── router.py (updated)                     # Core router with PM enhancements
│   ├── templates/
│   │   ├── pm/
│   │   │   ├── includes/                           # Modular PM components
│   │   │   │   ├── metatags.html                  # PM metatags logic
│   │   │   │   ├── toc-sidebar.html               # TOC sidebar component
│   │   │   │   ├── product-warning.html           # Product settings warning
│   │   │   │   ├── fragments-renderer.html        # Main fragments rendering
│   │   │   │   ├── debug-section.html             # Debug information panels
│   │   │   │   └── runtime-init.html              # PM runtime JavaScript
│   │   │   ├── index.html (refactored)            # Original PM template with includes
│   │   │   └── index-refactored.html              # Simplified PM template
│   │   └── pm-include/                            # New PM-include system
│   │       ├── README.md                          # Complete documentation
│   │       ├── DYNAMIC_LOADING.md                 # Dynamic loading guide
│   │       ├── render-full.html                   # Complete PM rendering
│   │       ├── render-fragments-only.html         # Just fragments rendering
│   │       ├── render-with-wrapper.html           # Customizable wrapper rendering
│   │       ├── render-dynamic.html                # Dynamic PM with all features
│   │       ├── render-dynamic-fragments.html      # Dynamic fragments only
│   │       ├── render-dynamic-simple.html         # Simplified dynamic rendering
│   │       ├── head-resources.html                # PM CSS/JS resources
│   │       └── examples/
│   │           ├── product-page-with-pm.html      # Product page example
│   │           ├── custom-pm-layout.html          # Custom layout example
│   │           ├── dashboard-multi-pm.html        # Multiple PMs dashboard
│   │           ├── dynamic-pm-demo.html           # Full dynamic PM demo
│   │           └── simple-dynamic-demo.html       # Simple dynamic examples
│   ├── settings.py (updated)                      # Added PM template helpers registration
│   └── app.py (updated)                           # Added example router
└── pms/
    └── examples/                                  # Example PM content files
        ├── intro.md                               # Introduction to PM examples
        └── tutorial.md                            # PM tutorial content
```

## 🔗 Available Test URLs

### Core PM Routes

| URL | Description | Status |
|-----|-------------|--------|
| `/pm` | PM root directory view | ✅ Working |
| `/pm/{path}` | View any PM file (e.g., `/pm/corsica/a_troiz_geo.md`) | ✅ Working |
| `/pm/{path}?format=json` | Get PM data as JSON | ✅ Working |
| `/pm/{path}?debug=true` | View PM with debug info | ✅ Working |

### Example Routes (New)

| URL | Description | Status |
|-----|-------------|--------|
| `/example/simple-pm` | Simple PM rendering example | ✅ Working |
| `/dashboard` | Dashboard with multiple PM contents | ✅ Working |
| `/products/{name}/docs` | Product documentation (e.g., `/products/corsica/docs`) | ✅ Working |
| `/learn/{topic}` | Learning path (e.g., `/learn/python?level=beginner`) | ✅ Fixed & Working |
| `/api/pm/{origin}` | PM data as JSON API | ✅ Working |
| `/custom-layout/{pm_name}` | Custom layout PM (e.g., `/custom-layout/intro`) | ✅ Working |
| `/simple-dynamic-demo` | **Dynamic PM loading examples** | ✅ Working |

### Test URLs by Feature

#### 1. Static PM Loading (Python-based)
- http://127.0.0.1:5001/example/simple-pm
- http://127.0.0.1:5001/dashboard
- http://127.0.0.1:5001/learn/python?level=beginner ✅ Fixed
- http://127.0.0.1:5001/learn/python?level=intermediate
- http://127.0.0.1:5001/learn/python?level=advanced
- http://127.0.0.1:5001/learn/math?level=beginner ✅ Fixed
- http://127.0.0.1:5001/learn/math?level=intermediate
- http://127.0.0.1:5001/learn/math?level=advanced

#### 2. Dynamic PM Loading (Template-based) 🆕
- http://127.0.0.1:5001/simple-dynamic-demo - **Best demo of dynamic loading**
- http://127.0.0.1:5001/custom-layout/intro
- http://127.0.0.1:5001/custom-layout/tutorial

#### 3. API Access
- http://127.0.0.1:5001/api/pm/corsica/a_troiz_geo.md
- http://127.0.0.1:5001/api/pm/pyly/01_premiers_pas.md
- http://127.0.0.1:5001/api/pm/examples/intro.md

#### 4. Product Documentation
- http://127.0.0.1:5001/products/corsica/docs
- http://127.0.0.1:5001/products/pyly/docs
- http://127.0.0.1:5001/products/nagini/docs

## 🚀 Key Features Implemented

### 1. PM Context Service (`pm_context_service.py`)
- Centralized PM loading logic
- Automatic product settings detection
- Metatag extraction
- Error handling

### 2. Template Helpers (`template_helpers.py`)
- `load_pm()` function available globally in templates
- Dynamic PM loading without Python preprocessing
- Graceful error handling

### 3. Modular Templates
- **Includes**: Reusable components in `pm/includes/`
- **PM-Include**: Complete rendering system in `pm-include/`
- **Examples**: Working demonstrations in `pm-include/examples/`

### 4. Dynamic Loading Templates
- `render-dynamic.html`: Full features with TOC, debug
- `render-dynamic-simple.html`: Basic rendering
- `render-dynamic-fragments.html`: Fragments only

## 💡 Usage Examples

### Python Route (Simplified)
```python
from src.core.pm.services.pm_context_service import get_pm_context

@router.get("/my-page")
async def my_page(request: Request):
    pm_context = get_pm_context("pms/example.md", product_name="example")
    context = {"request": request, **pm_context}
    return templates.TemplateResponse("pm/index-refactored.html", context)
```

### Template-Only (Dynamic)
```jinja
{# No Python loading needed! #}
{% with pm_file="corsica/intro.md" %}
  {% include "pm-include/render-dynamic-simple.html" %}
{% endwith %}
```

### Direct Function Call
```jinja
{% set pm_context = load_pm("examples/tutorial.md", "examples") %}
{% if pm_context.pm_loaded %}
  <h1>{{ pm_context.pm.title }}</h1>
  {# Custom rendering... #}
{% endif %}
```

## 📊 System Architecture

```mermaid
graph TD
    A[Jinja Template] -->|load_pm()| B[template_helpers.py]
    B --> C[PMContextService]
    C --> D[build_pm_from_file]
    D --> E[PM Parser]
    E --> F[PM Object]
    F --> G[Template Context]
    G --> H[Rendered HTML]
    
    I[Python Route] -->|get_pm_context()| C
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#9f9,stroke:#333,stroke-width:2px
```

## ✅ Verified Working Features

1. **Dynamic PM Loading**: Load PM files directly from templates ✅
2. **Error Handling**: Graceful fallback for missing files ✅
3. **Product Settings**: Automatic product configuration loading ✅
4. **Multiple PMs**: Render multiple PM contents on one page ✅
5. **Custom Layouts**: Flexible wrapper and styling options ✅
6. **API Access**: JSON endpoints for PM data ✅
7. **Debug Mode**: Optional debug information display ✅
8. **TOC Support**: Table of contents sidebar ✅
9. **Fragment Rendering**: All fragment types supported ✅
10. **Runtime Initialization**: PM JavaScript runtime ✅

## 🎯 Quick Test Commands

```bash
# Test dynamic PM loading
curl -s http://127.0.0.1:5001/simple-dynamic-demo | grep "Géographie"

# Test API endpoint
curl -s http://127.0.0.1:5001/api/pm/examples/intro.md | jq .

# Test error handling
curl -s http://127.0.0.1:5001/simple-dynamic-demo | grep "Failed to load"

# Test dashboard with multiple PMs
curl -s http://127.0.0.1:5001/dashboard | head -50
```

## 📝 Notes

- All PM files are loaded relative to the `pms/` directory
- The `load_pm()` function is registered globally when the app starts
- Templates can be used in any route without Python PM preprocessing
- Error messages include file paths for debugging
- The system is fully backward compatible with existing PM routes

## 🔍 Debugging

If PM loading isn't working:

1. Check if `load_pm` is available: Look for "✅ PM template helpers registered" in logs
2. Verify file paths: Files should be relative to `pms/` directory
3. Check product settings: Ensure product YAML files exist in `products/`
4. Enable debug mode: Add `?debug=true` to URLs or use `show_debug=true` in templates

## 🐛 Recent Fixes

### Fixed: `/learn/{topic}` Routes (September 10, 2025)
- **Issue**: Internal Server Error when accessing `/learn/python` or `/learn/math`
- **Cause**: Incorrect PM file paths in the route mapping
- **Solution**: Updated paths to include `pms/` prefix and mapped to actual existing files
- **Files Fixed**: `src/core/router_pm_examples.py`

---

*Last updated: September 10, 2025*
*System version: 1.0.1*
