# PM Include Templates - Comprehensive Guide

## Overview

The PM Include template system provides a modular way to render Pedagogical Message (PM) content dynamically in Jinja2 templates. This guide documents the complete system, common issues, and best practices.

## Architecture

### Core Templates

1. **`pm-include/render-dynamic.html`**
   - Main template for full PM rendering with all features
   - Includes TOC, fragments, debug info, and runtime initialization
   - Uses the `load_pm()` Jinja function to dynamically load PM files

2. **`pm-include/render-dynamic-fragments.html`**
   - Lightweight template for rendering only PM fragments
   - No TOC, no wrapper, minimal styling
   - Ideal for embedding PM content inline

3. **`pm-include/head-resources.html`**
   - Consolidates all required CSS and JavaScript resources
   - Includes MathLive, CodeMirror, and PM-specific styles

4. **`pm-include/render-full.html`**
   - Complete drop-in replacement for standard PM page content
   - Includes everything needed for a full PM page

### Supporting Templates (in `pm/includes/`)

- **`toc-sidebar.html`** - Table of Contents sidebar
- **`fragments-renderer.html`** - Renders PM fragments with radio buttons
- **`runtime-init.html`** - JavaScript initialization for PM features
- **`debug-section.html`** - Debug information display
- **`product-warning.html`** - Product-specific warning messages
- **`metatags.html`** - SEO and social media meta tags

## Common Issues and Solutions

### 1. Duplicate Table of Contents (TOC)

**Problem**: TOC appears twice on the page

**Cause**: Both the parent template and `render-dynamic.html` include the TOC

**Solutions**:
```jinja
{# Option 1: Disable TOC in render-dynamic #}
{% set show_toc = false %}
{% include "pm-include/render-dynamic.html" %}

{# Option 2: Use fragments-only template #}
{% include "pm-include/render-dynamic-fragments.html" %}
```

### 2. Missing Radio Button Transitions

**Problem**: Radio buttons don't have smooth transitions or animations

**Cause**: Missing PM runtime JavaScript initialization

**Solution**: Ensure `runtime-init.html` is included:
```jinja
{% include 'pm/includes/runtime-init.html' %}
```

### 3. Jinja2 Template Syntax Errors

**Problem**: `TemplateSyntaxError: expected token 'end of statement block', got 'with'`

**Cause**: Incorrect syntax for passing variables to included templates

**Wrong**:
```jinja
{% include "template.html" with var=value %}
```

**Correct**:
```jinja
{# Set variables before include #}
{% set pm_file = "path/to/file.md" %}
{% set product_name = "corsica" %}
{% include "pm-include/render-dynamic.html" %}
```

### 4. PM Content Not Loading

**Problem**: PM file fails to load or shows error

**Common Causes**:
- Incorrect file path (must be relative to `pms/` directory)
- Missing product configuration
- File doesn't exist

**Debugging**:
```jinja
{# Enable debug mode to see detailed error info #}
{% set show_debug = true %}
{% include "pm-include/render-dynamic.html" %}
```

## Usage Patterns

### Basic PM Rendering

```jinja
{% extends "base/main-alt.html" %}

{% block extra_head %}
  {% include "pm-include/head-resources.html" %}
{% endblock %}

{% block content %}
  {% set pm_file = "corsica/intro.md" %}
  {% set product_name = "corsica" %}
  {% include "pm-include/render-dynamic.html" %}
{% endblock %}
```

### Multiple PM Files in Cards

```jinja
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  <div class="card">
    {% set pm_file = "pyly/basics.md" %}
    {% set product_name = "pyly" %}
    {% include "pm-include/render-dynamic-fragments.html" %}
  </div>
  
  <div class="card">
    {% set pm_file = "nagini/intro.md" %}
    {% set product_name = "nagini" %}
    {% include "pm-include/render-dynamic-fragments.html" %}
  </div>
</div>
```

### Conditional PM Loading

```jinja
{% set selected_topic = request.args.get('topic', 'default') %}
{% set pm_file = selected_topic ~ "/content.md" %}

{% if pm_file %}
  {% include "pm-include/render-dynamic.html" %}
{% else %}
  <p>No content selected</p>
{% endif %}
```

### Inline PM Fragments

```jinja
<article class="prose">
  <h1>My Article</h1>
  <p>Introduction text...</p>
  
  {# Embed PM content inline #}
  <div class="bg-base-200 p-4 rounded">
    {% set pm_file = "examples/snippet.md" %}
    {% include "pm-include/render-dynamic-fragments.html" %}
  </div>
  
  <p>Conclusion text...</p>
</article>
```

## Variable Reference

