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

# Load sujets0 product settings once at module level
sujets0_product = None
for product in settings.products:
    if product.name == "sujets0":
        sujets0_product = product
        break


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

        # Add product-specific context if available
        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": sujets0_product.title_html,
                    "product_description": getattr(
                        sujets0_product, "description", "Générateur d'exercices mathématiques"
                    ),
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


# @sujets0_router.get("/sujets0/originals", response_class=HTMLResponse)


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

        # Filter generators to only include gen_ and spe_ with 4 underscores
        import re

        pattern = re.compile(r"^(gen|spe)_[^_]+_[^_]+_[^_]+_question$")

        filtered_generators = []
        total_questions = 0
        total_failed = 0

        for generator in index_data.get("generators", []):
            if pattern.match(generator["name"]):
                filtered_generators.append(generator)
                total_questions += generator.get("successful", 0)
                total_failed += generator.get("failed", 0)

        # Create filtered index data
        filtered_index_data = {
            **index_data,
            "generators": filtered_generators,
            "total_questions": total_questions,
            "total_failed": total_failed,
            "total_generators": len(filtered_generators),
        }

        # Build context for template
        context = {
            "request": request,
            "page": {"title": "Questions Pré-générées - Sujets 0"},
            "questions_index": filtered_index_data,
            "questions_base_url": "/static/sujets0/questions/",
        }

        # Use global sujets0_product for consistent styling
        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": "Questions Pré-générées",
                    "product_description": f"{filtered_index_data.get('total_questions', 0)} questions disponibles instantanément",
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

        # Filter generators to only include gen_ and spe_ with 4 underscores
        import re

        pattern = re.compile(r"^(gen|spe)_[^_]+_[^_]+_[^_]+_question$")

        filtered_generators = []
        for generator in index_data.get("generators", []):
            if pattern.match(generator["name"]):
                filtered_generators.append(generator)

        # Collect all error data
        errors = []
        for generator in filtered_generators:
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
            "total_generators": len(filtered_generators),
            "generators_with_errors": len(
                [g for g in filtered_generators if g.get("failed", 0) > 0]
            ),
        }

        # Use global sujets0_product for consistent styling
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


@sujets0_router.get("/sujets0/originals/{filiere_number}", response_class=HTMLResponse)
async def sujets0_originals(request: Request, filiere_number: str):
    """
    Original curriculum questions viewer by filiere.

    Displays the official curriculum questions from YAML files organized by filiere:
    - gen-1, gen-2, gen-3: General mathematics subjects
    - spe-1, spe-2: Specialty mathematics subjects

    Args:
        filiere_number: One of "gen-1", "gen-2", "gen-3", "spe-1", "spe-2"
    """
    try:
        import yaml
        from pathlib import Path

        # Validate filiere_number
        valid_filieres = ["gen-1", "gen-2", "gen-3", "spe-1", "spe-2"]
        if filiere_number not in valid_filieres:
            return HTMLResponse(
                f"""
                <div style="padding: 2rem; font-family: system-ui;">
                    <h1>❌ Filière invalide: {filiere_number}</h1>
                    <p>Les filières valides sont: {", ".join(valid_filieres)}</p>
                    <a href="/sujets0">← Retour aux Sujets 0</a>
                </div>
                """,
                status_code=404,
            )

        # Simple filiere configuration
        filiere_config = {
            "gen-1": {"yaml_file": None, "title": "Sujet Général 1", "pattern": "gen_sujet1_*"},
            "gen-2": {"yaml_file": None, "title": "Sujet Général 2", "pattern": "gen_sujet2_*"},
            "gen-3": {"yaml_file": None, "title": "Sujet Général 3", "pattern": "gen_sujet3_*"},
            "spe-1": {
                "yaml_file": "sujet_0_spe_sujet_1.yml",
                "title": "Sujet Spécialité 1",
                "pattern": "spe_sujet1_*",
            },
            "spe-2": {
                "yaml_file": "sujet_0_spe_sujet_2.yml",
                "title": "Sujet Spécialité 2",
                "pattern": "spe_sujet2_*",
            },
        }

        config = filiere_config[filiere_number]

        # Load YAML file if specified
        curriculum_data = None
        if config["yaml_file"]:
            yaml_path = (
                Path(settings.base_dir)
                / "official_curriculums"
                / "france"
                / "premiere"
                / "yamelized"
                / config["yaml_file"]
            )
            if yaml_path.exists():
                with open(yaml_path, "r", encoding="utf-8") as f:
                    curriculum_data = yaml.safe_load(f)

        # Find related generators
        generators_dir = Path(settings.base_dir) / "src" / "sujets0" / "generators"
        pattern = config["pattern"].replace("*", "")

        related_generators = []
        if generators_dir.exists():
            for gen_file in generators_dir.glob(f"{pattern}*.py"):
                if gen_file.name != "__init__.py":
                    related_generators.append(
                        {
                            "name": gen_file.stem,
                            "file": gen_file.name,
                            "path": f"/src/sujets0/generators/{gen_file.name}",
                        }
                    )

        related_generators.sort(key=lambda x: x["name"])

        # Build context for template
        context = {
            "request": request,
            "page": {"title": config["title"]},
            "filiere_number": filiere_number,
            "filiere_title": config["title"],
            "filiere_description": f"Questions officielles du curriculum - {config['title']}",
            "curriculum_data": curriculum_data,
            "related_generators": related_generators,
            "valid_filieres": valid_filieres,
            "has_official_data": bool(curriculum_data),
            "filiere_config": filiere_config,
        }

        # Add product context for consistent styling
        if sujets0_product:
            context.update(
                {
                    "product_name": sujets0_product.name,
                    "product_title": config["title"],
                    "product_description": context["filiere_description"],
                    "product_metatags": sujets0_product.metatags,
                    "current_product": sujets0_product,
                }
            )

        return settings.templates.TemplateResponse("sujets0/originals.html", context)

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

        # Add product-specific context if available (reusing sujets0 settings for scenery)
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
