import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-10]
    >>> generate_components(None, 0)
    {'a': Integer(n=1), 'c': Integer(n=-7), 'x': Symbol(s='x')}
    """

    gen = tg.MathsGenerator(seed)

    # a = gen.random_integer(1, 10)
    dir1 = gen.random_element_from([-1, 1])
    a = tm.Integer(n=dir1)
    c = gen.random_integer(1, 10)
    dir2 = gen.random_element_from([-1, 1])
    c = tm.Integer(n=dir2) * c
    c = c.simplified()
    x = tm.Symbol(s="x")

    return {
        "a": a,
        "c": c,
        "x": x,
    }


def solve(*, x, a, c):
    """[sujets0][spé][sujet-1][automatismes][question-10]
    >>> a, c, x = tm.Integer(n=1), tm.Integer(n=-7), tm.Symbol(s='x')
    >>> answer = solve(x=x, a=a, c=c)
    >>> answer["maths_object"]
    Add(l=Mul(l=Integer(n=1), r=Pow(base=Symbol(s='x'), exp=Integer(n=2))), r=Integer(n=-7))
    >>> answer["maths_object"].simplified()
    Add(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Integer(n=-7))
    """
    maths_object = a * x ** tm.Integer(n=2) + c
    return {"maths_object": maths_object}


def render_question(*, x, a, c):
    """[sujets0][spé][sujet-1][automatismes][question-10]
    >>> a, c, x = tm.Integer(n=1), tm.Integer(n=-7), tm.Symbol(s='x')
    >>> statement = render_question(x=x, a=a, c=c)
    >>> statement["statement"]
    "La courbe ci-contre représente la courbe d\'équation $ax^2 + bx + c$. On suppose $\\\\\\\\lvert a \\\\\\\\rvert = 1$. Donner l\'équation de la parabole."
    >>> statement["graph_description"]
    "Une parabole d'équation $x^2-7$, avec simplement la valeur l'ordonée à l'origine"
    """
    statement = r"La courbe ci-contre représente la courbe d'équation $ax^2 + bx + c$. On suppose $\\lvert a \\rvert = 1$. Donner l'équation de la parabole."
    if a.n == 1 and c.n > 0:
        graph_description = (
            f"Une parabole d'équation $x^2+{c.n}$, avec simplement la valeur l'ordonée à l'origine"
        )
    elif a.n == 1 and c.n < 0:
        graph_description = (
            f"Une parabole d'équation $x^2{c.n}$, avec simplement la valeur l'ordonée à l'origine"
        )
    elif a.n == -1 and c.n > 0:
        graph_description = (
            f"Une parabole d'équation $-x^2+{c.n}$, avec simplement la valeur l'ordonée à l'origine"
        )
    elif a.n == -1 and c.n < 0:
        graph_description = (
            f"Une parabole d'équation $-x^2{c.n}$, avec simplement la valeur l'ordonée à l'origine"
        )
    else:
        raise ValueError(f"{a.n=}, {c.n=}")

    return {"statement": statement, "graph_description": graph_description}


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-10]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "c": components["c"].latex(),
            "x": components["x"].latex(),
        },
    }
)
