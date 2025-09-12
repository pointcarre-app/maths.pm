#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Web Routes for Maths.pm Application
HTML pages and user-facing routes
"""

import logging
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Any

import markdown
import orjson
from fastapi import APIRouter, Request, Query, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from ..settings import settings, get_product_settings
from .pm.services.pm_runner import build_pm_from_file
from .pm.services.pm_fs_service import (
    build_pm_tree,
    resolve_pm_path,
    build_file_preview_data,
)

# Get the logger
logger = logging.getLogger("maths_pm")


# Create sujets0 router
core_router = APIRouter(tags=["core"])


@core_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page - displays all resources for the current domain"""
    products_for_template = [p.to_template_context() for p in settings.products]
    return settings.templates.TemplateResponse(
        "index.html",
        {"request": request, "page": {"title": "Homepage"}, "products": products_for_template},
    )


@core_router.get("/ressources", response_class=HTMLResponse)
async def ressources(request: Request):
    """Main page - displays all resources for the current domain"""
    products_for_template = [p.to_template_context() for p in settings.products]
    return settings.templates.TemplateResponse(
        "ressources.html",
        {"request": request, "page": {"title": "Homepage"}, "products": products_for_template},
    )


@core_router.get("/sitemap.xml", response_class=Response)
async def sitemap(request: Request):
    """Generate XML sitemap for SEO - includes all PM files, product pages, and static routes"""

    # Get base URL from request
    base_url = str(request.base_url).rstrip("/")

    # Track all URLs
    urls = []

    # Helper to add URL with priority and changefreq
    def add_url(path: str, priority: float = 0.5, changefreq: str = "weekly", lastmod: str = None):
        if not lastmod:
            lastmod = datetime.now().strftime("%Y-%m-%d")

        # Ensure path starts with /
        if not path.startswith("/"):
            path = "/" + path

        urls.append(
            {
                "loc": f"{base_url}{path}",
                "lastmod": lastmod,
                "changefreq": changefreq,
                "priority": str(priority),
            }
        )

    # 1. Core pages (highest priority)
    add_url("/", priority=1.0, changefreq="daily")
    add_url("/ressources", priority=0.9, changefreq="weekly")

    # 2. Product pages (high priority)
    for product in settings.products:
        if not product.is_hidden:  # Include products that are not hidden
            # Add main product page
            add_url(f"/{product.name}", priority=0.8, changefreq="weekly")

            # Add special product routes if they exist
            if product.name == "sujets0":
                add_url("/sujets0/form", priority=0.7, changefreq="weekly")

    # 3. PM Documentation pages (medium-high priority)
    add_url("/pm", priority=0.7, changefreq="weekly")

    # Scan PM files from pms directory
    pms_dir = settings.base_dir / "pms"
    if pms_dir.exists():
        for pm_file in pms_dir.rglob("*.md"):
            relative_path = pm_file.relative_to(pms_dir)
            # Get file modification time
            file_mtime = datetime.fromtimestamp(pm_file.stat().st_mtime).strftime("%Y-%m-%d")

            # Determine priority based on depth and product
            depth = len(relative_path.parts)
            priority = max(0.4, 0.7 - (depth * 0.1))

            # Special priority for index files
            if pm_file.name == "index.md":
                priority = min(0.8, priority + 0.2)

            pm_path = f"/pm/{relative_path.as_posix()}"
            add_url(pm_path, priority=priority, changefreq="monthly", lastmod=file_mtime)

    # 4. Utility pages (lower priority)
    add_url("/readme", priority=0.3, changefreq="monthly")
    add_url("/settings", priority=0.2, changefreq="monthly")
    add_url("/kill-service-workers", priority=0.1, changefreq="yearly")

    # 5. API documentation (low priority)
    add_url("/docs", priority=0.3, changefreq="monthly")
    add_url("/redoc", priority=0.3, changefreq="monthly")

    # Generate XML content
    url_entries = []
    for url_data in urls:
        url_entries.append(f"""    <url>
        <loc>{url_data["loc"]}</loc>
        <lastmod>{url_data["lastmod"]}</lastmod>
        <changefreq>{url_data["changefreq"]}</changefreq>
        <priority>{url_data["priority"]}</priority>
    </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_entries)}
</urlset>"""

    return Response(
        content=sitemap_content,
        media_type="application/xml",
        headers={
            "Content-Type": "application/xml; charset=utf-8",
            "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
        },
    )


@core_router.get("/sitemap-readable", response_class=HTMLResponse)
async def sitemap_readable(request: Request):
    """Readable sitemap for humans - displays all site URLs organized by category."""

    # Get base URL from request
    base_url = str(request.base_url).rstrip("/")

    # Organize URLs by category
    sitemap_data = {
        "core_pages": [],
        "products": [],
        "pm_documentation": [],
        "utilities": [],
        "api_docs": [],
        "base_url": base_url,
    }

    # Helper to add URL with metadata
    def add_url(
        category: str,
        path: str,
        title: str = None,
        description: str = None,
        priority: float = 0.5,
        changefreq: str = "weekly",
        lastmod: str = None,
    ):
        if not lastmod:
            lastmod = datetime.now().strftime("%Y-%m-%d")

        # Ensure path starts with /
        if not path.startswith("/"):
            path = "/" + path

        # Generate title from path if not provided
        if not title:
            if path == "/":
                title = "Home"
            else:
                title = path.strip("/").replace("-", " ").replace("_", " ").title()

        sitemap_data[category].append(
            {
                "path": path,
                "url": f"{base_url}{path}",
                "title": title,
                "description": description,
                "lastmod": lastmod,
                "changefreq": changefreq,
                "priority": priority,
            }
        )

    # 1. Core pages (highest priority)
    add_url(
        "core_pages",
        "/",
        title="Home",
        description="Main landing page",
        priority=1.0,
        changefreq="daily",
    )
    add_url(
        "core_pages",
        "/ressources",
        title="Resources",
        description="Educational resources and materials",
        priority=0.9,
    )

    # 2. Product pages (high priority)
    for product in settings.products:
        if not product.is_hidden:
            # Format product title and description
            product_title = (
                product.display_name if hasattr(product, "display_name") else product.name.title()
            )
            product_desc = (
                product.description
                if hasattr(product, "description")
                else f"Explore {product_title}"
            )

            add_url(
                "products",
                f"/{product.name}",
                title=product_title,
                description=product_desc,
                priority=0.8,
            )

            # Add special product routes
            if product.name == "sujets0":
                add_url(
                    "products",
                    "/sujets0/form",
                    title="Sujets0 Form",
                    description="Generate custom practice materials",
                    priority=0.7,
                )

    # 3. PM Documentation pages
    add_url(
        "pm_documentation",
        "/pm",
        title="PM Documentation Hub",
        description="Central documentation for PM system",
        priority=0.7,
    )

    # Scan PM files from pms directory
    pms_dir = settings.base_dir / "pms"
    if pms_dir.exists():
        # Collect and sort PM files
        pm_files = []
        for pm_file in pms_dir.rglob("*.md"):
            relative_path = pm_file.relative_to(pms_dir)
            pm_files.append((relative_path, pm_file))

        # Sort by path for consistent ordering
        pm_files.sort(key=lambda x: str(x[0]))

        # Add first 50 PM files (to avoid overwhelming the page)
        for relative_path, pm_file in pm_files[:50]:
            file_mtime = datetime.fromtimestamp(pm_file.stat().st_mtime).strftime("%Y-%m-%d")

            # Generate title from filename
            file_title = pm_file.stem.replace("-", " ").replace("_", " ").title()

            # Determine priority
            depth = len(relative_path.parts)
            priority = max(0.4, 0.7 - (depth * 0.1))

            if pm_file.name == "index.md":
                file_title = f"{relative_path.parent.name.title()} Index"
                priority = min(0.8, priority + 0.2)

            pm_path = f"/pm/{relative_path.as_posix()}"
            add_url(
                "pm_documentation",
                pm_path,
                title=file_title,
                description=f"Documentation: {relative_path.parent}",
                priority=priority,
                changefreq="monthly",
                lastmod=file_mtime,
            )

        # Add note if there are more files
        total_pm_files = sum(1 for _ in pms_dir.rglob("*.md"))
        sitemap_data["pm_files_total"] = total_pm_files
        sitemap_data["pm_files_shown"] = len(pm_files[:50])

    # 4. Utility pages
    add_url(
        "utilities",
        "/readme",
        title="README",
        description="Project documentation and setup guide",
        priority=0.3,
        changefreq="monthly",
    )
    add_url(
        "utilities",
        "/settings",
        title="Settings",
        description="Application configuration viewer",
        priority=0.2,
        changefreq="monthly",
    )
    add_url(
        "utilities",
        "/kill-service-workers",
        title="Kill Service Workers",
        description="Utility to clear service worker cache",
        priority=0.1,
        changefreq="yearly",
    )

    # 5. API documentation
    add_url(
        "api_docs",
        "/docs",
        title="API Documentation (Swagger)",
        description="Interactive API documentation with Swagger UI",
        priority=0.3,
        changefreq="monthly",
    )
    add_url(
        "api_docs",
        "/redoc",
        title="API Documentation (ReDoc)",
        description="Alternative API documentation with ReDoc",
        priority=0.3,
        changefreq="monthly",
    )

    # Calculate totals
    sitemap_data["total_urls"] = sum(
        len(urls) for category, urls in sitemap_data.items() if isinstance(urls, list)
    )

    return settings.templates.TemplateResponse(
        "core/sitemap-readable.html",
        {
            "request": request,
            "sitemap_data": sitemap_data,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


@core_router.get("/sitemap-display", response_class=HTMLResponse)
async def plan_du_site(request: Request):
    """Simple sitemap for footer link - clean and minimal presentation."""

    # Organize URLs by category (simpler structure)
    sitemap_simple = {
        "main_sections": [],
        "products": [],
        "resources": [],
    }

    # Main sections
    sitemap_simple["main_sections"] = [
        {"path": "/", "title": "Accueil", "icon": "🏠"},
        {"path": "/ressources", "title": "Ressources", "icon": "📚"},
        {"path": "/pm", "title": "Accès aux documents PM", "icon": "📖"},
    ]

    # Products (only visible ones)
    for product in settings.products:
        if not product.is_hidden:
            product_title = (
                product.display_name if hasattr(product, "display_name") else product.name.title()
            )
            sitemap_simple["products"].append(
                {
                    "path": f"/{product.name}",
                    "title": product_title,
                    "icon": "🔧" if product.name in ["cubrick", "nagini", "estafette"] else "📝",
                }
            )

    # Additional resources
    sitemap_simple["resources"] = [
        {"path": "/readme", "title": "README", "icon": "📄"},
        {"path": "/settings", "title": "Configuration", "icon": "⚙️"},
        {"path": "/docs", "title": "API Docs", "icon": "🔌"},
        {"path": "/sitemap.xml", "title": "Sitemap XML", "icon": "🗺️"},
        {"path": "/sitemap-readable", "title": "Sitemap détaillé", "icon": "📋"},
    ]

    return settings.templates.TemplateResponse(
        "core/plan-du-site.html",
        {
            "request": request,
            "sitemap": sitemap_simple,
        },
    )


class ORJSONPrettyResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2,
        )


# Product configuration is already logged in settings.py


def _build_pm_tree(base_pms_dir: Path, root_dir: Path) -> dict:
    """Compatibility wrapper around the service function.

    Kept to avoid touching templates that call this helper name.
    """
    return build_pm_tree(base_pms_dir=base_pms_dir, root_dir=root_dir)


@core_router.get("/pm", response_class=HTMLResponse)
async def get_pm_root(request: Request):
    """Directory view for the PM root folder (pms/)."""
    base_pms_dir: Path = settings.base_dir / "pms"
    if not base_pms_dir.exists():
        raise HTTPException(status_code=404, detail="PM root folder not found")

    tree = _build_pm_tree(base_pms_dir=base_pms_dir, root_dir=base_pms_dir)
    context = {
        "request": request,
        "page": {"title": "PM Folder - root"},
        "product_name": None,
        "product_settings": None,
        "tree": tree,
    }
    return settings.templates.TemplateResponse("pm/dir.html", context)


# TODO : only when starting the app
@core_router.get("/readme", response_class=HTMLResponse)
async def readme(request: Request):
    """Display README.md (from root of repo) with DaisyUI prose styling"""
    readme_path = settings.base_dir / "README.md"

    if not readme_path.exists():
        return settings.templates.TemplateResponse(
            "readme.html",
            {
                "request": request,
                "page": {"title": "README"},
                "readme_content": "<p>README.md not found</p>",
                "error": True,
            },
        )

    # Read and convert markdown to HTML
    with open(readme_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        markdown_content, extensions=["codehilite", "fenced_code", "tables", "toc"]
    )

    return settings.templates.TemplateResponse(
        "readme.html",
        {
            "request": request,
            "page": {"title": "README - Documentation"},
            "readme_content": html_content,
            "error": False,
        },
    )


@core_router.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request):
    """Display all loaded product settings in a clean table format"""

    # Build unified settings table data
    unified_settings = []

    # 1. Domain settings - domain_specific_metatags
    for key, value in settings.domain_config.domain_specific_metatags.items():
        unified_settings.append(
            {
                "type": "domain",
                "source": "domains/maths.pm.yml",
                "category": "domain_specific_metatags",
                "key": key,
                "value": value,
                "used_in": "Toutes les pages (base/main-alt.html)",
                "description": _get_metatag_description(key),
            }
        )

    # 2. Domain settings - index_view_specific_metatags
    for key, value in settings.domain_config.index_view_specific_metatags.items():
        unified_settings.append(
            {
                "type": "domain",
                "source": "domains/maths.pm.yml",
                "category": "index_view_specific_metatags",
                "key": key,
                "value": value,
                "used_in": "Page d'accueil et fallback (base/main-alt.html)",
                "description": _get_metatag_description(key),
            }
        )

    # 3. Domain settings - templating
    for key, value in settings.domain_config.templating.dict().items():
        unified_settings.append(
            {
                "type": "domain",
                "source": "domains/maths.pm.yml",
                "category": "templating",
                "key": key,
                "value": value,
                "used_in": "Templates (navbar, footer, base)",
                "description": _get_template_description(key),
            }
        )

    # 4. Domain settings - extra_head
    if settings.domain_config.extra_head:
        for key, value in settings.domain_config.extra_head.dict().items():
            if value:  # Only include if not empty
                unified_settings.append(
                    {
                        "type": "domain",
                        "source": "domains/maths.pm.yml",
                        "category": "extra_head",
                        "key": key,
                        "value": value,
                        "used_in": "Head de toutes les pages (base/main-alt.html)",
                        "description": "Ressources externes JS/CSS",
                    }
                )

    # 5. Product settings
    for product in settings.products:
        # Backend settings
        if product.backend_settings:
            for key, value in product.backend_settings.items():
                unified_settings.append(
                    {
                        "type": "product",
                        "source": f"products/{product.name}.yml",
                        "category": "backend_settings",
                        "key": key,
                        "value": value,
                        "used_in": f"Routes /{product.name}/*, JavaScript",
                        "description": f"Configuration backend pour {product.title_html}",
                    }
                )

        # Metatags (if present)
        if hasattr(product, "metatags") and product.metatags:
            for key, value in product.metatags.items():
                unified_settings.append(
                    {
                        "type": "product",
                        "source": f"products/{product.name}.yml",
                        "category": "metatags",
                        "key": key,
                        "value": value,
                        "used_in": f"PM pages /{product.name}/* (pm/index.html)",
                        "description": _get_metatag_description(key),
                    }
                )

    return settings.templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "page": {"title": "Settings - Configuration"},
            "unified_settings": unified_settings,
        },
    )


