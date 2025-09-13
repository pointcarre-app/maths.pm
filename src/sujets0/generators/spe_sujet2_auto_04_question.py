import random

import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> generate_components(None, 0)
    {'p1': Fraction(p=Integer(n=1), q=Integer(n=3)), 'p2': Fraction(p=Integer(n=1), q=Integer(n=3))}
    """

    gen = tg.MathsGenerator(seed)

    # Mixing of p and q in names careful : p cant  be name for both numerator and fraction

    # q1 = gen.random_integer(2, 4)
    # p1 = tm.Fraction(p=1, q=q1)
    # q2 = gen.random_integer(2, 4)
    # p2 = tm.Fraction(p=1, q=q2)

    q1 = random.choice([2, 4, 5])

    f1_tm = tm.Fraction(p=1, q=q1)

    q2 = random.choice([2, 4, 5])

    f2_tm = tm.Fraction(p=1, q=q2)

    return {
        "f1_tm": f1_tm,
        "f2_tm": f2_tm,
    }


def solve(*, f1_tm, f2_tm):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=1), q=Integer(n=3)), r=Fraction(p=Integer(n=1), q=Integer(n=3)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=9))
    """
    answer = f1_tm * f2_tm
    return {
        "maths_object": answer,
    }


def render_question(*, f1_tm, f2_tm):
    r"""[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Dans un lycée, le le tiers des élèves sont internes, parmi eux, le tiers sont des gauchers. Calculer le pourcentage de gauchers internes par rapport à l'ensemble des élèves du lycée."
    """

    # selfb : removed 1/3 to ensure proper exact decimals

    literal_proportions = {
        2: "la moitié",
        4: "le quart",
        5: "le cinquième",
    }

    statement = f"Dans un lycée, {literal_proportions[f1_tm.q.n]} des élèves sont internes, parmi eux, {literal_proportions[f2_tm.q.n]} sont des gauchers. Calculer le pourcentage d'élèves qui sont gauchers et internes par rapport à l'ensemble des élèves du lycée."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


statement_html = f"<div>{question['statement']}</div>"

missive_dict = {
    "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-4]",
    "statement": question["statement"],
    "statement_html": statement_html,
    "answer": {
        "latex": answer["maths_object"].latex(),
        "simplified_latex": [
            (answer["maths_object"] * tm.Integer(n=100)).simplified().latex().replace(".", ",")
            + "\%",
            (answer["maths_object"] * tm.Integer(n=100))
            .simplified()
            .as_decimal.latex()
            .replace(".", ",")
            + "\%",
        ],
        "sympy_exp_data": answer["maths_object"].sympy_expr_data,
        "formal_repr": repr(answer["maths_object"]),
    },
    "components": {
        "f1_tm": components["f1_tm"].latex(),
        "f2_tm": components["f2_tm"].latex(),
    },
}


try:
    missive(missive_dict)
except NameError:
    from pprint import pprint

    pprint(missive_dict)
# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])
# print("Simplified answer:", question["maths_object"].simplified())
# print("LaTeX representation:", question["maths_object"].latex())
