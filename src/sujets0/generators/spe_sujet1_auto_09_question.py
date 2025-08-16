import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> generate_components(None, 0)
    {'x': Symbol(s='x'), 'c1': Integer(n=2), 'a2': Fraction(p=Integer(n=1), q=Integer(n=7)), 'b2': Fraction(p=Integer(n=1), q=Integer(n=7)), 'c2': Fraction(p=Integer(n=1), q=Integer(n=7)), 'a3': Fraction(p=Integer(n=9), q=Integer(n=8)), 'b3': Integer(n=2), 'c3': Decimal(p=4, q=8), 'expr1': Add(l=Pow(base=Symbol(s='x'), exp=Integer(n=2)), r=Mul(l=Integer(n=-1), r=Pow(base=Add(l=Symbol(s='x'), r=Integer(n=2)), exp=Integer(n=2)))), 'expr2': Add(l=Mul(l=Fraction(p=Integer(n=1), q=Integer(n=7)), r=Symbol(s='x')), r=Mul(l=Integer(n=-1), r=Add(l=Integer(n=-9), r=Fraction(p=Integer(n=1), q=Pow(base=Integer(n=5), exp=Fraction(p=Integer(n=1), q=Integer(n=2))))))), 'expr3': Fraction(p=Add(l=Mul(l=Fraction(p=Integer(n=9), q=Integer(n=8)), r=Symbol(s='x')), r=Integer(n=2)), q=Decimal(p=4, q=8))}
    """

    gen = tg.MathsGenerator(seed)
    x = tm.Symbol(s="x")
    # f1 = tm.Function(name="f1")
    # f2 = tm.Function(name="f2")
    # f3 = tm.Function(name="f3")
    c1 = gen.random_integer(-10, 10)
    a2, b2, c2 = (
        tm.Fraction(p=1, q=gen.random_integer(1, 10)),
        gen.random_integer(-10, 10),
        gen.random_integer(1, 10),
    )
    a3, b3, c3 = (
        tm.Fraction(p=gen.random_integer(1, 10), q=gen.random_integer(1, 10)),
        gen.random_integer(-10, 10),
        (gen.random_integer(0, 10) / gen.random_integer(1, 10)).as_decimal,
    )
    expr1 = x ** tm.Integer(n=2) - (x + c1) ** tm.Integer(n=2)
    expr2 = a2 * x - (b2 + tm.Integer(n=1) / (c2 ** (tm.Integer(n=1) / tm.Integer(n=2))))
    expr3 = (a3 * x + b3) / c3

    # TODO: there was a mistkae in the retunred context here 
    # but this did not affect solve or statement rendering so far
    # I keep it for history until Sel has merged stuff

    # return {
    #     "x": x,
    #     "c1": c1,
    #     "a2": a2,
    #     "b2": a2,
    #     "c2": a2,
    #     "a3": a3,
    #     "b3": b3,
    #     "c3": c3,
    #     "expr1": expr1,
    #     "expr2": expr2,
    #     "expr3": expr3,
    # }

    return {
        "x": x,
        "c1": c1,
        "a2": a2,
        "b2": b2,
        "c2": c2,
        "a3": a3,
        "b3": b3,
        "c3": c3,
        "expr1": expr1,
        "expr2": expr2,
        "expr3": expr3,
    }


def solve(*, x, c1, a2, b2, c2, a3, b3, c3, expr1, expr2, expr3):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=4)
    >>> answer["maths_object"].simplified()
    Integer(n=4)
    """
    coef1 = (tm.Integer(n=2) * c1).simplified()
    coef2 = a2
    coef3 = a3 / c3

    coef1_eval = coef1.eval()
    coef2_eval = coef2.eval()
    coef3_eval = coef3.eval()

    max_value = max(abs(coef1_eval), abs(coef2_eval), abs(coef3_eval))
    if max_value == abs(coef1_eval):
        answer = coef1
    elif max_value == abs(coef2_eval):
        answer = coef2
    elif max_value == abs(coef3_eval):
        answer = coef3

    return {
        "maths_object": answer,
    }


def render_question(*, x, c1, a2, b2, c2, a3, b3, c3, expr1, expr2, expr3):
    """[sujets0][spé][sujet-1][automatismes][question-?]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Parmi les 3 fonctions $$f1: x \\\\mapsto x^\\\\{2\\\\} -\\\\left(x + 2\\\\right)^\\\\{2\\\\}$$, $$f2: x \\\\mapsto \\\\\\\\dfrac\\\\{1\\\\}\\\\{7\\\\}x --9 + \\\\\\\\dfrac\\\\{1\\\\}\\\\{5^\\\\{\\\\\\\\dfrac\\\\{1\\\\}\\\\{2\\\\}\\\\}\\\\}$$, $$f3: x \\\\mapsto \\\\\\\\dfrac\\\\{\\\\\\\\dfrac\\\\{9\\\\}\\\\{8\\\\}x + 2\\\\}\\\\{0,5\\\\}$$ Au sein des fonctions affines parmis $f1, f2, f3$, quel est le coefficient directeur avec la plus grande valeur absolue ?'
    """

    statement = f"Parmi les 3 fonctions $$f1: {x.latex()} \\mapsto {expr1.latex()}$$, $$f2: {x.latex()} \\mapsto {expr2.latex()}$$, $$f3: {x.latex()} \\mapsto {expr3.latex()}$$ Au sein des fonctions affines parmis $f1, f2, f3$, quel est le coefficient directeur avec la plus grande valeur absolue ?"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-9]",
        "statement": question["statement"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "x": components["x"].latex(),
            "c1": components["c1"].latex(),
            "a2": components["a2"].latex(),
            "b2": components["b2"].latex(),
            "c2": components["c2"].latex(),
            "a3": components["a3"].latex(),
            "b3": components["b3"].latex(),
            "c3": components["c3"].latex(),
            "expr1": components["expr1"].latex(),
            "expr2": components["expr2"].latex(),
            "expr3": components["expr3"].latex(),
        },
    }
)
# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("Simplified answer:", answer["maths_object"].simplified())
# print("LaTeX representation:", answer["maths_object"].latex())
