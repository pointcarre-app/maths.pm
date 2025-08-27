import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-7]
    >>> generate_components(None, 0)
    {'n': Integer(n=49), 'x': Symbol(s='x'), 'relation': StrictGreaterThan(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Integer(n=49))}
    """

    gen = tg.MathsGenerator(seed)
    n = gen.random_integer(1, 11)  # for being nice with the graph + not degenerate case
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
        elements=[x < -(n ** tm.Fraction(p=1, q=2)), x > n ** tm.Fraction(p=1, q=2)]
    )
    return {
        "maths_object": answer,
        "left_interval_left_bound_latex": "-\\infty",
        "left_interval_right_bound_latex": (-(n ** tm.Fraction(p=1, q=2))).simplified().latex(),
        "right_interval_left_bound_latex": (n ** tm.Fraction(p=1, q=2)).simplified().latex(),
        "right_interval_right_bound_latex": "\\infty",
    }


def render_question(*, n, x, relation):
    r"""[sujets0][spé][sujet-1][automatismes][question-7]
    >>> n, x = tm.Integer(n=49), tm.Symbol(s='x')
    >>> relation = tm.StrictGreaterThan(l=tm.Pow(base=x, exp=tm.Integer(n=2)), r=n)
    >>> statement = render_question(n=n, x=x, relation=relation)
    >>> statement["statement"]
    "On a représenté ci-contre la parabole d'équation $y = x^2$. l'inéquation $x^2 > 49$, sur $mathbb{R}$. ."
    """

    statement = (
        "On a représenté ci-contre la parabole d'équation $y = x^2$.  Résoudre sur $\\mathbb{R}$ l'inéquation : "
        + "$"
        + relation.latex()
        + "$"
    )
    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with graph reference and equation
statement_html = f"<div>{question['statement']}</div>"

# Define latex_0 for multiple possible answers
latex_0 = f"x \\in \\left] {answer['left_interval_left_bound_latex']}, {answer['left_interval_right_bound_latex']} \\right[ \\cup \\left] {answer['right_interval_left_bound_latex']}, {answer['right_interval_right_bound_latex']} \\right["

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-7]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": [latex_0],  # hmm hmm
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
