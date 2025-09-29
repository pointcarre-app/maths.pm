# Advanced Matplotlib: Complete API Reference & Best Practices

A comprehensive guide to matplotlib's advanced features, focusing on precise control, professional styling, and production-ready visualizations.
{: .pm-subtitle}

[TOC]

## 1. Configuration & Environment Setup

### 1.1. Global Configuration with rcParams

```yaml
f_type: "codex_"
height_in_px: 400
inline: |
  import matplotlib.pyplot as plt
  import matplotlib as mpl
  import numpy as np
  import warnings
  
  # Suppress font warnings
  warnings.filterwarnings('ignore', message='findfont')
  
  # Complete rcParams configuration
  mpl.rcParams.update({
      # Figure properties
      'figure.figsize': (10, 6),
      'figure.dpi': 100,
      'figure.facecolor': 'white',
      'figure.edgecolor': 'none',
      'figure.autolayout': False,
      'figure.max_open_warning': 20,
      
      # Axes properties
      'axes.facecolor': 'white',
      'axes.edgecolor': '#333333',
      'axes.linewidth': 1.0,
      'axes.grid': True,
      'axes.titlesize': 14,
      'axes.titleweight': 'bold',
      'axes.labelsize': 12,
      'axes.labelweight': 'normal',
      'axes.labelcolor': '#333333',
      'axes.axisbelow': True,
      'axes.prop_cycle': plt.cycler('color', 
          ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
           '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']),
      
      # Grid properties
      'grid.color': '#b0b0b0',
      'grid.linestyle': '--',
      'grid.linewidth': 0.5,
      'grid.alpha': 0.5,
      
      # Font properties
      'font.family': 'sans-serif',
      'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
      'font.size': 10,
      
      # Tick properties
      'xtick.labelsize': 10,
      'ytick.labelsize': 10,
      'xtick.color': '#333333',
      'ytick.color': '#333333',
      'xtick.direction': 'out',
      'ytick.direction': 'out',
      
      # Legend properties
      'legend.frameon': True,
      'legend.framealpha': 0.9,
      'legend.facecolor': 'white',
      'legend.edgecolor': '#CCCCCC',
      'legend.fontsize': 10,
      
      # Save figure properties
      'savefig.dpi': 300,
      'savefig.bbox': 'tight',
      'savefig.pad_inches': 0.1,
      'savefig.facecolor': 'white',
      'savefig.edgecolor': 'none'
  })
  
  # Demonstration plot
  x = np.linspace(0, 10, 100)
  fig, ax = plt.subplots()
  for i in range(5):
      ax.plot(x, np.sin(x + i*0.5), label=f'Wave {i+1}')
  
  ax.set_title('Default Configuration Applied')
  ax.set_xlabel('X axis')
  ax.set_ylabel('Y axis')
  ax.legend(loc='upper right')
  plt.show()
  
  print("✅ Global configuration applied successfully")
```

### 1.2. Context Managers for Temporary Settings

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  x = np.linspace(0, 10, 100)
  y = np.sin(x)
  
  # Create subplots to show the difference
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
  
  # Normal plot
  ax1.plot(x, y)
  ax1.set_title('Default Style')
  ax1.grid(True)
  
  # Using context manager for temporary style
  with plt.rc_context({'lines.linewidth': 3, 
                        'lines.linestyle': '--',
                        'axes.facecolor': '#f0f0f0',
                        'grid.alpha': 0.8}):
      ax2.plot(x, y, color='red')
      ax2.set_title('Temporary Style with Context Manager')
      ax2.grid(True)
  
  plt.tight_layout()
  plt.show()
  
  # Style contexts can also be used with 'with' statements
  with plt.style.context('seaborn-v0_8-darkgrid'):
      fig, ax = plt.subplots(figsize=(8, 4))
      ax.plot(x, np.cos(x), 'g-', linewidth=2)
      ax.set_title('Using Seaborn Dark Grid Style Context')
      plt.show()
