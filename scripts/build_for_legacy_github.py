#!/usr/bin/env python3
"""
Helper script to build for legacy GitHub Pages (pointcarre-app.github.io/maths.pm)
This is a wrapper around build_for_github.py with LEGACY_GITHUB_PAGES=true
"""

import os
import sys
from pathlib import Path

# Set the legacy GitHub Pages flag
os.environ["LEGACY_GITHUB_PAGES"] = "true"

# Add the current directory to path and import the main build function
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    print("📄 Building for legacy GitHub Pages (pointcarre-app.github.io/maths.pm)...")
    print("📝 Setting LEGACY_GITHUB_PAGES=true")

    # Import and run the main build function
    from build_for_github import build_static_site
    import asyncio

    success = asyncio.run(build_static_site())
    sys.exit(0 if success else 1)
