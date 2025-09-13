import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-10]
    >>> generate_components(None, 0)
    {'a1': Integer(n=2), 'b1': Integer(n=-9), 'a2': Integer(n=3), 'b2': Integer(n=-2), 'root1': Mul(l=Integer(n=-1), r=Fraction(p=Integer(n=-9), q=Integer(n=2))), 'root2': Fraction(p=Integer(n=-2), q=Integer(n=3)), 'f': Function(name=f), 'interval': Interval(l=Fraction(p=Integer(n=-2), q=Integer(n=3)), r=Inf(), left_open=True, right_open=True), 'x': Symbol(s='x')}
    """

    gen = tg.MathsGenerator(seed)
    a1, a2 = tm.Integer(n=0), tm.Integer(n=0)
    while a1.n == 0 or a2.n == 0:  # ✅ CORRECT: ensure BOTH are non-zero
        a1 = gen.random_integer(-10, 10)
        a2 = gen.random_integer(-10, 10)

    b1 = gen.random_integer(-10, 10)
    b2 = gen.random_integer(-10, 10)

    root1, root2 = -(b1 / a1), (b2 / a2)
    f = tm.Function(name="f")
    x = tm.Symbol(s="x")

    # 🧂 magic solutio ?
    if root1.eval() > root2.eval():  # ✅ Reverse the condition
        root1, root2 = root2, root1
    i = gen.random_element_from([0, 1, 2])
    if i == 0:
        interval = tm.Interval(l=-tm.Inf(), r=root1, left_open=True, right_open=True)
    elif i == 1:
        interval = tm.Interval(l=root1, r=root2, left_open=True, right_open=True)
    else:
        interval = tm.Interval(l=root2, r=tm.Inf(), left_open=True, right_open=True)
    return {
        "a1": a1,
        "b1": b1,
        "a2": a2,
        "b2": b2,
        "root1": root1,
        "root2": root2,
        "f": f,
        "interval": interval,
        "x": x,
    }


def solve(*, root1, root2, a1, b1, a2, b2, f, interval, x):
    """[sujets0][spé][sujet-2][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    StrictGreaterThan(l=Function(name=f)(Symbol(s='x')), r=Integer(n=0))
    """

    if (a1 * a2).eval() > 0:
        if interval.l == -tm.Inf() or interval.r == tm.Inf():
            maths_object = f(x) > tm.Integer(n=0)
        else:
            maths_object = f(x) < tm.Integer(n=0)
    else:
        if interval.l == -tm.Inf() or interval.r == tm.Inf():
            maths_object = f(x) < tm.Integer(n=0)
        else:
            maths_object = f(x) > tm.Integer(n=0)
    # z = (a1*x - root1) * (x - root2) * (x - root3)
    # if z.eval() > 0:
    #     maths_object = x * f(x) > tm.Integer(n=0)
    # else:
    #     maths_object = x * f(x) < tm.Integer(n=0)

    return {"maths_object": maths_object}


def render_question(*, root1, root2, a1, b1, a2, b2, f, interval, x):
    """[sujets0][spé][sujet-2][automatismes][question-10]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "La fonction ${f}$ définie sur $\\\\\\\\mathbb\\\\{R\\\\}$ par $f(x) = \\\\left(2x -9\\\\right) \\\\times \\\\left(3x -2\\\\right)$. Quel est le signe de f sur l'intervalle $\\\\\\\\lbracket-\\\\\\\\dfrac\\\\{2\\\\}\\\\{3\\\\};\\\\infty\\\\rbracket$ ?"
    """

    func_def = tm.Equality(l=f(x), r=(a1 * x + b1) * (a2 * x + b2))

    statement = f"""La fonction ${f.name}$ définie sur $\\mathbb{{R}}$ par ${func_def.latex().replace("\\times", "")}$. """
    statement += "<br>Établir le tableau de signes de $f$ sur $\\mathbb{R}$."
    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with function definition
func_def = tm.Equality(
    l=components["f"](components["x"]),
    r=(components["a1"] * components["x"] + components["b1"])
    * (components["a2"] * components["x"] + components["b2"]),
)

statement_html = f"<div>{question['statement']}</div>"

missive_dict = {
    "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-10]",
    "statement": question["statement"],
    "statement_html": statement_html,
    "answer": {
        "latex": answer["maths_object"].latex(),
        "simplified_latex": answer["maths_object"].simplified().latex(),
        "sympy_exp_data": answer["maths_object"].sympy_expr_data,
        "formal_repr": repr(answer["maths_object"]),
    },
    "components": {
        "root1": components["root1"].latex(),
        "root2": components["root2"].latex(),
        "a1": components["a1"].latex(),
        "a2": components["a2"].latex(),
        "b1": components["b1"].latex(),
        "b2": components["b2"].latex(),
        "interval": components["interval"].latex(),
        "x": components["x"].latex(),
        "f": components["f"].name,
    },
}


try:
    missive(missive_dict)
except NameError:
    from pprint import pprint

    pprint(missive_dict)