```

## 2. Advanced Figure and Axes Management

### 2.1. GridSpec for Complex Layouts

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  import numpy as np
  
  # Create figure
  fig = plt.figure(figsize=(12, 8))
  
  # Create GridSpec with custom spacing
  gs = gridspec.GridSpec(3, 3, 
                         width_ratios=[1, 2, 1],   # Column width ratios
                         height_ratios=[1, 2, 1],  # Row height ratios
                         wspace=0.3,               # Width space between subplots
                         hspace=0.3)               # Height space between subplots
  
  # Create subplots using GridSpec indices
  ax1 = fig.add_subplot(gs[0, :])      # Top row, all columns
  ax2 = fig.add_subplot(gs[1, 0])      # Middle row, first column
  ax3 = fig.add_subplot(gs[1, 1:])     # Middle row, columns 2-3
  ax4 = fig.add_subplot(gs[2, :2])     # Bottom row, first two columns
  ax5 = fig.add_subplot(gs[2, 2])      # Bottom row, last column
  
  # Add sample data to each subplot
  x = np.linspace(0, 10, 100)
  
  ax1.plot(x, np.sin(x), 'b-')
  ax1.set_title('Spanning Full Width')
  
  ax2.bar(['A', 'B', 'C'], [3, 7, 5])
  ax2.set_title('Bar Chart')
  
  ax3.scatter(np.random.randn(50), np.random.randn(50), alpha=0.5)
  ax3.set_title('Scatter Plot (2x width)')
  
  ax4.plot(x, np.cos(x), 'r--')
  ax4.set_title('Cosine Wave')
  
  ax5.pie([30, 25, 20, 25], labels=['A', 'B', 'C', 'D'])
  ax5.set_title('Pie')
  
  fig.suptitle('Complex Layout with GridSpec', fontsize=16, y=0.98)
  plt.show()
```

