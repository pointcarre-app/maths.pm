"""Fragment module for representing and validating document fragments.

This module provides the Fragment model for representing different types of content
fragments in a document, with validation specific to each fragment type.
"""

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator, computed_field

# Use our local FType enum instead of importing from app
from .f_type import FType


class Fragment(BaseModel):
    """Fragment model representing a content element in a document.

    A Fragment is a discrete piece of content (text, heading, list, etc.) with
    validation rules specific to its type. The type determines the expected structure
    and content of the fragment.
    """

    f_type: FType = Field(
        description="The type of fragment, determines validation rules and rendering"
    )
    interaction_pos: int | None = Field(
        default=None, description="Position of this fragment among all interactive fragments"
    )
    answerable_interaction_pos: int | None = Field(
        default=None, description="Position of this fragment among answerable interactive fragments"
    )
    class_list: list[str] = Field(
        default_factory=list, description="List of CSS classes to apply to this fragment"
    )
    slug: str | None = Field(
        default=None, description="URL-safe slug generated from heading text for anchor links"
    )

    @computed_field  # type: ignore[misc]
    @property
    def classes(self) -> str:
        """Compute space-separated string of CSS classes from class_list."""
        return " ".join(self.class_list) if self.class_list else ""

    html: str = Field(
        default="", description="HTML content of the fragment, may be empty depending on type"
    )
    data: dict[str, Any] = Field(
        default_factory=dict, description="Additional data specific to the fragment type"
    )

    # Optional layout directive metadata (e.g., columns grouping)
    # When present, it typically appears on divider (hr_) fragments created from
    # hr with attribute list or inline directive paragraphs.
    layout: dict[str, Any] | None = Field(
        default=None,
        description="Layout directive metadata (e.g., {'type': 'columns', 'breakpoint': 'md', 'columns': 2, 'utilities': [...]})",
    )

    class Config:
        validate_assignment = True
        # Because of enums
        arbitrary_types_allowed = True

    @field_validator("html")
    def validate_html(cls, v: Any) -> str:
        """Validate that the HTML content is a string.

        Args:
            v: The value to validate

        Returns:
            The validated string

        Raises:
            ValueError: If the value is not a string

        """
        if not isinstance(v, str):
            raise ValueError(f"HTML must be a string, got {type(v)}")
        return v

    @field_validator("class_list")
    def validate_class_list(cls, v: Any) -> list[str]:
        """Validate that class_list is a list.

        Args:
            v: The value to validate

        Returns:
            The validated list

        Raises:
            ValueError: If the value is not a list

        """
        if not isinstance(v, list):
            raise ValueError(f"class_list must be a list, got {type(v)}")
        return v

    @field_validator("data")
    def validate_data(cls, v: Any) -> dict[str, Any]:
        """Validate that data is a dictionary.

        Args:
            v: The value to validate

        Returns:
            The validated dictionary

        Raises:
            ValueError: If the value is not a dictionary

        """
        if not isinstance(v, dict):
            raise ValueError(f"data must be a dict, got {type(v)}")
        return v

    @model_validator(mode="before")
    def validate_by_type(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate fragment fields based on the fragment type.

        Different fragment types have different validation rules for their content.
        This validator ensures that the fragment data matches the expected structure
        for its type.

        Args:
            values: The values to validate

        Returns:
            The validated values

        Raises:
            ValueError: If the values don't match the expected structure for the fragment type

        """
        f_type = values.get("f_type")
        html = values.get("html", "")
        data = values.get("data", {})

        if f_type in [FType.TOC, FType.PARAGRAPH, FType.BLOCKQUOTE]:
            if len(data) != 0:
                raise ValueError(f"Text type {f_type} should have empty data")

        elif f_type in [FType.H1, FType.H2, FType.H3, FType.H4]:
            if len(data) not in [1, 2]:
                raise ValueError(f"Title type {f_type} should have 1 or 2 data items")

        elif f_type in [FType.LIST, FType.NUMBERED_LIST, FType.LBL]:
            # Accept either structured lists (data['list']) or raw HTML lists
            # produced upstream (html contains <ul>/<ol> and data is empty).
            is_structured_list = bool(data) and list(data.keys())[0] == "list" and html == ""
            is_raw_html_list = html != "" and data == {}
            if not (is_structured_list or is_raw_html_list):
                raise ValueError(
                    f"List type {f_type} must be either structured with data['list'] and empty html, "
                    f"or raw HTML with non-empty html and empty data"
                )

        elif f_type == FType.TABLE:
            # Tables can have either:
            # 1. HTML content (from markdown tables) - for direct rendering
            # 2. Structured data (headers and rows) - for programmatic generation
            if html:
                # If HTML is provided, we don't need structured data validation
                pass
            else:
                # If no HTML, we need proper structured data
                if set(data.keys()) != {"headers", "rows"}:
                    raise ValueError("Table without HTML should have 'headers' and 'rows' keys")
                if not isinstance(data.get("headers"), list):
                    raise ValueError("Table headers must be a list")
                if not isinstance(data.get("rows"), list) or (
                    data.get("rows") and not isinstance(data.get("rows")[0], list)
                ):
                    raise ValueError("Table rows must be a list of lists")

        elif f_type == FType.DIVIDER:
            # Allow optional layout metadata on divider; html and data must remain empty
            if html != "" or data != {}:
                raise ValueError("Divider should have empty html and empty data")

        elif f_type == FType.IMAGE:
            if set(data.keys()) != {"src"}:
                raise ValueError("Image should have 'src' key in data")

        elif f_type == FType.SVG:
            if not ({"src", "content"} == set(data.keys())):
                raise ValueError("SVG should have 'src' and 'content' keys in data")

        elif f_type == FType.CODE:
            if set(data.keys()) != {"content", "language"}:
                raise ValueError("Code should have 'content' and 'language' keys in data")

        elif f_type == FType.RADIO:
            radio_keys_ok = True
            if not (set(data.keys()) == {"radios"} or set(data.keys()) == {"radios", "comment"}):
                radio_keys_ok = False

            # Required keys for all radio items
            required_radio_keys = {"name", "flag", "html", "classes", "pos"}
            # Optional keys that may be present
            optional_radio_keys = {"feedback"}
            allowed_radio_keys = required_radio_keys | optional_radio_keys

            if "radios" in data:
                for radio in data["radios"]:
                    radio_keys = set(radio.keys())
                    # Check that all required keys are present
                    if not required_radio_keys.issubset(radio_keys):
                        radio_keys_ok = False
                        break
                    # Check that no unexpected keys are present
                    if not radio_keys.issubset(allowed_radio_keys):
                        radio_keys_ok = False
                        break

            if not radio_keys_ok:
                raise ValueError("Radio validation failed")

        elif f_type == FType.MATHS:
            if html != "":
                raise ValueError("Math should have empty html")
            # MATHS fragments can have various data structures depending on the source
            # Don't enforce strict key requirements as they vary based on usage

        elif f_type == FType.GRAPH:
            if html != "":
                raise ValueError("Graph should have empty html")

        elif f_type == FType.SCRIPT_MODULE:
            if html != "":
                raise ValueError("SCRIPT_MODULE should have empty html")
            # Either content (inline) or src (file reference) is required
            content_keys = {"content"}
            file_keys = {"src"}
            optional_keys = {"type", "version", "fType"}
            allowed_keys = content_keys | file_keys | optional_keys

            # Must have either content OR src, but not both
            has_content = content_keys.issubset(set(data.keys()))
            has_src = file_keys.issubset(set(data.keys()))

            if not (has_content or has_src):
                raise ValueError("SCRIPT_MODULE requires either 'content' or 'src' key in data")
            if has_content and has_src:
                raise ValueError("SCRIPT_MODULE cannot have both 'content' and 'src' keys")
            if not set(data.keys()).issubset(allowed_keys):
                extra_keys = set(data.keys()) - allowed_keys
                raise ValueError(f"SCRIPT_MODULE has unexpected keys: {extra_keys}")

        return values

    def to_dict(self) -> dict[str, Any]:
        """Convert the Fragment to a dictionary representation.

        Transforms the f_type enum value to its string value for compatibility
        with serialization formats that don't support enums. Also includes the
        computed classes field.

        Returns:
            Dict[str, Any]: Dictionary representation of the Fragment

        """
        result = self.dict()
        result["f_type"] = self.f_type.value
        # The computed field 'classes' should already be included by .dict()
        # but let's make sure it's there
        result["classes"] = self.classes
        return result

    @classmethod
    def from_tag(cls, tag, h_lvl_counts) -> tuple["Fragment", dict[str, int]]:
        """Create a Fragment from a BeautifulSoup tag.

        Args:
            tag: BeautifulSoup tag to convert to a Fragment
            h_lvl_counts: Dictionary of heading level counts for maintaining heading numbering

        Returns:
            Tuple containing:
            - The created Fragment instance
            - Updated h_lvl_counts dictionary

        """
        # from app.services.v1.fragment.builder import FragmentBuilder
        from core.pm.services.fragment_builder import FragmentBuilder

        fragment_dict, h_lvl_counts = FragmentBuilder.from_tag(tag=tag, h_lvl_counts=h_lvl_counts)
        return cls(**fragment_dict), h_lvl_counts


def has_flag_from_radio(fragment: Fragment, flag_values: list) -> bool:
    """Check if a Fragment has any radio options with flags from the given list.

    Args:
        fragment: Fragment object to check for flags
        flag_values: List of flag values to check for

    Returns:
        True if any radio option in the fragment has a flag in the flag_values list,
        False otherwise

    """
    radios = fragment.data.get("radios", [])
    for radio in radios:
        if radio.get("flag") in flag_values:
            return True
    return False
