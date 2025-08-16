#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
API Router for Maths.pm Application
"""

import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..settings import settings

# Create API router
api_router = APIRouter(tags=["api"])


@api_router.get("/settings")
async def get_public_settings():
    """
    Returns backend settings organized by product.
    Each product has its own namespace to avoid conflicts.
    """
    return {"products": settings.products_settings, "domain": settings.domain_backend_settings}


@api_router.get("/settings/serialized")
async def get_serialized_settings():
    """
    Returns template-ready backend settings (with JSON strings).
    Each product's settings are pre-serialized for template use.
    """
    return {
        "products": settings.serialized_products_settings,
        "domain": json.dumps(settings.domain_backend_settings),
    }


@api_router.get("/health")
async def health_check():
    """
    Application health check endpoint.

    Returns useful information about the application state,
    including how many products were loaded and domain info.
    """
    return {
        "status": "healthy",
        "products_loaded": len(settings.products),
        "version": settings.app_version,
        "jupyterlite_enabled": settings.jupyterlite_enabled,
        "domain": settings.domain_name,
        "product_names": [p.name for p in settings.products],
    }


@api_router.get("/build")
async def build_static_site():
    """
    Build static site for deployment.

    This endpoint triggers the static site generation process,
    crawling all routes and saving them as static HTML/JSON files.
    Used by GitHub Actions for deployment.
    """
    try:
        from ..build import build_static_site as build_func

        # Run the build process
        result = await build_func(base_url="http://127.0.0.1:8000")

        return JSONResponse(
            content=result, status_code=200 if result["status"] == "success" else 207
        )
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
