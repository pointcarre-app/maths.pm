#!/usr/bin/env python3
"""
PM FS Service
Utilities for PM folder navigation and file preview data.

This module centralizes file-system related logic used by the PM routes so that
the web views stay minimal and declarative.
"""

from __future__ import annotations

from pathlib import Path
import mimetypes
from typing import Any, Dict, Optional


def build_pm_tree(base_pms_dir: Path, root_dir: Path) -> Dict[str, Any]:
    """Build a nested dict representing a PM directory tree.

    Includes both directories and files. Files carry an `is_md` flag so the UI
    (or router) can decide whether to render as a PM or as an asset preview.
    """

    def build_tree(current: Path) -> Dict[str, Any]:
        rel_path = current.relative_to(base_pms_dir)
        node: Dict[str, Any] = {
            "name": current.name or str(rel_path),
            "rel_path": str(rel_path),
            "is_dir": current.is_dir(),
            "children": [],
        }

        if current.is_dir():
            entries = sorted(
                list(current.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower())
            )
            for entry in entries:
                if entry.is_dir():
                    node["children"].append(build_tree(entry))
                else:
                    node["children"].append(
                        {
                            "name": entry.name,
                            "rel_path": str(entry.relative_to(base_pms_dir)),
                            "is_dir": False,
                            "is_md": entry.suffix.lower() == ".md",
                        }
                    )

        return node

    return build_tree(root_dir)


def resolve_pm_path(origin: str, base_dir: Path) -> Path:
    """Resolve a PM-origin into an absolute file system path.

    Tries `<base_dir>/pms/<origin>` first, then `<base_dir>/<origin>` for assets.
    """
    candidate = base_dir / "pms" / origin
    if candidate.exists():
        return candidate
    candidate2 = base_dir / origin
    return candidate2


def guess_media_type(path: Path) -> str:
    media_type, _ = mimetypes.guess_type(str(path))
    return media_type or "application/octet-stream"


def is_text_like_media(media_type: str) -> bool:
    return media_type.startswith("text/") or media_type in {
        "application/json",
        "application/xml",
        "image/svg+xml",
    }


def read_text_if_possible(path: Path, media_type: str) -> Optional[str]:
    if is_text_like_media(media_type):
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None
    return None


def build_file_preview_data(
    *,
    path: Path,
    origin: str,
    base_dir: Path,
) -> Dict[str, Any]:
    """Prepare an asset preview context (view-agnostic).

    Returns a plain dict that a view can pass to a template, including:
    - file name, relative path, media type
    - `raw_url` to fetch the asset directly
    - optional `file_text` if the file is text-like (JSON, SVG, etc.)
    """
    media_type = guess_media_type(path)
    file_text = read_text_if_possible(path, media_type)

    return {
        "file_name": path.name,
        "file_rel_path": str(path.relative_to(base_dir)),
        "media_type": media_type,
        "raw_url": f"/pm/{origin}?format=raw",
        "file_text": file_text,
    }
