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


from .settings import settings
from .core.router import core_router
from .nagini.router import nagini_router
from .sujets0.router import sujets0_router
from .api.router import api_router
from .corsica.router import corsica_router

from .jupyterlite.router import jupyterlite_router, jupyter_compat_router

# --- Centralized Logging Configuration ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("maths_pm")
# --- End of Logging Configuration ---


def build_jupyterlite():
    """
    Build JupyterLite exactly like the working example.
    Build directly in the jupyterlite directory, not in a nested _output subdirectory.
    """
    try:
        source_dir = settings.jupyterlite_content_dir  # files-for-lite/
        jupyterlite_dir = settings.jupyterlite_dir  # src/static/jupyterlite/

        logger.info("📂 Building JupyterLite...")
        logger.info(f"   Source: {source_dir}")
        logger.info(f"   Build directory: {jupyterlite_dir}")

        if not source_dir.exists():
            logger.warning(f"⚠️  Source directory not found: {source_dir}")
            return

        # Always build to pick up new files - no caching check
        logger.info("🔄 Building JupyterLite (fresh build to pick up any new files)...")

        # Create jupyterlite directory if it doesn't exist
        jupyterlite_dir.mkdir(parents=True, exist_ok=True)

        # Change to jupyterlite directory for the build (exactly like working example)
        import subprocess
        import os

        original_cwd = os.getcwd()
        os.chdir(str(jupyterlite_dir))

        try:
            logger.info("🔨 Running jupyter lite build...")

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

            logger.info(f"Build command: {' '.join(build_cmd)}")
            logger.info(f"Working directory: {jupyterlite_dir}")
            logger.info(f"Contents path: {relative_source}")

            result = subprocess.run(build_cmd, capture_output=True, text=True, check=True)
            logger.info("✅ JupyterLite build completed successfully")

            if result.stdout:
                logger.debug(f"Build output: {result.stdout}")

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ JupyterLite build failed: {e}")
            if e.stdout:
                logger.error(f"Build stdout: {e.stdout}")
            if e.stderr:
                logger.error(f"Build stderr: {e.stderr}")
        finally:
            os.chdir(original_cwd)

        # Verify the build worked - files should be in _output directory
        output_dir = jupyterlite_dir / "_output"
        files_dir = output_dir / "files"
        if files_dir.exists():
            data_files_dir = files_dir / "data"
            if data_files_dir.exists():
                logger.info(f"✅ Data files found in {data_files_dir}")
                # List what's actually there for debugging
                for root, dirs, files in os.walk(data_files_dir):
                    for file in files:
                        rel_path = os.path.relpath(os.path.join(root, file), files_dir)
                        logger.info(f"   📄 {rel_path}")
            else:
                logger.warning("⚠️  Data files directory not found in files/")
        else:
            logger.warning("⚠️  Files directory not found")

        # Check if main files exist
        if (output_dir / "index.html").exists():
            logger.info("✅ JupyterLite index.html created")
        if (output_dir / "lab" / "index.html").exists():
            logger.info("✅ JupyterLite lab/index.html created")

    except Exception as e:
        logger.error(f"❌ Failed to build JupyterLite content: {e}", exc_info=True)


async def async_build_jupyterlite(force_rebuild: bool = True):
    """
    Async wrapper for build_jupyterlite with optional cache clearing.

    Args:
        force_rebuild: If True, clears cache for fresh rebuild. If False, uses existing cache.
    """
    import subprocess

    if force_rebuild:
        logger.info("🧹 Clearing JupyterLite build cache for fresh rebuild...")

        # Clear build cache to ensure fresh rebuild picks up new files
        output_dir = settings.jupyterlite_dir / "_output"
        cache_db = settings.jupyterlite_dir / ".jupyterlite.doit.db"

        try:
            # Remove output directory
            if output_dir.exists():
                subprocess.run(["rm", "-rf", str(output_dir)], check=True)
                logger.info("✅ Removed old build output")

            # Remove cache database
            if cache_db.exists():
                subprocess.run(["rm", "-f", str(cache_db)], check=True)
                logger.info("✅ Removed build cache database")

        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Cache cleanup failed: {e}")
    else:
        logger.info("🔄 Building JupyterLite (using existing cache)...")

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
            logger.info("🔧 Cleaning up service worker cache issues...")

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

            logger.info("✅ Service worker cache buster added")
        else:
            logger.debug("ℹ️  Service worker file not found, skipping cleanup")

    except Exception as e:
        logger.warning(f"⚠️  Failed to cleanup service worker: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """
    logger.info("🚀 Starting Maths.pm FastAPI app...")
    # 1) Optionally build JupyterLite
    if settings.jupyterlite_enabled:
        logger.info("🔧 Building JupyterLite...")
        await async_build_jupyterlite()

    # 2) Copy entire pms/ to static/pm/ for stable static references
    try:
        pms_dir = settings.base_dir / "pms"
        static_pm_dir = settings.static_dir / "pm"
        if pms_dir.exists():
            logger.info("📦 Rewriting pms/ to static/pm/ ...")

            # Remove existing static/pm/ directory to ensure a clean copy
            if static_pm_dir.exists():
                logger.info("🗑️ Removing existing static/pm/ directory...")
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
            logger.info("✅ pms/ rewrite complete")
        else:
            logger.info("ℹ️ pms/ directory not found; skipping static sync")
    except Exception as e:
        logger.warning(f"⚠️ Failed rewriting pms/ to static/pm/: {e}")
    logger.info("✅ Application startup completed")

    yield

    logger.info("👋 Shutting down Maths.pm FastAPI app...")
    logger.info("✅ Application shutdown completed")


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
