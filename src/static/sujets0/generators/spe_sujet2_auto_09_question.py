import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> generate_components(None, 0)
    {'n': Integer(n=49), 'x': Symbol(s='x'), 'relation': Equality(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Integer(n=49))}
    """

    gen = tg.MathsGenerator(seed)
    n = gen.random_integer(0, 100)
    x = tm.Symbol(s="x")
    relation = tm.Equality(l=x ** tm.Integer(n=2), r=n)

    return {
        "n": n,
        "x": x,
        "relation": relation,
    }


def solve(*, n, x, relation):
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> n, x = tm.Integer(n=49), tm.Symbol(s='x')
    >>> relation = tm.StrictGreaterThan(l=tm.Pow(base=x, exp=tm.Integer(n=2)), r=n)
    >>> answer = solve(n=n, x=x, relation=relation)
    >>> answer["maths_object"]
    (Pow(base=Integer(n=49), exp=Fraction(p=Integer(n=1), q=Integer(n=2))), Mul(l=Integer(n=-1), r=Pow(base=Integer(n=49), exp=Fraction(p=Integer(n=1), q=Integer(n=2)))))
    >>> answer["maths_object"].simplified()
    (Integer(n=7), Integer(n=-7))
    """
    answer = tm.MathsCollection(
        elements=[n ** tm.Fraction(p=1, q=2), -(n ** tm.Fraction(p=1, q=2))]
    )
    return {
        "maths_object": answer,
    }


def render_question(*, n, x, relation):
    r"""[sujets0][spé][sujet-2][automatismes][question-9]
    >>> n, x = tm.Integer(n=49), tm.Symbol(s='x')
    >>> relation = tm.StrictGreaterThan(l=tm.Pow(base=x, exp=tm.Integer(n=2)), r=n)
    >>> statement = render_question(n=n, x=x, relation=relation)
    >>> statement["statement"]
    "On note $\\\\mathcal\\{S\\}$ l'ensemble des solutions de l'équation $x^2=49$ sur $\\\\mathbb\\{R\\}$. Calculer $\\\\mathcal\\{S\\}$"
    """

    statement = (
        r"On note $\\mathcal\{S\}$ l'ensemble des solutions de l'équation $"
        + f"{x.latex()}^2={n.latex()}"
        + r"$ sur $\\mathbb\{R\}$. Calculer $\\mathcal\{S\}$"
    )

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with equation
statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="alert alert-info mb-3">
            <span>On note $\\mathcal{S}$ l'ensemble des solutions de l'équation <span class="badge badge-primary">${x.latex()}^2={n.latex()}$</span> sur $\\mathbb{R}$</span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Calculer $\\mathcal{S}$
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-9]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
            "x": components["x"].latex(),
            "relation": components["relation"].latex(),
        },
    }
)
