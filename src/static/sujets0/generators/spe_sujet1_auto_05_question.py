import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-5]
    >>> generate_components(None, 0)
    {'probabilities': (Fraction(p=Integer(n=13), q=Integer(n=24)), Fraction(p=Integer(n=7), q=Integer(n=24)), Fraction(p=Integer(n=1), q=Integer(n=24)), Fraction(p=Integer(n=3), q=Integer(n=24)))}
    """
    # NOTE: use 24 as it allows nice divisions by /2 and /3,

    gen = tg.MathsGenerator(seed)
    probabilities = gen.discrete_dirichlet_dist(n=4, q=24, exclude_zero=True)

    return {
        "probabilities": probabilities,
    }


def solve(*, probabilities: list[tm.Fraction]):
    """[sujets0][spé][sujet-1][automatismes][question-5]
    >>> probabilities = [tm.Fraction(p=tm.Integer(n=13), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=24))]
    >>> probabilities = tm.MathsCollection(elements=probabilities)
    >>> answer = solve(probabilities=probabilities)
    >>> answer["maths_object"]
    Fraction(p=Integer(n=3), q=Integer(n=24))
    >>> answer["maths_object"].simplified()
    Fraction(p=Integer(n=1), q=Integer(n=8))
    """
    maths_object = probabilities[-1]
    return {"maths_object": maths_object}


def render_question(*, probabilities: list[tm.Fraction]):
    r"""[sujets0][spé][sujet-1][automatismes][question-5z]
    >>> probabilities = [tm.Fraction(p=tm.Integer(n=13), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=7), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=1), q=tm.Integer(n=24)), tm.Fraction(p=tm.Integer(n=3), q=tm.Integer(n=24))]
    >>> statement = render_question(probabilities=probabilities)
    >>> statement["statement"]
    "On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans le tableau suivant:\n- Face numéro 1: $\\\\dfrac\\{13\\}\\{24\\}$\n- Face numéro 2: $\\\\dfrac\\{13\\}\\{24\\}$\n- Face numéro 3: $\\\\dfrac\\{13\\}\\{24\\}$\n- Face numéro 4: $x$\n"
    """

    str_probabilities = []

    for p in probabilities[:-1]:
        p_simple = p.simplified()
        prime_factors = set(p_simple.q.primefactors)
        if prime_factors.difference({2, 5}):
            str_probabilities.append(p_simple.latex())
        else:
            # TODO: should be a decimal
            str_probabilities.append(p_simple.latex())

    # NOTE mad: long string still need to be one line, otherwise doctest execution with backend executor are broken because of the try indentation it makes
    statement = f"""On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans ce tableau suivant :\n- Face numéro 1: ${str_probabilities[0]}$\n- Face numéro 2: ${str_probabilities[1]}$\n- Face numéro 3: ${str_probabilities[2]}$\n- Face numéro 4: $x$\n"""

    statement_html = f"""<div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    <div style='flex: 1; min-width: 250px;'>On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans le tableau ci-contre. Calculer $x$.</div>
    <div style='flex: 0 1 auto;'>    
        <table style="margin: 0; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">Face</th>
                    <th style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">1</th>
                    <th style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">2</th>
                    <th style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">3</th>
                    <th style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">4</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">Probabilité</td>
                    <td style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">${str_probabilities[0]}$</td>
                    <td style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">${str_probabilities[1]}$</td>
                    <td style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">${str_probabilities[2]}$</td>
                    <td style="padding: 4px; font-size:0.85rem !important; text-align: center; border: 1px solid currentColor;">$x$</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
"""

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-5]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "mask": "x=",
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "probabilities": components["probabilities"].latex(),
        },
    }
)
