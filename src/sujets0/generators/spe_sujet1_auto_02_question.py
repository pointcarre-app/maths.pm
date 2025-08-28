import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED):
    """[sujets0][spé][sujet-1][automatismes][question-2]
    >>> generate_components(None, 0)
    {'a': Fraction(p=Integer(n=1), q=Integer(n=7)), 'b': Integer(n=7), 'c': Integer(n=1), 'd': Fraction(p=Integer(n=-1), q=Integer(n=5))}
    """
    # Generate random values
    gen = tg.MathsGenerator(seed)

    # Non degenerate cases
    p = tm.Integer(n=1)
    q = gen.random_integer(1, 10)
    a = tm.Fraction(p=p, q=q)  # so need : a.simplified().latex()}
    # a = tm.Fraction(p=tm.Integer(n=1), q=gen.random_integer(1, 10))
    b = gen.random_integer(1, 10)
    c = gen.random_integer(1, 10)
    d = tm.Fraction(p=tm.Integer(n=-1), q=gen.random_integer(2, 10))  # so doesnt need

    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
    }


def solve(*, a, b, c, d):
    """[sujets0][spé][sujet-1][automatismes][question-2]
    >>> a, b, c, d = tm.Fraction(p=1, q=7), tm.Integer(n=7), tm.Integer(n=1), tm.Fraction(p=-1, q=5)
    >>> answer = solve(a=a, b=b, c=c, d=d)
    >>> answer["maths_object"]
    Add(l=Fraction(p=Integer(n=1), q=Integer(n=7)), r=Fraction(p=Integer(n=7), q=Mul(l=Integer(n=1), r=Fraction(p=Integer(n=-1), q=Integer(n=5)))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=-244), q=Integer(n=7))
    """
    maths_object = a + b / (c * d)
    # formatting = {tf.Formatting.FRACTION_OR_INTEGER}
    return {"maths_object": maths_object}


def render_question(*, a, b, c, d):
    """[sujets0][spé][sujet-1][automatismes][question-2]
    >>> a, b, c, d = tm.Fraction(p=1, q=7), tm.Integer(n=7), tm.Integer(n=1), tm.Fraction(p=-1, q=5)
    >>> statement = render_question(a=a, b=b, c=c, d=d)
    >>> statement["statement"]
    'Soit $F=a+\\\\dfrac\\{b\\}\\{cd\\}$. Lorsque $a=\\\\dfrac\\{1\\}\\{7\\}$, $b = 7$, $c = 1$, $d = -\\\\dfrac\\{1\\}\\{5\\}$, quelle est la valeur de $F$ ?'
    """
    # Create the question in French with proper LaTeX
    statement = "Soit $F=a+\\dfrac{b}{cd}$. "
    statement += f"Lorsque $a={a.simplified().latex()}$, $b = {b.latex()}$, $c = {c.latex()}$, $d = {d.latex()}$, quelle est la valeur de $F$ ?"
    return {"statement": statement}


# def correct():
#     r"""
#     >>> import teachers.corrector as tc
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex=r"-\\frac\{244\}\{7\}"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)
# print(
#     {
#         "statement": question["statement"],
#         "a": components["a"].latex(),
#         "b": components["b"].latex(),
#         "c": components["c"].latex(),
#         "d": components["d"].latex(),
#         "answer": answer["maths_object"].latex(),
#     }
# )


# Create HTML version with formula highlighted
statement_html = f"""<div>Soit $F=a+\\dfrac{{b}}{{cd}}$. 
Lorsque : $a={components["a"].simplified().latex()}$ ; $b = {components["b"].latex()}$ ; $c = {components["c"].latex()}$ ; $d = {components["d"].latex()}$, quelle est la valeur de $F$ ?</div>"""

# <br><span class="italic">La réponse doit être exprimée sous forme d'une fraction irréductible ou d'entier.</span>

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-2]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "mask": "F=",
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "c": components["c"].latex(),
            "d": components["d"].latex(),
        },
    }
)


# question = teachers.build_question(generate_components, solve, render_question, None)
# print("Statement:", question["statement"])
# print("Answer:", question["maths_object"])
# missive({"question": question})
