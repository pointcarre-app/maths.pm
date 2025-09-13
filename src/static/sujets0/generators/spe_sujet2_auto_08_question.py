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

    statement_html = f"""<div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    <div style='flex: 1; min-width: 250px;'>La courbe ci-contre représente une droite dont le coefficient directeur vaut $1$, en valeur absolue (c'est à dire qu'il vaut $1$ ou $-1$). Donner l'équation de la droite sous la forme $a{x.latex()} + b{y.latex()} + c = 0$.</div>
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
            <foreignObject x="55" y="40" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p1">$$</span>
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
            <foreignObject x="170" y="16" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p2"></span>
                </div>
            </foreignObject>
            
            <foreignObject x="170" y="120" width="30" height="15" style="overflow: visible;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
                <span style="line-height: 1; text-align: center; font-size: 12px;" id="p3"></span>
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

    # graph_description = f"La droite d'équation y = {a.n}x + {c.n}"

    return {"statement": statement_html, "statement_html": statement_html}


components = generate_components(None)
answer = solve(**components)
question = render_question(**components)


print(components | answer | question)


# Create HTML version with graph description
statement_html = question["statement_html"]

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
