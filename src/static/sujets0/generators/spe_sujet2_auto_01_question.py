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
    "On considère l'arbre de probabilité ci-contre. Calculer la proabilité de B."
    """

    # NOTE mad: long string still need to be one line, otherwise doctest execution with backend executor are broken because of the try indentation it makes
    # statement = "On considère l'arbre de probabilité ci-contre. <br>Calculer la probabilité de l'évènement $B$."
    graph_description = "A proability tree with event A followed by continonal proabillity of B"

    statement_html = f"""<div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    <div style='flex: 1; min-width: 250px;'>On considère l'arbre de probabilité ci-contre. <br>Calculer la probabilité de l'évènement $B$.</div>
    <div style='flex: 0 1 auto;'>  
        <svg width="300" height="150" style="display: block; max-width: 100%; height: auto; border: 1px solid var(--color-base-300);">
            <!-- Define arrowhead marker -->
            <defs>
                <marker id="arrowhead" markerWidth="6" markerHeight="4" 
                refX="5" refY="2" orient="auto">
                <polygon points="0 0, 6 2, 0 4" fill="#333" />
                </marker>
            </defs>
            
            <!-- First level branches with arrows -->
            <line x1="30" y1="75" x2="110" y2="45" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            <line x1="30" y1="75" x2="110" y2="105" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            
            <!-- Second level branches from A with arrows -->
            <line x1="140" y1="45" x2="220" y2="25" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            <line x1="140" y1="45" x2="220" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            
            <!-- Second level branches from Ā with arrows -->
            <line x1="140" y1="105" x2="220" y2="95" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            <line x1="140" y1="105" x2="220" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
            
            <!-- First level probability labels -->
            <foreignObject x="55" y="38" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p1">${p_A.as_decimal.latex().replace(".", ",")}$</span>
                </div>
            </foreignObject>
            
            <!-- First level event labels -->
            <foreignObject x="115" y="35" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventA">$A$</span>
                </div>
            </foreignObject>
            
            <foreignObject x="115" y="100" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotA">$\\bar{{A}}$</span>
                </div>
            </foreignObject>
            
            <!-- Second level probability labels -->
            <foreignObject x="170" y="14" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p2">${p_B_if_A.as_decimal.latex().replace(".", ",")}$</span>
                </div>
            </foreignObject>
            
            <foreignObject x="170" y="122" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p3">${p_B_if_notA.as_decimal.latex().replace(".", ",")}$</span>
                </div>
            </foreignObject>
            
            <!-- Second level event labels -->
            <foreignObject x="225" y="20" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventB1">$B$</span>
                </div>
            </foreignObject>
            
            <foreignObject x="225" y="50" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotB1">$\\bar{{B}}$</span>
                </div>
            </foreignObject>
            
            <foreignObject x="225" y="90" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventB2">$B$</span>
                </div>
            </foreignObject>
            
            <foreignObject x="225" y="120" width="20" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotB2">$\\bar{{B}}$</span>
                </div>
            </foreignObject>
         </svg>
    </div>
</div>
"""

    return {
        "statement": statement_html,
        "statement_html": statement_html,
        "graph_description": graph_description,
    }


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


# print(components | answer | question)


# Create HTML version with probability tree description
statement_html = question["statement_html"]

missive(
    {
        "beacon": "[1ere][sujets0][spé][sujet-2][automatismes][question-1]",
        "statement": question["statement"],
        "statement_html": statement_html,
        "answer": {
            "latex": answer["maths_object"].latex(),
            "simplified_latex": [
                answer["maths_object"].simplified().latex(),
                answer["maths_object"].simplified().as_decimal.latex().replace(".", ","),
            ],
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
