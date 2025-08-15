#!/usr/bin/env python3
"""
Sujets0 Router - Mathematics Exercise Generator
Uses product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings, sujets0_settings

# Create sujets0 router
sujets0_router = APIRouter(tags=["sujets0"])


@sujets0_router.get("/sujets0", response_class=HTMLResponse)
async def sujets0(request: Request):
    """
    Sujets0 application page - Mathematics exercise generator.

    Uses sujets0_settings for product-specific configuration.
    All settings are loaded automatically in settings.py.
    """
    try:
        # Build template context with product-specific settings
        context = {
            "request": request,
            "page": {"title": "Sujets 0 - Générateur d'exercices"},
        }

        # Add product-specific context if available
        if sujets0_settings and sujets0_settings.product:
            product = sujets0_settings.product
            context.update(
                {
                    "product_name": product.name,
                    "product_title": product.title_html,
                    "product_description": product.description,
                    "product_settings": sujets0_settings.to_dict(),
                    # Pass product metatags for template to use
                    "product_metatags": product.metatags,
                    # Pass backend settings if any
                    "product_backend_settings": product.backend_settings,
                    # Add the full product object for template access
                    "current_product": product,
                    # Specific settings for Sujets0
                    "arpege_script_paths": sujets0_settings.get_setting(
                        "arpege_generator_script_paths", []
                    ),
                    "is_enabled": sujets0_settings.is_enabled,
                }
            )

            print(context)
            print("somallaal")

        return settings.templates.TemplateResponse("sujets0/index.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)
