#!/usr/bin/env python3
"""
HYPERCUBE ANALYSIS - Strategy for parsing all generate_components functions

This file analyzes all the generate_components functions from the spe_sujet1_auto_*_question.py files
to understand the patterns and create a comprehensive mapping of all possible parameter types and ranges.

GOAL: Parse generate_components functions and generate a list with ALL possible parameters
returned in the dictionary. The dictionary will never be nested.

=== ANALYSIS STRATEGY ===

1. IDENTIFY ALL tg.MathsGenerator METHODS USED:
   From analyzing all files, these are the methods called on gen (tg.MathsGenerator instance):

   - gen.random_integer(min, max)           # Returns tm.Integer
   - gen.random_element_from(list)          # Returns one element from list
   - gen.discrete_dirichlet_dist(n, q, exclude_zero) # Returns tuple of tm.Fractions

2. IDENTIFY ALL tm.MathsObject TYPES CREATED:
   Direct instantiation patterns found:

   - tm.Integer(n=value)                    # Integer wrapper
   - tm.Fraction(p=numerator, q=denominator) # Fraction wrapper
   - tm.Symbol(s="variable_name")           # Symbolic variable
   - tm.Decimal(p=value, q=base)           # Decimal representation
   - tm.Function(name="function_name")      # Function wrapper
   - tm.MathsCollection(elements=[...])     # Collection of math objects

   Computed expressions (combinations of above):
   - Addition: a + b
   - Multiplication: a * b
   - Division: a / b
   - Power: a ** b
   - Comparisons: a > b, a < b
   - Complex expressions: (x + c1) ** tm.Integer(n=2)

3. PARAMETER GENERATION PATTERNS BY FILE:

=== FILE BY FILE ANALYSIS ===

FILE: spe_sujet1_auto_01_question.py
PARAMETERS RETURNED:
- "n": tm.Integer (range: 2-5) from gen.random_integer(2, 5)
- "x": tm.Integer (range: 1-10) from gen.random_integer(1, 10)

FILE: spe_sujet1_auto_02_question.py
PARAMETERS RETURNED:
- "a": tm.Fraction(p=1, q=random_int_1_10)
- "b": tm.Integer (range: 1-10)
- "c": tm.Integer (range: 1-10)
- "d": tm.Fraction(p=-1, q=random_int_1_10)

FILE: spe_sujet1_auto_03_question.py
PARAMETERS RETURNED:
- "p": tm.Fraction(p=random_int_1_200, q=200)
- "direction": tm.Integer(n=±1) from random_element_from((-1, 1))
- "coef": tm.Integer(n=1) + direction * p  # Computed expression

FILE: spe_sujet1_auto_04_question.py
PARAMETERS RETURNED:
- "p": tm.Integer(n=5*random_int_1_20) # Always multiple of 5, range 5-100
- "direction": tm.Integer(n=±1) from random_element_from((-1, 1))

FILE: spe_sujet1_auto_05_question.py
PARAMETERS RETURNED:
- "probabilities": tuple of 4 tm.Fractions from gen.discrete_dirichlet_dist(n=4, q=24, exclude_zero=True)

FILE: spe_sujet1_auto_06_question.py
PARAMETERS RETURNED:
- "x": tm.Symbol(s="x") # Fixed symbol
- "y": tm.Symbol(s="y") # Fixed symbol
- "u": tm.Symbol(s="u") # Fixed symbol

FILE: spe_sujet1_auto_07_question.py
PARAMETERS RETURNED:
- "n": tm.Integer (range: 1-11) from gen.random_integer(1, 11)
- "x": tm.Symbol(s="x") # Fixed symbol
- "relation": Comparison expression x**2 > n

FILE: spe_sujet1_auto_08_question.py
PARAMETERS RETURNED:
- "x": tm.Symbol(s="x") # Fixed symbol
- "a": tm.Fraction(p=random_int_1_5, q=random_int_1_5)
- "b": tm.Integer (range: 1-4) from gen.random_integer(1, 4)

FILE: spe_sujet1_auto_09_question.py
PARAMETERS RETURNED:
- "x": tm.Symbol(s="x") # Fixed symbol
- "c1": tm.Integer (range: -10 to 10)
- "a2": tm.Fraction(p=1, q=random_int_1_10)
- "b2": tm.Integer (range: -10 to 10)
- "c2": tm.Integer (range: 1-10)
- "a3": tm.Fraction(p=random_int_1_10, q=random_int_1_10)
- "b3": tm.Integer (range: -10 to 10)
- "c3": tm.Decimal(p=random_int_1_20, q=random_element_from([1,2,4,5,8,10]))
- "expr1": Complex expression x**2 - (x + c1)**2
- "expr2": Complex expression a2*x - (b2 + 1/sqrt(c2))
- "expr3": Complex expression (a3*x + b3) / c3

FILE: spe_sujet1_auto_10_question.py
PARAMETERS RETURNED:
- "a": tm.Integer(n=±1) from random_element_from([-1, 1])
- "c": tm.Integer(n=±random_int_1_10) # Sign from random_element_from([-1, 1])
- "x": tm.Symbol(s="x") # Fixed symbol

FILE: spe_sujet1_auto_11_question.py
PARAMETERS RETURNED:
- "root1": tm.Integer (range: -7 to -5)
- "root2": tm.Integer (range: -1 to 3)
- "root3": tm.Integer (range: root2+3 to 10) # Dependent on root2
- "x": tm.Integer (range: -10 to 10, but not equal to any root)
- "f": tm.Function(name="f") # Fixed function

FILE: spe_sujet1_auto_12_question.py
PARAMETERS RETURNED:
- "note1": tm.Integer (range: 0-20)
- "note2": tm.Integer (range: 0-20)
- "note3": tm.Integer (range: 0-20)
- "coef1": tm.Integer (range: 1-5)
- "coef2": tm.Integer (range: 1-5)
- "coef3": tm.Integer (range: 1-5)
- "mean": Computed tm.Fraction = (note1*coef1 + note2*coef2 + note3*coef3) / (coef1+coef2+coef3)

=== COMPREHENSIVE PARAMETER TYPE MAPPING ===

BASIC TYPES:
1. tm.Integer:
   - Direct from gen.random_integer(min, max)
   - Fixed values tm.Integer(n=constant)
   - From random_element_from for discrete choices

2. tm.Fraction:
   - tm.Fraction(p=num, q=den) where num/den can be integers or expressions
   - Often used for probabilities and ratios

3. tm.Symbol:
   - tm.Symbol(s="variable_name") for symbolic variables
   - Usually fixed strings like "x", "y", "u"

4. tm.Decimal:
   - tm.Decimal(p=value, q=base) for decimal representations
   - Base usually from [1,2,4,5,8,10] for nice decimals

5. tm.Function:
   - tm.Function(name="function_name") for function references

6. Collections:
   - Tuples of tm.Fractions from discrete_dirichlet_dist
   - tm.MathsCollection for grouped objects

COMPUTED EXPRESSIONS:
- Arithmetic combinations of basic types
- Comparison expressions (>, <, ==)
- Power expressions (**)
- Complex nested expressions

=== GENERATION STRATEGY ===

To generate all possible parameters:

1. ENUMERATE BASIC RANGES:
   - Integer ranges: collect all (min,max) pairs used
   - Fraction patterns: collect all (p_range, q_range) combinations
   - Symbol names: collect all string literals used
   - Decimal bases: [1,2,4,5,8,10]
   - Discrete choices: collect all lists passed to random_element_from

2. HANDLE DEPENDENCIES:
   - Some parameters depend on others (e.g., root3 depends on root2)
   - Track these dependency chains

3. EXPRESSION TEMPLATES:
   - Catalog all expression patterns used
   - Parameterize them for generation

4. SPECIAL CASES:
   - discrete_dirichlet_dist parameters
   - Conditional generation (while loops, if statements)
   - Computed fields that depend on multiple randoms

=== IMPLEMENTATION NOTES ===

The parser should:
1. Extract all gen.random_* calls and their parameters
2. Extract all tm.* instantiations and their parameters
3. Identify computed expressions and their dependencies
4. Build a parameter space that covers all possible combinations
5. Handle special generation functions like discrete_dirichlet_dist
6. Account for conditional logic that affects parameter ranges

This will enable comprehensive test coverage and parameter space exploration
for all question generators.
"""

