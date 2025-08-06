#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Maths.pm - FastAPI Static Site Generator
Main application with organized router architecture
"""

import logging
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from .settings import settings
from .root.router import root_router
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


async def build_jupyterlite():
    """
    Build JupyterLite by copying content from files-for-lite to output directory.
    This ensures notebooks and other content are available in the JupyterLite interface.
    """
    try:
        source_dir = settings.jupyterlite_content_dir  # files-for-lite/
        output_files_dir = settings.jupyterlite_dir / "_output" / "files"

        logger.info("📂 Building JupyterLite content...")
        logger.info(f"   Source: {source_dir}")
        logger.info(f"   Output: {output_files_dir}")

        if not source_dir.exists():
            logger.warning(f"⚠️  Source directory not found: {source_dir}")
            return

        # Create output directory if it doesn't exist
        output_files_dir.mkdir(parents=True, exist_ok=True)

        # Copy all files from source to output
        copied_files = []
        for file_path in source_dir.iterdir():
            if file_path.is_file():
                dest_path = output_files_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                copied_files.append(file_path.name)
                logger.debug(f"   ✅ Copied: {file_path.name}")

        if copied_files:
            logger.info(f"🎉 Successfully copied {len(copied_files)} files to JupyterLite:")
            for filename in copied_files:
                logger.info(f"   📄 {filename}")
        else:
            logger.warning("⚠️  No files found to copy from files-for-lite/")

        # Clean up service worker cache issues
        await cleanup_service_worker_issues()

    except Exception as e:
        logger.error(f"❌ Failed to build JupyterLite content: {e}", exc_info=True)


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
    if settings.jupyterlite_enabled:
        logger.info("🔧 Building JupyterLite...")
        await build_jupyterlite()
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

# Mount static files
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

# Include routers


app.include_router(root_router)
app.include_router(nagini_router)
app.include_router(api_router, prefix="/api")
app.include_router(sujets0_router)
app.include_router(corsica_router)

# Conditionally include JupyterLite router
if settings.jupyterlite_enabled:
    app.include_router(jupyterlite_router)
    app.include_router(jupyter_compat_router)  # Backward compatibility
