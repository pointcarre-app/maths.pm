import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-6]
    >>> generate_components(None, 0)
    {'k': Mul(l=Integer(n=50), r=Pow(base=Integer(n=10), exp=Integer(n=7))), 'factor': Mul(l=Decimal(p=36, q=10), r=Pow(base=Integer(n=10), exp=Integer(n=6)))}
    """

    gen = tg.MathsGenerator(seed)

    x = gen.random_integer(1, 100)
    x = x.simplified()
    n = gen.random_integer(1, 8)
    k = x * (tm.Integer(n=10) ** n)

    # TODO: we should be able to randomly choose conversion when we have proper units system
    factor = tm.Decimal(p=36, q=10) * tm.Pow(base=tm.Integer(n=10), exp=tm.Integer(n=6))

    return {
        "k": k,
        "factor": factor,
    }


def solve(*, k, factor):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Decimal(x=138.89)
    >>> answer["maths_object"].simplified()
    Decimal(x=138.89)
    """
    answer = (k / factor).as_decimal.round(2)
    return {
        "maths_object": answer,
    }


def render_question(*, k, factor):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Un appareil a besoin d\'une énergie de $50 \\\\times 10^\\\\{7\\\\}$ Joules (J) pour se mettre en route. A combien de kiloWatt-heure (kWh) cela correspond-il. On donne $1kWh=3,6 \\\\times 10^\\\\{6\\\\}J$."
    """

    statement = f"Un appareil a besoin d'une énergie de ${k.latex()}$ Joules (J) pour se mettre en route. A combien de kiloWatt-heure (kWh) cela correspond-il. On donne $1kWh={factor.latex()}J$."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with unit conversion
statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            Un appareil a besoin d'une énergie de :
        </div>
        <div class="stats shadow mb-3">
            <div class="stat">
                <div class="stat-title">Energie requise</div>
                <div class="stat-value text-primary">${k.latex()}$</div>
                <div class="stat-desc">Joules (J)</div>
            </div>
        </div>
        <div class="alert">
            <span>Conversion : $1\\text{ kWh} = {factor.latex()}\\text{ J}$</span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            A combien de kiloWatt-heure (kWh) cela correspond-il ?
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-6]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "k": components["k"].latex(),
            "factor": components["factor"].latex(),
        },
    }
)


# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("LaTeX representation:", answer["maths_object"].latex())