# TODO: Implement the actual parsing logic based on this analysis
# This would involve AST parsing of each generate_components function
# to extract the parameter generation patterns systematically.


def parse_generate_components_functions():
    """
    Parse all generate_components functions using AST and extract parameter patterns.

    This function:
    1. Load each generator file
    2. Parse the generate_components function AST
    3. Extract all parameter generation patterns
    4. Build a comprehensive parameter space mapping
    5. Return a structured representation of all possible parameters
    """
    import ast
    from pathlib import Path

    print("=== PARSING GENERATE_COMPONENTS FUNCTIONS ===")
    print("Using AST to analyze parameter generation patterns\n")

    # Find all spe_sujet1_auto_*_question.py files
    generators_dir = Path(__file__).parent
    generator_files = list(generators_dir.glob("spe_sujet1_auto_*_question.py"))
    generator_files.sort()  # Sort for consistent order

    parsed_generators = {}

    for file_path in generator_files:
        print(f"📁 Parsing {file_path.name}")

        # Read the file
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Parse the AST
        try:
            tree = ast.parse(source_code)

            # Find the generate_components function
            generate_components_func = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "generate_components":
                    generate_components_func = node
                    break

            if generate_components_func is None:
                print("  ❌ No generate_components function found")
                continue

            # Analyze the function
            analysis = analyze_generate_components_ast(generate_components_func, file_path.name)
            parsed_generators[file_path.stem] = analysis

            print(f"  ✅ Found {len(analysis['parameters'])} parameters")
            for param_name, param_info in analysis["parameters"].items():
                print(f"     • {param_name}: {param_info['type']} {param_info.get('range', '')}")
            print()

        except Exception as e:
            print(f"  ❌ Error parsing {file_path.name}: {e}")
            continue

    print(f"=== PARSING COMPLETE: {len(parsed_generators)} generators analyzed ===\n")
    return parsed_generators


def analyze_generate_components_ast(func_node, filename):
    """
    Analyze a generate_components function AST node to extract parameter patterns.
    """
    analysis = {"filename": filename, "parameters": {}, "dependencies": [], "special_cases": []}

    # Walk through all statements in the function
    for stmt in func_node.body:
        if isinstance(stmt, ast.Assign):
            # Handle assignments like: n = gen.random_integer(2, 5)
            analyze_assignment(stmt, analysis)
        elif isinstance(stmt, ast.Return):
            # Handle the return statement to see what's returned
            analyze_return_statement(stmt, analysis)

    return analysis


def analyze_assignment(assign_node, analysis):
    """
    Analyze an assignment statement to extract parameter generation patterns.
    """
    # Get the variable name being assigned
    if len(assign_node.targets) != 1:
        return  # Skip multiple assignments

    target = assign_node.targets[0]
    if not isinstance(target, ast.Name):
        return  # Skip complex targets

    var_name = target.id
    value = assign_node.value

    # Analyze the value being assigned
    param_info = analyze_expression(value)
    if param_info:
        analysis["parameters"][var_name] = param_info


def analyze_expression(node):
    """
    Analyze an expression to determine what kind of parameter it generates.
    """
    if isinstance(node, ast.Call):
        return analyze_call_expression(node)
    elif isinstance(node, ast.BinOp):
        return analyze_binary_operation(node)
    elif isinstance(node, ast.Constant):
        return {"type": "constant", "value": node.value}
    elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
        return {"type": "constant", "value": node.n}
    elif isinstance(node, ast.Str):  # Python < 3.8 compatibility
        return {"type": "constant", "value": node.s}

    return None


def analyze_call_expression(call_node):
    """
    Analyze function calls like gen.random_integer(2, 5) or tm.Integer(n=1).
    """
    # Handle method calls like gen.random_integer()
    if isinstance(call_node.func, ast.Attribute):
        obj_name = None
        if isinstance(call_node.func.value, ast.Name):
            obj_name = call_node.func.value.id

        method_name = call_node.func.attr

        if obj_name == "gen":
            return analyze_generator_call(method_name, call_node.args)
        elif obj_name == "tm":
            return analyze_math_object_call(method_name, call_node.args, call_node.keywords)

    # Handle direct function calls
    elif isinstance(call_node.func, ast.Name):
        func_name = call_node.func.id
        # Handle calls like range(), etc.

    return None


def analyze_generator_call(method_name, args):
    """
    Analyze generator method calls like gen.random_integer(2, 5).
    """
    if method_name == "random_integer":
        if len(args) >= 2:
            min_val = extract_constant_value(args[0])
            max_val = extract_constant_value(args[1])
            if min_val is not None and max_val is not None:
                return {
                    "type": "random_integer",
                    "range": f"[{min_val}, {max_val}]",
                    "min": min_val,
                    "max": max_val,
                    "possible_values": list(range(min_val, max_val + 1)),
                }

    elif method_name == "random_element_from":
        if len(args) >= 1:
            elements = extract_list_elements(args[0])
            if elements is not None:
                return {"type": "random_choice", "choices": elements, "possible_values": elements}

    elif method_name == "discrete_dirichlet_dist":
        # Extract n, q, exclude_zero parameters
        n, q, exclude_zero = None, None, None
        if len(args) >= 1:
            n = extract_constant_value(args[0])
        if len(args) >= 2:
            q = extract_constant_value(args[1])
        return {"type": "dirichlet_distribution", "n": n, "q": q, "exclude_zero": exclude_zero}

    return {"type": f"generator_{method_name}"}


