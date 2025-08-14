---
title: CSS Consistency Fixes
description: Documentation of CSS updates to match new fragment structure
chapter: Documentation
---

# CSS Consistency Fixes

## Issues Fixed

### 1. Nested Element Selectors

**Problem:** CSS was targeting `.fragment p` assuming `p` was nested inside `.fragment`
**Fix:** Changed to `p.fragment` since `<p>` now IS the `.fragment`

```css
/* Before (incorrect) */
.pm-container .fragment p {
    margin: 0.5rem 0 0.9rem;
}

/* After (correct) */
.pm-container p.fragment {
    margin: 0.5rem 0 0.9rem;
}
```

### 2. Complex Context Selectors

**Problem:** Selectors like `.fragment-wrapper[...] .fragment p` assumed nested structure
**Fix:** Changed to `.fragment-wrapper[...] p.fragment`

```css
/* Before (incorrect) */
.fragment-wrapper[data-f_type="p_"]:has(+ .fragment-wrapper[data-f_type="svg_"]) .fragment p

/* After (correct) */
.fragment-wrapper[data-f_type="p_"]:has(+ .fragment-wrapper[data-f_type="svg_"]) p.fragment
```

### 3. Adjacent Sibling Selectors

**Problem:** `h3.fragment+h2.fragment` won't work because elements are wrapped
**Fix:** Target through wrapper relationships

```css
/* Before (won't work) */
h3.fragment+h2.fragment {
    margin-top: 0.9rem;
}

/* After (works) */
.fragment-wrapper[data-f_type="h3_"] + .fragment-wrapper[data-f_type="h2_"] h2.fragment {
    margin-top: 0.9rem;
}
```

### 4. Media Query Selectors

**Problem:** `.lead.fragment` doesn't match our structure
**Fix:** Changed to `.fragment-wrapper.lead`

```css
/* Before */
@media (max-width: 768px) {
    .lead.fragment { ... }
}

/* After */
@media (max-width: 768px) {
    .fragment-wrapper.lead { ... }
}
```

## CSS That Remained Correct

These selectors were already correct:
- `ul.fragment`, `ol.fragment` - Correct since these elements ARE the fragments
- `h1.fragment`, `h2.fragment`, etc. - Correct since headings ARE the fragments
- `blockquote.fragment` - Correct since blockquote IS the fragment
- `table.fragment-table` - Correct as a specific class for tables
- `.fragment.image img` - Correct for image containers
- `.fragment.svg svg` - Correct for SVG containers

## Key Principles

1. **Semantic elements ARE fragments**: `<p class="fragment">`, `<h1 class="fragment">`
2. **Use wrapper for spacing**: `.fragment-wrapper + .fragment-wrapper`
3. **Target inner elements through wrapper**: `.fragment-wrapper[...] p.fragment`
4. **Custom classes on wrapper**: `.fragment-wrapper.lead`

## Benefits

- **More predictable**: CSS matches HTML structure
- **Better performance**: Less complex selectors
- **Easier debugging**: Clear relationship between CSS and HTML
- **Future-proof**: Easy to add new fragment types
