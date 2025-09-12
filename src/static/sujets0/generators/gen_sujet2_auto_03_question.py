import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-3]
    >>> generate_components(None, 0)
    {'n': Integer(n=5)}
    """

    gen = tg.MathsGenerator(seed)

    n = gen.random_integer(2, 5)

    return {
        "n": n,
    }


def solve(*, n):
    """[sujets0][gén][sujet-2][automatismes][question-3]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=400)
    >>> answer["maths_object"].simplified()
    Integer(n=400)
    """
    maths_object = (n - tm.Integer(n=1)).simplified().as_percent
    return {
        "maths_object": maths_object,
    }


def render_question(*, n):
    r"""[sujets0][gén][sujet-2][automatismes][question-3]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le prix d'un article a quintuplé. Calculer la variation relative $V_r$."
    """

    literal_n = {
        2: "doublé",
        3: "triplé",
        4: "quadruplé",
        5: "quintuplé",
    }

    statement = f"Le prix d'un article a {literal_n[n.n]}. Calculer la variation relative $V_r$."
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-3]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": [answer["maths_object"].latex()],
            "simplified_latex": [answer["maths_object"].simplified().latex() + " \\%"],
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
        },
    }
)
