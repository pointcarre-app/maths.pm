from enum import Enum


class FType(Enum):
    """Fragment types enum."""

    # Text fragments
    TOC = "toc_"
    H1 = "h1_"
    H2 = "h2_"
    H3 = "h3_"
    H4 = "h4_"
    PARAGRAPH = "p_"
    BLOCKQUOTE = "q_"

    # List fragments
    LIST = "ul_"
    NUMBERED_LIST = "ol_"
    LBL = "lbl_"

    # Special content fragments
    TABLE = "table_"
    DIVIDER = "hr_"
    IMAGE = "image_"
    SVG = "svg_"
    HTML = "html_"
    CODE = "code_"
    TABVAR = "tabvar_"

    # Interactive fragments
    RADIO = "radio_"
    MATHS = "maths_"
    GRAPH = "graph_"
    CODEX = "codex_"
    # Number input fragments
    NUMBER = "number_"
