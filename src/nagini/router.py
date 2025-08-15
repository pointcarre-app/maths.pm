#!/usr/bin/env python3
"""
Nagini Router - Python in Browser Execution
Uses product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings, nagini_settings

# Create nagini router
nagini_router = APIRouter(tags=["nagini"])


@nagini_router.get("/nagini", response_class=HTMLResponse)
async def nagini(request: Request):
    """
    Nagini application page - Python execution in browser.

    Uses nagini_settings for product-specific configuration.
    All settings are loaded automatically in settings.py.
    """
    try:
        # Build template context with product-specific settings
        context = {
            "request": request,
            "page": {"title": "Nagini - Python dans le navigateur"},
        }

        # Add product-specific context if available
        if nagini_settings and nagini_settings.product:
            product = nagini_settings.product
            context.update(
                {
                    "product_name": product.name,
                    "product_title": product.title_html,
                    "product_description": product.description,
                    "product_settings": nagini_settings.to_dict(),
                    # Pass product metatags for template to use
                    "product_metatags": product.metatags,
                    # Pass backend settings if any
                    "product_backend_settings": product.backend_settings,
                    # Add the full product object for template access
                    "current_product": product,
                    # Specific settings for Nagini
                    "nagini_endpoint": nagini_settings.get_nested_setting("nagini", "endpoint", ""),
                    "nagini_js_url": nagini_settings.get_nested_setting("nagini", "js_url", ""),
                    "pyodide_worker_url": nagini_settings.get_nested_setting(
                        "nagini", "pyodide_worker_url", ""
                    ),
                    "is_enabled": nagini_settings.is_enabled,
                }
            )

        return settings.templates.TemplateResponse("nagini/index.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)
