import random
import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-4]
    >>> generate_components(None, 0)
    {'p': Fraction(p=Integer(n=65), q=Integer(n=100))}
    """
    gen = tg.MathsGenerator(seed)

    multiplier_int = random.choice([1, 2, 4, 6])
    p = tm.Integer(n=5 * multiplier_int) / tm.Integer(n=100)

    # Mène donc à p = 5% ou 10% ou 20% ou 30%
    # Donc

    return {"p": p}


def solve(*, p):
    """[sujets0][gén][sujet-1][automatismes][question-4]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Add(l=Mul(l=Integer(n=2), r=Fraction(p=Integer(n=65), q=Integer(n=100))), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=689), q=Integer(n=400))
    """
    maths_object = (tm.Integer(n=1) + p) * (tm.Integer(n=1) + p) - tm.Integer(n=1)
    return {"maths_object": maths_object}


def render_question(*, p):
    """[sujets0][gén][sujet-1][automatismes][question-4]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Un article augmente de $\\\\dfrac{65}{100}\\\\%$ puis de nouveau de $\\\\dfrac{65}{100}\\\\%$. A l'issue de ces deux variations, de combien le prix a-t-il varié en pourcentage ?"
    """

    statement = f"""Un article augmente de ${(tm.Integer(n=100) * p).simplified().as_decimal.latex().replace(".", ",")}\\%$ puis de nouveau de ${(tm.Integer(n=100) * p).simplified().as_decimal.latex().replace(".", ",")}\\%$. A l'issue de ces deux variations, quel est le pourcentage d'évolution ?"""
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
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-4]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": [
                answer["maths_object"].simplified().latex() + "\\%",
                (answer["maths_object"] * tm.Integer(n=100)).simplified().as_decimal.latex()
                + "\\%",
            ],
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p": components["p"].latex(),
        },
    }
)