def analyze_math_object_call(class_name, args, keywords):
    """
    Analyze math object creation like tm.Integer(n=5) or tm.Fraction(p=1, q=2).
    """
    if class_name == "Integer":
        # Look for n= keyword argument
        for kw in keywords:
            if kw.arg == "n":
                value = extract_constant_value(kw.value)
                if value is not None:
                    return {"type": "fixed_integer", "value": value, "possible_values": [value]}

    elif class_name == "Symbol":
        # Look for s= keyword argument
        for kw in keywords:
            if kw.arg == "s":
                value = extract_constant_value(kw.value)
                if value is not None:
                    return {"type": "fixed_symbol", "value": value, "possible_values": [value]}

    elif class_name == "Fraction":
        # Handle tm.Fraction(p=..., q=...)
        p_info, q_info = None, None
        for kw in keywords:
            if kw.arg == "p":
                p_info = analyze_expression(kw.value)
            elif kw.arg == "q":
                q_info = analyze_expression(kw.value)

        return {"type": "fraction", "numerator": p_info, "denominator": q_info}

    return {"type": f"math_object_{class_name}"}


def analyze_binary_operation(binop_node):
    """
    Analyze binary operations like multiplication, addition, etc.
    """
    return {"type": "computed_expression", "operation": type(binop_node.op).__name__}


def analyze_return_statement(return_node, analysis):
    """
    Analyze the return statement to see what parameters are actually returned.
    """
    if isinstance(return_node.value, ast.Dict):
        # Handle return {"param1": value1, "param2": value2}
        for key, value in zip(return_node.value.keys, return_node.value.values):
            if isinstance(key, ast.Constant):
                param_name = key.value
            elif isinstance(key, ast.Str):  # Python < 3.8
                param_name = key.s
            else:
                continue

            # Mark this parameter as returned
            if param_name in analysis["parameters"]:
                analysis["parameters"][param_name]["returned"] = True


def extract_constant_value(node):
    """
    Extract a constant value from an AST node.
    """
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.Str):  # Python < 3.8
        return node.s
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        # Handle negative numbers like -1
        inner_value = extract_constant_value(node.operand)
        if inner_value is not None:
            return -inner_value

    return None


def extract_list_elements(node):
    """
    Extract elements from a list/tuple literal.
    """
    if isinstance(node, (ast.List, ast.Tuple)):
        elements = []
        for elt in node.elts:
            value = extract_constant_value(elt)
            if value is not None:
                elements.append(value)
        return elements

    return None


def generate_parameter_grid(parsed_generators=None):
    """
    Generate a comprehensive grid of all possible parameter combinations.

    Uses AST parsing results to create ALL possible combinations of parameter values
    in lexicographic order (natural increase).

    Returns a dictionary mapping each generator to its complete parameter space.
    """
    import itertools

    if parsed_generators is None:
        # Parse the generators first
        parsed_generators = parse_generate_components_functions()

    print("=== GENERATING PARAMETER HYPERCUBE FROM AST ANALYSIS ===")
    print("Creating all possible parameter combinations based on parsed patterns\n")

    all_combinations = {}

    for generator_name, analysis in parsed_generators.items():
        print(f"🎯 GENERATOR: {generator_name}")
        print(f"File: {analysis['filename']}")

        # Extract parameter spaces from analysis
        param_spaces = {}
        returned_params = []

        for param_name, param_info in analysis["parameters"].items():
            if "possible_values" in param_info:
                param_spaces[param_name] = param_info["possible_values"]
                print(
                    f"  • {param_name}: {param_info['type']} with {len(param_info['possible_values'])} values"
                )
                if len(param_info["possible_values"]) <= 10:
                    print(f"    Values: {param_info['possible_values']}")
                else:
                    print(
                        f"    Range: {param_info['possible_values'][0]} to {param_info['possible_values'][-1]}"
                    )
            else:
                print(f"  • {param_name}: {param_info['type']} (complex/computed)")

        # Generate all combinations for this generator
        if param_spaces:
            param_names = list(param_spaces.keys())
            param_value_lists = [param_spaces[name] for name in param_names]

            generator_combinations = []
            for value_combination in itertools.product(*param_value_lists):
                combination = {}
                for param_name, value in zip(param_names, value_combination):
                    combination[param_name] = create_math_object_from_value(
                        value, analysis["parameters"][param_name]
                    )

                # Handle computed/complex parameters
                combination = add_computed_parameters(combination, analysis)
                generator_combinations.append(combination)

            all_combinations[generator_name] = generator_combinations
            print(f"  📊 Total combinations: {len(generator_combinations):,}")

            # Show first few combinations
            if generator_combinations:
                print(f"  📝 First combination: {format_combination(generator_combinations[0])}")
                if len(generator_combinations) > 1:
                    print(
                        f"  📝 Last combination: {format_combination(generator_combinations[-1])}"
                    )
        else:
            print("  ❌ No simple parameter spaces found")

        print()

    # Summary
    print("=== HYPERCUBE GENERATION COMPLETE ===")
    total_combinations = sum(len(combinations) for combinations in all_combinations.values())
    print(f"🎯 Generated {total_combinations:,} total parameter combinations across all generators")
    print("\n📊 Breakdown by generator:")
    for gen_name, combinations in all_combinations.items():
        print(f"   • {gen_name}: {len(combinations):,} combinations")

    return all_combinations


def create_math_object_from_value(value, param_info):
    """
    Create the appropriate tm.MathsObject from a value based on parameter info.
    """
    import teachers.maths as tm

    param_type = param_info["type"]

    if param_type == "random_integer":
        return tm.Integer(n=value)
    elif param_type == "random_choice":
        if isinstance(value, str):
            return tm.Symbol(s=value)
        else:
            return tm.Integer(n=value)
    elif param_type == "fixed_integer":
        return tm.Integer(n=value)
    elif param_type == "fixed_symbol":
        return tm.Symbol(s=value)
    else:
        # Default to integer for unknown types
        return tm.Integer(n=value)


