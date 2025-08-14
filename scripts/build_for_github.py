#!/usr/bin/env python3
"""
GitHub Pages static site builder.
Builds the site with proper base path for GitHub Pages deployment.
"""

import asyncio
import sys
import logging
import time
import threading
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from src import app
from src.build import build_static_site as build_func

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_server():
    """Run the FastAPI server in a background thread"""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)


async def build_for_github():
    """Build the static site with GitHub Pages configuration"""
    logger.info("🚀 Building static site for GitHub Pages...")

    # For GitHub Pages at https://pointcarre-app.github.io/maths.pm/
    # we need to set the base_path to /maths.pm
    result = await build_func(
        base_url="http://127.0.0.1:8000",
        base_path="/maths.pm",  # This is the repository name
    )

    return result


def main():
    """Main function to coordinate server startup and build"""
    logger.info("🚀 Starting GitHub Pages static site build...")

    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    logger.info("Waiting for server to start...")
    time.sleep(3)

    # Run the build with GitHub Pages configuration
    result = asyncio.run(build_for_github())

    if result.get("status") in ["success", "partial"]:
        logger.info("✅ Build completed successfully!")
        logger.info(f"📊 Routes exported: {result.get('successful')}/{result.get('total_routes')}")
        logger.info(f"📁 Output directory: {result.get('output_dir')}")
        logger.info("🚀 Ready for GitHub Pages deployment!")
        return 0
    else:
        logger.error("❌ Build failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
