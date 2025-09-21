---
js_dependencies:
  - "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"
---


# Sandbox - Interactive Python Execution

Test the interactive Python execution with matplotlib, pandas, and Bokeh.
{: .pm-subtitle}


[TOC]

## Python built-in libraries


### Basic example

```yaml
f_type: "codex_"
height_in_px: 350
inline: |
  # Testing built-in library import
  import math
  import datetime

  # Testing printing
  print("Hello from DataViz!")
  print("Current date and time:", datetime.datetime.now())

  # Testing basic logic
  primes_below_100 = [
    x 
    for x in range(2, 100) 
    if all(x % y != 0 for y in range(2, int(math.sqrt(x)) + 1))
  ]
  print("All the prime numbers below 100 are:")
  print(primes_below_100)
```


### 🔴 Inputs Not working

*Nagini timeout should stop execution after 30 seconds*

```yaml
f_type: "codex_"
height_in_px: 120
inline: |
  try:
    x = input()
    print(f"You entered: {x}")
  except Exception as e:
    print(f"Error: {e}")
```


## `matplotlib` (+ `pandas`) examples


### Simple `matplotlib` example

```yaml
f_type: "codex_"
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  import warnings
  import matplotlib
  
  # Suppress matplotlib font warnings for cleaner output
  warnings.filterwarnings('ignore', message='findfont: Generic family')
  matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # Use available fallback font
  
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


### `pandas`-only example

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

### `pandas` + `matplotlib` time series example

```yaml
f_type: "codex_"
inline: |
  import pandas as pd
  import matplotlib.pyplot as plt
  import numpy as np
  import warnings
  import matplotlib
  
  # Suppress matplotlib font warnings for cleaner output
  warnings.filterwarnings('ignore', message='findfont: Generic family')
  matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # Use available fallback font
  
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




## `bokeh` interactive plots


### 🟢 Working example (for `pm-codex`)


This code creates a fully interactive sine wave plot using Bokeh with hover tooltips, zoom/pan functionality, and clickable legends.


```yaml
f_type: "codex_"
height_in_px: 1150
inline: |
  # 🚀 ORIGINAL VERSION - Works with your Pyodide wrapper
  # 📦 Import Bokeh plotting + document
  from bokeh.plotting import figure, curdoc  
  # 🎯 Import hover functionality
  from bokeh.models import HoverTool     
  # 🔢 Import numerical operations     
  import numpy as np                          

  # 🔢 100 points from 0 to 4π (2 sine cycles)
  x = np.linspace(0, 4*np.pi, 100)           
  # 📈 Calculate sine values for each x
  y = np.sin(x)                              

  # 📝 Plot title: `title` argument
  # 📏 Plot width in pixels: `width` argument
  # 📏 Plot height in pixels: `height` argument
  # 🛠️ Interactive tools available: `tools` argument
  p = figure(
      title="Interactive Sine Wave - Try zooming and panning!",  
      width=600,                             
      height=400,                           
      tools="pan,wheel_zoom,box_zoom,reset"  
  )

  # 📊 Blue sine curve
  p.line(x, y, legend_label="sin(x)", line_width=2, color='navy')  
  # 🔴 Red dots every 5th point
  p.scatter(x[::5], y[::5], size=8, color='red', alpha=0.5)      

  # 💬 Add hover functionality: show coordinates on hover
  hover = HoverTool(tooltips=[("(x,y)", "($x, $y)")])  
  # ➕ Add hover tool to plot
  p.add_tools(hover)                         

  # 🎨 Customize plot appearance
  # 📊 X-axis label
  p.xaxis.axis_label = "x"                   
  # 📊 Y-axis label
  p.yaxis.axis_label = "sin(x)"             
  # 👁️ Click legend to hide/show lines
  p.legend.click_policy = "hide"             

  # 📺 Display plot in document (`pm-codex`): `curdoc().add_root(p)`
  curdoc().add_root(p)                       

  # 📢 Success messages
  print("✅ Interactive Bokeh plot created!")
  print("🎯 Use mouse to pan, scroll to zoom, hover for values!")
```


