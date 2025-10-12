import re
import math
from colour.models import Oklab_to_XYZ
from colour.models.rgb import XYZ_to_sRGB


def oklch_to_rgb(l, c, h):
    # Convert L from percentage to [0, 1]
    L_ok = l / 100.0

    # Convert C and H to Oklab a and b components
    h_rad = math.radians(h)
    a_ok = c * math.cos(h_rad)
    b_ok = c * math.sin(h_rad)

    # Convert Oklab (L, a, b) to XYZ
    XYZ = Oklab_to_XYZ([L_ok, a_ok, b_ok])

    # Convert XYZ to sRGB
    # XYZ_to_sRGB expects normalized XYZ values (0-1)
    rgb_linear = XYZ_to_sRGB(XYZ)

    # Convert linear sRGB to sRGB 0-255 values, clamping to [0, 255]
    r_255 = int(max(0, min(255, round(rgb_linear[0] * 255))))
    g_255 = int(max(0, min(255, round(rgb_linear[1] * 255))))
    b_255 = int(max(0, min(255, round(rgb_linear[2] * 255))))

    return (r_255, g_255, b_255)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])
    if len(hex_color) == 6:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return None


def parse_color_string(color_string):
    color_string = color_string.strip()
    if color_string.startswith("oklch"):
        match = re.match(r"oklch\((\d+\.?\d*)%\s*(\d+\.?\d*)\s*(\d+\.?\d*)(deg)?\)", color_string)
        if match:
            l = float(match.group(1))
            c = float(match.group(2))
            h = float(match.group(3))
            return oklch_to_rgb(l, c, h)
        print(f"Warning: Could not parse OKLCH color: {color_string}")
        return None
    elif color_string.startswith("#"):
        return hex_to_rgb(color_string)
    elif color_string.startswith("rgb"):
        match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color_string)
        if match:
            return int(match.group(1)), int(match.group(2)), int(match.group(3))
    elif color_string.lower() == "red":
        return (255, 0, 0)
    elif color_string.lower() == "white":
        return (255, 255, 255)
    elif color_string.lower() == "black":
        return (0, 0, 0)

    if "color-mix" in color_string:
        print(f"Warning: Skipping color-mix function: {color_string}")
        return None

    print(f"Warning: Could not parse color string: {color_string}")
    return None


def get_luminance(rgb_color):
    if rgb_color is None:
        return None
    r, g, b = [x / 255.0 for x in rgb_color]

    def to_linear(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    R_linear = to_linear(r)
    G_linear = to_linear(g)
    B_linear = to_linear(b)

    luminance = (0.2126 * R_linear) + (0.7152 * G_linear) + (0.0722 * B_linear)
    return luminance


def get_contrast_ratio(lum1, lum2):
    if lum1 is None or lum2 is None:
        return None
    if lum1 < lum2:
        lum1, lum2 = lum2, lum1

    return (lum1 + 0.05) / (lum2 + 0.05)


def check_wcag_compliance(contrast_ratio):
    if contrast_ratio is None:
        return {"AA_large": False, "AA_normal": False, "AAA_normal": False}

    compliance = {}
    compliance["AA_large"] = contrast_ratio >= 3.0
    compliance["AA_normal"] = contrast_ratio >= 4.5
    compliance["AAA_normal"] = contrast_ratio >= 7.0
    return compliance


def check_rgaa_compliance(contrast_ratio):
    """
    Check RGAA 4.0 compliance for contrast ratios.

    According to RGAA 4.0 Critère 3.2:
    - Test 3.2.1: Normal text < 24px needs 4.5:1
    - Test 3.2.2: Bold text < 18.5px needs 4.5:1
    - Test 3.2.3: Normal text >= 24px needs 3:1
    - Test 3.2.4: Bold text >= 18.5px needs 3:1

    Critère 3.3 for UI components:
    - Test 3.3.1-3.3.3: UI components and graphics need 3:1
    """
    if contrast_ratio is None:
        return {
            "text_normal_small": False,  # < 24px
            "text_bold_small": False,  # < 18.5px
            "text_normal_large": False,  # >= 24px
            "text_bold_large": False,  # >= 18.5px
            "ui_components": False,  # UI elements
            "graphics": False,  # Graphical elements
        }

    compliance = {}

    # Text compliance (Critère 3.2)
    # Small text needs 4.5:1
    compliance["text_normal_small"] = contrast_ratio >= 4.5  # Test 3.2.1
    compliance["text_bold_small"] = contrast_ratio >= 4.5  # Test 3.2.2

    # Large text needs 3:1
    compliance["text_normal_large"] = contrast_ratio >= 3.0  # Test 3.2.3
    compliance["text_bold_large"] = contrast_ratio >= 3.0  # Test 3.2.4

    # UI components and graphics (Critère 3.3)
    compliance["ui_components"] = contrast_ratio >= 3.0  # Test 3.3.1
    compliance["graphics"] = contrast_ratio >= 3.0  # Test 3.3.2 & 3.3.3

    return compliance
