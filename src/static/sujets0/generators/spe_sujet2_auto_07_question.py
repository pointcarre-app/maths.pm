import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-7]
    >>> generate_components(None, 0)
    {'x1': Integer(n=2), 'y1': Integer(n=-9), 'x2': Integer(n=3), 'y2': Integer(n=-2)}
    """

    gen = tg.MathsGenerator(seed)

    x1 = gen.random_integer(-10, 10)
    x2 = gen.random_integer(-10, 10)
    # Ensure x1 != x2 to avoid division by zero (vertical line)
    while x2 == x1:
        x2 = gen.random_integer(-10, 10)
    y1 = gen.random_integer(-10, 10)
    y2 = gen.random_integer(-10, 10)

    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
    }


def solve(*, x1, y1, x2, y2):
    """[sujets0][spé][sujet-1][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Add(l=Integer(n=-2), r=Integer(n=9)), q=Add(l=Integer(n=3), r=Integer(n=-2)))
    >>> answer["maths_object"].simplified()
    Integer(n=7)
    """
    answer = (y2 - y1) / (x2 - x1)
    return {
        "maths_object": answer,
    }


def render_question(*, x1, y1, x2, y2):
    r"""[sujets0][spé][sujet-1][automatismes][question-7]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le plan est muni d'un repère orthogonal. On note $d$ la droite passant par les points $A(2;-9)$ et $B(3;-2)$. Calculer le coefficient directeur de la droite $d$."
    """

    statement = f"Le plan est muni d'un repère orthogonal. On note $d$ la droite passant par les points $A({x1.latex()};{y1.latex()})$ et $B({x2.latex()};{y2.latex()})$. Calculer le coefficient directeur de la droite $d$."
    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with points table
statement_html = f"""
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            Le plan est muni d'un repère orthogonal. On note $d$ la droite passant par les points :
        </div>
        <div class="overflow-x-auto">
            <table class="table table-compact w-full">
                <thead>
                    <tr>
                        <th class="text-center">Point</th>
                        <th class="text-center">Coordonnées</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-center font-mono">$A$</td>
                        <td class="text-center">$({x1.latex()} ; {y1.latex()})$</td>
                    </tr>
                    <tr>
                        <td class="text-center font-mono">$B$</td>
                        <td class="text-center">$({x2.latex()} ; {y2.latex()})$</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Calculer le coefficient directeur de la droite $d$.
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-7]",
        "statement": question["statement"],
        "statement_html": statement_html,
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
