import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-7]
    >>> generate_components(None, 0)
    {'n': Integer(n=49), 'x': Symbol(s='x'), 'relation': StrictGreaterThan(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Integer(n=49))}
    """

    gen = tg.MathsGenerator(seed)
    n = gen.random_integer(0, 100)
    x = tm.Symbol(s="x")
    relation = x ** tm.Integer(n=2) > n

    return {
        "n": n,
        "x": x,
        "relation": relation,
    }


def solve(*, n, x, relation):
    """[sujets0][spé][sujet-1][automatismes][question-7]
    >>> n, x = tm.Integer(n=49), tm.Symbol(s='x')
    >>> relation = tm.StrictGreaterThan(l=tm.Pow(base=x, exp=tm.Integer(n=2)), r=n)
    >>> answer = solve(n=n, x=x, relation=relation)
    >>> answer["maths_object"]
    (StrictGreaterThan(l=Symbol(s='x'), r=Pow(base=Integer(n=49), exp=Fraction(p=Integer(n=1), q=Integer(n=2)))), StrictGreaterThan(l=Mul(l=Integer(n=-1), r=Pow(base=Integer(n=49), exp=Fraction(p=Integer(n=1), q=Integer(n=2)))), r=Symbol(s='x')))
    >>> answer["maths_object"].simplified()
    (StrictGreaterThan(l=Symbol(s='x'), r=Integer(n=7)), StrictGreaterThan(l=Integer(n=-7), r=Symbol(s='x')))
    """
    answer = tm.MathsCollection(
        elements=[x > n ** tm.Fraction(p=1, q=2), x < -(n ** tm.Fraction(p=1, q=2))]
    )
    return {
        "maths_object": answer,
    }


def render_question(*, n, x, relation):
    r"""[sujets0][spé][sujet-1][automatismes][question-7]
    >>> n, x = tm.Integer(n=49), tm.Symbol(s='x')
    >>> relation = tm.StrictGreaterThan(l=tm.Pow(base=x, exp=tm.Integer(n=2)), r=n)
    >>> statement = render_question(n=n, x=x, relation=relation)
    >>> statement["statement"]
    "On a représenté ci-contre la parabole d'équation $y = x^2$. On note (\\\\mathcal\\{J\\}) l'inéquation, sur \\\\mathbb\\{R\\}, $x^\\{2\\} > 49$. Donner la ou les inéquation(s) du premier degré équivalente à \\\\mathcal\\{J\\}."
    """

    statement = (
        r"On a représenté ci-contre la parabole d'équation $y = x^2$. On note (\\mathcal\{J\}) l'inéquation, sur \\mathbb\{R\}, $"
        + relation.latex()
        + "$. "
    )
    statement += r"Donner la ou les inéquation(s) du premier degré équivalente à \\mathcal\{J\}."

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with graph reference and equation
statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            On a représenté ci-contre la parabole d'équation $y = x^2$.
        </div>
        <div class="alert">
            <span>On note $(\\mathcal{J})$ l'inéquation, sur $\\mathbb{R}$, <span class="badge badge-primary">${relation.latex()}$</span></span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Donner la ou les inéquation(s) du premier degré équivalente à $\\mathcal{J}$.
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-7]",
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
