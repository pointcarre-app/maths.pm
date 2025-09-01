import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-4]
    >>> generate_components(None, 0)
    {'p0': Integer(n=70), 'p1': Integer(n=77), 'x': Fraction(p=Integer(n=1), q=Integer(n=10)), 'direction': Integer(n=1)}
    """

    gen = tg.MathsGenerator(seed)

    p0 = gen.random_integer(1, 10) * tm.Integer(n=10)
    direction = gen.random_element_from([-1, 1])
    x = (gen.random_integer(1, 9) * tm.Integer(n=10)) / tm.Integer(n=100)

    direction = tm.Integer(n=direction)

    p1 = (tm.Integer(n=1) + direction * x) * p0

    p0 = p0.simplified()
    x = x.simplified()
    p1 = p1.simplified()

    return {
        "p0": p0,
        "p1": p1,
        "x": x,
        "direction": direction,
    }


def solve(*, p0, p1, direction, x):
    """[sujets0][gén][sujet-2][automatismes][question-4]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=70)
    >>> answer["maths_object"].simplified()
    Integer(n=70)
    """
    maths_object = p0
    return {
        "maths_object": maths_object,
    }


def render_question(*, p0, p1, direction, x):
    """[sujets0][gén][sujet-2][automatismes][question-4]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Suite à une augmentation de $10 \\\\%$, un article coûte $77$ euros. Quel était son prix initial ?'
    """

    literal_direction = {-1: "diminution", 1: "augmentation"}

    statement = f"Suite à une {literal_direction[direction.n]} de ${x.as_percent.latex()} \\%$, un article coûte ${p1.latex()}$ euros. Quel était son prix initial ?"
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-4]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p0": components["p0"].latex(),
            "p1": components["p1"].latex(),
            "x": components["x"].latex(),
            "direction": components["direction"].latex(),
        },
    }
)
