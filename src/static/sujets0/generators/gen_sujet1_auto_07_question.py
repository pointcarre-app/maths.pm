import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-7]
    >>> generate_components(None, 0)
    {'n1': Integer(n=6), 'n2': Integer(n=-4)}
    """

    gen = tg.MathsGenerator(seed)

    n1 = gen.random_integer(0, 10)
    n2 = gen.random_integer(-3, -1)

    return {
        "n1": n1,
        "n2": n2,
    }


def solve(*, n1, n2):
    """[sujets0][gén][sujet-1][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Integer(n=10), exp=Integer(n=6))
    """
    answer = tm.Integer(n=10) ** n1
    return {
        "maths_object": answer,
    }


def render_question(*, n1, n2):
    """[sujets0][gén][sujet-1][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Donner l\'arrondi de $10^{6} + 10^{-4}$ à l\'unité près, en utilisant l\'écriture scientifique."
    """
    expr = tm.Integer(n=10) ** n1 + tm.Integer(n=10) ** n2
    statement = f"Donner l'arrondi de ${expr.latex()}$ à l'unité près. Donner le résultat sous la forme d'un entier."
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
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-7]",
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


# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("LaTeX representation:", answer["maths_object"].latex())
