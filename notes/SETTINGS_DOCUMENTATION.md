# Settings System Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Domain Configuration](#domain-configuration)
4. [Product Configuration](#product-configuration)
5. [Models](#models)
6. [Settings Processing Flow](#settings-processing-flow)
7. [Template Usage](#template-usage)
8. [Dependencies](#dependencies)
9. [Examples](#examples)

## Overview

The Maths.pm application uses a centralized settings system that loads configuration from YAML files and makes them available throughout the application. The system separates domain-wide settings from product-specific settings, allowing for modular configuration and dynamic resource loading.

### Key Components
- **Domain Configuration**: Site-wide settings, metatags, and resources (`domains/maths.pm.yml`)
- **Product Configurations**: Individual product settings and resources (`products/*.yml`)
- **Settings Class**: Central processor that loads and aggregates all configurations
- **Models**: Type-safe data structures for configurations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     settings.py                          │
│                                                          │
│  ┌──────────────────┐      ┌──────────────────────┐    │
│  │ Domain Config    │      │ Product Configs      │    │
│  │ Loader           │      │ Loader               │    │
│  └────────┬─────────┘      └─────────┬────────────┘    │
│           │                           │                  │
│           ▼                           ▼                  │
│  ┌──────────────────┐      ┌──────────────────────┐    │
│  │ DomainModel      │      │ List[ProductModel]   │    │
│  └────────┬─────────┘      └─────────┬────────────┘    │
│           │                           │                  │
│           └─────────────┬─────────────┘                  │
│                         ▼                                │
│              ┌──────────────────────┐                   │
│              │ Aggregated Settings  │                   │
│              └──────────────────────┘                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                    Jinja2 Templates
```

## Domain Configuration

### File Location
`domains/maths.pm.yml`

### Schema

#### Root Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain_url` | string | Yes | The full URL of the domain (e.g., "https://maths.pm") |
| `domain_specific_metatags` | dict | No | Generic metatags applied to ALL pages |
| `index_view_specific_metatags` | dict | No | Metatags specific to the index/home page |
| `templating` | object | Yes | Template configuration settings |
| `extra_head` | object | No | Additional JS/CSS resources for all pages |
| `backend_settings` | dict | No | Domain-level backend settings (deprecated - use product settings) |

#### Domain Specific Metatags

Generic metatags applied site-wide. Common fields include:

| Field | Description | Example |
|-------|-------------|---------|
| `viewport` | Viewport settings | "width=device-width, initial-scale=1.0" |
| `theme-color` | Browser theme color | "#FFFFFF" |
| `charset` | Character encoding | "UTF-8" |
| `author` | Site author | "Maths.pm, contact@pointcarre.app" |
| `copyright` | Copyright holder | "SAS POINTCARRE.APP" |
| `language` | Site language | "FR" |
| `robots` | Search engine directives | "index, follow" |
| `og:site_name` | Open Graph site name | "Maths.pm" |
| `twitter:site` | Twitter handle | "@mathspm" |

#### Index View Specific Metatags

Page-specific metatags for the home page:

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Page title | "Maths.pm - Logiciels libres..." |
| `description` | Page description | "Plateforme d'enseignement..." |
| `keywords` | SEO keywords | "mathématiques, enseignement..." |
| `og:title` | Open Graph title | "Maths.pm - Ressources..." |
| `og:description` | Open Graph description | "Plateforme éducative..." |
| `og:image` | Social media preview image | "https://maths.pm/static/images/..." |
| `twitter:card` | Twitter card type | "summary_large_image" |

#### Templating Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base_template` | string | Yes | Base HTML template to use |
| `footer_template` | string | Yes | Footer template path |
| `navbar_title` | string | Yes | Title displayed in navbar |
| `button_primary_text` | string | Yes | Primary button text |
| `button_primary_href` | string | Yes | Primary button link |
| `button_ghost_text` | string | Yes | Secondary button text |
| `button_ghost_href` | string | Yes | Secondary button link |

#### Extra Head Configuration

Optional domain-wide resources:

| Field | Type | Description |
|-------|------|-------------|
| `js` | string[] | JavaScript files to load on all pages |
| `css` | string[] | CSS files to load on all pages |

## Product Configuration

### File Location
`products/*.yml` (e.g., `01_nagini.yml`, `14_sujets0.yml`)

### Schema

#### Root Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique product identifier (e.g., "nagini") |
| `title_html` | string | Yes | Product title (supports HTML) |
| `subtitle_html` | string | No | Product subtitle (supports HTML) |
| `description` | string | Yes | Product description |
| `domains` | string[] | Yes | List of domains where product is available |
| `local_path` | string | No | URL path for the product (e.g., "/nagini") |
| `source_link` | string | No | Link to source code |
| `color` | string | Yes | DaisyUI color class (primary, secondary, accent, etc.) |
| `figure_svg` | string | No | SVG template file for product icon |
| `figure_png` | string | No | PNG image for product icon |
| `classes_formatted` | string[] | No | Target class levels (e.g., ["2<sup>nde</sup>", "1<sup>ère</sup>"]) |
| `tags` | string[] | No | Product tags for categorization |
| `is_hidden` | string | No | "true" to hide product from listings |
| `is_beta` | string | No | "true" to mark as beta |
| `owner_rdb` | string | Yes | Product owner organization |
| `owner_url` | string | Yes | Product owner URL |
| `backend_settings` | dict | No | Product-specific backend configuration |

#### Backend Settings

Product-specific configuration that can include:

```yaml
backend_settings:
  product_key:
    endpoint: "https://api.example.com/"
    js_url: "https://cdn.example.com/script.js"
    css_url: "https://cdn.example.com/styles.css"
    pyodide_worker_url: "https://cdn.example.com/worker.js"
    # Any other product-specific settings
```

Special fields for automatic resource loading:
- `js_url`: JavaScript file automatically loaded when visiting product routes
- `css_url`: CSS file automatically loaded when visiting product routes

## Models

### DomainModel (Pydantic BaseModel)

```python
class DomainModel(BaseModel):
    domain_url: str                                    # Required
    domain_specific_metatags: Dict[str, Any] = {}     # Optional, defaults to empty dict
    index_view_specific_metatags: Dict[str, Any] = {} # Optional, defaults to empty dict
    templating: TemplatingModel                        # Required
    extra_head: ExtraHeadModel = ExtraHeadModel()     # Optional, defaults to empty
    backend_settings: Dict[str, Any] = {}             # Deprecated, kept for compatibility
```

### TemplatingModel (Pydantic BaseModel)

```python
class TemplatingModel(BaseModel):
    base_template: str          # e.g., "base/main-alt.html"
    footer_template: str        # e.g., "domains/maths-pm/footers.html"
    navbar_title: str           # e.g., "Maths.pm"
    button_primary_text: str    # e.g., "Ressources"
    button_primary_href: str    # e.g., "/"
    button_ghost_text: str      # e.g., "Contact"
    button_ghost_href: str      # e.g., "/contact"
```

### ExtraHeadModel (Pydantic BaseModel)

```python
class ExtraHeadModel(BaseModel):
    js: List[str] = []   # JavaScript file URLs
    css: List[str] = []  # CSS file URLs
```

### ProductModel (Custom Class)

```python
class ProductModel:
    def __init__(self, data: Dict[str, Any]):
        self.domains: List[str]                  # Domains where product is active
        self.name: str                           # Product identifier
        self.title_html: str                     # Display title
        self.is_hidden: bool                     # Hide from listings
        self.is_beta: bool                       # Beta status
        self.subtitle_html: Optional[str]        # Subtitle
        self.description: str                    # Description
        self.local_path: Optional[str]           # URL path
        self.source_link: Optional[str]          # Source code link
        self.figure_svg: Optional[str]           # SVG template
        self.figure_png: Optional[str]           # PNG image
        self.color: str                          # DaisyUI color
        self.classes_formatted: Optional[List[str]]  # Class levels
        self.tags: Optional[List[str]]           # Tags
        self.owner_rdb: str                      # Owner name
        self.owner_url: str                      # Owner URL
        self.backend_settings: Dict[str, Any]    # Backend config
```

### ProductSettings (Wrapper Class)

```python
class ProductSettings:
    def __init__(self, product: ProductModel):
        self.product = product
        self.name = product.name
        self.backend_settings = product.backend_settings
    
    # Properties for easy access
    title: str                    # Product title
    description: str               # Product description
    local_path: Optional[str]      # Product route
    is_enabled: bool               # Has backend settings
    
    # Helper methods
    get_setting(key, default)     # Get backend setting
    get_nested_setting(*keys, default)  # Get nested setting
```

## Settings Processing Flow

### 1. Domain Configuration Loading

```python
# In Settings.domain_config computed field
1. Read domains/maths.pm.yml
2. Parse YAML with yaml.safe_load()
3. Create DomainModel instance
4. Handle errors with fallback to minimal config
```

### 2. Product Loading and Filtering

```python
# In Settings.products computed field
1. Scan products/*.yml files
2. For each file:
   a. Parse YAML with strictyaml schema validation
   b. Check if current domain in product.domains
   c. If match, create ProductModel instance
   d. Add to products list
```

### 3. Backend Settings Aggregation

```python
# In Settings.aggregated_backend_settings
1. Initialize empty dict
2. For each loaded product:
   a. Extract backend_settings
   b. Merge into aggregated dict
3. Return aggregated settings
```

### 4. Settings Serialization

```python
# In Settings.serialized_backend_settings
1. Take aggregated_backend_settings
2. Convert complex objects to JSON strings
3. Convert simple values to strings
4. Return template-ready dict
```

### 5. Template Context Injection

```python
# In Settings.templates property
1. Create Jinja2Templates instance
2. Inject globals:
   - DOMAIN_CONFIG (domain configuration)
   - products (list of products)
   - backend_public_settings (serialized settings)
```

## Template Usage

### Accessing Domain Configuration

```jinja2
<!-- Metatags -->
<meta name="description" content="{{ DOMAIN_CONFIG.index_view_specific_metatags.description }}" />
<meta name="author" content="{{ DOMAIN_CONFIG.domain_specific_metatags.author }}" />

<!-- Templating settings -->
<title>{{ DOMAIN_CONFIG.templating.navbar_title }}</title>
```

### Loading Domain-wide Resources

```jinja2
<!-- In base template head -->
{% if DOMAIN_CONFIG.extra_head %}
  {% for js_url in DOMAIN_CONFIG.extra_head.js %}
    <script src="{{ js_url }}"></script>
  {% endfor %}
  {% for css_url in DOMAIN_CONFIG.extra_head.css %}
    <link rel="stylesheet" href="{{ css_url }}" />
  {% endfor %}
{% endif %}
```

### Smart Product Resource Loading

```jinja2
<!-- Automatic route-based loading -->
{% set path_segments = request.url.path.strip('/').split('/') %}
{% set current_route = path_segments[0] if path_segments else '' %}

{% for product in products %}
  {% if product.name == current_route and product.backend_settings %}
    {% for setting_key, setting_value in product.backend_settings.items() %}
      {% if setting_value.js_url %}
        <script src="{{ setting_value.js_url }}"></script>
      {% endif %}
      {% if setting_value.css_url %}
        <link rel="stylesheet" href="{{ setting_value.css_url }}" />
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}
```

### Accessing Backend Settings

```jinja2
<!-- In templates -->
{{ backend_public_settings.NAGINI_ENDPOINT }}
{{ backend_public_settings.CORPUS_PATHS_TO_LOAD }}

<!-- As data attributes -->
<div id="backend-settings"
  {% for key, value in backend_public_settings.items() %}
    data-{{ key|lower }}="{{ value }}"
  {% endfor %}>
</div>
```

## Dependencies

### Python Dependencies

```python
# Core dependencies (from settings.py imports)
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from strictyaml import (
    Any as YamlAny, 
    Map, 
    MapPattern, 
    Optional as StrictOptional, 
    Seq, 
    Str, 
    load
)
import logging
import yaml
```

### Required Packages

```text
# requirements.txt
pydantic>=2.0.0
pydantic-settings>=2.0.0
strictyaml>=1.7.0
PyYAML>=6.0
fastapi>=0.100.0
jinja2>=3.1.0
```

### File System Dependencies

```
Repository Root/
├── domains/
│   └── maths.pm.yml         # Required: Domain configuration
├── products/
│   ├── *.yml                # Product configurations
│   └── ...
├── src/
│   ├── settings.py          # Settings processor
│   ├── models.py            # Data models
│   └── templates/           # Jinja2 templates
│       └── base/
│           └── main-alt.html  # Base template
└── ...
```

## Examples

### Example Domain Configuration

```yaml
# domains/maths.pm.yml
domain_url: "https://maths.pm"

domain_specific_metatags:
  viewport: "width=device-width, initial-scale=1.0"
  theme-color: "#FFFFFF"
  author: "Maths.pm Team"

index_view_specific_metatags:
  title: "Maths.pm - Educational Platform"
  description: "Learn mathematics with interactive tools"
  og:image: "https://maths.pm/social.jpg"

templating:
  base_template: "base/main-alt.html"
  footer_template: "domains/maths-pm/footers.html"
  navbar_title: "Maths.pm"
  button_primary_text: "Resources"
  button_primary_href: "/"
  button_ghost_text: "Contact"
  button_ghost_href: "/contact"

extra_head:
  js:
    - "https://cdn.example.com/analytics.js"
  css:
    - "https://fonts.googleapis.com/css2?family=Inter"
```

### Example Product Configuration

```yaml
# products/01_nagini.yml
name: nagini
title_html: Nagini
subtitle_html: Python in the Browser
description: Execute Python scripts directly in your browser
domains:
  - maths.pm
local_path: /nagini
color: accent
is_beta: true
tags:
  - python
  - browser
  - education
owner_rdb: "POINTCARRE.APP"
owner_url: "https://pointcarre.app"

backend_settings:
  nagini:
    endpoint: "https://cdn.jsdelivr.net/gh/org/nagini@0.0.17/"
    js_url: "https://cdn.jsdelivr.net/gh/org/nagini@0.0.17/nagini.js"
    css_url: "https://cdn.jsdelivr.net/gh/org/nagini@0.0.17/nagini.css"
    pyodide_version: "0.26.4"
```

### Accessing Settings in Python

```python
# Import the singleton settings instance
from src.settings import settings

# Access domain configuration
domain_url = settings.domain_config.domain_url
metatags = settings.domain_config.domain_specific_metatags

# Access products
for product in settings.products:
    print(f"Product: {product.name}")
    if product.backend_settings:
        print(f"  Settings: {product.backend_settings}")

# Get aggregated backend settings
all_settings = settings.aggregated_backend_settings

# Access specific product settings
from src.settings import nagini_settings
if nagini_settings:
    endpoint = nagini_settings.get_nested_setting('nagini', 'endpoint')
```

### Using Settings in Templates

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Domain metatags -->
  <meta name="author" content="{{ DOMAIN_CONFIG.domain_specific_metatags.author }}">
  
  <!-- Page-specific metatags -->
  <title>{{ DOMAIN_CONFIG.index_view_specific_metatags.title }}</title>
  
  <!-- Load domain-wide resources -->
  {% if DOMAIN_CONFIG.extra_head %}
    {% for js in DOMAIN_CONFIG.extra_head.js %}
      <script src="{{ js }}"></script>
    {% endfor %}
  {% endif %}
  
  <!-- Smart product loading (automatic) -->
  <!-- If URL is /nagini/something, loads nagini resources -->
</head>
<body>
  <!-- Access backend settings -->
  <div id="app" data-endpoint="{{ backend_public_settings.NAGINI_ENDPOINT }}">
    <!-- Product list -->
    {% for product in products %}
      {% if not product.is_hidden %}
        <a href="{{ product.local_path }}">{{ product.title_html }}</a>
      {% endif %}
    {% endfor %}
  </div>
</body>
</html>
```

## Best Practices

1. **Domain vs Product Settings**: Keep domain-wide settings in `domains/` and product-specific settings in `products/`

2. **Resource Loading**: Use `js_url` and `css_url` in product backend_settings for automatic loading

3. **Metatags Organization**: 
   - Generic tags in `domain_specific_metatags`
   - Page-specific tags in `index_view_specific_metatags`

4. **Product Filtering**: Always include appropriate domains in product files to control visibility

5. **Settings Access**: Use the singleton `settings` instance throughout the application

6. **Template Globals**: Rely on injected globals (DOMAIN_CONFIG, products, backend_public_settings) rather than passing context

7. **Error Handling**: The system includes fallbacks for missing configurations to prevent crashes

## Troubleshooting

### Products Not Loading
- Check that product file includes current domain in `domains` array
- Verify YAML syntax is valid
- Check logs for validation errors

### Resources Not Loading
- Ensure `js_url` or `css_url` are inside a dict within `backend_settings`
- Verify the product route matches the URL path
- Check browser console for 404 errors

### Missing Metatags
- Verify field names in YAML match exactly
- Check template is using correct path (e.g., `DOMAIN_CONFIG.domain_specific_metatags.author`)

### Backend Settings Not Available
- Ensure products are loaded (check `/settings` endpoint)
- Verify aggregation is working (check logs)
- Check template is using `backend_public_settings` global

---

*Last Updated: January 2025*
*Version: 2.0.0*
