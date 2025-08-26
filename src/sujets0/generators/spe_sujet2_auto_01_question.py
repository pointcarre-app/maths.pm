import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-1]
    >>> generate_components(None, 0)
    {'p_A': Fraction(p=Integer(n=7), q=Integer(n=10)), 'p_B_if_A': Fraction(p=Integer(n=7), q=Integer(n=10)), 'p_B_if_notA': Fraction(p=Integer(n=1), q=Integer(n=10))}"""
    # NOTE: use 12 as it allows nice divisions by /2 and /3,

    gen = tg.MathsGenerator(seed)
    p_A = gen.random_integer(1, 10) / tm.Integer(n=10)
    p_B_if_A = gen.random_integer(1, 10) / tm.Integer(n=10)
    p_B_if_notA = gen.random_integer(1, 10) / tm.Integer(n=10)

    return {
        "p_A": p_A,
        "p_B_if_A": p_B_if_A,
        "p_B_if_notA": p_B_if_notA,
    }


def solve(*, p_A, p_B_if_A, p_B_if_notA):
    """[sujets0][spé][sujet-2][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Fraction(p=Integer(n=7), q=Integer(n=10)), r=Add(l=Fraction(p=Integer(n=7), q=Integer(n=10)), r=Fraction(p=Integer(n=1), q=Integer(n=10))))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=14), q=Integer(n=25))
    """
    maths_object = p_A * (p_B_if_A + p_B_if_notA)
    return {"maths_object": maths_object}


def render_question(*, p_A, p_B_if_A, p_B_if_notA):
    r"""[sujets0][spé][sujet-2][automatismes][question-1]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "On considère l'arbre de probabilité ci-dessous. Calculer la proabilité de B."
    """

    # NOTE mad: long string still need to be one line, otherwise doctest execution with backend executor are broken because of the try indentation it makes
    statement = "On considère l'arbre de probabilité ci-dessous. Calculer la proabilité de B."
    graph_description = "A proability tree with event A followed by continonal proabillity of B"
    return {
        "statement": statement,
        "graph_description": graph_description,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with probability tree description
statement_html = f'''
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="text-sm mb-3">
            On considère l'arbre de probabilité ci-dessous.
        </div>
        <div class="alert alert-info">
            <span class="text-xs">Note: {question.get('graph_description', 'Un arbre de probabilité avec l\''événement A suivi de la probabilité conditionnelle de B')}</span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Calculer la probabilité de B.
        </div>
    </div>
</div>
'''

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-1]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "p_A": components["p_A"].latex(),
            "p_B_if_A": components["p_B_if_A"].latex(),
            "p_B_if_notA": components["p_B_if_notA"].latex(),
        },
    }
)
