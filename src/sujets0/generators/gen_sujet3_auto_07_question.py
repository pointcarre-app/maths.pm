import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-3][automatismes][question-7]
    >>> generate_components(None, 4)
    {'n1': Integer(n=4), 'n2': Integer(n=13), 'p': Fraction(p=Integer(n=78), q=Integer(n=10))}
    """

    gen = tg.MathsGenerator(seed)

    n1 = gen.random_integer(1, 10)
    p = gen.random_integer(1, 200) / tm.Integer(n=10)
    n2 = tm.Integer(n=n1.n)
    while n2.n == n1.n:
        n2 = gen.random_integer(1, 20)

    return {
        "n1": n1,
        "n2": n2,
        "p": p,
    }


def solve(*, n1, n2, p):
    """[sujets0][gén][sujet-3][automatismes][question-7]
    >>> components= generate_components(None, 4)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=78), q=Integer(n=10)), r=Integer(n=13))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=507), q=Integer(n=5))
    """
    maths_object = (p * n2)
    return {
        "maths_object": maths_object,
    }


def render_question(*, n1, n2, p):
    r"""[sujets0][gén][sujet-3][automatismes][question-7]
    >>> components= generate_components(None, 4)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    '4 articles coûtent 31,2 euros. Combien coûtent 13 articles ?'
    """

    p1 = (p * n1).simplified().as_decimal

    statement = f"{n1.latex()} articles coûtent {p1.latex()} euros. Combien coûtent {n2.latex()} articles ?"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-3][automatismes][question-7]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n1": components["n1"].latex(),
            "n2": components["n2"].latex(),
            "p": components["p"].latex(),
        },
    }
)
