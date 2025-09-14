import random
import teachers.generator as tg
import teachers.maths as tm
from teachers.defaults import SEED


def generate_components(difficulty, seed=SEED) -> dict[str, tm.MathsObject]:
    """[sujets0][spé][sujet-2][automatismes][question-9]
    >>> generate_components(None, 0)
    {'a': Integer(n=1), 'c': Integer(n=1), 'x': Symbol(s='x'), 'y': Symbol(s='y')}
    """

    gen = tg.MathsGenerator(seed)

    case = random.choice(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    )

    if case == 0:
        a = tm.Integer(n=1)
        c = tm.Integer(n=1)
    elif case == 1:
        a = tm.Integer(n=1)
        c = tm.Integer(n=2)
    elif case == 2:
        a = tm.Integer(n=2)
        c = tm.Integer(n=1)
    elif case == 3:
        a = tm.Integer(n=2)
        c = tm.Integer(n=2)
    elif case == 4:
        a = tm.Fraction(p=1, q=2)
        c = tm.Integer(n=1)
    elif case == 5:
        a = tm.Fraction(p=1, q=2)
        c = tm.Integer(n=2)
    elif case == 6:
        a = tm.Fraction(p=2, q=1)
        c = tm.Integer(n=1)
    elif case == 7:
        a = tm.Fraction(p=2, q=1)
        c = tm.Integer(n=2)
    elif case == 8:
        a = tm.Fraction(p=1, q=3)
        c = tm.Integer(n=1)
    elif case == 9:
        a = tm.Fraction(p=1, q=3)
        c = tm.Integer(n=2)
    elif case == 10:
        a = tm.Fraction(p=2, q=3)
        c = tm.Integer(n=1)
    elif case == 11:
        a = tm.Fraction(p=2, q=3)
        c = tm.Integer(n=2)
    elif case == 12:
        a = tm.Fraction(p=1, q=4)
        c = tm.Integer(n=1)
    elif case == 13:
        a = tm.Fraction(p=1, q=4)
        c = tm.Integer(n=2)
    elif case == 14:
        a = tm.Fraction(p=2, q=4)
        c = tm.Integer(n=1)
    elif case == 15:
        a = tm.Fraction(p=2, q=4)
        c = tm.Integer(n=2)
    elif case == 16:
        a = tm.Fraction(p=3, q=4)
        c = tm.Integer(n=1)
    elif case == 17:
        a = tm.Fraction(p=3, q=4)
        c = tm.Integer(n=2)
    elif case == 18:
        a = tm.Fraction(p=4, q=4)
        c = tm.Integer(n=1)
    elif case == 19:
        a = tm.Fraction(p=4, q=4)
        c = tm.Integer(n=2)
    elif case == 20:
        a = tm.Fraction(p=5, q=4)
        c = tm.Integer(n=1)
    elif case == 21:
        a = tm.Fraction(p=5, q=4)
        c = tm.Integer(n=2)
    else:
        raise ValueError(f"Invalid case: {case}")

    # # a = gen.random_integer(1, 10)
    # dir1 = gen.random_element_from([-1, 1])
    # dir2 = gen.random_element_from([-1, 1])
    # a = tm.Integer(n=dir1)
    # c = gen.random_integer(1, 10)
    # c = tm.Integer(n=dir2) * c
    # c = c.simplified()
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

    # Extract numeric values for line calculation
    slope = float(a.sympy_expr)  # Will be -1 or 1
    y_intercept = float(c.sympy_expr)  # Random integer with random sign

    # Calculate SVG coordinates for line y = slope*x + y_intercept
    # Very compact coordinate system: origin at (100, 100), scale 18px per unit, minimal margins
    origin_x, origin_y, scale = 100, 100, 18
    margin = 15  # Minimal margin around the chart
    x1, x2 = -4, 4
    y1 = slope * x1 + y_intercept
    y2 = slope * x2 + y_intercept

    # Convert to SVG coordinates
    svg_x1 = origin_x + x1 * scale
    svg_y1 = origin_y - y1 * scale  # Y is flipped in SVG
    svg_x2 = origin_x + x2 * scale
    svg_y2 = origin_y - y2 * scale

    # SVG chart definition with very compact layout and consistent grid
    chart_size = 200  # Much smaller overall size
    svg_chart = f"""<svg id="spe_sujet2_auto_08_question_svg" width="{chart_size}" height="{chart_size}" style="display: block; max-width: 100%; height: auto; border: 1px solid #333;">
  <!-- Define arrowhead marker -->
  <defs>
    <marker id="axisArrowMarker_spe_sujet2_auto_08_question_chart" markerWidth="6" markerHeight="4" 
     refX="5" refY="2" orient="auto">
      <polygon points="0 0, 6 2, 0 4" fill="#333" />
    </marker>
  </defs>
  
  <!-- Grid lines (consistent coverage) -->
  <!-- Vertical grid lines -->
  <line x1="{origin_x + (-4) * scale}" y1="{margin}" x2="{origin_x + (-4) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (-3) * scale}" y1="{margin}" x2="{origin_x + (-3) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (-2) * scale}" y1="{margin}" x2="{origin_x + (-2) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (-1) * scale}" y1="{margin}" x2="{origin_x + (-1) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (1) * scale}" y1="{margin}" x2="{origin_x + (1) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (2) * scale}" y1="{margin}" x2="{origin_x + (2) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (3) * scale}" y1="{margin}" x2="{origin_x + (3) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{origin_x + (4) * scale}" y1="{margin}" x2="{origin_x + (4) * scale}" y2="{chart_size - margin}" class="stroke-base-300" stroke-width="0.5"/>
  
  <!-- Horizontal grid lines -->
  <line x1="{margin}" y1="{origin_y - (4) * scale}" x2="{chart_size - margin}" y2="{origin_y - (4) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y - (3) * scale}" x2="{chart_size - margin}" y2="{origin_y - (3) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y - (2) * scale}" x2="{chart_size - margin}" y2="{origin_y - (2) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y - (1) * scale}" x2="{chart_size - margin}" y2="{origin_y - (1) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y + (1) * scale}" x2="{chart_size - margin}" y2="{origin_y + (1) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y + (2) * scale}" x2="{chart_size - margin}" y2="{origin_y + (2) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y + (3) * scale}" x2="{chart_size - margin}" y2="{origin_y + (3) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  <line x1="{margin}" y1="{origin_y + (4) * scale}" x2="{chart_size - margin}" y2="{origin_y + (4) * scale}" class="stroke-base-300" stroke-width="0.5"/>
  
  <!-- Axes -->
  <line x1="{margin}" y1="{origin_y}" x2="{chart_size - margin}" y2="{origin_y}" stroke="#333" stroke-width="1" marker-end="url(#axisArrowMarker_spe_sujet2_auto_08_question_chart)"/>
  <line x1="{origin_x}" y1="{chart_size - margin}" x2="{origin_x}" y2="{margin}" stroke="#333" stroke-width="1" marker-end="url(#axisArrowMarker_spe_sujet2_auto_08_question_chart)"/>
  
  <!-- X-axis ticks -->
  <line x1="{origin_x + (1) * scale}" y1="{origin_y - 3}" x2="{origin_x + (1) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (2) * scale}" y1="{origin_y - 3}" x2="{origin_x + (2) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (3) * scale}" y1="{origin_y - 3}" x2="{origin_x + (3) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (4) * scale}" y1="{origin_y - 3}" x2="{origin_x + (4) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (-1) * scale}" y1="{origin_y - 3}" x2="{origin_x + (-1) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (-2) * scale}" y1="{origin_y - 3}" x2="{origin_x + (-2) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (-3) * scale}" y1="{origin_y - 3}" x2="{origin_x + (-3) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x + (-4) * scale}" y1="{origin_y - 3}" x2="{origin_x + (-4) * scale}" y2="{origin_y + 3}" class="stroke-base-300" stroke-width="1"/>
  
  <!-- Y-axis ticks -->
  <line x1="{origin_x - 3}" y1="{origin_y - (1) * scale}" x2="{origin_x + 3}" y2="{origin_y - (1) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y - (2) * scale}" x2="{origin_x + 3}" y2="{origin_y - (2) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y - (3) * scale}" x2="{origin_x + 3}" y2="{origin_y - (3) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y - (4) * scale}" x2="{origin_x + 3}" y2="{origin_y - (4) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y + (1) * scale}" x2="{origin_x + 3}" y2="{origin_y + (1) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y + (2) * scale}" x2="{origin_x + 3}" y2="{origin_y + (2) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y + (3) * scale}" x2="{origin_x + 3}" y2="{origin_y + (3) * scale}" class="stroke-base-300" stroke-width="1"/>
  <line x1="{origin_x - 3}" y1="{origin_y + (4) * scale}" x2="{origin_x + 3}" y2="{origin_y + (4) * scale}" class="stroke-base-300" stroke-width="1"/>
  
  <!-- X-axis tick labels -->
  <foreignObject x="{origin_x + (1) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$1$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (2) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$2$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (3) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$3$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (4) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$4$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (-1) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$-1$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (-2) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$-2$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (-3) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$-3$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x + (-4) * scale - 7}" y="{origin_y + 5}" width="14" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 8px;">$-4$</span>
    </div>
  </foreignObject>
  
  <!-- Y-axis tick labels -->
  <foreignObject x="{origin_x - 12}" y="{origin_y - (1) * scale - 4}" width="10" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$1$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 12}" y="{origin_y - (2) * scale - 4}" width="10" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$2$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 12}" y="{origin_y - (3) * scale - 4}" width="10" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$3$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 12}" y="{origin_y - (4) * scale - 4}" width="10" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$4$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 15}" y="{origin_y + (1) * scale - 4}" width="13" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$-1$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 15}" y="{origin_y + (2) * scale - 4}" width="13" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$-2$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 15}" y="{origin_y + (3) * scale - 4}" width="13" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$-3$</span>
    </div>
  </foreignObject>
  <foreignObject x="{origin_x - 15}" y="{origin_y + (4) * scale - 4}" width="13" height="8" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: flex-end;">
      <span style="line-height: 1; text-align: right; font-size: 7px;">$-4$</span>
    </div>
  </foreignObject>
  
  <!-- Axis labels -->
  <foreignObject x="{origin_x + (4) * scale + 10}" y="{origin_y + 4}" width="12" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 10px;">$x$</span>
    </div>
  </foreignObject>
  
  <foreignObject x="{origin_x}" y="{origin_y - (5) * scale - 2}" width="12" height="10" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 10px;">$y$</span>
    </div>
  </foreignObject>
  
  <!-- Line with dynamic coordinates -->
  <line id="mainLine_spe_sujet2_auto_08_question_chart" stroke="#e74c3c" stroke-width="1.5" x1="{svg_x1}" y1="{svg_y1}" x2="{svg_x2}" y2="{svg_y2}"/>
</svg>"""

    # JavaScript line drawing function
    js_line_function = """
// Function to draw line y = ax + b with robust DOM handling
function drawLineSpeSubject2Auto08Question(a, b) {
  const line = document.getElementById('mainLine_spe_sujet2_auto_08_question_chart');
  
  if (!line) {
    console.warn('Line element not found, retrying...');
    return false;
  }
  
  // Define coordinate system: origin at (100, 100), scale 18px per unit
  const originX = 100;
  const originY = 100;
  const scale = 18;
  
  // Calculate line endpoints for x from -4 to 4
  const x1 = -4;
  const x2 = 4;
  const y1 = a * x1 + b;
  const y2 = a * x2 + b;
  
  // Convert to SVG coordinates
  const svgX1 = originX + x1 * scale;
  const svgY1 = originY - y1 * scale; // Y is flipped in SVG
  const svgX2 = originX + x2 * scale;
  const svgY2 = originY - y2 * scale;
  
  line.setAttribute('x1', svgX1);
  line.setAttribute('y1', svgY1);
  line.setAttribute('x2', svgX2);
  line.setAttribute('y2', svgY2);
  
  return true;
}"""

    # Simple MutationObserver with actual values
    js_execution_strategy = f"""
// Simple MutationObserver to watch for SVG
const observer = new MutationObserver(function() {{
  const svg = document.getElementById('spe_sujet2_auto_08_question_svg');
  if (svg) {{
    console.log('✅ SVG found, drawing line y = {slope}x + {y_intercept}');
    observer.disconnect();
    drawLineSpeSubject2Auto08Question({slope}, {y_intercept});
  }}
}});

observer.observe(document, {{ childList: true, subtree: true }});

// Stop after 5 seconds
setTimeout(() => observer.disconnect(), 5000);"""

    # Complete script combining all parts
    complete_script = f"""<script>
{js_line_function}

{js_execution_strategy}
</script>"""

    # Build the complete SVG with script
    svg_with_script = f"{svg_chart}\n{complete_script}"

    # Create the statement HTML with better structure
    statement_html = f"""<div style='display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-start;'>
    <div style='flex: 1; min-width: 250px;'>
        Donner l'équation de la droite sous la forme $a{x.latex()} + b{y.latex()} + c = 0$.
    </div>
    <div style='flex: 0 1 auto;'>  
        {svg_with_script}
    </div>
</div>"""

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
