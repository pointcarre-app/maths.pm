# Dynamic PM Loading from Jinja Templates

This document explains how to load and render PM (Pedagogical Markdown) files dynamically from within Jinja templates, without any Python preprocessing.

## ✨ Key Feature

You can now load PM files directly from Jinja templates using the `load_pm()` function, which means:
- No need to load PM in Python routes
- Dynamic file selection based on template logic
- Simplified code with better separation of concerns

## 🚀 Quick Start

### Basic Usage

```jinja
{# Load and render a PM file #}
{% with pm_file="corsica/intro.md" %}
  {% include "pm-include/render-dynamic-simple.html" %}
{% endwith %}
```

### With Product Settings

```jinja
{# Load with product-specific settings #}
{% with pm_file="corsica/a_troiz_geo.md", product_name="corsica" %}
  {% include "pm-include/render-dynamic.html" %}
{% endwith %}
```

### Just Fragments

```jinja
{# Render only the fragments without wrapper #}
{% include "pm-include/render-dynamic-fragments.html" with pm_file="pyly/01_premiers_pas.md" %}
```

## 📚 Available Templates

### 1. `render-dynamic.html`
Full PM rendering with TOC, debug options, and wrapper.

**Variables:**
- `pm_file` (required): Path to PM file relative to `pms/`
- `product_name`: Product name for settings
- `show_toc`: Show table of contents (default: true)
- `show_debug`: Show debug info (default: false)
- `wrapper_class`: Custom CSS class for wrapper

### 2. `render-dynamic-simple.html`
Simplified rendering with basic wrapper.

**Variables:**
- `pm_file` (required): Path to PM file

### 3. `render-dynamic-fragments.html`
Just the fragments, no wrapper or extras.

**Variables:**
- `pm_file` (required): Path to PM file
- `product_name`: Product name for settings
- `show_error`: Show errors (default: true)

## 🔧 How It Works

1. **Template Helper Function**: The `load_pm()` function is registered as a Jinja global
2. **Dynamic Loading**: When called from a template, it loads and parses the PM file
3. **Context Creation**: Returns a context dictionary with the parsed PM and metadata
4. **Error Handling**: Gracefully handles missing files with error messages

## 💡 Examples

### Dynamic File Selection

```jinja
{# Select PM based on variable #}
{% set topic = "python" %}
{% set level = "beginner" %}

{% if topic == "python" and level == "beginner" %}
  {% set pm_file = "pyly/01_premiers_pas.md" %}
{% elif topic == "python" and level == "advanced" %}
  {% set pm_file = "pyly/advanced.md" %}
{% else %}
  {% set pm_file = "examples/intro.md" %}
{% endif %}

{% include "pm-include/render-dynamic.html" %}
```

### Multiple PM Files

```jinja
{# Load multiple PM files in a grid #}
<div class="grid grid-cols-2 gap-4">
  <div>
    {% with pm_file="corsica/intro.md" %}
      {% include "pm-include/render-dynamic-fragments.html" %}
    {% endwith %}
  </div>
  <div>
    {% with pm_file="pyly/intro.md" %}
      {% include "pm-include/render-dynamic-fragments.html" %}
    {% endwith %}
  </div>
</div>
```

### Direct Function Call

```jinja
{# Call load_pm directly for custom rendering #}
{% set pm_context = load_pm("examples/tutorial.md", "examples", false) %}

{% if pm_context.pm_loaded %}
  <h1>{{ pm_context.pm.title }}</h1>
  <p>Fragments: {{ pm_context.pm.fragments|length }}</p>
  
  {# Custom fragment rendering #}
  {% for fragment in pm_context.pm.fragments[:5] %}
    {# Render first 5 fragments only #}
    ...
  {% endfor %}
{% endif %}
```

### Error Handling

```jinja
{# Handle errors gracefully #}
{% set pm_context = load_pm(user_selected_file) %}

{% if pm_context.pm_loaded %}
  {# Render PM content #}
  {% set pm = pm_context.pm %}
  {% include 'pm/includes/fragments-renderer.html' %}
{% else %}
  <div class="alert alert-warning">
    <p>Could not load the requested content.</p>
    <p>Error: {{ pm_context.pm_error }}</p>
    <a href="/default-content" class="btn btn-sm">View Default Content</a>
  </div>
{% endif %}
```

## 🎯 Use Cases

### 1. Documentation Pages
Load documentation dynamically based on URL parameters:

```python
# Route
@router.get("/docs/{category}/{page}")
async def docs(request: Request, category: str, page: str):
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "category": category,
        "page": page
    })
```

```jinja
{# Template: docs.html #}
{% set pm_file = category ~ "/" ~ page ~ ".md" %}
{% include "pm-include/render-dynamic.html" %}
```

### 2. Learning Paths
Select content based on user progress:

```jinja
{% if user.level == "beginner" %}
  {% set pm_file = "tutorials/beginner/" ~ topic ~ ".md" %}
{% elif user.level == "intermediate" %}
  {% set pm_file = "tutorials/intermediate/" ~ topic ~ ".md" %}
{% else %}
  {% set pm_file = "tutorials/advanced/" ~ topic ~ ".md" %}
{% endif %}

{% include "pm-include/render-dynamic.html" with product_name="tutorials" %}
```

### 3. A/B Testing
Show different content versions:

```jinja
{% if user.experiment_group == "A" %}
  {% set pm_file = "content/version_a.md" %}
{% else %}
  {% set pm_file = "content/version_b.md" %}
{% endif %}

{% include "pm-include/render-dynamic.html" %}
```

## 🔍 Debugging

To debug PM loading issues:

1. **Check Function Availability**:
```jinja
{% if load_pm %}
  <p>✅ load_pm function is available</p>
{% else %}
  <p>❌ load_pm function NOT available</p>
{% endif %}
```

2. **Enable Debug Mode**:
```jinja
{% with pm_file="test.md", show_debug=true %}
  {% include "pm-include/render-dynamic.html" %}
{% endwith %}
```

3. **Check Context**:
```jinja
{% set pm_context = load_pm("test.md") %}
<pre>{{ pm_context | tojson(indent=2) }}</pre>
```

## 📝 Notes

- PM files are loaded relative to the `pms/` directory by default
- The `load_pm()` function is registered when the app starts
- Templates are cached, but PM content is loaded fresh each time
- Error messages include the attempted file path for debugging

## 🔗 Working Examples

Visit these routes to see dynamic PM loading in action:

- `/test-dynamic-pm` - Basic functionality test
- `/simple-dynamic-demo` - Simple examples with error handling
- `/dynamic-pm-demo` - Full-featured demonstration (if fixed)

## 🚦 Migration from Static Loading

Before (Python route):
```python
pm_context = get_pm_context("pms/example.md")
context = {"request": request, **pm_context}
return templates.TemplateResponse("template.html", context)
```

After (Template only):
```python
# Python route - much simpler!
return templates.TemplateResponse("template.html", {"request": request})
```

```jinja
{# Template - loads PM dynamically #}
{% include "pm-include/render-dynamic.html" with pm_file="example.md" %}
```

This approach keeps your Python routes clean and moves content selection logic to the templates where it belongs!
