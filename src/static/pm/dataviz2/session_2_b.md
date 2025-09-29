# Advanced matplotlib: Complete API reference & best practices

A comprehensive guide to matplotlib's advanced features, focusing on precise control, professional styling, and production-ready visualizations.
{: .pm-subtitle}

[TOC]

## 1. Configuration & environment setup

### 1.1. Global configuration with rcParams

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

### 1.2. Context managers for temporary settings

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

## 2. Advanced figure and axes management

### 2.1. GridSpec for complex layouts

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

### 2.2. Nested and irregular layouts

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

## 3. Precise positioning and spacing control

### 3.1. Manual axes positioning

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

## 4. Advanced annotation and text control

### 4.1. Comprehensive annotation options

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import matplotlib.patches as patches
  import numpy as np
  
  fig, ax = plt.subplots(figsize=(12, 8))
  
  # Sample data
  x = np.linspace(0, 10, 100)
  y = np.sin(x) * np.exp(-x/10)
  
  ax.plot(x, y, 'b-', linewidth=2, label='Damped sine wave')
  
  # Different annotation styles
  
  # 1. Simple annotation with arrow
  ax.annotate('Local maximum',
              xy=(1.5, 0.85), xytext=(3, 1.2),
              arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
              fontsize=11, color='red')
  
  # 2. Fancy arrow with bbox
  ax.annotate('Important point',
              xy=(5, -0.1), xytext=(6.5, -0.4),
              arrowprops=dict(arrowstyle='fancy', 
                            connectionstyle='arc3,rad=0.3',
                            color='green', lw=2),
              bbox=dict(boxstyle='round,pad=0.5', 
                       facecolor='yellow', alpha=0.7),
              fontsize=10, fontweight='bold')
  
  # 3. Curved arrow with custom connectionstyle
  ax.annotate('Decay region',
              xy=(8, 0.05), xytext=(8.5, 0.3),
              arrowprops=dict(arrowstyle='wedge',
                            connectionstyle='arc3,rad=-0.3',
                            color='purple', lw=1.5),
              fontsize=10, color='purple')
  
  # 4. Double-headed arrow
  ax.annotate('', xy=(0.5, -0.5), xytext=(2.5, -0.5),
              arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
  ax.text(1.5, -0.6, 'Period', ha='center', fontsize=10, color='blue')
  
  # 5. Text with rotation and alignment
  ax.text(7, 0.6, 'Rotated text\nwith line break', 
          rotation=25, fontsize=11,
          ha='center', va='bottom',
          bbox=dict(boxstyle='sawtooth,pad=0.3', 
                   facecolor='lightblue', alpha=0.7))
  
  # 6. Mathematical notation
  ax.text(4, 0.7, r'$y = \sin(x) \cdot e^{-x/10}$',
          fontsize=14, color='black',
          bbox=dict(boxstyle='round,pad=0.5', 
                   facecolor='white', edgecolor='black'))
  
  ax.set_xlim(0, 10)
  ax.set_ylim(-0.8, 1.4)
  ax.set_title('Advanced Annotation Techniques', fontsize=14, fontweight='bold')
  ax.set_xlabel('X axis')
  ax.set_ylabel('Y axis')
  ax.grid(True, alpha=0.3)
  ax.legend(loc='upper right')
  
  plt.tight_layout()
  plt.show()
```

## 5. Professional styling and themes

### 5.1. Custom style sheets

```yaml
f_type: "codex_"
height_in_px: 700
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Define custom style dictionary
  custom_style = {
      # Colors
      'axes.prop_cycle': plt.cycler('color', 
          ['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557']),
      
      # Figure
      'figure.facecolor': '#F8F9FA',
      'figure.edgecolor': 'none',
      
      # Axes
      'axes.facecolor': 'white',
      'axes.edgecolor': '#CCCCCC',
      'axes.linewidth': 1.5,
      'axes.grid': True,
      'axes.spines.top': False,
      'axes.spines.right': False,
      'axes.spines.left': True,
      'axes.spines.bottom': True,
      
      # Grid
      'grid.color': '#E0E0E0',
      'grid.linestyle': '-',
      'grid.linewidth': 0.8,
      'grid.alpha': 0.5,
      
      # Ticks
      'xtick.major.size': 5,
      'xtick.major.width': 1.5,
      'ytick.major.size': 5,
      'ytick.major.width': 1.5,
      'xtick.minor.visible': True,
      'ytick.minor.visible': True,
      'xtick.minor.size': 3,
      'ytick.minor.size': 3,
      
      # Font
      'font.size': 11,
      'axes.titlesize': 14,
      'axes.labelsize': 12,
      
      # Legend
      'legend.frameon': True,
      'legend.fancybox': True,
      'legend.shadow': True,
      'legend.framealpha': 0.9,
      'legend.edgecolor': '#CCCCCC'
  }
  
  # Apply custom style
  with plt.rc_context(custom_style):
      fig, axes = plt.subplots(2, 2, figsize=(12, 8))
      
      x = np.linspace(0, 10, 100)
      
      # Different plot types with custom style
      axes[0, 0].plot(x, np.sin(x), linewidth=2, label='sin')
      axes[0, 0].plot(x, np.cos(x), linewidth=2, label='cos')
      axes[0, 0].set_title('Line Plot')
      axes[0, 0].legend()
      
      axes[0, 1].bar(['A', 'B', 'C', 'D'], [23, 45, 56, 78], alpha=0.8)
      axes[0, 1].set_title('Bar Chart')
      
      axes[1, 0].scatter(np.random.randn(50), np.random.randn(50), 
                        s=100, alpha=0.6, edgecolors='black', linewidth=1)
      axes[1, 0].set_title('Scatter Plot')
      
      axes[1, 1].hist(np.random.randn(100), bins=20, alpha=0.7, edgecolor='black')
      axes[1, 1].set_title('Histogram')
      
      fig.suptitle('Custom Professional Style', fontsize=16, fontweight='bold')
      plt.tight_layout()
      plt.show()
  
  print("✅ Custom style applied successfully")
```

### 5.2. Publication-ready figures

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib.ticker import MultipleLocator, FormatStrFormatter
  
  # Publication settings
  plt.rcParams.update({
      'font.size': 10,
      'font.family': 'serif',
      'font.serif': ['Times New Roman', 'DejaVu Serif'],
      'text.usetex': False,  # Would be True for LaTeX rendering
      'axes.linewidth': 0.8,
      'lines.linewidth': 1.5,
      'lines.markersize': 6,
      'xtick.major.width': 0.8,
      'ytick.major.width': 0.8,
      'xtick.major.size': 4,
      'ytick.major.size': 4,
      'figure.dpi': 100,
      'savefig.dpi': 300
  })
  
  # Create figure with precise dimensions (in inches for publications)
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))  # Common journal width
  
  # Left panel: Multiple time series
  x = np.linspace(0, 4*np.pi, 200)
  y1 = np.sin(x) * np.exp(-x/10)
  y2 = np.cos(x) * np.exp(-x/10)
  
  ax1.plot(x, y1, 'k-', label='Dataset A', linewidth=1.5)
  ax1.plot(x, y2, 'k--', label='Dataset B', linewidth=1.5)
  ax1.fill_between(x, y1, y2, where=(y1 >= y2), alpha=0.3, color='gray', label='A > B')
  
  ax1.set_xlabel('Time (s)', fontsize=11)
  ax1.set_ylabel('Amplitude (a.u.)', fontsize=11)
  ax1.set_title('(a) Time Series Comparison', fontsize=11, fontweight='bold', loc='left')
  
  # Set precise tick locations
  ax1.xaxis.set_major_locator(MultipleLocator(np.pi))
  ax1.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
  ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
  
  ax1.legend(loc='upper right', fontsize=9, framealpha=1)
  ax1.grid(True, alpha=0.3, which='major')
  ax1.grid(True, alpha=0.1, which='minor')
  
  # Right panel: Statistical plot
  data = [np.random.normal(0, std, 100) for std in range(1, 4)]
  positions = [1, 2, 3]
  
  bp = ax2.boxplot(data, positions=positions, widths=0.6,
                   patch_artist=True,
                   boxprops=dict(facecolor='lightgray', color='black'),
                   whiskerprops=dict(color='black'),
                   capprops=dict(color='black'),
                   medianprops=dict(color='red', linewidth=2),
                   flierprops=dict(marker='o', markerfacecolor='gray', 
                                  markersize=4, alpha=0.5))
  
  ax2.set_xlabel('Group', fontsize=11)
  ax2.set_ylabel('Value', fontsize=11)
  ax2.set_title('(b) Statistical Distribution', fontsize=11, fontweight='bold', loc='left')
  ax2.set_xticks(positions)
  ax2.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
  ax2.grid(True, alpha=0.3, axis='y')
  
  # Add significance markers
  y_max = 6
  ax2.plot([1, 2], [y_max-0.5, y_max-0.5], 'k-', linewidth=1)
  ax2.plot([1, 1], [y_max-0.5, y_max-0.7], 'k-', linewidth=1)
  ax2.plot([2, 2], [y_max-0.5, y_max-0.7], 'k-', linewidth=1)
  ax2.text(1.5, y_max-0.3, '**', ha='center', fontsize=12)
  
  # Adjust layout with precise spacing
  plt.tight_layout(pad=1.5)
  
  # Add figure label
  fig.text(0.02, 0.98, 'Figure 1', fontsize=12, fontweight='bold', 
           transform=fig.transFigure)
  
  plt.show()
  
  print("📊 Publication-ready figure created")
  print("💡 For actual publication: set text.usetex=True for LaTeX rendering")
```

### 4.2. Text positioning and transforms

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
  import matplotlib.pyplot as plt
  import matplotlib.transforms as transforms
  import numpy as np
  
  fig, ax = plt.subplots(figsize=(10, 6))
  
  # Sample data
  x = np.linspace(0, 10, 50)
  y = 2 * np.sin(x) + 1
  ax.plot(x, y, 'b-', linewidth=2)
  
  # Different coordinate systems
  
  # 1. Data coordinates (default)
  ax.text(5, 2, 'Data coords (5, 2)', 
          fontsize=10, color='blue',
          bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
  
  # 2. Axes coordinates (0-1 for both x and y)
  ax.text(0.1, 0.9, 'Axes coords (0.1, 0.9)',
          transform=ax.transAxes, fontsize=10, color='red',
          bbox=dict(boxstyle='round', facecolor='pink', alpha=0.5))
  
  # 3. Figure coordinates
  fig.text(0.15, 0.02, 'Figure coords (0.15, 0.02)',
           fontsize=10, color='green',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
  
  # 4. Blended transforms (x in data, y in axes)
  trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
  ax.text(7, 0.5, 'Blended\n(x=data, y=axes)',
          transform=trans, fontsize=10, color='purple',
          ha='center', va='center',
          bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))
  
  # 5. Offset from data point
  offset = transforms.ScaledTranslation(0.1, 0.1, fig.dpi_scale_trans)
  shadow_transform = ax.transData + offset
  
  # Plot point with shadow text
  ax.plot(3, 1.5, 'ro', markersize=10)
  ax.text(3, 1.5, 'Point', ha='center', va='center', color='white', fontweight='bold')
  ax.text(3, 1.5, 'Shadow', transform=shadow_transform, 
          ha='center', va='center', color='gray', alpha=0.5)
  
  ax.set_xlim(0, 10)
  ax.set_ylim(-2, 4)
  ax.set_title('Text Positioning with Different Coordinate Systems', fontsize=12, fontweight='bold')
  ax.grid(True, alpha=0.3)
  
  plt.tight_layout()
  plt.show()
```

## 5. Professional styling and themes

### 5.1. Custom style sheets

```yaml
f_type: "codex_"
height_in_px: 700
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Define custom style dictionary
  custom_style = {
      # Colors
      'axes.prop_cycle': plt.cycler('color', 
          ['#E63946', '#F1FAEE', '#A8DADC', '#457B9D', '#1D3557']),
      
      # Figure
      'figure.facecolor': '#F8F9FA',
      'figure.edgecolor': 'none',
      
      # Axes
      'axes.facecolor': 'white',
      'axes.edgecolor': '#CCCCCC',
      'axes.linewidth': 1.5,
      'axes.grid': True,
      'axes.spines.top': False,
      'axes.spines.right': False,
      'axes.spines.left': True,
      'axes.spines.bottom': True,
      
      # Grid
      'grid.color': '#E0E0E0',
      'grid.linestyle': '-',
      'grid.linewidth': 0.8,
      'grid.alpha': 0.5,
      
      # Ticks
      'xtick.major.size': 5,
      'xtick.major.width': 1.5,
      'ytick.major.size': 5,
      'ytick.major.width': 1.5,
      'xtick.minor.visible': True,
      'ytick.minor.visible': True,
      'xtick.minor.size': 3,
      'ytick.minor.size': 3,
      
      # Font
      'font.size': 11,
      'axes.titlesize': 14,
      'axes.labelsize': 12,
      
      # Legend
      'legend.frameon': True,
      'legend.fancybox': True,
      'legend.shadow': True,
      'legend.framealpha': 0.9,
      'legend.edgecolor': '#CCCCCC'
  }
  
  # Apply custom style
  with plt.rc_context(custom_style):
      fig, axes = plt.subplots(2, 2, figsize=(12, 8))
      
      x = np.linspace(0, 10, 100)
      
      # Different plot types with custom style
      axes[0, 0].plot(x, np.sin(x), linewidth=2, label='sin')
      axes[0, 0].plot(x, np.cos(x), linewidth=2, label='cos')
      axes[0, 0].set_title('Line Plot')
      axes[0, 0].legend()
      
      axes[0, 1].bar(['A', 'B', 'C', 'D'], [23, 45, 56, 78], alpha=0.8)
      axes[0, 1].set_title('Bar Chart')
      
      axes[1, 0].scatter(np.random.randn(50), np.random.randn(50), 
                        s=100, alpha=0.6, edgecolors='black', linewidth=1)
      axes[1, 0].set_title('Scatter Plot')
      
      axes[1, 1].hist(np.random.randn(100), bins=20, alpha=0.7, edgecolor='black')
      axes[1, 1].set_title('Histogram')
      
      fig.suptitle('Custom Professional Style', fontsize=16, fontweight='bold')
  plt.tight_layout()
  plt.show()
  
  print("✅ Custom style applied successfully")
```

### 5.2. Publication-ready figures

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib.ticker import MultipleLocator, FormatStrFormatter
  
  # Publication settings
  plt.rcParams.update({
      'font.size': 10,
      'font.family': 'serif',
      'font.serif': ['Times New Roman', 'DejaVu Serif'],
      'text.usetex': False,  # Would be True for LaTeX rendering
      'axes.linewidth': 0.8,
      'lines.linewidth': 1.5,
      'lines.markersize': 6,
      'xtick.major.width': 0.8,
      'ytick.major.width': 0.8,
      'xtick.major.size': 4,
      'ytick.major.size': 4,
      'figure.dpi': 100,
      'savefig.dpi': 300
  })
  
  # Create figure with precise dimensions (in inches for publications)
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))  # Common journal width
  
  # Left panel: Multiple time series
  x = np.linspace(0, 4*np.pi, 200)
  y1 = np.sin(x) * np.exp(-x/10)
  y2 = np.cos(x) * np.exp(-x/10)
  
  ax1.plot(x, y1, 'k-', label='Dataset A', linewidth=1.5)
  ax1.plot(x, y2, 'k--', label='Dataset B', linewidth=1.5)
  ax1.fill_between(x, y1, y2, where=(y1 >= y2), alpha=0.3, color='gray', label='A > B')
  
  ax1.set_xlabel('Time (s)', fontsize=11)
  ax1.set_ylabel('Amplitude (a.u.)', fontsize=11)
  ax1.set_title('(a) Time Series Comparison', fontsize=11, fontweight='bold', loc='left')
  
  # Set precise tick locations
  ax1.xaxis.set_major_locator(MultipleLocator(np.pi))
  ax1.xaxis.set_minor_locator(MultipleLocator(np.pi/2))
  ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
  
  ax1.legend(loc='upper right', fontsize=9, framealpha=1)
  ax1.grid(True, alpha=0.3, which='major')
  ax1.grid(True, alpha=0.1, which='minor')
  
  # Right panel: Statistical plot
  data = [np.random.normal(0, std, 100) for std in range(1, 4)]
  positions = [1, 2, 3]
  
  bp = ax2.boxplot(data, positions=positions, widths=0.6,
                   patch_artist=True,
                   boxprops=dict(facecolor='lightgray', color='black'),
                   whiskerprops=dict(color='black'),
                   capprops=dict(color='black'),
                   medianprops=dict(color='red', linewidth=2),
                   flierprops=dict(marker='o', markerfacecolor='gray', 
                                  markersize=4, alpha=0.5))
  
  ax2.set_xlabel('Group', fontsize=11)
  ax2.set_ylabel('Value', fontsize=11)
  ax2.set_title('(b) Statistical Distribution', fontsize=11, fontweight='bold', loc='left')
  ax2.set_xticks(positions)
  ax2.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
  ax2.grid(True, alpha=0.3, axis='y')
  
  # Add significance markers
  y_max = 6
  ax2.plot([1, 2], [y_max-0.5, y_max-0.5], 'k-', linewidth=1)
  ax2.plot([1, 1], [y_max-0.5, y_max-0.7], 'k-', linewidth=1)
  ax2.plot([2, 2], [y_max-0.5, y_max-0.7], 'k-', linewidth=1)
  ax2.text(1.5, y_max-0.3, '**', ha='center', fontsize=12)
  
  # Adjust layout with precise spacing
  plt.tight_layout(pad=1.5)
  
  # Add figure label
  fig.text(0.02, 0.98, 'Figure 1', fontsize=12, fontweight='bold', 
           transform=fig.transFigure)
  
  plt.show()
  
  print("📊 Publication-ready figure created")
  print("💡 For actual publication: set text.usetex=True for LaTeX rendering")
```

## 6. Color management and colormaps

### 6.1. Advanced colormap usage

```yaml
f_type: "codex_"
height_in_px: 700
inline: |
  import matplotlib.pyplot as plt
  import matplotlib.colors as mcolors
  import numpy as np
  from matplotlib.colors import LinearSegmentedColormap, ListedColormap
  
  fig, axes = plt.subplots(2, 3, figsize=(14, 8))
  
  # Generate sample data
  x = np.linspace(-3, 3, 100)
  y = np.linspace(-3, 3, 100)
  X, Y = np.meshgrid(x, y)
  Z = np.sin(np.sqrt(X**2 + Y**2))
  
  # 1. Sequential colormap
  im1 = axes[0, 0].imshow(Z, cmap='viridis', aspect='auto')
  axes[0, 0].set_title('Sequential: Viridis')
  plt.colorbar(im1, ax=axes[0, 0], fraction=0.046)
  
  # 2. Diverging colormap with custom center
  norm = mcolors.TwoSlopeNorm(vmin=Z.min(), vcenter=0, vmax=Z.max())
  im2 = axes[0, 1].imshow(Z, cmap='RdBu_r', norm=norm, aspect='auto')
  axes[0, 1].set_title('Diverging: RdBu (centered at 0)')
  plt.colorbar(im2, ax=axes[0, 1], fraction=0.046)
  
  # 3. Discrete colormap
  n_bins = 8
  cmap_discrete = plt.cm.get_cmap('plasma', n_bins)
  im3 = axes[0, 2].imshow(Z, cmap=cmap_discrete, aspect='auto')
  axes[0, 2].set_title(f'Discrete: Plasma ({n_bins} levels)')
  plt.colorbar(im3, ax=axes[0, 2], fraction=0.046)
  
  # 4. Custom colormap from list
  colors_list = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF']
  n_bins = 100
  cmap_custom = LinearSegmentedColormap.from_list('custom', colors_list, N=n_bins)
  im4 = axes[1, 0].imshow(Z, cmap=cmap_custom, aspect='auto')
  axes[1, 0].set_title('Custom: Rainbow from List')
  plt.colorbar(im4, ax=axes[1, 0], fraction=0.046)
  
  # 5. Logarithmic normalization
  Z_positive = np.abs(Z) + 0.01  # Make all values positive
  norm_log = mcolors.LogNorm(vmin=Z_positive.min(), vmax=Z_positive.max())
  im5 = axes[1, 1].imshow(Z_positive, cmap='YlOrRd', norm=norm_log, aspect='auto')
  axes[1, 1].set_title('Logarithmic Scale: YlOrRd')
  plt.colorbar(im5, ax=axes[1, 1], fraction=0.046)
  
  # 6. Bounded normalization
  bounds = [-1, -0.5, 0, 0.5, 1]
  norm_bounded = mcolors.BoundaryNorm(bounds, plt.cm.coolwarm.N)
  im6 = axes[1, 2].contourf(X, Y, Z, levels=20, cmap='coolwarm', norm=norm_bounded)
  axes[1, 2].set_title('Bounded Norm: Coolwarm')
  plt.colorbar(im6, ax=axes[1, 2], fraction=0.046, boundaries=bounds, ticks=bounds)
  
  fig.suptitle('Advanced Colormap Techniques', fontsize=14, fontweight='bold')
  plt.tight_layout()
  plt.show()
```

### 6.2. Color accessibility and best practices

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Colorblind-friendly palettes
  colorblind_colors = {
      'blue': '#0173B2',
      'orange': '#DE8F05',
      'green': '#029E73',
      'red': '#CC78BC',
      'purple': '#ECE133',
      'brown': '#56B4E9',
      'pink': '#F0E442',
      'gray': '#999999'
  }
  
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
  
  # Sample data
  categories = list(colorblind_colors.keys())[:5]
  values = [23, 45, 56, 78, 32]
  x = np.linspace(0, 10, 100)
  
  # Left: Bar chart with colorblind-friendly colors
  colors = [colorblind_colors[cat] for cat in categories]
  bars = ax1.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
  
  # Add patterns for additional distinction
  patterns = ['/', '\\\\', '|', '-', '+']
  for bar, pattern in zip(bars, patterns):
      bar.set_hatch(pattern)
  
  ax1.set_title('Colorblind-Friendly with Patterns', fontsize=12, fontweight='bold')
  ax1.set_ylabel('Values')
  ax1.grid(axis='y', alpha=0.3)
  
  # Right: Line plot with distinct styles
  line_styles = ['-', '--', '-.', ':', '-']
  markers = ['o', 's', '^', 'D', 'v']
  
  for i, (cat, color) in enumerate(list(colorblind_colors.items())[:5]):
      y = np.sin(x + i) * np.exp(-x/10)
      ax2.plot(x, y, color=color, linestyle=line_styles[i], 
              marker=markers[i], markevery=10, markersize=8,
              linewidth=2, label=cat)
  
  ax2.set_title('Multiple Line Styles for Accessibility', fontsize=12, fontweight='bold')
  ax2.set_xlabel('X axis')
  ax2.set_ylabel('Y axis')
  ax2.legend(loc='upper right', framealpha=1)
  ax2.grid(True, alpha=0.3)
  
  fig.suptitle('Accessibility Best Practices', fontsize=14, fontweight='bold', y=1.02)
  
  # Add note about accessibility
  fig.text(0.5, -0.02, 
           '💡 Tip: Use both color and patterns/styles for maximum accessibility',
           ha='center', fontsize=10, style='italic', color='gray')
  
  plt.tight_layout()
  plt.show()
```

## 7. Performance optimization

### 7.1. Efficient plotting for large datasets

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  import time
  
  # Generate large dataset
  n_points = 100000
  x = np.random.randn(n_points)
  y = np.random.randn(n_points)
  
  fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
  
  # Method 1: Regular scatter (slow for large data)
  start = time.time()
  ax1.scatter(x[:5000], y[:5000], alpha=0.5, s=1)
  time1 = time.time() - start
  ax1.set_title(f'Regular Scatter (5k points)\nTime: {time1:.3f}s')
  ax1.set_xlabel('X')
  ax1.set_ylabel('Y')
  
  # Method 2: plot with markers (faster)
  start = time.time()
  ax2.plot(x[:50000], y[:50000], 'o', markersize=1, alpha=0.5)
  time2 = time.time() - start
  ax2.set_title(f'Plot with markers (50k points)\nTime: {time2:.3f}s')
  ax2.set_xlabel('X')
  
  # Method 3: hexbin for density (best for large data)
  start = time.time()
  hb = ax3.hexbin(x, y, gridsize=50, cmap='YlOrRd', mincnt=1)
  time3 = time.time() - start
  ax3.set_title(f'Hexbin (all {n_points} points)\nTime: {time3:.3f}s')
  ax3.set_xlabel('X')
  plt.colorbar(hb, ax=ax3, label='Count')
  
  fig.suptitle('Performance Optimization for Large Datasets', fontsize=14, fontweight='bold')
  
  plt.tight_layout()
  plt.show()
  
  print(f"\n📊 Performance Comparison:")
  print(f"  Scatter (5k): {time1:.3f}s")
  print(f"  Plot markers (50k): {time2:.3f}s")
  print(f"  Hexbin (100k): {time3:.3f}s")
  print(f"\n💡 Recommendation: Use hexbin or hist2d for datasets > 10k points")
```

### 7.2. Rasterization for complex plots

```yaml
f_type: "codex_"
height_in_px: 400
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
  
  # Generate data
  n = 10000
  x = np.random.randn(n)
  y = np.random.randn(n)
  
  # Left: Vector graphics (large file size)
  ax1.scatter(x, y, alpha=0.1, s=1, rasterized=False)
  ax1.set_title('Vector Graphics\n(Large file, slow rendering)')
  ax1.set_xlabel('X')
  ax1.set_ylabel('Y')
  
  # Right: Rasterized (small file size)
  ax2.scatter(x, y, alpha=0.1, s=1, rasterized=True)
  ax2.set_title('Rasterized\n(Small file, fast rendering)')
  ax2.set_xlabel('X')
  ax2.set_ylabel('Y')
  
  # Add vector elements on top (not rasterized)
  for ax in [ax1, ax2]:
      ax.axhline(0, color='red', linewidth=2, alpha=0.5)
      ax.axvline(0, color='red', linewidth=2, alpha=0.5)
      ax.grid(True, alpha=0.3)
  
  fig.suptitle('Rasterization for Performance', fontsize=14, fontweight='bold')
  
  plt.tight_layout()
  plt.show()
  
  print("💡 Rasterization benefits:")
  print("  • Smaller file sizes for saved figures")
  print("  • Faster rendering in viewers")
  print("  • Text and axes remain vector (sharp)")
  print("  • Use for: scatter plots, images, pcolormesh with many points")
```

## 8. Backend selection and LaTeX support

### 8.1. Understanding matplotlib backends

Matplotlib uses backends to render figures. The backend determines how plots are displayed and what features are available. When running locally (not in a browser-based environment), you can choose backends that support advanced features like LaTeX rendering.

**Key backend types:**

- **Interactive backends**: Qt5Agg, TkAgg, MacOSX - for GUI windows
- **Non-interactive backends**: Agg, PDF, PS, SVG - for file output only
- **Notebook backends**: notebook, widget - for Jupyter environments

For more details, see the [official matplotlib backend documentation](https://matplotlib.org/stable/users/explain/backends.html).

### 8.2. LaTeX rendering with matplotlib

When running matplotlib locally, you can use LaTeX for beautiful mathematical typography. This requires a LaTeX installation on your system.



The latex below won't be displayed as latex when directly executed in a browser environment with `pyodide`. You need to run it locally.
{: .alert .alert-warning .alert-soft}

```yaml
f_type: "codex_"
height_in_px: 400
inline: |
  import matplotlib.pyplot as plt
  import numpy as np
  
  # Note: LaTeX rendering requires local execution with LaTeX installed
  # This example shows the syntax but won't render LaTeX in browser environments
  
  # Configure matplotlib for LaTeX (for local execution)
  plt.rcParams.update({
      'text.usetex': False,  # Set to True when running locally with LaTeX
      'font.family': 'serif',
      'font.serif': ['Computer Modern Roman'],
      'font.size': 12
  })
  
  # Create sample plot with mathematical notation
  x = np.linspace(0, 2*np.pi, 100)
  y1 = np.sin(x)
  y2 = np.cos(x)
  
  fig, ax = plt.subplots(figsize=(10, 6))
  
  ax.plot(x, y1, 'b-', label=r'$\sin(x)$', linewidth=2)
  ax.plot(x, y2, 'r--', label=r'$\cos(x)$', linewidth=2)
  
  # Mathematical expressions in labels
  ax.set_xlabel(r'$x$ (radians)', fontsize=14)
  ax.set_ylabel(r'$f(x)$', fontsize=14)
  ax.set_title(r'Trigonometric Functions: $\sin(x)$ and $\cos(x)$', fontsize=16)
  
  # Add complex mathematical annotation
  ax.text(np.pi, 0, r'$\int_{0}^{2\pi} \sin(x)\,dx = 0$',
          fontsize=12, ha='center', va='bottom',
          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
  
  # Another mathematical expression
  ax.annotate(r'$\sin^2(x) + \cos^2(x) = 1$',
              xy=(np.pi/4, np.sin(np.pi/4)), xytext=(np.pi/4 + 1, 0.5),
              arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
              fontsize=12, color='green')
  
  ax.legend(loc='upper right', fontsize=12)
  ax.grid(True, alpha=0.3)
  ax.set_xlim(0, 2*np.pi)
  ax.set_ylim(-1.5, 1.5)
  
  plt.tight_layout()
  plt.show()
  
  print("📝 LaTeX rendering notes:")
  print("• Requires LaTeX installation (TeX Live, MiKTeX, or MacTeX)")
  print("• Set text.usetex=True in rcParams")
  print("• Use raw strings (r'...') for LaTeX expressions")
  print("• Expressions between $ signs for math mode")
  print("• Full LaTeX commands available (\\frac, \\sqrt, \\int, etc.)")
```

### 8.3. Backend selection for local execution

```python
# Example of backend selection (for local Python scripts)
import matplotlib
matplotlib.use('Qt5Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt

# Or check current backend
print(matplotlib.get_backend())

# Common backend choices:
# - 'Qt5Agg': High-quality interactive backend (requires PyQt5)
# - 'TkAgg': Default interactive backend (uses Tkinter)
# - 'Agg': High-quality non-interactive backend
# - 'pdf': Direct PDF output
# - 'svg': Scalable vector graphics output
```

**Installation for LaTeX support:**
```bash
# On macOS
brew install --cask mactex

# On Ubuntu/Debian
sudo apt-get install texlive-full

# On Windows
# Download and install MiKTeX from https://miktex.org/

# Python packages
pip install matplotlib[latex]
```

## Summary and quick reference

### Key takeaways

1. **Configuration**: Use `rcParams` for global settings, context managers for temporary changes
2. **Layout**: Master `GridSpec` for complex layouts, `subplots_adjust` for fine-tuning
3. **Performance**: Use appropriate plot types for data size, rasterize when needed
4. **Styling**: Create custom styles for consistency, follow accessibility guidelines
5. **Export**: Match format and DPI to intended use (web/print/publication)
6. **Backends**: Choose appropriate backend for your environment and needs

### Essential commands reference

```python
# Configuration
plt.rcParams.update({...})          # Global settings
with plt.rc_context({...}):         # Temporary settings

# Layout
gs = GridSpec(rows, cols, ...)      # Complex layouts
plt.subplots_adjust(...)            # Fine spacing control
fig.add_axes([l, b, w, h])         # Manual positioning

# Performance
ax.plot(..., rasterized=True)       # Rasterize dense plots
ax.hexbin(x, y, ...)                # Efficient for large data

# Styling
plt.style.use('style_name')         # Apply style
ax.set_prop_cycle(...)              # Custom color cycle

# Export
fig.savefig('file.pdf', dpi=300, bbox_inches='tight')
plt.close(fig)                      # Free memory

# Backend & LaTeX
matplotlib.use('backend_name')      # Set backend
plt.rcParams['text.usetex'] = True  # Enable LaTeX
```

This comprehensive guide covers the advanced aspects of matplotlib not detailed in the basic tutorials, providing you with professional-level control over your visualizations.
