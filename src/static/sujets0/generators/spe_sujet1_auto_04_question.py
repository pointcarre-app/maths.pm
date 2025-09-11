import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-4]
    >>> generate_components(None, 0)
    {'p': Integer(n=65), 'direction': Integer(n=1)}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 19)  # Avoid 100%
    p = tm.Integer(n=5 * p.n)

    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    return {"p": p, "direction": direction}


def solve(*, p, direction):
    """[sujets0][spé][sujet-1][automatismes][question-4]
    >>> answer = solve(p=tm.Integer(n=65), direction=tm.Integer(n=1))
    >>> answer["maths_object"]
    Mul(l=Integer(n=-1), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-169), q=Integer(n=400))
    """
    maths_object = -((p / tm.Integer(n=100)) ** tm.Integer(n=2))
    return {"maths_object": maths_object}


def render_question(*, p, direction):
    r"""[sujets0][spé][sujet-1][automatismes][question-4]
    >>> p = tm.Integer(n=65)
    >>> direction = tm.Integer(n=1)
    >>> statement = render_question(p=p, direction=direction)
    >>> statement["statement"]
    "Le prix d'un article est noté $P$. Ce prix augmente de $65\\%$ puis diminue de $65\\%$. A l'issue de ces deux variations, quelle est la variation du prix en pourcentage ?"
    """
    if direction == -1:
        dir1, dir2 = "diminue", "augmente"
    else:
        dir1, dir2 = "augmente", "diminue"

    statement = f"""Le prix d'un article est noté $P$. Ce prix {dir1} de ${p.latex()}\\%$ puis {dir2} de ${p.latex()}\\%$. A l'issue de ces deux variations, quelle est la variation du prix en pourcentage ?"""

    statement_html = f"""<div>Le prix d'un article est noté $P$. Ce prix {dir1} de ${p.latex()}\\%$ puis {dir2} de ${p.latex()}\\%$. À l'issue de ces deux variations, quelle est la variation du prix en pourcentage ?</div>"""
    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


statement_html = question["statement_html"]

# print(components | answer | question)


# Create HTML version with two-step process
if components["direction"].n == -1:
    dir1, dir2 = "diminue", "augmente"
else:
    dir1, dir2 = "augmente", "diminue"


# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()  # Fraction form
simplified_0 = answer["maths_object"].simplified().latex()  # Simplified fraction

# Convert fraction to percentage by multiplying by 100
# The answer is already a percentage variation (as a fraction), so multiply by 100 to get the percentage value
percent_value = answer["maths_object"] * tm.Integer(n=100)
percent_simplified = percent_value.simplified()

# If it's a nice decimal, show it as decimal, otherwise keep as fraction
if hasattr(percent_simplified, "as_decimal"):
    latex_1 = percent_simplified.as_decimal.latex() + r"\%"
    simplified_1 = percent_simplified.as_decimal.latex() + r"\%"  # Already simplified
else:
    latex_1 = percent_simplified.latex() + r"\%"
    simplified_1 = percent_simplified.latex() + r"\%"  # Already simplified

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-4]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "mask": "V_r=",
        "answer": {
            "latex": [
                latex_0.replace(".", ","),
                latex_1.replace(".", ","),
            ],  # List to support multiple correct answers
            "simplified_latex": [
                simplified_0.replace(".", ","),
                simplified_1.replace(".", ","),
            ],  # List of simplified versions
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p": components["p"].latex(),
            "direction": components["direction"].latex(),
        },
    }
)
