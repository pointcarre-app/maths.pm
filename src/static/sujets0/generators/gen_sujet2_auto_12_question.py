import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-12]
    >>> generate_components(None, 0)
    {'center': Integer(n=-1), 'disp_low': Integer(n=6), 'disp_high': Integer(n=12), 'a': (Integer(n=-13), Integer(n=-1), Integer(n=-1), Integer(n=11)), 'b': (Integer(n=-7), Integer(n=-1), Integer(n=-1), Integer(n=5))}
    """

    gen = tg.MathsGenerator(seed)

    center = gen.random_integer(-50, 50)

    disp_low = gen.random_integer(0, 9)
    disp_high = gen.random_integer(10, 50)

    l_low = [center - disp_low, center, center, center + disp_low]
    l_high = [center - disp_high, center, center, center + disp_high]
    l_low = [e.simplified() for e in l_low]
    l_high = [e.simplified() for e in l_high]

    ix = gen.random_element_from([0, 1])

    if ix == 0:
        a = tm.MathsCollection(elements=l_low)
        b = tm.MathsCollection(elements=l_high)
    else:
        a = tm.MathsCollection(elements=l_high)
        b = tm.MathsCollection(elements=l_low)

    return {
        "center": center,
        "disp_low": disp_low,
        "disp_high": disp_high,
        "a": a,
        "b": b,
    }


def solve(*, center, disp_low, disp_high, a, b):
    """[sujets0][gén][sujet-2][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Symbol(s='A')
    >>> answer["maths_object"].simplified()
    Symbol(s='A')
    """
    if a[0].n < b[0].n:
        maths_object = tm.Symbol(s="A")
    else:
        maths_object = tm.Symbol(s="B")
    return {"maths_object": maths_object}


def render_question(*, center, disp_low, disp_high, a, b):
    """[sujets0][gén][sujet-2][automatismes][question-12]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    'On considère les deux séries $A=-13 ; -1 ; -1 ; 11$  et $B=-7 ; -1 ; -1 ; 5$. Quelle est celle avec le plus grand écart type ?'
    """

    a_latex = " ; ".join(e.latex() for e in a.elements)
    b_latex = " ; ".join(e.latex() for e in b.elements)

    statement = f"On considère les deux séries $A={a_latex}$  et $B={b_latex}$. Quelle est celle avec le plus grand écart type ?"
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
        "beacon": "[1ere][sujets0][gén][sujet-2][automatismes][question-12]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "b": components["b"].latex(),
            "center": components["center"].latex(),
            "disp_low": components["disp_low"].latex(),
            "disp_high": components["disp_high"].latex(),
        },
    }
)
