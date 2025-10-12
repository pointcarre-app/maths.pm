import re
import os
import csv
from colors import (
    parse_color_string,
    get_luminance,
    get_contrast_ratio,
    check_wcag_compliance,
    check_rgaa_compliance,
)


def extract_colors_from_css(css_content):
    themes = {}
    current_theme = None

    # Regex to find theme blocks, e.g., [data-theme="anchor"] {
    theme_pattern = re.compile(r'\[data-theme="([a-zA-Z0-9\-]+)"\]\s*\{')
    # Regex to find CSS variables, e.g., --color-base-100: oklch(...);
    color_variable_pattern = re.compile(r"\s*(--[a-zA-Z0-9\-]+):\s*(.*?);.*")

    for line in css_content.splitlines():
        theme_match = theme_pattern.match(line)
        if theme_match:
            current_theme = theme_match.group(1)
            themes[current_theme] = {}
            continue

        if current_theme:
            color_match = color_variable_pattern.match(line)
            if color_match:
                var_name = color_match.group(1)
                var_value = color_match.group(2).strip()
                themes[current_theme][var_name] = var_value
            elif "}" in line:
                current_theme = None

    return themes


def load_contrast_matrix(filepath):
    color_pairs = []
    with open(filepath, "r") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row
        background_vars = header[1:]  # First element is 'Foreground/Background'

        for row in reader:
            fg_var = row[0]
            for i, should_check in enumerate(row[1:]):
                if should_check == "1":
                    bg_var = background_vars[i]
                    color_pairs.append((fg_var, bg_var, f"{fg_var} on {bg_var} Background"))
    return color_pairs


def analyze_theme_contrast(theme_name, colors, color_pairs_to_check):
    print(f"\n--- Analyzing Theme: {theme_name} ---")
    print("=" * 80)

    for fg_var, bg_var, description in color_pairs_to_check:
        fg_color_str = colors.get(fg_var)
        bg_color_str = colors.get(bg_var)

        if not fg_color_str or not bg_color_str:
            print(
                f"  Skipping '{description}': One or both colors not found ({fg_var}: {fg_color_str}, {bg_var}: {bg_color_str})"
            )
            continue

        fg_rgb = parse_color_string(fg_color_str)
        bg_rgb = parse_color_string(bg_color_str)

        if fg_rgb is None or bg_rgb is None:
            print(
                f"  Skipping '{description}': Could not parse one or both colors ({fg_color_str}, {bg_color_str})"
            )
            continue

        fg_lum = get_luminance(fg_rgb)
        bg_lum = get_luminance(bg_rgb)

        if fg_lum is None or bg_lum is None:
            print(
                f"  Skipping '{description}': Could not calculate luminance for one or both colors."
            )
            continue

        contrast_ratio = get_contrast_ratio(fg_lum, bg_lum)
        wcag_compliance = check_wcag_compliance(contrast_ratio)
        rgaa_compliance = check_rgaa_compliance(contrast_ratio)

        print(f"\n  {description}:")
        print(f"    Foreground: {fg_color_str} (RGB: {fg_rgb}, Lum: {fg_lum:.4f})")
        print(f"    Background: {bg_color_str} (RGB: {bg_rgb}, Lum: {bg_lum:.4f})")
        print(f"    Contrast Ratio: {contrast_ratio:.2f}:1")

        print("\n    WCAG 2.1 Compliance:")
        print(f"      AA Large Text (3:1): {'✓' if wcag_compliance['AA_large'] else '✗'}")
        print(f"      AA Normal Text (4.5:1): {'✓' if wcag_compliance['AA_normal'] else '✗'}")
        print(f"      AAA Normal Text (7:1): {'✓' if wcag_compliance['AAA_normal'] else '✗'}")

        print("\n    RGAA 4.0 Compliance (Critère 3.2 - Contraste du texte):")
        print(
            f"      Test 3.2.1 - Texte normal < 24px (4.5:1): {'✓' if rgaa_compliance['text_normal_small'] else '✗'}"
        )
        print(
            f"      Test 3.2.2 - Texte gras < 18.5px (4.5:1): {'✓' if rgaa_compliance['text_bold_small'] else '✗'}"
        )
        print(
            f"      Test 3.2.3 - Texte normal ≥ 24px (3:1): {'✓' if rgaa_compliance['text_normal_large'] else '✗'}"
        )
        print(
            f"      Test 3.2.4 - Texte gras ≥ 18.5px (3:1): {'✓' if rgaa_compliance['text_bold_large'] else '✗'}"
        )

        print("\n    RGAA 4.0 Compliance (Critère 3.3 - Composants d'interface):")
        print(
            f"      Test 3.3.1 - Composants d'interface (3:1): {'✓' if rgaa_compliance['ui_components'] else '✗'}"
        )
        print(
            f"      Test 3.3.2/3.3.3 - Éléments graphiques (3:1): {'✓' if rgaa_compliance['graphics'] else '✗'}"
        )


