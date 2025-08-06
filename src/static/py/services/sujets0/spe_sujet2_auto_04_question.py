import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> generate_components(None, 0)
    {'p1': Fraction(p=Integer(n=1), q=Integer(n=3)), 'p2': Fraction(p=Integer(n=1), q=Integer(n=3))}
    """

    gen = tg.MathsGenerator(seed)

    q1 = gen.random_integer(2, 4)
    p1 = tm.Fraction(p=1, q=q1)
    q2 = gen.random_integer(2, 4)
    p2 = tm.Fraction(p=1, q=q2)

    return {
        "p1": p1,
        "p2": p2,
    }


def solve(*, p1, p2):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=1), q=Integer(n=3)), r=Fraction(p=Integer(n=1), q=Integer(n=3)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=9))
    """
    answer = p1 * p2
    return {
        "maths_object": answer,
    }


def render_question(*, p1, p2):
    r"""[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Dans un lycée, le le tiers des élèves sont internes, parmi eux, le tiers sont des gauchers. Calculer le pourcentage de gauchers internes par rapport à l'ensemble des élèves du lycée."
    """

    literal_proportions = {
        2: "la moitié",
        3: "le tiers",
        4: "le quart",
    }

    statement = f"Dans un lycée, le {literal_proportions[p1.q.n]} des élèves sont internes, parmi eux, {literal_proportions[p2.q.n]} sont des gauchers. Calculer le pourcentage de gauchers internes par rapport à l'ensemble des élèves du lycée."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-4]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p1": components["p1"].latex(),
            "p2": components["p2"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])
# print("Simplified answer:", question["maths_object"].simplified())
# print("LaTeX representation:", question["maths_object"].latex())
