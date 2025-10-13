#!/usr/bin/env python3
"""
Static site builder with HARDCODED routes for multiple deployment targets.
This script explicitly builds ALL routes to ensure nothing is missed.

Deployment targets:
- Modern (maths.pm): Clean URLs without /maths.pm prefix (DEFAULT)
- Legacy GitHub Pages: https://pointcarre-app.github.io/maths.pm/ (set LEGACY_GITHUB_PAGES=true)

Usage:
  # For modern deployment (maths.pm) - DEFAULT
  python scripts/build_for_github.py

  # For legacy GitHub Pages (pointcarre-app.github.io/maths.pm)
  LEGACY_GITHUB_PAGES=true python scripts/build_for_github.py
"""

import asyncio
import sys
import logging
import time
import threading
from pathlib import Path
import shutil
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from src import app
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_server():
    """Run the FastAPI server in a background thread"""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)


async def fetch_and_save(client, route, output_dir, base_path="/maths.pm", modern_paths=False):
    """Fetch a route and save it to disk with proper path conversion"""
    try:
        url = f"http://127.0.0.1:8000{route}"
        logger.info(f"Fetching: {route}")
        response = await client.get(url, follow_redirects=True)

        if response.status_code != 200:
            logger.error(f"Failed {route}: Status {response.status_code}")
            return False

        # Determine output path
        output_dir = Path(output_dir)

        # Remove query parameters from route for file path determination
        route_path = route.split("?")[0]

        if route_path == "/":
            output_path = output_dir / "index.html"
        elif route_path.endswith("/"):
            output_path = output_dir / route_path[1:] / "index.html"
        elif "." in route_path.split("/")[-1]:
            # Has extension - convert .md to .html for PM routes
            if route_path.endswith(".md") and route_path.startswith("/pm/"):
                output_path = output_dir / route_path[1:].replace(".md", ".html")
            else:
                output_path = output_dir / route_path[1:]
        else:
            # No extension, save as HTML
            output_path = output_dir / f"{route_path[1:]}.html"

        # Create parent directories
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Fix paths in HTML content
        if response.headers.get("content-type", "").startswith("text/html"):
            content = response.text

            # CRITICAL: Remove all localhost URLs first
            content = content.replace("http://127.0.0.1:8000/", "/")
            content = content.replace("http://localhost:8000/", "/")
            content = content.replace("https://127.0.0.1:8000/", "/")
            content = content.replace("https://localhost:8000/", "/")

            # Fix all absolute paths to include base_path (only for legacy GitHub Pages)
            if base_path and not modern_paths:
                # Legacy GitHub Pages deployment: add /maths.pm prefix
                content = content.replace('href="/', f'href="{base_path}/')
                content = content.replace("href='/", f"href='{base_path}/")
                content = content.replace('src="/', f'src="{base_path}/')
                content = content.replace("src='/", f"src='{base_path}/")
                content = content.replace('action="/', f'action="{base_path}/')

                # Fix imports
                content = content.replace("import '/static/", f"import '{base_path}/static/")
                content = content.replace('import "/static/', f'import "{base_path}/static/')
                content = content.replace("from '/static/", f"from '{base_path}/static/")
                content = content.replace('from "/static/', f'from "{base_path}/static/')

                # Fix PMRuntime import specifically
                content = content.replace(
                    "import PMRuntime from '/static/js/",
                    f"import PMRuntime from '{base_path}/static/js/",
                )
                content = content.replace(
                    'import PMRuntime from "/static/js/',
                    f'import PMRuntime from "{base_path}/static/js/',
                )
            # Modern deployment (maths.pm): keep original paths
            # No transformations needed - paths stay as /sujets0/form, /static/css/main.css, etc.

            # Convert PM links from .md to .html and remove ?format=html
            # This ensures links work in the static site
            content = content.replace('.md?format=html"', '.html"')
            content = content.replace(".md?format=html'", ".html'")
            content = content.replace('.md"', '.html"')  # Convert any remaining .md links
            content = content.replace(".md'", ".html'")

            output_path.write_text(content, encoding="utf-8")
        else:
            output_path.write_bytes(response.content)

        logger.info(f"✓ Saved: {output_path.relative_to(output_dir)}")
        return True

    except Exception as e:
        logger.error(f"✗ Failed {route}: {e}")
        return False


