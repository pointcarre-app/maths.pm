import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict:
    """[1ere][sujets0][gén][sujet-1][automatismes][question-5]
    >>> generate_components(None, 0)
    {'n1': Integer(n=3), 'n2': Integer(n=3)}
    """
    gen = tg.MathsGenerator(seed)

    n1 = gen.random_integer(2, 4)
    n2 = gen.random_integer(2, 4)

    return {
        "n1": n1,
        "n2": n2,
    }


def solve(*, n1: tm.Integer, n2: tm.Integer):
    """[1ere][sujets0][gén][sujet-1][automatismes][question-5]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=1), q=Mul(l=Integer(n=3), r=Integer(n=3)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=9))
    """
    maths_object = tm.Fraction(p=tm.Integer(n=1), q=n1 * n2)

    return {"maths_object": maths_object}


def render_question(*, n1: tm.Integer, n2: tm.Integer):
    """[1ere][sujets0][gén][sujet-1][automatismes][question-5]
    >>> components = generate_components(None, 0)
    >>> question = render_question(**components)
    >>> question["statement"]
    "Calculer le tiers d\'un tiers ?"
    """
    literal_inverse_n1 = {
        2: "la moitié",
        3: "le tiers",
        4: "le quart",
    }
    literal_inverse_n2 = {
        2: "d'une moitié",
        3: "d'un tiers",
        4: "d'un quart",
    }

    statement = f"Quelle fraction représente {literal_inverse_n1[n1.n]} {literal_inverse_n2[n2.n]} ?<br><span class='italic'>Note : le cinquième de la moitié est représenté par la fraction $\\dfrac{{1}}{{10}}$.</span>"
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)

missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-5]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n1": components["n1"].latex(),
            "n2": components["n2"].latex(),
        },
    }
)
