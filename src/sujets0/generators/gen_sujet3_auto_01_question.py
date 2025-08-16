import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict:
    """[1ere][sujets0][gén][sujet-3][automatismes][question-1]
    >>> generate_components(None, 0)
    {'a': Decimal(p=99990, q=1), 'b': Decimal(p=99000, q=1), 'n1': Integer(n=5), 'n2': Integer(n=5), 'n3': Integer(n=1), 'n4': Integer(n=3), 'expr': Mul(l=Decimal(p=99990, q=1), r=Decimal(p=99000, q=1))}
    """
    gen = tg.MathsGenerator(seed)

    n1 = gen.random_integer(2, 5)
    n2 = gen.random_integer(2, 5)
    n3 = gen.random_integer(1, n1.n - 1)
    n4 = gen.random_integer(1, n2.n - 1)
    a = tm.Integer(n=10) ** n1 - tm.Integer(n=10) ** n3
    b = tm.Integer(n=10) ** n2 - tm.Integer(n=10) ** n4

    a = a.simplified().as_decimal
    b = b.simplified().as_decimal

    expr = a * b


    return {
        "a": a,
        "b": b,
        "n1": n1,
        "n2": n2,
        "n3": n3,
        "n4": n4,
        "expr" : expr
    }


def solve(*, a, b, n1, n2, n3, n4, expr):
    """[1ere][sujets0][gén][sujet-3][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Integer(n=10), exp=Integer(n=10))
    >>> answer["maths_object"].simplified()
    Integer(n=10000000000)
    """
    maths_object = tm.Integer(n=10) ** (n1 + n2).simplified()

    # maths_object = a

    return {"maths_object": maths_object}


def render_question(*,  a, b, n1, n2, n3, n4, expr):
    """[1ere][sujets0][gén][sujet-3][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> question = render_question(**components)
    >>> question["statement"]
    "Donner l\'ordre de grandeur de $99990 \\\\times 99000$."
    """

    statement = f"Donner l'ordre de grandeur de ${expr.latex()}$."

    return {
        "statement": statement,
    }



components = generate_components(None)
answer = solve(**components)
question = render_question(**components)

missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-3][automatismes][question-1]",
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
            "n1": components["n1"].latex(),
            "n2": components["n2"].latex(),
            "n3": components["n3"].latex(),
            "n4": components["n4"].latex(),
            "expr" : components["expr"].latex(),
        },
    }
)
