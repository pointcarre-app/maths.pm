###############################################################################
# NOTE : exactly the same as [sujets0][spé][sujet-2][automatismes][question-3]
###############################################################################


import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-3]
    >>> generate_components(None, 0)
    {'p': Integer(n=65), 'direction': Integer(n=1)}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 20)
    p = tm.Integer(n=5 * p.n)

    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    return {"p": p, "direction": direction}


def solve(*, p, direction):
    """[sujets0][spé][sujet-2][automatismes][question-3]
    >>> answer = solve(p=tm.Integer(n=65), direction=tm.Integer(n=1))
    >>> answer["maths_object"]
    Mul(l=Integer(n=-1), r=Pow(base=Fraction(p=Integer(n=65), q=Integer(n=100)), exp=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-169), q=Integer(n=400))
    """
    maths_object = -((p / tm.Integer(n=100)) ** tm.Integer(n=2))
    return {"maths_object": maths_object}


def render_question(*, p, direction):
    r"""[sujets0][spé][sujet-2][automatismes][question-3]
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
print("components ok")
answer = solve(**components)
print("answer ok")
question = render_question(**components)
print("question ok")


# print(components | answer | question)


# Create HTML version - same as sujet1 question 4
if components["direction"].n == -1:
    dir1, dir2 = "diminue", "augmente"
else:
    dir1, dir2 = "augmente", "diminue"

statement_html = f"""
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            Le prix d'un article est noté $P$.
        </div>
        <div class="steps steps-vertical">
            <div class="step step-primary">
                <div class="text-sm">Ce prix {dir1} de <span class="badge badge-warning">${{p.latex()}}\\%$</span></div>
            </div>
            <div class="step step-primary">
                <div class="text-sm">Puis {dir2} de <span class="badge badge-warning">${{p.latex()}}\\%$</span></div>
            </div>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            A l'issue de ces deux variations, de combien le prix a-t-il varié en pourcentage ?
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-3]",
        "statement": question["statement"],
        "statement_html": statement_html,
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
