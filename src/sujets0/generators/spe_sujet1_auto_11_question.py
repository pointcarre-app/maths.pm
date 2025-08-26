import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-11]
    >>> generate_components(None, 0)
    {'root1': Integer(n=-4), 'root2': Integer(n=7), 'root3': Integer(n=8), 'x': Integer(n=-2), 'f': Function(name=f)}
    """

    gen = tg.MathsGenerator(seed)

    root1 = gen.random_integer(-7, -5)
    root2 = gen.random_integer(-1, 3)
    root3 = gen.random_integer(root2.n + 3, 10)
    x = gen.random_integer(-10, 10)
    while x in [root1, root2, root3]:
        x = gen.random_integer(-10, 10)
    f = tm.Function(name="f")

    return {"root1": root1, "root2": root2, "root3": root3, "x": x, "f": f}


def solve(*, x, root1, root2, root3, f):
    """[sujets0][spé][sujet-1][automatismes][question-11]
    >>> root1, root2, root3 = tm.Integer(n=-4), tm.Integer(n=7), tm.Integer(n=8),
    >>> x= tm.Integer(n=-2)
    >>> f = tm.Function(name='f')
    >>> answer = solve(x=x, root1=root1, root2=root2, root3=root3, f=f)
    >>> answer["maths_object"]
    StrictGreaterThan(l=Integer(n=0), r=Mul(l=Integer(n=-2), r=Function(name=f)(Integer(n=-2))))
    """
    z = x * (x - root1) * (x - root2) * (x - root3)
    if z.eval() > 0:
        maths_object = x * f(x) > tm.Integer(n=0)
    else:
        maths_object = x * f(x) < tm.Integer(n=0)

    return {"maths_object": maths_object}


def render_question(*, x, root1, root2, root3, f):
    r"""[sujets0][spé][sujet-1][automatismes][question-11]
    >>> root1, root2, root3 = tm.Integer(n=-4), tm.Integer(n=7), tm.Integer(n=8),
    >>> x = tm.Integer(n=-2)
    >>> f = tm.Function(name='f')
    >>> statement = render_question(x=x, root1=root1, root2=root2, root3=root3, f=f)
    >>> statement["statement"]
    "On a représenté ci-contre la courbe $\\\\mathcal\\{C\\}$ d'une fonction ${f}$.\nOn note $A$ le point d'abscisse $x_A=-2$ tel que le point appartienne à la courbe $\\\\mathcal\\{C\\}$.\nEcrire l'inégalité correcte de la forme $x\\\\times f(x) ? 0$"
    """

    statement = (
        r"""On a représenté ci-contre la courbe $\\mathcal\{C\}$ d'une fonction ${"""
        + f.name
        + """}$.\nOn note $A$ le point d'abscisse $x_A="""
        + str(x.n)
        + r"""$ tel que le point appartienne à la courbe $\\mathcal\{C\}$."""
        + "\n"
        + r"""Ecrire l'inégalité correcte de la forme $x\\times f(x) ? 0$"""
    )
    graph_description = f"La courbe d'équation y=(x-{root1.n})(x-{root2.n})(x-{root3.n})"

    return {
        "statement": statement,
        "graph_description": graph_description,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with point description
statement_html = f"""
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            On a représenté ci-contre la courbe $\\mathcal{{C}}$ d'une fonction ${{f.name}}$.
        </div>
        <div class="alert">
            <span>On note $A$ le point d'abscisse <span class="badge badge-primary">$x_A={{x.n}}$</span> tel que le point appartienne à la courbe $\\mathcal{{C}}$.</span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Ecrire l'inégalité correcte de la forme $x \\times f(x) \\; ? \\; 0$
        </div>
        {f'<div class="text-xs text-base-content/60 mt-2 italic">Note: {question.get("graph_description", "")}</div>' if "graph_description" in question else ""}
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-11]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "root1": components["root1"].latex(),
            "root2": components["root2"].latex(),
            "root3": components["root3"].latex(),
            "x": components["x"].latex(),
            "f": components["f"].name,
        },
    }
)
