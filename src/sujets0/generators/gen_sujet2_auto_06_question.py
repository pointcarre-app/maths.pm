import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> generate_components(None, 0)
    {'x1': Integer(n=-2), 'y1': Integer(n=7), 'x2': Integer(n=94), 'y2': Integer(n=-90)}
    """

    gen = tg.MathsGenerator(seed)

    x1 = gen.random_integer(-10, 10)
    x2 = gen.random_integer(-10, 10)

    # Ensure x2 ≠ x1 to avoid division by zero
    while x2.n == x1.n:
        x2 = gen.random_integer(-10, 10)

    y1 = gen.random_integer(-20, 20)
    y2 = gen.random_integer(-20, 20)

    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
    }


def solve(*, x1, y1, x2, y2):
    """[sujets0][gén][sujet-2][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Add(l=Integer(n=-90), r=Integer(n=-7)), q=Add(l=Integer(n=94), r=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-97), q=Integer(n=96))
    """
    answer = (y2 - y1) / (x2 - x1)
    return {
        "maths_object": answer,
    }


def render_question(*, x1, y1, x2, y2):
    r"""[sujets0][gén][sujet-2][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le plan est muni d'un repère orthogonal. On note $d$ la droite passant par les points $A(-2;7)$ et $B(94;-90)$. Calculer le coefficient directeur de la droite $d$."
    """

    statement = f"Le plan est muni d'un repère orthogonal. On note $d$ la droite passant par les points $A({x1.latex()};{y1.latex()})$ et $B({x2.latex()};{y2.latex()})$. Calculer le coefficient directeur de la droite $d$."
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-7]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x1": components["x1"].latex(),
            "y1": components["y1"].latex(),
            "x2": components["x2"].latex(),
            "y2": components["y2"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])
# print("Simplified answer:", question["maths_object"].simplified())
# print("LaTeX representation:", question["maths_object"].latex())
