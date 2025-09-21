---
# Standard PM metadata
class_at_school: examples
chapter: "Demonstration"

# Page-specific metatags - These will be rendered in the HTML <head>
title: "Example PM Page with Custom Metatags"
description: "This page demonstrates how to add unique metatags to individual PM pages for better SEO and social sharing."
keywords: "example, metatags, SEO, PM pages, maths.pm"
author: "Maths.pm Documentation Team"
robots: "index, follow, max-snippet:200"

# Open Graph metatags for social media
og:title: "PM Page Metatags Example | Maths.pm"
og:description: "Learn how to add custom metatags to PM pages for improved SEO and social media sharing."
og:type: "article"
og:image: "https://maths.pm/static/images/pm-metatags-example.jpg"
og:url: "https://maths.pm/pm/examples/metatags_example.md"

# Twitter Card metatags
twitter:card: "summary_large_image"
twitter:title: "Custom Metatags in PM Pages"
twitter:description: "Add unique SEO and social media tags to each PM page"
twitter:image: "https://maths.pm/static/images/pm-metatags-twitter.jpg"

# Dublin Core metadata
DC.title: "PM Page Metatags Documentation"
DC.creator: "Maths.pm Team"
DC.subject: "Web Development, SEO, Education"
DC.description: "Technical documentation for PM page metatags"
DC.publisher: "Maths.pm"
DC.date: "2025-01-15"

# Additional SEO metatags
abstract: "A comprehensive guide to adding page-specific metatags to PM markdown files"
topic: "Web Development and SEO"
summary: "This example shows all available metatag options for PM pages"
category: "Documentation, SEO"
revised: "2025-01-15"
pagename: "PM Metatags Example"
subtitle: "SEO and Social Media Optimization"
canonical: "https://maths.pm/pm/examples/metatags_example"
---

# PM Page with Custom Metatags

This page demonstrates how to add **unique metatags** to individual PM pages.

## Why Use Page-Specific Metatags?

Each PM page can have its own unique metatags for:
- **Better SEO**: Custom titles, descriptions, and keywords
- **Social Media Sharing**: Open Graph and Twitter Card tags
- **Documentation**: Dublin Core metadata
- **Search Engine Control**: Robots directives

## How It Works

Simply add metatags to the YAML front matter at the top of your PM file:

```yaml
---
title: "Your Page Title"
description: "Your page description"
keywords: "keyword1, keyword2, keyword3"
og:title: "Social Media Title"
og:description: "Social Media Description"
---
```

## Priority Order

The metatags are applied with the following priority:
1. **PM page metatags** (highest priority) - Defined in the markdown file
2. **Product metatags** - Defined in products/*.yml
3. **Domain defaults** - Defined in domains/maths.pm.yml

## Available Metatag Fields

### Basic SEO
- `title` - Page title
- `description` - Page description
- `keywords` - Comma-separated keywords
- `author` - Page author
- `robots` - Search engine directives

### Open Graph (Facebook, LinkedIn)
- `og:title` - Social media title
- `og:description` - Social media description
- `og:image` - Preview image URL
- `og:type` - Content type (article, website, etc.)
- `og:url` - Canonical URL

### Twitter Cards
- `twitter:card` - Card type (summary, summary_large_image)
- `twitter:title` - Twitter title
- `twitter:description` - Twitter description
- `twitter:image` - Twitter preview image

### Dublin Core
- `DC.title` - Formal title
- `DC.creator` - Creator/Author
- `DC.subject` - Subject/Topics
- `DC.description` - Formal description

### Additional Fields
- `abstract` - Brief summary
- `topic` - Main topic
- `category` - Categories
- `revised` - Last revision date
- `canonical` - Canonical URL
