#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025 SAS POINTCARRE.APP
"""
Settings configuration for Maths.pm FastAPI application
Uses Pydantic Settings for type-safe configuration management
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from strictyaml import Any as YamlAny, Map, MapPattern, Optional as StrictOptional, Seq, Str, load

import logging
import yaml

from .models import ProductModel, DomainModel, ProductSettings

# Get the logger instance from the app
logger = logging.getLogger("maths_pm")


# Global constants - defined once and used throughout
_BASE_DIR = Path(__file__).parent.parent
_SRC_DIR = Path(__file__).parent

# Schema for a single product
product_schema = Map(
    {
        "name": Str(),
        "title_html": Str(),
        StrictOptional("font_class"): Str(),
        StrictOptional("is_hidden"): Str(),
        StrictOptional("is_beta"): Str(),
        StrictOptional("subtitle_html"): Str(),
        "description": Str(),
        StrictOptional("local_path"): Str(),
        StrictOptional("source_link"): Str(),
        StrictOptional("figure_svg"): Str(),
        StrictOptional("figure_png"): Str(),
        "color": Str(),
        StrictOptional("classes_formatted"): Seq(Str()),
        StrictOptional("tags"): Seq(Str()),
        "domains": Seq(Str()),
        "owner_rdb": Str(),
        "owner_url": Str(),
        # Add backend_settings support
        StrictOptional("backend_settings"): MapPattern(Str(), YamlAny()),
    }
)

# Schema for the main domain configuration
domain_config_schema = Map(
    {
        "domain_url": Str(),
        "domain_specific_metatags": MapPattern(Str(), YamlAny()),
        "index_view_specific_metatags": MapPattern(Str(), YamlAny()),
        "templating": Map(
            {
                "base_template": Str(),
                "footer_template": Str(),
                "navbar_title": Str(),
                "button_primary_text": Str(),
                "button_primary_href": Str(),
                "button_ghost_text": Str(),
                "button_ghost_href": Str(),
            }
        ),
        StrictOptional("extra_head"): Map(
            {
                StrictOptional("js"): Seq(Str()),
                StrictOptional("css"): Seq(Str()),
            }
        ),
        "backend_settings": MapPattern(Str(), YamlAny()),
    }
)


class Settings(BaseSettings):
    """
    🎯 MAIN SETTINGS CLASS - The Single Source of Truth

    This class manages ALL application configuration:
    - Loads domain config from domains/maths.pm.yml
    - Loads and filters products from products/*.yml (only matching domain)
    - Provides template context and backend settings
    - Handles JupyterLite configuration

    Usage: Import the singleton instance `settings` from this module
    Example: `from .settings import settings`
    """

    # Core application settings
    base_dir: Path = Field(default=_BASE_DIR, description="Base directory of the project")
    src_dir: Path = Field(default=_SRC_DIR, description="Source directory")
    domain_name: str = Field(default="maths.pm", description="Domain name for the application")
    app_title: str = Field(default="Maths.pm Static Generator", description="FastAPI app title")
    app_version: str = Field(default="2.0.0", description="Application version")

    # JupyterLite configuration - ENABLED BY DEFAULT
    jupyterlite_enabled: bool = Field(default=True, description="Enable JupyterLite integration")
    jupyterlite_auto_install: bool = Field(
        default=True, description="Automatically install JupyterLite if missing"
    )

    @computed_field
    @property
    def domain_config(self) -> DomainModel:
        """
        Loads the domain configuration file and parses it with the Pydantic model.
        """
        config_path = self.base_dir / "domains" / "maths.pm.yml"
        logger.info(f"Loading domain configuration from: {config_path}")

        if not config_path.exists():
            logger.critical(f"Domain configuration file not found: {config_path}")
            # Fallback to a minimal default to prevent crashing
            return DomainModel(domain_url="", templating={})

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                # Use the standard, more forgiving YAML loader
                yaml_data = yaml.safe_load(f)
                return DomainModel(**yaml_data)
        except Exception as e:
            logger.critical(
                f"FATAL: Invalid domain configuration in {config_path}: {e}", exc_info=True
            )
            # Fallback to a minimal default
            return DomainModel(domain_url="", templating={})

    @computed_field
    @property
    def products(self) -> List[ProductModel]:
        """Load and validate all products for the current domain."""
        logger.debug("=" * 20 + " Starting Product Loading " + "=" * 20)
        products_dir = self.products_dir
        logger.debug(f"Scanning for products in: {products_dir}")

        if not products_dir.exists():
            logger.critical("Products directory not found. No products will be loaded.")
            return []

        product_files = sorted(products_dir.glob("*.yml"))
        logger.debug(f"Found {len(product_files)} YAML files: {[p.name for p in product_files]}")

        loaded_products = []
        for product_file in product_files:
            logger.debug(f"--- Processing file: {product_file.name} ---")
            try:
                with open(product_file, "r", encoding="utf-8") as f:
                    yaml_content = f.read()
                    logger.debug(f"Raw YAML content:\n{yaml_content}")
                    product_yaml = load(yaml_content, product_schema)
                    logger.debug("YAML content is valid against schema.")

                    product_domains = product_yaml["domains"].data
                    logger.debug(
                        f"Checking if product domains {product_domains} match current domain '{self.domain_name}'..."
                    )

                    if self.domain_name in product_domains:
                        logger.info(f"Domain match! Loading '{product_file.name}' as a product.")
                        product_data = product_yaml.data
                        loaded_products.append(ProductModel(product_data))
                    else:
                        logger.warning(f"Domain mismatch for '{product_file.name}'. Skipping.")

            except Exception as e:
                logger.error(f"FATAL ERROR loading product {product_file.name}: {e}", exc_info=True)

        logger.debug("=" * 20 + " Finished Product Loading " + "=" * 20)
        logger.info(f"Total products loaded: {len(loaded_products)}")
        logger.debug(f"Loaded product names: {[p.name for p in loaded_products]}")
        return loaded_products

    @computed_field
    @property
    def serialized_backend_settings(self) -> Dict[str, str]:
        """
        Serialize backend settings for template use.

        Templates need strings, so we convert complex objects (lists/dicts) to JSON strings.
        This is why the /settings endpoint looks messy - it's template-ready data.
        """
        # Get the clean aggregated settings
        aggregated_settings = self.aggregated_backend_settings
        serialized = {}

        # Convert complex objects to JSON strings for template compatibility
        for key, value in aggregated_settings.items():
            if isinstance(value, (list, dict)):
                # Complex objects become JSON strings for templates
                serialized[key] = json.dumps(value)
            else:
                # Simple values become strings
                serialized[key] = str(value)
        return serialized

    @computed_field
    @property
    def aggregated_backend_settings(self) -> Dict[str, Any]:
        """
        Aggregate backend settings from all loaded products.

        This creates a clean dict with raw Python objects (not JSON strings).
        Each product's backend_settings section gets merged into one dict.
        """
        aggregated = {}

        # Go through each loaded product (already domain-filtered)
        for product in self.products:
            if hasattr(product, "backend_settings") and product.backend_settings:
                logger.debug(f"Merging backend settings from product: {product.name}")

                # Merge this product's backend settings into the main dict
                for key, value in product.backend_settings.items():
                    aggregated[key] = value
                    logger.debug(f"  Added setting: {key}")

        logger.debug(f"Final aggregated backend settings keys: {list(aggregated.keys())}")
        return aggregated

    @computed_field
    @property
    def jupyterlite_dir(self) -> Path:
        """JupyterLite build output directory"""
        return self.static_dir / "jupyterlite"

    @computed_field
    @property
    def jupyterlite_content_dir(self) -> Path:
        """JupyterLite content source directory"""
        return self.base_dir / "files-for-lite"

    jupyterlite_version: str = Field(default="0.4.3", description="JupyterLite version to use")
    jupyterlite_kernels: List[str] = Field(default=["python"], description="Available kernels")
    jupyterlite_packages: List[str] = Field(
        default=["numpy", "matplotlib", "sympy"], description="Pre-installed packages"
    )

    # Pyodide configuration (for JupyterLite)
    pyodide_version: str = Field(default="0.26.4", description="Pyodide version")
    pyodide_packages: List[str] = Field(
        default=["micropip", "numpy", "matplotlib"], description="Pyodide packages"
    )

    # ------------------------------------------------------------------
    # PCA Codex support
    # ------------------------------------------------------------------
    def build_codex_path_from_script_path(self, script_path: str) -> Path:
        """Resolve the absolute path to a codex script file.

        By convention, codex files are stored under the repository-level
        'files/' directory. The script_path is a POSIX-like relative path
        such as 'pyly/premiers-pas-affichages-strings.py'.
        """
        return (self.base_dir / "files" / script_path).resolve()

    @computed_field
    @property
    def templates_dir(self) -> Path:
        return self.src_dir / "templates"

    @computed_field
    @property
    def static_dir(self) -> Path:
        return self.src_dir / "static"

    @computed_field
    @property
    def images_files_dir(self) -> Path:
        """Directory for user-provided images served at /images."""
        return self.base_dir / "files" / "images"

    @computed_field
    @property
    def assets_dir(self) -> Path:
        return self.base_dir / "assets"

    @computed_field
    @property
    def dist_dir(self) -> Path:
        return self.base_dir / "dist"

    @computed_field
    @property
    def domain_config_file(self) -> str:
        return f"{self.domain_name}.yml"

    @computed_field
    @property
    def domains_config_path(self) -> Path:
        return self.base_dir / "domains" / self.domain_config_file

    @computed_field
    @property
    def products_dir(self) -> Path:
        return self.base_dir / "products"

    @computed_field
    @property
    def templates(self) -> Jinja2Templates:
        """
        Creates and configures the Jinja2Templates instance.
        Injects global variables that should be available in all templates.
        """
        templates = Jinja2Templates(directory=str(self.templates_dir))
        templates.env.globals["DOMAIN_CONFIG"] = (
            self.domain_config.dict()
        )  # Use dict() to get a plain dict
        templates.env.globals["products"] = self.products
        templates.env.globals["backend_public_settings"] = self.serialized_backend_settings
        return templates

    @computed_field
    @property
    def static_files(self) -> StaticFiles:
        return StaticFiles(directory=str(self.static_dir))

    @computed_field
    @property
    def assets_files(self) -> StaticFiles:
        return StaticFiles(directory=str(self.assets_dir))

    def assets_exist(self) -> bool:
        return self.assets_dir.exists()

    def jupyterlite_built(self) -> bool:
        """Check if JupyterLite has been built properly"""
        output_dir = self.jupyterlite_dir / "_output"
        return (
            output_dir.exists()
            and (output_dir / "lab" / "index.html").exists()
            and (output_dir / "repl" / "index.html").exists()
        )

    def get_jupyterlite_config(self) -> Dict[str, Any]:
        return {
            "enabled": self.jupyterlite_enabled,
            "version": self.jupyterlite_version,
            "kernels": self.jupyterlite_kernels,
            "packages": self.jupyterlite_packages,
            "pyodide": {"version": self.pyodide_version, "packages": self.pyodide_packages},
        }

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


# ============================================================================
# SINGLE GLOBAL SETTINGS INSTANCE
# ============================================================================
# This is THE ONLY settings instance in the entire application.
# Import this everywhere you need settings: `from .settings import settings`
# No more global variables, no more confusion!
settings = Settings()

# ============================================================================
# PRODUCT-SPECIFIC SETTINGS INSTANCES - DYNAMICALLY CREATED
# ============================================================================
# Each loaded product gets its own settings instance.
# Import these in routers: `from ..settings import nagini_settings, jupyterlite_settings`


def _create_product_settings_instances():
    """
    🎯 DYNAMICALLY CREATE PRODUCT SETTINGS INSTANCES

    This function creates individual ProductSettings instances for each loaded product
    and makes them available as module-level variables using globals().

    After this runs, you can import: `from ..settings import nagini_settings, jupyterlite_settings`
    """
    from .models import ProductSettings

    logger.info("🎯 Creating individual product settings instances...")

    # Clear any existing product settings from globals
    current_globals = dict(globals())
    for key in current_globals:
        if key.endswith("_settings") and key != "settings":
            globals().pop(key, None)

    # Create new instances for each loaded product
    created_instances = []

    for product in settings.products:
        # Create the ProductSettings instance
        product_settings = ProductSettings(product)

        # Create the variable name (e.g., 'nagini' -> 'nagini_settings')
        settings_var_name = f"{product.name}_settings"

        # Add to module globals so it can be imported
        globals()[settings_var_name] = product_settings

        created_instances.append(settings_var_name)
        logger.info(
            f"   ✅ Created {settings_var_name} -> {product_settings.__class__.__name__}('{product.name}')"
        )

    logger.info(f"🎉 Created {len(created_instances)} product settings instances")
    logger.info(f"📦 Available for import: {', '.join(created_instances)}")

    return created_instances


# ============================================================================
# INITIALIZE PRODUCT SETTINGS INSTANCES
# ============================================================================
# This runs when the module is imported and creates all product settings instances
_available_product_settings = _create_product_settings_instances()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def get_product_settings(product_name: str) -> Optional["ProductSettings"]:
    """
    Get product settings by name.

    Args:
        product_name: Name of the product (e.g., 'nagini', 'jupyterlite')

    Returns:
        ProductSettings instance or None if not found
    """
    settings_var_name = f"{product_name}_settings"
    return globals().get(settings_var_name)


def list_available_product_settings() -> List[str]:
    """
    List all available product settings instances.

    Returns:
        List of available product settings variable names
    """
    return [key for key in globals().keys() if key.endswith("_settings") and key != "settings"]


def reload_product_settings():
    """
    Reload all product settings instances.

    Useful for development when products change.
    """
    logger.info("🔄 Reloading product settings instances...")
    return _create_product_settings_instances()


# Log what's available at module load time
logger.info(f"📋 Module loaded with product settings: {list_available_product_settings()}")
