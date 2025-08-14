#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Web Routes for Maths.pm Application
HTML pages and user-facing routes
"""

import markdown
from fastapi import APIRouter, Request, Query, HTTPException, Response
from pathlib import Path
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import JSONResponse
import mimetypes

from ..settings import settings, get_product_settings
from .pm.services.pm_runner import build_pm_from_file
from .pm.services.pm_fs_service import (
    build_pm_tree,
    resolve_pm_path,
    build_file_preview_data,
)


from typing import Any
import orjson


class ORJSONPrettyResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2,
        )


# Create sujets0 router
core_router = APIRouter(tags=["core"])

print(settings.products)


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


@core_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page - displays all resources for the current domain"""
    products_for_template = [p.to_template_context() for p in settings.products]
    return settings.templates.TemplateResponse(
        "index.html",
        {"request": request, "page": {"title": "Homepage"}, "products": products_for_template},
    )


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
    return settings.templates.TemplateResponse(
        "settings.html", {"request": request, "page": {"title": "Settings - Configuration"}}
    )


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
