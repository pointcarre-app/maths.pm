# ruff: noqa : E402


import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# TODO: variabiliser sur le format


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> generate_components(None, 0)
    {'p': Fraction(p=Integer(n=99), q=Integer(n=200)), 'direction': Integer(n=1), 'coef': Add(l=Integer(n=1), r=Mul(l=Integer(n=1), r=Fraction(p=Integer(n=99), q=Integer(n=200))))}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 200)
    p = tm.Fraction(p=p, q=200)
    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    coef = tm.Integer(n=1) + direction * p

    return {
        "p": p,
        "direction": direction,
        "coef": coef,
    }


def solve(*, p, direction, coef):
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> answer = solve(p=tm.Fraction(p=99, q=200), direction=1, coef=tm.Fraction(p=299, q=200))
    >>> answer["maths_object"]
    Fraction(p=Integer(n=99), q=Integer(n=200))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=99), q=Integer(n=200))
    """
    maths_object = p
    return {"maths_object": maths_object}


def render_question(*, p, direction, coef):
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> p = tm.Fraction(p=99, q=200)
    >>> direction = tm.Integer(n=1)
    >>> coef = tm.Fraction(p=299, q=200)
    >>> statement = render_question(p=p, direction=direction, coef=coef)
    >>> statement["statement"]
    "Le prix d'un article est multiplié par $1,495$. De combien de pourcent le prix de cet article a-t-il augmenté ?"
    """
    literal_direction = {
        -1: "diminué",
        1: "augmenté",
    }

    # was : coef.simplified().latex
    coef = coef.simplified().as_decimal
    statement = f"Le prix d'un article est multiplié par ${coef.latex()}$. De combien de pourcent le prix de cet article a-t-il {literal_direction[direction.n]} ?"
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


# print(
#     {
#         "statement": question["statement"],
#         "answer": answer["maths_object"].latex(),
#         "p": components["p"].latex(),
#         "direction": components["direction"].latex(),
#         "coef": components["coef"].latex(),
#     }
# )

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-3]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p": components["p"].latex(),
            "direction": components["direction"].latex(),
            "coef": components["coef"].latex(),
        },
    }
)
