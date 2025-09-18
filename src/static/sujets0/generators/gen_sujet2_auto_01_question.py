import random
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

    a = 0
    while a == 0:  # consistent with pm objects ?
        num_a = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )
        denom_a = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )

        a = num_a / denom_a

    b = 0
    while b == 0:
        num_b = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )

        denom_b = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )
        b = num_b / denom_b

    c = 0
    while c == 0:
        num_c = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )

        denom_c = random.choice(
            [
                tm.Integer(n=1),
                tm.Integer(n=2),
                tm.Integer(n=3),
                tm.Integer(n=4),
                tm.Integer(n=5),
                tm.Integer(n=10),
            ]
        )
        c = num_c / denom_c

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
    statement_html = f"<div>{statement}</div>"
    return {
        "statement": statement,
        "statement_html": statement_html,
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
        "statement_html": question["statement_html"],
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
