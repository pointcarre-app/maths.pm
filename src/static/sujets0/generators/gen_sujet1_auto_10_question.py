import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-10]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'x0': Integer(n=9), 'f': Function(name=f), 'a': Integer(n=9), 'b': Fraction(p=Integer(n=-8), q=Integer(n=8)), 'c': Integer(n=7)}
    """

    gen = tg.MathsGenerator(seed)

    a = tm.Integer(n=0)
    p = tm.Integer(n=0)
    while a.n == 0 or p.n == 0:
        a = gen.random_integer(-9, 9)
        p = gen.random_integer(-9, 9)
    
    c = gen.random_integer(1, 9)
    q = gen.random_integer(1, 9)

    b = tm.Fraction(p=p, q=q)
    x = tm.Symbol(s="x")
    x0 = gen.random_integer(-9, 9)

    f = tm.Function(name="f")

    return {
        "x": x,
        "x0": x0,
        "f": f,
        "a": a,
        "b": b,
        "c": c,
    }


def solve(*, x, f, x0, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Integer(n=3), r=Mul(l=Fraction(p=Integer(n=4), q=Integer(n=5)), r=Pow(base=Add(l=Integer(n=7), r=Integer(n=-1)), exp=Integer(n=2))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=159), q=Integer(n=5))
    """
    maths_object = a + b*(x0-c) ** tm.Integer(n=2)
    return {"maths_object": maths_object}


def render_question(*, x, x0, f, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "On définit la function $f$ par $f(x)=3 + \\\\dfrac{4}{5}\\\\left(x -1\\\\right)^{2}$. Calculer l'image de $7$ par $f$."
    """
    expr = a + b*(x-c) ** tm.Integer(n=2)


    statement = f"On définit la function ${f.latex()}$ par ${f(x).latex()}={expr.latex()}$. Calculer l'image de ${x0.latex()}$ par ${f.latex()}$."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-10]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "f": components["f"].latex(),
            "x0": components["x0"].latex(),
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "c": components["c"].latex(),
        },
    }
)
