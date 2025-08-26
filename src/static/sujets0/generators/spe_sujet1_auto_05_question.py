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
    statement = f"""On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans le tableau suivant:\n- Face numéro 1: ${str_probabilities[0]}$\n- Face numéro 2: ${str_probabilities[0]}$\n- Face numéro 3: ${str_probabilities[0]}$\n- Face numéro 4: $x$\n"""

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with a proper table
str_probs = []
for p in components["probabilities"][:-1]:
    p_simple = p.simplified()
    str_probs.append(p_simple.latex())

statement_html = """
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <p class="text-sm mb-3">On lance un dé à 4 faces. La probabilité d'obtenir chacune des faces est donnée dans le tableau suivant:</p>
        <div class="overflow-x-auto">
            <table class="table table-compact w-full">
                <thead>
                    <tr>
                        <th class="text-center">Face</th>
                        <th class="text-center">1</th>
                        <th class="text-center">2</th>
                        <th class="text-center">3</th>
                        <th class="text-center">4</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="font-semibold">Probabilité</td>
                        <td class="text-center">${str_probs[0]}$</td>
                        <td class="text-center">${str_probs[1]}$</td>
                        <td class="text-center">${str_probs[2]}$</td>
                        <td class="text-center"><span class="badge badge-primary">$x$</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Quelle est la valeur de $x$ ?
        </div>
    </div>
</div>
"""

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-5]",
        "statement": question["statement"],
        "statement_html": statement_html,
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
