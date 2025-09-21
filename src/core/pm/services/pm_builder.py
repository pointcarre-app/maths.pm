from typing import Any

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import markdown
from markdown.extensions.tables import TableExtension


from ..models.pm import PM
# from src.core.shared.models.block import Block

from ..external.full_yaml_metadata_extension import FullYamlMetadataExtension

from .fragment_builder import FragmentBuilder
# from src.core.shared.services.block.md_full_metadata import FullYamlMetadataExtension

# from src.core.shared.services.close_watch import close_watch_logger as cw
# from src.core.shared.services.fragment.builder import FragmentBuilder


class PMBuilder:
    """Service for building PM models from markdown content."""

    MD_EXTENSIONS = [
        "toc",
        TableExtension(use_align_attribute=True),
        "fenced_code",
        "abbr",
        "attr_list",
        FullYamlMetadataExtension(),
        # We'll need to implement a new metadata extension for Pydantic
        # "full_yaml_metadata",
    ]

    @staticmethod
    def from_markdown(md_content: str, origin: str, verbosity: int = 0) -> PM:
        """Create a Block model from markdown content."""
        if verbosity > 1:
            # print(f"Building block from {origin}")
            # TODO: better
            print(f"Building block from {origin}")

        html_content, metadata = PMBuilder._markdown_to_html(md_content)
        soup = PMBuilder._html_to_soup(html_content)
        first_lvl_tags = list(soup.children)

        fragments, special_fragments, interaction_count, answerable_count = PMBuilder._process_tags(
            first_lvl_tags, verbosity
        )

        # Get title from first fragment or fallback to origin
        title = fragments[0].get("html") if fragments else origin

        # Clean up origin path
        origin = origin.replace("../markdowns/", "").rstrip(".md")
        origin_parts = origin.split("/")
        origin_fn = origin_parts[-1]

        # print(f"origin_fn: {origin_fn}")
        # print(f"origin_parts: {origin_parts}")

        # Extract class and chapter info
        # Now prefer metadata; fall back to None if missing
        class_at_school = metadata.get("class_at_school")
        chapter = metadata.get("chapter")

        # Build the Block model
        block_data = {
            "origin": origin,
            "origin_fn": origin_fn,
            "class_at_school": class_at_school,
            "theme": metadata.get("theme"),
            "theme_rdb": metadata.get("theme_rdb"),
            "chapter": chapter,
            "chapter_rdb": metadata.get("chapter_rdb"),
            # PMBuilder._get_chapter_rdb(chapter, class_at_school),
            "mode": metadata.get("mode"),
            "b_type": PMBuilder._determine_block_type(origin_fn),
            "needs_pen": metadata.get("needs_pen"),
            "toc": special_fragments.get("toc", {}),
            "title": title,
            "metadata": metadata,
            "science": metadata.get("science", {}),
            "fragments": fragments,
            "html_content": html_content,
            "interaction_count": interaction_count,
            "answerable_interaction_count": answerable_count,
            "checked_by_mad": bool(metadata.get("checked_by_mad", 0))
            if "checked_by_mad" in metadata
            else None,
            "checked_by_sel": bool(metadata.get("checked_by_sel", 0))
            if "checked_by_sel" in metadata
            else None,
            "without_fragments": False,
            # Extract dependencies from metadata
            "js_dependencies": metadata.get("js_dependencies"),
            "css_dependencies": metadata.get("css_dependencies"),
        }

        if verbosity > 0:
            print(f"🟣 {origin_fn}")
            print(f"\t{block_data['chapter']}: {block_data['class_at_school']}")
            print(f"\t{block_data['mode']} mode")
            print(f"\t{block_data['b_type']} block type")
            print(f"\t{block_data['interaction_count']} interactions")
            print(f"\t{block_data['answerable_interaction_count']} answerable interactions")
            print(f"\t{block_data['checked_by_mad']} checked by mad")
            print(f"\t{block_data['checked_by_sel']} checked by sel")
            print(f"\t{block_data['needs_pen']} needs pen")

            print(f"{block_data['html_content']}")

        if verbosity > 0:
            # Summarize all fragment ftypes counts
            ftype_counts = {}
            for fragment in fragments:
                f_type = str(fragment.get("f_type", "unknown"))
                if f_type in ftype_counts:
                    ftype_counts[f_type] += 1
                else:
                    ftype_counts[f_type] = 1
            for f_type, count in sorted(ftype_counts.items()):
                print(f"\t{f_type}: {count}")

        # Add fragment type counts to block data

        return PM(**block_data)

    @staticmethod
    def _markdown_to_html(md_content: str) -> tuple[str, dict[str, Any]]:
        """Convert markdown to HTML and extracts metadata."""
        md = markdown.Markdown(extensions=PMBuilder.MD_EXTENSIONS)
        html_content = md.convert(md_content)
        # We'll need to implement proper metadata extraction
        metadata = getattr(md, "Meta", {}) or {}
        return html_content, metadata

    @staticmethod
    def _html_to_soup(html_content: str) -> BeautifulSoup:
        """Convert HTML string to BeautifulSoup object."""
        return BeautifulSoup(html_content, "html.parser")

    @staticmethod
    def _process_tags(
        tags: list[Any], verbosity: int = 0
    ) -> tuple[list[dict[str, Any]], dict[str, Any], int, int]:
        """Process HTML tags to extract fragments and counts."""
        fragments = []
        special_fragments = {}
        interaction_count = 0
        answerable_count = 0

        # TODO : add in block validation
        # same way fragments are validated
        h_lvl_counts = {"h2": 0, "h3": 0, "h4": 0}

        if verbosity > 2:
            print(f"Processing {len(tags)} tags")

        for tag in tags:
            if isinstance(tag, NavigableString):
                continue
            if not isinstance(tag, Tag):
                continue

            # Process the tag and create fragment
            # This is a simplified version - you'll need to implement the full fragment processing logic
            fragment, h_lvl_counts = PMBuilder._create_fragment(
                tag, h_lvl_counts, verbosity=verbosity
            )

            if verbosity > 2:
                print(
                    f"h_lvl_counts: 2:{h_lvl_counts['h2']} 3:{h_lvl_counts['h3']} 4:{h_lvl_counts['h4']}"
                )

            if fragment.get("f_type").value == "toc_":
                special_fragments["toc"] = fragment
            else:
                fragments.append(fragment)

            # Update counts based on fragment type
            if fragment.get("f_type") in ["radio", "maths"]:
                interaction_count += 1
                if fragment.get("answerable", False):
                    answerable_count += 1

        return fragments, special_fragments, interaction_count, answerable_count

    @staticmethod
    def _create_fragment(
        tag: Tag, h_lvl_counts: dict[str, int], verbosity: int = 0
    ) -> tuple[dict[str, Any], dict[str, int]]:
        """Create a fragment dictionary from a tag."""
        fragment_dict, h_lvl_counts = FragmentBuilder.from_tag(
            tag=tag, h_lvl_counts=h_lvl_counts, verbosity=verbosity
        )
        return fragment_dict, h_lvl_counts

    @staticmethod
    def _get_theme(chapter: str, class_at_school: str) -> str:
        """Get theme for chapter."""
        # Implement theme lookup logic
        return f"theme_{chapter}"

    @staticmethod
    def _get_theme_rdb(chapter: str, class_at_school: str) -> str:
        """Get theme RDB for chapter."""
        # Implement theme RDB lookup logic
        return f"theme_rdb_{chapter}"

    @staticmethod
    def _get_chapter_rdb(chapter: str, class_at_school: str) -> str:
        """Get chapter RDB."""
        # Implement chapter RDB lookup logic
        return f"chapter_rdb_{chapter}"

    @staticmethod
    def _determine_block_type(origin_fn: str) -> str:
        """Determine block type from filename."""
        # Implement block type determination logic
        return "default"
