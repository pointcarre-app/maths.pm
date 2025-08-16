import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-11]
    >>> generate_components(None, 10)
    {'f': Function(name=f), 'x': Symbol(s='x'), 'a': Integer(n=4), 'b': Integer(n=-20), 'c': Integer(n=24), 'x1': Integer(n=2), 'x2': Integer(n=3), 'expr': Add(l=Add(l=Mul(l=Integer(n=4), r=Pow(base=Symbol(s='x'), exp=Integer(n=2))), r=Mul(l=Integer(n=-20), r=Symbol(s='x'))), r=Integer(n=24))}
    """

    gen = tg.MathsGenerator(seed)

    x1 = gen.random_integer(-2, 2)
    x2 = gen.random_integer(3, 10)

    a = tm.Integer(n=0)

    while a.n == 0 :
        a = gen.random_integer(-9, 9)

    x = tm.Symbol(s='x')

    b = - a * (x1 + x2)
    b = b.simplified()

    c = a * x1 * x2
    c = c.simplified()

    expr = a * x ** tm.Integer(n=2) + b * x + c

    f = tm.Function(name="f")

    return {
        "f": f,
        "x": x,
        "a": a,
        "b": b,
        "c": c,
        "x1": x1,
        "x2": x2,
        "expr": expr,
    }


def solve(*, a, b, c, x, x1, x2, f, expr):
    """[sujets0][gén][sujet-2][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=1)
    >>> answer["maths_object"].simplified()
    Integer(n=1)
    """
    maths_object = x1
    return {"maths_object": maths_object}


def render_question(*, a, b, c, x, x1, x2, f, expr):
    """[sujets0][gén][sujet-2][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Soit $f$ une fonction définie sur $\\\\mathbb{R}$ par $f(x) = -8 \\\\times x^{2} + 80x -72$. Parmis la série A: -2; -1, 0, 1, 2, quel est l\'antécédent de 0 par la fonction $f$ ?"
    """

    statement = f"Soit ${f.latex()}$ une fonction définie sur $\\mathbb{{R}}$ par ${f.latex()}({x.latex()}) = {expr.latex()}$. Parmis la série A: -2; -1, 0, 1, 2, quel est l'antécédent de 0 par la fonction $f$ ?"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-11]",
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
            "c": components["c"].latex(),
            "x1": components["x1"].latex(),
            "x2": components["x2"].latex(),
            "expr": components["expr"].latex(),
            "f": components["f"].latex(),
        },
    }
)
