# Data Types Classification and Introduction to Matplotlib

Understanding data types and basic visualization with matplotlib
{: .pm-subtitle}

[TOC]

## Data Types Classification

### 1. Qualitative (Categorical) Variables

#### 1.1. Nominal Variables

- **Definition**: Categories without inherent order
- **Examples**: 
    - Country names (France, USA, Japan)
    - Colors (red, blue, green)
    - Gender (male, female, other)
- **Operations**: Equality (=, ≠) only
- **Basic visualization**: Bar charts, pie charts

#### 1.2. Ordinal Variables  

- **Definition**: Categories with meaningful order
- **Examples**:
    - Education level (Primary < Secondary < University)
    - Survey ratings (Poor < Fair < Good < Excellent)
    - Size categories (Small < Medium < Large)
- **Operations**: Equality and comparison (<, >, ≤, ≥)
- **Basic visualization**: Bar charts with ordered categories

### 2. Quantitative (Numerical) Variables

#### 2.1. Discrete Variables
- **Definition**: Countable values, often integers
- **Examples**:
    - Number of employees: 25, 126, 512
    - Year of construction: 2010, 2015, 2023
    - Number of children: 0, 1, 2, 3
- **Operations**: Most of the times, all numerical operations
- **Basic visualization**: Bar charts, scatter plots

#### 2.2. Continuous Variables
- **Definition**: Any value within a range
- **Examples**:
    - Temperature: 23.5°C, 24.7°C
    - GDP: 1.234 trillion dollars, 45.678 billion dollars
    - Height: 1.75m, 1.823m
- **Operations**: All numerical operations
- **Basic visualization**: Line plots, histograms, scatter plots

### Quick Reference Table

| Type | Order | Math Operations | Example | Best Chart Types |
|------|-------|----------------|---------|------------------|
| **Nominal** | ❌ | Count only | Country names | Bar, Pie |
| **Ordinal** | ✓ | Count, Compare | Education level | Ordered Bar |
| **Discrete** | ✓ | All | Year, Count | Bar, Scatter |
| **Continuous** | ✓ | All | GDP, Temperature | Line, Histogram |

## Basics with Matplotlib

### 2.1. Getting Started with Simple Plots




#### Key principles


`matplotlib` is a powerful library for creating static, interactive, and animated visualizations in Python.
{: .alert .alert-success .alert-soft}


**In particular, a lot of the complexity related to the the building of the layout of the plot is handled by `matplotlib`, without us having to worry about it.**<br>
{: .alert .alert-success .alert-soft}

**However, if more control is needed, we can always use the `matplotlib` API to customize the plot.**
{: .alert .alert-info .alert-soft}

