# 🧪 Domain and Product Settings Verification Report

This report verifies that domain configuration (maths.pm.yml) and product
configurations (00_corsica.yml, 01_nagini.yml) are correctly injected into
the HTML responses.

---

## 📍 Testing: /corsica/
**URL**: http://127.0.0.1:5001/corsica/
**Product**: corsica
**Timestamp**: 2025-08-15T22:24:27.913762

### 📊 Basic Information
- **Page Title**: Maths.Corsica - Exercices mathématiques autour de la Corse
- **Total Metatags Found**: 30
- **Total Scripts Loaded**: 4
- **Total Stylesheets**: 8
- **Data Brick**: ✅ Found with 5 elements
  - Elements: domain-config, backend-public-settings, nagini-settings, pca-corpus-settings, pca-teachers-settings
  - Domain config attrs: 92
  - Backend settings attrs: 3

### 🌍 Domain-Wide Metatags (from maths.pm.yml)
**Found:**
  ✅ viewport: width=device-width, initial-scale=1.0
  ✅ theme-color: #FFFFFF
  ✅ subject: Enseignement des mathématiques et logiciels libres (Open Source)
  ✅ copyright: SAS POINTCARRE.APP
  ✅ language: FR
  ... and 6 more

### 📄 Page-Specific Metatags
**Found:**
  ✅ description: Exercices de mathématiques inspirés de la géograph...
  ✅ keywords: mathématiques, corse, géométrie, trigonométrie, py...
  ✅ og:title: Maths.Corsica - Exercices mathématiques autour de ...
  ✅ og:description: Exercices de maths inspirés de la Corse : trigonom...
  ✅ twitter:title: Maths.Corsica - La Corse en mathématiques...
  ✅ twitter:description: Exercices mathématiques inspirés de la géographie ...
**Missing:**
  ❌ title: missing

### ⚙️ Backend Settings (from corsica.yml)
**Error:** No backend_settings found in corsica.yml
**All scripts in page:**
  - https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4
  - https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js
  - https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js
  - http://127.0.0.1:5001/static/js/navbar-active-state.js

### 🔍 Raw Data Samples
<details>
<summary>Click to expand metatags sample</summary>

```json
{
  "viewport": "width=device-width, initial-scale=1.0",
  "theme-color": "#FFFFFF",
  "subject": "Enseignement des math\u00e9matiques et logiciels libres (Open Source)",
  "copyright": "SAS POINTCARRE.APP",
  "language": "FR",
  "Classification": "Education",
  "rating": "General",
  "HandheldFriendly": "True",
  "MobileOptimized": "320",
  "twitter:site": "@mathspm"
}
```
</details>

<details>
<summary>Click to expand scripts list</summary>

- https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4
- https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js
- https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js
- http://127.0.0.1:5001/static/js/navbar-active-state.js
</details>

<details>
<summary>Click to expand HTML head snippet (first 2000 chars)</summary>

```html
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>
      
  
    Maths.Corsica - Exercices mathématiques autour de la Corse
  

    </title>
<link href="http://127.0.0.1:5001/static/favicon/apple-icon-57x57.png" rel="icon" type="image/x-icon"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&amp;family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&amp;family=Dancing+Script:wght@400..700&amp;family=EB+Garamond:ital,wght@0,400..800;1,400..800&amp;family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&amp;family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&amp;family=Lora:ital,wght@0,400..700;1,400..700&amp;family=Playfair+Display:ital,wght@0,400..900;1,400..900&amp;family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&amp;family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&amp;family=Playfair+Display:ital,wght@0,400..900;1,400..900&amp;display=swap" rel="stylesheet"/>
<script>
    // Suppress Tailwind production warning for development
    window.process = {
        env: {
            NODE_ENV: 'development'
        }
    };
</script>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<script type="tailwind-config">
    {
        plugins: [
            tailwind.plugin.typography,
        ],
    }
</script>
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css"/>
<link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css"/>
<link href="http://127.0.0.1:5001/static/css/root.css" rel="stylesheet"/>
<link href="http://127.0.0.1:5001/static/css/styles.css" rel="style
... (truncated)
```
</details>

<details>
<summary>Click to expand data-brick HTML</summary>

