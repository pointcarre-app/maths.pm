---
title: Fragment Architecture Documentation
description: Architectural decisions and patterns for PM fragment rendering
chapter: Documentation

# Page-specific metatags
title: "Fragment Architecture - PM Fragments System"
description: "Understanding and using the PM fragments architecture for content creation"
keywords: "fragments, PM system, content, architecture, components"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "Fragment Architecture"
og:description: "Understanding and using the PM fragments architecture for content creation"
og:type: "article"
og:url: "https://maths.pm/pm/documentation/fragment_architecture.md"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "Fragment Architecture"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "Architecture, Documentation"
revised: "2025-01-15"
pagename: "Fragment Architecture"

---

# Fragment Architecture Guide

## HTML Structure Pattern

### Consistent Two-Level Architecture

All fragments follow this pattern:

```html
<div class="fragment-wrapper {custom-classes}" data-f_type="{type}">
  <{element} class="fragment {element-specific-classes}" data-f_type="{type}">
    {content}
  </{element}>
</div>
```

### Benefits of This Approach

1. **Dual-level data attributes**: Both wrapper and inner element have `data-f_type`
   - Enables flexible CSS targeting: `.fragment[data-f_type="h1_"]` or `.fragment-wrapper[data-f_type="h1_"]`
   - Better JavaScript selectors for different use cases
   - Clearer debugging in browser DevTools

2. **Wrapper for layout control**: 
   - Handles spacing between fragments
   - Applies custom classes from markdown
   - Controls max-width and alignment

3. **Inner element for content**:
   - Has semantic HTML element (h1, p, blockquote, etc.)
   - Carries the `fragment` class for consistent styling
   - Contains the actual content

## Fragment Types and Their Elements

| Fragment Type | Inner Element | Notes |
|--------------|---------------|--------|
| `h1_` | `<h1>` | Direct heading element |
| `h2_` | `<h2>` | Direct heading element |
| `h3_` | `<h3>` | Direct heading element |
| `h4_` | `<h4>` | Direct heading element |
| `p_` | `<p>` | Paragraph element |
| `q_` | `<blockquote>` | Quote element |
| `hr_` | `<hr>` | Horizontal rule |
| `ul_` | `<ul>` | Unordered list |
| `ol_` | `<ol>` | Ordered list |
| `table_` | `<div>` | Container for table |
| `image_` | `<div>` | Container for img |
| `svg_` | `<div>` | Container for SVG |
| `code_` | `<div>` | Container for pre/code |
| `codex_` | `<div>` | Container for CodeMirror |
| `radio_` | `<div>` | Interactive radio container |
| `maths_` | `<div>` | Math input container |
| `graph_` | `<div>` | Graph visualization |
| `tabvar_` | `<div>` | Variation table |
| `toc_` | `<nav>` | Table of contents |

## CSS Targeting Examples

```css
/* Target all fragments of a specific type */
.fragment[data-f_type="h1_"] {
  /* Styles for h1 content */
}

/* Target wrapper for spacing */
.fragment-wrapper[data-f_type="p_"] + .fragment-wrapper[data-f_type="h2_"] {
  margin-top: 2rem;
}

/* Target by both class and type */
.fragment.lead[data-f_type="p_"] {
  font-size: 1.25rem;
}

/* Custom class on wrapper */
.fragment-wrapper.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
```

## JavaScript Selectors

```javascript
// Select all headings
const headings = document.querySelectorAll('.fragment[data-f_type^="h"]');

// Select specific fragment type
const radios = document.querySelectorAll('.fragment[data-f_type="radio_"]');

// Select wrapper for layout manipulation
const wrappers = document.querySelectorAll('.fragment-wrapper[data-f_type="image_"]');

// Query within a specific fragment
const radioButtons = fragment.querySelectorAll('button[data-flag]');
```

## Special Cases

### Radio Fragments
Radio fragments have additional nested structure for feedback:
```html
<div class="fragment-wrapper" data-f_type="radio_">
  <div class="fragment" data-f_type="radio_">
    <!-- Radio buttons -->
    <div id="radio-feedback-{index}">...</div>
    <div id="radio-explanation-{index}">...</div>
  </div>
</div>
```

### Tables
Tables maintain their semantic structure:
```html
<div class="fragment-wrapper" data-f_type="table_">
  <div class="fragment overflow-x-auto" data-f_type="table_">
    <table class="fragment-table">
      <!-- Table content -->
    </table>
  </div>
</div>
```

## Migration Notes

When updating existing code:
1. Remove unnecessary intermediary divs
2. Apply `fragment` class directly to semantic elements
3. Add `data-f_type` to both wrapper and fragment
4. Ensure custom classes go on the wrapper

## Benefits Summary

1. **Consistency**: All fragments follow the same pattern
2. **Flexibility**: Dual targeting for CSS and JS
3. **Semantic**: Uses appropriate HTML elements
4. **Maintainable**: Clear separation of concerns
5. **Debuggable**: Easy to identify in DevTools
6. **Extensible**: Easy to add new fragment types
