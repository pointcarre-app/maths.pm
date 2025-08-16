import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-10]
    >>> generate_components(None, 10)
    {'x': Symbol(s='x'), 'x0': Integer(n=6), 'f': Function(name=f), 'a': Integer(n=9), 'b': Integer(n=-8), 'c': Integer(n=4)}
    """

    gen = tg.MathsGenerator(seed)

    a = tm.Integer(n=0)
    b = tm.Integer(n=0)
    c = tm.Integer(n=0)
    while a.n == 0 or b.n == 0 or c.n == 0:
        a = gen.random_integer(-9, 9)
        b = gen.random_integer(-9, 9)
        c = gen.random_integer(-9, 9)
    
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
    """[sujets0][gén][sujet-2][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Add(l=Mul(l=Integer(n=3), r=Pow(base=Integer(n=-1), exp=Integer(n=2))), r=Mul(l=Integer(n=4), r=Integer(n=-1))), r=Integer(n=-8))
    >>> answer["maths_object"].simplified()
    Integer(n=-9)
    """
    maths_object = a * x0 ** tm.Integer(n=2) + b * x0 + c
    return {"maths_object": maths_object}


def render_question(*, x, x0, f, a, b, c):
    """[sujets0][gén][sujet-2][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "On définit la function $f$ par $f(x)=3 \\\\times x^{2} + 4x -8$. Calculer l\'image de $-1$ par $f$."
    """

    expr = a * x ** tm.Integer(n=2) + b * x + c


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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-10]",
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