#### Official documentation
[https://matplotlib.org/stable/api/index.html](https://matplotlib.org/stable/api/index.html)
{: .alert .alert-success .alert-soft}

#### Basic import and first plot
```yaml
f_type: "codex_"
height_in_px: 350
inline: |
    import matplotlib.pyplot as plt
    
    # Simple line plot with hardcoded data
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    
    # plt.plot() creates a line plot connecting x and y points
    plt.plot(x, y)
    
    # plt.title() sets the title at the top of the plot
    plt.title('My First Plot')
    
    # plt.show() displays the plot on screen
    plt.show()
```

### 2.2. Line Plot (`plt.plot`)

**Key parameters:** `x`, `y`, `color`, `linewidth`, `linestyle`, `marker`, `markersize`, `label`, `alpha`

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    
    x = [0, 1, 2, 3, 4, 5, 6]
    y1 = [0, 1, 4, 9, 16, 25, 36]
    y2 = [0, 2, 3, 8, 15, 24, 35]
    
    # plt.figure() creates a new figure with specified size (width, height) in inches
    plt.figure(figsize=(10, 5))
    
    # First line: solid blue with circle markers
    plt.plot(x, y1, color='blue', linewidth=2, linestyle='-', 
             marker='o', markersize=8, label='Quadratic', alpha=0.8)
    
    # Second line: dashed red with square markers  
    plt.plot(x, y2, color='red', linewidth=1.5, linestyle='--',
             marker='s', markersize=6, label='Near linear', alpha=0.7)
    
    # plt.xlabel() sets the label for the x-axis
    plt.xlabel('X values')
    # plt.ylabel() sets the label for the y-axis
    plt.ylabel('Y values')
    plt.title('Line Plot with Multiple Parameters')
    # plt.legend() displays a legend box showing labels from plots
    plt.legend()
    # plt.grid() adds a grid to the plot for easier reading
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 2.3. Scatter Plot (`plt.scatter`)

**Key parameters:** `x`, `y`, `s` (size), `c` (color), `alpha`, `edgecolors`, `linewidths`, `marker`

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Generate random data
    np.random.seed(42)
    x = np.random.randn(50)
    y = np.random.randn(50)
    colors = np.random.rand(50)
    sizes = np.random.randint(20, 200, 50)
    
    plt.figure(figsize=(10, 6))
    
    # plt.scatter() creates a scatter plot with individual points
    plt.scatter(x, y, s=sizes, c=colors, alpha=0.6, 
                edgecolors='black', linewidths=1, 
                cmap='viridis', marker='o')
    
    # plt.colorbar() adds a color scale bar showing the mapping of colors to values
    plt.colorbar(label='Color values')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.title('Scatter Plot with Size and Color Mapping')
    plt.grid(True, alpha=0.3)
    plt.show()
```

### 2.4. Bar Chart (`plt.bar`)

**Key parameters:** `x`, `height`, `width`, `color`, `edgecolor`, `linewidth`, `alpha`, `label`

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    
    # Simple data
    x = ['A', 'B', 'C', 'D', 'E']
    y = [23, 45, 56, 78, 32]
    
    plt.figure(figsize=(10, 5))
    
    # plt.bar() creates a bar chart with vertical bars
    bars = plt.bar(x, y, width=0.6, color=['red', 'blue', 'green', 'orange', 'purple'],
                   edgecolor='black', linewidth=2, alpha=0.7)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        # plt.text() adds text annotation at specified coordinates
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}', ha='center', va='bottom')
    
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart with Custom Colors')
    # plt.ylim() sets the y-axis limits (min, max)
    plt.ylim(0, 90)
    plt.grid(axis='y', alpha=0.3)
    plt.show()
```

### 2.5. Pie Chart (`plt.pie`)

**Key parameters:** `x`, `labels`, `colors`, `autopct`, `startangle`, `explode`, `shadow`

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    
    # Data for pie chart
    sizes = [30, 25, 20, 15, 10]
    labels = ['Part A', 'Part B', 'Part C', 'Part D', 'Part E']
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    explode = (0.1, 0, 0, 0, 0)  # Explode first slice
    
    plt.figure(figsize=(10, 8))
    
    # plt.pie() creates a pie chart showing proportions
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, explode=explode, shadow=True)
    
    plt.title('Pie Chart with Exploded Slice')
    # plt.axis('equal') ensures equal aspect ratio for circular shape
    plt.axis('equal')
    plt.show()
```

### 2.6. Subplots (`plt.subplots`)

**Creating multiple plots:** `fig, axes = plt.subplots(nrows, ncols)`

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    
    # plt.subplots() creates a figure and multiple axes (subplots) in one call
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Data
    x = np.linspace(0, 10, 100)
    
    # Top left - Line plot
    axes[0, 0].plot(x, np.sin(x), 'b-', linewidth=2)
    # ax.set_title() sets title for individual subplot
    axes[0, 0].set_title('Sine Wave')
    # ax.set_xlabel() and ax.set_ylabel() label axes for individual subplot
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_ylabel('sin(x)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Top right - Scatter plot
    axes[0, 1].scatter(np.random.rand(30), np.random.rand(30), 
                      c='red', s=50, alpha=0.6)
    axes[0, 1].set_title('Random Scatter')
    axes[0, 1].set_xlabel('x')
    axes[0, 1].set_ylabel('y')
    
    # Bottom left - Bar chart
    categories = ['A', 'B', 'C', 'D']
    values = [3, 7, 2, 5]
    axes[1, 0].bar(categories, values, color='green', alpha=0.7)
    axes[1, 0].set_title('Bar Chart')
    axes[1, 0].set_ylabel('Values')
    
    # Bottom right - Multiple lines
    axes[1, 1].plot(x, x, 'r-', label='Linear')
    axes[1, 1].plot(x, x**0.5, 'b--', label='Square root')
    axes[1, 1].plot(x, np.log(x+1), 'g-.', label='Logarithmic')
    axes[1, 1].set_title('Multiple Functions')
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('f(x)')
    axes[1, 1].legend()
    
    # plt.suptitle() adds a centered title for the entire figure
    plt.suptitle('Subplots Example', fontsize=16, y=1.02)
    # plt.tight_layout() automatically adjusts spacing to prevent overlaps
    plt.tight_layout()
    plt.show()
```

