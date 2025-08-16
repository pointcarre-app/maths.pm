import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-9]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'a': Integer(n=-1), 'b': Integer(n=4)}
    """

    gen = tg.MathsGenerator(seed)
    a = gen.random_element_from([-1, 1])
    b = gen.random_integer(1, 5)
    b = gen.random_element_from([-b.n, b.n])

    a = tm.Integer(n=a)
    b = tm.Integer(n=b)
    x = tm.Symbol(s="x")

    return {
        "x": x,
        "a": a,
        "b": b,
    }


def solve(*, x, a, b):
    """[sujets0][gén][sujet-1][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Mul(l=Integer(n=1), r=Symbol(s='x')), r=Integer(n=-4))
    """
    maths_object = (a * x) + b
    return {"maths_object": maths_object}


def render_question(*, x, a, b):
    """[sujets0][gén][sujet-1][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "On a représenté ci-contre une droite (\\\\mathcal{D} dans un repère orthonormé. Sachant que $\\\\lvert a \\\\rvert=1$ et $\\\\lvert b \\\\rvert = 4$. Donner l'équation de la droite \\\\mathcal{D} sous la forme $y=ax+b$"
    """

    abs_b = abs(b.n)

    statement = f"On a représenté ci-contre une droite (\\mathcal{{D}} dans un repère orthonormé. Sachant que $\\lvert a \\rvert=1$ et $\\lvert b \\rvert = {abs_b}$. Donner l'équation de la droite \\mathcal{{D}} sous la forme $y=ax+b$"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-9]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
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
