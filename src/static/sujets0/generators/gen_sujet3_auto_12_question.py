import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-3][automatismes][question-12]
    >>> generate_components(None, 0)
    {'root1': Integer(n=-9), 'root2': Integer(n=-2), 'root3': Integer(n=2), 'root4': Integer(n=3), 'f': Function(name=f), 'x': Symbol(s='x'), 'polynomial': ...}
    """

    gen = tg.MathsGenerator(seed)

    root1 = gen.random_integer(-10, 10)
    root2 = gen.random_integer(-10, 10)
    root3 = gen.random_integer(-10, 10)
    root4 = gen.random_integer(-10, 10)

    root1, root2, root3, root4 = sorted((root1, root2, root3, root4), key=lambda x: x.n)

    f = tm.Function(name="f")
    x = tm.Symbol(s="x")

    # Create polynomial f(x) = a(x-root1)(x-root2)(x-root3)(x-root4)
    # with scaling factor to keep values reasonable
    scale_factor = tm.Fraction(p=1, q=100)  # Small factor to prevent huge values

    term1 = x - root1
    term2 = x - root2
    term3 = x - root3
    term4 = x - root4

    polynomial = scale_factor * term1 * term2 * term3 * term4
    polynomial = polynomial.simplified()

    return {
        "root1": root1,
        "root2": root2,
        "root3": root3,
        "root4": root4,
        "f": f,
        "x": x,
        "polynomial": polynomial,
    }


def solve(*, root1, root2, root3, root4, f, x, polynomial):
    """[sujets0][spé][sujet-3][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    (Integer(n=-9), Integer(n=-2), Integer(n=2), Integer(n=3))
    """

    roots = set(x.n for x in [root1, root2, root3, root4])
    roots = [tm.Integer(n=x) for x in sorted(roots)]

    maths_object = tm.MathsCollection(elements=roots)

    return {"maths_object": maths_object}


def render_question(*, root1, root2, root3, root4, f, x, polynomial):
    """[sujets0][spé][sujet-3][automatismes][question-12]"""

    equation = tm.Equality(l=f(x), r=tm.Integer(n=0))

    statement = "Soit $f$ une fonction définie sur l'intervalle $[ -6; 6 ]$, dont la représentation graphique est donnée ci-contre. "
    statement += f"Quel est l'ensemble $\\mathcal{{S}}$ des solutions de ${equation.latex()}.$"
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-3][automatismes][question-12]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
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
            "polynomial": components["polynomial"].latex(),
        },
    }
)


# import teachers.generator as tg
# import teachers.maths as tm
# from teachers.defaults import SEED


# def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
#     """[sujets0][spé][sujet-3][automatismes][question-12]
#     >>> generate_components(None, 0)
#     {'root1': Integer(n=-9), 'root2': Integer(n=-2), 'root3': Integer(n=2), 'root4': Integer(n=3), 'f': Function(name=f), 'x': Symbol(s='x')}
#     """

#     gen = tg.MathsGenerator(seed)

#     root1 = gen.random_integer(-10, 10)
#     root2 = gen.random_integer(-10, 10)
#     root3 = gen.random_integer(-10, 10)
#     root4 = gen.random_integer(-10, 10)

#     root1, root2, root3, root4 = sorted((root1, root2, root3, root4), key=lambda x: x.n)

#     f = tm.Function(name="f")
#     x = tm.Symbol(s="x")

#     return {
#         "root1": root1,
#         "root2": root2,
#         "root3": root3,
#         "root4": root4,
#         "f": f,
#         "x": x,
#     }


# def solve(*, root1, root2, root3, root4, f, x):
#     """[sujets0][spé][sujet-3][automatismes][question-12]
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> answer["maths_object"]
#     (Integer(n=-9), Integer(n=-2), Integer(n=2), Integer(n=3))
#     >>> answer["maths_object"].simplified()
#     (Integer(n=-9), Integer(n=-2), Integer(n=2), Integer(n=3))
#     """

#     roots = set(x.n for x in [root1, root2, root3, root4])
#     roots = [tm.Integer(n=x) for x in sorted(roots)]

#     maths_object = tm.MathsCollection(elements=roots)

#     return {"maths_object": maths_object}


# def render_question(*, root1, root2, root3, root4, f, x):
#     """[sujets0][spé][sujet-3][automatismes][question-12]
#     >>> components= generate_components(None, 0)
#     >>> statement = render_question(**components)
#     >>> statement["statement"]
#     "Soit $f$ la fonction définie sur l\'intervalle $\\lbracket -9; 9 \\\\rbracket$ dont la représentation grpahique est donnée ci-contre. Donner l'ensemble $\\\\mathcal{S}$ des solutions de $f(x) = 0$"
#     """

#     equation = tm.Equality(l=f(x), r=tm.Integer(n=0))

#     statement = f"Soit ${f.latex()}$ la fonction définie sur l'intervalle $\\lbracket -9; 9 \\rbracket$ dont la représentation grpahique est donnée ci-contre. "
#     statement += f"Donner l'ensemble $\\mathcal{{S}}$ des solutions de ${equation.latex()}$"
#     statement_html = f"<div>{statement}</div>"
#     return {
#         "statement": statement,
#         "statement_html": statement_html,
#     }


# components = generate_components(None)
# answer = solve(**components)
# question = render_question(**components)


# # print(components | answer | question)


# missive(
#     {
#         "beacon": "[1ere][sujets0][spé][sujet-3][automatismes][question-12]",
#         "statement": question["statement"],
#         "statement_html": question["statement_html"],
#         "answer": {
#             "latex": answer["maths_object"].latex(),
#             "simplified_latex": answer["maths_object"].simplified().latex(),
#             "sympy_exp_data": answer["maths_object"].sympy_expr_data,
#             "formal_repr": repr(answer["maths_object"]),
#         },
#         "components": {
#             "root1": components["root1"].latex(),
#             "root2": components["root2"].latex(),
#             "root3": components["root3"].latex(),
#             "root4": components["root4"].latex(),
#             "x": components["x"].latex(),
#             "f": components["f"].name,
#         },
#     }
# )