```html
<data-brick>
<div data-domain_specific_metatags.apple-mobile-web-app-capable="yes" data-domain_specific_metatags.apple-mobile-web-app-status-bar-style="black" data-domain_specific_metatags.apple-touch-fullscreen="yes" data-domain_specific_metatags.author="Maths.pm, contact@pointcarre.app" data-domain_specific_metatags.charset="UTF-8" data-domain_specific_metatags.classification="Education" data-domain_specific_metatags.copyright="SAS POINTCARRE.APP" data-domain_specific_metatags.coverage="Europe" data-domain_specific_metatags.designer="SAS POINTCARRE.APP" data-domain_specific_metatags.directory="education" data-domain_specific_metatags.distribution="Europe" data-domain_specific_metatags.format-detection="telephone=no" data-domain_specific_metatags.generator="HTML5" data-domain_specific_metatags.geo.placename="Paris" data-domain_specific_metatags.geo.region="FR-IDF" data-domain_specific_metatags.handheldfriendly="True" data-domain_specific_metatags.http-equiv-cache-control="no-cache" data-domain_specific_metatags.http-equiv-expires="0" data-domain_specific_metatags.http-equiv-imagetoolbar="no" data-domain_specific_metatags.http-equiv-pragma="no-cache" data-domain_specific_metatags.http-equiv-x-dns-prefetch-control="off" data-domain_specific_metatags.icbm="48.8566, 2.3522" data-domain_specific_metatags.language="FR" data-domain_specific_metatags.medium="website" data-domain_specific_metatags.mobile-web-app-capable="yes" data-domain_specific_metatags.mobileoptimized="320" data-d
... (truncated)
```
</details>

---

## 📍 Testing: /nagini
**URL**: http://127.0.0.1:5001/nagini
**Product**: nagini
**Timestamp**: 2025-08-15T22:24:28.087380

### 📊 Basic Information
- **Page Title**: Nagini - Python dans le navigateur pour l'éducation
- **Total Metatags Found**: 21
- **Total Scripts Loaded**: 5
- **Total Stylesheets**: 8
- **Data Brick**: ✅ Found with 5 elements
  - Elements: domain-config, backend-public-settings, nagini-settings, pca-corpus-settings, pca-teachers-settings
  - Domain config attrs: 92
  - Backend settings attrs: 3

### 🌍 Domain-Wide Metatags (from maths.pm.yml)
**Found:**
  ✅ viewport: width=device-width, initial-scale=1.0
  ✅ theme-color: #FFFFFF
  ✅ subject: Enseignement des mathématiques et logiciels libres (Open Source)
  ✅ copyright: SAS POINTCARRE.APP
  ✅ language: FR
  ... and 6 more

### 📄 Page-Specific Metatags
**Found:**
  ✅ description: Exécutez du Python directement dans votre navigate...
  ✅ keywords: python, navigateur, pyodide, jupyter, education, p...
  ✅ og:title: Nagini - Python dans le navigateur...
  ✅ og:description: Environnement Python interactif sans installation....
  ✅ twitter:title: Nagini - Python dans le navigateur...
  ✅ twitter:description: Exécutez du Python directement dans votre navigate...
**Missing:**
  ❌ title: missing

### ⚙️ Backend Settings (from nagini.yml)
**Expected backend_settings from YAML:**
```yaml
nagini:
  endpoint: https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/
  js_url: https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/nagini.js
  pyodide_worker_url: https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/pyodide/worker/worker-dist.js

```
**Scripts Loaded:**
  ✅ nagini.js_url: https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17...
  ℹ️ nagini.endpoint: https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17...
**All scripts in page:**
  - https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4
  - https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js
  - https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js
  - https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/nagini.js
  - http://127.0.0.1:5001/static/js/navbar-active-state.js

### 🔍 Raw Data Samples
<details>
<summary>Click to expand metatags sample</summary>

```json
{
  "viewport": "width=device-width, initial-scale=1.0",
  "theme-color": "#FFFFFF",
  "subject": "Enseignement des math\u00e9matiques et logiciels libres (Open Source)",
  "copyright": "SAS POINTCARRE.APP",
  "language": "FR",
  "Classification": "Education",
  "rating": "General",
  "HandheldFriendly": "True",
  "MobileOptimized": "320",
  "twitter:site": "@mathspm"
}
```
</details>

<details>
<summary>Click to expand scripts list</summary>

- https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4
- https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js
- https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js
- https://cdn.jsdelivr.net/gh/your-org/nagini@0.0.17/src/nagini.js
- http://127.0.0.1:5001/static/js/navbar-active-state.js
</details>

<details>
<summary>Click to expand HTML head snippet (first 2000 chars)</summary>

