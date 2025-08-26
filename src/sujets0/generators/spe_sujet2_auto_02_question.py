import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED

# TODO: variabiliser sur le format


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-2]
    >>> generate_components(None, 0)
    {'price': Mul(l=Integer(n=13), r=Integer(n=10)), 'p': Fraction(p=Integer(n=7), q=Integer(n=10)), 'direction': Integer(n=-1)}
    """
    gen = tg.MathsGenerator(seed)

    price = gen.random_integer(1, 20) * tm.Integer(n=10)
    p = gen.random_integer(1, 9)
    p = tm.Fraction(p=p, q=10)
    direction = tm.Integer(n=gen.random_element_from((-1, 1)))

    return {
        "price": price,
        "p": p,
        "direction": direction,
    }


def solve(*, price, p, direction):
    """[sujets0][spé][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Mul(l=Mul(l=Integer(n=13), r=Integer(n=10)), r=Add(l=Integer(n=1), r=Mul(l=Integer(n=-1), r=Fraction(p=Integer(n=7), q=Integer(n=10)))))
    >>> answer["maths_object"].simplified()
    Integer(n=39)
    """
    maths_object = price * (tm.Integer(n=1) + direction * p)
    return {"maths_object": maths_object}


def render_question(*, price, p, direction):
    r"""[sujets0][spé][sujet-2][automatismes][question-2]
    >>> components = generate_components(None, 0)
    >>> statement = render_question(**components)
    >>> statement["statement"]
    "Le prix d'un article est de $130$ euros. Son prix diminue de $70$\\%. Quel est le nouveau prix de l'article ?"
    """
    literal_direction = {
        -1: "diminue",
        1: "augmente",
    }

    p = p.simplified().as_percent

    statement = f"Le prix d'un article est de ${price.simplified().latex()}$ euros. Son prix {literal_direction[direction.n]} de ${p.latex()}$\\%. Quel est le nouveau prix de l'article ?"
    return {
        "statement": statement,
    }


# def correct():
#     r"""
#     >>> import teachers.corrector as tc
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> user_answer_latex=r"49,5"
#     >>> correction = tc.main(user_answer_latex, **answer)
#     >>> assert correction["cleaned_latex_are_equal"]
#     """


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with price change
literal_direction = "diminue" if components["direction"].n == -1 else "augmente"
p_percent = components["p"].simplified().as_percent

statement_html = f"""
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <div class="stats stats-vertical shadow mb-3">
            <div class="stat">
                <div class="stat-title">Prix initial</div>
                <div class="stat-value text-primary">${{components["price"].simplified().latex()}}$ €</div>
            </div>
            <div class="stat">
                <div class="stat-title">Variation</div>
                <div class="stat-value text-{"error" if components["direction"].n == -1 else "success"}">
                    {"↓" if components["direction"].n == -1 else "↑"} ${{p_percent.latex()}}\\%$
                </div>
                <div class="stat-desc">{literal_direction}</div>
            </div>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Quel est le nouveau prix de l'article ?
        </div>
    </div>
</div>
"""

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-2]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "price": components["price"].latex(),
            "p": components["p"].latex(),
            "direction": components["direction"].latex(),
        },
    }
)
