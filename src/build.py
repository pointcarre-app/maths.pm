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

    def __init__(self, base_url: str = "http://localhost:8000", output_dir: str = "dist"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.client = None

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
                    # Has extension, keep as is
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
                output_path.write_bytes(response.content)

            logger.info(f"✓ Saved {path} → {output_path.relative_to(self.output_dir)}")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to fetch {path}: {e}")
            return False

    async def build(self) -> Dict:
        """Build the static site"""
        # Clean and create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Define routes to export
        routes = [
            "/",
            "/readme",
            "/settings",
            "/sujets0",
            "/corsica",
            "/nagini",
            "/api/health",
            "/api/products",
            "/api/settings",
            "/kill-service-workers",
            "/pm",  # PM root directory
        ]

        # Add JupyterLite routes
        jupyterlite_routes = [
            "/jupyterlite/",
            "/jupyterlite/lab",
            "/jupyterlite/repl",
            "/jupyterlite/embed",
            "/jupyterlite/sandbox/repl",
        ]
        routes.extend(jupyterlite_routes)

        # Add PM example routes (these are important documentation)
        pm_routes = [
            "/pm/documentation/README",
            "/pm/examples/i_radio_example",
            "/pm/pyly/00_index",
            "/pm/pyly/01_premiers_pas",
            "/pm/corsica/a_troiz_geo",
            "/pm/corsica/e_seconde_stats_python",
        ]
        routes.extend(pm_routes)

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


async def build_static_site(base_url: str = "http://localhost:8000") -> Dict:
    """Main build function"""
    async with StaticSiteBuilder(base_url=base_url) as builder:
        return await builder.build()