def _get_metatag_description(key: str) -> str:
    """Get description for common metatag keys"""
    descriptions = {
        "title": "Titre de la page (SEO)",
        "description": "Description pour moteurs de recherche",
        "keywords": "Mots-clés SEO",
        "author": "Auteur du contenu",
        "robots": "Directives pour robots d'indexation",
        "og:title": "Titre pour partage social (Facebook)",
        "og:description": "Description pour partage social",
        "og:image": "Image pour partage social",
        "twitter:card": "Type de carte Twitter",
        "twitter:title": "Titre pour Twitter",
        "twitter:description": "Description pour Twitter",
        "viewport": "Configuration d'affichage mobile",
        "theme-color": "Couleur du thème mobile",
        "copyright": "Information de copyright",
        "language": "Langue du contenu",
        "Classification": "Classification du site",
        "rating": "Classification d'âge",
    }
    return descriptions.get(key, "Métadonnée personnalisée")


def _get_template_description(key: str) -> str:
    """Get description for template configuration keys"""
    descriptions = {
        "base_template": "Template HTML de base",
        "footer_template": "Template du pied de page",
        "navbar_title": "Titre affiché dans la navbar",
        "button_primary_text": "Texte du bouton principal",
        "button_primary_href": "Lien du bouton principal",
        "button_ghost_text": "Texte du bouton secondaire",
        "button_ghost_href": "Lien du bouton secondaire",
    }
    return descriptions.get(key, "Configuration de template")


