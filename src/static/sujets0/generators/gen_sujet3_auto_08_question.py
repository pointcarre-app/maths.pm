import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> generate_components(None, 0)
    {'t': Integer(n=4), 'd': Integer(n=5), 'factor': Fraction(p=Integer(n=1), q=Integer(n=60))}
    """

    gen = tg.MathsGenerator(seed)
    
    n1, n2, n3 = gen.random_integer(0, 2), gen.random_integer(0, 1), gen.random_integer(0, 1)

    t = (tm.Integer(n=2) ** n1) * (tm.Integer(n=2) ** n2) * (tm.Integer(n=2) ** n3) 
    t = t.simplified()

    d = gen.random_integer(1, 10)

    factor = tm.Integer(n=1) / tm.Integer(n=60)


    return {
        "t": t,
        "d": d,
        "factor": factor,
    }


def solve(*, d, t, factor):
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Fraction(p=Integer(n=5), q=Integer(n=4)), q=Fraction(p=Integer(n=1), q=Integer(n=60)))
    >>> answer["maths_object"].simplified()
    Integer(n=75)
    """
    maths_object = (d/t) / factor
    return {
        "maths_object": maths_object,
    }


def render_question(*, d, t, factor):
    """[sujets0][gén][sujet-1][automatismes][question-8]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Un object parcours $5$ km en 4 minutes. Quelle est sa vitesse moyenne en km/h ?'
    """

    statement = f"Un object parcours ${d.latex()}$ km en {t.latex()} minutes. Quelle est sa vitesse moyenne en km/h ?"

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
            "d": components["d"].latex(),
            "t": components["t"].latex(),
            "factor": components["factor"].latex(),
        },
    }
)


# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("LaTeX representation:", answer["maths_object"].latex())