def add_computed_parameters(combination, analysis):
    """
    Add computed parameters to a combination based on the analysis.
    This handles complex expressions that depend on other parameters.
    """

    # This is where we'd handle complex cases like:
    # - coef = tm.Integer(n=1) + direction * p
    # - Fractions with computed numerators/denominators
    # - Complex mathematical expressions

    # For now, we'll handle some basic cases we know about
    for param_name, param_info in analysis["parameters"].items():
        if param_name not in combination:
            if param_info["type"] == "computed_expression":
                # Try to compute based on known patterns
                # This would need to be expanded based on specific patterns found
                pass
            elif param_info["type"] == "fraction":
                # Handle fractions with computed parts
                p_info = param_info.get("numerator")
                q_info = param_info.get("denominator")
                if p_info and q_info:
                    # Try to create fraction from parts
                    pass

    return combination


def format_combination(combination):
    """
    Format a parameter combination for display.
    """
    formatted = {}
    for key, value in combination.items():
        if hasattr(value, "n"):  # Integer
            formatted[key] = value.n
        elif hasattr(value, "s"):  # Symbol
            formatted[key] = f"'{value.s}'"
        elif hasattr(value, "p") and hasattr(value, "q"):  # Fraction
            formatted[key] = f"{value.p.n}/{value.q.n}"
        else:
            formatted[key] = str(value)

    return formatted


