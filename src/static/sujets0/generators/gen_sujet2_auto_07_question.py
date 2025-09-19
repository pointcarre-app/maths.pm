import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> generate_components(None, 0)
    {'a': Fraction(p=Integer(n=-2), q=Integer(n=10)), 'x1': Integer(n=3), 'y1': Integer(n=-2), 'x2': Integer(n=-9)}
    """

    gen = tg.MathsGenerator(seed)

    a = gen.random_integer(-20, 20) / tm.Integer(n=10)
    x1 = gen.random_integer(-10, 10)
    x2 = gen.random_integer(-10, 10)

    # Ensure x2 ≠ x1 to avoid division by zero
    while x2.n == x1.n:
        x2 = gen.random_integer(-100, 100)

    y1 = gen.random_integer(-10, 10)

    return {
        "a": a,
        "x1": x1,
        "y1": y1,
        "x2": x2,
    }


def solve(*, a, x1, y1, x2):
    """[sujets0][gén][sujet-2][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Integer(n=-2), r=Mul(l=Add(l=Integer(n=-9), r=Integer(n=-3)), r=Fraction(p=Integer(n=-2), q=Integer(n=10))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=2), q=Integer(n=5))
    """
    # Because of this line, x1 and x2 Must different
    maths_object = y1 + (x2 - x1) * a
    return {
        "maths_object": maths_object,
    }


def render_question(*, a, x1, y1, x2):
    """[sujets0][gén][sujet-2][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le plan est muni d\'un repère orthogonal. On note $d$ la droite de coeffcient directeur -0,2 passant par le points $A(3;-2)$. On note $B$ le point de la droite $d$ d'abscisse $-9$. Calculer l\'ordonnée de $B$."
    """

    statement = f"Le plan est muni d'un repère orthogonal. On note $d$ la droite de coeffcient directeur ${a.as_decimal.latex().replace('.', ',')}$ (= ${a.simplified().latex()}$) passant par le points $A({x1.latex()};{y1.latex()})$. On note $B$ le point de la droite $d$ d'abscisse ${x2.latex()}$. Calculer l'ordonnée de $B$."
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
            "a": components["a"].latex(),
            "x1": components["x1"].latex(),
            "y1": components["y1"].latex(),
            "x2": components["x2"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])
# print("Simplified answer:", question["maths_object"].simplified())
# print("LaTeX representation:", question["maths_object"].latex())
