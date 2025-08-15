#!/usr/bin/env python3
"""
Corsica Router - Maths in Corsica
(Maths.Corsica & Python.Corsica)
Product-specific settings for configuration
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..settings import settings, corsica_settings


corsica_router = APIRouter(tags=["corsica"], prefix="/corsica")


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


@corsica_router.get("/", response_class=HTMLResponse)
async def corsica(request: Request):
    """Corsica index page with product-specific metatags and settings."""

    # Build comprehensive context with product-specific settings
    context = {
        "request": request,
    }

    # Add product-specific context if available
    if corsica_settings and corsica_settings.product:
        # Get the product model directly
        product = corsica_settings.product

        context.update(
            {
                "product_name": product.name,
                "product_title": product.title_html,
                "product_description": product.description,
                "product_settings": corsica_settings.to_dict(),
                # Pass product metatags for template to use
                "product_metatags": product.metatags,
                # Pass backend settings if any
                "product_backend_settings": product.backend_settings,
                # Add the full product object for template access
                "current_product": product,
            }
        )

    return settings.templates.TemplateResponse("corsica/index.html", context)


## TODO: will be imported from root and dynamically rebuilt


# @corsica_router.get("/pm/<origin:path>", response_class=HTMLResponse)
# async def pm(request: Request):
#     # try:
#     # Build template context with product-specific settings
#     # context = {
#     #
#     # }

#     return settings.templates.TemplateResponse(
#         "corsica/index.html",
#         {
#             "request": request,
#             # "page": {"title": "Nagini - Python dans le navigateur"},
#         },
#     )
