import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-12]
    >>> generate_components(None, 0)
    {'v': Symbol(s='v'), 'a': Symbol(s='a'), 'r': Symbol(s='R'), 'expr': Equality(l=Symbol(s='a'), r=Fraction(p=Pow(base=Symbol(s='v'), exp=Integer(n=2)), q=Symbol(s='R')))}
    """

    gen = tg.MathsGenerator(seed)
    v = tm.Symbol(s="v")
    a = tm.Symbol(s="a")
    r = tm.Symbol(s="R")
    expr = tm.Equality(l=a, r=tm.Fraction(p=tm.Pow(base=v, exp=tm.Integer(n=2)), q=r))

    return {"v": v, "a": a, "r": r, "expr": expr}


def solve(*, v, a, r, expr):
    """[sujets0][spé][sujet-2][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Pow(base=Mul(l=Symbol(s='a'), r=Symbol(s='R')), exp=Fraction(p=Integer(n=1), q=Integer(n=2)))
    >>> answer["maths_object"].simplified()
    Pow(base=Mul(l=Symbol(s='a'), r=Symbol(s='R')), exp=Fraction(p=Integer(n=1), q=Integer(n=2)))
    """
    answer = tm.Pow(base=tm.Mul(l=a, r=r), exp=tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=2)))
    return {
        "maths_object": answer,
    }


def render_question(*, v, a, r, expr):
    """[sujets0][spé][sujet-2][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Si un point mobile suit une trajectoire circulaire de rayon $R$, en mètre ($m$), son accélération centripète $a$ (en $m/s^2$) s'exprime en fonction de la vitesse $v$ (en $m/s$) de la manière suivante: $$a = \\\\\\\\dfrac\\\\{v^\\\\{2\\\\}\\\\}\\\\{R\\\\}$$ Exprimer $v$ en fonction de a et R."
    """

    statement = (
        "Si un point mobile suit une trajectoire circulaire de rayon $R$, en mètre ($m$), son accélération centripète $a$ (en $m/s^2$) s'exprime en fonction de la vitesse $v$ (en $m/s$) de la manière suivante: $$"
        + expr.latex()
        + "$$ Exprimer $v$ en fonction de "
        + f"${a.latex()}$"
        + " et "
        + f"${r.latex()}$"
        + "."
    )

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with physics formula
statement_html = f"<div>{question['statement']}</div>"

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-12]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "v": components["v"].latex(),
            "a": components["a"].latex(),
            "r": components["r"].latex(),
            "expr": components["expr"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("Simplified answer:", answer["maths_object"].simplified())
# print("LaTeX representation:", answer["maths_object"].latex())
