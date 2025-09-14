import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-3][automatismes][question-9]
    Génère une question sur les pourcentages simples.
    """
    gen = tg.MathsGenerator(seed)

    # Génère un prix initial entre 10 et 100 (multiple de 5)
    price = gen.random_integer(2, 20) * tm.Integer(n=5)

    # Génère un pourcentage de réduction (5%, 10%, 15%, 20%, 25%, 30%, 40%, 50%)
    reduction_options = [5, 10, 15, 20, 25, 30, 40, 50]
    reduction_value = gen.random_element_from(reduction_options)
    reduction = tm.Integer(n=reduction_value)

    return {
        "price": price,
        "reduction": reduction,
    }


def solve(*, price, reduction):
    """[sujets0][gén][sujet-3][automatismes][question-9]
    Calcule le prix après réduction.
    """
    # Prix après réduction = prix * (1 - reduction/100)
    reduction_fraction = reduction / tm.Integer(n=100)
    multiplier = tm.Integer(n=1) - reduction_fraction
    final_price = price * multiplier

    return {
        "final_price": final_price,
        "simplified_price": final_price.simplified(),
    }


def render_question(*, price, reduction):
    """[sujets0][gén][sujet-3][automatismes][question-9]
    Génère l'énoncé de la question.
    """
    statement = f"Un article coûte ${price.simplified().latex()}$ €. Il bénéficie d'une réduction de ${reduction.latex()}\\%$. Quel est son nouveau prix ?"
    statement_html = f"<div>{statement}</div>"

    return {
        "statement": statement,
        "statement_html": statement_html,
    }


# Generate and solve
components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


missive(
    {
        "beacon": "[1ere][sujets0][gén][sujet-3][automatismes][question-9]",
        "statement": question["statement"],
        "statement_html": question["statement_html"],
        "answer": {
            "latex": answer["final_price"].latex(),
            "simplified_latex": answer["simplified_price"].latex(),
            "sympy_exp_data": answer["final_price"].sympy_expr_data,
            "formal_repr": repr(answer["final_price"]),
        },
        "components": {
            "price": components["price"].latex(),
            "reduction": components["reduction"].latex(),
        },
    }
)