# TODO : make better cause can be very very useful
@core_router.get("/kill-service-workers", response_class=HTMLResponse)
async def kill_service_workers(request: Request):
    """Emergency service worker elimination tool (pyodide / jupyterlite ...)"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 Service Worker Elimination</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { display: inline-block; background: #d32f2f; color: white; padding: 15px 30px; text-decoration: none; border-radius: 4px; margin: 10px; cursor: pointer; border: none; font-size: 16px; }
            .btn:hover { background: #c62828; }
            .btn.safe { background: #1976d2; }
            .btn.safe:hover { background: #1565c0; }
            #status { background: #f5f5f5; padding: 15px; border-radius: 4px; margin: 20px 0; height: 300px; overflow-y: scroll; font-family: monospace; font-size: 12px; }
            .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Service Worker Elimination Tool</h1>
            
            <div class="warning">
                <strong>⚠️ WARNING:</strong> JupyterLite service workers are interfering with your entire site!<br>
                This tool will completely eliminate all service workers and caches to fix the problem.
            </div>

            <button class="btn" onclick="killEverything()">💀 ELIMINATE ALL SERVICE WORKERS</button>
            <button class="btn safe" onclick="checkStatus()">📊 Check Current Status</button>
            
            <div id="status"></div>
            
            <h3>🔗 Test After Cleanup:</h3>
            <a href="/" class="btn safe">🏠 Home (should be clean)</a>
            <a href="/sujets0" class="btn safe">📚 Sujets0 (should be clean)</a>
        </div>

        <script>
        function log(msg) {
            const status = document.getElementById('status');
            const timestamp = new Date().toLocaleTimeString();
            status.innerHTML += `[${timestamp}] ${msg}<br>`;
            status.scrollTop = status.scrollHeight;
            console.log(msg);
        }
        
        async function checkStatus() {
            log('🔍 Checking service worker status...');
            
            if ('serviceWorker' in navigator) {
                try {
                    const registrations = await navigator.serviceWorker.getRegistrations();
                    log(`📊 Found ${registrations.length} active service workers:`);
                    
                    registrations.forEach((reg, index) => {
                        log(`  ${index + 1}. Scope: ${reg.scope}`);
                        log(`     State: ${reg.active?.state || 'inactive'}`);
                        log(`     Script: ${reg.active?.scriptURL || 'unknown'}`);
                    });
                    
                    if (registrations.length === 0) {
                        log('✅ No service workers found - site is clean!');
                    }
                } catch (error) {
                    log(`❌ Error checking status: ${error}`);
                }
            } else {
                log('ℹ️ Service workers not supported');
            }
            
            // Check caches
            if ('caches' in window) {
                try {
                    const cacheNames = await caches.keys();
                    log(`📦 Found ${cacheNames.length} caches: ${cacheNames.join(', ')}`);
                } catch (error) {
                    log(`❌ Error checking caches: ${error}`);
                }
            }
        }
        
        async function killEverything() {
            log('🚀 Starting COMPLETE ELIMINATION...');
            log('');
            
            // 1. Kill all service workers
            if ('serviceWorker' in navigator) {
                try {
                    const registrations = await navigator.serviceWorker.getRegistrations();
                    log(`💀 Eliminating ${registrations.length} service workers...`);
                    
                    for (const registration of registrations) {
                        log(`  💀 Killing: ${registration.scope}`);
                        await registration.unregister();
                    }
                    log('✅ All service workers ELIMINATED');
                } catch (error) {
                    log(`❌ Error eliminating service workers: ${error}`);
                }
            }
            
            // 2. Clear all caches
            if ('caches' in window) {
                try {
                    const cacheNames = await caches.keys();
                    log(`🧹 Clearing ${cacheNames.length} caches...`);
                    
                    for (const cacheName of cacheNames) {
                        log(`  🧹 Clearing: ${cacheName}`);
                        await caches.delete(cacheName);
                    }
                    log('✅ All caches CLEARED');
                } catch (error) {
                    log(`❌ Error clearing caches: ${error}`);
                }
            }
            
            // 3. Clear storage
            try {
                localStorage.clear();
                sessionStorage.clear();
                log('✅ Local storage CLEARED');
            } catch (error) {
                log(`❌ Error clearing storage: ${error}`);
            }
            
            log('');
            log('🎉 COMPLETE ELIMINATION FINISHED!');
            log('🔄 Your site should now be completely clean');
            log('📝 Test the links below to verify');
            
            if (confirm('🎉 Complete elimination finished!\\n\\nRefresh the page to see clean results?')) {
                window.location.reload();
            }
        }
        
        // Auto-check on load
        window.onload = function() {
            log('🔧 Service Worker Elimination Tool loaded');
            log('📊 Checking current status...');
            checkStatus();
        };
        </script>
    </body>
    </html>
    """)


