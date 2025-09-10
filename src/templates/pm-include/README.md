# PM-Include: Reusable PM Rendering System

This folder contains reusable templates and utilities for rendering PM (pedagogical markdown) content anywhere in your application.

## 🎯 Philosophy

The PM-Include system follows DRY (Don't Repeat Yourself) principles by providing:
- **Reusable templates** that can be included in any view
- **A context service** that handles all PM loading logic
- **Minimal boilerplate** for adding PM content to any route

## 📁 Structure

```
pm-include/
├── render-full.html              # Complete PM rendering with TOC, debug, etc.
├── render-fragments-only.html    # Just the PM fragments, no wrapper
├── render-with-wrapper.html      # PM with customizable wrapper
├── head-resources.html           # All CSS/JS resources needed for PM
└── examples/                     # Example usage templates
    ├── product-page-with-pm.html
    ├── custom-pm-layout.html
    └── dashboard-multi-pm.html
```

## 🚀 Quick Start

### 1. Simple PM Rendering in Any Route

```python
from src.core.pm.services.pm_context_service import get_pm_context

@router.get("/my-page")
async def my_page(request: Request):
    # Load PM with one line
    pm_context = get_pm_context("pms/myproduct/intro.md", product_name="myproduct")
    
    context = {
        "request": request,
        **pm_context  # Includes pm, pm_json, product_settings, etc.
    }
    
    # Use the refactored template
    return templates.TemplateResponse("pm/index-refactored.html", context)
```

### 2. Embed PM in Existing Page

In your template:

```jinja
{% extends "base/main-alt.html" %}

{% block extra_head %}
  {# Include PM resources #}
  {% include "pm-include/head-resources.html" %}
{% endblock %}

{% block content %}
  <div class="my-page">
    <h1>My Page Title</h1>
    
    {# Render PM content without wrapper #}
    {% include "pm-include/render-fragments-only.html" %}
    
    <div>Other content...</div>
  </div>
{% endblock %}
```

### 3. PM with Custom Wrapper

```jinja
{% block content %}
  {% with wrapper_class="my-custom-wrapper", show_toc=false %}
    {% include "pm-include/render-with-wrapper.html" %}
  {% endwith %}
{% endblock %}
```

## 📚 Templates Reference

### `render-full.html`
Complete PM rendering with all features.

**Required context:**
- `pm`: Parsed PM object
- `request`: Request object

**Optional context:**
- `debug`: Enable debug mode
- `product_settings`: Product configuration
- `product_name`: Product identifier

### `render-fragments-only.html`
Renders only the PM fragments without any wrapper.

**Required context:**
- `pm`: Parsed PM object with fragments

### `render-with-wrapper.html`
PM rendering with customizable wrapper.

**Required context:**
- `pm`: Parsed PM object
- `request`: Request object

**Optional parameters (via `with` statement):**
- `wrapper_class`: Custom CSS classes for wrapper
- `show_toc`: Show TOC sidebar (default: true)
- `show_debug`: Show debug info (default: follows debug flag)
- `container_width`: Container width class

### `head-resources.html`
All CSS and JS resources needed for PM rendering.

**Required context:**
- `request`: Request object

**Optional context:**
- `include_mathlive`: Include MathLive (default: true)
- `include_codemirror`: Include CodeMirror (default: true)
- `pm_metatags`: PM-specific metatags
- `product_settings`: Product settings
- `origin`: Origin path for canonical URL

## 🔧 Python Service: PMContextService

The `PMContextService` handles all PM loading and context preparation:

```python
from src.core.pm.services.pm_context_service import PMContextService

# Load from file path
context = PMContextService.load_pm_from_file(
    pm_path="pms/corsica/intro.md",
    product_name="corsica",
    debug=True
)

# Load from origin (auto-detects product)
context = PMContextService.load_pm_from_origin(
    origin="corsica/intro.md",
    debug=False
)

# Quick helper function
from src.core.pm.services.pm_context_service import get_pm_context
context = get_pm_context("pms/pyly/functions.md", product_name="pyly")
```

### Context Variables Provided

The service returns a dictionary with:
- `pm`: Parsed PM object
- `pm_json`: JSON representation for debugging
- `pm_metatags`: Extracted metatags from PM metadata
- `product_name`: Product identifier
- `product_settings`: Full product configuration
- `product_title`: Product title
- `product_description`: Product description
- `product_backend_settings`: Backend settings
- `is_product_enabled`: Product enabled flag
- `page`: Page metadata with title
- `debug`: Debug flag
- `origin`: Origin path

## 💡 Use Cases

### Multiple PMs on One Page

```python
@router.get("/dashboard")
async def dashboard(request: Request):
    intro = get_pm_context("pms/intro.md")
    tutorial = get_pm_context("pms/tutorial.md")
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "intro_pm": intro["pm"],
        "tutorial_pm": tutorial["pm"],
    })
```

Template:
```jinja
{% set pm = intro_pm %}
{% include "pm-include/render-fragments-only.html" %}

{% set pm = tutorial_pm %}
{% include "pm-include/render-fragments-only.html" %}
```

### Dynamic PM Selection

```python
@router.get("/learn/{topic}/{level}")
async def learning_path(request: Request, topic: str, level: str):
    pm_map = {
        "python": {
            "beginner": "pms/python/intro.md",
            "advanced": "pms/python/advanced.md"
        }
    }
    
    pm_path = pm_map[topic][level]
    context = get_pm_context(pm_path, product_name=topic)
    
    return templates.TemplateResponse("learning.html", {
        "request": request,
        **context
    })
```

### API Endpoint for PM Data

```python
@router.get("/api/pm/{origin:path}")
async def get_pm_data(origin: str):
    context = PMContextService.load_pm_from_origin(origin)
    return {
        "title": context["pm"].title,
        "fragments_count": len(context["pm"].fragments),
        "metatags": context["pm_metatags"]
    }
```

## 🎨 Customization

### Custom Fragment Rendering

Create your own fragment filter:

```jinja
{# Render only code fragments #}
{% for fragment in pm.fragments %}
  {% if fragment.f_type.value in ['code_', 'codex_'] %}
    {% set fragment_index = loop.index0 %}
    {% include 'pm/fragments/' ~ fragment.f_type.value ~ '.html' %}
  {% endif %}
{% endfor %}
```

### Custom Styles

Override PM styles in your template:

```jinja
{% block extra_head %}
  {% include "pm-include/head-resources.html" %}
  <style>
    .pm-container { 
      max-width: 1200px; 
    }
    .fragment-wrapper {
      margin: 2rem 0;
    }
  </style>
{% endblock %}
```

## 🔍 Best Practices

1. **Always include head resources** when rendering PM content
2. **Use the context service** instead of manually loading PMs
3. **Choose the right template**:
   - `render-full.html` for standalone PM pages
   - `render-fragments-only.html` for embedding in existing layouts
   - `render-with-wrapper.html` for custom styling needs
4. **Handle missing PMs gracefully** with try/except blocks
5. **Cache PM contexts** if loading the same PM multiple times

## 📖 Examples

See the `examples/` folder for complete working examples:
- `product-page-with-pm.html` - Product page with embedded PM
- `custom-pm-layout.html` - PM with custom layout
- `dashboard-multi-pm.html` - Dashboard with multiple PMs

Also check `src/core/router_pm_examples.py` for Python route examples.