### 2.7. Figure and Axes Control

**Key methods for customization:**

- `plt.figure()`: Create a new figure with `figsize`, `dpi`, `facecolor`
- `plt.xlabel()`, `plt.ylabel()`: Set axis labels with `fontsize`, `fontweight`
- `plt.title()`: Set plot title with `fontsize`, `fontweight`, `pad`
- `plt.xlim()`, `plt.ylim()`: Set axis limits
- `plt.xticks()`, `plt.yticks()`: Customize tick positions and labels
- `plt.legend()`: Add legend with `loc`, `fontsize`, `title`
- `plt.grid()`: Add grid with `axis`, `alpha`, `linestyle`

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Create figure with specific properties
    fig = plt.figure(figsize=(12, 6), facecolor='lightgray')
    
    # Plot data
    plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
    plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')
    
    # Customize axes
    plt.xlabel('Angle (radians)', fontsize=14, fontweight='bold')
    plt.ylabel('Value', fontsize=14, fontweight='bold')
    plt.title('Trigonometric Functions', fontsize=16, fontweight='bold', pad=20)
    
    # plt.xlim() sets the x-axis range limits
    plt.xlim(0, 2*np.pi)
    # plt.ylim() sets the y-axis range limits  
    plt.ylim(-1.5, 1.5)
    
    # plt.xticks() customizes x-axis tick positions and labels
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
               ['0', 'π/2', 'π', '3π/2', '2π'], fontsize=12)
    # plt.yticks() customizes y-axis tick positions and labels
    plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=12)
    
    # plt.axhline() draws a horizontal line across the plot
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Legend with custom position
    plt.legend(loc='upper right', fontsize=12, title='Functions')
    
    # Grid with custom style
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    plt.tight_layout()
    plt.show()
```

## 3. Real Data Examples with GDP Dataset

### 3.1. Loading External Data

```yaml
f_type: "codex_"
height_in_px: 180
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    from pyodide.http import open_url
    
    # Load GDP data from GitHub
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Years range: {df['Year'].min()} - {df['Year'].max()}")
```

### 3.2. Line Plot with Real Time Series Data

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    from pyodide.http import open_url
    
    # Load and prepare data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Get USA GDP over time (continuous variable)
    usa_gdp = df[df['Country Name'] == 'United States'].copy()
    usa_gdp = usa_gdp[usa_gdp['Year'] >= 2000]
    
    # Create line plot
    plt.figure(figsize=(10, 5))
    plt.plot(usa_gdp['Year'], usa_gdp['Value'] / 1e12, 
             linewidth=2, color='blue', marker='o', markersize=4)
    
    plt.title('USA GDP Over Time (Continuous Data)', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('GDP (Trillion USD)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
```