def main():
    css_file_path = "../../src/static/css/root.css"
    contrast_matrix_path = "contrast_matrix.csv"

    if not os.path.exists(css_file_path):
        print(f"Error: CSS file not found at {css_file_path}")
        return

    if not os.path.exists(contrast_matrix_path):
        print(f"Error: Contrast matrix CSV not found at {contrast_matrix_path}")
        print("Please run generate_contrast_matrix.py first and then populate the CSV.")
        return

    with open(css_file_path, "r") as f:
        css_content = f.read()

    themes = extract_colors_from_css(css_content)
    color_pairs_to_check = load_contrast_matrix(contrast_matrix_path)

    # Define specific themes to check
    themes_to_check = ["anchor"]
    filtered_themes = {name: data for name, data in themes.items() if name in themes_to_check}

    if not filtered_themes:
        print("No matching themes found or parsed from the CSS file.")
        return

    if not color_pairs_to_check:
        print(
            "No color pairs to check in contrast matrix. Please populate contrast_matrix.csv with '1's."
        )
        return

    print("\n" + "=" * 80)
    print("RAPPORT DE CONFORMITÉ RGAA 4.0 & WCAG 2.1 - CONTRASTE DES COULEURS")
    print("=" * 80)

    print("\n📋 RÉFÉRENCE RGAA 4.0 - Critère 3.2:")
    print("   'Dans chaque page web, le contraste entre la couleur du texte")
    print("   et la couleur de son arrière-plan est-il suffisamment élevé'")
    print("\n   Tests requis:")
    print("   • Test 3.2.1: Texte normal < 24px → ratio minimum 4.5:1")
    print("   • Test 3.2.2: Texte gras < 18.5px → ratio minimum 4.5:1")
    print("   • Test 3.2.3: Texte normal ≥ 24px → ratio minimum 3:1")
    print("   • Test 3.2.4: Texte gras ≥ 18.5px → ratio minimum 3:1")

    print("\n📋 RÉFÉRENCE RGAA 4.0 - Critère 3.3:")
    print("   'Les couleurs utilisées dans les composants d'interface ou les éléments")
    print("   graphiques porteurs d'informations sont-elles suffisamment contrastées'")
    print("\n   Tests requis:")
    print("   • Test 3.3.1: Composants d'interface → ratio minimum 3:1")
    print("   • Test 3.3.2: Éléments graphiques → ratio minimum 3:1")
    print("   • Test 3.3.3: Couleurs contiguës d'éléments graphiques → ratio minimum 3:1")

    for theme_name, colors in filtered_themes.items():
        analyze_theme_contrast(theme_name, colors, color_pairs_to_check)

    print("\n" + "=" * 80)
    print("FIN DU RAPPORT")
    print("=" * 80)


if __name__ == "__main__":
    main()
