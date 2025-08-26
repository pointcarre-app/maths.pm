# ruff: noqa : E402


import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# TODO: variabiliser sur le format


# This generation lead to "mandatorilu cleaned percet representation"
def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> generate_components(None, 0)
    {'p': Fraction(p=Integer(n=99), q=Integer(n=200)), 'direction': Integer(n=1), 'coef': Add(l=Integer(n=1), r=Mul(l=Integer(n=1), r=Fraction(p=Integer(n=99), q=Integer(n=200))))}
    """
    gen = tg.MathsGenerator(seed)

    p = gen.random_integer(1, 200)
    p = tm.Fraction(p=p, q=200)
    direction = tm.Integer(n=gen.random_element_from((-1, 1)))
    coef = tm.Integer(n=1) + direction * p

    return {
        "p": p,
        "direction": direction,
        "coef": coef,
    }


def solve(*, p, direction, coef):
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> answer = solve(p=tm.Fraction(p=99, q=200), direction=1, coef=tm.Fraction(p=299, q=200))
    >>> answer["maths_object"]
    Fraction(p=Integer(n=99), q=Integer(n=200))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=99), q=Integer(n=200))
    """
    maths_object = p
    return {"maths_object": maths_object}


def render_question(*, p, direction, coef):
    """[sujets0][spé][sujet-1][automatismes][question-3]
    >>> p = tm.Fraction(p=99, q=200)
    >>> direction = tm.Integer(n=1)
    >>> coef = tm.Fraction(p=299, q=200)
    >>> statement = render_question(p=p, direction=direction, coef=coef)
    >>> statement["statement"]
    "Le prix d'un article est multiplié par $1,495$. De combien de pourcent le prix de cet article a-t-il augmenté ?"
    """
    # was : coef.simplified().latex
    coef = coef.simplified().as_decimal
    statement = (
        f"Le prix d'un article est multiplié par ${coef.latex()}$. Calculer la variation relative."
    )
    return {
        "statement": statement,
    }


# def correct():
#     r"""
#     >>> import teachers.corrector as tc
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex=r"49,5"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(
#     {
#         "statement": question["statement"],
#         "answer": answer["maths_object"].latex(),
#         "p": components["p"].latex(),
#         "direction": components["direction"].latex(),
#         "coef": components["coef"].latex(),
#     }
# )

# Create HTML version with percentage highlight
coef_display = components["coef"].simplified().as_decimal.latex()
literal_dir = "augmenté" if components["direction"].n == 1 else "diminué"


# Create HTML version with formula highlighted
statement_html = f"""
<div>
    Le prix d'un article est multiplié par ${coef_display}$. Calculer la variation relative.<br>
</div>
"""


# <span class="italic">La réponse doit être exprimée sous forme d'une fraction irréductible ou d'entier.</span>


# Define latex_0 for multiple possible answers
# The answer is already a percentage in fraction form (e.g., 99/200 = 49.5%)
# So we display both the fraction and the percentage notation
latex_0 = answer["maths_object"].latex()  # Fraction form: "99/200"
simplified_0 = (
    answer["maths_object"].simplified().latex()
)  # Simplified fraction: "99/200" or simpler

# Convert fraction to percentage by multiplying by 100
percent_value = answer["maths_object"] * tm.Integer(n=100)
percent_simplified = percent_value.simplified()

# If it's a nice decimal, show it as decimal, otherwise keep as fraction
if hasattr(percent_simplified, "as_decimal"):
    latex_1 = percent_simplified.as_decimal.latex() + r"\%"
    simplified_1 = percent_simplified.as_decimal.latex() + r"\%"  # Already simplified
else:
    latex_1 = percent_simplified.latex() + r"\%"
    simplified_1 = percent_simplified.latex() + r"\%"  # Already simplified

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-3]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0, latex_1],  # List to support multiple correct answers
            "simplified_latex": [simplified_0, simplified_1],  # List of simplified versions
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p": components["p"].latex(),
            "direction": components["direction"].latex(),
            "coef": components["coef"].latex(),
        },
    }
)
