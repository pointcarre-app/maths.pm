import teachers.maths as tm
from teachers.defaults import SEED
import random


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-11]
    >>> generate_components(None, 0)
    {'root1': Integer(n=-4), 'root2': Integer(n=7), 'root3': Integer(n=8), 'x': Integer(n=-2), 'f': Function(name=f)}
    """

    # Case A
    # ROOT1 = -4
    # ROOT2 = 2
    # ROOT3 = 5

    # Case B
    # ROOT1 = -4
    # ROOT2 = 3
    # ROOT3 = 5

    # Case C
    # ROOT1 = -4
    # ROOT2 = 2
    # ROOT3 = 4

    cases = [
        {
            "root1": tm.Integer(n=-4),
            "root2": tm.Integer(n=2),
            "root3": tm.Integer(n=5),
            # "x": tm.Integer(n=-2),
            "case": "case_a",
        },
        {
            "root1": tm.Integer(n=-4),
            "root2": tm.Integer(n=3),
            "root3": tm.Integer(n=5),
            # "x": tm.Integer(n=-2),
            "case": "case_b",
        },
        {
            "root1": tm.Integer(n=-4),
            "root2": tm.Integer(n=2),
            "root3": tm.Integer(n=4),
            # "x": tm.Integer(n=-2),
            "case": "case_c",
        },
    ]

    random.seed(seed)
    case = random.choice(cases)

    case["f"] = tm.Function(name="f")

    root1, root2, root3 = case["root1"], case["root2"], case["root3"]
    zero = tm.Integer(n=0)
    min_root = min(root1.n, root2.n, root3.n)
    max_root = max(root1.n, root2.n, root3.n)
    # + 1 because enough room right but not left

    x = tm.Integer(n=random.randint(min_root, max_root + 1))  # last one included
    # Zero creates an issue cause strict inequality is not possible anymore (0=0)
    while x in [root1, root2, root3, zero]:
        x = tm.Integer(n=random.randint(min_root, max_root + 1))  # terminaison is ensured
    case["x"] = x

    return case

    # x = tm.Integer(n=random.randint(min_root, max_root + 1))
    # TODO : generate smarter generation (fractions for instance)

    # Old version
    # But graph are very restricted (3 cases)

    # x = gen.random_integer(-10, 10)
    # while x in [root1, root2, root3]:
    #     x = gen.random_integer(-10, 10)

    # gen = tg.MathsGenerator(seed)

    # root1 = gen.random_integer(-7, -5)
    # root2 = gen.random_integer(-1, 3)
    # root3 = gen.random_integer(root2.n + 3, 10)
    # x = gen.random_integer(-10, 10)
    # while x in [root1, root2, root3]:
    #     x = gen.random_integer(-10, 10)
    # f = tm.Function(name="f")

    # return {"root1": root1, "root2": root2, "root3": root3, "x": x, "f": f}


def solve(*, x, root1, root2, root3, f, case=None):
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


def render_question(*, x, root1, root2, root3, f, case=None):
    r"""[sujets0][spé][sujet-1][automatismes][question-11]
    >>> root1, root2, root3 = tm.Integer(n=-4), tm.Integer(n=7), tm.Integer(n=8),
    >>> x = tm.Integer(n=-2)
    >>> f = tm.Function(name='f')
    >>> statement = render_question(x=x, root1=root1, root2=root2, root3=root3, f=f)
    >>> statement["statement"]
    "On a représenté ci-contre la courbe $\\\\mathcal\\{C\\}$ d'une fonction ${f}$.\nOn note $A$ le point d'abscisse $x_A=-2$ tel que le point appartienne à la courbe $\\\\mathcal\\{C\\}$.\nEcrire l'inégalité correcte de la forme $x\\\\times f(x) ? 0$"
    """

    statement = (
        "On a représenté ci-contre la courbe $\\mathcal{C}$ "
        + f"d'une fonction ${f.name}$.\nOn note $A$ le point d'abscisse $x_A={x.n}$ tel que le point appartienne à la courbe $\\mathcal{{C}}$."
        + "<br>"
        + """Parmi les deux inégalités suivantes : <br>$x_a \\times f(x_a) > 0$ et $x_a \\times f(x_a) < 0$<br>Laquelle est correcte ?"""
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
statement_html = f"<div>{question['statement']}</div>"

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-11]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
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
            "case": components["case"],
        },
    }
)
