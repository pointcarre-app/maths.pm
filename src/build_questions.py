#!/usr/bin/env python3
"""
Build script to pre-generate questions from all generator files.
Generates 100 questions (seeds 0-99) for each generator and saves as JSON.
"""

import json
import sys
import importlib.util
from pathlib import Path
import traceback
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add the sujets0/generators to path so imports work
sys.path.insert(0, str(Path(__file__).parent / "sujets0" / "generators"))

# Import teachers modules (will be available to all generators)
try:
    import teachers.generator as tg
    import teachers.maths as tm
    from teachers.formatting import Formatting
    from teachers.defaults import SEED
except ImportError:
    print("⚠️ Teachers module not found, generators may fail")
    pass


def load_generator_module(filepath: Path):
    """Dynamically load a generator module from file path"""
    # Create a custom globals dict with missive function
    import builtins

    # Save original builtins
    original_missive = getattr(builtins, "missive", None)

    # Add missive to builtins so it's available everywhere
    builtins.missive = capture_missive

    try:
        spec = importlib.util.spec_from_file_location("generator", filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules["generator"] = module
        spec.loader.exec_module(module)
        return module
    finally:
        # Restore original builtins
        if original_missive is None:
            delattr(builtins, "missive")
        else:
            builtins.missive = original_missive


def capture_missive(*args, **kwargs):
    """Capture missive calls"""
    global last_missive
    last_missive = {"args": args, "kwargs": kwargs}
    # Return the first argument which is usually the data dict
    if args:
        return args[0]
    return kwargs


def generate_question(generator_file: Path, seed: int) -> Dict[str, Any]:
    """Generate a single question from a generator file with given seed

    Always returns a dict - either with question data or error information
    """
    global last_missive
    last_missive = None

    # Capture stdout and stderr
    import io
    import sys
    import random

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Save original seeds
    original_teachers_seed = None

    try:
        # Redirect output
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        # CRITICAL: Set seeds BEFORE loading the module
        # This ensures any module-level randomization uses our seed
        random.seed(seed)

        # Try to set numpy seed if available
        try:
            import numpy as np

            np.random.seed(seed)
        except ImportError:
            pass

        # Override teachers.defaults.SEED if it exists
        try:
            import teachers.defaults

            original_teachers_seed = getattr(teachers.defaults, "SEED", None)
            teachers.defaults.SEED = seed
        except ImportError:
            pass

        # Load the generator module
        module = load_generator_module(generator_file)

        # Force seed into module namespace as well
        if hasattr(module, "SEED"):
            module.SEED = seed

        # Mock the missive function to capture output
        if hasattr(module, "missive"):
            original_missive = module.missive
        module.missive = capture_missive

        # Check if module has required functions
        if not hasattr(module, "generate_components"):
            return {
                "seed": seed,
                "generator": generator_file.stem,
                "success": False,
                "error": f"No generate_components in {generator_file.name}",
                "error_type": "missing_function",
                "stdout": stdout_capture.getvalue(),
                "stderr": stderr_capture.getvalue(),
            }

        # Generate components with specific seed
        components = module.generate_components(None, seed=seed)

        # Solve if available
        answer = None
        if hasattr(module, "solve") and components:
            answer = module.solve(**components)

        # Render question if available
        question = None
        if hasattr(module, "render_question") and components:
            question = module.render_question(**components)

        # Try to call main if it exists (some generators use this pattern)
        if hasattr(module, "main"):
            module.main()

        # Build result from captured missive or from components
        if last_missive and last_missive.get("args"):
            result = last_missive["args"][0] if isinstance(last_missive["args"][0], dict) else {}
        else:
            result = {}

        # Add components and answer if not already in result
        if components and "components" not in result:
            # Convert components to JSON-serializable format
            result["components"] = {}
            for key, value in components.items():
                if hasattr(value, "__dict__"):
                    result["components"][key] = str(value)
                else:
                    result["components"][key] = value

        if answer and "answer" not in result:
            result["answer"] = {}
            if isinstance(answer, dict):
                for key, value in answer.items():
                    if hasattr(value, "latex"):
                        result["answer"][key] = value.latex()
                    elif hasattr(value, "__dict__"):
                        result["answer"][key] = str(value)
                    else:
                        result["answer"][key] = value
            else:
                # Handle non-dict answers
                if hasattr(answer, "latex"):
                    result["answer"] = {"latex": answer.latex()}
                elif hasattr(answer, "__dict__"):
                    result["answer"] = str(answer)
                else:
                    result["answer"] = answer

        if question and "statement" not in result:
            if isinstance(question, dict) and "statement" in question:
                result["statement"] = question["statement"]
            elif isinstance(question, str):
                result["statement"] = question

        # Add metadata
        result["seed"] = seed
        result["generator"] = generator_file.stem
        result["success"] = True
        result["stdout"] = stdout_capture.getvalue()
        result["stderr"] = stderr_capture.getvalue()

        return result

    except Exception as e:
        # Capture full traceback
        tb_str = traceback.format_exc()

        error_result = {
            "seed": seed,
            "generator": generator_file.stem,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": tb_str,
            "stdout": stdout_capture.getvalue(),
            "stderr": stderr_capture.getvalue(),
        }

        # Try to include partial data if available
        if last_missive:
            error_result["partial_missive"] = last_missive

        print(f"  ❌ Error with seed {seed}: {e}")
        return error_result

    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        # Restore original teachers seed if it was modified
        if original_teachers_seed is not None:
            try:
                import teachers.defaults

                teachers.defaults.SEED = original_teachers_seed
            except ImportError:
                pass


def build_all_questions():
    """Build questions for all generators"""
    # Paths
    base_dir = Path(__file__).parent.parent
    generators_dir = base_dir / "src" / "sujets0" / "generators"
    output_dir = base_dir / "src" / "static" / "sujets0" / "questions"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all generator files
    generator_files = []
    for pattern in ["spe_*.py", "gen_*.py"]:
        generator_files.extend(generators_dir.glob(pattern))

    generator_files = sorted(generator_files)

    print(f"📚 Found {len(generator_files)} generator files")
    print(f"📁 Output directory: {output_dir}")
    print("-" * 50)

    # Index to track all generators
    index = {
        "generators": [],
        "total_questions": 0,  # Successful questions only
        "total_attempts": 0,  # All questions including failures
        "total_successful": 0,
        "total_failed": 0,
        "seeds_per_generator": 100,
    }

    # Process each generator
    for generator_file in generator_files:
        generator_name = generator_file.stem
        print(f"\n🔧 Processing {generator_name}...")

        # Create directory for this generator
        generator_output_dir = output_dir / generator_name
        generator_output_dir.mkdir(parents=True, exist_ok=True)

        # Track this generator
        generator_info = {
            "name": generator_name,
            "file": generator_file.name,
            "questions": [],
            "successful": 0,
            "failed": 0,
        }

        # Generate questions with different seeds
        for seed in range(100):
            if seed % 10 == 0:
                print(f"  Generating seeds {seed}-{min(seed + 9, 99)}...")

            result = generate_question(generator_file, seed)

            # Always save the result (success or failure)
            output_file = generator_output_dir / f"{seed}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            # Track success/failure
            if result.get("success", False):
                generator_info["successful"] += 1
                generator_info["questions"].append(seed)
            else:
                generator_info["failed"] += 1
                if "failed_seeds" not in generator_info:
                    generator_info["failed_seeds"] = []
                generator_info["failed_seeds"].append(seed)

        # Save generator metadata
        metadata_file = generator_output_dir / "metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(generator_info, f, ensure_ascii=False, indent=2)

        # Add to index
        index["generators"].append(generator_info)
        index["total_questions"] += generator_info["successful"]
        index["total_successful"] += generator_info["successful"]
        index["total_failed"] += generator_info["failed"]
        index["total_attempts"] += 100  # Always 100 attempts per generator

        print(f"  ✅ Generated {generator_info['successful']} questions")
        if generator_info["failed"] > 0:
            print(f"  ⚠️  Failed: {generator_info['failed']}")

    # Save index
    index_file = output_dir / "index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 50)
    print("✨ Build complete!")
    print(f"📊 Total attempts: {index['total_attempts']}")
    print(f"   ✅ Successful: {index['total_successful']}")
    print(f"   ❌ Failed: {index['total_failed']}")
    print(f"📁 Output location: {output_dir}")

    return index


if __name__ == "__main__":
    # ```bash
    # rm -rf src/static/sujets0/questions/

    # # Run build with seed injection
    # python src/build_questions.py --force-seed-injection

    # # Verify randomization
    # python -c "
    # import json
    # from pathlib import Path
    # # Check if different seeds produce different results
    # for gen in Path('src/static/sujets0/questions').iterdir():
    #     if gen.is_dir():
    #         q0 = json.load(open(gen / '0.json'))
    #         q1 = json.load(open(gen / '1.json'))
    #         if q0.get('statement') == q1.get('statement'):
    #             print(f'⚠️ {gen.name}: No variation detected')
    # "

    import subprocess

    subprocess.run(["rm", "-rf", "src/static/sujets0/questions/"])
    build_all_questions()
    # subprocess.run(["python", "src/build_questions.py", "--force-seed-injection"])
    subprocess.run(
        [
            "python",
            "-c",
            """
import json
from pathlib import Path
for gen in Path('src/static/sujets0/questions').iterdir():
    if gen.is_dir():
        q0 = json.load(open(gen / '0.json'))
        q1 = json.load(open(gen / '1.json'))
        if q0.get('statement') == q1.get('statement'):
            print(f'⚠️ {gen.name}: No variation detected')""",
        ]
    )
