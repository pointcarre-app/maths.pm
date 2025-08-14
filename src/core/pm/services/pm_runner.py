"""Entry point for the PMBuilder service.

This script builds PM objects from Markdown files in a specified directory.

Arguments:
    directory               Directory or file path containing markdown files to process
                            If not provided, a usage message will be displayed

Options:
    -v, --verbosity INT     Set verbosity level (0-3) [default: 0]
                              0: Only essential output
                              1: Basic processing information (per object)
                              2: Detailed processing information
                              3: Debug level information
    -h, --help              Show this help message and exit

Examples:


Output:
    The script will output the number of PMs successfully built.

"""


# python3 -m src.root.pm.services.pm_runner pms/pyly/index.md

# Not sure
# # Process all markdown files in a directory with default verbosity
# python -m root.pm.services.pm_runner ../markdowns/seconde/notion_de_fonction

# # Process with increased verbosity
# python -m root.pm.services.pm_runner ../markdowns/seconde/notion_de_fonction --verbosity 2

import argparse
import glob
import os
import traceback

from ..models.pm import PM
from .pm_builder import PMBuilder


def build_pm_from_file(filepath: str, verbosity: int = 0) -> PM:
    """Build a PM from a markdown file.

    Args:
        filepath: Path to the markdown file
        verbosity: Verbosity level for debugging

    Returns:
        PM object

    """
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    return PMBuilder.from_markdown(
        md_content=content,
        origin=filepath,
        verbosity=verbosity,
    )


def build_pms_from_directory(directory: str, pattern: str = "*.md", verbosity: int = 0) -> list[PM]:
    """Build PMs from all markdown files in a directory.

    Args:
        directory: Directory path
        pattern: Glob pattern to match files
        verbosity: Verbosity level for debugging

    Returns:
        List of PM objects

    """
    PMs = []
    for filepath in sorted(glob.glob(os.path.join(directory, pattern))):
        try:
            PM = build_pm_from_file(filepath, verbosity)
            PMs.append(PM)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error message: {e}")
            print(f"Error traceback: {traceback.format_exc()}")

    return PMs


if __name__ == "__main__":
    print("🏗️ -> 🧱 PM Builder Runner")

    # Parse command line arguments using argparse
    parser = argparse.ArgumentParser(description="PM Builder Runner")
    parser.add_argument("-v", "--verbosity", type=int, default=0, help="Set verbosity level (0-3)")
    parser.add_argument("directory", nargs="?", help="Directory or file path to process")

    # Parse args
    args = parser.parse_args()
    verbosity = args.verbosity
    directory = args.directory

    print(f"Running with: {directory}")

    if directory:
        # Check if the path is a file or directory
        if os.path.isfile(directory):
            # Single file processing
            try:
                PM = build_pm_from_file(directory, verbosity)
                PMs = [PM]
            except Exception as e:
                print(f"Error processing {directory}: {e}")
                print(f"Error type: {type(e)}")
                print(f"Error message: {e}")
                print(f"Error traceback: {traceback.format_exc()}")
                PMs = []
        else:
            # Directory processing
            PMs = build_pms_from_directory(directory, verbosity=verbosity)
        print(f"🧱🧱🧱🧱 Built {len(PMs)} PMs")

    else:
        print("No directory provided")
        print("Usage: python -m core.shared.runners.PM_builder_runner <filepath or directory>")
