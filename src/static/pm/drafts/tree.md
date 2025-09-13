

# Tree example


lala


```svg
<svg width="400" height="200" style="border: 1px solid #333;">
  <line x1="50" y1="100" x2="150" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="100" x2="150" y2="140" stroke="#333" stroke-width="2"/>
  
  <line x1="150" y1="60" x2="300" y2="30" stroke="#333" stroke-width="2"/>
  <line x1="150" y1="60" x2="300" y2="70" stroke="#333" stroke-width="2"/>
  
  <!-- Second level branches from Ā -->
  <line x1="150" y1="140" x2="300" y2="130" stroke="#333" stroke-width="2"/>
  <line x1="150" y1="140" x2="300" y2="170" stroke="#333" stroke-width="2"/>
  
  <!-- First level labels -->
  <text x="100" y="75" fill="#333" font-size="14" id="p1"></text>
  <text x="160" y="55" fill="#333" font-size="16" font-weight="bold">A</text>
  
  <text x="160" y="145" fill="#333" font-size="16" font-weight="bold" id="notA"></text>
  
  <!-- Second level labels -->
  <text x="225" y="20" fill="#333" font-size="14" id="p2"></text>
  <text x="310" y="35" fill="#333" font-size="16" font-weight="bold">B</text>
  
  <text x="310" y="75" fill="#333" font-size="16" font-weight="bold" id="notB1"></text>
  
  <text x="310" y="135" fill="#333" font-size="16" font-weight="bold">B</text>
  
  <text x="225" y="185" fill="#333" font-size="14" id="p3"></text>
  <text x="310" y="175" fill="#333" font-size="16" font-weight="bold" id="notB2"></text>
</svg>
```

```html
<script>
katex.render("0.4", document.getElementById('p1'));
katex.render("\\overline{A}", document.getElementById('notA'));
katex.render("0.3", document.getElementById('p2'));
katex.render("\\overline{B}", document.getElementById('notB1'));
katex.render("0.9", document.getElementById('p3'));
katex.render("\\overline{B}", document.getElementById('notB2'));
</script>
```