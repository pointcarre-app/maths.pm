---
js_dependencies:
  - "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.6.2.min.js"
---


[TOC]
# DataViz2 Sandbox - Bokeh Interactive Visualizations

Test interactive Bokeh plots with Python execution in the browser.

## Simple Bokeh Line Plot

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.models import HoverTool
  import numpy as np
  
  # Create data
  x = np.linspace(0, 4*np.pi, 100)
  y = np.sin(x)
  
  # Create a new plot with tools
  p = figure(
      title="Interactive Sine Wave",
      width=600, 
      height=400,
      tools="pan,wheel_zoom,box_zoom,reset,save"
  )
  
  # Add a line renderer with legend and line thickness
  line = p.line(x, y, legend_label="sin(x)", line_width=2, color='navy', alpha=0.8)
  
  # Add circle markers
  p.circle(x[::5], y[::5], size=8, color='red', alpha=0.5, legend_label="Points")
  
  # Add hover tool
  hover = HoverTool(tooltips=[("(x,y)", "($x, $y)")])
  p.add_tools(hover)
  
  # Customize the plot
  p.xaxis.axis_label = "x"
  p.yaxis.axis_label = "y"
  p.legend.location = "top_right"
  p.legend.click_policy = "hide"
  
  # Add the plot to the document
  curdoc().add_root(p)
  
  print("✅ Bokeh plot created successfully!")
  print("🎯 Try: Pan, Zoom, Hover over points, Click legend items")
```

## Interactive Scatter Plot with Color Mapping

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.models import HoverTool
  from bokeh.transform import linear_cmap
  from bokeh.palettes import Viridis256
  import numpy as np
  
  # Generate random data
  n = 200
  x = np.random.random(n) * 100
  y = np.random.random(n) * 100
  colors = np.random.random(n) * 100
  sizes = np.random.randint(10, 25, n)
  
  # Create figure
  p = figure(
      title="Interactive Scatter Plot",
      width=600,
      height=400,
      tools="pan,wheel_zoom,box_select,lasso_select,reset"
  )
  
  # Create color mapper
  mapper = linear_cmap(field_name='colors', palette=Viridis256, 
                       low=min(colors), high=max(colors))
  
  # Add scatter with color mapping
  scatter = p.scatter(
      x, y, 
      size=sizes, 
      color=mapper,
      alpha=0.6,
      line_color="navy",
      line_alpha=0.3
  )
  
  # Add hover tool
  hover = HoverTool(tooltips=[
      ("Index", "$index"),
      ("(X,Y)", "($x, $y)"),
      ("Size", "@sizes")
  ])
  p.add_tools(hover)
  
  # Style the plot
  p.xaxis.axis_label = "X Coordinate"
  p.yaxis.axis_label = "Y Coordinate"
  
  # Add to document
  curdoc().add_root(p)
  
  print(f"✅ Created scatter plot with {n} points")
  print("🎯 Try: Select points with box or lasso select tools!")
```

## Multiple Subplots with Linked Axes

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.layouts import column
  from bokeh.models import Range1d
  import numpy as np
  
  # Generate data
  x = np.linspace(0, 4*np.pi, 100)
  
  # Create figures with shared x-range
  shared_x_range = Range1d(0, 4*np.pi)
  
  # Top plot - Sine and Cosine
  p1 = figure(width=600, height=200, title="Trigonometric Functions", 
              x_range=shared_x_range)
  p1.line(x, np.sin(x), legend_label="sin(x)", line_width=2, color="navy")
  p1.line(x, np.cos(x), legend_label="cos(x)", line_width=2, color="red")
  p1.legend.click_policy = "hide"
  
  # Bottom plot - Exponential decay
  p2 = figure(width=600, height=200, title="Exponential Decay", 
              x_range=shared_x_range)
  p2.line(x, np.exp(-x/5) * np.sin(x), 
          legend_label="e^(-x/5) * sin(x)", 
          line_width=2, color="green")
  p2.circle(x[::5], np.exp(-x[::5]/5) * np.sin(x[::5]), 
            size=6, color="orange")
  
  # Arrange plots
  layout = column(p1, p2)
  
  # Add to document
  curdoc().add_root(layout)
  
  print("✅ Created multiple linked plots!")
  print("🎯 Pan or zoom in one plot - others follow!")
```

## Heatmap Visualization

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.models import ColorBar, LinearColorMapper
  from bokeh.palettes import RdYlBu11
  import numpy as np
  
  # Generate data
  N = 20
  x = np.linspace(0, 10, N)
  y = np.linspace(0, 10, N)
  xx, yy = np.meshgrid(x, y)
  z = np.sin(xx) * np.cos(yy)
  
  # Flatten for plotting
  x_flat = xx.flatten()
  y_flat = yy.flatten()
  z_flat = z.flatten()
  
  # Create color mapper
  color_mapper = LinearColorMapper(palette=RdYlBu11, 
                                    low=z_flat.min(), 
                                    high=z_flat.max())
  
  # Create figure
  p = figure(
      title="Heatmap: sin(x) * cos(y)",
      width=600,
      height=500,
      x_range=(-0.5, 10.5),
      y_range=(-0.5, 10.5),
      tools="pan,wheel_zoom,reset,hover"
  )
  
  # Create heatmap using rect glyphs
  p.rect(
      x=x_flat,
      y=y_flat,
      width=10/N,
      height=10/N,
      fill_color={'field': z_flat, 'transform': color_mapper},
      line_color=None
  )
  
  # Add color bar
  color_bar = ColorBar(color_mapper=color_mapper, width=8, location=(0,0))
  p.add_layout(color_bar, 'right')
  
  # Configure hover tool
  p.hover.tooltips = [
      ("(x,y)", "(@x{0.00}, @y{0.00})"),
      ("value", "@z{0.000}")
  ]
  
  # Add to document
  curdoc().add_root(p)
  
  print(f"✅ Created {N}x{N} heatmap!")
  print("📊 Hover to see values!")
```

## Combined Matplotlib and Bokeh

```yaml
f_type: "codex_"
inline: |
  import numpy as np
  import matplotlib.pyplot as plt
  from bokeh.plotting import figure, curdoc
  
  # Generate data
  x = np.linspace(0, 2*np.pi, 100)
  y = np.sin(x)
  
  # Create Matplotlib figure (static)
  plt.figure(figsize=(8, 3))
  plt.plot(x, y, 'b-', linewidth=2, label='Static plot')
  plt.title('Matplotlib: Static Sine Wave')
  plt.xlabel('x')
  plt.ylabel('sin(x)')
  plt.grid(True, alpha=0.3)
  plt.legend()
  plt.show()
  
  # Create Bokeh figure (interactive)
  p = figure(
      title="Bokeh: Interactive Sine Wave",
      width=600, 
      height=300,
      tools="pan,wheel_zoom,reset"
  )
  
  p.line(x, y, line_width=2, color='red', 
         legend_label="Interactive plot")
  p.legend.location = "top_right"
  
  # Add to document
  curdoc().add_root(p)
  
  print("✅ Created both static (Matplotlib) and interactive (Bokeh) plots!")
  print("📊 Matplotlib: Static image")
  print("🎯 Bokeh: Try panning and zooming!")
```

## Notes

- **Bokeh plots** are interactive - you can pan, zoom, select points, and hover for tooltips
- **BokehJS libraries** are loaded automatically via the metadata at the top of this file
- **Matplotlib plots** are still supported and will display as static images
- All plots are captured and rendered automatically after execution
- Use `curdoc().add_root(plot)` to make Bokeh plots available for capture
