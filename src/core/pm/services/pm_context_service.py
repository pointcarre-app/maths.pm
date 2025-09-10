#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
PM Context Service - Reusable PM loading and context preparation
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union
import logging

from .pm_runner import build_pm_from_file
from ....settings import settings, get_product_settings

logger = logging.getLogger("maths_pm")


class PMContextService:
    """Service for preparing PM context for templates"""

    @classmethod
    def load_pm_from_file(
        cls,
        pm_path: Union[str, Path],
        product_name: Optional[str] = None,
        origin: Optional[str] = None,
        debug: bool = False,
        extract_metatags: bool = True,
        verbosity: int = 0,
    ) -> Dict[str, Any]:
        """
        Load a PM file and prepare complete context for template rendering.

        Args:
            pm_path: Path to the PM markdown file
            product_name: Optional product name for loading product settings
            origin: Optional origin path for canonical URLs
            debug: Enable debug mode
            extract_metatags: Whether to extract metatags from PM metadata
            verbosity: Verbosity level for PM building

        Returns:
            Complete context dictionary ready for template rendering
        """
        # Convert to Path if string
        if isinstance(pm_path, str):
            pm_path = Path(pm_path)

        # Ensure absolute path
        if not pm_path.is_absolute():
            pm_path = settings.base_dir / pm_path

        if not pm_path.exists():
            raise FileNotFoundError(f"PM file not found: {pm_path}")

        # Build PM from file
        pm = build_pm_from_file(str(pm_path), verbosity=verbosity)

        # Convert to JSON for debugging
        pm_json = pm.model_dump_json()

        # Get product settings if product name provided
        product_settings = None
        if product_name:
            product_settings = get_product_settings(product_name)

        # Build base context
        context = {
            "pm": pm,
            "pm_json": pm_json,
            "debug": debug,
            "origin": origin,
            "product_name": product_name,
        }

        # Extract metatags if requested
        if extract_metatags:
            context["pm_metatags"] = cls._extract_metatags(pm)

        # Add product settings and related fields if available
        if product_settings:
            context.update(
                {
                    "product_settings": product_settings.to_dict(),
                    "product_title": product_settings.title,
                    "product_description": product_settings.description,
                    "product_backend_settings": product_settings.backend_settings,
                    "is_product_enabled": product_settings.is_enabled,
                }
            )
        else:
            context.update(
                {
                    "product_settings": None,
                    "product_title": None,
                    "product_description": None,
                    "product_backend_settings": None,
                    "is_product_enabled": False,
                }
            )

        # Add page title
        page_title = pm.title
        if pm.chapter:
            page_title = f"{pm.title} - {pm.chapter}"
        context["page"] = {"title": page_title}

        return context

    @classmethod
    def _extract_metatags(cls, pm) -> Dict[str, str]:
        """Extract metatags from PM metadata"""
        pm_metatags = {}

        if not pm.metadata:
            return pm_metatags

        # Common metatag fields
        metatag_fields = [
            "title",
            "description",
            "keywords",
            "author",
            "robots",
            "og:title",
            "og:description",
            "og:image",
            "og:url",
            "og:type",
            "twitter:card",
            "twitter:title",
            "twitter:description",
            "twitter:image",
            "DC.title",
            "DC.creator",
            "DC.subject",
            "DC.description",
            "abstract",
            "topic",
            "summary",
            "category",
            "revised",
            "pagename",
            "subtitle",
            "canonical",
        ]

        # Extract any metatag fields from metadata
        for field in metatag_fields:
            if field in pm.metadata:
                pm_metatags[field] = pm.metadata[field]

        # Also extract any fields with common metatag prefixes
        for key, value in pm.metadata.items():
            if any(key.startswith(prefix) for prefix in ["og:", "twitter:", "DC.", "itemprop"]):
                pm_metatags[key] = value

        return pm_metatags

    @staticmethod
    def load_pm_from_origin(origin: str, debug: bool = False, verbosity: int = 0) -> Dict[str, Any]:
        """
        Load a PM file from an origin path (e.g., "corsica/a_surface.md").
        Automatically extracts product name from the path.

        Args:
            origin: Origin path relative to pms/ directory
            debug: Enable debug mode
            verbosity: Verbosity level for PM building

        Returns:
            Complete context dictionary ready for template rendering
        """
        # Extract product name from origin
        origin_parts = origin.split("/")
        product_name = origin_parts[0] if origin_parts else None

        # Build full path
        pm_path = settings.base_dir / "pms" / origin

        # Use the main load function
        return PMContextService.load_pm_from_file(
            pm_path=pm_path,
            product_name=product_name,
            origin=origin,
            debug=debug,
            verbosity=verbosity,
        )

    @staticmethod
    def prepare_minimal_context(
        pm_content: str, product_name: Optional[str] = None, debug: bool = False
    ) -> Dict[str, Any]:
        """
        Prepare minimal context for PM rendering from raw markdown content.
        Useful for dynamic PM content that isn't from a file.

        Args:
            pm_content: Raw markdown content
            product_name: Optional product name for loading product settings
            debug: Enable debug mode

        Returns:
            Minimal context dictionary for template rendering
        """
        # This would require modifications to pm_runner to accept content directly
        # For now, raise NotImplementedError
        raise NotImplementedError(
            "Direct markdown content parsing not yet implemented. "
            "Use load_pm_from_file or load_pm_from_origin instead."
        )


# Convenience function for quick imports
def get_pm_context(
    pm_path: Union[str, Path], product_name: Optional[str] = None, **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to quickly get PM context.

    Example:
        from src.core.pm.services.pm_context_service import get_pm_context
        context = get_pm_context("pms/corsica/intro.md", product_name="corsica")
    """
    return PMContextService.load_pm_from_file(pm_path, product_name, **kwargs)
