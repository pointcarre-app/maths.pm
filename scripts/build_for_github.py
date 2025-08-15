#!/usr/bin/env python3
"""
GitHub Pages static site builder with HARDCODED routes.
This script explicitly builds ALL routes to ensure nothing is missed.
Specifically designed for deployment to https://pointcarre-app.github.io/maths.pm/
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


async def fetch_and_save(client, route, output_dir, base_path="/maths.pm"):
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
        if route == "/":
            output_path = output_dir / "index.html"
        elif route.endswith("/"):
            output_path = output_dir / route[1:] / "index.html"
        elif "." in route.split("/")[-1]:
            # Has extension - convert .md to .html for PM routes
            if route.endswith(".md") and route.startswith("/pm/"):
                output_path = output_dir / route[1:].replace(".md", ".html")
            else:
                output_path = output_dir / route[1:]
        else:
            # No extension, save as HTML
            output_path = output_dir / f"{route[1:]}.html"

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

            # Fix all absolute paths to include base_path
            if base_path:
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
                content = content.replace("from '@js/", f"from '{base_path}/static/js/")
                content = content.replace('from "@js/', f'from "{base_path}/static/js/')

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

    # Clean and create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Start server
    logger.info("Starting server...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(5)  # Wait for server to start

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Check server is running
        try:
            health = await client.get("http://127.0.0.1:8000/api/health")
            logger.info(f"Server running: {health.status_code}")
        except Exception as e:
            logger.error(f"Server not responding: {e}")
            return False

        # HARDCODED ROUTES - ALL OF THEM
        routes = []

        # Core routes
        routes.extend(
            [
                "/",  # CRITICAL - Main index
                "/readme",
                "/settings",
                "/kill-service-workers",
                "/pm",  # PM root
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
                route_path = f"/pm/{relative_path.as_posix()}"
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
            success = await fetch_and_save(client, route, output_dir)
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

        return True


if __name__ == "__main__":
    success = asyncio.run(build_static_site())
    sys.exit(0 if success else 1)
