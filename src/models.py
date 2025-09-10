#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Data models for the application.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ProductModel:
    """Represents a product, initialized from YAML data."""

    def __init__(self, data: Dict[str, Any]):
        self.domains: List[str] = data.get("domains", [])
        self.name: str = data.get("name", "")
        self.title_html: str = data.get("title_html", "")
        self.product_type: Optional[str] = data.get("product_type")  # New field (e.g., "repo")
        # Support both 'hidden' and 'is_hidden' for backward compatibility
        self.is_hidden: bool = (
            str(data.get("is_hidden", "")).lower() == "true"
            or str(data.get("hidden", "")).lower() == "true"
        )
        self.is_beta: bool = str(data.get("is_beta", "")).lower() == "true"
        self.subtitle_html: Optional[str] = data.get("subtitle_html")
        self.description: str = data.get("description", "")
        self.local_path: Optional[str] = data.get("local_path")
        self.source_link: Optional[str] = data.get("source_link")
        self.is_source_private: bool = str(data.get("is_source_private", "")).lower() == "true"
        self.figure_svg: Optional[str] = data.get("figure_svg")
        self.figure_png: Optional[str] = data.get("figure_png")
        self.color: str = data.get("color", "primary")
        self.classes_formatted: Optional[List[str]] = data.get("classes_formatted")
        self.tags: Optional[List[str]] = data.get("tags")
        self.owner_rdb: str = data.get("owner_rdb", "")
        self.owner_url: str = data.get("owner_url", "")
        # Add backend settings support
        self.backend_settings: Dict[str, Any] = data.get("backend_settings", {})
        # Add metatags support for product-specific SEO
        self.metatags: Dict[str, Any] = data.get("metatags", {})

    def to_template_context(self) -> Dict[str, Any]:
        """Convert to template context format."""
        return self.__dict__

    def __repr__(self):
        """Clean representation for logging."""
        return f"ProductModel(name='{self.name}', type='{self.product_type or 'standard'}', hidden={self.is_hidden}, beta={self.is_beta})"


class ProductSettings:
    """
    🎯 PRODUCT-SPECIFIC SETTINGS CLASS

    Each loaded product gets its own instance of this class.
    Contains all the configuration and settings specific to that product.

    Usage: Import the specific product settings in each router
    Example: `from ..settings import nagini_settings, jupyterlite_settings`
    """

    def __init__(self, product: ProductModel):
        """Initialize with a ProductModel instance."""
        self.product = product
        self.name = product.name
        self.backend_settings = product.backend_settings

    @property
    def title(self) -> str:
        """Product title for display."""
        return self.product.title_html

    @property
    def description(self) -> str:
        """Product description."""
        return self.product.description

    @property
    def local_path(self) -> Optional[str]:
        """Local path/route for this product."""
        return self.product.local_path

    @property
    def is_enabled(self) -> bool:
        """Check if this product is enabled (has backend settings)."""
        return bool(self.backend_settings)

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a specific backend setting for this product.

        Args:
            key: The setting key to retrieve
            default: Default value if key not found

        Returns:
            The setting value or default
        """
        return self.backend_settings.get(key, default)

    def get_nested_setting(self, *keys: str, default: Any = None) -> Any:
        """
        Get a nested setting using dot notation.

        Example: get_nested_setting('jupyterlite', 'version')
        Gets backend_settings['jupyterlite']['version']
        """
        current = self.backend_settings
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for template context."""
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "local_path": self.local_path,
            "is_enabled": self.is_enabled,
            "backend_settings": self.backend_settings,
            "product": self.product.to_template_context(),
        }


# --- Robust Domain Configuration Models ---


class ExtraHeadModel(BaseModel):
    """Defines the structure for extra JS/CSS dependencies."""

    js: List[str] = Field(default_factory=list)
    css: List[str] = Field(default_factory=list)


class TemplatingModel(BaseModel):
    """Defines the structure for templating settings."""

    base_template: str
    footer_template: str
    navbar_title: str
    button_primary_text: str
    button_primary_href: str
    button_ghost_text: str
    button_ghost_href: str
    rgpd_template: str


class DomainModel(BaseModel):
    """
    A robust Pydantic model for the entire domain configuration.
    It provides default values for optional sections to prevent template errors.
    Backend settings are now loaded from individual products.
    """

    domain_url: str
    domain_specific_metatags: Dict[str, Any] = Field(default_factory=dict)
    index_view_specific_metatags: Dict[str, Any] = Field(default_factory=dict)
    templating: TemplatingModel
    extra_head: ExtraHeadModel = Field(default_factory=ExtraHeadModel)
    # Keep backend_settings for backward compatibility, but it will be empty
    backend_settings: Dict[str, Any] = Field(default_factory=dict)
