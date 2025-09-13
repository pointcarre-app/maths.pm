###############################################################################
# NOTE : exactly the same as [sujets0][spé][sujet-2][automatismes][question-3]
###############################################################################


import random
import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


# TODO selfb: discuss
# For p = 10:

# Formula: -100 × (10/100)² = -100 × 0.01 = -1%
# Verification: 1.10 × 0.90 = 0.99 → -1%

# For p = 20:

# Formula: -100 × (20/100)² = -100 × 0.04 = -4%
# Verification: 1.20 × 0.80 = 0.96 → -4%

# For p = 50:

# Formula: -100 × (50/100)² = -100 × 0.25 = -25%
# Verification: 1.50 × 0.50 = 0.75 → -25%


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-3]
    >>> generate_components(None, 0)
    {'p': Integer(n=65), 'direction': Integer(n=1)}
    """
    gen = tg.MathsGenerator(seed)
    p = random.choice([tm.Integer(n=10), tm.Integer(n=20), tm.Integer(n=50)])

    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    return {"p": p, "direction": direction}


# TODO selfb: compare to exercices grom spe_sujet_1 avec retours


def solve(*, p, direction):
    """[sujets0][spé][sujet-2][automatismes][question-3]
    >>> answer = solve(p=tm.Integer(n=65), direction=tm.Integer(n=1))
    >>> answer["maths_object"]
    Mul(l=Integer(n=-100), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-4225), q=Integer(n=100))
    """
    maths_object = -tm.Integer(n=100) * ((p / tm.Integer(n=100)) ** tm.Integer(n=2))
    return {"maths_object": maths_object}


# def solve(*, p, direction):
#     """[sujets0][spé][sujet-2][automatismes][question-3]
#     >>> answer = solve(p=tm.Integer(n=65), direction=tm.Integer(n=1))
#     >>> answer["maths_object"]
#     Mul(l=Integer(n=-1), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
#     >>> answer["maths_object"].simplified()
#     Fraction(p=Integer(n=-169), q=Integer(n=400))
#     """
#     maths_object = -((p / tm.Integer(n=100)) ** tm.Integer(n=2))
#     return {"maths_object": maths_object}


def render_question(*, p, direction):
    r"""[sujets0][spé][sujet-2][automatismes][question-3]
    >>> p = tm.Integer(n=65)
    >>> direction = tm.Integer(n=1)
    >>> statement = render_question(p=p, direction=direction)
    >>> statement["statement"]
    "Le prix d'un article est noté $P$. Ce prix augmente de $65\\%$ puis diminue de $65\\%$. A l'issue de ces deux variations, quel est le pourcentage d'évolution ?"
    """
    if direction == -1:
        dir1, dir2 = "diminue", "augmente"
    else:
        dir1, dir2 = "augmente", "diminue"

    statement = f"""Le prix d'un article est noté $P$. Ce prix {dir1} de ${p.latex()}\\%$ puis {dir2} de ${p.latex()}\\%$. À l'issue de ces deux variations, quel est le pourcentage d'évolution ?"""

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# # Create HTML version - same as sujet1 question 4
# if components["direction"].n == -1:
#     dir1, dir2 = "diminue", "augmente"
# else:
#     dir1, dir2 = "augmente", "diminue"

statement_html = f"<div>{question['statement']}</div>"


missive_dict = {
    "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-3]",
    "statement": question["statement"],
    "statement_html": statement_html,
    "answer": {
        "latex": [answer["maths_object"].latex()],
        "simplified_latex": answer["maths_object"].simplified().latex() + " \\% ",
        "sympy_exp_data": answer["maths_object"].sympy_expr_data,
        "formal_repr": repr(answer["maths_object"]),
    },
    "components": {
        "p": components["p"].latex(),
        "direction": components["direction"].latex(),
    },
}


try:
    missive(missive_dict)
except NameError:
    from pprint import pprint

    pprint(missive_dict)