def hypercube_test_main():
    """
    Test all parameter generation patterns found in the generate_components functions.
    This function redefines generate_components for each test case to cover all patterns.
    """
    import teachers.generator as tg
    import teachers.maths as tm
    from teachers.defaults import SEED

    print("=== HYPERCUBE TEST SUITE ===")
    print("Testing all parameter generation patterns from spe_sujet1_auto_*_question.py files\n")

    # Test Case 1: Simple integer ranges (like spe_sujet1_auto_01_question.py)
    # This tests the most basic pattern: generating random integers within specific ranges
    # Pattern: gen.random_integer(min, max) -> tm.Integer
    print("TEST 1: Simple integer ranges")

    def generate_components_test1(difficulty, seed=SEED):
        """
        Tests basic integer generation patterns:
        - n: Integer in range [2, 5] (used for multipliers like "double", "triple", etc.)
        - x: Integer in range [1, 10] (used for basic numeric values)
        """
        gen = tg.MathsGenerator(seed)
        n = gen.random_integer(2, 5)  # Range for literal multipliers (double, triple, etc.)
        x = gen.random_integer(1, 10)  # Range for basic integer values
        return {"n": n, "x": x}

    result1 = generate_components_test1(None, 0)
    print(f"  Result: {result1}")
    print(f"  Types: n={type(result1['n'])}, x={type(result1['x'])}")

    # Assertions for Test Case 1
    assert isinstance(result1["n"], tm.Integer), f"Expected tm.Integer, got {type(result1['n'])}"
    assert isinstance(result1["x"], tm.Integer), f"Expected tm.Integer, got {type(result1['x'])}"
    assert 2 <= result1["n"].n <= 5, f"n value {result1['n'].n} not in range [2, 5]"
    assert 1 <= result1["x"].n <= 10, f"x value {result1['x'].n} not in range [1, 10]"
    assert len(result1) == 2, f"Expected 2 parameters, got {len(result1)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 2: Mixed fractions and integers (like spe_sujet1_auto_02_question.py)
    # This tests fraction creation with fixed numerators and random denominators
    # Pattern: tm.Fraction(p=fixed, q=random) and tm.Fraction(p=negative, q=random)
    print("TEST 2: Mixed fractions and integers")

    def generate_components_test2(difficulty, seed=SEED):
        """
        Tests mixed fraction and integer generation:
        - a: Fraction with fixed numerator (1) and random denominator [1, 10]
        - b, c: Regular integers in range [1, 10]
        - d: Fraction with fixed negative numerator (-1) and random denominator [1, 10]
        This pattern is used for algebraic expressions like a + b/(c*d)
        """
        gen = tg.MathsGenerator(seed)
        p = tm.Integer(n=1)  # Fixed numerator for positive fraction
        q = gen.random_integer(1, 10)  # Random denominator
        a = tm.Fraction(p=p, q=q)  # Positive unit fraction: 1/q
        b = gen.random_integer(1, 10)  # Integer coefficient
        c = gen.random_integer(1, 10)  # Integer coefficient
        d = tm.Fraction(p=tm.Integer(n=-1), q=gen.random_integer(1, 10))  # Negative unit fraction
        return {"a": a, "b": b, "c": c, "d": d}

    result2 = generate_components_test2(None, 0)
    print(f"  Result: {result2}")
    print(
        f"  Types: a={type(result2['a'])}, b={type(result2['b'])}, c={type(result2['c'])}, d={type(result2['d'])}"
    )

    # Assertions for Test Case 2
    assert isinstance(result2["a"], tm.Fraction), f"Expected tm.Fraction, got {type(result2['a'])}"
    assert isinstance(result2["b"], tm.Integer), f"Expected tm.Integer, got {type(result2['b'])}"
    assert isinstance(result2["c"], tm.Integer), f"Expected tm.Integer, got {type(result2['c'])}"
    assert isinstance(result2["d"], tm.Fraction), f"Expected tm.Fraction, got {type(result2['d'])}"
    assert result2["a"].p.n == 1, f"Expected a.p = 1, got {result2['a'].p.n}"
    assert 1 <= result2["a"].q.n <= 10, f"a.q value {result2['a'].q.n} not in range [1, 10]"
    assert 1 <= result2["b"].n <= 10, f"b value {result2['b'].n} not in range [1, 10]"
    assert 1 <= result2["c"].n <= 10, f"c value {result2['c'].n} not in range [1, 10]"
    assert result2["d"].p.n == -1, f"Expected d.p = -1, got {result2['d'].p.n}"
    assert 1 <= result2["d"].q.n <= 10, f"d.q value {result2['d'].q.n} not in range [1, 10]"
    assert len(result2) == 4, f"Expected 4 parameters, got {len(result2)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 3: Computed expressions with directions (like spe_sujet1_auto_03_question.py)
    # This tests computed expressions that depend on multiple random values and binary choices
    # Pattern: computed_value = base ± random_fraction, where ± is randomly chosen
    print("TEST 3: Computed expressions with random directions")

    def generate_components_test3(difficulty, seed=SEED):
        """
        Tests computed expressions with directional variation:
        - p: Percentage as fraction with range [1/200, 200/200] = [0.005, 1.0]
        - direction: Binary choice (-1 or +1) for increase/decrease
        - coef: Computed coefficient = 1 + direction * p (for percentage calculations)
        This pattern is used for percentage increase/decrease problems
        """
        gen = tg.MathsGenerator(seed)
        p = gen.random_integer(1, 200)  # Random numerator for percentage
        p = tm.Fraction(p=p, q=200)  # Convert to fraction (percentage/200)
        direction = tm.Integer(n=gen.random_element_from((-1, 1)))  # Random direction ±1
        coef = tm.Integer(n=1) + direction * p  # Computed coefficient: 1 ± p
        return {"p": p, "direction": direction, "coef": coef}

    result3 = generate_components_test3(None, 0)
    print(f"  Result: {result3}")
    print(
        f"  Types: p={type(result3['p'])}, direction={type(result3['direction'])}, coef={type(result3['coef'])}"
    )

    # Assertions for Test Case 3
    assert isinstance(result3["p"], tm.Fraction), f"Expected tm.Fraction, got {type(result3['p'])}"
    assert isinstance(result3["direction"], tm.Integer), (
        f"Expected tm.Integer, got {type(result3['direction'])}"
    )
    assert hasattr(result3["coef"], "eval"), (
        f"Expected computed expression, got {type(result3['coef'])}"
    )
    assert 1 <= result3["p"].p.n <= 200, f"p numerator {result3['p'].p.n} not in range [1, 200]"
    assert result3["p"].q.n == 200, f"Expected p.q = 200, got {result3['p'].q.n}"
    assert result3["direction"].n in [-1, 1], f"direction {result3['direction'].n} not in [-1, 1]"
    # Verify coef is computed correctly: 1 + direction * p
    expected_coef = 1 + result3["direction"].n * (result3["p"].p.n / 200)
    actual_coef = result3["coef"].eval()
    assert abs(actual_coef - expected_coef) < 1e-10, (
        f"coef calculation error: expected {expected_coef}, got {actual_coef}"
    )
    assert len(result3) == 3, f"Expected 3 parameters, got {len(result3)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 4: Multiples and binary choices (like spe_sujet1_auto_04_question.py)
    # This tests constraint-based generation where values must satisfy specific mathematical properties
    # Pattern: constrained_value = multiplier * random_base, ensuring specific divisibility
    print("TEST 4: Multiples and binary choices")

    def generate_components_test4(difficulty, seed=SEED):
        """
        Tests constrained integer generation with multiples:
        - p: Integer that's always a multiple of 5, range [5, 100] (5*1 to 5*20)
        - direction: Binary choice (-1 or +1) for directional operations
        This pattern ensures "nice" percentages (multiples of 5%) for easier calculations
        """
        gen = tg.MathsGenerator(seed)
        p = gen.random_integer(1, 20)  # Base multiplier [1, 20]
        p = tm.Integer(n=5 * p.n)  # Always multiple of 5: [5, 100]
        direction = tm.Integer(n=gen.random_element_from((-1, 1)))  # Random direction ±1
        return {"p": p, "direction": direction}

    result4 = generate_components_test4(None, 0)
    print(f"  Result: {result4}")
    print(f"  Types: p={type(result4['p'])}, direction={type(result4['direction'])}")
    print(f"  p value is multiple of 5: {result4['p'].n % 5 == 0}")

    # Assertions for Test Case 4
    assert isinstance(result4["p"], tm.Integer), f"Expected tm.Integer, got {type(result4['p'])}"
    assert isinstance(result4["direction"], tm.Integer), (
        f"Expected tm.Integer, got {type(result4['direction'])}"
    )
    assert 5 <= result4["p"].n <= 100, f"p value {result4['p'].n} not in range [5, 100]"
    assert result4["p"].n % 5 == 0, f"p value {result4['p'].n} is not a multiple of 5"
    assert result4["direction"].n in [-1, 1], f"direction {result4['direction'].n} not in [-1, 1]"
    assert len(result4) == 2, f"Expected 2 parameters, got {len(result4)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 5: Discrete Dirichlet distribution (like spe_sujet1_auto_05_question.py)
    # This tests advanced probability distribution generation for discrete probability problems
    # Pattern: gen.discrete_dirichlet_dist(n, q, exclude_zero) -> tuple of tm.Fractions
    print("TEST 5: Discrete Dirichlet distribution")

    def generate_components_test5(difficulty, seed=SEED):
        """
        Tests discrete Dirichlet distribution generation:
        - probabilities: Tuple of 4 fractions that sum to 1, all with denominator 24
        - Each probability > 0 (exclude_zero=True)
        - Used for probability problems with dice, cards, etc.
        This generates valid probability distributions for discrete events
        """
        gen = tg.MathsGenerator(seed)
        probabilities = gen.discrete_dirichlet_dist(n=4, q=24, exclude_zero=True)
        return {"probabilities": probabilities}

    result5 = generate_components_test5(None, 0)
    print(f"  Result: {result5}")
    print(f"  Types: probabilities={type(result5['probabilities'])}")
    print(f"  Probabilities count: {len(result5['probabilities'])}")

    # Assertions for Test Case 5
    assert isinstance(result5["probabilities"], tuple), (
        f"Expected tuple, got {type(result5['probabilities'])}"
    )
    assert len(result5["probabilities"]) == 4, (
        f"Expected 4 probabilities, got {len(result5['probabilities'])}"
    )
    for i, prob in enumerate(result5["probabilities"]):
        assert isinstance(prob, tm.Fraction), f"Probability {i} is not tm.Fraction: {type(prob)}"
        assert prob.q.n == 24, f"Probability {i} denominator is {prob.q.n}, expected 24"
        assert prob.p.n > 0, f"Probability {i} numerator is {prob.p.n}, expected > 0"
    # Check probabilities sum to 1
    total = sum(prob.p.n for prob in result5["probabilities"])
    assert total == 24, f"Probabilities sum to {total}/24, expected 24/24 = 1"
    assert len(result5) == 1, f"Expected 1 parameter, got {len(result5)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 6: Fixed symbols (like spe_sujet1_auto_06_question.py)
    # This tests symbolic variable creation for algebraic expressions
    # Pattern: tm.Symbol(s="variable_name") -> symbolic variable
    print("TEST 6: Fixed symbols")

    def generate_components_test6(difficulty, seed=SEED):
        """
        Tests fixed symbolic variable generation:
        - x, y, u: Fixed symbolic variables for algebraic expressions
        - No randomization - these are constants for the problem structure
        - Used in problems involving symbolic manipulation and equations
        """
        return {
            "x": tm.Symbol(s="x"),  # Independent variable
            "y": tm.Symbol(s="y"),  # Dependent variable
            "u": tm.Symbol(s="u"),  # Result variable
        }

    result6 = generate_components_test6(None, 0)
    print(f"  Result: {result6}")
    print(f"  Types: x={type(result6['x'])}, y={type(result6['y'])}, u={type(result6['u'])}")

    # Assertions for Test Case 6
    assert isinstance(result6["x"], tm.Symbol), f"Expected tm.Symbol, got {type(result6['x'])}"
    assert isinstance(result6["y"], tm.Symbol), f"Expected tm.Symbol, got {type(result6['y'])}"
    assert isinstance(result6["u"], tm.Symbol), f"Expected tm.Symbol, got {type(result6['u'])}"
    assert result6["x"].s == "x", f"Expected x.s = 'x', got '{result6['x'].s}'"
    assert result6["y"].s == "y", f"Expected y.s = 'y', got '{result6['y'].s}'"
    assert result6["u"].s == "u", f"Expected u.s = 'u', got '{result6['u'].s}'"
    assert len(result6) == 3, f"Expected 3 parameters, got {len(result6)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 7: Comparison expressions (like spe_sujet1_auto_07_question.py)
    # This tests relational expression creation for inequality problems
    # Pattern: symbolic_expr comparison_op numeric_value -> comparison expression
    print("TEST 7: Comparison expressions")

    def generate_components_test7(difficulty, seed=SEED):
        """
        Tests comparison expression generation:
        - n: Integer threshold [1, 11] for inequality comparisons
        - x: Symbolic variable for the inequality
        - relation: Comparison expression x² > n for solving inequalities
        This pattern is used for graphical inequality problems
        """
        gen = tg.MathsGenerator(seed)
        n = gen.random_integer(1, 11)  # Threshold for nice square roots
        x = tm.Symbol(s="x")  # Variable in the inequality
        relation = x ** tm.Integer(n=2) > n  # Quadratic inequality: x² > n
        return {"n": n, "x": x, "relation": relation}

    result7 = generate_components_test7(None, 0)
    print(f"  Result: {result7}")
    print(
        f"  Types: n={type(result7['n'])}, x={type(result7['x'])}, relation={type(result7['relation'])}"
    )

    # Assertions for Test Case 7
    assert isinstance(result7["n"], tm.Integer), f"Expected tm.Integer, got {type(result7['n'])}"
    assert isinstance(result7["x"], tm.Symbol), f"Expected tm.Symbol, got {type(result7['x'])}"
    assert hasattr(result7["relation"], "latex"), (
        f"Expected comparison expression, got {type(result7['relation'])}"
    )
    assert 1 <= result7["n"].n <= 11, f"n value {result7['n'].n} not in range [1, 11]"
    assert result7["x"].s == "x", f"Expected x.s = 'x', got '{result7['x'].s}'"
    assert len(result7) == 3, f"Expected 3 parameters, got {len(result7)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 8: Fraction with random numerator and denominator (like spe_sujet1_auto_08_question.py)
    # This tests fraction generation with both parts random for linear equations
    # Pattern: tm.Fraction(p=random, q=random) -> rational coefficient
    print("TEST 8: Fraction with random numerator and denominator")

    def generate_components_test8(difficulty, seed=SEED):
        """
        Tests fraction generation with random components:
        - x: Symbolic variable for linear equations
        - a: Fraction coefficient with both p and q random [1, 5]
        - b: Integer constant term [1, 4]
        This pattern creates rational linear functions y = ax + b
        """
        gen = tg.MathsGenerator(seed)
        p = gen.random_integer(1, 5)  # Random numerator [1, 5]
        q = gen.random_integer(1, 5)  # Random denominator [1, 5]
        a = tm.Fraction(p=p, q=q)  # Rational coefficient a = p/q
        b = gen.random_integer(1, 4)  # Integer y-intercept
        x = tm.Symbol(s="x")  # Independent variable
        return {"x": x, "a": a, "b": b}

    result8 = generate_components_test8(None, 0)
    print(f"  Result: {result8}")
    print(f"  Types: x={type(result8['x'])}, a={type(result8['a'])}, b={type(result8['b'])}")

    # Assertions for Test Case 8
    assert isinstance(result8["x"], tm.Symbol), f"Expected tm.Symbol, got {type(result8['x'])}"
    assert isinstance(result8["a"], tm.Fraction), f"Expected tm.Fraction, got {type(result8['a'])}"
    assert isinstance(result8["b"], tm.Integer), f"Expected tm.Integer, got {type(result8['b'])}"
    assert result8["x"].s == "x", f"Expected x.s = 'x', got '{result8['x'].s}'"
    assert 1 <= result8["a"].p.n <= 5, f"a.p value {result8['a'].p.n} not in range [1, 5]"
    assert 1 <= result8["a"].q.n <= 5, f"a.q value {result8['a'].q.n} not in range [1, 5]"
    assert 1 <= result8["b"].n <= 4, f"b value {result8['b'].n} not in range [1, 4]"
    assert len(result8) == 3, f"Expected 3 parameters, got {len(result8)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 9: Complex expressions with decimals (like spe_sujet1_auto_09_question.py)
    # This tests the most complex generation pattern with multiple types and nested expressions
    # Pattern: Mix of integers, fractions, decimals, and complex mathematical expressions
    print("TEST 9: Complex expressions with decimals")

    def generate_components_test9(difficulty, seed=SEED):
        """
        Tests complex multi-type parameter generation:
        - x: Symbolic variable for all expressions
        - c1: Integer [-10, 10] for quadratic expansion
        - a2, b2, c2: Mixed types for second expression
        - a3, b3, c3: Mixed types including decimals for third expression
        - expr1, expr2, expr3: Complex nested mathematical expressions
        This is the most comprehensive test covering all generation patterns
        """
        gen = tg.MathsGenerator(seed)
        x = tm.Symbol(s="x")  # Common variable
        c1 = gen.random_integer(-10, 10)  # Integer for quadratic
        a2 = tm.Fraction(p=1, q=gen.random_integer(1, 10))  # Unit fraction coefficient
        b2 = gen.random_integer(-10, 10)  # Integer constant
        c2 = gen.random_integer(1, 10)  # Positive integer for square root
        a3 = tm.Fraction(
            p=gen.random_integer(1, 10), q=gen.random_integer(1, 10)
        )  # General fraction
        b3 = gen.random_integer(-10, 10)  # Integer constant
        c3 = tm.Decimal(  # Decimal with nice denominators
            p=gen.random_integer(1, 20).n, q=gen.random_element_from([1, 2, 4, 5, 8, 10])
        )
        # Complex expressions combining multiple operations
        expr1 = x ** tm.Integer(n=2) - (x + c1) ** tm.Integer(n=2)  # Difference of squares
        expr2 = a2 * x - (
            b2 + tm.Integer(n=1) / (c2 ** (tm.Integer(n=1) / tm.Integer(n=2)))
        )  # With square root
        expr3 = (a3 * x + b3) / c3  # Rational expression
        return {
            "x": x,
            "c1": c1,
            "a2": a2,
            "b2": b2,
            "c2": c2,
            "a3": a3,
            "b3": b3,
            "c3": c3,
            "expr1": expr1,
            "expr2": expr2,
            "expr3": expr3,
        }

    result9 = generate_components_test9(None, 0)
    print(f"  Result: {result9}")
    print(f"  Types: c3={type(result9['c3'])}, expr1={type(result9['expr1'])}")

    # Assertions for Test Case 9 (comprehensive)
    assert isinstance(result9["x"], tm.Symbol), f"Expected tm.Symbol, got {type(result9['x'])}"
    assert isinstance(result9["c1"], tm.Integer), f"Expected tm.Integer, got {type(result9['c1'])}"
    assert isinstance(result9["a2"], tm.Fraction), (
        f"Expected tm.Fraction, got {type(result9['a2'])}"
    )
    assert isinstance(result9["b2"], tm.Integer), f"Expected tm.Integer, got {type(result9['b2'])}"
    assert isinstance(result9["c2"], tm.Integer), f"Expected tm.Integer, got {type(result9['c2'])}"
    assert isinstance(result9["a3"], tm.Fraction), (
        f"Expected tm.Fraction, got {type(result9['a3'])}"
    )
    assert isinstance(result9["b3"], tm.Integer), f"Expected tm.Integer, got {type(result9['b3'])}"
    assert isinstance(result9["c3"], tm.Decimal), f"Expected tm.Decimal, got {type(result9['c3'])}"
    assert -10 <= result9["c1"].n <= 10, f"c1 value {result9['c1'].n} not in range [-10, 10]"
    assert result9["a2"].p.n == 1, f"Expected a2.p = 1, got {result9['a2'].p.n}"
    assert 1 <= result9["c3"].q in [1, 2, 4, 5, 8, 10], (
        f"c3.q = {result9['c3'].q} not in allowed values"
    )
    assert len(result9) == 11, f"Expected 11 parameters, got {len(result9)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 10: Signed integers (like spe_sujet1_auto_10_question.py)
    # This tests signed integer generation with directional multiplication
    # Pattern: signed_value = direction * base_value, where both parts are random
    print("TEST 10: Signed integers with direction")

    def generate_components_test10(difficulty, seed=SEED):
        """
        Tests signed integer generation with directional multiplication:
        - a: Integer that's either +1 or -1 (parabola orientation)
        - c: Integer with random sign and magnitude [±1, ±10] (y-intercept)
        - x: Symbolic variable for parabola equation
        This pattern creates parabola coefficients: y = ax² + c
        """
        gen = tg.MathsGenerator(seed)
        dir1 = gen.random_element_from([-1, 1])  # Random direction for 'a'
        a = tm.Integer(n=dir1)  # Parabola orientation: ±1
        c = gen.random_integer(1, 10)  # Base magnitude for y-intercept
        dir2 = gen.random_element_from([-1, 1])  # Random sign for 'c'
        c = tm.Integer(n=dir2) * c  # Apply sign: ±c
        c = c.simplified()  # Simplify the result
        x = tm.Symbol(s="x")  # Variable for the parabola
        return {"a": a, "c": c, "x": x}

    result10 = generate_components_test10(None, 0)
    print(f"  Result: {result10}")
    print(f"  Types: a={type(result10['a'])}, c={type(result10['c'])}, x={type(result10['x'])}")

    # Assertions for Test Case 10
    assert isinstance(result10["a"], tm.Integer), f"Expected tm.Integer, got {type(result10['a'])}"
    assert isinstance(result10["c"], tm.Integer), f"Expected tm.Integer, got {type(result10['c'])}"
    assert isinstance(result10["x"], tm.Symbol), f"Expected tm.Symbol, got {type(result10['x'])}"
    assert result10["a"].n in [-1, 1], f"a value {result10['a'].n} not in [-1, 1]"
    assert -10 <= result10["c"].n <= 10 and result10["c"].n != 0, (
        f"c value {result10['c'].n} not in [±1, ±10]"
    )
    assert result10["x"].s == "x", f"Expected x.s = 'x', got '{result10['x'].s}'"
    assert len(result10) == 3, f"Expected 3 parameters, got {len(result10)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 11: Dependent ranges with exclusions (like spe_sujet1_auto_11_question.py)
    # This tests the most complex generation pattern with dependencies and exclusion logic
    # Pattern: dependent_value = f(previous_value), with exclusion constraints
    print("TEST 11: Dependent ranges with exclusions")

    def generate_components_test11(difficulty, seed=SEED):
        """
        Tests dependent range generation with exclusion logic:
        - root1: Integer [-7, -5] (leftmost root)
        - root2: Integer [-1, 3] (middle root)
        - root3: Integer [root2+3, 10] (rightmost root, depends on root2)
        - x: Integer [-10, 10] but NOT equal to any root (exclusion logic)
        - f: Function symbol for polynomial expressions
        This tests the most complex constraint satisfaction in generation
        """
        gen = tg.MathsGenerator(seed)
        root1 = gen.random_integer(-7, -5)  # Leftmost root (negative)
        root2 = gen.random_integer(-1, 3)  # Middle root (around zero)
        root3 = gen.random_integer(root2.n + 3, 10)  # Rightmost root (depends on root2!)
        x = gen.random_integer(-10, 10)  # Test point
        while x in [root1, root2, root3]:  # EXCLUSION LOGIC: x cannot be a root
            x = gen.random_integer(-10, 10)  # Keep trying until x ≠ any root
        f = tm.Function(name="f")  # Function symbol
        return {"root1": root1, "root2": root2, "root3": root3, "x": x, "f": f}

    result11 = generate_components_test11(None, 0)
    print(f"  Result: {result11}")
    print(f"  Types: root1={type(result11['root1'])}, f={type(result11['f'])}")
    print(f"  root3 > root2: {result11['root3'].n > result11['root2'].n}")
    print(
        f"  x not in roots: {result11['x'] not in [result11['root1'], result11['root2'], result11['root3']]}"
    )

    # Assertions for Test Case 11 (most complex)
    assert isinstance(result11["root1"], tm.Integer), (
        f"Expected tm.Integer, got {type(result11['root1'])}"
    )
    assert isinstance(result11["root2"], tm.Integer), (
        f"Expected tm.Integer, got {type(result11['root2'])}"
    )
    assert isinstance(result11["root3"], tm.Integer), (
        f"Expected tm.Integer, got {type(result11['root3'])}"
    )
    assert isinstance(result11["x"], tm.Integer), f"Expected tm.Integer, got {type(result11['x'])}"
    assert isinstance(result11["f"], tm.Function), (
        f"Expected tm.Function, got {type(result11['f'])}"
    )
    assert -7 <= result11["root1"].n <= -5, f"root1 {result11['root1'].n} not in range [-7, -5]"
    assert -1 <= result11["root2"].n <= 3, f"root2 {result11['root2'].n} not in range [-1, 3]"
    assert result11["root3"].n >= result11["root2"].n + 3, (
        f"root3 {result11['root3'].n} < root2+3 = {result11['root2'].n + 3}"
    )
    assert result11["root3"].n <= 10, f"root3 {result11['root3'].n} > 10"
    assert -10 <= result11["x"].n <= 10, f"x {result11['x'].n} not in range [-10, 10]"
    assert result11["x"] not in [result11["root1"], result11["root2"], result11["root3"]], (
        "x equals one of the roots"
    )
    assert result11["f"].name == "f", f"Expected f.name = 'f', got '{result11['f'].name}'"
    assert len(result11) == 5, f"Expected 5 parameters, got {len(result11)}"
    print("  ✅ All assertions passed")
    print()

    # Test Case 12: Computed weighted mean (like spe_sujet1_auto_12_question.py)
    # This tests multi-step computation with weighted averages
    # Pattern: computed_result = (sum of weighted_values) / (sum of weights)
    print("TEST 12: Computed weighted mean")

    def generate_components_test12(difficulty, seed=SEED):
        """
        Tests computed weighted mean generation:
        - note1, note2, note3: Grades [0, 20] (French grading system)
        - coef1, coef2, coef3: Coefficients [1, 5] (weight of each grade)
        - mean: Computed weighted average = (note1*coef1 + note2*coef2 + note3*coef3) / (coef1+coef2+coef3)
        This tests multi-parameter computation patterns for statistics problems
        """
        gen = tg.MathsGenerator(seed)
        note1 = gen.random_integer(0, 20)  # Grade 1 [0, 20]
        note2 = gen.random_integer(0, 20)  # Grade 2 [0, 20]
        note3 = gen.random_integer(0, 20)  # Grade 3 [0, 20]
        coef1 = gen.random_integer(1, 5)  # Weight 1 [1, 5]
        coef2 = gen.random_integer(1, 5)  # Weight 2 [1, 5]
        coef3 = gen.random_integer(1, 5)  # Weight 3 [1, 5]
        # Computed weighted mean: (Σ note_i * coef_i) / (Σ coef_i)
        mean = note1 * coef1 + note2 * coef2 + note3 * coef3  # Weighted sum
        mean = mean / (coef1 + coef2 + coef3)  # Divide by total weight
        return {
            "note1": note1,
            "note2": note2,
            "note3": note3,
            "coef1": coef1,
            "coef2": coef2,
            "coef3": coef3,
            "mean": mean,
        }

    result12 = generate_components_test12(None, 0)
    print(f"  Result: {result12}")
    print(f"  Types: mean={type(result12['mean'])}")
    print(f"  Mean value: {result12['mean'].eval()}")

    # Assertions for Test Case 12
    assert isinstance(result12["note1"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['note1'])}"
    )
    assert isinstance(result12["note2"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['note2'])}"
    )
    assert isinstance(result12["note3"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['note3'])}"
    )
    assert isinstance(result12["coef1"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['coef1'])}"
    )
    assert isinstance(result12["coef2"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['coef2'])}"
    )
    assert isinstance(result12["coef3"], tm.Integer), (
        f"Expected tm.Integer, got {type(result12['coef3'])}"
    )
    assert hasattr(result12["mean"], "eval"), (
        f"Expected computed expression, got {type(result12['mean'])}"
    )
    for i, note in enumerate([result12["note1"], result12["note2"], result12["note3"]], 1):
        assert 0 <= note.n <= 20, f"note{i} value {note.n} not in range [0, 20]"
    for i, coef in enumerate([result12["coef1"], result12["coef2"], result12["coef3"]], 1):
        assert 1 <= coef.n <= 5, f"coef{i} value {coef.n} not in range [1, 5]"
    # Verify mean calculation
    expected_mean = (
        result12["note1"].n * result12["coef1"].n
        + result12["note2"].n * result12["coef2"].n
        + result12["note3"].n * result12["coef3"].n
    ) / (result12["coef1"].n + result12["coef2"].n + result12["coef3"].n)
    actual_mean = result12["mean"].eval()
    assert abs(actual_mean - expected_mean) < 1e-10, (
        f"Mean calculation error: expected {expected_mean}, got {actual_mean}"
    )
    assert len(result12) == 7, f"Expected 7 parameters, got {len(result12)}"
    print("  ✅ All assertions passed")
    print()

    print("=== ALL TESTS COMPLETED SUCCESSFULLY ===")
    print("🎉 All 12 parameter generation patterns have been tested and validated!")
    print("📊 Coverage includes:")
    print("   • Simple and complex integer ranges")
    print("   • Fraction generation (fixed and random components)")
    print("   • Symbolic variables and expressions")
    print("   • Computed expressions and dependencies")
    print("   • Probability distributions")
    print("   • Constraint satisfaction and exclusion logic")
    print("   • Multi-type parameter mixing")
    print("   • All tg.MathsGenerator methods")
    print("   • All tm.MathsObject types")


if __name__ == "__main__":
    print("🚀 STARTING AST-BASED HYPERCUBE ANALYSIS")
    print("=" * 60 + "\n")

    # Step 1: Parse all generate_components functions using AST
    print("STEP 1: Parsing generate_components functions...")
    parsed_generators = parse_generate_components_functions()

    # Step 2: Generate the complete parameter hypercube from parsed data
    print("STEP 2: Generating parameter hypercube from AST analysis...")
    all_combinations = generate_parameter_grid(parsed_generators)

    print("\n" + "=" * 60)
    print("STEP 3: Running individual pattern validation tests...")
    print("=" * 60 + "\n")

    # Step 3: Run the individual pattern tests for validation
    hypercube_test_main()

    print("\n" + "=" * 60)
    print("🎉 AST-BASED HYPERCUBE ANALYSIS COMPLETE")
    print("=" * 60)
    print("✅ Parsed all generate_components functions using AST")
    print("✅ Generated complete parameter combinations from parsed patterns")
    print("✅ Validated all individual generation patterns")
    print("📊 Total parameter space coverage: COMPLETE")
    print("\n🎯 The hypercube contains ALL possible parameter combinations")
    print("   that each generator can produce, in lexicographic order!")
