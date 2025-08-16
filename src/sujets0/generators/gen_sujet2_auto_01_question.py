import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# TODO: variabiliser sur le format


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> generate_components(None, 0)
    {'a': Fraction(p=Integer(n=-1), q=Integer(n=7)), 'b': Integer(n=-9), 'c': Fraction(p=Integer(n=15), q=Integer(n=8)), 'expr': Add(l=Fraction(p=Integer(n=-1), q=Integer(n=7)), r=Mul(l=Integer(n=-9), r=Fraction(p=Integer(n=15), q=Integer(n=8))))}
    """
    gen = tg.MathsGenerator(seed)

    a = gen.random_integer(-50, 50) / gen.random_integer(1, 10) 
    b = gen.random_integer(-50, 50) / gen.random_integer(1, 10)
    c = gen.random_integer(-50, 50) / gen.random_integer(1, 10)

    a = a.simplified()
    b = b.simplified()
    c = c.simplified()

    expr = a + b * c

    return {
        "a": a,
        "b": b,
        "c": c,
        "expr": expr,
    }


def solve(*, a, b, c, expr):
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Fraction(p=Integer(n=-1), q=Integer(n=7)), r=Mul(l=Integer(n=-9), r=Fraction(p=Integer(n=15), q=Integer(n=8))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-953), q=Integer(n=56))
    """
    maths_object = expr
    return {"maths_object": maths_object}


def render_question(*, a, b, c, expr):
    """[sujets0][gén][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Calculer $-\\\\dfrac{1}{7} -9\\\\dfrac{15}{8}$.'
    """


    statement = f"Calculer ${expr.latex()}$."
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
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "c": components["c"].latex(),
        },
    }
)


