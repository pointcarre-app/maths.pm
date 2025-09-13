

# All



## Tree 




<code>spe_sujet2_auto_01_question.py</code>
{: .my-4}



```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.8/katex.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.8/katex.min.css">

<svg width="300" height="150" style="display: block; max-width: 100%; height: auto; border: 1px solid #333;">
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
      <span style="line-height: 1; text-align: center; font-size: 12px;" id="p1"></span>
    </div>
  </foreignObject>
  
  <!-- First level event labels -->
  <foreignObject x="115" y="35" width="20" height="15" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventA"></span>
    </div>
  </foreignObject>
  
  <foreignObject x="115" y="100" width="20" height="15" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotA"></span>
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
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventB1"></span>
    </div>
  </foreignObject>
  
  <foreignObject x="225" y="50" width="20" height="15" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotB1"></span>
    </div>
  </foreignObject>
  
  <foreignObject x="225" y="90" width="20" height="15" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventB2"></span>
    </div>
  </foreignObject>
  
  <foreignObject x="225" y="120" width="20" height="15" style="overflow: visible;">
    <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
      <span style="line-height: 1; text-align: center; font-size: 14px;" id="eventNotB2"></span>
    </div>
  </foreignObject>
</svg>

<script>
katex.render("0,4", document.getElementById('p1'));
katex.render("0,3", document.getElementById('p2'));
katex.render("0,9", document.getElementById('p3'));
katex.render("A", document.getElementById('eventA'));
katex.render("\\bar{A}", document.getElementById('eventNotA'));
katex.render("B", document.getElementById('eventB1'));
katex.render("\\bar{B}", document.getElementById('eventNotB1'));
katex.render("B", document.getElementById('eventB2'));
katex.render("\\bar{B}", document.getElementById('eventNotB2'));
</script>
```