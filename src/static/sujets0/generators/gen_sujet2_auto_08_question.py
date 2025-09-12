import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-08]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'a1': Integer(n=9), 'a2': Integer(n=-8), 'b1': Integer(n=4), 'b2': Integer(n=6), 'expr': Mul(l=Add(l=Mul(l=Integer(n=9), r=Symbol(s='x')), r=Integer(n=4)), r=Add(l=Mul(l=Integer(n=-8), r=Symbol(s='x')), r=Integer(n=6)))}
    """

    gen = tg.MathsGenerator(seed)

    a1 = tm.Integer(n=0)
    a2 = tm.Integer(n=0)

    while a1.n == 0 or a2.n == 0 or b1.n == 0 or b2.n == 0:
        a1 = gen.random_integer(-9, 9)
        a2 = gen.random_integer(-9, 9)
        b1 = gen.random_integer(-9, 9)
        b2 = gen.random_integer(-9, 9)

    x = tm.Symbol(s="x")

    expr = (a1 * x + b1) * (a2 * x + b2)

    return {
        "x": x,
        "a1": a1,
        "a2": a2,
        "b1": b1,
        "b2": b2,
        "expr": expr,
    }


def solve(*, x, a1, a2, b1, b2, expr):
    """[sujets0][gén][sujet-2][automatismes][question-08]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Mul(l=Integer(n=12), r=Pow(base=Symbol(s='x'), exp=Integer(n=2))), r=Add(l=Mul(l=Integer(n=-35), r=Symbol(s='x')), r=Integer(n=8)))
    >>> answer["maths_object"].simplified()
    Add(l=Mul(l=Integer(n=12), r=Pow(base=Symbol(s='x'), exp=Integer(n=2))), r=Add(l=Mul(l=Integer(n=-35), r=Symbol(s='x')), r=Integer(n=8)))
    """
    maths_object = expr.simplified()
    maths_object = tm.group_terms(maths_object)
    return {"maths_object": maths_object}


def render_question(*, x, a1, a2, b1, b2, expr):
    """[sujets0][gén][sujet-2][automatismes][question-08]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Dévelloper $\\\\left(3x -8\\\\right) \\\\times \\\\left(4x -1\\\\right)$.'
    """

    statement = f"Développer ${expr.latex()}$."
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-08]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "a1": components["a1"].latex(),
            "b1": components["b1"].latex(),
            "a2": components["a2"].latex(),
            "b2": components["b2"].latex(),
            "expr": components["expr"].latex(),
        },
    }
)
