#!/usr/bin/env python3
"""
Script to add metatags to PM markdown files that don't have them yet.
"""

import os
from pathlib import Path

# Define metatag templates for different file categories
METATAG_TEMPLATES = {
    "i_radio": {
        "title": "Interactive Radio Button Components",
        "description": "Guide for creating interactive radio button questions and quizzes in PM pages",
        "keywords": "i_radio, radio buttons, interactive, quiz, questions, PM components",
        "category": "Components, Interactive, Documentation",
    },
    "fragments": {
        "title": "PM Fragments System",
        "description": "Understanding and using the PM fragments architecture for content creation",
        "keywords": "fragments, PM system, content, architecture, components",
        "category": "Architecture, Documentation",
    },
    "layout": {
        "title": "Layout Directives and Responsive Design",
        "description": "Guide for creating responsive layouts with PM layout directives",
        "keywords": "layout, responsive, directives, columns, PM design",
        "category": "Layout, Design, Documentation",
    },
    "number_input": {
        "title": "Number Input Components",
        "description": "Interactive number input fields for mathematical exercises",
        "keywords": "number input, forms, interactive, mathematics, components",
        "category": "Components, Forms, Documentation",
    },
}


def get_file_category(filename):
    """Determine category based on filename."""
    fn = filename.lower()
    if "i_radio" in fn:
        return "i_radio"
    elif "fragment" in fn:
        return "fragments"
    elif "layout" in fn:
        return "layout"
    elif "number" in fn:
        return "number_input"
    else:
        return "fragments"  # default


def create_metatags(filepath, filename):
    """Create appropriate metatags based on file content."""
    category = get_file_category(filename)
    template = METATAG_TEMPLATES[category]

    # Create specific title based on filename
    title_base = filename.replace(".md", "").replace("_", " ").title()

    return f"""---
# Page-specific metatags
title: "{title_base} - {template["title"]}"
description: "{template["description"]}"
keywords: "{template["keywords"]}"
author: "Maths.pm - Documentation Team"
robots: "index, follow"
# Open Graph metatags
og:title: "{title_base}"
og:description: "{template["description"]}"
og:type: "article"
og:url: "https://maths.pm/pm/{filepath}"
# Twitter Card metatags
twitter:card: "summary"
twitter:title: "{title_base}"
twitter:description: "PM System Documentation"
# Additional metatags
topic: "PM System Documentation"
category: "{template["category"]}"
revised: "2025-01-15"
pagename: "{title_base}"
---"""


def update_file(filepath):
    """Update a markdown file with metatags if it doesn't have them."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if file already has comprehensive metatags
    if "# Page-specific metatags" in content or "og:title" in content:
        print(f"  ✅ Skipping {filepath} (already has metatags)")
        return False

    # Get relative path for URL
    rel_path = str(filepath).replace(str(Path.cwd()) + "/pms/", "")
    filename = os.path.basename(filepath)

    # Create metatags
    metatags = create_metatags(rel_path, filename)

    # If file starts with ---, update it
    if content.startswith("---"):
        # Find the end of existing front matter
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Merge with existing front matter
            existing = parts[1].strip()
            new_content = metatags[3:-3]  # Remove --- markers
            content = f"---\n{existing}\n{new_content}\n---{parts[2]}"
        else:
            content = metatags + "\n" + content[3:]
    else:
        # Add new front matter
        content = metatags + "\n" + content

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✅ Updated {filepath}")
    return True


def main():
    """Process all markdown files in pms/documentation and pms/examples."""
    base_dir = Path.cwd() / "pms"

    # Process documentation files
    print("📚 Processing documentation files...")
    doc_dir = base_dir / "documentation"
    for filepath in doc_dir.glob("*.md"):
        if filepath.name not in ["README.md", "pm_metatags_guide.md"]:  # Skip already done
            update_file(filepath)

    # Process example files
    print("\n📝 Processing example files...")
    ex_dir = base_dir / "examples"
    for filepath in ex_dir.glob("*.md"):
        if filepath.name != "metatags_example.md":  # Skip already done
            update_file(filepath)

    print("\n✨ Done!")


if __name__ == "__main__":
    main()
