#!/usr/bin/env python3
"""
Test script to verify all routes are properly configured for static site generation.
This script validates that the build system includes all necessary routes.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.build import StaticSiteBuilder


def test_route_generation():
    """Test that all expected routes are generated"""
    print("🧪 Testing route generation...")

    builder = StaticSiteBuilder()

    # Test PM route generation
    markdown_routes, asset_routes = builder._generate_pm_routes()

    print("\n📊 Route Statistics:")
    print(f"   - Markdown routes: {len(markdown_routes)}")
    print(f"   - Asset routes: {len(asset_routes)}")
    print(f"   - Total PM routes: {len(markdown_routes) + len(asset_routes)}")

    # Verify expected markdown files exist
    expected_markdown_patterns = [
        "documentation/README.md",
        "corsica/a_troiz_geo.md",
        "corsica/e_seconde_stats_python.md",
        "pyly/00_index.md",
        "pyly/01_premiers_pas.md",
        "examples/i_radio_example.md",
    ]

    print("\n✅ Checking expected markdown routes:")
    for pattern in expected_markdown_patterns:
        found = any(pattern in route for route in markdown_routes)
        status = "✓" if found else "✗"
        print(f"   {status} /pm/{pattern}")
        if not found:
            print("     ⚠️ WARNING: Expected route not found!")

    # Verify expected asset files exist
    expected_asset_patterns = [
        "corsica/files/",  # Should have SVG files
    ]

    print("\n✅ Checking expected asset routes:")
    for pattern in expected_asset_patterns:
        found = any(pattern in route for route in asset_routes)
        status = "✓" if found else "✗"
        print(f"   {status} Assets in /pm/{pattern}")
        if not found:
            print("     ⚠️ WARNING: Expected assets not found!")

    # List all unique file extensions found
    extensions = set()
    for route in asset_routes:
        path = Path(route)
        if path.suffix:
            extensions.add(path.suffix)

    if extensions:
        print(f"\n📁 Asset file types found: {', '.join(sorted(extensions))}")

    return markdown_routes, asset_routes


def check_required_routes():
    """Check that all required API and core routes are defined"""
    print("\n🔍 Checking required routes in build configuration...")

    # Read the build.py file to check route definitions
    build_file = Path(__file__).parent.parent / "src" / "build.py"
    build_content = build_file.read_text()

    required_routes = {
        "Core": ["/", "/readme", "/settings", "/pm", "/kill-service-workers"],
        "API": ["/api/health", "/api/settings", "/api/settings/serialized", "/api/build"],
        "Products": ["/sujets0", "/corsica/", "/nagini"],
        "JupyterLite": ["/jupyterlite/", "/jupyter", "/jupyter/repl"],
        "Documentation": ["/openapi.json", "/docs", "/redoc"],
    }

    print("\n📋 Required routes by category:")
    for category, routes in required_routes.items():
        print(f"\n{category}:")
        for route in routes:
            # Simple check if route is mentioned in the build file
            found = f'"{route}"' in build_content or f"'{route}'" in build_content
            status = "✓" if found else "✗"
            print(f"   {status} {route}")
            if not found:
                print("     ⚠️ WARNING: Route not found in build.py!")

    return all(
        f'"{route}"' in build_content or f"'{route}'" in build_content
        for routes in required_routes.values()
        for route in routes
    )


def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 Static Site Build Route Verification")
    print("=" * 60)

    # Test PM route generation
    markdown_routes, asset_routes = test_route_generation()

    # Check required routes
    all_routes_present = check_required_routes()

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total PM routes discovered: {len(markdown_routes) + len(asset_routes)}")
    print(f"  - Markdown files: {len(markdown_routes)}")
    print(f"  - Asset files: {len(asset_routes)}")
    print(f"Required routes configured: {'✅ Yes' if all_routes_present else '❌ No'}")

    if not all_routes_present:
        print("\n⚠️ WARNING: Some required routes are missing from build.py!")
        print("Please review the warnings above and update the build configuration.")
        return 1

    print("\n✅ All route checks passed!")
    print("The build system is properly configured for static site generation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
