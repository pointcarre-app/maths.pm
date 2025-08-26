import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-11]
    >>> generate_components(None, 0)
    {'x': Symbol(s='x'), 'a': Decimal(p=50, q=100), 'expr': Pow(base=Add(l=Symbol(s='x'), r=Decimal(p=50, q=100)), exp=Integer(n=2))}
    """

    gen = tg.MathsGenerator(seed)
    x = tm.Symbol(s="x")
    p = gen.random_integer(1, 100)

    # TODO: we could randomize on decimal vs fraction

    a = tm.Decimal(p=p.n, q=100)  # tm.Integer(n=100)
    expr = (x + a) ** tm.Integer(n=2)

    return {
        "x": x,
        "a": a,
        "expr": expr,
    }


def solve(*, x, a, expr):
    """[sujets0][spé][sujet-2][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Add(l=Symbol(s='x'), r=Decimal(p=50, q=100)), exp=Integer(n=2))
    >>> answer["maths_object"].simplified()
    Add(l=Add(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Mul(l=Decimal(p=100, q=100), r=Symbol(s='x'))), r=Pow(base=Decimal(p=50, q=100), exp=Integer(n=2)))
    """
    answer = expr
    return {
        "maths_object": answer,
    }


def render_question(*, x, a, expr):
    """[sujets0][spé][sujet-2][automatismes][question-11]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Quelle est l\'expression développée de $\\\\left(x + 0,5\\\\right)^\\\\{2\\\\}$ ?"
    """

    statement = f"Quelle est l'expression développée de ${expr.latex()}$ ?"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with expression to expand
statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            Quelle est l'expression développée de :
        </div>
        <div class="alert alert-info">
            <span class="text-lg">${expr.latex()}$</span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Développer et simplifier l'expression.
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-11]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "a": components["a"].latex(),
            "expr": components["expr"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("Simplified answer:", answer["maths_object"].simplified())
# print("LaTeX representation:", answer["maths_object"].latex())
