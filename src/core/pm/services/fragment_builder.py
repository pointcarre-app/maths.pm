"""Fragment builder module for creating Fragment objects from HTML elements.

This module provides utilities to convert BeautifulSoup tags into Fragment model instances,
with specialized handling for different types of content.
"""

import html as html_module
import re
from typing import Any

from bs4.element import Tag
import yaml

from src.settings import settings
from ..models.f_type import FType

# from src.core.shared.services.close_watch import close_watch_logger as cw
from ..services.legacy.codex_.py.composer import PythonComposer
from ..services.legacy.codex_.py.parser import PythonParser

# Setup basic logger
# logger = logging.getLogger(__name__)

# Type for h_lvl_counts dictionary
HLvlCounts = dict[str, int]


def slugify(text: str) -> str:
    """Convert text to a URL-friendly format."""
    # Convert to lowercase
    s = text.lower()
    # Replace spaces with hyphens
    s = re.sub(r"\s+", "-", s)
    # Remove non-alphanumeric characters (keeping hyphens)
    s = re.sub(r"[^a-z0-9\-]", "", s)
    # Remove multiple consecutive hyphens
    s = re.sub(r"-+", "-", s)
    # Remove leading/trailing hyphens
    return s.strip("-")


try:
    from markdown.extensions.toc import slugify as slugify_md
except ImportError:
    # If markdown module is not available, use our slugify
    slugify_md = slugify