### 3.3. Bar Chart with Country Comparison

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    from pyodide.http import open_url
    
    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Top 5 countries by GDP in 2020 (nominal categories)
    df_2020 = df[df['Year'] == 2020].nlargest(5, 'Value')
    
    # Create bar chart
    plt.figure(figsize=(10, 5))
    bars = plt.bar(range(len(df_2020)), df_2020['Value'].values / 1e12, 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    
    plt.xticks(range(len(df_2020)), df_2020['Country Name'].values, rotation=45, ha='right')
    plt.title('Top 5 Economies by GDP in 2020 (Nominal Categories)', fontsize=14)
    plt.ylabel('GDP (Trillion USD)')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
```

### 3.4. Scatter Plot - GDP Growth Comparison

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Compare GDP in 2000 vs 2020 for countries
    df_2000 = df[df['Year'] == 2000][['Country Name', 'Value']].rename(columns={'Value': 'GDP_2000'})
    df_2020 = df[df['Year'] == 2020][['Country Name', 'Value']].rename(columns={'Value': 'GDP_2020'})
    df_compare = df_2000.merge(df_2020, on='Country Name')
    
    # Filter for visibility
    df_compare = df_compare[(df_compare['GDP_2000'] > 1e11) & (df_compare['GDP_2020'] > 1e11)]
    
    # Create scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter(df_compare['GDP_2000'] / 1e12, df_compare['GDP_2020'] / 1e12, 
                s=80, alpha=0.6, c='blue', edgecolor='black')
    
    # Add diagonal reference line
    max_val = max(df_compare[['GDP_2000', 'GDP_2020']].max() / 1e12)
    plt.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='No growth line')
    
    plt.xlabel('GDP 2000 (Trillion USD)', fontsize=12)
    plt.ylabel('GDP 2020 (Trillion USD)', fontsize=12)
    plt.title('GDP Growth: 2000 vs 2020', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
```

### 3.5. Complex Visualization with Subplots

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    from pyodide.http import open_url
    
    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Prepare data for different countries
    countries = ['United States', 'China', 'Japan', 'Germany']
    colors = ['blue', 'red', 'green', 'orange']
    
    # Create 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('GDP Trends for Major Economies', fontsize=16)
    
    for idx, (country, color) in enumerate(zip(countries, colors)):
        ax = axes[idx // 2, idx % 2]
        country_data = df[(df['Country Name'] == country) & (df['Year'] >= 2010)]
        
        ax.plot(country_data['Year'], country_data['Value'] / 1e12, 
                color=color, linewidth=2, marker='o', markersize=3)
        ax.set_title(country)
        ax.set_xlabel('Year')
        ax.set_ylabel('GDP (Trillion USD)')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
```

## 4. Quick Reference Guide

### Essential Matplotlib Methods

| Function | Purpose | Common Parameters |
|----------|---------|-------------------|
| `plt.figure()` | Create new figure | `figsize=(width, height)`, `dpi`, `facecolor` |
| `plt.plot()` | Line plot | `x`, `y`, `color`, `linewidth`, `linestyle`, `marker` |
| `plt.scatter()` | Scatter plot | `x`, `y`, `s` (size), `c` (color), `alpha`, `edgecolors` |
| `plt.bar()` | Bar chart | `x`, `height`, `width`, `color`, `edgecolor` |
| `plt.pie()` | Pie chart | `x`, `labels`, `colors`, `autopct`, `explode` |
| `plt.subplot()` | Create subplots | `rows`, `cols`, `index` |
| `plt.subplots()` | Create figure and axes | `nrows`, `ncols`, `figsize` |
| `plt.xlabel()` | Set x-axis label | `label`, `fontsize`, `fontweight` |
| `plt.ylabel()` | Set y-axis label | `label`, `fontsize`, `fontweight` |
| `plt.title()` | Set plot title | `title`, `fontsize`, `fontweight`, `pad` |
| `plt.legend()` | Add legend | `labels`, `loc`, `fontsize` |
| `plt.grid()` | Add grid | `True/False`, `axis`, `alpha`, `linestyle` |
| `plt.xlim()` | Set x-axis limits | `left`, `right` |
| `plt.ylim()` | Set y-axis limits | `bottom`, `top` |
| `plt.xticks()` | Set x-axis ticks | `ticks`, `labels`, `rotation` |
| `plt.tight_layout()` | Adjust subplot params | `pad`, `h_pad`, `w_pad` |
| `plt.show()` | Display plot | - |

### Common Line Styles and Markers

| Line Styles | Description | Markers | Description |
|-------------|-------------|---------|-------------|
| `'-'` | Solid line | `'o'` | Circle |
| `'--'` | Dashed line | `'s'` | Square |
| `'-.'` | Dash-dot line | `'^'` | Triangle up |
| `':'` | Dotted line | `'v'` | Triangle down |
| | | `'*'` | Star |
| | | `'d'` | Diamond |
| | | `'+'` | Plus |
| | | `'x'` | Cross |

## Summary

- **Data Types**: Understanding variable types (nominal, ordinal, discrete, continuous) is crucial for choosing appropriate visualizations
- **Matplotlib Basics**: Start with `plt.figure()`, use `plt.plot()` for continuous data, `plt.bar()` for categories, and `plt.scatter()` for relationships
- **Key Principle**: Match visualization type to data type for effective communication
