import re
import os
import csv


def extract_color_variables(css_content):
    foreground_vars = set()
    background_vars = set()
    all_colors = set()

    color_variable_pattern = re.compile(r"\s*(--[a-zA-Z0-9\-]+):\s*(.*?);.*")

    for line in css_content.splitlines():
        match = color_variable_pattern.match(line)
        if match:
            var_name = match.group(1)
            all_colors.add(var_name)
            if "-content" in var_name:  # Heuristic for foreground colors
                foreground_vars.add(var_name)
            elif "--color-base-" in var_name:  # Heuristic for base backgrounds
                background_vars.add(var_name)
            # Also add general colors like --color-primary to both as they can be fg or bg
            elif var_name not in foreground_vars:  # Avoid adding content colors again
                foreground_vars.add(var_name)
            if var_name not in background_vars:  # Add all to background if not already a base
                background_vars.add(var_name)

    # Refine foreground and background lists to be mutually exclusive where possible, or clearly defined
    # For this matrix, we'll use a broad definition then refine the '1's

    # Ensure specific base backgrounds are in background_vars
    background_vars.add("--color-base-100")
    background_vars.add("--color-base-200")
    background_vars.add("--color-base-300")

    # Ensure specific content colors are in foreground_vars
    content_suffixes = ["content"]
    main_color_prefixes = [
        "primary",
        "secondary",
        "accent",
        "info",
        "success",
        "warning",
        "error",
        "neutral",
    ]

    # Filter out -ghost and -soft variants
    all_colors = {c for c in all_colors if "-ghost" not in c and "-soft" not in c}
    foreground_vars = {c for c in foreground_vars if "-ghost" not in c and "-soft" not in c}
    background_vars = {c for c in background_vars if "-ghost" not in c and "-soft" not in c}

    for color_var in all_colors:
        is_content = any(suffix in color_var for suffix in content_suffixes)
        is_main_color = any(f"--color-{prefix}" in color_var for prefix in main_color_prefixes)

        if is_content:
            foreground_vars.add(color_var)
        elif (
            is_main_color and "-content" not in color_var
        ):  # Main colors (e.g. --color-primary) can be foreground
            foreground_vars.add(color_var)

        # All colors can potentially be backgrounds, but we want to focus on explicit backgrounds
        # for the columns of the matrix

    # Prioritize specific backgrounds for the columns
    explicit_backgrounds = sorted(
        list(
            filter(
                lambda x: "--color-base-" in x
                or any(f"--color-{p}" in x and "-content" not in x for p in main_color_prefixes),
                background_vars,
            )
        )
    )

    # Prioritize specific foregrounds for the rows
    explicit_foregrounds = [
        "--color-accent",
        "--color-accent-content",
        "--color-base-content",
        "--color-error",
        "--color-error-content",
        "--color-info",
        "--color-info-content",
        "--color-neutral",
        "--color-neutral-content",
        "--color-primary",
        "--color-primary-content",
        "--color-secondary",
        "--color-secondary-content",
        "--color-success",
        "--color-success-content",
        "--color-warning",
        "--color-warning-content",
    ]

    # Ensure only these explicitly listed foregrounds are considered
    explicit_foregrounds = sorted([f for f in explicit_foregrounds if f in foreground_vars])

    return explicit_foregrounds, explicit_backgrounds


def generate_adjacency_matrix(foreground_vars, background_vars):
    matrix = {}  # {(fg, bg): 0/1}

    # Initialize matrix with 0s for all combinations
    for fg in foreground_vars:
        for bg in background_vars:
            matrix[(fg, bg)] = 0

    # Rule 1: -content colors against their corresponding main color
    # This is important for RGAA 3.3.1 (UI components)
    for fg in foreground_vars:
        if "-content" in fg:
            main_color_name = fg.replace("-content", "")
            # Ensure the main_color_name is a valid background variable
            if main_color_name in background_vars:
                if (fg, main_color_name) in matrix:
                    matrix[(fg, main_color_name)] = 1

    # Rule 2: Specific foreground colors against specific base backgrounds
    # This covers RGAA 3.2 (text contrast) requirements
    specific_foregrounds = [
        "--color-accent",
        "--color-primary",
        "--color-secondary",
        "--color-base-content",
    ]
    specific_backgrounds = [
        "--color-base-100",
        "--color-base-200",
        "--color-base-300",
    ]

    for fg in specific_foregrounds:
        if fg in foreground_vars:
            for bg in specific_backgrounds:
                if bg in background_vars:
                    if (fg, bg) in matrix:
                        matrix[(fg, bg)] = 1

    # Rule 3: UI component colors against base backgrounds
    # For RGAA 3.3 compliance (UI components need 3:1 ratio)
    ui_component_colors = [
        "--color-error",
        "--color-warning",
        "--color-success",
        "--color-info",
        "--color-neutral",
    ]

    for ui_color in ui_component_colors:
        if ui_color in foreground_vars:
            for bg in specific_backgrounds:
                if bg in background_vars:
                    if (ui_color, bg) in matrix:
                        matrix[(ui_color, bg)] = 1

    return matrix


def write_matrix_to_csv(foreground_vars, background_vars, matrix, output_filepath):
    with open(output_filepath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header row with RGAA context
        header = ["Foreground/Background"] + background_vars
        writer.writerow(header)

        # Add a comment row explaining the purpose
        comment = ["# RGAA 4.0 Compliance Matrix"] + [""] * len(background_vars)
        writer.writerow(comment)

        # Write data rows
        for fg in foreground_vars:
            row = [fg]
            for bg in background_vars:
                row.append(matrix.get((fg, bg), 0))  # Default to 0 if not explicitly set
            writer.writerow(row)


def main():
    css_file_path = "/Users/selim/madles/pca-mathspm/src/static/css/root.css"
    output_csv_path = "/Users/selim/madles/pca-mathspm/contrast_matrix.csv"

    if not os.path.exists(css_file_path):
        print(f"Error: CSS file not found at {css_file_path}")
        return

    with open(css_file_path, "r") as f:
        css_content = f.read()

    print("\n" + "=" * 80)
    print("GÉNÉRATEUR DE MATRICE DE CONTRASTE - CONFORMITÉ RGAA 4.0")
    print("=" * 80)
    print("\nCe générateur crée une matrice de vérification pour:")
    print("  • RGAA 4.0 Critère 3.2: Contraste du texte")
    print("  • RGAA 4.0 Critère 3.3: Contraste des composants d'interface")
    print("\nExtraction des variables de couleur...")

    foreground_vars, background_vars = extract_color_variables(css_content)

    print(f"  • Variables de premier plan trouvées: {len(foreground_vars)}")
    print(f"  • Variables d'arrière-plan trouvées: {len(background_vars)}")

    print("\nGénération de la matrice d'adjacence...")
    matrix = generate_adjacency_matrix(foreground_vars, background_vars)

    # Count active checks
    active_checks = sum(1 for v in matrix.values() if v == 1)
    print(f"  • Nombre de combinaisons à vérifier: {active_checks}")

    print("\nÉcriture de la matrice CSV...")
    write_matrix_to_csv(foreground_vars, background_vars, matrix, output_csv_path)

    print("\n✓ Matrice de contraste générée et sauvegardée dans:")
    print(f"  {output_csv_path}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