class FragmentBuilder:
    """Builder class for creating Fragment instances from HTML tags.

    This class provides static methods to convert BeautifulSoup tags into Fragment model
    instances, with specialized handling for different types of content.
    """

    # TODO: should be model_args_from_tag
    @staticmethod
    def from_tag(
        tag: Tag, h_lvl_counts: HLvlCounts, verbosity: int = 0
    ) -> tuple[dict[str, Any], HLvlCounts]:
        """Convert a BeautifulSoup tag to a Fragment dictionary.

        Args:
            tag: BeautifulSoup tag to convert
            h_lvl_counts: Dictionary tracking heading levels for numbering

        Returns:
            Tuple containing:
            - Dictionary with Fragment attributes
            - Updated h_lvl_counts dictionary

        """
        tag_name = tag.name
        html = ""
        data = {}
        f_type = None
        slug = None  # Initialize slug as None by default

        if verbosity > 2:
            print(f"tag_name: {tag_name}")

        # FRAGMENT CLASSES
        class_list = tag.get("class", [])

        ##############################
        # LISTS
        # hence -> i-radio + later i-select
        ##############################
        if tag_name in ["ul", "ol"]:
            html, f_type, data, li_classes = FragmentBuilder.from_list(tag)
            # TODO: careful type
            class_list = class_list + li_classes

        ##############################
        # TITLES
        ##############################
        elif tag_name in ["h1", "h2", "h3", "h4"]:
            f_type, html, data, slug = FragmentBuilder.from_title(tag)

            if tag_name in ["h2", "h3", "h4"]:
                h_lvl_counts[tag_name] += 1

                data["h_lvl_count"] = h_lvl_counts[tag_name]

                if tag_name == "h2":
                    data["h_lvl_count"] = to_roman(data["h_lvl_count"])
                    h_lvl_counts["h3"] = 0
                    h_lvl_counts["h4"] = 0

                elif tag_name == "h3":
                    data["h_lvl_count"] = chr(data["h_lvl_count"] + 64)
                    # reset
                    h_lvl_counts["h4"] = 0

                elif tag_name == "h4":
                    data["h_lvl_count"] = data["h_lvl_count"]
                    # reset

        ##############################
        # PARAGRAPHS
        # hence -> images
        ##############################
        elif tag_name == "p":
            # Inline directive fallback: paragraph containing only directive text
            # Pattern: --- {: .pm-cols-... }
            text_only = tag.get_text(strip=True)
            m_inline = re.match(r"^---\s*\{:\s*([^}]+)\}$", text_only or "")
            if m_inline:
                attrs = m_inline.group(1)
                tokens = [t.strip() for t in re.split(r"\s+", attrs) if t.strip()]
                directive = next(
                    (t.lstrip(".") for t in tokens if t.lstrip(".").startswith("pm-cols-")), None
                )
                if directive:
                    d = re.match(r"^pm-cols-(sm|md|lg)?-?(2|3)$", directive)
                    if d:
                        bp = d.group(1) or "md"
                        cols = int(d.group(2))
                        # Build divider-like fragment with layout metadata
                        f_type, html, data = "hr_", "", {}
                        # classes: all tokens normalized without leading dots
                        class_list = [t.lstrip(".") for t in tokens]
                        # Store layout meta early
                        layout_meta = {
                            "type": "columns",
                            "breakpoint": bp,
                            "columns": cols,
                            "utilities": [
                                t.lstrip(".")
                                for t in tokens
                                if not t.lstrip(".").startswith("pm-cols-")
                            ],
                        }
                        fragment_dict = {
                            "f_type": FType(f_type),
                            "class_list": class_list,
                            "html": html,
                            "data": data,
                            "layout": layout_meta,
                        }
                        return fragment_dict, h_lvl_counts
            # Default paragraph processing
            f_type, html, data = FragmentBuilder.from_paragraph(tag)

        ##############################
        # Blockquotes
        ##############################

        elif tag_name == "blockquote":
            print(class_list)
            f_type, html, data = FragmentBuilder.from_blockquote(tag)

        ##############################
        # DIVIDERS
        ##############################
        elif tag_name == "hr":
            f_type, html, data = FragmentBuilder.from_divider(tag)
            # Detect layout directive from hr classes (attr_list)
            # Class pattern: pm-cols-(sm|md|lg)?-?(2|3)
            classes = tag.get("class", [])
            directive = next((c for c in classes if str(c).startswith("pm-cols-")), None)
            if directive:
                m_dir = re.match(r"^pm-cols-(sm|md|lg)?-?(2|3)$", directive)
                if m_dir:
                    bp = m_dir.group(1) or "md"
                    cols = int(m_dir.group(2))
                    # Keep classes at fragment level for runtime/styles
                    # And add structured layout metadata for early knowledge
                    layout_meta = {
                        "type": "columns",
                        "breakpoint": bp,
                        "columns": cols,
                        "utilities": [c for c in classes if not str(c).startswith("pm-cols-")],
                    }
                else:
                    layout_meta = None
            else:
                layout_meta = None

        ##############################
        # TABLE
        ##############################
        elif tag_name == "table":
            f_type, html, data = FragmentBuilder.from_table(tag)

        ##############################
        # CODE
        ##############################
        elif tag_name == "pre":
            f_type, html, data, class_list = FragmentBuilder.from_code(tag)
            # If language could not be detected in a <code> child (e.g., missing),
            # but this is a math-style example (contains inline math markers),
            # fallback to code_ with plaintext content.
            if f_type == "code_" and (not data or "content" not in data):
                code_tag = tag.find("code")
                fallback = code_tag.decode_contents() if code_tag else tag.decode_contents()
                data = {"content": fallback, "language": "text"}

        ##############################
        # ERRORS for other
        ##############################
        elif tag_name == "div" and ("toc" in class_list):
            f_type, html, data = "toc_", tag.decode_contents(), {}

        else:
            message = f"[NOT IMPLEMENTED] tag:{tag_name} - classes: {tag.get('class')}"
            print(message)
            # Default to paragraph type for unhandled tags
            f_type, html, data = "p_", tag.decode_contents(), {}

        # TODO:hmmm ? model here ?
        fragment_dict = {
            "f_type": FType(f_type),
            "class_list": class_list,
            "html": html,
            "data": data,
        }
        # Attach layout metadata when available
        if tag_name == "hr" and "layout_meta" in locals() and layout_meta is not None:
            fragment_dict["layout"] = layout_meta

        # Add slug if it's present (for headings)
        if slug is not None:
            fragment_dict["slug"] = slug

        return fragment_dict, h_lvl_counts

    @staticmethod
    def from_list(tag: Tag) -> tuple[str, str, dict[str, Any], list[str]]:
        """Convert a list tag (ul/ol) to fragment data.

        Args:
            tag: BeautifulSoup list tag

        Returns:
            Tuple containing:
            - Fragment type string
            - Fragment data dictionary
            - List of CSS classes

        """
        lis = tag.find_all("li")

        html = str(tag)
        data = {}

        # Check for i-radio class on the parent list element (ul/ol)
        list_classes = tag.get("class", [])

        #  WARNING : all on all then... bad
        li_classes = list(set([i for s in lis for i in s.get("class", [])]))

        # Check both list element classes AND li element classes for i-radio
        if "i-radio" in list_classes or "i-radio" in li_classes:
            # li_classes.remove("i-radio")

            data["radios"] = []

            for radio_pos, li in enumerate(lis):
                li_inner = li.decode_contents().strip()
                # Use new parser that supports feedback
                html, flag, classes, feedback = FragmentBuilder.capture_html_flag_feedback(li_inner)

                # assert all classes starts with .
                class_list = (
                    [c.lstrip(".") for c in classes.split(" ") if c.startswith(".")]
                    if classes is not None
                    else []
                )

                if flag is None:
                    flag = -1
                    html = li_inner
                    data["comment"] = li_inner

                else:
                    radio_data = {
                        "pos": radio_pos,
                        "name": slugify(html),
                        "flag": int(flag),
                        "html": html,
                        "classes": " ".join(class_list),
                    }

                    # Add feedback if present
                    if feedback:
                        radio_data["feedback"] = feedback

                    data["radios"].append(radio_data)

            f_type = "radio_"

        elif ("lbl" in li_classes) or ("lbl" in list_classes):
            f_type = "lbl_"
            # Structured label list; support reveal-first-N via attr_list on the list element
            html = ""
            reveal_first = (
                tag.get("data-reveal-first")
                or tag.get("reveal-first")
                or tag.get("data_reveal_first")
            )
            if reveal_first is None:
                # Fallback: allow attribute on first li (authoring convenience)
                for li in lis:
                    reveal_first = (
                        li.get("data-reveal-first")
                        or li.get("reveal-first")
                        or li.get("data_reveal_first")
                    )
                    if reveal_first is not None:
                        break
            try:
                reveal_first = int(reveal_first) if reveal_first is not None else 0
            except Exception:
                reveal_first = 0
            data = {"list": FragmentBuilder.parse_list(tag), "reveal_first": reveal_first}

        # Already sure f_type is ul or ol
        else:
            f_type = f"{tag.name}_"  # ul or ol SI FINE

            # Remove all classes from li tags
            for li in tag.find_all("li"):
                li.attrs = {}

            tag.attrs["class"] = ""

            # print(tag)

            # parse data
            html = str(tag)

        return html, f_type, data, li_classes

    @staticmethod
    def parse_list(list_: Tag) -> list[dict[str, Any]]:
        """Parse a list tag into a nested list structure.

        Args:
            list_: BeautifulSoup list tag

        Returns:
            List of dictionaries representing the nested list structure

        """
        result = []
        for item in list_.find_all(["li", "ul", "ol"], recursive=False):
            sublist = item.find(["ul", "ol"])

            for ul in item.select("ul"):
                ul.extract()

            key = str(item.decode_contents())

            if sublist:
                result.append({key: FragmentBuilder.parse_list(sublist)})
            else:
                result.append({key: None})

        return result

    @staticmethod
    def from_table(table: Tag) -> tuple[str, str, dict[str, Any]]:
        """Convert a table tag to fragment data.

        Args:
            table: BeautifulSoup table tag

        Returns:
            Tuple containing:
            - Fragment type string
            - HTML content (the full table HTML)
            - Table data dictionary with headers and rows

        """
        f_type = "table_"
        # Store the full HTML so it can be rendered directly with | safe
        html = str(table)
        headers, rows = FragmentBuilder.parse_table(table)

        data = {"headers": headers, "rows": rows}
        return f_type, html, data

    @staticmethod
    def parse_table(table: Tag) -> tuple[list[str], list[list[str]]]:
        """Parse a table tag into headers and rows.

        Args:
            table: BeautifulSoup table tag

        Returns:
            Tuple containing:
            - List of header strings
            - List of row lists

        """
        # Check if the provided tag is a table
        assert table.name == "table", "Input is not a <table> tag"

        # Find all the rows in the table
        rows = table.find_all("tr")

        # Check if there are rows in the table
        assert len(rows) > 0, "Table is empty"

        # Extract headers from the first row (if present)
        header_row = rows[0]
        headers = [header.text.strip() for header in header_row.find_all("th")]

        # Extract data rows and convert them to a list of lists
        data = []
        for row in rows[1:]:
            data_row = [cell.decode_contents().strip() for cell in row.find_all(["td", "th"])]
            data.append(data_row)

        return headers, data

    @staticmethod
    def from_paragraph(tag: Tag) -> tuple[str, str, dict[str, Any]]:
        """Convert a paragraph tag to fragment data.

        Args:
            tag: BeautifulSoup paragraph tag

        Returns:
            Tuple containing:
            - Fragment type string
            - HTML content
            - Fragment data dictionary

        """
        # print(tag)
        img = tag.find("img")
        if img is not None:
            src = img.get("src", "").replace("v1", "")
            alt_text = img.get("alt", "")

            # HTML include via image syntax: ![Header](/path/file.html)
            if src.lower().endswith(".html"):
                inc_src = src[1:] if src.startswith("/") else src
                possible_paths = [
                    settings.base_dir / inc_src,
                    settings.static_dir / inc_src.replace("static/", "")
                    if inc_src.startswith("static/")
                    else None,
                ]
                loaded = None
                for path in possible_paths:
                    if path and path.exists() and path.is_file():
                        try:
                            loaded = path.read_text(encoding="utf-8")
                            break
                        except Exception as e:
                            print(f"Error reading HTML file {path}: {e}")
                if loaded:
                    # Try to render Jinja syntax inside included HTML (supports {% include %})
                    try:
                        rendered = settings.templates.env.from_string(loaded).render()
                    except Exception as e:
                        print(f"Error rendering Jinja in included HTML {inc_src}: {e}")
                        rendered = loaded
                    return "html_", alt_text, {"src": src, "content": rendered}

            # Check if this is an SVG image
            if src.lower().endswith(".svg"):
                # For SVG, we need to load the content inline
                svg_content = FragmentBuilder.load_svg_content(src)
                if svg_content:
                    f_type, html, data = (
                        "svg_",
                        alt_text,
                        {"src": src, "content": svg_content},
                    )
                else:
                    # Fallback to regular image if we can't load the SVG
                    f_type, html, data = (
                        "image_",
                        alt_text,
                        {"src": src},
                    )
            else:
                # Regular image handling
                f_type, html, data = (
                    "image_",
                    alt_text,
                    {"src": src},
                )

        # Embedded HTML include via image-like syntax:
        # ![Header](/static/.../file.html)
        elif tag.find("a") is None and tag.find("img") is None:
            # detect single link to .html embedded via markdown image workaround
            content = tag.decode_contents().strip()
            if content.lower().endswith(".html") and not content.startswith("<"):
                # Try to load inline HTML content similar to SVG strategy
                src = content
                if src.startswith("/"):
                    src = src[1:]
                possible_paths = [
                    settings.base_dir / src,
                    settings.static_dir / src.replace("static/", "")
                    if src.startswith("static/")
                    else None,
                ]
                loaded = None
                for path in possible_paths:
                    if path and path.exists() and path.is_file():
                        try:
                            loaded = path.read_text(encoding="utf-8")
                            break
                        except Exception as e:
                            print(f"Error reading HTML file {path}: {e}")
                if loaded:
                    try:
                        rendered = settings.templates.env.from_string(loaded).render()
                    except Exception as e:
                        print(f"Error rendering Jinja in included HTML {src}: {e}")
                        rendered = loaded
                    return "html_", "", {"content": rendered, "src": "/" + src}
            # fallback to plain paragraph if not include-like or not loaded
            f_type, html, data = "p_", tag.decode_contents(), {}
            return f_type, html, data

        # # TODO : non executable codex
        # elif "codex" in tag.get("class", []):
        #     f_type, html, data = "codex_", tag.decode_contents(), {}

        else:
            # get rid of <p> tags but not tags inside
            f_type, html, data = "p_", tag.decode_contents(), {}

        return f_type, html, data

    @staticmethod
    def from_blockquote(tag: Tag) -> tuple[str, str, dict[str, Any]]:
        """Convert a blockquote tag to fragment data.

        Args:
            tag: BeautifulSoup blockquote tag

        Returns:
            Tuple containing:
            - Fragment type string
            - HTML content
            - Fragment data dictionary

        """
        # tag.decode_contents()- > would return a paragraph -> then it fucks up the front
        # todo : distingush html from text ?
        # Are always know it ?
        f_type, html, data = "q_", tag.find("p").decode_contents(), {}
        # print("q_____")
        # print(tag.decode_contents())
        return f_type, html, data

    @staticmethod
    def from_divider(tag: Tag) -> tuple[str, str, dict[str, Any]]:
        """Convert a divider (hr) tag to fragment data.

        Args:
            tag: BeautifulSoup hr tag

        Returns:
            Tuple containing fragment type, empty HTML, and empty data

        """
        return "hr_", "", {}

    @staticmethod
    def from_title(tag: Tag) -> tuple[str, str, dict[str, Any], str]:
        """Convert a heading tag to fragment data.

        Args:
            tag: BeautifulSoup heading tag (h1-h4)

        Returns:
            Tuple containing:
            - Fragment type string
            - HTML content
            - Fragment data dictionary with ID href
            - Slug for the heading

        """
        f_type, html, data = (
            f"{tag.name}_",
            tag.decode_contents().strip(),
            {},
        )
        slug = slugify_md(tag.text, separator="-")
        data = {"id_href": slug}  # Keep for backward compatibility
        return f_type, html, data, slug

    @staticmethod
    def from_code(tag: Tag) -> tuple[str, str, dict[str, Any], list[str]]:
        """Convert a code block (pre) tag to fragment data.

        Args:
            tag: BeautifulSoup pre tag

        Returns:
            Tuple containing:
            - Fragment type string
            - HTML content
            - Fragment data dictionary
            - List of CSS classes

        """
        classes = tag.get("class", [])
        f_type = "code_"
        html = ""
        data = {}

        # Default to Python if no language is specified
        language = "python"

        # Extract language class from code tag
        code_tag = tag.find("code")
        if code_tag and code_tag.get("class"):
            language_class = code_tag.get("class", [None])[0]
            if language_class and "-" in language_class:
                language = language_class.split("-")[1]

        if code_tag:
            code_content = code_tag.decode_contents()

            if language == "yaml":
                try:
                    data = yaml.safe_load(code_content)

                    # Special handling for different YAML content types
                    if "codexPCAVersion" in data:
                        # Simplified codex handling without file access
                        # data["script_path"] = data.get("script_path", "")
                        # MUST BE THERE FOR NOW ?
                        # Or other option: comes from code

                        f_type = "codex_"
                        html = ""
                        data = yaml.safe_load(code_content)
                        script_path = data["script_path"]
                        path = settings.build_codex_path_from_script_path(script_path)
                        with open(path) as file:
                            codex_script = file.read()

                            # print(codex_script)

                            pp = PythonParser()
                            # sections, asts
                            sections, _ = pp.parse(html_module.escape(codex_script))

                            pcomp = PythonComposer()
                            data["composed_script"] = pcomp.compose(
                                foreground_script=sections["foreground_script"],
                                background_script=sections["background_script"],
                                publics_checks=sections["public_checks"],
                                privates_checks=sections["private_checks"],
                            )
                            # data["foreground_script"] = sections["foreground_script"]
                            # data["background_script"] = sections["background_script"]
                            # data["public_checks"] = sections["public_checks"]
                            # data["private_checks"] = sections["private_checks"]
                            # data[""]
                            # from pprint import pprint

                            # pprint(sections)
                            # data["codex_script"] = html_module.escape(codex_script)

                            data |= sections

                    elif ("graphPCAVersion" in data) or ("graph" in classes):
                        f_type = "graph_"
                        html = ""

                    elif ("mathPCAVersion" in data) or "i-maths" in classes:
                        f_type = "maths_"
                        if "i-maths" not in classes:
                            classes.append("i-maths fromhere")

                        # Convert values and handle HTML entities
                        for key, value in data.items():
                            if isinstance(value, int):
                                data[key] = str(value)
                            elif isinstance(value, str):
                                if "&gt;" in value:
                                    value = value.replace("&gt;", ">")
                                if "&lt;" in value:
                                    value = value.replace("&lt;", "<")
                                if "&amp;" in value:
                                    value = value.replace("&amp;", "&")
                                data[key] = value

                    elif "table-variations" in classes:
                        f_type = "tabvar_"
                        html = ""

                    # New: NumberInputPCA YAML block → number_ fragment
                    # Accept both new schema (key: NumberInputPCA -> version string)
                    # and legacy schema (version: NumberInputPCA) for backward compatibility
                    elif ("NumberInputPCA" in data) or (data.get("version") == "NumberInputPCA"):
                        # Normalize: extract version string if provided as key
                        if "NumberInputPCA" in data and "version" not in data:
                            try:
                                data["version"] = str(data["NumberInputPCA"])  # e.g., v0.0.1
                            except Exception:
                                data["version"] = "v0.0.1"
                        f_type = "number_"
                        html = ""
                        # normalize fields (ensure numbers)
                        for k in ["min", "max", "step", "correct", "tolerance"]:
                            if k in data and isinstance(data[k], str):
                                try:
                                    data[k] = float(data[k])
                                except Exception:
                                    pass

                except Exception as e:
                    print(f"Error parsing YAML: {e}")
                    f_type = "code_"
                    data = {"content": code_content, "language": language}

            elif language == "html":
                html_content = code_content
                # Decode HTML entities
                decoded_html_content = html_module.unescape(html_content).strip()

                # TODO: old vg deleted
                if True:
                    f_type = "code_"
                    data = {"content": code_content, "language": language}
            else:
                # Default code handling
                f_type = "code_"
                data = {"content": code_content, "language": language}

        return f_type, html, data, classes

    @staticmethod
    def load_svg_content(src: str) -> str | None:
        """Load SVG content from a file path.

        Args:
            src: The source path from the img tag (e.g. "/static/pm/corsica/files/...")

        Returns:
            The SVG content as a string, or None if the file can't be loaded
        """

        # Convert src path to actual file path
        # Remove leading slash if present
        if src.startswith("/"):
            src = src[1:]

        # Try different path resolutions
        possible_paths = [
            # Direct path from settings base
            settings.base_dir / src,
            # If it starts with 'static/', remove that and look in static_dir
            settings.static_dir / src.replace("static/", "") if src.startswith("static/") else None,
            # Look in pms directory (for relative paths in markdown)
            settings.base_dir / "pms" / src.replace("static/pm/", "")
            if "static/pm/" in src
            else None,
        ]

        for path in possible_paths:
            if path and path.exists() and path.is_file():
                try:
                    return path.read_text(encoding="utf-8")
                except Exception as e:
                    print(f"Error reading SVG file {path}: {e}")

        # If we couldn't find/read the file, return None
        return None

    @staticmethod
    def capture_html_flag_classes(s: str) -> tuple[str | None, str | None, str | None]:
        """Parse an HTML string to extract flag and classes.

        The format is: "content{:flag classes}"

        Args:
            s: String to parse

        Returns:
            Tuple containing:
            - HTML content
            - Flag value
            - CSS classes

        """
        pattern = r"^(.*?){:\s*(\d+)\s*(.*?)\s*}$"
        match = re.search(pattern, s)

        if match:
            return (
                match.group(1).strip(),
                match.group(2),
                match.group(3).strip() or None,
            )
        return None, None, None

    @staticmethod
    def capture_html_flag_feedback(s: str) -> tuple[str | None, str | None, str | None, str | None]:
        """Parse an HTML string to extract flag, classes, and feedback message.

        The format is: "content{:flag | feedback}" or "content{:flag classes | feedback}"

        Args:
            s: String to parse

        Returns:
            Tuple containing:
            - HTML content
            - Flag value
            - CSS classes
            - Feedback message

        """
        # First try with feedback
        pattern_with_feedback = r"^(.*?){:\s*(\d+)\s*([^|]*?)\s*\|\s*(.*?)\s*}$"
        match = re.search(pattern_with_feedback, s)

        if match:
            classes_str = match.group(3).strip()
            # Parse classes (those starting with .)
            class_list = [c.strip() for c in classes_str.split() if c.startswith(".")]
            classes = " ".join(class_list) if class_list else None

            return (
                match.group(1).strip(),  # content
                match.group(2),  # flag
                classes,  # classes
                match.group(4).strip(),  # feedback
            )

        # Fallback to original format without feedback
        html, flag, classes = FragmentBuilder.capture_html_flag_classes(s)
        return html, flag, classes, None


def to_roman(value: int) -> str:
    """Convert integer to Roman numeral.

    Args:
        value: Integer to convert

    Returns:
        Roman numeral string

    """
    roman_map = {
        1000: "M",
        900: "CM",
        500: "D",
        400: "CD",
        100: "C",
        90: "XC",
        50: "L",
        40: "XL",
        10: "X",
        9: "IX",
        5: "V",
        4: "IV",
        1: "I",
    }
    result = ""
    remainder = value

    for i in sorted(roman_map.keys(), reverse=True):
        if remainder > 0:
            multiplier = i
            roman_digit = roman_map[i]

            times = remainder // multiplier
            remainder = remainder % multiplier
            result += roman_digit * times

    return result
