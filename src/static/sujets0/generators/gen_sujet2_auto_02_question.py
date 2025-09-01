import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> generate_components(None, 1)
    {'n1': Integer(n=3), 'n2': Integer(n=9), 'p': Fraction(p=Integer(n=146), q=Integer(n=10))}
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
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components= generate_components(None, 1)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=146), q=Integer(n=10)), r=Integer(n=9))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=657), q=Integer(n=5))
    """
    maths_object = p * n2
    return {
        "maths_object": maths_object,
    }


def render_question(*, n1, n2, p):
    r"""[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components= generate_components(None, 1)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    '3 articles coûtent 43,8 euros. Combien coûtent 9 articles ?'
    """

    p1 = (p * n1).simplified().as_decimal

    statement = (
        f"{n1.latex()} articles coûtent {p1.latex()} euros. Combien coûtent {n2.latex()} articles ?"
    )
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-2]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
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
