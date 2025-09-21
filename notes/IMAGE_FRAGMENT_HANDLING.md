# Image Fragment Handling Documentation

## Overview
The PCA MathsPM system provides comprehensive support for images and visual content through the fragment system. Images are automatically detected in markdown and converted to appropriate fragment types based on their file extension and usage context.

## Image Storage Locations

### 1. Product-Specific Images (`/pms/[product]/images/`)
**Recommended for**: Images specific to a product's educational content
```
pms/dataviz2/images/
├── covid19-states-analysis.png
├── scatter-plot-example.jpg
└── data-flow-diagram.svg
```

**Note**: Files in `/pms/` are automatically synced to `/src/static/pm/` for serving.

**Usage in markdown**:
```markdown
![Description](images/filename.png)  # Relative path
![Description](/static/pm/dataviz2/images/filename.png)  # Absolute path
```

**Direct URL Access**:
```
✅ Correct: http://127.0.0.1:5001/static/pm/dataviz2/images/filename.png
❌ Wrong:   http://127.0.0.1:5001/pm/dataviz2/images/filename.png
```

### 2. Static Directory (`/static/images/`)
**Recommended for**: Shared assets, logos, common diagrams
```
static/images/
├── logo.png
├── common-icons.svg
└── background-patterns/
```
**Usage in markdown**:
```markdown
![Company Logo](/static/images/logo.png)
```

### 3. Files Directory (`/files/images/`)
**Recommended for**: External resources, imported content
```
files/images/
├── external-chart.jpg
└── third-party-diagram.png
```
**Usage in markdown**:
```markdown
![External Resource](/files/images/external-chart.jpg)
```

## Fragment Types for Visual Content

### 1. Image Fragment (`image_`)
**Created for**: PNG, JPG, JPEG, GIF, WebP files
**Fragment structure**:
```python
{
    "f_type": FType("image_"),
    "html": "Alt text from markdown",
    "data": {
        "src": "/path/to/image.png"
    }
}
```

### 2. SVG Fragment (`svg_`)
**Created for**: SVG files
**Special behavior**: Content is loaded inline for CSS/JS interaction
**Fragment structure**:
```python
{
    "f_type": FType("svg_"),
    "html": "Alt text from markdown",
    "data": {
        "src": "/path/to/diagram.svg",
        "content": "<svg>...</svg>"  # Actual SVG markup
    }
}
```

### 3. HTML Fragment (`html_`)
**Created for**: HTML files referenced as images
**Use case**: Embedding interactive widgets or complex HTML content
**Fragment structure**:
```python
{
    "f_type": FType("html_"),
    "html": "Alt text or empty",
    "data": {
        "src": "/path/to/widget.html",
        "content": "<div>...</div>"  # Rendered HTML
    }
}
```

## Path Resolution Logic

The `FragmentBuilder.from_paragraph()` method (lines 450-563) handles image detection with the following resolution order:

1. **Direct path from base directory**: `/Users/selim/madles/pca-mathspm/[path]`
2. **Static directory**: `/Users/selim/madles/pca-mathspm/src/static/[path]`
3. **PMs directory**: `/Users/selim/madles/pca-mathspm/pms/[path]`
4. **Files directory**: `/Users/selim/madles/pca-mathspm/files/[path]`

## Best Practices

### 1. File Naming
- Use descriptive, kebab-case names: `covid19-states-analysis.png`
- Include dimensions for multiple versions: `logo-128x128.png`
- Prefix with date for temporal data: `20200530-covid-data.png`

### 2. Organization
```
pms/dataviz2/
├── images/
│   ├── chapter01/
│   │   ├── figure-1-1.png
│   │   └── figure-1-2.svg
│   ├── chapter02/
│   └── shared/
│       └── logo.png
```

### 3. Markdown Usage
```markdown
<!-- Prefer relative paths for portability -->
![Local diagram](images/diagram.png)

<!-- Use absolute paths for shared resources -->
![Shared logo](/static/images/logo.png)

<!-- Always include meaningful alt text -->
![COVID-19 death rates by state showing correlation with lockdown timing](images/covid-analysis.png)
```

### 4. Performance Considerations
- **Optimize images**: Use appropriate formats (WebP for photos, SVG for diagrams)
- **Lazy loading**: Large images are automatically lazy-loaded by the browser
- **Responsive images**: Consider providing multiple resolutions

## Special Image Behaviors

### 1. SVG Inline Loading
SVGs are loaded inline to enable:
- CSS styling of SVG elements
- JavaScript event handling
- Dynamic color theming
- SMIL animations

### 2. HTML Includes
Using the image syntax with `.html` files:
```markdown
![Interactive Widget](/static/widgets/calculator.html)
```
This embeds the HTML content directly, supporting:
- Jinja2 template rendering
- JavaScript execution
- Full HTML/CSS capabilities

