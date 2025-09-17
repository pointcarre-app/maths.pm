#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Maths.pm - FastAPI Static Site Generator
Main application with organized router architecture
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# --- Centralized Logging Configuration ---
# Configure logging BEFORE importing settings to catch all logs
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("maths_pm")
# --- End of Logging Configuration ---

from .settings import settings  # noqa: E402
from .core.router import core_router  # noqa: E402
from .nagini.router import nagini_router  # noqa: E402
from .sujets0.router import sujets0_router  # noqa: E402
from .api.router import api_router  # noqa: E402
from .corsica.router import corsica_router  # noqa: E402

from .jupyterlite.router import jupyterlite_router, jupyter_compat_router  # noqa: E402


from .core.router_pm_examples import example_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events by delegating to the lifespan manager.
    """
    # Local import to avoid heavy imports at module load time
    from .lifespan import lifespan_manager

    async with lifespan_manager(app):
        yield


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
app.include_router(example_router)


# Conditionally include JupyterLite router
if settings.jupyterlite_enabled:
    app.include_router(jupyterlite_router)
    app.include_router(jupyter_compat_router)  # Backward compatibility
