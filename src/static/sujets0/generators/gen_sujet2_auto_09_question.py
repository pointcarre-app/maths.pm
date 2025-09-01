# import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-9]
    >>> generate_components(None, 0)
    {'v': Symbol(s='V'), 'h': Symbol(s='h'), 'r': Symbol(s='r'), 'expr': Equality(l=Symbol(s='V'), r=Mul(l=Mul(l=Mul(l=Fraction(p=Integer(n=1), q=Integer(n=3)), r=Constant(c='Pi')), r=Pow(base=Symbol(s='r'), exp=Integer(n=2))), r=Symbol(s='h')))}
    """

    # gen = tg.MathsGenerator(seed)
    v = tm.Symbol(s="V")
    r = tm.Symbol(s="r")
    h = tm.Symbol(s="h")
    expr = tm.Equality(
        l=v,
        r=tm.Fraction(p=1, q=3) * tm.Pi() * r ** tm.Integer(n=2) * h,
    )
    # expr = tm.Equality(l=a, r=tm.Fraction(p=tm.Pow(base=v, exp=tm.Integer(n=2)), q=r))

    return {"v": v, "h": h, "r": r, "expr": expr}


def solve(*, v, h, r, expr):
    """[sujets0][gén][sujet-2][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Mul(l=Integer(n=3), r=Symbol(s='V')), q=Mul(l=Constant(c='Pi'), r=Pow(base=Symbol(s='r'), exp=Integer(n=2))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Mul(l=Integer(n=3), r=Symbol(s='V')), q=Mul(l=Constant(c='Pi'), r=Pow(base=Symbol(s='r'), exp=Integer(n=2))))
    """
    maths_object = tm.Integer(n=3) * v / (tm.Pi() * r ** tm.Integer(n=2))

    return {
        "maths_object": maths_object,
    }


def render_question(*, v, h, r, expr):
    """[sujets0][gén][sujet-2][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le volume $V$ d\'un cône de hauteur $h$ et de rayon $r$ est $V = \\\\dfrac{1}{3}\\\\pi r^{2}h$. Isoler $h$."
    """

    statement = f"Le volume ${v.latex()}$ d'un cône de hauteur ${h.latex()}$ et de rayon ${r.latex()}$ est ${expr.latex()}$. Isoler $h$."
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-9]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "v": components["v"].latex(),
            "h": components["h"].latex(),
            "r": components["r"].latex(),
            "expr": components["expr"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("Simplified answer:", answer["maths_object"].simplified())
# print("LaTeX representation:", answer["maths_object"].latex())
