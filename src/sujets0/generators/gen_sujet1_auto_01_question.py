import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# TODO: variabiliser sur le format


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> generate_components(None, 0)
    {'n': Integer(n=250), 'x': Fraction(p=Integer(n=14), q=Integer(n=20))}
    """
    gen = tg.MathsGenerator(seed)

    n = gen.random_integer(1, 50) * tm.Integer(n=10)
    n = n.simplified()
    x = gen.random_integer(1, 20)
    x = tm.Fraction(p=x, q=20)

    return {
        "n": n,
        "x": x,
    }


def solve(*, n, x):
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=14), q=Integer(n=20)), r=Integer(n=250))
    >>> answer["maths_object"].simplified()
    Integer(n=175)
    """
    maths_object = x * n
    return {"maths_object": maths_object}


def render_question(*, n, x):
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Calculer $70 \\\\%$ de $250$.'
    """

    x = x.simplified()

    statement = f"Calculer ${x.as_percent.latex()} \\%$ de ${n.latex()}$."
    return {
        "statement": statement,
    }


# def correct():
#     r"""
#     >>> import teachers.corrector as tc
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex=r"49,5"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][gen][sujet-2][automatismes][question-2]",
        "statement": question["statement"],
        "mask": "",
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
            "x": components["x"].latex(),
        },
    }
)


