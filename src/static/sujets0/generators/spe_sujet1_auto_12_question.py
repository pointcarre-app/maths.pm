import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-1][automatismes][question-12]
    >>> generate_components(None, 0)
    {'note1': Integer(n=12), 'note2': Integer(n=13), 'note3': Integer(n=1), 'coef1': Integer(n=3), 'coef2': Integer(n=5), 'coef3': Integer(n=4), 'mean': Fraction(p=Add(l=Add(l=Mul(l=Integer(n=12), r=Integer(n=3)), r=Mul(l=Integer(n=13), r=Integer(n=5))), r=Mul(l=Integer(n=1), r=Integer(n=4))), q=Add(l=Add(l=Integer(n=3), r=Integer(n=5)), r=Integer(n=4)))}
    """

    gen = tg.MathsGenerator(seed)

    note1 = gen.random_integer(0, 20)
    note2 = gen.random_integer(0, 20)
    note3 = gen.random_integer(0, 20)

    coef1 = gen.random_integer(1, 5)
    coef2 = gen.random_integer(1, 5)
    coef3 = gen.random_integer(1, 5)

    mean = note1 * coef1 + note2 * coef2 + note3 * coef3
    mean = mean / (coef1 + coef2 + coef3)

    return {
        "note1": note1,
        "note2": note2,
        "note3": note3,
        "coef1": coef1,
        "coef2": coef2,
        "coef3": coef3,
        "mean": mean,
    }


def solve(*, note1, note2, note3, coef1, coef2, coef3, mean):
    """[sujets0][spé][sujet-1][automatismes][question-12]
    >>> note1, note2, note3 = tm.Integer(n=12), tm.Integer(n=13), tm.Integer(n=1)
    >>> coef1, coef2, coef3 = tm.Integer(n=3), tm.Integer(n=5), tm.Integer(n=4)
    >>> mean = tm.Fraction(p=tm.Add(l=tm.Add(l=tm.Mul(l=tm.Integer(n=12), r=tm.Integer(n=3)), r=tm.Mul(l=tm.Integer(n=13), r=tm.Integer(n=5))), r=tm.Mul(l=tm.Integer(n=1), r=tm.Integer(n=4))), q=tm.Add(l=tm.Add(l=tm.Integer(n=3), r=tm.Integer(n=5)), r=tm.Integer(n=4)))
    >>> answer = solve(note1=note1, note2=note2, note3=note3, coef1=coef1, coef2=coef2, coef3=coef3, mean=mean)
    >>> answer["maths_object"]
    Integer(n=4)
    """
    maths_object = coef3
    return {"maths_object": maths_object}


def render_question(*, note1, note2, note3, coef1, coef2, coef3, mean):
    r"""[sujets0][spé][sujet-1][automatismes][question-12]
    >>> note1, note2, note3 = tm.Integer(n=12), tm.Integer(n=13), tm.Integer(n=1)
    >>> coef1, coef2, coef3 = tm.Integer(n=3), tm.Integer(n=5), tm.Integer(n=4)
    >>> mean = tm.Fraction(p=tm.Integer(n=105), q=tm.Integer(n=12))
    >>> statement = render_question(note1=note1, note2=note2, note3=note3, coef1=coef1, coef2=coef2, coef3=coef3, mean=mean)
    >>> statement["statement"]
    'Voici une série de notes avec les coefficients associés\n-12 coefficient 3\n-13 coefficient 5\n-1 coefficient $x$\nOn note $m$ la moyenne de cette série. Que doit valoir $x$ pour que $m = 8.75$ ?'
    """

    statement = f"""Voici une série de notes avec les coefficients associés\n-{note1.n} coefficient {coef1.n}\n-{note2.n} coefficient {coef2.n}\n-{note3.n} coefficient $x$\nOn note $m$ la moyenne de cette série. Que doit valoir $x$ pour que $m = """
    statement += str(mean.eval())
    statement += "$ ?"

    return {
        "statement": statement,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with table for notes
statement_html = f"""
<div class="card bg-base-100 shadow-sm">
    <div class="card-body">
        <p class="text-sm mb-3">Voici une série de notes avec les coefficients associés :</p>
        <div class="overflow-x-auto">
            <table class="table table-compact w-full">
                <thead>
                    <tr>
                        <th class="text-center">Note</th>
                        <th class="text-center">Coefficient</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-center">{components["note1"].n}</td>
                        <td class="text-center">{components["coef1"].n}</td>
                    </tr>
                    <tr>
                        <td class="text-center">{components["note2"].n}</td>
                        <td class="text-center">{components["coef2"].n}</td>
                    </tr>
                    <tr>
                        <td class="text-center">{components["note3"].n}</td>
                        <td class="text-center"><span class="badge badge-primary">$x$</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="alert alert-info mt-3">
            <span>On note $m$ la moyenne de cette série. On veut que <span class="badge badge-warning">$m = {components["mean"].eval()}$</span></span>
        </div>
        <div class="divider"></div>
        <div class="text-sm font-semibold">
            Que doit valoir $x$ ?
        </div>
    </div>
</div>
"""

# Define latex_0 for multiple possible answers
latex_0 = answer["maths_object"].latex()

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-1][automatismes][question-12]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": [latex_0],  # List to support multiple correct answers
            "simplified_latex": answer["maths_object"].simplified().latex(),
            "sympy_exp_data": answer["maths_object"].sympy_expr_data,
            "formal_repr": repr(answer["maths_object"]),
        },
        "components": {
            "note1": components["note1"].latex(),
            "note2": components["note2"].latex(),
            "note3": components["note3"].latex(),
            "coef1": components["coef1"].latex(),
            "coef2": components["coef2"].latex(),
            "coef3": components["coef3"].latex(),
            "mean": components["mean"].latex(),
        },
    }
)
