import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-4]
    >>> generate_components(None, 0)
    {'p': Integer(n=65), 'direction': Integer(n=1)}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 20)
    p = tm.Integer(n=5 * p.n)

    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    return {"p": p, "direction": direction}


def solve(*, p, direction):
    """[sujets0][spé][sujet-1][automatismes][question-4]
    >>> answer = solve(p=tm.Integer(n=65), direction=tm.Integer(n=1))
    >>> answer["maths_object"]
    Mul(l=Integer(n=-1), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-169), q=Integer(n=400))
    """
    maths_object = -((p / tm.Integer(n=100)) ** tm.Integer(n=2))
    return {"maths_object": maths_object}


def render_question(*, p, direction):
    r"""[sujets0][spé][sujet-1][automatismes][question-4]
    >>> p = tm.Integer(n=65)
    >>> direction = tm.Integer(n=1)
    >>> statement = render_question(p=p, direction=direction)
    >>> statement["statement"]
    "Le prix d'un article est noté $P$. Ce prix augmente de $65\\%$ puis diminue de $65\\%$. A l'issue de ces deux variations, de combien le prix a-t-il varié en pourcentage ?"
    """
    if direction == -1:
        dir1, dir2 = "diminue", "augmente"
    else:
        dir1, dir2 = "augmente", "diminue"

    statement = f"""Le prix d'un article est noté $P$. Ce prix {dir1} de ${p.latex()}\\%$ puis {dir2} de ${p.latex()}\\%$. A l'issue de ces deux variations, de combien le prix a-t-il varié en pourcentage ?"""

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-4]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p": components["p"].latex(),
            "direction": components["direction"].latex(),
        },
    }
)
