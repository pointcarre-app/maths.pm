import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-3][automatismes][question-4]
    >>> generate_components(None, 0)
    {'n': Integer(n=70), 'x': Fraction(p=Mul(l=Pow(base=Integer(n=2), exp=Integer(n=1)), r=Pow(base=Integer(n=5), exp=Integer(n=0))), q=Integer(n=100))}
    """
    gen = tg.MathsGenerator(seed)

    n = gen.random_integer(1, 10) * tm.Integer(n=10)
    n = n.simplified()

    n1, n2 = tm.Integer(n=0), tm.Integer(n=0)
    while n1.n == 0 and n2.n == 0:
        n1 = gen.random_integer(0, 2)
        n2 = gen.random_integer(0, 2)

    x = ((tm.Integer(n=2) ** n1) * (tm.Integer(n=5) ** n2))  / tm.Integer(n=100)
    # x = x.simplified()
    
    return {
        "n": n,
        "x": x,
    }


def solve(*, n, x):
    """[sujets0][gén][sujet-3][automatismes][question-4]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=70), q=Fraction(p=Mul(l=Pow(base=Integer(n=2), exp=Integer(n=1)), r=Pow(base=Integer(n=5), exp=Integer(n=0))), q=Integer(n=100)))
    >>> answer["maths_object"].simplified()
    Integer(n=3500)
    """
    maths_object = (n / x)
    return {"maths_object": maths_object}


def render_question(*, n, x):
    """[sujets0][gén][sujet-3][automatismes][question-4]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Dans un établissement scolaire, $70$ élèves étudient le Grec, ce qui représente de $2\\\\%$. Combien d'élèves au total sont inscrits dans l\'établissement ?"
    """

    x = x.simplified()

    statement = f"Dans un établissement scolaire, ${n.latex()}$ élèves étudient le Grec, ce qui représente de ${x.as_percent.latex()}\\%$. Combien d'élèves au total sont inscrits dans l'établissement ?"
    return {
        "statement": statement,
    }





components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][gen][sujet-3][automatismes][question-4]",
        "statement": question["statement"],
        "mask": "",
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
            "x": components["x"].latex(),
        },
    }
)


