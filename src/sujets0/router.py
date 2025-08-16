#!/usr/bin/env python3
"""
Sujets0 Router - Mathematics Exercise Generator
Uses product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings

# Create sujets0 router
sujets0_router = APIRouter(tags=["sujets0"])


@sujets0_router.get("/sujets0", response_class=HTMLResponse)
async def sujets0(request: Request):
    """
    Sujets0 application page - Mathematics exercise generator.

    Uses product settings from the main settings module.
    """
    try:
        # Build template context with product-specific settings
        context = {
            "request": request,
            "page": {"title": "Sujets 0 - Générateur d'exercices"},
        }

        # Find the sujets0 product
        sujets0_product = None
        for product in settings.products:
            if product.name == "sujets0":
                sujets0_product = product
                break

        # Add product-specific context if available
        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": sujets0_product.title_html,
                    "product_description": sujets0_product.description,
                    # Pass product metatags for template to use
                    "product_metatags": sujets0_product.metatags,
                    # Pass backend settings if any
                    "product_backend_settings": sujets0_product.backend_settings,
                    # Add the full product object for template access
                    "current_product": sujets0_product,
                    # Specific settings for Sujets0
                    "arpege_script_paths": sujets0_product.backend_settings.get(
                        "arpege_generator_script_paths", []
                    )
                    if sujets0_product.backend_settings
                    else [],
                    "is_enabled": not sujets0_product.is_hidden,
                }
            )

        return settings.templates.TemplateResponse("sujets0/index.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)


@sujets0_router.get("/scenery", response_class=HTMLResponse)
async def scenery(request: Request):
    """
    Scenery page - Testing environment for Nagini and exercise generation.
    Uses the same template structure as sujets0 but for testing purposes.
    """
    try:
        # Build template context with product-specific settings
        context = {
            "request": request,
            "page": {"title": "Scenery - Testing Environment"},
        }

        # Find the sujets0 product for settings (reusing for now)
        sujets0_product = None
        for product in settings.products:
            if product.name == "sujets0":
                sujets0_product = product
                break

        # Add product-specific context if available
        if sujets0_product:
            context.update(
                {
                    "product_name": "scenery",
                    "product_title": "Scenery Testing",
                    "product_description": "Testing environment for Nagini and exercise generation",
                    # Pass product metatags for template to use
                    "product_metatags": sujets0_product.metatags,
                    # Pass backend settings if any
                    "product_backend_settings": sujets0_product.backend_settings,
                    # Add the full product object for template access
                    "current_product": sujets0_product,
                    # Specific settings for Sujets0
                    "arpege_script_paths": sujets0_product.backend_settings.get(
                        "arpege_generator_script_paths", []
                    )
                    if sujets0_product.backend_settings
                    else [],
                    "is_enabled": not sujets0_product.is_hidden,
                }
            )

        return settings.templates.TemplateResponse("sujets0/scenery.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)
