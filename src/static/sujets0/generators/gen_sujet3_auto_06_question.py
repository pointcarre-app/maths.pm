import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-3][automatismes][question-6]
    >>> generate_components(None, 0)
    {'a': Integer(n=3), 'b': Integer(n=7)}
    """

    gen = tg.MathsGenerator(seed)
    a = gen.random_integer(-3, 3)
    b = gen.random_integer(1, 10)

    return {
        "a": a,
        "b": b,
    }


def solve(*, a, b):
    """[sujets0][gén][sujet-3][automatismes][question-6]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=3)
    >>> answer["maths_object"].simplified()
    Integer(n=3)
    """
    maths_object = a
    return {"maths_object": maths_object}


def render_question(*, a, b):
    """[sujets0][gén][sujet-3][automatismes][question-6]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'On a représenté ci-contre une droite \\\\mathcal{D} dans un repère orthonormé. Donner la valeur de son coefficient directeur.'
    """

    statement = "On a représenté ci-contre une droite \\mathcal{D} dans un repère orthonormé. Donner la valeur de son coefficient directeur."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-3][automatismes][question-6]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "b": components["b"].latex(),
        },
    }
)