@core_router.get("/pm/{origin:path}")
async def get_pm(
    request: Request,
    origin: str,
    format: str = Query(
        "html", description="Response format (json or html)", regex="^(json|html)$"
    ),
    debug: bool = Query(False, description="Debug mode"),
) -> Response:
    """Get a PM from a markdown file.

    Args:
        request: The request object
        origin: Path to the markdown file (first part is treated as product name)
        format: Response format ('json' or 'html')

    Returns:
        JSON representation of the PM or template response

    Examples:
        - `/pm/corsica/a_surface.md` - HTML view with corsica product settings
        - `/pm/pyly/index.md` - HTML view with pyly product settings
        - `/pm/pyly/index.md?format=json` - JSON data of Python curriculum
        - `/pm/pyly/index.md?format=html` - Explicit HTML format

    """
    # Extract product name from the first part of the origin path
    origin_parts = origin.split("/")
    product_name = origin_parts[0] if origin_parts else ""
    # print("product_name")
    # print("product_name")
    # print("product_name")
    # print("product_name")
    # print("product_name")
    # print("product_name")
    # print("product_name")
    # print(product_name)
    # Get product-specific settings dynamically
    product_settings = get_product_settings(product_name) if product_name else None

    # Build path from origin - for now assume it's relative to pms/ directory
    # This can be made configurable later
    # TODO sel: OK for now but
    pm_path = resolve_pm_path(origin, settings.base_dir)

    if not pm_path.exists():
        raise HTTPException(status_code=404, detail=f"PM file not found: {origin}")

    # If path is a directory, render a tree view of its contents
    if pm_path.is_dir():
        root_dir: Path = pm_path
        base_pms_dir: Path = settings.base_dir / "pms"
        tree = _build_pm_tree(base_pms_dir=base_pms_dir, root_dir=root_dir)

        context = {
            "request": request,
            "page": {"title": f"PM Folder - {tree['rel_path']}"},
            "product_name": product_name,
            "product_settings": product_settings.to_dict() if product_settings else None,
            "tree": tree,
        }
        return settings.templates.TemplateResponse("pm/dir.html", context)

    # Serve non-markdown files directly (images, data, etc.)
    if pm_path.is_file() and pm_path.suffix.lower() != ".md":
        media_type, _ = mimetypes.guess_type(str(pm_path))

        # Raw mode keeps previous behavior (direct file response)
        if format == "raw":
            return FileResponse(str(pm_path), media_type=media_type, filename=pm_path.name)

        # Otherwise render a simple preview page that embeds the asset
        preview_data = build_file_preview_data(
            path=pm_path, origin=origin, base_dir=settings.base_dir
        )

        context = {
            "request": request,
            "page": {"title": f"File - {pm_path.name}"},
            "product_name": product_name,
            "product_settings": product_settings.to_dict() if product_settings else None,
            **preview_data,
        }
        return settings.templates.TemplateResponse("pm/file.html", context)

    # Regular file rendering for markdown
    pm = build_pm_from_file(str(pm_path), verbosity=0)

    if format == "json":
        # Include product settings in JSON response if available
        response_data = pm.model_dump()
        if product_settings:
            response_data["product_settings"] = product_settings.to_dict()
        return ORJSONPrettyResponse(content=response_data)

    elif format == "html":
        # Convert PM to JSON-compatible dict using Pydantic's json method
        pm_json = pm.model_dump_json()

        # Build template context with product settings
        context = {
            "request": request,
            "debug": debug,
            "pm": pm,
            "pm_json": pm_json,
            "origin": origin,
            "product_name": product_name,
            "page": {"title": f"PM - {pm.title}"},
        }

        # Extract page-specific metatags from PM metadata
        pm_metatags = {}
        if pm.metadata:
            # Common metatags that might be in PM files
            metatag_fields = [
                "title",
                "description",
                "keywords",
                "author",
                "robots",
                "og:title",
                "og:description",
                "og:image",
                "og:url",
                "og:type",
                "twitter:card",
                "twitter:title",
                "twitter:description",
                "twitter:image",
                "DC.title",
                "DC.creator",
                "DC.subject",
                "DC.description",
                "abstract",
                "topic",
                "summary",
                "category",
                "revised",
                "pagename",
                "subtitle",
                "canonical",
            ]

            # Extract any metatag fields from metadata
            for field in metatag_fields:
                if field in pm.metadata:
                    pm_metatags[field] = pm.metadata[field]

            # Also extract any fields that start with common metatag prefixes
            for key, value in pm.metadata.items():
                if any(key.startswith(prefix) for prefix in ["og:", "twitter:", "DC.", "itemprop"]):
                    pm_metatags[key] = value

        # Add PM metatags to context
        context["pm_metatags"] = pm_metatags

        # Add product-specific context if settings are available
        if product_settings:
            context.update(
                {
                    "product_settings": product_settings.to_dict(),
                    "product_title": product_settings.title,
                    "product_description": product_settings.description,
                    "product_backend_settings": product_settings.backend_settings,
                    "is_product_enabled": product_settings.is_enabled,
                }
            )

        return settings.templates.TemplateResponse("pm/index.html", context)


@core_router.get("/identity", response_class=HTMLResponse)
async def identity(request: Request):
    """HTML interface for frontend execution with logs."""
    return settings.templates.TemplateResponse("identity/index.html", {"request": request})


@core_router.get("/rgpd", response_class=HTMLResponse)
async def rgpd(request: Request):
    """HTML interface for frontend execution with logs."""
    return settings.templates.TemplateResponse("core/rgpd.html", {"request": request})
