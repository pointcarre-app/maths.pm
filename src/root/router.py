#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Web Routes for Maths.pm Application
HTML pages and user-facing routes
"""

import markdown
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings

# Create sujets0 router
root_router = APIRouter(tags=["root"])


@root_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page - displays all resources"""
    products_for_template = [p.to_template_context() for p in settings.products]
    return settings.templates.TemplateResponse(
        "index.html", {"request": request, "page": {"title": "Homepage"}, "products": products_for_template}
    )


@root_router.get("/readme", response_class=HTMLResponse)
async def readme(request: Request):
    """Display README.md with DaisyUI prose styling"""
    readme_path = settings.base_dir / "README.md"
    
    if not readme_path.exists():
        return settings.templates.TemplateResponse(
            "readme.html", 
            {
                "request": request, 
                "page": {"title": "README"}, 
                "readme_content": "<p>README.md not found</p>",
                "error": True
            }
        )
    
    # Read and convert markdown to HTML
    with open(readme_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        markdown_content, 
        extensions=['codehilite', 'fenced_code', 'tables', 'toc']
    )
    
    return settings.templates.TemplateResponse(
        "readme.html", 
        {
            "request": request, 
            "page": {"title": "README - Documentation"}, 
            "readme_content": html_content,
            "error": False
        }
    )


@root_router.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request):
    """Display all loaded product settings in a clean table format"""
    return settings.templates.TemplateResponse(
        "settings.html", 
        {
            "request": request, 
            "page": {"title": "Settings - Configuration"}
        }
    )


@root_router.get("/kill-service-workers", response_class=HTMLResponse)
async def kill_service_workers(request: Request):
    """Emergency service worker elimination tool"""
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