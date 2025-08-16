# ruff: noqa : E402


import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED



def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-3][automatismes][question-3]
    >>> generate_components(None, 0)
    {'p': Fraction(p=Integer(n=865), q=Integer(n=1000)), 'direction': Integer(n=1), 'coef': Add(l=Integer(n=1), r=Mul(l=Integer(n=1), r=Fraction(p=Integer(n=865), q=Integer(n=1000))))}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 1000)
    p = tm.Fraction(p=p, q=1000)
    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    coef = tm.Integer(n=1) + direction * p

    return {
        "p": p,
        "direction": direction,
        "coef": coef,
    }


def solve(*, p, direction, coef):
    """[sujets0][spé][sujet-3][automatismes][question-3]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Decimal(p=373, q=200)
    >>> answer["maths_object"].simplified()
    Decimal(p=373, q=200)
    """
    maths_object = coef.simplified().as_decimal
    return {"maths_object": maths_object}


def render_question(*, p, direction, coef):
    """[sujets0][spé][sujet-3][automatismes][question-3]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Par combien faut-il multiplier une quantité positive pour que celle-ci augmente de $86,5\\\\%$ ?'
    """
    literal_direction = {
        -1: "diminue",
        1: "augmente",
    }

    statement = f"Par combien faut-il multiplier une quantité positive pour que celle-ci {literal_direction[direction.n]} de ${p.as_percent.latex()}\\%$ ?"
    return {
        "statement": statement,
    }



components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-3][automatismes][question-3]",
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
