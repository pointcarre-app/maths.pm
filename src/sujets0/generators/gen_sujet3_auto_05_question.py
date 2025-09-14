import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-3][automatismes][question-5]
    >>> generate_components(None, 0)
    {'n': Symbol(s='n'), 'v': Function(name=V), 'x': Fraction(p=Integer(n=50), q=Integer(n=100))}
    """
    gen = tg.MathsGenerator(seed)

    x = gen.random_integer(1, 100) / tm.Integer(n=100)
    n = tm.Symbol(s="n")
    v = tm.Function(name="V")

    return {
        "n": n,
        "v": v,
        "x": x,
    }


def solve(*, n, v, x):
    """[sujets0][gén][sujet-3][automatismes][question-5]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Decimal(p=1, q=2), r=Function(name=V)(Symbol(s='n')))
    >>> answer["maths_object"].simplified()
    Mul(l=Decimal(p=1, q=2), r=Function(name=V)(Symbol(s='n')))
    """
    coef = (tm.Integer(n=1) - x).simplified().as_decimal
    maths_object = coef * v(n)
    return {"maths_object": maths_object}


def render_question(*, n, v, x):
    """[sujets0][gén][sujet-3][automatismes][question-5]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le volume $V(n)$ d\'un glacier diminue de $50\\\\%$ chaque année.  Exprimer $V(n + 1)$ en fonction de $V(n)$"
    """

    x = x.simplified()

    statement = f"Le volume ${v(n).latex()}$ d'un glacier diminue de ${x.as_percent.latex()}\\%$ chaque année.  Exprimer ${v(n + tm.Integer(n=1)).latex()}$ en fonction de ${v(n).latex()}$"
    statement_html = f"<div>{statement}</div>"
    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][gen][sujet-3][automatismes][question-5]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "mask": "",
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
            "v": components["v"].latex(),
            "x": components["x"].latex(),
        },
    }
)
