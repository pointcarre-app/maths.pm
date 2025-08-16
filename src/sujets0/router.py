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


@sujets0_router.get("/sujets0/ex-ante-generated", response_class=HTMLResponse)
async def sujets0_ex_ante_generated(request: Request):
    """
    Pre-generated questions viewer - Displays questions from the build process.

    This route serves pre-generated questions from JSON files created by
    src/build_questions.py. No Python execution happens in the browser.
    Questions are loaded instantly from static JSON files.

    Benefits:
    - Instant loading (no Pyodide/Nagini needed)
    - All questions validated at build time
    - Reproducible with seeds 0-99 per generator
    - Browser cacheable
    """
    try:
        import json
        from pathlib import Path

        # Load the index of pre-generated questions
        questions_dir = Path(settings.base_dir) / "src" / "static" / "sujets0" / "questions"
        index_file = questions_dir / "index.json"

        # Check if questions have been generated
        if not index_file.exists():
            return HTMLResponse(
                """
                <div style="padding: 2rem; font-family: system-ui;">
                    <h1>⚠️ Questions not yet generated</h1>
                    <p>Run the build script first:</p>
                    <pre style="background: #f0f0f0; padding: 1rem;">python src/build_questions.py</pre>
                    <p>This will generate ~5000 questions from all generator files.</p>
                </div>
                """,
                status_code=503,
            )

        # Load index data
        with open(index_file, "r", encoding="utf-8") as f:
            index_data = json.load(f)

        # Build context for template
        context = {
            "request": request,
            "page": {"title": "Questions Pré-générées - Sujets 0"},
            "questions_index": index_data,
            "questions_base_url": "/static/sujets0/questions/",
        }

        # Find the sujets0 product for consistent styling
        sujets0_product = None
        for product in settings.products:
            if product.name == "sujets0":
                sujets0_product = product
                break

        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": "Questions Pré-générées",
                    "product_description": f"{index_data.get('total_questions', 0)} questions disponibles instantanément",
                    "product_metatags": sujets0_product.metatags,
                    "current_product": sujets0_product,
                }
            )

        return settings.templates.TemplateResponse("sujets0/ex_ante_generated.html", context)

    except Exception as e:
        return HTMLResponse(f"Error: {e}", status_code=500)


@sujets0_router.get("/sujets0/ex-ante-generated-error-analysis", response_class=HTMLResponse)
async def sujets0_ex_ante_generated_error_analysis(request: Request):
    """
    Error analysis view for pre-generated questions.

    Displays all failed questions in a table format for analysis.
    Perfect for feeding to LLMs for debugging patterns.
    """
    try:
        import json
        from pathlib import Path

        # Load the index of pre-generated questions
        questions_dir = Path(settings.base_dir) / "src" / "static" / "sujets0" / "questions"
        index_file = questions_dir / "index.json"

        # Check if questions have been generated
        if not index_file.exists():
            return HTMLResponse(
                """
                <div style="padding: 2rem; font-family: system-ui;">
                    <h1>⚠️ Questions not yet generated</h1>
                    <p>Run the build script first:</p>
                    <pre style="background: #f0f0f0; padding: 1rem;">python src/build_questions.py</pre>
                </div>
                """,
                status_code=503,
            )

        # Load index data
        with open(index_file, "r", encoding="utf-8") as f:
            index_data = json.load(f)

        # Collect all error data
        errors = []
        for generator in index_data.get("generators", []):
            if generator.get("failed", 0) > 0:
                # Load error details for each failed seed
                gen_dir = questions_dir / generator["name"]
                for seed in generator.get("failed_seeds", []):
                    error_file = gen_dir / f"{seed}.json"
                    if error_file.exists():
                        with open(error_file, "r", encoding="utf-8") as ef:
                            error_data = json.load(ef)
                            if not error_data.get("success", True):
                                errors.append(
                                    {
                                        "generator": generator["name"],
                                        "seed": seed,
                                        "error": error_data.get("error", "Unknown error"),
                                        "error_type": error_data.get("error_type", "Unknown"),
                                        "traceback": error_data.get("traceback", ""),
                                        "stdout": error_data.get("stdout", ""),
                                        "stderr": error_data.get("stderr", ""),
                                    }
                                )

        # Build context for template
        context = {
            "request": request,
            "page": {"title": "Error Analysis - Questions Pré-générées"},
            "errors": errors,
            "total_errors": len(errors),
            "total_generators": len(index_data.get("generators", [])),
            "generators_with_errors": len(
                [g for g in index_data.get("generators", []) if g.get("failed", 0) > 0]
            ),
        }

        # Find the sujets0 product for consistent styling
        sujets0_product = None
        for product in settings.products:
            if product.name == "sujets0":
                sujets0_product = product
                break

        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": "Error Analysis",
                    "product_description": f"Analyse de {len(errors)} erreurs de génération",
                    "product_metatags": sujets0_product.metatags,
                    "current_product": sujets0_product,
                }
            )

        return settings.templates.TemplateResponse(
            "sujets0/ex_ante_generated_error_analysis.html", context
        )

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