### 🔴 Working example (for `jupyter`)


**This code is designed to work in standard and local JupyterLab**. It creates a fully interactive sine wave plot using Bokeh with hover tooltips, zoom/pan functionality, and clickable legends.


```yaml
f_type: "codex_"
inline: |
  # 📚 JUPYTER VERSION - Works in standard JupyterLab
  # 📦 Import plotting + show function
  from bokeh.plotting import figure, show   
  # ❌ OLD: curdoc not needed for Jupyter
  # from bokeh.plotting import figure, curdoc 
  # ✨ NEW: Enable notebook output mode
  from bokeh.io import output_notebook    
  # 🎯 Import hover functionality
  from bokeh.models import HoverTool   

  # 🔢 Import numerical operations
  import numpy as np                          

  # 🔧 CRITICAL: Specific NOTEBOOK: Enable Jupyter notebook display mode
  # ✨ Specific NOTEBOOK: Tell Bokeh to render in notebook cells
  output_notebook()                           

  # 🔢 100 points from 0 to 4π (2 sine cycles)
  x = np.linspace(0, 4*np.pi, 100)           
  # 📈 Calculate sine values for each x
  y = np.sin(x)                              

  # 📝 Plot title
  # 📏 Plot width in pixels
  # 📏 Plot height in pixels
  # 🛠️ Interactive tools available
  p = figure(
      title="Interactive Sine Wave - Try zooming and panning!",  
      width=600,                             
      height=400,                            
      tools="pan,wheel_zoom,box_zoom,reset"  
  )

  # 📊 Blue sine curve
  p.line(x, y, legend_label="sin(x)", line_width=2, color='navy')  
  # 🔴 Red dots every 5th point
  p.scatter(x[::5], y[::5], size=8, color='red', alpha=0.5)       

  # 💬 Add hover functionality: show coordinates on hover
  hover = HoverTool(tooltips=[("(x,y)", "($x, $y)")])  
  # ➕ Add hover tool to plot
  p.add_tools(hover)                         

  # 🎨 Customize plot appearance
  # 📊 X-axis label
  p.xaxis.axis_label = "x"        
  # 📊 Y-axis label
  p.yaxis.axis_label = "sin(x)"       
  # 👁️ Click legend to hide/show lines
  p.legend.click_policy = "hide"             

  # 📺 Display plot (Jupyter method)
  # ✨ NEW: Specific NOTEBOOK: Display plot directly in cell output
  show(p)        
  # ❌ OLD: Not needed for Jupyter
  # curdoc().add_root(p)                     

  # 📢 Success messages
  print("✅ Interactive Bokeh plot created!")
  print("🎯 Use mouse to pan, scroll to zoom, hover for values!")
```

### 🟡 Deprecation warning (for `pm-codex`)

This example intentionally uses the deprecated `circle()` method to demonstrate the compact warning display.

```yaml
f_type: "codex_"
inline: |
  from bokeh.plotting import figure, curdoc
  from bokeh.models import HoverTool
  import numpy as np
  
  # Create simple data
  x = [1, 2, 3, 4, 5]
  y = [2, 5, 3, 8, 7]
  
  # Create plot
  p = figure(
      title="Deprecation Warning Demo",
      width=400, 
      height=300,
      tools="pan,wheel_zoom,reset"
  )
  
  # This will trigger the deprecation warning
  p.circle(x, y, size=15, color='red', alpha=0.6)
  
  # Add to document
  curdoc().add_root(p)
  
  print("⚠️  This example uses deprecated circle() method")
  print("📏 Check the compact warning display below!")
```












## `pm-codex` integration tests 

#### With `height_in_px`

```yaml 
f_type: "codex_"
height_in_px: 100
inline: |
    # CodeMirror will set the height to 250px for the Codex container
    # Your Python code here
    print("Hello World")
```

#### With `script_path`

```yaml
f_type: "codex_"
script_path: "intro/variables_intro.py"
```



## Legacy 

### Codex_ original work

```yaml
f_type: "codex_"
script_path: "intro/variables_intro.py"
```