### For `render-dynamic.html`

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `pm_file` | string | **required** | Path to PM file relative to `pms/` |
| `product_name` | string | `none` | Product identifier for settings |
| `show_toc` | boolean | `true` | Whether to show Table of Contents |
| `show_debug` | boolean | `false` | Display debug information |
| `wrapper_class` | string | `none` | Custom CSS class for wrapper div |

### For `render-dynamic-fragments.html`

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `pm_file` | string | **required** | Path to PM file relative to `pms/` |
| `product_name` | string | `none` | Product identifier for settings |

## Best Practices

### 1. Variable Setting

Always set variables before the include statement:
```jinja
{# Good #}
{% set pm_file = "path/to/file.md" %}
{% set show_toc = false %}
{% include "pm-include/render-dynamic.html" %}

{# Bad - will cause syntax error #}
{% include "pm-include/render-dynamic.html" with pm_file="path/to/file.md" %}
```

### 2. TOC Management

- Use `show_toc=false` when the parent template already has a TOC
- Use `render-dynamic-fragments.html` for content without TOC
- Only one TOC should be present per page

### 3. Resource Loading

Include head resources once per page:
```jinja
{% block extra_head %}
  {% include "pm-include/head-resources.html" %}
{% endblock %}
```

### 4. Error Handling

Always handle potential PM loading failures:
```jinja
{% set pm_context = load_pm(pm_file) %}
{% if pm_context.pm_loaded %}
  {# Render content #}
{% else %}
  <div class="alert alert-error">
    Failed to load: {{ pm_context.pm_error }}
  </div>
{% endif %}
```

### 5. Performance Considerations

- Use `render-dynamic-fragments.html` for lightweight embedding
- Enable debug mode only in development
- Cache PM content when possible using template caching

## JavaScript Runtime Features

The PM runtime (`runtime-init.html`) provides:

1. **Radio Button Transitions**: Smooth animations when switching between fragments
2. **Code Highlighting**: Automatic syntax highlighting for code blocks
3. **LaTeX Rendering**: MathLive integration for mathematical expressions
4. **Interactive Elements**: Various PM-specific interactive components
5. **Fragment Navigation**: Keyboard shortcuts and navigation aids

## Debugging Tips

### Enable Debug Mode

```jinja
{% set show_debug = true %}
{% include "pm-include/render-dynamic.html" %}
```

This displays:
- PM loading status
- Product settings
- Fragment count
- TOC structure
- Any loading errors

### Check Browser Console

The PM runtime logs useful information:
```javascript
console.log('PM loaded:', pm_json);
console.log('Product settings:', product_settings);
```

### Verify File Paths

PM files must be relative to the `pms/` directory:
- ✅ `"corsica/intro.md"` → `pms/corsica/intro.md`
- ❌ `"pms/corsica/intro.md"` → `pms/pms/corsica/intro.md`
- ❌ `"/corsica/intro.md"` → Invalid absolute path

## Migration Guide

### From Standard PM Template to PM-Include

**Before** (standard PM page):
```jinja
{% extends "base/main-alt.html" %}
{% block content %}
  <!-- Complex PM rendering logic -->
  {% include "pm/includes/toc-sidebar.html" %}
  <div class="pm-container">
    <!-- More complex logic -->
  </div>
{% endblock %}
```

**After** (using PM-include):
```jinja
{% extends "base/main-alt.html" %}
{% block extra_head %}
  {% include "pm-include/head-resources.html" %}
{% endblock %}
{% block content %}
  {% include "pm-include/render-full.html" %}
{% endblock %}
```

## Troubleshooting Checklist

- [ ] Is `pm_file` path correct and relative to `pms/`?
- [ ] Are variables set before the include statement?
- [ ] Is only one TOC being rendered?
- [ ] Is `runtime-init.html` included for interactive features?
- [ ] Are head resources included in the `extra_head` block?
- [ ] Is the product configuration available if needed?
- [ ] Check browser console for JavaScript errors
- [ ] Enable debug mode to see detailed error information
- [ ] Clear browser cache if seeing outdated behavior
- [ ] Verify the PM file exists and is valid Markdown

## Related Documentation

- [PM Routes Deployment Fix](PM_ROUTES_DEPLOYMENT_FIX.md)
- [Product Metatags Implementation](PRODUCT_METATAGS_IMPLEMENTATION.md)
- [Settings Documentation](SETTINGS_DOCUMENTATION.md)

## Version History

- **v1.0** (2024): Initial PM-include template system
- **v1.1**: Added dynamic PM loading with `load_pm()` function
- **v1.2**: Fixed Jinja2 syntax issues and duplicate TOC problems
- **v1.3**: Added comprehensive error handling and debug mode

---

*Last updated: September 2025*
