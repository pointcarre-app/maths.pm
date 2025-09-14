import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-3]
    >>> generate_components(None, 0)
    {'a': Pow(base=Fraction(p=Integer(n=1), q=Integer(n=2)), exp=Integer(n=5)), 'b': Pow(base=Fraction(p=Integer(n=1), q=Integer(n=3)), exp=Integer(n=5)), 'c': Pow(base=Fraction(p=Integer(n=1), q=Integer(n=5)), exp=Integer(n=2)), 'd': Decimal(p=1, q=100)}
    """

    gen = tg.MathsGenerator(seed)
    a = tm.Fraction(p=1, q=2) ** gen.random_integer(2, 5)
    b = tm.Fraction(p=1, q=3) ** gen.random_integer(2, 5)
    c = tm.Fraction(p=1, q=5) ** gen.random_integer(2, 5)

    # NOTE: being smart to have a nice decimal
    q = tm.Integer(n=2) ** gen.random_integer(1, 3) * tm.Integer(n=5) ** gen.random_integer(1, 2)

    d = tm.Fraction(p=tm.Integer(n=1), q=q)

    d = d.as_decimal

    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
    }


def solve(*, a, b, c, d):
    """[sujets0][gén][sujet-1][automatismes][question-3]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Fraction(p=Integer(n=1), q=Integer(n=5)), exp=Integer(n=2))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=25))
    """

    maths_object = max(a, b, c, d, key=lambda x: x.eval())
    return {"maths_object": maths_object}


def render_question(*, a, b, c, d):
    """[sujets0][gén][sujet-1][automatismes][question-3]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Quel est le maximum parmi les nombres suivants: $A=\\\\left(\\\\dfrac{1}{2}\\\\right)^{5}$, $B=\\\\left(\\\\dfrac{1}{3}\\\\right)^{5}$, $C=\\\\left(\\\\dfrac{1}{5}\\\\right)^{2}$, $D=0,01$'
    """

    statement = f"""Quel est le maximum parmi les nombres suivants : <br>$A={a.latex()}$, $B={b.latex()}$, $C={c.latex()}$, $D={d.latex().replace(".", ",")}$"""
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
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-3]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "c": components["c"].latex(),
            "d": components["d"].latex(),
        },
    }
)