```html
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>
      
  
    Nagini - Python dans le navigateur pour l'éducation
  

    </title>
<link href="http://127.0.0.1:5001/static/favicon/apple-icon-57x57.png" rel="icon" type="image/x-icon"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&amp;family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&amp;family=Dancing+Script:wght@400..700&amp;family=EB+Garamond:ital,wght@0,400..800;1,400..800&amp;family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&amp;family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&amp;family=Lora:ital,wght@0,400..700;1,400..700&amp;family=Playfair+Display:ital,wght@0,400..900;1,400..900&amp;family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&amp;family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&amp;family=Playfair+Display:ital,wght@0,400..900;1,400..900&amp;display=swap" rel="stylesheet"/>
<script>
    // Suppress Tailwind production warning for development
    window.process = {
        env: {
            NODE_ENV: 'development'
        }
    };
</script>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<script type="tailwind-config">
    {
        plugins: [
            tailwind.plugin.typography,
        ],
    }
</script>
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css"/>
<link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css"/>
<link href="http://127.0.0.1:5001/static/css/root.css" rel="stylesheet"/>
<link href="http://127.0.0.1:5001/static/css/styles.css" rel="stylesheet"/
... (truncated)
```
</details>

<details>
<summary>Click to expand data-brick HTML</summary>

```html
<data-brick>
<div data-domain_specific_metatags.apple-mobile-web-app-capable="yes" data-domain_specific_metatags.apple-mobile-web-app-status-bar-style="black" data-domain_specific_metatags.apple-touch-fullscreen="yes" data-domain_specific_metatags.author="Maths.pm, contact@pointcarre.app" data-domain_specific_metatags.charset="UTF-8" data-domain_specific_metatags.classification="Education" data-domain_specific_metatags.copyright="SAS POINTCARRE.APP" data-domain_specific_metatags.coverage="Europe" data-domain_specific_metatags.designer="SAS POINTCARRE.APP" data-domain_specific_metatags.directory="education" data-domain_specific_metatags.distribution="Europe" data-domain_specific_metatags.format-detection="telephone=no" data-domain_specific_metatags.generator="HTML5" data-domain_specific_metatags.geo.placename="Paris" data-domain_specific_metatags.geo.region="FR-IDF" data-domain_specific_metatags.handheldfriendly="True" data-domain_specific_metatags.http-equiv-cache-control="no-cache" data-domain_specific_metatags.http-equiv-expires="0" data-domain_specific_metatags.http-equiv-imagetoolbar="no" data-domain_specific_metatags.http-equiv-pragma="no-cache" data-domain_specific_metatags.http-equiv-x-dns-prefetch-control="off" data-domain_specific_metatags.icbm="48.8566, 2.3522" data-domain_specific_metatags.language="FR" data-domain_specific_metatags.medium="website" data-domain_specific_metatags.mobile-web-app-capable="yes" data-domain_specific_metatags.mobileoptimized="320" data-d
... (truncated)
```
</details>

---

## 📋 Summary and Recommendations

### Current Implementation Analysis

The current template system (`main-alt.html`) correctly:
1. ✅ Loads domain-wide metatags from `DOMAIN_CONFIG.domain_specific_metatags`
2. ✅ Loads page defaults from `DOMAIN_CONFIG.index_view_specific_metatags`
3. ✅ Implements Smart Product Dependency Loader for backend settings
4. ✅ Includes `data-brick.html` for additional data injection

### 🚀 Proposed Refactoring: Lifespan Validation

Instead of runtime testing, implement validation at app startup:

```python
# In app.py or a new startup.py module
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Validate all settings
    from .settings import settings
    
    # 1. Verify domain config is loaded
    assert settings.domain_config.domain_url
    assert settings.domain_config.templating
    
    # 2. Verify products are loaded and have required fields
    for product in settings.products:
        assert product.name
        assert product.title_html
        # Verify product metatags if present
        if hasattr(product, 'metatags'):
            assert product.metatags.get('title')
    
    # 3. Pre-compile template context for validation
    context = {
        'DOMAIN_CONFIG': settings.domain_config.dict(),
        'products': settings.products,
        'backend_public_settings': settings.serialized_backend_settings
    }
    
    # 4. Log validation results
    logger.info(f'✅ Loaded {len(settings.products)} products')
    logger.info(f'✅ Domain config valid for {settings.domain_name}')
    
    yield  # App runs here
    
    # Shutdown: Cleanup if needed
    logger.info('Shutting down...')

app = FastAPI(lifespan=lifespan)
```

### Benefits of Lifespan Validation:
1. **Early Detection**: Settings errors caught at startup, not runtime
2. **Performance**: No validation overhead during requests
3. **Reliability**: App won't start with invalid configuration
4. **Observability**: Clear startup logs showing what's loaded
