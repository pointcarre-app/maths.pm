import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


# TODO selfb : too complex

# Current code produces:
# p = (x*y)^(n1+n2)
# q = x^n1
# Result: ((xy)^(n1+n2))/x^n1
# To get ((xy)^n)/x^n, you need:


# HYPERCUBE


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-?]
    >>> generate_components(None, 0)
    {'x': Integer(n=3), 'y': Integer(n=2), 'n1': Integer(n=5), 'n2': Integer(n=9), 'expr': Fraction(p=Pow(base=Integer(n=6), exp=Integer(n=14)), q=Pow(base=Integer(n=3), exp=Integer(n=5)))}
    """

    gen = tg.MathsGenerator(seed)

    x = gen.random_element_from([2, 3, 4, 5, 6])
    y = gen.random_element_from([2, 3])
    n1 = gen.random_integer(2, 3)  # no 1
    n2 = gen.random_integer(2, 4)  # no 1
    x, y = tm.Integer(n=x), tm.Integer(n=y)

    # TODO: difficulty could swith p and q
    p = tm.Pow(base=(x * y).simplified(), exp=(n1 * n2).simplified())
    q = tm.Pow(base=x, exp=n1)
    expr = tm.Fraction(p=p, q=q)

    return {"x": x, "y": y, "n1": n1, "n2": n2, "expr": expr}


def solve(*, x, y, n1, n2, expr):
    """[sujets0][spé][sujet-2][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Pow(base=Integer(n=3), exp=Integer(n=4)), r=Pow(base=Integer(n=2), exp=Integer(n=9)))
    >>> answer["maths_object"].simplified()
    Integer(n=41472)
    """
    answer = tm.Pow(base=x, exp=(n2 - n1).simplified()) * tm.Pow(base=y, exp=n2)
    return {
        "maths_object": answer,
    }


def render_question(*, x, y, n1, n2, expr):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'On considère le nombre $N=\\\\\\\\dfrac\\\\{6^\\\\{14\\\\}\\\\}\\\\{3^\\\\{5\\\\}\\\\}$. Exprimer $N$ sous la forme d'un entier.'
    """

    statement = (
        f"On considère le nombre $N={expr.latex()}$. Exprimer $N$ sous la forme d'un entier."
    )

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with prime factorization
statement_html = f"<div>{question['statement']}</div>"

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-5]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "y": components["y"].latex(),
            "n1": components["n1"].latex(),
            "n2": components["n2"].latex(),
            "expr": components["expr"].latex(),
        },
    }
)
