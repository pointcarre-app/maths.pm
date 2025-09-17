#!/usr/bin/env python3
"""
Fix JupyterLite files availability by copying to the correct runtime location
"""

import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fix_jupyterlite_files():
    """Copy files from source to runtime JupyterLite location"""

    # Paths
    source_dir = Path("files-for-lite")
    runtime_output = Path("src/static/jupyterlite/_output")
    runtime_files = runtime_output / "files"

    logger.info(f"Source: {source_dir}")
    logger.info(f"Runtime output: {runtime_output}")
    logger.info(f"Runtime files: {runtime_files}")

    # Check if source exists
    if not source_dir.exists():
        logger.error(f"❌ Source directory not found: {source_dir}")
        return False

    # Check if runtime output exists
    if not runtime_output.exists():
        logger.error(f"❌ Runtime output directory not found: {runtime_output}")
        logger.info("Run the server first to build JupyterLite")
        return False

    # Create files directory if it doesn't exist
    runtime_files.mkdir(exist_ok=True)

    # Copy all files from source to runtime
    logger.info("📦 Copying files to runtime location...")

    copied = 0
    for item in source_dir.rglob("*"):
        if item.is_file():
            # Calculate relative path
            rel_path = item.relative_to(source_dir)
            dest_path = runtime_files / rel_path

            # Create parent directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            try:
                shutil.copy2(item, dest_path)
                copied += 1
                logger.debug(f"Copied: {rel_path}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to copy {rel_path}: {e}")

    logger.info(f"✅ Copied {copied} files to runtime location")

    # Verify
    if runtime_files.exists():
        total_files = len([f for f in runtime_files.rglob("*") if f.is_file()])
        logger.info(f"📊 Total files in runtime location: {total_files}")

        # Check data directory specifically
        data_dir = runtime_files / "data"
        if data_dir.exists():
            data_files = len([f for f in data_dir.rglob("*") if f.is_file()])
            logger.info(f"📁 Data files: {data_files}")

            # List some data files
            for root, dirs, files in data_dir.walk():
                if files:
                    rel_root = root.relative_to(data_dir)
                    logger.info(f"  📂 {rel_root}: {files[:3]}{'...' if len(files) > 3 else ''}")

        return True

    return False


if __name__ == "__main__":
    print("🔧 Fixing JupyterLite files availability...")
    success = fix_jupyterlite_files()
    if success:
        print("\n🎉 SUCCESS! Your data should now be visible in JupyterLite.")
        print("\n🚀 Access JupyterLite at:")
        print("   http://localhost:8000/static/jupyterlite/_output/lab/index.html")
    else:
        print("\n❌ Failed to fix files. Check the logs above.")
