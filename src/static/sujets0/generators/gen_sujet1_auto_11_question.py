import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-11]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'a': Integer(n=9), 'b': Integer(n=-8)}
    """

    gen = tg.MathsGenerator(seed)
    a = tm.Integer(n=0)
    b = tm.Integer(n=0)
    while a.n == 0 or b.n == 0:
        a = gen.random_integer(-9, 9)
        b = gen.random_integer(-9, 9)

    x = tm.Symbol(s="x")

    return {
        "x": x,
        "a": a,
        "b": b,
    }


def solve(*, x, a, b):
    """[sujets0][gén][sujet-1][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Add(l=Mul(l=Integer(n=3), r=Symbol(s='x')), r=Integer(n=4)), exp=Integer(n=2))
    >>> answer["maths_object"].simplified()
    Add(l=Add(l=Mul(l=Integer(n=9), r=Pow(base=Symbol(s='x'), exp=Integer(n=2))), r=Mul(l=Integer(n=24), r=Symbol(s='x'))), r=Integer(n=16))
    """
    maths_object = (a*x + b) ** tm.Integer(n=2)
    return {"maths_object": maths_object}


def render_question(*, x, a, b):
    """[sujets0][gén][sujet-1][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Développer $\\\\left(3x + 4\\\\right)^{2}$'
    """
    expr = (a*x + b) ** tm.Integer(n=2)


    statement = f"Développer ${expr.latex()}$"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-11]",
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
