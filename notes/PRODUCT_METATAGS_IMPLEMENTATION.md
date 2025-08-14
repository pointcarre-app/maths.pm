# Product-Specific Metatags Implementation

## Overview
This document describes the implementation of product-specific metatags for PM pages in the Maths.pm application. The system allows each product to define its own SEO metatags that override domain defaults.

## Architecture

### 1. Data Model Updates (`src/models.py`)
- Added `metatags: Dict[str, Any]` field to `ProductModel` class
- Metatags are loaded from product YAML files and stored as a dictionary

### 2. Settings Configuration (`src/settings.py`)
- Updated product schema to include optional `metatags` field
- Schema: `StrictOptional("metatags"): MapPattern(Str(), YamlAny())`

### 3. Template Hierarchy

#### Base Template (`templates/base/main-alt.html`)
- Provides domain-wide generic metatags from `DOMAIN_CONFIG`
- Includes essential tags: viewport, theme-color, copyright, language, etc.
- Sets default description, keywords, and author that can be overridden

#### PM Template (`templates/pm/index.html`)
- Overrides title block with fallback chain:
  1. Product metatags title
  2. PM title + domain title  
  3. Domain default title
- In `extra_head` block, adds product-specific metatags:
  - Handles different meta tag formats (og:, twitter:, DC., itemprop)
  - Overrides description and keywords when present
  - Adds canonical URLs for PM pages

## Metatag Priority (Cascade Order)

1. **Product-specific metatags** (highest priority)
   - Defined in `/products/*.yml` files
   - Override everything else when present

2. **PM metadata** 
   - Falls back to PM title and content when no product metatags

3. **Domain defaults** (lowest priority)
   - From `domains/maths.pm.yml`
   - Always present as fallback

## Product YAML Structure

```yaml
name: product-name
# ... other product fields ...

# Product-specific metatags
metatags:
  # Basic SEO
  title: "Product Title - Descriptive title for SEO"
  description: "Product description for search results (150-160 chars)"
  keywords: "comma, separated, keywords"
  
  # Page metadata
  robots: "index, follow"
  revised: "Dec. 1, 2024, 10:00 am"
  topic: "Main topic of product"
  category: "Product category"
  
  # Dublin Core
  "DC.title": "Academic title"
  "DC.creator": "Author name"
  "DC.subject": "Subject keywords"
  
  # Open Graph (Facebook, LinkedIn)
  "og:title": "Social media title"
  "og:description": "Social media description"
  "og:image": "https://domain.com/image.jpg"
  "og:type": "website"
  "og:url": "https://domain.com/product/"
  
  # Twitter Cards
  "twitter:card": "summary_large_image"
  "twitter:title": "Twitter title"
  "twitter:description": "Twitter description"
  "twitter:image": "https://domain.com/twitter-image.jpg"
```

## Examples Implemented

### 1. Corsica (`products/00_corsica.yml`)
- Math exercises using Corsican geography
- Targeted for 3rd and 2nd year students
- Full set of SEO and social media tags

### 2. Nagini (`products/01_nagini.yml`)
- Python in the browser for education
- Focus on programming and interactive learning
- Simplified metatag set

### 3. JupyterLite (`products/50_jupyterlite.yml`)
- Complete Jupyter environment in browser
- Scientific computing focus
- Includes image metatags for social sharing

## Fallback Behavior

- **Missing metatags field**: System continues to work with domain defaults
- **Empty metatags**: No override, uses domain defaults
- **Partial metatags**: Only specified tags override, others use defaults
- **No product settings**: Falls back to PM metadata or domain defaults

## Testing

To test the implementation:

1. Start the server:
   ```bash
   python -m src.app
   ```

2. Visit a PM page with product metatags:
   ```
   http://127.0.0.1:5001/pm/corsica/a_troiz_geo.md
   ```

3. View page source to verify metatags are properly rendered

4. Test with curl:
   ```bash
   curl -s 'http://127.0.0.1:5001/pm/corsica/a_troiz_geo.md?format=html' | grep -E 'meta|title'
   ```

## Benefits

1. **SEO Optimization**: Each product can have unique, optimized metadata
2. **Social Sharing**: Customized Open Graph and Twitter cards per product
3. **Flexibility**: Products can override only what they need
4. **Backward Compatible**: Existing products without metatags continue to work
5. **Maintainable**: Centralized in product YAML files

## Future Enhancements

1. **Dynamic generation**: Generate metatags from PM content when not specified
2. **Image optimization**: Auto-generate social media images
3. **Structured data**: Add JSON-LD schema markup
4. **Multi-language**: Support for language-specific metatags
5. **A/B testing**: Support for testing different metatag variations