async def build_static_site():
    """Build the static site with ALL routes hardcoded"""

    output_dir = Path("dist")

    # Detect deployment type
    # DEFAULT: GitHub Pages with custom domain (maths.pm) - no /maths.pm prefix needed
    # LEGACY: Old GitHub Pages format (pointcarre-app.github.io/maths.pm) - needs /maths.pm prefix
    import os

    legacy_github_pages = os.environ.get("LEGACY_GITHUB_PAGES", "false").lower() == "true"

    if legacy_github_pages:
        logger.info(
            "📄 Legacy GitHub Pages deployment (pointcarre-app.github.io/maths.pm) - applying /maths.pm path transformations"
        )
        base_path = "/maths.pm"
        use_legacy_paths = True
    else:
        logger.info("🌐 Modern deployment (maths.pm) - using clean paths without /maths.pm prefix")
        base_path = ""  # No base path for modern deployment
        use_legacy_paths = False

    # Clean and create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Start server
    logger.info("Starting server...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to start with retries
    max_retries = 10
    retry_delay = 2
    server_ready = False

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i in range(max_retries):
            try:
                health = await client.get("http://127.0.0.1:8000/api/health")
                if health.status_code == 200:
                    logger.info(f"Server is ready (attempt {i + 1})")
                    server_ready = True
                    break
            except Exception:
                if i < max_retries - 1:
                    logger.info(f"Waiting for server... (attempt {i + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Server failed to start after {max_retries} attempts")

        if not server_ready:
            logger.error("Server is not responding - build cannot continue")
            sys.exit(1)

        # HARDCODED ROUTES - ALL OF THEM
        routes = []

        # Core routes
        routes.extend(
            [
                "/",  # CRITICAL - Main index
                "/ressources",
                "/readme",
                "/settings",
                "/sitemap.xml",  # SEO sitemap
                "/kill-service-workers",
                "/pm",  # PM root
                "/rgpd",
                "/identity",
            ]
        )

        # PM example/demo routes
        routes.extend(
            [
                "/dynamic-pm-demo",  # Dynamic PM loading demo
                "/simple-dynamic-demo",  # Simple dynamic PM demo
                # Add any other PM example routes here as needed
            ]
        )

        # API routes
        routes.extend(
            [
                "/api/health",
                "/api/settings",
                "/api/settings/serialized",
                "/openapi.json",
                "/docs",
                "/redoc",
            ]
        )

        # Product routes
        routes.extend(
            [
                "/sujets0",
                "/sujets0/form",
                "/corsica/",
                "/nagini",
            ]
        )

        # JupyterLite routes (may fail but try anyway)
        routes.extend(
            [
                "/jupyterlite/",
                "/jupyterlite/lab",
                "/jupyterlite/repl",
                "/jupyterlite/embed",
                "/jupyterlite/sandbox/repl",
                "/jupyter",
                "/jupyter/repl",
            ]
        )

        # HARDCODE ALL PM ROUTES FROM pms/ directory
        pms_dir = Path("pms")
        if pms_dir.exists():
            logger.info("Scanning pms/ directory for ALL files...")

            # Get ALL markdown files
            for md_file in pms_dir.rglob("*.md"):
                relative_path = md_file.relative_to(pms_dir)
                # Add ?format=html to get rendered HTML instead of raw markdown
                route_path = f"/pm/{relative_path.as_posix()}?format=html"
                routes.append(route_path)
                logger.info(f"  Added MD route: {route_path}")

            # Get ALL other files (SVG, HTML, etc.)
            for file_path in pms_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix != ".md":
                    relative_path = file_path.relative_to(pms_dir)
                    route_path = f"/pm/{relative_path.as_posix()}"
                    routes.append(route_path)
                    logger.info(f"  Added asset route: {route_path}")

        logger.info(f"Total routes to fetch: {len(routes)}")

        # Fetch all routes
        results = []
        for route in routes:
            success = await fetch_and_save(
                client, route, output_dir, base_path, not use_legacy_paths
            )
            results.append({"route": route, "success": success})

        # Copy static files DIRECTLY
        logger.info("Copying static files...")
        src_static = Path("src/static")
        dst_static = output_dir / "static"
        if src_static.exists():
            shutil.copytree(src_static, dst_static, dirs_exist_ok=True)
            logger.info(f"✓ Copied static files to {dst_static}")

        # Copy PM files DIRECTLY as fallback
        logger.info("Copying PM files directly as fallback...")
        src_pms = Path("pms")
        dst_pm = output_dir / "pm"
        if src_pms.exists():
            # Ensure pm directory exists
            dst_pm.mkdir(parents=True, exist_ok=True)
            # Copy entire pms directory content
            for item in src_pms.rglob("*"):
                if item.is_file():
                    relative = item.relative_to(src_pms)
                    dst_path = dst_pm / relative
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dst_path)
            logger.info(f"✓ Copied PM files to {dst_pm}")

        # Create .nojekyll
        (output_dir / ".nojekyll").touch()
        logger.info("✓ Created .nojekyll file")

        # Save build report
        successful = sum(1 for r in results if r["success"])
        failed = sum(1 for r in results if not r["success"])

        report = {
            "status": "success" if failed == 0 else "partial",
            "total_routes": len(results),
            "successful": successful,
            "failed": failed,
            "routes": results,
        }

        report_path = output_dir / "build-report.json"
        report_path.write_text(json.dumps(report, indent=2))

        logger.info("=" * 60)
        logger.info("BUILD COMPLETE")
        logger.info(f"  Total routes: {len(results)}")
        logger.info(f"  Successful: {successful}")
        logger.info(f"  Failed: {failed}")
        logger.info(f"  Output: {output_dir}")
        logger.info("=" * 60)

        # List what we actually have
        html_files = list(output_dir.rglob("*.html"))
        logger.info(f"HTML files created: {len(html_files)}")

        # Check critical files
        critical_files = [
            output_dir / "index.html",
            output_dir / "pm" / "corsica" / "a_troiz_geo.html",
            output_dir / "static" / "css" / "root.css",
        ]

        for file in critical_files:
            if file.exists():
                logger.info(f"✓ Critical file exists: {file.relative_to(output_dir)}")
            else:
                logger.error(f"✗ MISSING CRITICAL FILE: {file.relative_to(output_dir)}")

        # Generate optimized static sitemap after build
        logger.info("Generating optimized sitemap.xml...")
        generate_static_sitemap(output_dir, legacy_github_pages)

        return True


