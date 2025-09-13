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
    p = gen.random_integer(1, 10)

    # TODO: we could randomize on decimal vs fraction

    a = tm.Fraction(p=p.n, q=10)  # tm.Integer(n=100)
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
    answer = tm.group_terms(expr)
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

    exp_latex_decimal = f"(x+{a.as_decimal.latex().replace('.', ',')})^{2}"

    statement = f"Quelle est l'expression développée de ${exp_latex_decimal}$ ?"

    # statement = ""
    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with expression to expand
statement_html = f"<div>{question['statement']}</div>"


first_order_term_latex = (
    (tm.Integer(n=2) * components["a"]).simplified().as_decimal.latex().replace(".", ",")
)
zero_order_term_latex = (
    (components["a"] ** tm.Integer(n=2)).simplified().as_decimal.latex().replace(".", ",")
)


missive_dict = {
    "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-11]",
    "statement": question["statement"],
    "statement_html": statement_html,
    "answer": {
        "latex": answer["maths_object"].latex(),
        "simplified_latex": [
            answer["maths_object"].latex(),
            "x^{2} + " + f"{first_order_term_latex}x + {zero_order_term_latex}",
        ],
        "sympy_exp_data": answer["maths_object"].sympy_expr_data,
        "formal_repr": repr(answer["maths_object"]),
    },
    "components": {
        "x": components["x"].latex(),
        "a": components["a"].latex(),
        "expr": components["expr"].latex(),
    },
}


try:
    missive(missive_dict)
except NameError:
    from pprint import pprint

    pprint(missive_dict)