### 3. Image Error Handling
If an image cannot be loaded:
- Regular images: Show broken image icon with alt text
- SVGs: Fall back to `image_` fragment type
- HTML includes: Fall back to paragraph fragment

## Template Rendering

The image fragment is rendered using the `image_.html` template:
```html
<div class="fragment-wrapper" data-f_type="image_">
  <figure class="fragment">
    <img src="{{ fragment.data.src }}" 
         alt="{{ fragment.html }}"
         loading="lazy"
         class="{{ ' '.join(fragment.class_list) }}">
    {% if fragment.html %}
    <figcaption>{{ fragment.html }}</figcaption>
    {% endif %}
  </figure>
</div>
```

## URL Routing Structure

Understanding how URLs map to files is crucial for accessing raw assets:

### Route Types

| Route Pattern | Purpose | Example |
|--------------|---------|---------|
| `/pm/[product]/[file].md` | Markdown processing | `/pm/dataviz2/00_plan.md` |
| `/static/[path]` | Static file serving | `/static/pm/dataviz2/images/chart.png` |
| `/images/[file]` | Files/images directory | `/images/logo.png` |

### Important Notes

1. **Markdown Routes (`/pm/`)**: 
   - Process `.md` files through the template system
   - Cannot serve raw images or other static files
   - Always append `?format=html` for proper rendering

2. **Static Routes (`/static/`)**: 
   - Serve files from `src/static/` directory
   - Images in `pms/` are synced to `src/static/pm/`
   - Direct file access without processing

3. **Automatic Sync**:
   - Files in `pms/[product]/` are mirrored to `src/static/pm/[product]/`
   - This enables both markdown processing and raw file access

### Examples

```bash
# Markdown file (processed)
http://127.0.0.1:5001/pm/dataviz2/00_plan.md?format=html

# Image in markdown (raw access)
http://127.0.0.1:5001/static/pm/dataviz2/images/covid19-states-analysis.png

# Wrong - this won't work for images
http://127.0.0.1:5001/pm/dataviz2/images/covid19-states-analysis.png
```

## Debugging Image Issues

### 1. Check Console Logs
The fragment builder logs path resolution attempts:
```
Error reading SVG file /path/to/file.svg: [error details]
```

### 2. Verify Fragment Type
In browser console:
```javascript
document.querySelectorAll('[data-f_type="image_"]').forEach(img => {
    console.log(img.querySelector('img').src);
});
```

### 3. Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Image not showing | Wrong path | Check relative vs absolute paths |
| SVG not interactive | Loaded as image | Ensure `.svg` extension is lowercase |
| HTML not rendering | Security restrictions | Verify file exists and path is correct |
| Broken image icon | File not found | Check file exists at specified location |

## Migration Guide

### Moving Images to Proper Structure
```bash
# Create proper directory structure
mkdir -p pms/dataviz2/images

# Move and rename images
mv "pms/old-image (1).png" "pms/dataviz2/images/descriptive-name.png"

# Update markdown references
# From: ![Alt](old-image (1).png)
# To: ![Alt](images/descriptive-name.png)
```

### Batch Processing
```python
import os
from pathlib import Path

# Script to update image references
def update_image_paths(md_file):
    content = md_file.read_text()
    # Update relative paths
    content = content.replace('](../images/', '](images/')
    # Update absolute paths
    content = content.replace('](/images/', '](/static/pm/dataviz2/images/')
    md_file.write_text(content)
```

## Integration with Other Fragment Types

### Images in Codex Fragments
```yaml
f_type: codex_
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Generate and display image
  plt.figure(figsize=(10, 6))
  plt.plot(np.random.randn(100))
  plt.title("Generated Plot")
  plt.savefig("/tmp/plot.png")
  plt.show()
```

### Images in HTML Fragments
```html
<div class="image-gallery">
  <img src="/static/pm/dataviz2/images/chart1.png" alt="Chart 1">
  <img src="/static/pm/dataviz2/images/chart2.png" alt="Chart 2">
</div>
```

### Images in Tables
```markdown
| State | Chart |
|-------|-------|
| NY | ![NY Data](images/ny-chart.png) |
| CA | ![CA Data](images/ca-chart.png) |
```

## Security Considerations

1. **Path Traversal**: The system prevents `../` path traversal attacks
2. **File Type Validation**: Only specific extensions trigger image fragments
3. **HTML Sanitization**: Embedded HTML is not automatically sanitized - use trusted content only
4. **SVG Security**: Inline SVGs can contain JavaScript - verify source

## Future Enhancements

### Planned Features
1. **Responsive Images**: `<picture>` element support with srcset
2. **Image Optimization**: Automatic WebP conversion
3. **CDN Support**: External image hosting integration
4. **Image Galleries**: Native carousel/lightbox support
5. **Lazy Loading Config**: Configurable lazy loading strategies

### Under Consideration
1. Base64 inline images for small files
2. Automatic alt text generation
3. Image compression on upload
4. AVIF format support

---

*Last Updated: November 2024*
*Document Version: 1.0.0*
