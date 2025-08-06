#!/usr/bin/env python3
"""
Nagini Router - Python in Browser Execution
Uses product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings

# Create nagini router
corsica_router = APIRouter(tags=["corsica"], prefix="/corsica")


@corsica_router.get("/", response_class=HTMLResponse)
async def corsica(request: Request):
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

        # # Add product-specific context if available
        # if corsica_settings:
        #     context.update(
        #         {
        #             "product_name": corsica_settings.name,
        #             "product_title": corsica_settings.title,
        #             "product_description": corsica_settings.description,
        #             "product_settings": corsica_settings.to_dict(),
        #             # Specific settings for Nagini
        #             "nagini_endpoint": corsica_settings.get_nested_setting(
        #                 "nagini", "endpoint", ""
        #             ),
        #             "nagini_js_url": corsica_settings.get_nested_setting("nagini", "js_url", ""),
        #             "pyodide_worker_url": corsica_settings.get_nested_setting(
        #                 "nagini", "pyodide_worker_url", ""
        #             ),
        #             "is_enabled": corsica_settings.is_enabled,
        #         }
        #     )

        return settings.templates.TemplateResponse("corsica/index.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)
