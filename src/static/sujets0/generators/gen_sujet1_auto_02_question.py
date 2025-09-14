import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-2]
    >>> generate_components(None, 0)
    {'a': Fraction(p=Integer(n=13), q=Integer(n=20)), 'b': Fraction(p=Integer(n=98), q=Integer(n=100)), 'c': Decimal(p=54, q=100)}
    """

    gen = tg.MathsGenerator(seed)
    a = tm.Fraction(p=tm.Integer(n=5) * gen.random_integer(1, 20), q=tm.Integer(n=100))
    b = tm.Fraction(p=gen.random_integer(1, 100), q=tm.Integer(n=100))
    c = tm.Fraction(p=gen.random_integer(1, 100), q=tm.Integer(n=100))

    a = a.simplified()
    c = c.as_decimal

    return {
        "a": a,
        "b": b,
        "c": c,
    }


def solve(*, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=98), q=Integer(n=100))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=49), q=Integer(n=50))
    """

    maths_object = max(a, b, c, key=lambda x: x.eval())
    return {"maths_object": maths_object}


def render_question(*, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Quel est le maximum parmis les nombres suivants: $A=\\\\dfrac{13}{20}$, $B=\\\\dfrac{98}{100}$, $C=0,54$'
    """

    statement = f"""Quel est le maximum parmi les nombres suivants :<br>$A={a.latex()}$ ; $B={b.latex()}$ ; $C={c.latex().replace(".", ",")}$"""
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
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-2]",
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
        },
    }
)
