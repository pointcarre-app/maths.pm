import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict:
    """[1ere][sujets0][gén][sujet-1][automatismes][question-6]
    >>> generate_components(None, 0)
    {'a': Pow(base=Integer(n=10), exp=Integer(n=4)), 'b': Decimal(p=1, q=10000), 'c': Fraction(p=Integer(n=1), q=Integer(n=10))}
    """
    gen = tg.MathsGenerator(seed)

    n1 = gen.random_integer(1, 4)
    n2 = gen.random_integer(1, 4)
    n3 = gen.random_integer(1, 4)

    a = tm.Integer(n=10) ** n1
    b = tm.Integer(n=10) ** (-n2)
    c = tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=10) ** (n3))
    
    b = b.simplified().as_decimal
    c = c.simplified()

    return {
        "a": a,
        "b": b,
        "c": c,
    }


def solve(*, a, b, c):
    """[1ere][sujets0][gén][sujet-1][automatismes][question-6]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Add(l=Pow(base=Integer(n=10), exp=Integer(n=4)), r=Decimal(p=1, q=10000)), r=Fraction(p=Integer(n=1), q=Integer(n=10)))
    >>> answer["maths_object"].simplified()
    Decimal(p=1000010010, q=100000)
    """
    maths_object = a + b + c
    # maths_object = a

    return {"maths_object": maths_object}


def render_question(*, a, b, c):
    """[1ere][sujets0][gén][sujet-1][automatismes][question-6]
    >>> components = generate_components(None, 0)
    >>> question = render_question(**components)
    >>> question["statement"]
    'Calculer $10^{4} + 0,0001 + \\\\dfrac{1}{10}$.'
    """

    expr = a + b + c

    statement = f"Calculer ${expr.latex()}$."

    return {
        "statement": statement,
    }



components = generate_components(None)
answer = solve(**components)
question = render_question(**components)

missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-6]",
        "statement": question["statement"],
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
