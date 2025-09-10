import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> generate_components(None, 0)
    {'x': Integer(n=500), 'factor': Fraction(p=Integer(n=1000), q=Integer(n=700))}
    """

    gen = tg.MathsGenerator(seed)

    x = gen.random_integer(1, 99) * tm.Integer(n=10)
    x = x.simplified()

    factor = gen.random_integer(1, 9) * tm.Integer(n=100)
    factor = factor.simplified()
    factor = tm.Integer(n=1000) / factor

    return {
        "x": x,
        "factor": factor,
    }


def solve(*, x, factor):
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=500), q=Fraction(p=Integer(n=1000), q=Integer(n=700)))
    >>> answer["maths_object"].simplified()
    Integer(n=350)
    """
    answer = x / factor
    return {
        "maths_object": answer,
    }


def render_question(*, x, factor):
    """[sujets0][gén][sujet-2][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'On considère un liquide pour lequel $1$ L pèse $700$ g. Combien pèse $500$ mL de ce liquide ?'
    """

    mass = tm.Integer(n=1000) / factor
    mass = mass.simplified().as_decimal

    statement = f"On considère un liquide pour lequel $1$ L pèse ${mass.latex()}$ g. Combien pèse ${x.latex()}$ mL de ce liquide ?"
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-8]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "factor": components["factor"].latex(),
        },
    }
)


# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("LaTeX representation:", answer["maths_object"].latex())
