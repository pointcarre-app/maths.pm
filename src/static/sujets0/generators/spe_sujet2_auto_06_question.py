import random

import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


# Note selfb : we must adapt thoroughly
# they dont have computator


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    gen = tg.MathsGenerator(seed)

    # Generate a multiple of 18 for nice division by 36
    multiple = gen.random_integer(1, 4)  # 1 to 4
    prefix_joules_to_multiply_by_power = (tm.Integer(n=18) * multiple).simplified()

    # Choose power of 10 (either 10^6 or 10^12)
    power = tm.Integer(n=random.choice([6, 8]))

    # Total energy in Joules
    energy_joules = prefix_joules_to_multiply_by_power * (tm.Integer(n=10) ** power)

    # Conversion factor: 1 kWh = 3.6×10^6 J
    factor = tm.Fraction(p=36, q=10) * (tm.Integer(n=10) ** tm.Integer(n=6))

    return {
        "prefix_joules_to_multiply_by_power": prefix_joules_to_multiply_by_power,
        "power": power,
        "energy_joules": energy_joules,
        "factor": factor,
    }


def solve(*, prefix_joules_to_multiply_by_power, power, energy_joules, factor, **kwargs):
    """Convert Joules to kWh
    energy_joules / factor = kWh
    """
    # Perform the conversion: Joules / (3.6×10^6 J/kWh) = kWh
    answer = energy_joules / factor
    return {"maths_object": answer}


# def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
#     """[sujets0][spé][sujet-2][automatismes][question-6]
#     >>> generate_components(None, 0)
#     {'k': Mul(l=Integer(n=50), r=Pow(base=Integer(n=10), exp=Integer(n=7))), 'factor': Mul(l=Decimal(p=36, q=10), r=Pow(base=Integer(n=10), exp=Integer(n=6)))}
#     """

#     gen = tg.MathsGenerator(seed)

#     x = gen.random_integer(1, 100)
#     x = x.simplified()
#     n = gen.random_integer(1, 8)
#     k = x * (tm.Integer(n=10) ** n)

#     # TODO: we should be able to randomly choose conversion when we have proper units system
#     factor = tm.Decimal(p=36, q=10) * tm.Pow(base=tm.Integer(n=10), exp=tm.Integer(n=6))

#     return {
#         "k": k,
#         "factor": factor,
#     }


# def solve(*, k, factor):
#     """[sujets0][spé][sujet-1][automatismes][question-?]
#     >>> components= generate_components(None, 0)
#     >>> answer = solve(**components)
#     >>> answer["maths_object"]
#     Decimal(x=138.89)
#     >>> answer["maths_object"].simplified()
#     Decimal(x=138.89)
#     """
#     answer = (k / factor).as_decimal.round(2)
#     return {
#         "maths_object": answer,
#     }


def render_question(*, prefix_joules_to_multiply_by_power, power, **kwargs):
    """[sujets0][spé][sujet-2][automatismes][question-6]
    Generate the question statement about energy conversion
    """

    statement = f"""Un appareil a besoin d'une énergie de ${prefix_joules_to_multiply_by_power.latex()} \\times 10^{{{power.latex()}}}$ Joules ($\\text{{J}}$) pour se mettre en route. À combien de kiloWatt-heure ($\\text{{kWh}}$) cela correspond-il?
    <br><span class="italic underline" style="font-weight: bold;">Données :</span> $1\\text{{kWh}} = 3,6 \\times 10^{{6}}\\text{{J}}$."""

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# Create HTML version with unit conversion
statement_html = f"<div>{question['statement']}</div>"


missive_dict = {
    "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-6]",
    "statement": question["statement"],
    "statement_html": statement_html,
    "answer": {
        "latex": f"{components['prefix_joules_to_multiply_by_power'].latex()} * 10^{{{components['power'].latex()}}} / ({components['factor'].simplified().as_decimal.latex()})",
        "simplified_latex": [
            # answer["maths_object"].simplified().latex(),
            answer["maths_object"].simplified().as_decimal.latex() + " kWh",
        ],
        "sympy_exp_data": answer["maths_object"].sympy_expr_data,
        "formal_repr": repr(answer["maths_object"]),
    },
    "components": {
        "prefix_joules_to_multiply_by_power": components[
            "prefix_joules_to_multiply_by_power"
        ].latex(),
        "power": components["power"].latex(),
        "energy_joules": components["energy_joules"].latex(),
        "factor": components["factor"].latex(),
    },
}


try:
    missive(missive_dict)
except NameError:
    from pprint import pprint

    pprint(missive_dict)


# print("Statement:", question["statement"])
# print("Answer:", answer["maths_object"])
# print("LaTeX representation:", answer["maths_object"].latex())
