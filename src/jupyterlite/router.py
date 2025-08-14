#!/usr/bin/env python3
"""
JupyterLite router for Maths.pm FastAPI application
Provides routes for JupyterLite Lab, REPL, and embedded views
Uses product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from ..settings import settings, jupyterlite_settings

jupyterlite_router = APIRouter(prefix="/jupyterlite", tags=["jupyterlite"])


@jupyterlite_router.get("/")
async def jupyterlite_index(request: Request):
    """JupyterLite main page - redirect to lab by default"""
    return RedirectResponse(url="/jupyterlite/lab", status_code=302)


@jupyterlite_router.get("/lab")
async def jupyterlite_lab(request: Request):
    """
    JupyterLite notebook interface - redirect to static files.

    Uses jupyterlite_settings for product-specific configuration.
    All settings are loaded automatically in settings.py.
    """
    try:
        # Get JupyterLite specific settings (simplified)
        jupyter_config = {"enabled": "Unknown", "version": "Unknown", "kernels": []}
        if jupyterlite_settings:
            jupyter_config = {
                "enabled": jupyterlite_settings.get_nested_setting("jupyterlite", "enabled", True),
                "version": jupyterlite_settings.get_nested_setting(
                    "jupyterlite", "version", "0.4.3"
                ),
                "kernels": jupyterlite_settings.get_nested_setting(
                    "jupyterlite", "kernels", ["python"]
                ),
            }

        # Check if JupyterLite assets exist and are properly configured
        output_dir = settings.jupyterlite_dir / "_output"
        lab_index = output_dir / "lab" / "index.html"

        if not lab_index.exists():
            return HTMLResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>JupyterLite - Setup Required</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #d32f2f; }}
                    .status {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin: 20px 0; }}
                    .btn {{ display: inline-block; background: #1976d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 15px; }}
                    .btn:hover {{ background: #1565c0; }}
                    pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; font-size: 12px; }}
                    .config {{ background: #e3f2fd; padding: 10px; border-radius: 4px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔧 JupyterLite Building...</h1>
                    <div class="status">
                        <strong>Status:</strong> JupyterLite is being built automatically.
                    </div>
                    
                    <div class="config">
                        <strong>🎯 Product Configuration:</strong><br>
                        Enabled: {jupyter_config.get("enabled", "Unknown")}<br>
                        Version: {jupyter_config.get("version", "Unknown")}<br>
                        Kernels: {", ".join(str(k) for k in jupyter_config.get("kernels", []))}
                    </div>
                    
                    <p>JupyterLite is enabled and auto-installation is running in the background.</p>
                    <h3>What's happening:</h3>
                    <ul>
                        <li>📦 Installing JupyterLite packages</li>
                        <li>🔨 Building JupyterLite from content in <code>files-for-lite/</code></li>
                        <li>📁 Creating Lab and REPL interfaces</li>
                        <li>⚙️ Setting up Python kernel with Pyodide</li>
                    </ul>
                    <p><strong>Expected files:</strong></p>
                    <pre>src/static/jupyterlite/_output/
├── lab/index.html      (Full Jupyter Lab)
├── repl/index.html     (Python REPL)
├── files/              (Your notebooks)
└── build/              (Assets)</pre>
                    <p><strong>Please wait a moment and refresh the page.</strong></p>
                    <a href="/" class="btn">← Back to Main Page</a>
                    <a href="/sujets0" class="btn">Try Sujets0 Instead</a>
                    <a href="/jupyterlite/lab" class="btn">🔄 Refresh</a>
                </div>
            </body>
            </html>
            """)

        # Redirect to the actual JupyterLite lab interface
        return RedirectResponse(url="/static/jupyterlite/_output/lab/index.html", status_code=302)

    except Exception as e:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>JupyterLite - Error</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #d32f2f; }}
                .error {{ background: #ffebee; border: 1px solid #ffcdd2; padding: 15px; border-radius: 4px; margin: 20px 0; }}
                .btn {{ display: inline-block; background: #1976d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 15px; }}
                .btn:hover {{ background: #1565c0; }}
                pre {{ background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ JupyterLite Error</h1>
                <div class="error">
                    <strong>Error:</strong> {str(e)}
                </div>
                <h3>Error Details:</h3>
                <pre>{repr(e)}</pre>
                <p>Try restarting the server to trigger a fresh build.</p>
                <a href="/" class="btn">← Back to Main Page</a>
            </div>
        </body>
        </html>
        """)


@jupyterlite_router.get("/repl")
async def jupyterlite_repl(request: Request):
    """JupyterLite REPL interface - redirect to static files"""
    try:
        output_dir = settings.jupyterlite_dir / "_output"
        repl_index = output_dir / "repl" / "index.html"

        if not repl_index.exists():
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>JupyterLite REPL - Setup Required</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    h1 { color: #d32f2f; }
                    .status { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 4px; margin: 20px 0; }
                    .btn { display: inline-block; background: #1976d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-top: 15px; }
                    .btn:hover { background: #1565c0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔧 JupyterLite REPL Building...</h1>
                    <div class="status">
                        <strong>Status:</strong> JupyterLite REPL is being built automatically.
                    </div>
                    <p>Please wait for the build to complete and try again.</p>
                    <a href="/jupyterlite/lab" class="btn">← Back to Lab</a>
                    <a href="/" class="btn">← Back to Main Page</a>
                    <a href="/jupyterlite/repl" class="btn">🔄 Refresh</a>
                </div>
            </body>
            </html>
            """)

        # Redirect to the actual JupyterLite REPL interface
        return RedirectResponse(url="/static/jupyterlite/_output/repl/index.html", status_code=302)

    except Exception as e:
        return HTMLResponse(f"<h1>Error loading REPL: {str(e)}</h1>")


@jupyterlite_router.get("/embed")
async def jupyterlite_embed(request: Request):
    """JupyterLite embedded view with both Lab and REPL in iframes"""
    # Build template context with product-specific settings
    context = {
        "request": request,
        "page": {"title": "JupyterLite - Demo"},
    }

    # Add product-specific context if available
    if jupyterlite_settings:
        context.update(
            {
                "product_name": jupyterlite_settings.name,
                "product_title": jupyterlite_settings.title,
                "jupyter_config": jupyterlite_settings.get_setting("jupyterlite", {}),
            }
        )

    return settings.templates.TemplateResponse("jupyterlite/sandbox/embed.html", context)


@jupyterlite_router.get("/sandbox/repl")
async def jupyterlite_sandbox_repl(request: Request):
    """JupyterLite REPL in a dedicated sandbox page"""
    return settings.templates.TemplateResponse(
        "jupyterlite/sandbox/repl.html", {"request": request}
    )


# Backward compatibility routes
from fastapi import APIRouter

# Create a separate router for backward compatibility
jupyter_compat_router = APIRouter(tags=["jupyter-compat"])


@jupyter_compat_router.get("/jupyter")
async def jupyter_redirect(request: Request):
    """Backward compatibility: redirect /jupyter to /jupyterlite/lab"""
    return RedirectResponse(url="/jupyterlite/lab", status_code=301)


@jupyter_compat_router.get("/jupyter/repl")
async def jupyter_repl_redirect(request: Request):
    """Backward compatibility: redirect /jupyter/repl to /jupyterlite/repl"""
    return RedirectResponse(url="/jupyterlite/repl", status_code=301)


@jupyterlite_router.get("/debug/service-worker")
async def debug_service_worker(request: Request):
    """Debug service worker issues"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>JupyterLite Service Worker Debug</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { display: inline-block; background: #1976d2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin: 5px; cursor: pointer; border: none; }
            .btn:hover { background: #1565c0; }
            .btn.danger { background: #d32f2f; }
            .btn.danger:hover { background: #c62828; }
            .status { background: #e3f2fd; border: 1px solid #2196f3; padding: 15px; border-radius: 4px; margin: 20px 0; }
            .error { background: #ffebee; border: 1px solid #f44336; }
            .success { background: #e8f5e8; border: 1px solid #4caf50; }
            pre { background: #f5f5f5; padding: 10px; border-radius: 4px; font-size: 12px; overflow-x: auto; }
            #log { height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; background: #fafafa; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 JupyterLite Service Worker Debug</h1>
            
            <div class="status">
                <strong>Current Server:</strong> <span id="currentServer"></span><br>
                <strong>Expected JupyterLite URL:</strong> <span id="expectedUrl"></span>
            </div>

            <h3>🛠️ Quick Fixes</h3>
            <button class="btn" onclick="checkStatus()">📊 Check Status</button>
            <button class="btn danger" onclick="clearServiceWorkers()">🗑️ Clear Service Workers</button>
            <button class="btn danger" onclick="clearCaches()">🧹 Clear Caches</button>
            <button class="btn danger" onclick="completeCleanup()">🔄 Complete Cleanup</button>
            <button class="btn" onclick="testJupyterLite()">🧪 Test JupyterLite</button>

            <h3>📋 Debug Log</h3>
            <div id="log"></div>

            <h3>🔗 Links</h3>
            <a href="/jupyterlite/lab" class="btn">🔬 JupyterLite Lab</a>
            <a href="/jupyterlite/repl" class="btn">💻 JupyterLite REPL</a>
            <a href="/" class="btn">🏠 Home</a>
        </div>

        <script type="module">
            import { ServiceWorkerFix } from '/static/js/utils/service-worker-fix.js';

            // Initialize
            document.getElementById('currentServer').textContent = window.location.origin;
            document.getElementById('expectedUrl').textContent = window.location.origin + '/static/jupyterlite/_output/lab/index.html';

            function log(message) {
                const logDiv = document.getElementById('log');
                const timestamp = new Date().toLocaleTimeString();
                logDiv.innerHTML += `[${timestamp}] ${message}<br>`;
                logDiv.scrollTop = logDiv.scrollHeight;
                console.log(message);
            }

            window.checkStatus = async function() {
                log('🔍 Checking service worker status...');
                await ServiceWorkerFix.checkServiceWorkerStatus();
                log('✅ Status check complete (see console for details)');
            };

            window.clearServiceWorkers = async function() {
                log('🗑️ Clearing service workers...');
                const result = await ServiceWorkerFix.unregisterAllServiceWorkers();
                log(result ? '✅ Service workers cleared' : '❌ Failed to clear service workers');
            };

            window.clearCaches = async function() {
                log('🧹 Clearing caches...');
                const result = await ServiceWorkerFix.clearAllCaches();
                log(result ? '✅ Caches cleared' : '❌ Failed to clear caches');
            };

            window.completeCleanup = async function() {
                log('🔄 Starting complete cleanup...');
                const result = await ServiceWorkerFix.completeCleanup();
                if (result) {
                    log('🎉 Complete cleanup successful!');
                    if (confirm('Cleanup complete! Reload the page now?')) {
                        window.location.reload();
                    }
                } else {
                    log('⚠️ Cleanup partially successful. Try manual browser cache clear.');
                }
            };

            window.testJupyterLite = async function() {
                log('🧪 Testing JupyterLite access...');
                try {
                    const response = await fetch('/static/jupyterlite/_output/lab/index.html');
                    if (response.ok) {
                        log('✅ JupyterLite Lab accessible');
                    } else {
                        log(`❌ JupyterLite Lab not accessible: ${response.status}`);
                    }
                } catch (error) {
                    log(`❌ JupyterLite test failed: ${error.message}`);
                }
            };

            // Auto-check on load
            log('🚀 Service Worker Debug Tool loaded');
            checkStatus();
        </script>
    </body>
    </html>
    """)
