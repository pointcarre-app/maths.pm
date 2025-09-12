import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][gén][sujet-2][automatismes][question-12]

    This exercise tests understanding of standard deviation (écart-type).

    MATHEMATICAL FOUNDATION:
    ========================
    We create two series with identical structure but different dispersions:
    - Series format: [center - d, center, center, center + d]
    - One uses d = disp_low (smaller spread: 0-9)
    - Other uses d = disp_high (larger spread: 10-50)

    KEY INSIGHT - Why this works:
    1) Both series have the same mean = center
       Mean = (center - d + center + center + center + d) / 4 = center

    2) For standard deviation σ with mean μ = center:
       σ² = Σ(xᵢ - μ)² / n
       σ² = [(center - d - center)² + (center - center)² + (center - center)² + (center + d - center)²] / 4
       σ² = [(-d)² + 0² + 0² + d²] / 4
       σ² = 2d² / 4 = d²/2

       Therefore: σ = d/√2

    3) Since σ is directly proportional to d:
       - Series with disp_high has σ = disp_high/√2 (LARGER)
       - Series with disp_low has σ = disp_low/√2 (smaller)

    EXAMPLE:
    If center = 10, disp_low = 3, disp_high = 12:
    - Low series: [7, 10, 10, 13] → σ = 3/√2 ≈ 2.12
    - High series: [-2, 10, 10, 22] → σ = 12/√2 ≈ 8.49

    >>> generate_components(None, 0)
    {'center': Integer(n=-1), 'disp_low': Integer(n=6), 'disp_high': Integer(n=12), 'a': (Integer(n=-13), Integer(n=-1), Integer(n=-1), Integer(n=11)), 'b': (Integer(n=-7), Integer(n=-1), Integer(n=-1), Integer(n=5))}
    """

    gen = tg.MathsGenerator(seed)

    # Choose a center value for both series (same mean)
    center = gen.random_integer(-50, 50)

    # Generate two different dispersion levels
    # disp_low is always smaller (0-9)
    # disp_high is always larger (10-50)
    # This ensures one series ALWAYS has larger standard deviation
    disp_low = gen.random_integer(0, 9)
    disp_high = gen.random_integer(10, 50)

    # Create the two series with the pattern [center - d, center, center, center + d]
    # This gives us two middle values at the center and two extreme values
    l_low = [center - disp_low, center, center, center + disp_low]
    l_high = [center - disp_high, center, center, center + disp_high]
    l_low = [e.simplified() for e in l_low]
    l_high = [e.simplified() for e in l_high]

    # Randomly assign which series is A and which is B
    # This prevents students from memorizing patterns
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

    SOLUTION LOGIC - Why comparing first elements works:
    =====================================================

    The first element of each series is either:
    - center - disp_low (for the low dispersion series)
    - center - disp_high (for the high dispersion series)

    Since disp_high > disp_low, we have:
    - center - disp_high < center - disp_low

    Therefore:
    - The series with the SMALLER first element has disp_high
    - The series with disp_high has the LARGER standard deviation

    MATHEMATICAL PROOF:
    If a[0] < b[0], then:
    - a[0] = center - disp_high
    - b[0] = center - disp_low
    - Series a has dispersion disp_high → σ_a = disp_high/√2
    - Series b has dispersion disp_low → σ_b = disp_low/√2
    - Since disp_high > disp_low → σ_a > σ_b
    - Therefore, A has the larger standard deviation

    CONCRETE EXAMPLE:
    If center = 20, disp_low = 5, disp_high = 15:
    - Series with low dispersion: [15, 20, 20, 25], first element = 15
    - Series with high dispersion: [5, 20, 20, 35], first element = 5
    - Since 5 < 15, the series starting with 5 has larger σ

    This elegant solution works because the first element directly
    encodes the dispersion magnitude through its distance from center!

    >>> components= generate_components(None, 0)
    >>> answer = solve(**components)
    >>> answer["maths_object"]
    Symbol(s='A')
    >>> answer["maths_object"].simplified()
    Symbol(s='A')
    """
    # Compare first elements to determine which has larger dispersion
    # Smaller first element = larger dispersion = larger standard deviation
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
    'On considère les deux séries : $A=\\{ -13 ; -1 ; -1 ; 11\\}$  et $B=\\{ -7 ; -1 ; -1 ; 5\\}$. Quelle série a le plus grand écart type ?'
    """

    a_latex = "&nbsp ; &nbsp ".join(e.latex() for e in a.elements)
    b_latex = "&nbsp ; &nbsp ".join(e.latex() for e in b.elements)

    statement = f"On considère les deux séries :<br>$A={a_latex}$  <br>$B={b_latex}$<br>Quelle est celle avec le plus grand écart type ?"
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
