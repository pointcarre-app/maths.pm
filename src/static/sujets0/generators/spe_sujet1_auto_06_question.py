# # ruff: noqa : E402


import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-6]
    >>> generate_components(None, 0)
    {'x': Symbol(s='x'), 'y': Symbol(s='y'), 'u': Symbol(s='u')}
    """

    # gen = tg.MathsGenerator(seed)

    return {
        "x": tm.Symbol(s="x"),
        "y": tm.Symbol(s="y"),
        "u": tm.Symbol(s="u"),
    }


def solve(*, x, y, u):
    """[sujets0][spé][sujet-1][automatismes][question-6]
    >>> x, y, u = tm.Symbol(s='x'), tm.Symbol(s='y'), tm.Symbol(s='u')
    >>> answer = solve(x=x, y=y, u=u)
    >>> answer["maths_object"]
    Fraction(p=Mul(l=Symbol(s='x'), r=Symbol(s='y')), q=Add(l=Symbol(s='x'), r=Symbol(s='y')))
    >>> answer["maths_object"].simplified()
    Fraction(p=Mul(l=Symbol(s='x'), r=Symbol(s='y')), q=Add(l=Symbol(s='x'), r=Symbol(s='y')))
    """
    maths_object = (x * y) / (x + y)
    return {
        "maths_object": maths_object,
    }


def render_question(*, x, y, u):
    r"""[sujets0][spé][sujet-1][automatismes][question-6]
    >>> x, y, u = tm.Symbol(s='x'), tm.Symbol(s='y'), tm.Symbol(s='u')
    >>> statement = render_question(x=x, y=y, u=u)
    >>> statement["statement"]
    'On considère $x$, $y$, et $u$ des réels non nuls tels que $\\dfrac{1}{x}+ \\dfrac{1}{y} = \\dfrac{1}{u}$. Exprimer $u$ en fonction $x$ et $y$.
    """

    statement = "On considère $x$, $y$, et $u$ des réels non nuls tels que $\\dfrac{1}{x}+ \\dfrac{1}{y} = \\dfrac{1}{u}$. Exprimer $u$ en fonction $x$ et $y$."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with highlighted equation
statement_html = """<div>On considère $x$, $y$, et $u$ des réels non nuls tels que : 
    <span>$\\dfrac{1}{x}+ \\dfrac{1}{y} = \\dfrac{1}{u}$</span>. Exprimer $u$ en fonction de $x$ et $y$.
</div>
"""

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-6]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "mask": "u=",
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "y": components["y"].latex(),
            "u": components["u"].latex(),
        },
    }
)
