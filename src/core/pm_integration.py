#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Integration example: Using PM rendering in core router

This demonstrates how to integrate PM rendering into existing routes
without major refactoring.
"""

from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse

from ..settings import settings
from .pm.services.pm_context_service import get_pm_context, PMContextService


def add_pm_routes(router):
    """
    Add PM-enabled routes to an existing router.

    Usage in your existing router file:
        from .router_pm_integration import add_pm_routes
        add_pm_routes(core_router)
    """

    # Example 1: Simplified PM route using the service
    @router.get("/pm-new/{origin:path}", response_class=HTMLResponse)
    async def get_pm_simplified(request: Request, origin: str, debug: bool = False):
        """
        Simplified version of the PM route using the new service.
        Compare this with the original get_pm() function in router.py
        """
        try:
            # Load PM context with one line
            context = PMContextService.load_pm_from_origin(origin, debug=debug)

            # Add request to context
            context["request"] = request

            # Use the simplified template
            return settings.templates.TemplateResponse("pm/index-refactored.html", context)

        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"PM file not found: {origin}")

    # Example 2: Add PM content to existing home page
    @router.get("/home-with-pm", response_class=HTMLResponse)
    async def home_with_pm(request: Request):
        """Enhanced home page with PM content"""

        # Try to load a welcome PM
        try:
            pm_context = get_pm_context("pms/welcome.md")
        except FileNotFoundError:
            # No welcome PM, set pm to None
            pm_context = {"pm": None}

        # Get products as usual
        products_for_template = [p.to_template_context() for p in settings.products]

        # Combine contexts
        context = {
            "request": request,
            "page": {"title": "Homepage with PM"},
            "products": products_for_template,
            **pm_context,  # Add PM context
        }

        # Use a custom template that includes PM rendering
        return settings.templates.TemplateResponse(
            "home-with-pm.html",  # You'd create this template
            context,
        )

    # Example 3: Product documentation route
    @router.get("/products/{product_name}/documentation", response_class=HTMLResponse)
    async def product_documentation(request: Request, product_name: str):
        """Product documentation using PM"""

        # Find the product
        product = next((p for p in settings.products if p.name == product_name), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product '{product_name}' not found")

        # Load PM documentation for the product
        pm_path = f"pms/{product_name}/index.md"
        try:
            pm_context = get_pm_context(pm_path, product_name=product_name)
        except FileNotFoundError:
            # Try README as fallback
            try:
                pm_path = f"pms/{product_name}/README.md"
                pm_context = get_pm_context(pm_path, product_name=product_name)
            except FileNotFoundError:
                # No documentation found
                raise HTTPException(
                    status_code=404, detail=f"No documentation found for product '{product_name}'"
                )

        # Add product info to context
        context = {"request": request, "product": product.to_template_context(), **pm_context}

        # Use the standard PM template or a custom one
        return settings.templates.TemplateResponse("pm/index-refactored.html", context)

    # Example 4: Learning path with dynamic PM selection
    @router.get("/learn/{subject}", response_class=HTMLResponse)
    async def learning_subject(request: Request, subject: str, level: str = "intro"):
        """Dynamic learning path based on subject and level"""

        # Map subjects to PM files
        subject_map = {
            "python": {
                "intro": "pms/pyly/intro.md",
                "functions": "pms/pyly/functions.md",
                "classes": "pms/pyly/classes.md",
            },
            "math": {
                "intro": "pms/corsica/intro.md",
                "geometry": "pms/corsica/a_surface.md",
                "algebra": "pms/corsica/b_volume.md",
            },
        }

        if subject not in subject_map:
            raise HTTPException(status_code=404, detail=f"Subject '{subject}' not found")

        if level not in subject_map[subject]:
            # Default to intro
            level = "intro"

        pm_path = subject_map[subject][level]

        try:
            pm_context = get_pm_context(pm_path, product_name=subject)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Content not found for {subject}/{level}")

        # Add navigation context
        context = {
            "request": request,
            "subject": subject,
            "level": level,
            "available_levels": list(subject_map[subject].keys()),
            **pm_context,
        }

        return settings.templates.TemplateResponse("pm/index-refactored.html", context)


# Helper function to enhance existing context with PM
def enhance_context_with_pm(
    context: dict, pm_path: str, product_name: str = None, required: bool = False
) -> dict:
    """
    Helper to add PM content to an existing context dictionary.

    Args:
        context: Existing context dictionary
        pm_path: Path to PM file
        product_name: Optional product name
        required: If True, raise exception if PM not found

    Returns:
        Enhanced context with PM data

    Example:
        context = {"request": request, "page": {"title": "My Page"}}
        context = enhance_context_with_pm(context, "pms/intro.md")
    """
    try:
        pm_context = get_pm_context(pm_path, product_name=product_name)
        context.update(pm_context)
    except FileNotFoundError:
        if required:
            raise
        # Set pm to None if not required and not found
        context["pm"] = None

    return context
