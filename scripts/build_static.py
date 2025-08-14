#!/usr/bin/env python3
"""
Local static site builder for testing before deployment.
Run this script to generate the static site locally.
"""

import asyncio
import sys
import logging
import time
import threading
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
import uvicorn
from src import app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_server():
    """Run the FastAPI server in a background thread"""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)


async def build_static_site():
    """Build the static site by calling the API endpoint"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Check server health
            logger.info("Checking server health...")
            health_response = await client.get("http://127.0.0.1:8000/api/health")
            health_response.raise_for_status()
            health_data = health_response.json()
            logger.info(f"Server is healthy: {health_data}")

            # Trigger build
            logger.info("Starting static site build...")
            response = await client.get("http://127.0.0.1:8000/api/build")
            response.raise_for_status()
            result = response.json()

            # Display results
            if result.get("status") == "success":
                logger.info("✅ Build successful!")
            elif result.get("status") == "partial":
                logger.warning("⚠️ Build partially successful")
            else:
                logger.error("❌ Build failed")

            logger.info(
                f"📊 Routes exported: {result.get('successful')}/{result.get('total_routes')}"
            )
            logger.info(f"📁 Output directory: {result.get('output_dir')}")

            # Show failed routes if any
            failed_routes = [r for r in result.get("routes", []) if not r.get("success")]
            if failed_routes:
                logger.warning("Failed routes:")
                for route in failed_routes:
                    logger.warning(f"  - {route.get('route')}")

            return result.get("status") in ["success", "partial"]

    except Exception as e:
        logger.error(f"Build failed with error: {e}")
        return False


def main():
    """Main function to coordinate server startup and build"""
    logger.info("🚀 Starting local static site build...")

    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    logger.info("Waiting for server to start...")
    time.sleep(3)

    # Run the build
    success = asyncio.run(build_static_site())

    if success:
        logger.info("✅ Build completed successfully!")
        logger.info("📝 You can now test the static site in the 'dist' directory")
        logger.info("💡 Tip: Use 'python -m http.server 8080 -d dist' to serve the static files")
        return 0
    else:
        logger.error("❌ Build failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
