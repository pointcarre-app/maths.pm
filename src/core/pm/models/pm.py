from typing import Any

from pydantic import BaseModel, field_validator
from .fragment import Fragment


class PM(BaseModel):
    """"""

    # Block belonging
    origin: str
    origin_fn: str
    class_at_school: str | None = None
    theme: str | None = None
    theme_rdb: str | None = None
    chapter: str | None = None
    chapter_rdb: str | None = None

    # Block parameters
    mode: str | None = None
    b_type: str | None = None
    needs_pen: bool | None = None
    metadata: dict[str, Any]

    # Block details
    toc: dict[str, Any]
    title: str
    science: dict[str, Any]
    interaction_count: int
    answerable_interaction_count: int

    checked_by_mad: bool | None = None
    checked_by_sel: bool | None = None

    # Fragments - list of Fragment objects (converted from dicts if needed)
    fragments: list[Fragment]

    # Optional fields
    html_content: str | None = None
    without_fragments: bool = False

    # Dynamic dependencies from metadata
    js_dependencies: list[str] | None = None
    css_dependencies: list[str] | None = None

    @field_validator("fragments", mode="before")
    def convert_fragments(cls, v):
        """Convert fragment dictionaries to Fragment instances."""
        if not isinstance(v, list):
            return v

        result = []
        for item in v:
            if isinstance(item, dict):
                # Convert dict to Fragment instance
                try:
                    fragment = Fragment(**item)
                    result.append(fragment)
                except Exception as e:
                    # If conversion fails, keep as dict
                    print(f"Warning: Could not convert fragment dict to Fragment: {e}")
                    result.append(item)
            else:
                # Already a Fragment instance or something else
                result.append(item)
        return result

    # class Config:
    #     from_attributes = True  # Allows conversion from ORM objects
