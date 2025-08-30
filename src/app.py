#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Maths.pm - FastAPI Static Site Generator
Main application with organized router architecture
"""

import logging
from contextlib import asynccontextmanager
from shutil import copy2, rmtree
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import asyncio
import httpx

# --- Centralized Logging Configuration ---
# Configure logging BEFORE importing settings to catch all logs
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("maths_pm")
# --- End of Logging Configuration ---

from .settings import settings
from .core.router import core_router
from .nagini.router import nagini_router
from .sujets0.router import sujets0_router
from .api.router import api_router
from .corsica.router import corsica_router

from .jupyterlite.router import jupyterlite_router, jupyter_compat_router


def build_jupyterlite():
    """
    Build JupyterLite exactly like the working example.
    Build directly in the jupyterlite directory, not in a nested _output subdirectory.
    """
    try:
        source_dir = settings.jupyterlite_content_dir  # files-for-lite/
        jupyterlite_dir = settings.jupyterlite_dir  # src/static/jupyterlite/

        if not source_dir.exists():
            logger.warning(f"⚠️  JupyterLite source not found: {source_dir}")
            return

        # Create jupyterlite directory if it doesn't exist
        jupyterlite_dir.mkdir(parents=True, exist_ok=True)

        # Change to jupyterlite directory for the build (exactly like working example)
        import subprocess
        import os

        original_cwd = os.getcwd()
        os.chdir(str(jupyterlite_dir))

        try:
            # Calculate relative path from jupyterlite dir to files-for-lite
            relative_source = os.path.relpath(source_dir, jupyterlite_dir)

            # Build command exactly like the working example
            build_cmd = [
                "jupyter",
                "lite",
                "build",
                "--contents",
                relative_source,
            ]

            result = subprocess.run(build_cmd, capture_output=True, text=True, check=True)

        except subprocess.CalledProcessError:
            logger.error("❌ JupyterLite build failed")
        finally:
            os.chdir(original_cwd)

        # Verify the build worked - files should be in _output directory
        output_dir = jupyterlite_dir / "_output"
        index_exists = (output_dir / "index.html").exists()
        lab_exists = (output_dir / "lab" / "index.html").exists()

        if index_exists and lab_exists:
            # Count data files for summary
            files_dir = output_dir / "files"
            if files_dir.exists():
                data_files_dir = files_dir / "data"
                if data_files_dir.exists():
                    file_count = sum(1 for _, _, files in os.walk(data_files_dir) for _ in files)
                    logger.info(f"✅ JupyterLite ready ({file_count} data files)")
                else:
                    logger.info("✅ JupyterLite ready")
            else:
                logger.info("✅ JupyterLite ready")
        else:
            logger.error("❌ JupyterLite build failed")

    except Exception as e:
        logger.error(f"❌ JupyterLite build failed: {e}")


async def async_build_jupyterlite(force_rebuild: bool = True):
    """
    Async wrapper for build_jupyterlite with optional cache clearing.

    Args:
        force_rebuild: If True, clears cache for fresh rebuild. If False, uses existing cache.
    """
    import subprocess

    if force_rebuild:
        # Clear build cache to ensure fresh rebuild picks up new files
        output_dir = settings.jupyterlite_dir / "_output"
        cache_db = settings.jupyterlite_dir / ".jupyterlite.doit.db"

        try:
            # Remove output directory
            if output_dir.exists():
                subprocess.run(["rm", "-rf", str(output_dir)], check=True)

            # Remove cache database
            if cache_db.exists():
                subprocess.run(["rm", "-f", str(cache_db)], check=True)

        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Cache cleanup failed: {e}")

    # Now build with fresh or existing cache
    build_jupyterlite()

    # Clean up service worker cache issues
    await cleanup_service_worker_issues()


async def cleanup_service_worker_issues():
    """
    Clean up potential service worker caching issues by updating service worker config.
    """
    try:
        service_worker_path = settings.jupyterlite_dir / "_output" / "service-worker.js"

        if service_worker_path.exists():
            # Read current service worker
            with open(service_worker_path, "r", encoding="utf-8") as f:
                sw_content = f.read()

            # Add cache-busting comment with timestamp
            import time

            timestamp = int(time.time())
            cache_buster = f"\n// Cache buster: {timestamp}\n// Service worker updated at startup\n"

            # Write updated service worker
            with open(service_worker_path, "w", encoding="utf-8") as f:
                f.write(cache_buster + sw_content)

    except Exception as e:
        logger.warning(f"⚠️  Failed to cleanup service worker: {e}")


async def download_safari_css_files(force_download: bool = False):
    """
    Download external CSS files locally for Safari CORS compatibility.
    These files will be served from the same origin to avoid CORS issues.

    Args:
        force_download: If True, always download. If False, check if files exist first.
    """
    try:
        safari_css_dir = settings.static_dir / "css" / "safari-local"
        safari_css_dir.mkdir(parents=True, exist_ok=True)

        # CSS files to download
        css_urls = {
            # Google Fonts (multiple font families)
            "fonts-comfortaa.css": "https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&family=Cormorant+Garamond:ital,wght@0,300..700;1,300..700&family=Dancing+Script:wght@400..700&family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Lora:ital,wght@0,400..700;1,400..700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&family=Spectral:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap",
            "fonts-lexend.css": "https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap",
            # DaisyUI
            "daisyui.css": "https://cdn.jsdelivr.net/npm/daisyui@5",
            "daisyui-themes.css": "https://cdn.jsdelivr.net/npm/daisyui@5/themes.css",
            # KaTeX
            "katex.min.css": "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css",
            # Papyrus styles
            "papyrus-index.css": "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/styles/index.css",
            "papyrus-print.css": "https://cdn.jsdelivr.net/gh/pointcarre-app/papyrus@v0.0.10/src/styles/print.css",
        }

        # Check if we should skip download (files already exist)
        if not force_download:
            # Check if all CSS files already exist
            all_exist = all((safari_css_dir / filename).exists() for filename in css_urls.keys())
            if all_exist:
                logger.info("🦁 Safari CSS files already exist, skipping download")
                return
            else:
                logger.info("🦁 Some Safari CSS files missing, downloading...")

        # Font files directory for actual font files (woff2, etc.)
        fonts_dir = safari_css_dir / "fonts"
        fonts_dir.mkdir(parents=True, exist_ok=True)

        async with httpx.AsyncClient(timeout=10.0) as client:
            # Download CSS files
            download_tasks = []
            for filename, url in css_urls.items():
                download_tasks.append(
                    download_css_file(client, url, safari_css_dir / filename, fonts_dir)
                )

            # Execute all downloads concurrently
            results = await asyncio.gather(*download_tasks, return_exceptions=True)

            # Count successful downloads
            successful = sum(1 for r in results if not isinstance(r, Exception))

            if successful > 0:
                logger.info(f"🦁 Safari CSS files downloaded ({successful}/{len(css_urls)} files)")
            else:
                logger.warning("⚠️  No Safari CSS files downloaded")

    except Exception as e:
        logger.warning(f"⚠️  Failed to download Safari CSS files: {e}")


async def download_css_file(client, url, dest_path, fonts_dir):
    """
    Download a single CSS file and optionally download referenced font files.
    """
    try:
        response = await client.get(url)
        if response.status_code == 200:
            content = response.text

            # For font CSS files, also download the actual font files
            if "fonts.googleapis" in url or "fonts.gstatic" in url:
                # Parse and download font files referenced in the CSS
                import re

                font_urls = re.findall(r"url\((https://[^)]+)\)", content)

                for font_url in font_urls:
                    font_filename = font_url.split("/")[-1].split("?")[0]
                    font_dest = fonts_dir / font_filename

                    # Download font file
                    font_response = await client.get(font_url)
                    if font_response.status_code == 200:
                        font_content = font_response.content
                        with open(font_dest, "wb") as f:
                            f.write(font_content)

                    # Update CSS to use local font path
                    relative_font_path = f"./fonts/{font_filename}"
                    content = content.replace(font_url, relative_font_path)

            # Write CSS file
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True
        else:
            logger.warning(f"⚠️  Failed to download {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"⚠️  Error downloading {url}: {e}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """
    logger.info(f"🚀 Starting Maths.pm ({settings.domain_config.domain_url or 'localhost'})")
    # 1) Optionally build JupyterLite
    if settings.jupyterlite_enabled:
        await async_build_jupyterlite()

        # 2) Download CSS files for Safari CORS compatibility
    # Strategy:
    # - In GitHub Actions/CI: SKIP downloads (files are already in git repository)
    # - Locally: Check DOWNLOAD_SAFARI_CSS env var (default: check and download if missing)
    # - Can override with DOWNLOAD_SAFARI_CSS=true for force download

    is_ci = os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true"
    should_download = os.environ.get("DOWNLOAD_SAFARI_CSS", "").lower() in ["true", "1", "yes"]

    if is_ci:
        # In CI/GitHub Actions: Skip downloads - files are already committed to git
        logger.info("🚀 GitHub Actions detected: Using Safari CSS files from repository")
        # No download needed - files are in src/static/css/safari-local/
    elif should_download:
        # Local development with explicit download request
        logger.info(
            "📦 Local environment: Force downloading Safari CSS files (DOWNLOAD_SAFARI_CSS=true)"
        )
        try:
            await download_safari_css_files(force_download=True)
        except Exception as e:
            logger.warning(f"⚠️  Safari CSS download failed (non-critical): {e}")
    else:
        # Local development: Check if files exist, download if missing
        logger.info("💻 Local environment: Checking Safari CSS files...")
        try:
            await download_safari_css_files(force_download=False)
        except Exception as e:
            logger.warning(f"⚠️  Safari CSS check/download failed (non-critical): {e}")

    # 3) Copy entire pms/ to static/pm/ for stable static references
    try:
        pms_dir = settings.base_dir / "pms"
        static_pm_dir = settings.static_dir / "pm"
        if pms_dir.exists():
            # Remove existing static/pm/ directory to ensure a clean copy
            if static_pm_dir.exists():
                rmtree(static_pm_dir)

            # Ensure destination exists
            static_pm_dir.mkdir(parents=True, exist_ok=True)

            # Walk and mirror tree; copy all files
            for root, dirs, files in os.walk(pms_dir):
                rel_root = os.path.relpath(root, pms_dir)
                dest_root = static_pm_dir / rel_root if rel_root != "." else static_pm_dir
                dest_root.mkdir(parents=True, exist_ok=True)

                for file_name in files:
                    src_file = Path(root) / file_name
                    dest_file = dest_root / file_name
                    try:
                        copy2(src_file, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {src_file} -> {dest_file}: {e}")
            # Count files copied
            file_count = sum(1 for _, _, files in os.walk(static_pm_dir) for _ in files)
            logger.info(f"🌍 PM files copied in static/pm/ ({file_count})")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying PM files: {e}")

    # 4) Copy sujets0/generators to static/sujets0/generators
    try:
        generators_dir = settings.base_dir / "src" / "sujets0" / "generators"
        static_generators_dir = settings.static_dir / "sujets0" / "generators"

        if generators_dir.exists():
            # Remove existing static/sujets0/generators directory to ensure a clean copy
            if static_generators_dir.exists():
                rmtree(static_generators_dir)

            # Ensure destination exists
            static_generators_dir.mkdir(parents=True, exist_ok=True)

            # Copy all Python files from generators
            for file_path in generators_dir.glob("*.py"):
                if file_path.name != "__pycache__":
                    try:
                        dest_file = static_generators_dir / file_path.name
                        copy2(file_path, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {file_path} -> {dest_file}: {e}")

            # Count files copied
            file_count = len(list(static_generators_dir.glob("*.py")))
            logger.info(f"📝  {file_count}  Sujets0 generators ready")
        else:
            logger.warning(f"⚠️ Generators directory not found: {generators_dir}")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying sujets0 generators: {e}")

    # 5) Copy entire official_curriculums/ to static/official_curriculums/
    try:
        official_curriculums_dir = settings.base_dir / "official_curriculums"
        static_official_curriculums_dir = settings.static_dir / "official_curriculums"

        os.makedirs(static_official_curriculums_dir, exist_ok=True)

        for root, dirs, files in os.walk(official_curriculums_dir):
            rel_root = os.path.relpath(root, official_curriculums_dir)
            dest_root = (
                static_official_curriculums_dir / rel_root
                if rel_root != "."
                else static_official_curriculums_dir
            )
            os.makedirs(dest_root, exist_ok=True)

            # Copy all files from official_curriculums/
            for file_path in official_curriculums_dir.glob("**/*"):
                if file_path.is_file():
                    try:
                        dest_file = static_official_curriculums_dir / file_path.relative_to(
                            official_curriculums_dir
                        )
                        copy2(file_path, dest_file)
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to copy {file_path} -> {dest_file}: {e}")

            # Count files copied
            file_count = len(list(static_official_curriculums_dir.glob("**/*")))
            logger.info(f"📝 Official curriculums ready ({file_count} files)")
    except Exception as e:
        logger.warning(f"⚠️ Failed copying official_curriculums: {e}")

    logger.info(
        "✅ All static files copied: JupyterLite (optional), PM, Sujets0, Official curriculums"
    )

    yield

    logger.info("👋 Shutting down...")


# Initialize application
app = FastAPI(
    title="Maths.pm",
    description="A modern web application for Maths.pm",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files and images from files/
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
app.mount("/images", StaticFiles(directory=settings.images_files_dir), name="images")

# Include routers


app.include_router(core_router)
app.include_router(nagini_router)
app.include_router(api_router, prefix="/api")
app.include_router(sujets0_router)
app.include_router(corsica_router)

# Conditionally include JupyterLite router
if settings.jupyterlite_enabled:
    app.include_router(jupyterlite_router)
    app.include_router(jupyter_compat_router)  # Backward compatibility
