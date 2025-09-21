---
js_dependencies:
  - "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"
---

# DataViz2 Sandbox - Interactive Python Execution

Test the interactive Python execution with matplotlib, pandas, and Bokeh support.

## Basic Python Example

```yaml
f_type: "codex_"
inline: |
  # Basic Python execution test
  print("Hello from DataViz2!")
  
  # Some calculations
  x = 10
  y = 20
  result = x + y
  print(f"The sum of {x} and {y} is {result}")
  
  # List operations
  numbers = [1, 2, 3, 4, 5]
  squared = [n**2 for n in numbers]
  print(f"Original: {numbers}")
  print(f"Squared: {squared}")
```

## Matplotlib Example

```yaml
f_type: "codex_"
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Create data
  x = np.linspace(0, 2 * np.pi, 100)
  y_sin = np.sin(x)
  y_cos = np.cos(x)
  
  # Create the plot
  plt.figure(figsize=(10, 6))
  plt.plot(x, y_sin, 'b-', label='sin(x)', linewidth=2)
  plt.plot(x, y_cos, 'r--', label='cos(x)', linewidth=2)
  plt.xlabel('x')
  plt.ylabel('y')
  plt.title('Sine and Cosine Functions')
  plt.legend()
  plt.grid(True, alpha=0.3)
  plt.show()
  
  print("Plot generated successfully!")
```

## Pandas Example

```yaml
f_type: "codex_"
inline: |
  import pandas as pd
  import numpy as np
  
  # Create a sample DataFrame
  data = {
      'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
      'Age': [25, 30, 35, 28, 32],
      'Score': [85, 92, 78, 91, 88],
      'Department': ['IT', 'HR', 'IT', 'Finance', 'HR']
  }
  
  df = pd.DataFrame(data)
  
  print("Original DataFrame:")
  print(df)
  print("\n" + "="*50 + "\n")
  
  # Basic statistics
  print("Statistics:")
  print(df.describe())
  print("\n" + "="*50 + "\n")
  
  # Group by department
  print("Average score by department:")
  dept_avg = df.groupby('Department')['Score'].mean()
  print(dept_avg)
```

## Data Visualization with Pandas

```yaml
f_type: "codex_"
inline: |
  import pandas as pd
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Create sample time series data
  dates = pd.date_range('20240101', periods=100)
  df = pd.DataFrame({
      'date': dates,
      'value': np.random.randn(100).cumsum() + 100,
      'volume': np.random.randint(50, 150, 100)
  })
  
  # Create subplots
  fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
  
  # Plot time series
  ax1.plot(df['date'], df['value'], 'b-', linewidth=2)
  ax1.set_title('Time Series Data')
  ax1.set_xlabel('Date')
  ax1.set_ylabel('Value')
  ax1.grid(True, alpha=0.3)
  
  # Plot volume bars
  ax2.bar(df['date'], df['volume'], color='green', alpha=0.6)
  ax2.set_title('Daily Volume')
  ax2.set_xlabel('Date')
  ax2.set_ylabel('Volume')
  ax2.grid(True, alpha=0.3)
  
  plt.tight_layout()
  plt.show()
  
  print(f"Data shape: {df.shape}")
  print(f"Date range: {df['date'].min()} to {df['date'].max()}")
  print(f"Value range: {df['value'].min():.2f} to {df['value'].max():.2f}")
```

## Original Codex (from file)

```yaml
f_type: "codex_"
script_path: "intro/variables_intro.py"
```

## Bokeh Interactive Plot Example

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.models import HoverTool
  import numpy as np
  
  # Create data
  x = np.linspace(0, 4*np.pi, 100)
  y = np.sin(x)
  
  # Create interactive plot
  p = figure(
      title="Interactive Sine Wave - Try zooming and panning!",
      width=600, 
      height=400,
      tools="pan,wheel_zoom,box_zoom,reset"
  )
  
  # Add line and points
  p.line(x, y, legend_label="sin(x)", line_width=2, color='navy')
  p.circle(x[::5], y[::5], size=8, color='red', alpha=0.5)
  
  # Add hover tool
  hover = HoverTool(tooltips=[("(x,y)", "($x, $y)")])
  p.add_tools(hover)
  
  # Customize
  p.xaxis.axis_label = "x"
  p.yaxis.axis_label = "sin(x)"
  p.legend.click_policy = "hide"
  
  # Add to document for capture
  curdoc().add_root(p)
  
  print("✅ Interactive Bokeh plot created!")
  print("🎯 Use mouse to pan, scroll to zoom, hover for values!")
```