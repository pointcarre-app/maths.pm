# Generator difficulty levels based on COMPETENCES_MAPPING.md analysis
# This maps each generator to its appropriate education level
GENERATOR_LEVELS = {
    # SPE Sujet 1 - All are 2DE level
    "spe_sujet1_auto_01_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_02_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_03_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_04_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_05_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_06_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_07_question": {"level": "1ERE", "note": "inéquation du second degré x² > n"},
    "spe_sujet1_auto_08_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_09_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_10_question": {"level": "1ERE", "note": None},  # polynome
    "spe_sujet1_auto_11_question": {"level": "2DE", "note": None},
    "spe_sujet1_auto_12_question": {"level": "2DE", "note": None},
    # SPE Sujet 2 - Mixed levels
    "spe_sujet2_auto_01_question": {"level": "1ERE", "note": "probabilités conditionnelles"},
    "spe_sujet2_auto_02_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_03_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_04_question": {
        "level": "2DE",
        "note": "utilise compétence 1ERE mais reste accessible",
    },
    "spe_sujet2_auto_05_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_06_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_07_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_08_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_09_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_10_question": {
        "level": "1ERE",
        "note": "signe d'expression factorisée du second degré",
    },
    "spe_sujet2_auto_11_question": {"level": "2DE", "note": None},
    "spe_sujet2_auto_12_question": {"level": "2DE", "note": None},
    # GEN Sujet 1 - Assuming 2DE by default (not explicitly in mapping doc)
    "gen_sujet1_auto_01_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_02_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_03_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_04_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_05_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_06_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_07_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_08_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_09_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_10_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_11_question": {"level": "2DE", "note": None},
    "gen_sujet1_auto_12_question": {"level": "2DE", "note": None},
    # GEN Sujet 2 - Assuming 2DE by default
    "gen_sujet2_auto_01_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_02_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_03_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_04_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_05_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_06_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_07_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_08_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_09_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_10_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_11_question": {"level": "2DE", "note": None},
    "gen_sujet2_auto_12_question": {"level": "2DE", "note": None},
    # GEN Sujet 3 - Assuming 2DE by default
    "gen_sujet3_auto_01_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_02_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_03_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_04_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_05_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_06_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_07_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_08_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_09_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_10_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_11_question": {"level": "2DE", "note": None},
    "gen_sujet3_auto_12_question": {"level": "2DE", "note": None},
}


def get_generator_level_info(generator_name):
    """Get level information for a generator, handling both with and without .py extension."""
    # Remove .py extension if present
    clean_name = generator_name.replace(".py", "") if generator_name else ""
    return GENERATOR_LEVELS.get(clean_name, {"level": "N/A", "note": None})
