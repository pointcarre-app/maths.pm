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

### 2.1. Essential Import and Setup

```yaml
f_type: "codex_"
height_in_px: 250
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load GDP data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities (regions, income groups, aggregates)
    exclude_codes = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    
    # Filter to keep only individual countries
    df_countries = df[~df['Country Code'].isin(exclude_codes)] if 'Country Code' in df.columns else df
    
    print(f"Full dataset shape: {df.shape}")
    print(f"Countries only shape: {df_countries.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Years range: {df_countries['Year'].min()} - {df_countries['Year'].max()}")
```

### 2.2. Core Matplotlib Components

#### Figure and Axes
```yaml
f_type: "codex_"
height_in_px: 400
inline: |
    import matplotlib.pyplot as plt
    
    # Create figure with specific size
    fig = plt.figure(figsize=(10, 6))
    
    # Add axes (subplot)
    ax = fig.add_subplot(111)  # 1 row, 1 col, plot 1
    
    # Basic configuration
    ax.set_title('Figure and Axes Structure', fontsize=14)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.grid(True, alpha=0.3)
    
    # Add some demo text
    ax.text(0.5, 0.5, 'This is the plotting area', 
            ha='center', va='center', fontsize=12)
    
    plt.show()
```

### 2.3. Line Plot - Continuous Data

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
    # USA is a real country so no filtering needed here
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

### 2.4. Bar Chart - Nominal Categories

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
    
    # Exclude non-country entities
    exclude_codes = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(exclude_codes)] if 'Country Code' in df.columns else df
    
    # Top 5 countries by GDP in 2020 (nominal categories)
    df_2020 = df_countries[df_countries['Year'] == 2020].nlargest(5, 'Value')
    
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

### 2.5. Scatter Plot - Two Quantitative Variables

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
    
    # Exclude non-country entities
    exclude_codes = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(exclude_codes)] if 'Country Code' in df.columns else df
    
    # Compare GDP in 2000 vs 2020 for countries
    df_2000 = df_countries[df_countries['Year'] == 2000][['Country Name', 'Value']].rename(columns={'Value': 'GDP_2000'})
    df_2020 = df_countries[df_countries['Year'] == 2020][['Country Name', 'Value']].rename(columns={'Value': 'GDP_2020'})
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

### 2.6. Subplot - Multiple Plots

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
    
    # Note: These are all real countries, so no filtering needed here
    # But for completeness, showing how to filter if needed
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

## Key Matplotlib Functions Reference

### Essential Methods

| Function | Purpose | Common Parameters |
|----------|---------|-------------------|
| `plt.figure()` | Create new figure | `figsize=(width, height)` |
| `plt.plot()` | Line plot | `x, y, color, linewidth, marker` |
| `plt.scatter()` | Scatter plot | `x, y, s=size, c=color, alpha` |
| `plt.bar()` | Bar chart | `x, height, width, color` |
| `plt.subplot()` | Create subplots | `rows, cols, index` |
| `plt.xlabel()` | Set x-axis label | `label, fontsize` |
| `plt.ylabel()` | Set y-axis label | `label, fontsize` |
| `plt.title()` | Set plot title | `title, fontsize` |
| `plt.legend()` | Add legend | `labels, loc` |
| `plt.grid()` | Add grid | `True/False, alpha` |
| `plt.show()` | Display plot | - |

### Color and Style Options

```yaml
f_type: "codex_"
height_in_px: 400
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.linspace(0, 10, 100)
    
    plt.figure(figsize=(12, 4))
    
    # Different line styles and colors
    styles = ['-', '--', '-.', ':']
    colors = ['blue', 'red', 'green', 'purple']
    markers = ['o', 's', '^', 'd']
    
    for i, (style, color, marker) in enumerate(zip(styles, colors, markers)):
        y = np.sin(x + i * np.pi/4)
        plt.plot(x[::10], y[::10], linestyle=style, color=color, 
                marker=marker, label=f'Style: {style}', linewidth=2)
    
    plt.title('Matplotlib Styling Options')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
```

## Summary

- **Data Types**: Understanding variable types (nominal, ordinal, discrete, continuous) is crucial for choosing appropriate visualizations
- **Matplotlib Basics**: Start with `plt.figure()`, use `plt.plot()` for continuous data, `plt.bar()` for categories, and `plt.scatter()` for relationships
- **Key Principle**: Match visualization type to data type for effective communication
