import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-2]

    Generates a proportionality problem with GUARANTEED clean decimal answers.

    >>> generate_components(None, 1)
    {'n1': Integer(n=3), 'n2': Integer(n=9), 'p': Fraction(p=Integer(n=146), q=Integer(n=10))}
    """

    gen = tg.MathsGenerator(seed)

    # ========================================================================
    # STEP 1: Choose quantities (n1 and n2)
    # ========================================================================
    # We need two different integer quantities to create the proportionality problem
    # n1: number of articles in the given information (2 to 10)
    # n2: number of articles we're asking about (2 to 20)
    n1 = gen.random_integer(2, 10)
    n2 = gen.random_integer(2, 10)
    while n2.n == n1.n:
        n2 = gen.random_integer(2, 20)

    # ========================================================================
    # STEP 2: Generate unit price with controlled decimal places
    # ========================================================================
    # THE KEY INSIGHT: By controlling the denominator of the unit price,
    # we mathematically GUARANTEE the decimal places in ANY multiplication.
    #
    # Mathematical proof:
    # - If price = integer/1 (whole number), then:
    #   n * price = n * integer = integer (0 decimals)
    #
    # - If price = integer/10 (one decimal max), then:
    #   n * price = n * (integer/10) = (n * integer)/10
    #   The result has denominator 10, so at most 1 decimal place
    #
    # - If price = integer/100 (two decimals max), then:
    #   n * price = n * (integer/100) = (n * integer)/100
    #   The result has denominator 100, so at most 2 decimal places
    #
    # This is a MATHEMATICAL CERTAINTY, not a probabilistic approach!

    choice = gen.random_integer(1, 10)
    if choice.n <= 3:
        # ====================================================================
        # 30% chance: Integer price (e.g., 25€)
        # ====================================================================
        # Examples: 1€, 15€, 50€
        # When multiplied by ANY integer n:
        # n * 25 = 25n (always an integer, 0 decimals)
        unit_price = gen.random_integer(1, 50)

    else:
        # choice.n <= 7:
        # ====================================================================
        # 40% chance: Price with exactly 1 decimal place (e.g., 12.5€)
        # ====================================================================
        # We generate integer/10, which gives values like:
        # 1/10 = 0.1, 235/10 = 23.5, 500/10 = 50.0
        #
        # When multiplied by any integer n:
        # n * (235/10) = 235n/10
        # The denominator is 10, so the decimal representation has AT MOST 1 decimal
        # Examples: 3 * 23.5 = 70.5 (1 decimal), 4 * 12.5 = 50 (0 decimals)
        unit_price = gen.random_integer(1, 500) / tm.Integer(n=10)

    # else:
    #     # ====================================================================
    #     # 30% chance: Price with exactly 2 decimal places (e.g., 12.99€)
    #     # ====================================================================
    #     # We generate integer/100, which gives values like:
    #     # 1/100 = 0.01, 1234/100 = 12.34, 5000/100 = 50.00
    #     #
    #     # When multiplied by any integer n:
    #     # n * (1234/100) = 1234n/100
    #     # The denominator is 100, so the decimal representation has AT MOST 2 decimals
    #     # Examples: 3 * 12.34 = 37.02 (2 decimals), 4 * 12.25 = 49 (0 decimals)
    #     unit_price = gen.random_integer(1, 5000) / tm.Integer(n=100)

    # ========================================================================
    # WHY THIS WORKS WITHOUT ANY LOOPS OR CHECKING:
    # ========================================================================
    # The mathematical principle is simple but powerful:
    #
    # 1. We control the DENOMINATOR of the unit price (1, 10, or 100)
    # 2. When we multiply by an integer, the denominator doesn't get worse
    # 3. A fraction with denominator 10^k has at most k decimal places
    #
    # This means:
    # - unit_price * n1 will have at most 2 decimal places
    # - unit_price * n2 will have at most 2 decimal places
    #
    # No need to check, no need to retry, it's GUARANTEED by arithmetic!
    # ========================================================================

    return {
        "n1": n1,
        "n2": n2,
        "p": unit_price,
    }


def solve(*, n1, n2, p):
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components= generate_components(None, 1)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=146), q=Integer(n=10)), r=Integer(n=9))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=657), q=Integer(n=5))
    """
    maths_object = p * n2
    return {
        "maths_object": maths_object,
    }


def render_question(*, n1, n2, p):
    r"""[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components= generate_components(None, 1)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    '3 articles coûtent 43,8 euros. Combien coûtent 9 articles ?'
    """

    p1 = (p * n1).simplified().as_decimal

    statement = f"${n1.latex()}$ articles coûtent ${p1.latex().replace('.', ',')}$ euros. Combien coûtent ${n2.latex()}$ articles ?"
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-2]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": [
                f"{components['n2'].latex()} \\times {components['p'].latex()}",
                answer["maths_object"].simplified().latex().replace(".", ","),
            ],
            "simplified_latex": [
                answer["maths_object"].simplified().latex().replace(".", ",") + " €",
                answer["maths_object"].simplified().as_decimal.latex().replace(".", ",") + " €",
            ],
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n1": components["n1"].latex(),
            "n2": components["n2"].latex(),
            "p": components["p"].latex(),
        },
    }
)
