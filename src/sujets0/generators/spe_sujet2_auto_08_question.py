import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> generate_components(None, 0)
    {'a': Integer(n=1), 'c': Integer(n=1), 'x': Symbol(s='x'), 'y': Symbol(s='y')}
    """

    gen = tg.MathsGenerator(seed)

    # a = gen.random_integer(1, 10)
    dir1 = gen.random_element_from([-1, 1])
    dir2 = gen.random_element_from([-1, 1])
    a = tm.Integer(n=dir1)
    c = gen.random_integer(1, 10)
    c = tm.Integer(n=dir2) * c
    c = c.simplified()
    x = tm.Symbol(s="x")
    y = tm.Symbol(s="y")

    return {
        "a": a,
        "c": c,
        "x": x,
        "y": y,
    }


def solve(*, x, y, a, c):
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Equality(l=Add(l=Add(l=Mul(l=Integer(n=-1), r=Symbol(s='x')), r=Symbol(s='y')), r=Integer(n=-1)), r=Integer(n=0))
    >>> answer["maths_object"].simplified()
    Equality(l=Add(l=Mul(l=Integer(n=-1), r=Symbol(s='x')), r=Add(l=Symbol(s='y'), r=Integer(n=-1))), r=Integer(n=0))
    """
    maths_object = tm.Equality(l=-a * x + y - c, r=tm.Integer(n=0))
    return {"maths_object": maths_object}


## TODO selfb : visibility (prévise ordonnée à l'origine entier?? bof)


def render_question(*, x, y, a, c):
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> components= generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "La courbe ci-contre représente un droite dont le coefficient directeur vaut 1, en valeur absolue. Donner l'équation de la droite sous la forme $ax + by + c = 0$."
    >>> statement["graph_description"]
    "La droite d\'équation y = 1x + 1"
    """
    statement = f"La courbe ci-contre représente une droite dont le coefficient directeur vaut $1$, en valeur absolue (c'est à dire qu'il vaut $1$ ou $-1$). Donner l'équation de la droite sous la forme $a{x.latex()} + b{y.latex()} + c = 0$."

    # graph_description = f"La droite d'équation y = {a.n}x + {c.n}"

    return {"statement": statement}


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


print(components | answer | question)


# Create HTML version with graph description
statement_html = f"<div>{question['statement']}</div>"

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-8]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "a": components["a"].latex(),
            "c": components["c"].latex(),
            "x": components["x"].latex(),
            "y": components["y"].latex(),
        },
    }
)