### 2.2. Nested and Irregular Layouts

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  import numpy as np
  
  fig = plt.figure(figsize=(14, 8))
  
  # Create outer grid
  outer_grid = gridspec.GridSpec(2, 2, wspace=0.3, hspace=0.3)
  
  # Top-left: single plot
  ax1 = fig.add_subplot(outer_grid[0, 0])
  ax1.plot(np.random.randn(100).cumsum())
  ax1.set_title('Single Plot')
  
  # Top-right: nested 2x2 grid
  inner_grid_1 = gridspec.GridSpecFromSubplotSpec(
      2, 2, subplot_spec=outer_grid[0, 1], wspace=0.1, hspace=0.1)
  
  for i in range(4):
      ax = fig.add_subplot(inner_grid_1[i // 2, i % 2])
      ax.plot(np.random.randn(50))
      ax.set_title(f'Nested {i+1}', fontsize=9)
      ax.tick_params(labelsize=8)
  
  # Bottom-left: nested 3x1 grid
  inner_grid_2 = gridspec.GridSpecFromSubplotSpec(
      3, 1, subplot_spec=outer_grid[1, 0], hspace=0.4)
  
  for i in range(3):
      ax = fig.add_subplot(inner_grid_2[i, 0])
      ax.bar(['A', 'B', 'C'], np.random.randint(1, 10, 3))
      ax.set_title(f'Bar {i+1}', fontsize=10)
  
  # Bottom-right: single large plot
  ax_large = fig.add_subplot(outer_grid[1, 1])
  x = np.linspace(0, 10, 100)
  ax_large.plot(x, np.sin(x), 'b-', label='sin')
  ax_large.plot(x, np.cos(x), 'r--', label='cos')
  ax_large.set_title('Large Plot with Legend')
  ax_large.legend()
  ax_large.grid(True, alpha=0.3)
  
  fig.suptitle('Nested GridSpec Layouts', fontsize=16, y=0.98)
  plt.show()
```

## 3. Precise Positioning and Spacing Control

### 3.1. Manual Axes Positioning

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  fig = plt.figure(figsize=(12, 8))
  
  # Manual positioning: [left, bottom, width, height] in figure coordinates (0-1)
  ax1 = fig.add_axes([0.1, 0.7, 0.35, 0.25])  # Top-left
  ax2 = fig.add_axes([0.55, 0.7, 0.35, 0.25]) # Top-right
  ax3 = fig.add_axes([0.1, 0.35, 0.35, 0.25]) # Middle-left
  ax4 = fig.add_axes([0.55, 0.35, 0.35, 0.25]) # Middle-right
  ax5 = fig.add_axes([0.1, 0.05, 0.8, 0.2])   # Bottom (wide)
  
  # Inset axes
  ax_inset = fig.add_axes([0.62, 0.77, 0.15, 0.1])  # Inside ax2
  
  # Add data
  x = np.linspace(0, 10, 100)
  
  ax1.plot(x, np.sin(x), 'b-')
  ax1.set_title('Sine Wave')
  
  ax2.plot(x, np.cos(x), 'r-')
  ax2.set_title('Cosine Wave')
  
  ax3.scatter(np.random.randn(30), np.random.randn(30))
  ax3.set_title('Scatter')
  
  ax4.hist(np.random.randn(100), bins=20, alpha=0.7)
  ax4.set_title('Histogram')
  
  ax5.plot(x, x**2, 'g-', linewidth=2)
  ax5.set_title('Wide Bottom Plot')
  ax5.set_xlabel('X axis')
  
  # Inset plot
  ax_inset.plot(x[:20], np.cos(x[:20]), 'r-', linewidth=1)
  ax_inset.set_title('Inset', fontsize=8)
  ax_inset.tick_params(labelsize=6)
  ax_inset.set_facecolor('#f0f0f0')
  
  fig.suptitle('Manual Axes Positioning', fontsize=16, y=0.98)
  plt.show()
  
  # Print positions for reference
  for i, ax in enumerate([ax1, ax2, ax3, ax4, ax5], 1):
      pos = ax.get_position()
      print(f"Ax{i}: left={pos.x0:.2f}, bottom={pos.y0:.2f}, width={pos.width:.2f}, height={pos.height:.2f}")
```

### 3.2. Fine-tuning with subplots_adjust

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  from pyodide.http import open_url
  import pandas as pd
  
  # Load GDP data
  url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
  df = pd.read_csv(open_url(url))
  
  # Get data for specific countries
  countries = ['United States', 'China', 'Japan', 'Germany']
  latest_year = 2019
  
  fig, axes = plt.subplots(2, 2, figsize=(14, 10))
  
  for idx, (ax, country) in enumerate(zip(axes.flat, countries)):
      country_data = df[df['Country Name'] == country]
      country_data = country_data[country_data['Year'] >= 2000]
      
      ax.plot(country_data['Year'], country_data['Value']/1e12, 
              marker='o', markersize=4, linewidth=2)
      ax.set_title(f'{country} GDP Evolution', fontsize=12, pad=10)
      ax.set_xlabel('Year', fontsize=10)
      ax.set_ylabel('GDP (Trillion USD)', fontsize=10)
      ax.grid(True, alpha=0.3)
      ax.tick_params(labelsize=9)
  
  # Fine-tune spacing
  plt.subplots_adjust(
      left=0.08,    # Left margin
      right=0.95,   # Right margin
      top=0.92,     # Top margin
      bottom=0.08,  # Bottom margin
      wspace=0.25,  # Width space between subplots
      hspace=0.35   # Height space between subplots
  )
  
  fig.suptitle('GDP Comparison with Fine-tuned Spacing', fontsize=14, y=0.98)
  
  # Add text annotation about spacing
  fig.text(0.5, 0.02, 'Spacing: left=0.08, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.35',
           ha='center', fontsize=9, style='italic', color='gray')
  
  plt.show()
```
