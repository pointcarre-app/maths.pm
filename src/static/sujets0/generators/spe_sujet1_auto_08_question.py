import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-8]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'a': Fraction(p=Integer(n=10), q=Integer(n=1)), 'b': Integer(n=7)}
    """

    gen = tg.MathsGenerator(seed)
    p = gen.random_integer(1, 5)  # not 10: 🧂 for safest / easier plotting
    q = gen.random_integer(1, 5)  # not 10: 🧂 for safest / easier plotting
    a = tm.Fraction(p=p, q=q)
    b = gen.random_integer(1, 4)  # not 10: 🧂 for safest / easier plotting
    x = tm.Symbol(s="x")

    return {
        "x": x,
        "a": a,
        "b": b,
    }


def solve(*, x, a, b):
    """[sujets0][spé][sujet-1][automatismes][question-8]
    >>> x, a, b = tm.Symbol(s="x"), tm.Fraction(p=tm.Integer(n=10), q=tm.Integer(n=1)), tm.Integer(n=7)
    >>> answer = solve(x=x, a=a, b=b)
    >>> answer["maths_object"]
    Add(l=Mul(l=Fraction(p=Integer(n=10), q=Integer(n=1)), r=Symbol(s='x')), r=Integer(n=7))
    """
    maths_object = (a * x) + b
    return {"maths_object": maths_object}


def render_question(*, x, a, b):
    r"""[sujets0][spé][sujet-1][automatismes][question-8]
    >>> x, a, b = tm.Symbol(s="x"), tm.Fraction(p=tm.Integer(n=10), q=tm.Integer(n=1)), tm.Integer(n=7)
    >>> statement = render_question(x=x, a=a, b=b)
    >>> statement["statement"]
    "On a représenté ci-contre une droite (\\\\mathcal\\{D\\} dans un repère orthonormé. Donner l'équation de la droite \\\\mathcal\\{D\\} sous la forme $y=ax+b$"
    """

    statement = r"On a représenté ci-contre une droite (\\mathcal\{D\} dans un repère orthonormé. Donner l'équation de la droite \\mathcal\{D\} sous la forme $y=ax+b$"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


print(components | answer | question)


# Create HTML version with graph reference
statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            On a représenté ci-contre une droite $(\\mathcal{D})$ dans un repère orthonormé.
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Donner l'équation de la droite $\\mathcal{D}$ sous la forme <span class="badge badge-primary">$y=ax+b$</span>
        </div>
    </div>
</div>
"""

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-8]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "a": components["a"].latex(),
            "b": components["b"].latex(),
        },
    }
)
