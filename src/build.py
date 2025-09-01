#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Static site builder for maths.pm
Generates static HTML files from the FastAPI application
"""

import json
import shutil
from pathlib import Path
from typing import Dict
import httpx
import logging

logger = logging.getLogger(__name__)


class StaticSiteBuilder:
    """Builds static site from FastAPI routes"""

    def __init__(
        self, base_url: str = "http://localhost:8000", output_dir: str = "dist", base_path: str = ""
    ):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.client = None
        self.base_path = base_path  # For GitHub Pages, this would be "/repository-name"

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def fetch_and_save(self, path: str, output_path: Path = None) -> bool:
        """Fetch a route and save to disk"""
        try:
            url = f"{self.base_url}{path}"
            response = await self.client.get(url)
            response.raise_for_status()

            # Determine output path
            if output_path is None:
                if path == "/":
                    output_path = self.output_dir / "index.html"
                elif path.endswith("/"):
                    output_path = self.output_dir / path[1:] / "index.html"
                elif "." in path.split("/")[-1]:
                    # Has extension - but convert .md to .html for PM routes
                    if path.endswith(".md") and path.startswith("/pm/"):
                        # PM markdown files should be saved as HTML
                        output_path = self.output_dir / path[1:].replace(".md", ".html")
                    else:
                        output_path = self.output_dir / path[1:]
                else:
                    # No extension, treat as HTML
                    output_path = (
                        self.output_dir / f"{path[1:]}.html"
                        if path != "/"
                        else self.output_dir / "index.html"
                    )

            # Create parent directories
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save content
            if response.headers.get("content-type", "").startswith("application/json"):
                output_path = output_path.with_suffix(".json")
                output_path.write_text(response.text, encoding="utf-8")
            else:
                content = response.content

                # Fix absolute URLs in HTML files
                if response.headers.get("content-type", "").startswith("text/html"):
                    content_str = content.decode("utf-8")

                    # Remove all server URLs (handle all internal links)
                    content_str = content_str.replace("http://127.0.0.1:8000/", "/")
                    content_str = content_str.replace("http://localhost:8000/", "/")
                    content_str = content_str.replace("//127.0.0.1:8000/", "/")

                    # Fix PM route links - change .md to .html
                    content_str = content_str.replace('.md?format=html"', '.html"')
                    content_str = content_str.replace(".md?format=html'", ".html'")
                    content_str = content_str.replace('.md"', '.html"')
                    content_str = content_str.replace(".md'", ".html'")

                    # IMPORTANT: For GitHub Pages, we need to handle the repository path
                    # The site is served at /maths.pm/ so absolute paths need this prefix

                    # First, add the GitHub Pages base path to all absolute URLs
                    if self.base_path:
                        # For GitHub Pages deployment, prepend the base path
                        content_str = content_str.replace('href="/', f'href="{self.base_path}/')
                        content_str = content_str.replace("href='/", f"href='{self.base_path}/")
                        content_str = content_str.replace('src="/', f'src="{self.base_path}/')
                        content_str = content_str.replace("src='/", f"src='{self.base_path}/")
                        content_str = content_str.replace('action="/', f'action="{self.base_path}/')

                        # Fix JavaScript import statements
                        content_str = content_str.replace(
                            "import '/static/", f"import '{self.base_path}/static/"
                        )
                        content_str = content_str.replace(
                            'import "/static/', f'import "{self.base_path}/static/'
                        )
                        content_str = content_str.replace(
                            "from '/static/", f"from '{self.base_path}/static/"
                        )
                        content_str = content_str.replace(
                            'from "/static/', f'from "{self.base_path}/static/'
                        )

                        # Fix @js alias in imports
                        content_str = content_str.replace(
                            "from '@js/", f"from '{self.base_path}/static/js/"
                        )
                        content_str = content_str.replace(
                            'from "@js/', f'from "{self.base_path}/static/js/'
                        )
                        content_str = content_str.replace(
                            "import '@js/", f"import '{self.base_path}/static/js/"
                        )
                        content_str = content_str.replace(
                            'import "@js/', f'import "{self.base_path}/static/js/'
                        )
                    else:
                        # For local testing, use relative paths
                        depth = len(Path(path).parts) - 1
                        if depth > 0:
                            # Create relative path prefix
                            prefix = "../" * depth
                            # Replace all absolute paths with relative ones
                            content_str = content_str.replace('href="/', f'href="{prefix}')
                            content_str = content_str.replace("href='/", f"href='{prefix}")
                            content_str = content_str.replace('src="/', f'src="{prefix}')
                            content_str = content_str.replace("src='/", f"src='{prefix}")
                            content_str = content_str.replace('action="/', f'action="{prefix}')

                            # Fix JavaScript import statements for local testing
                            content_str = content_str.replace(
                                "import '/static/", f"import '{prefix}static/"
                            )
                            content_str = content_str.replace(
                                'import "/static/', f'import "{prefix}static/'
                            )
                            content_str = content_str.replace(
                                "from '/static/", f"from '{prefix}static/"
                            )
                            content_str = content_str.replace(
                                'from "/static/', f'from "{prefix}static/'
                            )
                            content_str = content_str.replace(
                                "from '@js/", f"from '{prefix}static/js/"
                            )
                            content_str = content_str.replace(
                                'from "@js/', f'from "{prefix}static/js/'
                            )
                        else:
                            # For root level files, remove leading slashes
                            content_str = content_str.replace('href="/', 'href="')
                            content_str = content_str.replace("href='/", "href='")
                            content_str = content_str.replace('src="/', 'src="')
                            content_str = content_str.replace("src='/", "src='")
                            content_str = content_str.replace('action="/', 'action="')

                            # Fix imports for root level
                            content_str = content_str.replace("import '/static/", "import 'static/")
                            content_str = content_str.replace('import "/static/', 'import "static/')
                            content_str = content_str.replace("from '@js/", "from 'static/js/")
                            content_str = content_str.replace('from "@js/', 'from "static/js/')

                    content = content_str.encode("utf-8")

                output_path.write_bytes(content)

            logger.info(f"✓ Saved {path} → {output_path.relative_to(self.output_dir)}")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to fetch {path}: {e}")
            return False

    def _generate_pm_routes(self) -> tuple:
        """Dynamically generate routes for all files in pms/ directory

        Returns:
            tuple: (markdown_routes, asset_routes)
                   markdown_routes: List of .md file routes
                   asset_routes: List of other asset file routes (svg, html, etc.)
        """
        markdown_routes = []
        asset_routes = []
        pms_dir = Path("pms")

        if pms_dir.exists():
            logger.info("🔍 Scanning pms/ directory for all files...")

            # Walk through all subdirectories and categorize files
            for file_path in pms_dir.rglob("*"):
                if file_path.is_file():
                    # Convert file path to route path
                    # Example: pms/corsica/a_troiz_geo.md -> /pm/corsica/a_troiz_geo.md
                    relative_path = file_path.relative_to(pms_dir)
                    route_path = f"/pm/{relative_path.as_posix()}"

                    if file_path.suffix == ".md":
                        markdown_routes.append(route_path)
                    else:
                        # Other assets (SVG, HTML, images, etc.)
                        asset_routes.append(route_path)

            logger.info(f"✓ Found {len(markdown_routes)} markdown files in pms/ directory")
            logger.info(f"✓ Found {len(asset_routes)} asset files in pms/ directory")

            # Log some examples for debugging
            if markdown_routes:
                logger.info("📝 Example PM markdown routes:")
                for route in markdown_routes[:3]:  # Show first 3 as examples
                    logger.info(f"   - {route}")
                if len(markdown_routes) > 3:
                    logger.info(f"   ... and {len(markdown_routes) - 3} more")

            if asset_routes:
                logger.info("🎨 Example PM asset routes:")
                for route in asset_routes[:3]:  # Show first 3 as examples
                    logger.info(f"   - {route}")
                if len(asset_routes) > 3:
                    logger.info(f"   ... and {len(asset_routes) - 3} more")
        else:
            logger.warning("⚠️ pms/ directory not found, skipping PM route generation")

        return markdown_routes, asset_routes

    async def build(self) -> Dict:
        """Build the static site"""
        # Clean and create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # ====== CORE ROUTES ======
        # Basic application routes
        routes = [
            "/",  # Main index page
            "/readme",  # README/documentation page
            "/settings",  # Settings view page
            "/kill-service-workers",  # Service worker management
            "/pm",  # PM root directory listing
        ]

        # ====== API ROUTES ======
        # All API endpoints from OpenAPI spec
        api_routes = [
            "/api/health",  # Health check endpoint
            "/api/settings",  # Get public settings
            "/api/settings/serialized",  # Get serialized settings
            "/api/build",  # Build static site endpoint
            # Note: Add any additional API routes here as needed
        ]
        routes.extend(api_routes)

        # ====== API DOCUMENTATION ROUTES ======
        # FastAPI auto-generated documentation
        documentation_routes = [
            "/openapi.json",  # OpenAPI JSON schema
            "/docs",  # Swagger UI documentation
            "/redoc",  # ReDoc documentation
        ]
        routes.extend(documentation_routes)

        # ====== PRODUCT ROUTES ======
        # Product-specific routes
        product_routes = [
            "sujets0",  # Sujets0 product
            "/sujets0-form",  # Sujets0 generate page
            "/sujets0/teacher_manifest",  # Sujets0 teacher manifest
            "/sujets0/data-only",  # Sujets0 data-only page
            "/corsica/",  # Corsica product (trailing slash to avoid redirect)
            "/nagini",  # Nagini product
        ]
        routes.extend(product_routes)

        # ====== JUPYTERLITE ROUTES ======
        # JupyterLite and Jupyter compatibility routes
        jupyterlite_routes = [
            "/jupyterlite/",  # JupyterLite main page
            "/jupyterlite/lab",  # JupyterLite lab interface
            "/jupyterlite/repl",  # JupyterLite REPL
            "/jupyterlite/embed",  # JupyterLite embed mode
            "/jupyterlite/sandbox/repl",  # Sandbox REPL
            "/jupyter",  # Jupyter redirect (compatibility)
            "/jupyter/repl",  # Jupyter REPL redirect (compatibility)
        ]
        routes.extend(jupyterlite_routes)

        # ====== PM (MARKDOWN) ROUTES ======
        # Dynamically generate routes for all files in pms/ directory
        # Markdown routes require the .md extension to work properly
        # Examples:
        #   /pm/documentation/README.md -> Documentation readme
        #   /pm/corsica/a_troiz_geo.md -> Corsica geography content
        #   /pm/pyly/00_index.md -> Python curriculum index
        #   /pm/examples/i_radio_example.md -> Interactive radio example
        #
        # Asset routes serve static files (SVG, HTML, images, etc.)
        # Examples:
        #   /pm/corsica/files/corsica_grid.svg -> SVG graphics
        #   /pm/corsica/files/header.html -> HTML templates
        markdown_routes, asset_routes = self._generate_pm_routes()
        routes.extend(markdown_routes)
        routes.extend(asset_routes)

        # Fetch all routes
        results = []
        for route in routes:
            success = await self.fetch_and_save(route)
            results.append({"route": route, "success": success})

        # Copy static files
        logger.info("📁 Copying static files...")
        src_static = Path("src/static")
        dst_static = self.output_dir / "static"

        if src_static.exists():
            shutil.copytree(src_static, dst_static, dirs_exist_ok=True)
            logger.info(f"✓ Copied static files to {dst_static}")

        # Copy CNAME file for custom domain (if exists)
        cname_file = Path("CNAME")
        if cname_file.exists():
            shutil.copy2(cname_file, self.output_dir / "CNAME")
            logger.info("✓ Copied CNAME file for custom domain")

        # Copy .nojekyll file to disable Jekyll processing on GitHub Pages
        nojekyll_file = Path(".nojekyll")
        if nojekyll_file.exists():
            shutil.copy2(nojekyll_file, self.output_dir / ".nojekyll")
            logger.info("✓ Copied .nojekyll file to disable Jekyll processing")
        else:
            # Create it if it doesn't exist
            (self.output_dir / ".nojekyll").touch()
            logger.info("✓ Created .nojekyll file to disable Jekyll processing")

        # Copy JupyterLite output if it exists
        jupyterlite_output = Path("src/static/jupyterlite/_output")
        if jupyterlite_output.exists():
            dst_jupyter = self.output_dir / "static/jupyterlite/_output"
            shutil.copytree(jupyterlite_output, dst_jupyter, dirs_exist_ok=True)
            logger.info("✓ Copied JupyterLite files")

        # Generate build report
        total = len(results)
        successful = sum(1 for r in results if r["success"])

        report = {
            "status": "success" if successful == total else "partial",
            "total_routes": total,
            "successful": successful,
            "failed": total - successful,
            "output_dir": str(self.output_dir),
            "routes": results,
        }

        # Save build report
        report_path = self.output_dir / "build-report.json"
        report_path.write_text(json.dumps(report, indent=2))

        logger.info(f"📊 Build complete: {successful}/{total} routes exported")
        logger.info(f"📁 Output directory: {self.output_dir}")

        return report


async def build_static_site(base_url: str = "http://localhost:8000", base_path: str = "") -> Dict:
    """Main build function"""
    async with StaticSiteBuilder(base_url=base_url, base_path=base_path) as builder:
        return await builder.build()
