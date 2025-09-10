#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Example routes showing how to use PM rendering in different contexts
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from ..settings import settings
from .pm.services.pm_context_service import PMContextService, get_pm_context

# Example router
example_router = APIRouter(tags=["pm-examples"])


# Example 1: Simple PM rendering in any route
@example_router.get("/example/simple-pm", response_class=HTMLResponse)
async def simple_pm_example(request: Request):
    """Simplest way to add PM content to any route"""

    # Load PM and get complete context with one line
    pm_context = get_pm_context("pms/examples/intro.md", product_name="examples")

    # Add request and any other context
    context = {
        "request": request,
        **pm_context,  # Spreads all PM-related context
    }

    # Use the simplified PM template
    return settings.templates.TemplateResponse("pm/index-refactored.html", context)


# Example 2: PM embedded in product page
@example_router.get("/products/{product_name}/docs", response_class=HTMLResponse)
async def product_documentation(request: Request, product_name: str):
    """Product page with embedded PM documentation"""

    # Load product info (your existing logic)
    product_info = {
        "title": f"{product_name.title()} Product",
        "description": "This is a product with embedded PM documentation",
    }

    # Try to load PM documentation for this product
    try:
        pm_path = f"pms/{product_name}/index.md"
        pm_context = get_pm_context(pm_path, product_name=product_name)
    except FileNotFoundError:
        # No PM documentation, render without it
        pm_context = {"pm": None}

    # Combine contexts
    context = {"request": request, "product": product_info, **pm_context}

    return settings.templates.TemplateResponse(
        "pm-include/examples/product-page-with-pm.html", context
    )


# Example 3: Multiple PM fragments on one page
@example_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_with_multiple_pms(request: Request):
    """Dashboard showing multiple PM contents"""

    # Load multiple PM contents
    intro_context = get_pm_context("pms/examples/intro.md")
    tutorial_context = get_pm_context("pms/examples/tutorial.md")

    context = {
        "request": request,
        "page": {"title": "Dashboard"},
        "intro_pm": intro_context["pm"],
        "tutorial_pm": tutorial_context["pm"],
    }

    # Custom template that renders multiple PMs
    return settings.templates.TemplateResponse(
        "pm-include/examples/dashboard-multi-pm.html", context
    )


# Example 4: Dynamic PM selection based on user preferences
@example_router.get("/learn/{topic}", response_class=HTMLResponse)
async def learning_path(request: Request, topic: str, level: str = "beginner"):
    """Dynamic PM content based on topic and level"""

    # Map topic and level to PM file (paths include pms/ prefix)
    pm_mapping = {
        "python": {
            "beginner": "pms/pyly/01_premiers_pas.md",
            "intermediate": "pms/pyly/00_index.md",
            "advanced": "pms/examples/tutorial.md",  # Using example for now
        },
        "math": {
            "beginner": "pms/corsica/a_troiz_geo.md",
            "intermediate": "pms/corsica/e_seconde_stats_python.md",
            "advanced": "pms/examples/intro.md",  # Using example for now
        },
    }

    # Get the appropriate PM file
    if topic not in pm_mapping:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' not found")

    if level not in pm_mapping[topic]:
        level = "beginner"  # Default to beginner

    pm_path = pm_mapping[topic][level]

    # Map topic to actual product name
    product_map = {"python": "pyly", "math": "corsica"}
    product_name = product_map.get(topic, topic)

    # Load PM with context
    pm_context = PMContextService.load_pm_from_file(
        pm_path=pm_path, product_name=product_name, debug=request.query_params.get("debug", False)
    )

    # Add navigation context
    context = {
        "request": request,
        "current_topic": topic,
        "current_level": level,
        "available_levels": list(pm_mapping.get(topic, {}).keys()),
        **pm_context,
    }

    # Use a custom learning template or the standard PM template
    return settings.templates.TemplateResponse("pm/index-refactored.html", context)


# Example 5: API endpoint that returns PM data as JSON
@example_router.get("/api/pm/{origin:path}")
async def get_pm_json(origin: str):
    """API endpoint returning PM data as JSON"""

    try:
        # Load PM context
        pm_context = PMContextService.load_pm_from_origin(origin)

        # Return relevant data as JSON
        return {
            "title": pm_context["pm"].title,
            "chapter": pm_context["pm"].chapter,
            "fragments_count": len(pm_context["pm"].fragments),
            "has_toc": bool(pm_context["pm"].toc),
            "metatags": pm_context.get("pm_metatags", {}),
            "product": pm_context.get("product_name"),
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Example 6: Using PM rendering with custom wrapper
@example_router.get("/custom-layout/{pm_name}", response_class=HTMLResponse)
async def custom_layout_pm(request: Request, pm_name: str):
    """PM rendering with custom layout wrapper"""

    # Load PM
    pm_context = get_pm_context(f"pms/examples/{pm_name}.md")

    # Custom wrapper settings
    context = {
        "request": request,
        "wrapper_class": "custom-pm-wrapper max-w-7xl mx-auto",
        "show_toc": True,
        "container_width": "max-w-4xl",
        **pm_context,
    }

    # Template that uses render-with-wrapper.html
    return settings.templates.TemplateResponse("pm-include/examples/custom-pm-layout.html", context)


# Example 7: Dynamic PM loading demonstration
@example_router.get("/dynamic-pm-demo", response_class=HTMLResponse)
async def dynamic_pm_demo(request: Request):
    """Demonstrate dynamic PM loading from templates"""

    # No PM loading needed here! The template will load PMs dynamically
    context = {"request": request, "page": {"title": "Dynamic PM Loading Demo"}}

    # The template will use {% include "pm-include/render-dynamic.html" %}
    # to load PM files dynamically
    return settings.templates.TemplateResponse("pm-include/examples/dynamic-pm-demo.html", context)


# Example 8: Test dynamic PM loading
@example_router.get("/test-dynamic-pm", response_class=HTMLResponse)
async def test_dynamic_pm(request: Request):
    """Test if dynamic PM loading works"""

    context = {
        "request": request,
    }

    return settings.templates.TemplateResponse("test-dynamic-pm.html", context)


# Example 9: Simple dynamic PM demo
@example_router.get("/simple-dynamic-demo", response_class=HTMLResponse)
async def simple_dynamic_demo(request: Request):
    """Simple demonstration of dynamic PM loading"""

    # Just pass request - all PM loading happens in the template!
    context = {"request": request}

    return settings.templates.TemplateResponse(
        "pm-include/examples/simple-dynamic-demo.html", context
    )
