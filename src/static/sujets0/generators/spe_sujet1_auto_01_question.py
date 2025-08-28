# ruff: noqa : E402


import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# print(dir(teachers))
# print(dir(tm))
# print(dir(tc))
# print(dir(tf))
# print(dir(tg))


def generate_components(difficulty, seed=SEED) -> dict:
    """[1ere][sujets0][spé][sujet-1][automatismes][question-1]
    >>> generate_components(None, 0)
    {'n': Integer(n=5), 'x': Integer(n=7)}
    """
    gen = tg.MathsGenerator(seed)

    n = gen.random_integer(2, 5)
    x = gen.random_integer(1, 10)

    return {
        "n": n,
        "x": x,
    }


def solve(*, n: tm.Integer, x: tm.Integer):
    """[1ere][sujets0][spé][sujet-1][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=1), q=Mul(l=Integer(n=5), r=Integer(n=7)))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=35))
    """
    maths_object = tm.Fraction(p=tm.Integer(n=1), q=n * x)

    # formatting = {tf.Formatting.FRACTION_OR_INTEGER}
    return {"maths_object": maths_object}


def render_question(*, n: tm.Integer, x: tm.Integer):
    """[1ere][sujets0][spé][sujet-1][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> question = render_question(**components)
    >>> question["statement"]
    'Quel est l'inverse du triple de $6$ ?'
    """
    literal_n = {
        2: "double",
        3: "triple",
        4: "quadruple",
        5: "quintuple",
    }

    # 🔴 Sel: This lines break everything with pyodide
    # some stuff should be a function / instance and is considered as a string
    # print(x.latex({tf.Formatting.FRACTION_OR_INTEGER}))

    statement = f"Quel est l'inverse du {literal_n[n.n]} de ${x.latex()}$ ?"

    return {
        "statement": statement,
    }


# def correct():
#     r"""
#     >>> import teachers.corrector as tc
#     >>> components = generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex = r"\\frac\{1\}\{35\}"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """

# def correct(user_latex, answer_formal_repr):
#     r"""
#     >>> components = generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_latex = r"\\frac\{1\}\{35\}"
#     >>> correction = correct(user_latex, repr(answer['maths_object']))
#     >>> assert correction["is_perfect"]
#     >>> assert correction["is_correct"]
#     """
#     correction = tc.correct(user_latex, answer_formal_repr)
#     return correction

components = generate_components(None)
answer = solve(**components)
question = render_question(**components)
# correction = correct(r"\\frac\{1\}\{35\}", repr(answer["maths_object"]))

# print(answer["maths_object"].sympy_expr)
# print(type(answer["maths_object"].sympy_expr))
# print(components | answer | question)

# Create HTML version of the statement
statement_html = f"""<div>{question["statement"]}<br></div>"""


# <span class="italic">La réponse doit être exprimée sous forme d'une fraction irréductible ou d'entier.</span>

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-1]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "n": components["n"].latex(),
            "x": components["x"].latex(),
        },
    }
)

# missive(
#     {
#         "statement": question["statement"],
#         # "answer": answer["maths_object"].latex(),
#         "answer": answer["maths_object"].simplified().latex(),
#         "answer_sympy_expr": answer["maths_object"].model_dump(include={"sympy_expr"})[
#             "sympy_expr"
#         ],
#         "answer_formal_repr": repr(answer["maths_object"]),
#         # "answer_simplified": answer["maths_object"].simplified().latex(),
#         "answer_simplified": answer["maths_object"].simplified().latex(),
#         "x": components["x"].latex(),
#         "n": components["n"].latex(),
#     }
# )


# missive(
#     {
#         "statement": question["statement"],
#         "x": components["x"].latex,
#         "n": components["n"].latex,
#         "answer": answer["maths_object"].latex,
#     }
# )

# we will  need to JSON.stringify the key and value but else it breaks
# TODO : 🔴 Isnt there an issue about the build_question function ? only serializable stuff ?

# print(question)
# print(answer)
# print(components)

# missive()
# def correct():
#     r"""
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex=r"\\frac\{1\}\{35\}"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """


# print(render_question(n=tm.Integer(n=2), x=tm.Integer(n=3)))


# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])


# print(globals())

# # from src.services.sujets0.defaults import SEED

# # SEED = SEED
# # difficulty = None


# # if sys.platform == "emscripten":
# #     ...
# # # Only in backend mode and not if pyodide
# # else:
# #     from src.services.sujets0.defaults import default_missive as missive

# #     if sys.platform == "linux":
# #         # NOTE: mad
# #         sys.path.append("../pca-teachers/src")
# #     else:
# #         # NOTE: sel
# #         sys.path.append("../../madles/pca-teachers/src")


# print(sys.platform)
# print(sys.version_info)

# debug_missive_system()  # This will show the current state
# 🔴 Sel: This line also must not be there for front end
# sadly, the import based on the platform seems to be very dangerous
# (platform= emscripten always for pyodide ? investigate)

# Add default missive for when it's not available
# if sys.platform == "emscripten":
#     # In pyodide components, missive should be available globally
#     pass
# else:
#     # Default implementation for testing/development
#     def missive(data):
#         return data

# No use defaults for import reasons :
# We dont want to import anything locally outside of the pyodide Filesystem stuff
# Therefore, we prefer only one implementation based on the fuletoload argument

# 🔴 Sel: Fromatting creates shit because of serialization issue in missive
# import teachers.formatting as tf
