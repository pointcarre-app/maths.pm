---
title: "Guide: Page-Specific Metatags for PM Pages"
description: "Complete guide for adding unique SEO and social media metatags to individual PM markdown pages"
keywords: "PM pages, metatags, SEO, documentation, maths.pm"
author: "Maths.pm Documentation"
---

# PM Page-Specific Metatags Guide

## Overview

Every PM page (markdown file in the `pms/` directory) can have its own unique metatags for SEO and social media optimization. These metatags are defined in the YAML front matter at the top of each markdown file.

## How to Add Metatags

Add metatags to the YAML front matter at the beginning of your PM file:

```yaml
---
# Standard PM metadata
class_at_school: seconde
chapter: "Fonctions"

# Page-specific metatags
title: "Your Custom Page Title"
description: "A detailed description of your page content"
keywords: "keyword1, keyword2, keyword3"
author: "Author Name"
robots: "index, follow"

# Social media tags
og:title: "Title for Facebook/LinkedIn"
og:description: "Description for social media"
og:image: "https://example.com/image.jpg"
twitter:card: "summary_large_image"
twitter:title: "Title for Twitter"
---
```

## Available Metatag Fields

### Basic SEO Metatags
- `title` - Page title (appears in browser tab)
- `description` - Page description for search engines
- `keywords` - Comma-separated keywords
- `author` - Page author
- `robots` - Search engine directives (index, follow, noindex, etc.)
- `canonical` - Canonical URL to avoid duplicate content

### Open Graph (Facebook, LinkedIn)
- `og:title` - Title for social media
- `og:description` - Description for social media
- `og:image` - Preview image URL
- `og:url` - Page URL
- `og:type` - Content type (article, website, book, etc.)
- `og:site_name` - Website name
- `og:locale` - Language/region (e.g., fr_FR)

### Twitter Card
- `twitter:card` - Card type (summary, summary_large_image, player)
- `twitter:title` - Twitter title
- `twitter:description` - Twitter description
- `twitter:image` - Twitter preview image
- `twitter:creator` - Twitter handle of content creator
- `twitter:site` - Twitter handle of website

### Dublin Core Metadata
- `DC.title` - Formal title
- `DC.creator` - Creator/Author
- `DC.subject` - Subject/Topics
- `DC.description` - Formal description
- `DC.publisher` - Publisher
- `DC.date` - Publication date
- `DC.type` - Resource type
- `DC.format` - File format
- `DC.language` - Language

### Additional SEO Fields
- `abstract` - Brief summary of content
- `topic` - Main topic of the page
- `summary` - Content summary
- `category` - Page categories
- `revised` - Last revision date
- `pagename` - Internal page name
- `subtitle` - Page subtitle

## Priority Order

Metatags are applied with the following priority:
1. **PM page metatags** (highest) - From the markdown file's YAML front matter
2. **Product metatags** - From `products/*.yml` files
3. **Domain defaults** (lowest) - From `domains/maths.pm.yml`

## Best Practices

### 1. Title Tags
- Keep titles under 60 characters
- Include primary keywords
- Make each page title unique

```yaml
title: "Calcul de Surfaces - Géométrie de la Corse | Maths 3ème"
```

### 2. Description Tags
- Keep descriptions between 150-160 characters
- Include a call-to-action when appropriate
- Make descriptions compelling and accurate

```yaml
description: "Apprenez à calculer la surface de la Corse avec des méthodes géométriques simples. Exercice interactif pour élèves de troisième avec cartes et solutions."
```

### 3. Keywords
- Use relevant, specific keywords
- Separate with commas
- Don't keyword stuff

```yaml
keywords: "géométrie, surface, corse, mathématiques, troisième, exercices"
```

### 4. Social Media Images
- Use high-quality images (1200x630px for og:image)
- Include text overlay for context
- Use absolute URLs

```yaml
og:image: "https://maths.pm/static/images/corsica-geometry.jpg"
twitter:image: "https://maths.pm/static/images/corsica-geometry-twitter.jpg"
```

## Example: Complete PM File

```markdown
---
# PM metadata
class_at_school: troiz
chapter: "Géométrie"

# SEO metatags
title: "Géographie de la Corse - Calcul de surfaces | Maths 3ème"
description: "Exercice de géométrie appliquée : calculez la surface de la Corse avec un quadrillage. Niveau troisième avec solutions détaillées."
keywords: "corse, géométrie, surface, quadrillage, mathématiques, troisième"
author: "Équipe pédagogique Maths.pm"
robots: "index, follow"
canonical: "https://maths.pm/pm/corsica/a_troiz_geo"

# Open Graph
og:title: "Calculez la surface de la Corse - Exercice de Géométrie"
og:description: "Méthode simple pour calculer la surface d'une île avec un quadrillage géographique."
og:image: "https://maths.pm/static/images/corsica-grid.jpg"
og:type: "article"
og:url: "https://maths.pm/pm/corsica/a_troiz_geo"

# Twitter
twitter:card: "summary_large_image"
twitter:title: "Géométrie de la Corse - Maths 3ème"
twitter:description: "Exercice interactif de calcul de surface"
twitter:image: "https://maths.pm/static/images/corsica-twitter.jpg"

# Dublin Core
DC.title: "Géographie mathématique de la Corse"
DC.creator: "Maths.pm"
DC.subject: "Mathématiques, Géométrie, Géographie"

# Additional
revised: "2025-01-15"
topic: "Géométrie appliquée"
category: "Mathématiques, Troisième"
---

# Géographie de l'île

[Your PM content here...]
```

## Testing Your Metatags

After adding metatags to your PM file:

1. Navigate to your PM page
2. View page source (Ctrl+U or Cmd+Option+U)
3. Check the `<head>` section for your metatags
4. Use tools like:
   - [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
   - [Twitter Card Validator](https://cards-dev.twitter.com/validator)
   - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

## Troubleshooting

### Metatags Not Showing
- Ensure YAML front matter is at the very beginning of the file
- Check for YAML syntax errors (use proper indentation)
- Verify field names are spelled correctly

### Default Tags Still Appearing
- PM metatags should override defaults
- Check that field names match exactly (case-sensitive)
- Restart the server after making changes

### Social Media Not Updating
- Social platforms cache metatags
- Use their debugging tools to force a refresh
- Wait 24-48 hours for changes to propagate
