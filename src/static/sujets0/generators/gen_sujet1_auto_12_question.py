import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-1][automatismes][question-12]
    >>> generate_components(None, 0)
    {'f': Function(name=moyenne), 'a': Integer(n=-2), 'b': Integer(n=94), 'c': Integer(n=7)}
    >>> generate_components(None, 2)
    {'f': Function(name=médiane), 'a': Integer(n=-86), 'b': Integer(n=-77), 'c': Integer(n=-79)}
    """

    gen = tg.MathsGenerator(seed)

    a = gen.random_integer(-100, 100)
    b = gen.random_integer(-100, 100)
    c = gen.random_integer(-100, 100)

    f = gen.random_element_from(["moyenne", "médiane"])

    f = tm.Function(name=f)

    return {
        "f": f,
        "a": a,
        "b": b,
        "c": c,
    }


def solve(*, f, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Fraction(p=Add(l=Add(l=Integer(n=-2), r=Integer(n=94)), r=Integer(n=7)), q=Integer(n=3))
    >>> answer["maths_object"].simplified()
    Integer(n=33)
    >>> components= generate_components(None, 2)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Integer(n=-79)
    >>> answer["maths_object"].simplified()
    Integer(n=-79)
    """
    if f.name == "moyenne":
        maths_object = (a + b + c) / tm.Integer(n=3)
    elif f.name == "médiane":
        l = sorted([a, b, c], key=lambda x: x.eval())
        maths_object = l[1]
    else:
        raise ValueError(f"Unknown function {f.name}")
    return {"maths_object": maths_object}


def render_question(*, f, a, b, c):
    """[sujets0][gén][sujet-1][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'Calcluer la $moyenne$ de la série A : -2 ; 7 ; 94'
    """
    l = sorted([a, b, c], key=lambda x: x.eval())
    statement = f"Calculer la {f.latex()} de la série $A = {{ {l[0].latex()} ; {l[1].latex()} ; {l[2].latex()} }}$"
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-1][automatismes][question-12]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "f": components["f"].latex(),
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "c": components["c"].latex(),
        },
    }
)
