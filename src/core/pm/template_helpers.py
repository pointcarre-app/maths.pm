#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
PM Template Helpers - Jinja functions for dynamic PM rendering
"""

from typing import Optional, Dict, Any
import logging

from .services.pm_context_service import PMContextService

logger = logging.getLogger("maths_pm")


def load_pm_for_template(
    pm_path: str, product_name: Optional[str] = None, debug: bool = False
) -> Dict[str, Any]:
    """
    Load a PM file and return context for template rendering.
    This function is designed to be called from within Jinja templates.

    Args:
        pm_path: Path to the PM file (relative to base_dir or absolute)
        product_name: Optional product name for settings
        debug: Enable debug mode

    Returns:
        Dictionary with PM context or error information
    """
    try:
        # If path doesn't start with 'pms/', assume it's relative to pms/
        if not pm_path.startswith("/") and not pm_path.startswith("pms/"):
            pm_path = f"pms/{pm_path}"

        # Load PM using the service
        context = PMContextService.load_pm_from_file(
            pm_path=pm_path, product_name=product_name, debug=debug
        )

        # Add success flag
        context["pm_loaded"] = True
        context["pm_error"] = None

        return context

    except FileNotFoundError:
        logger.warning(f"PM file not found: {pm_path}")
        return {
            "pm": None,
            "pm_loaded": False,
            "pm_error": f"File not found: {pm_path}",
            "pm_json": None,
            "product_settings": None,
        }
    except Exception as e:
        logger.error(f"Error loading PM file {pm_path}: {e}")
        return {
            "pm": None,
            "pm_loaded": False,
            "pm_error": str(e),
            "pm_json": None,
            "product_settings": None,
        }


def register_pm_helpers(templates):
    """
    Register PM helper functions with the Jinja template environment.

    Args:
        templates: Jinja2Templates instance from FastAPI
    """
    # Add the load_pm function to global template context
    templates.env.globals["load_pm"] = load_pm_for_template

    # Also add as a filter for different usage patterns
    templates.env.filters["load_pm"] = load_pm_for_template

    logger.info("✅ PM template helpers registered")
