import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-3][automatismes][question-12]
    >>> generate_components(None, 0)
    {'root1': Integer(n=-9), 'root2': Integer(n=-2), 'root3': Integer(n=2), 'root4': Integer(n=3), 'f': Function(name=f), 'x': Symbol(s='x')}
    """

    gen = tg.MathsGenerator(seed)

    root1 = gen.random_integer(-10, 10)
    root2 = gen.random_integer(-10, 10)
    root3 = gen.random_integer(-10, 10)
    root4 = gen.random_integer(-10, 10)

    root1, root2, root3, root4 = sorted((root1, root2, root3, root4), key=lambda x: x.n)

    f = tm.Function(name="f")
    x = tm.Symbol(s="x")

    return {
        "root1": root1,
        "root2": root2,
        "root3": root3,
        "root4": root4,
        "f": f,
        "x": x,
    }


def solve(*, root1, root2, root3, root4, f, x):
    """[sujets0][spé][sujet-3][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    (Integer(n=-9), Integer(n=-2), Integer(n=2), Integer(n=3))
    >>> answer["maths_object"].simplified()
    (Integer(n=-9), Integer(n=-2), Integer(n=2), Integer(n=3))
    """

    roots = set(x.n for x in [root1, root2, root3, root4])
    roots = [tm.Integer(n=x) for x in sorted(roots)]

    maths_object = tm.MathsCollection(elements=roots)

    return {"maths_object": maths_object}


def render_question(*, root1, root2, root3, root4, f, x):
    """[sujets0][spé][sujet-3][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Soit $f$ la fonction définie sur l\'intervalle $\\\\lbracket -9; 9 \\\\rbracket$ dont la représentation grpahique est donnée ci-contre. Donner l'ensemble $\\\\mathcal{S}$ des solutions de $f(x) = 0$"
    """

    equation = tm.Equality(l=f(x), r=tm.Integer(n=0))

    statement = f"Soit ${f.latex()}$ la fonction définie sur l'intervalle $\\lbracket -9; 9 \\rbracket$ dont la représentation grpahique est donnée ci-contre. "
    statement += f"Donner l'ensemble $\\mathcal{{S}}$ des solutions de ${equation.latex()}$"
    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-3][automatismes][question-12]",
        "statement": question["statement"],
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
            "root4": components["root4"].latex(),
            "x": components["x"].latex(),
            "f": components["f"].name,
        },
    }
)
