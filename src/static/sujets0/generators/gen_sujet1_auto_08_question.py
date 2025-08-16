import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> generate_components(None, 0)
    {'x': Integer(n=250), 'factor': Integer(n=60)}
    """

    gen = tg.MathsGenerator(seed)

    x = gen.random_integer(1, 50)
    x = x * tm.Integer(n=10)
    x = x.simplified()

    factor = tm.Integer(n=60)

    return {
        "x": x,
        "factor": factor,
    }


def solve(*, x, factor):
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=250), q=Integer(n=60))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=25), q=Integer(n=6))
    """
    answer = x/ factor
    return {
        "maths_object": answer,
    }


def render_question(*, x, factor):
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Convertir en heures une durée de 250 minutes. Ta réponse doit être sous forme de fraction.'
    """

    statement = f"Convertir en heures une durée de {x.latex()} minutes. Ta réponse doit être sous forme de fraction."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-8]",
        "statement": question["statement"],
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