def generate_static_sitemap(output_dir: Path, legacy_mode: bool = False):
    """Generate a static sitemap.xml file optimized for SEO

    Args:
        output_dir: The dist directory where files are built
        legacy_mode: Whether this is for legacy GitHub Pages deployment
    """
    from datetime import datetime  # Import datetime here for the function

    # Determine base URL based on deployment type
    if legacy_mode:
        base_url = "https://pointcarre-app.github.io/maths.pm"
    else:
        # Modern deployment with custom domain
        base_url = "https://maths.pm"

    urls = []

    def add_url(path: str, priority: float = 0.5, changefreq: str = "weekly", lastmod: str = None):
        """Helper to add a URL to the sitemap"""
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
    if (output_dir / "index.html").exists():
        add_url("/", priority=1.0, changefreq="daily")
    if (output_dir / "ressources.html").exists():
        add_url("/ressources", priority=0.9, changefreq="weekly")

    # 2. Product pages (high priority)
    if (output_dir / "sujets0.html").exists():
        add_url(
            "/sujets0", priority=0.8, changefreq="weekly"
        )  # TODO sel : ensure make sense for changefreq
    if (output_dir / "sujets0/form.html").exists():
        add_url("/sujets0/form", priority=0.7, changefreq="weekly")
    if (output_dir / "corsica" / "index.html").exists():
        add_url("/corsica/", priority=0.8, changefreq="weekly")
    if (output_dir / "nagini.html").exists():
        add_url("/nagini", priority=0.8, changefreq="weekly")

    # 3. PM Documentation (scan actual built files)
    pm_dir = output_dir / "pm"
    if pm_dir.exists():
        # Add PM root
        add_url("/pm", priority=0.7, changefreq="weekly")

        # Scan for all HTML files in pm directory
        for html_file in pm_dir.rglob("*.html"):
            relative_path = html_file.relative_to(output_dir)

            # Get file modification time
            file_mtime = datetime.fromtimestamp(html_file.stat().st_mtime).strftime("%Y-%m-%d")

            # Construct URL path
            url_path = "/" + str(relative_path.with_suffix("")).replace("\\", "/")

            # Skip index.html files (use directory path instead)
            if html_file.name == "index.html":
                url_path = url_path.replace("/index", "")

            # Determine priority based on depth
            depth = len(relative_path.parts) - 1  # Subtract 1 for 'pm' directory
            priority = max(0.4, 0.7 - (depth * 0.1))

            # Special priority boost for certain products
            if "corsica" in str(relative_path):
                priority = min(0.8, priority + 0.1)
            elif "sujets0" in str(relative_path):
                priority = min(0.8, priority + 0.1)

            add_url(url_path, priority=priority, changefreq="monthly", lastmod=file_mtime)

    # 4. Utility pages (lower priority)
    if (output_dir / "readme.html").exists():
        add_url("/readme", priority=0.3, changefreq="monthly")
    if (output_dir / "settings.html").exists():
        add_url("/settings", priority=0.2, changefreq="monthly")
    if (output_dir / "kill-service-workers.html").exists():
        add_url("/kill-service-workers", priority=0.1, changefreq="yearly")

    # 5. Documentation pages
    if (output_dir / "docs.html").exists():
        add_url("/docs", priority=0.3, changefreq="monthly")
    if (output_dir / "redoc.html").exists():
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
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{chr(10).join(url_entries)}
</urlset>"""

    # Write sitemap file
    sitemap_path = output_dir / "sitemap.xml"
    sitemap_path.write_text(sitemap_content, encoding="utf-8")

    logger.info(f"✓ Generated sitemap.xml with {len(urls)} URLs")
    logger.info(f"  Base URL: {base_url}")
    logger.info(f"  Output: {sitemap_path}")

    # Also create robots.txt for better SEO
    robots_content = f"""# Robots.txt for maths.pm
User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml

# Crawl-delay (be nice to search engines)
Crawl-delay: 1

# Disallow certain paths
Disallow: /api/
Disallow: /kill-service-workers
Disallow: /_output/
Disallow: /env/
"""

    robots_path = output_dir / "robots.txt"
    robots_path.write_text(robots_content, encoding="utf-8")
    logger.info("✓ Generated robots.txt for SEO")


if __name__ == "__main__":
    success = asyncio.run(build_static_site())
    sys.exit(0 if success else 1)
