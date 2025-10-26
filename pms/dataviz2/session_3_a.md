---
js_dependencies:
  - "https://cdn.bokeh.org/bokeh/release/bokeh-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.6.2.min.js"
  - "https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.6.2.min.js"
---

# Bokeh presentation and basic usage

Bokeh enables the creation of interactive visualizations for data analysis and storytelling.
{: .pm-subtitle}

[TOC]

## Introduction to Bokeh

### What is Bokeh?

**Bokeh** is a Python library for creating interactive visualizations for modern web browsers. Unlike static plots from matplotlib, Bokeh plots allow users to pan, zoom, select, and hover over data points.
{: .alert .alert-success .alert-soft}



> [Bokeh official website](https://bokeh.org/)

**Key advantages of Bokeh:**

- **Interactive by default**: Pan, zoom, reset, save tools built-in
- **Web-ready**: Outputs HTML/JavaScript that works in any browser
- **Server capabilities**: Can build interactive dashboards and applications
- **Large dataset handling**: Efficient rendering of millions of points
{: .alert .alert-info .alert-soft}

### Core Concepts

#### Key Components

| Component | Description | Example Usage |
|-----------|-------------|---------------|
| **`figure()`** | Creates a plot object | `p = figure(width=600, height=400)` |
| **Glyphs** | Visual marks (circles, lines, bars) | `p.circle(x, y)`, `p.line(x, y)` |
| **Tools** | Interactive controls | Pan, Zoom, Reset, Hover, Select |
| **`curdoc()`** | Current document container | `curdoc().add_root(p)` |
| **Layouts** | Arrange multiple plots | `column()`, `row()`, `gridplot()` |

#### Basic Workflow

1. **Create a figure**: Define the canvas with tools and properties
2. **Add glyphs**: Plot your data using various visual elements
3. **Configure tools**: Customize interactivity (hover tooltips, selection)
4. **Style the plot**: Set colors, labels, titles, legends
5. **Add to document**: Make the plot available for rendering

## Getting Started with Bokeh

### 2.1. Your First Interactive Plot

```yaml
f_type: "codex_"
height_in_px: 400
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool
    import numpy as np
    
    # Generate sample data
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x)
    y2 = np.cos(x)
    
    # Create a new plot with a title and axis labels
    p = figure(
        title="Interactive Trigonometric Functions",
        x_axis_label='x',
        y_axis_label='y',
        width=700,
        height=400,
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    
    # Add line renderers with legend and line thickness
    line1 = p.line(x, y, legend_label="sin(x)", line_width=2, color='navy', alpha=0.8)
    line2 = p.line(x, y2, legend_label="cos(x)", line_width=2, color='red', alpha=0.8)
    
    # Add circle markers at specific points
    sample_indices = list(range(0, 100, 10))
    p.circle(x[sample_indices], y[sample_indices], size=8, color='navy', alpha=0.5)
    p.circle(x[sample_indices], y2[sample_indices], size=8, color='red', alpha=0.5)
    
    # Configure hover tool
    hover = HoverTool(tooltips=[("(x,y)", "($x, $y)")])
    p.add_tools(hover)
    
    # Customize the legend
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"  # Click legend to hide/show lines
    
    # Add grid styling
    p.grid.grid_line_alpha = 0.3
    
    # Add the plot to the current document
    curdoc().add_root(p)
    
    print("✅ Interactive plot created!")
    print("🎯 Try: Pan, zoom, hover over points, click legend items to toggle visibility")
```

### 2.2. Understanding Bokeh Tools

**Built-in tools provide interactivity without additional code:**

| Tool | Icon | Description | Keyboard Shortcut |
|------|------|-------------|-------------------|
| **Pan** | ✋ | Click and drag to move | Hold Shift |
| **Wheel Zoom** | 🔍 | Scroll to zoom | Mouse wheel |
| **Box Zoom** | ⬜ | Draw rectangle to zoom | - |
| **Reset** | ↺ | Return to original view | - |
| **Save** | 💾 | Download plot as PNG | - |
| **Hover** | ℹ️ | Show data on mouse over | - |

## Real Data Visualizations with GDP Dataset

### 3.1. Loading and Preparing Data

```yaml
f_type: "codex_"
height_in_px: 250
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, ColumnDataSource
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Category20_20
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load GDP data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities (regions, income groups)
    non_country_entities = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(non_country_entities)]
    
    # Get latest year data for top economies
    latest_year = df_countries['Year'].max()
    df_latest = df_countries[df_countries['Year'] == latest_year]
    
    print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")
    print(f"Year range: {df_countries['Year'].min()} - {df_countries['Year'].max()}")
    print(f"Latest year available: {latest_year}")
```

### 3.2. Interactive Time Series - GDP Evolution

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, Legend
    from bokeh.palettes import Category10
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Select major economies for comparison
    countries = ['United States', 'China', 'Japan', 'Germany', 'India', 'United Kingdom']
    df_selected = df[df['Country Name'].isin(countries)]
    
    # Create figure
    p = figure(
        title="GDP Growth of Major Economies (Interactive)",
        x_axis_label='Year',
        y_axis_label='GDP (Trillion USD)',
        width=800,
        height=450,
        tools="pan,wheel_zoom,box_zoom,reset,save,hover",
        background_fill_color='#fafafa'
    )
    
    # Plot each country with different color
    colors = Category10[6]
    legend_items = []
    
    for i, country in enumerate(countries):
        country_data = df_selected[df_selected['Country Name'] == country].sort_values('Year')
        
        # Convert to trillions
        gdp_trillion = country_data['Value'].values / 1e12
        years = country_data['Year'].values
        
        # Add line with markers
        line = p.line(years, gdp_trillion, line_width=2.5, color=colors[i], alpha=0.8)
        circle = p.circle(years[::5], gdp_trillion[::5], size=6, color=colors[i], alpha=0.8)
        
        # Store for legend
        legend_items.append((country, [line, circle]))
    
    # Create custom legend
    legend = Legend(items=legend_items, location="top_left")
    p.add_layout(legend, 'right')
    p.legend.click_policy = "hide"
    
    # Configure hover tool
    p.hover.tooltips = [
        ("Year", "$x{0}"),
        ("GDP", "$y{0.00} Trillion USD")
    ]
    p.hover.mode = 'vline'
    
    # Styling
    p.title.text_font_size = "14pt"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_alpha = 0.5
    
    curdoc().add_root(p)
    
    print("📊 Interactive time series created!")
    print("💡 Hover to see values, click legend to toggle countries")
```

## Advanced Interactive Features

### 4.1. Scatter Plot with Size and Color Mapping

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, ColorBar, LinearColorMapper
    from bokeh.transform import transform
    from bokeh.palettes import Viridis256
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load and prepare data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities
    non_country_entities = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP',
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT',
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC',
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST',
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(non_country_entities)]
    
    # Calculate growth rates for 2010-2020 period
    df_2010 = df_countries[df_countries['Year'] == 2010][['Country Name', 'Value']]
    df_2020 = df_countries[df_countries['Year'] == 2020][['Country Name', 'Value']]
    
    # Merge and calculate growth
    df_growth = pd.merge(df_2010, df_2020, on='Country Name', suffixes=('_2010', '_2020'))
    df_growth = df_growth[df_growth['Value_2010'] > 0]  # Remove countries with no 2010 data
    df_growth['Growth_Rate'] = ((df_growth['Value_2020'] - df_growth['Value_2010']) / df_growth['Value_2010']) * 100
    df_growth['GDP_2020_Trillion'] = df_growth['Value_2020'] / 1e12
    
    # Filter to significant economies (GDP > 100 billion in 2020)
    df_plot = df_growth[df_growth['Value_2020'] > 1e11].copy()
    
    # Calculate bubble sizes (normalized)
    df_plot['Size'] = 10 + (df_plot['Value_2020'] / df_plot['Value_2020'].max()) * 40
    
    # Create figure
    p = figure(
        title="GDP Growth Rate vs Size (2010-2020)",
        x_axis_label='GDP 2020 (Trillion USD, log scale)',
        y_axis_label='Growth Rate 2010-2020 (%)',
        width=800,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save,hover,tap",
        x_axis_type="log"
    )
    
    # Create color mapper for growth rates
    color_mapper = LinearColorMapper(
        palette=Viridis256,
        low=df_plot['Growth_Rate'].min(),
        high=df_plot['Growth_Rate'].max()
    )
    
    # Add scatter plot
    scatter = p.scatter(
        x='GDP_2020_Trillion',
        y='Growth_Rate',
        size='Size',
        source=df_plot,
        fill_color=transform('Growth_Rate', color_mapper),
        fill_alpha=0.6,
        line_color="navy",
        line_alpha=0.3
    )
    
    # Add color bar
    color_bar = ColorBar(
        color_mapper=color_mapper,
        width=8,
        location=(0,0),
        title="Growth %"
    )
    p.add_layout(color_bar, 'right')
    
    # Configure hover tool
    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Country", "@{Country Name}"),
        ("GDP 2020", "@GDP_2020_Trillion{0.00} Trillion USD"),
        ("Growth Rate", "@Growth_Rate{0.0}%"),
        ("2010 GDP", "@Value_2010{0.00} Billion USD"),
    ]
    
    # Add reference lines
    p.line([df_plot['GDP_2020_Trillion'].min(), df_plot['GDP_2020_Trillion'].max()], 
           [0, 0], line_dash="dashed", line_color="gray", alpha=0.5)
    
    # Styling
    p.title.text_font_size = "14pt"
    p.background_fill_color = "#f5f5f5"
    p.grid.grid_line_alpha = 0.3
    
    curdoc().add_root(p)
    
    print("🎨 Bubble chart created with color and size mapping!")
    print("📍 Size = GDP magnitude, Color = Growth rate")
    print("🔍 Hover for details, use log scale for better distribution")
```

### 4.2. Interactive Bar Chart with Sorting

```yaml
f_type: "codex_"
height_in_px: 450
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, ColumnDataSource
    from bokeh.transform import factor_cmap
    from bokeh.palettes import Spectral11
    import pandas as pd
    from pyodide.http import open_url
    
    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities (regions, income groups)
    non_country_entities  = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df = df[~df['Country Code'].isin(non_country_entities)]

    # Get top 15 economies in 2020
    df_2020 = df[df['Year'] == 2020].copy()
    df_2020['GDP_Trillion'] = df_2020['Value'] / 1e12
    top_15 = df_2020.nlargest(15, 'GDP_Trillion')
    
    # Sort by GDP for better visualization
    top_15 = top_15.sort_values('GDP_Trillion', ascending=True)
    
    # Create data source
    source = ColumnDataSource(data=dict(
        countries=top_15['Country Name'].tolist(),
        gdp=top_15['GDP_Trillion'].tolist(),
        gdp_formatted=[f"${g:.2f}T" for g in top_15['GDP_Trillion']]
    ))
    
    # Create figure
    p = figure(
        y_range=top_15['Country Name'].tolist(),
        title="Top 15 Economies by GDP (2020)",
        width=700,
        height=450,
        toolbar_location="above",
        tools="pan,wheel_zoom,reset,save,hover"
    )
    
    # Add horizontal bars with color mapping
    bars = p.hbar(
        y='countries',
        right='gdp',
        height=0.7,
        source=source,
        fill_color=factor_cmap('countries', palette=Spectral11*2, factors=top_15['Country Name'].tolist()),
        fill_alpha=0.8,
        line_color="white",
        line_width=2
    )
    
    # Configure hover tool
    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Country", "@countries"),
        ("GDP", "@gdp_formatted")
    ]
    hover.mode = 'hline'
    
    # Add value labels at the end of bars
    from bokeh.models import Label
    for i, (country, gdp) in enumerate(zip(top_15['Country Name'], top_15['GDP_Trillion'])):
        label = Label(
            x=gdp, y=i,
            text=f'${gdp:.1f}T',
            text_font_size='9pt',
            x_offset=5
        )
        p.add_layout(label)
    
    # Styling
    p.xaxis.axis_label = "GDP (Trillion USD)"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_color = None
    p.title.text_font_size = "14pt"
    
    curdoc().add_root(p)
    
    print("📊 Horizontal bar chart created!")
    print("🌍 Top economies ranked by GDP")
```

## Combining Multiple Plots

### 5.1. Dashboard Layout with Linked Plots


The data below is randomly generated.
{: .alert .alert-info .alert-soft}

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.layouts import column, row
    from bokeh.models import HoverTool, Range1d
    import numpy as np
    import pandas as pd
    
    # Generate synthetic economic data
    np.random.seed(42)
    months = pd.date_range('2023-01', periods=12, freq='ME')
    
    # Economic indicators
    gdp_growth = np.cumsum(np.random.randn(12) * 0.5 + 0.3)
    inflation = 2 + np.random.randn(12) * 0.5
    unemployment = 5 + np.cumsum(np.random.randn(12) * 0.2)
    
    # Create shared x-range for linked panning/zooming
    shared_x_range = Range1d(start=months[0], end=months[-1])
    
    # Plot 1: GDP Growth
    p1 = figure(
        width=700, height=200,
        title="GDP Growth (Cumulative %)",
        x_axis_type='datetime',
        x_range=shared_x_range,
        tools="pan,wheel_zoom,reset"
    )
    p1.line(months, gdp_growth, line_width=3, color='green', alpha=0.8)
    p1.circle(months, gdp_growth, size=8, color='green', alpha=0.6)
    p1.add_tools(HoverTool(tooltips=[("Date", "$x{%F}"), ("Growth", "$y{0.0}%")],
                           formatters={"$x": "datetime"}))
    
    # Plot 2: Inflation Rate
    p2 = figure(
        width=700, height=200,
        title="Inflation Rate (%)",
        x_axis_type='datetime',
        x_range=shared_x_range,
        tools="pan,wheel_zoom,reset"
    )
    p2.vbar(x=months, top=inflation, width=20*24*60*60*1000, color='orange', alpha=0.7)
    p2.line([months[0], months[-1]], [2, 2], line_dash='dashed', 
            line_color='red', line_width=2, legend_label='Target')
    p2.add_tools(HoverTool(tooltips=[("Date", "$x{%F}"), ("Inflation", "@top{0.00}%")],
                           formatters={"$x": "datetime"}))
    
    # Plot 3: Unemployment Rate
    p3 = figure(
        width=700, height=200,
        title="Unemployment Rate (%)",
        x_axis_type='datetime',
        x_range=shared_x_range,
        tools="pan,wheel_zoom,reset"
    )
    p3.line(months, unemployment, line_width=2, color='red', alpha=0.8)
    p3.patch(list(months) + list(months[::-1]), 
             list(unemployment) + [0]*12,
             color='red', alpha=0.2)
    p3.add_tools(HoverTool(tooltips=[("Date", "$x{%F}"), ("Rate", "$y{0.00}%")],
                           formatters={"$x": "datetime"}))
    
    # Style all plots
    for p in [p1, p2, p3]:
        p.xgrid.grid_line_alpha = 0.3
        p.ygrid.grid_line_alpha = 0.3
        p.title.text_font_size = "11pt"
    
    # Only show x-axis labels on bottom plot
    p1.xaxis.visible = False
    p2.xaxis.visible = False
    
    # Combine plots in a column layout
    layout = column(p1, p2, p3)
    
    curdoc().add_root(layout)
    
    print("📊 Dashboard created with 3 linked plots!")
    print("🔗 Pan or zoom in any plot - others follow!")
    print("📈 Economic indicators for 2023")
```

### 5.2. Mathematical Functions Explorer

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, Slider, CheckboxGroup
    from bokeh.layouts import column, row
    import numpy as np
    
    # Create figure for mathematical functions
    p = figure(
        title="Interactive Mathematical Functions Explorer",
        width=800,
        height=400,
        tools="pan,wheel_zoom,box_zoom,reset,save",
        x_range=(-10, 10),
        y_range=(-2, 2)
    )
    
    # Generate x values
    x = np.linspace(-10, 10, 500)
    
    # Define mathematical functions
    functions = {
        'Sine': np.sin(x),
        'Cosine': np.cos(x),
        'Tangent': np.tanh(x),  # Using tanh instead of tan for better visualization
        'Exponential': np.exp(-x**2/10),  # Gaussian
        'Logarithmic': np.log(np.abs(x) + 1) * np.sign(x) / 3,  # Modified log
        'Polynomial': x**3 / 100 - x / 5  # Cubic polynomial
    }
    
    # Colors for each function
    colors = ['navy', 'red', 'green', 'orange', 'purple', 'brown']
    
    # Plot all functions
    lines = {}
    for i, (name, y_values) in enumerate(functions.items()):
        line = p.line(x, y_values, line_width=2, color=colors[i], 
                     alpha=0.8, legend_label=name)
        lines[name] = line
    
    # Add hover tool
    hover = HoverTool(tooltips=[("x", "$x{0.00}"), ("y", "$y{0.00}")])
    p.add_tools(hover)
    
    # Configure legend
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.8
    
    # Grid styling
    p.xgrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_alpha = 0.3
    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "f(x)"
    
    # Add reference lines
    p.line([-10, 10], [0, 0], line_dash='dashed', line_color='gray', alpha=0.5)
    p.line([0, 0], [-2, 2], line_dash='dashed', line_color='gray', alpha=0.5)
    
    curdoc().add_root(p)
    
    print("🧮 Mathematical functions explorer created!")
    print("📐 Functions: Sine, Cosine, Tanh, Gaussian, Log, Polynomial")
    print("👆 Click legend items to hide/show functions")
```

## Interactive Widgets and Controls


There may be problems with the update of the plot when using the widgets in the browser. Use the `.py` files available in the Bokeh server apps folder (see [Practical work with `bokeh` server applications](session_3_b.md)).
{: .alert .alert-error .alert-soft}

<br>

### 6.1. Top 15 Economies Comparison (2019 Ranking)

```yaml
f_type: "codex_"
height_in_px: 500
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import HoverTool, CheckboxGroup
    from bokeh.layouts import column, row
    from bokeh.palettes import Category20
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load GDP data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities
    non_country_entities = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP',
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT',
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC',
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST',
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(non_country_entities)]
    
    # Get top 15 economies based on 2019 GDP
    df_2019 = df_countries[df_countries['Year'] == 2019]
    top_15_countries = df_2019.nlargest(15, 'Value')['Country Name'].tolist()
    
    print("Top 15 economies in 2019:")
    for i, country in enumerate(top_15_countries, 1):
        gdp_value = df_2019[df_2019['Country Name'] == country]['Value'].values[0] / 1e12
        print(f"{i}. {country}: ${gdp_value:.2f}T")
    
    # Create main figure
    p = figure(
        title="GDP Evolution - Top 15 Economies (2019 Ranking) - Click legend to toggle",
        width=900,
        height=450,
        x_axis_label='Year',
        y_axis_label='GDP (Trillion USD)',
        tools="pan,wheel_zoom,box_zoom,reset,save,hover",
        background_fill_color='#fafafa'
    )
    
    # Use Category20 for more colors (we have 15 countries)
    colors = Category20[20]
    
    # Plot data for each country - only show top 10 to keep it readable
    countries_to_plot = top_15_countries[:10]  # Top 10 for clarity
    
    for i, country in enumerate(countries_to_plot):
        country_data = df_countries[df_countries['Country Name'] == country].sort_values('Year')
        # Filter to years with data
        country_data = country_data[country_data['Year'] >= 2000]  # Focus on recent decades
        gdp_trillion = country_data['Value'].values / 1e12
        years = country_data['Year'].values
        
        # Add line with markers
        line = p.line(years, gdp_trillion, line_width=2.5, 
                     color=colors[i], alpha=0.8, legend_label=f"{i+1}. {country}")
        circle = p.circle(years[::5], gdp_trillion[::5], size=6, 
                         color=colors[i], alpha=0.6, legend_label=f"{i+1}. {country}")
    
    # Configure legend - make it interactive
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"  # Click to hide/show lines
    p.legend.label_text_font_size = "11pt"
    p.legend.background_fill_alpha = 0.8
    
    # Configure hover tool
    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Year", "$x{0}"),
        ("GDP", "$y{0.00} Trillion USD")
    ]
    hover.mode = 'vline'
    
    # Add annotations for key events
    from bokeh.models import Label
    
    # 2008 Financial Crisis annotation
    crisis_label = Label(x=2008, y=15, text='Financial Crisis',
                        text_font_size='10pt', text_color='red',
                        x_offset=5, y_offset=5)
    p.add_layout(crisis_label)
    p.line([2008, 2008], [0, 14], line_dash='dashed', 
           line_color='red', alpha=0.5, line_width=1)
    
    # 2020 COVID annotation
    covid_label = Label(x=2020, y=22, text='COVID-19',
                       text_font_size='10pt', text_color='darkred',
                       x_offset=5, y_offset=5)
    p.add_layout(covid_label)
    p.line([2020, 2020], [0, 21], line_dash='dashed',
           line_color='darkred', alpha=0.5, line_width=1)
    
    # Styling
    p.title.text_font_size = "14pt"
    p.xgrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_alpha = 0.3
    
    curdoc().add_root(p)
    
    print("\n📊 Top 15 Economies (2019 Ranking) - Showing top 10 for clarity")
    print("💡 Click on legend items to show/hide countries")
    print("🔍 Hover over the plot to see exact values")
    print("📌 Key events marked: 2008 Financial Crisis, 2020 COVID-19")
```

### 6.2. Comparative GDP Growth Analysis

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import ColumnDataSource, HoverTool, Label
    from bokeh.layouts import column
    from bokeh.transform import dodge
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load GDP data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities
    non_country_entities = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP',
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT',
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC',
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST',
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(non_country_entities)]
    
    # Focus on G7 countries for this example
    g7_countries = ['United States', 'Japan', 'Germany', 'United Kingdom', 
                    'France', 'Italy', 'Canada']
    df_g7 = df_countries[df_countries['Country Name'].isin(g7_countries)]
    
    # Set default year range
    min_year = 2000
    max_year = 2020
    
    # Filter data for the selected range
    df_filtered = df_g7[(df_g7['Year'] >= min_year) & (df_g7['Year'] <= max_year)]
    
    # Calculate average GDP growth for each country in the period
    growth_data = []
    for country in g7_countries:
        country_data = df_filtered[df_filtered['Country Name'] == country].sort_values('Year')
        if len(country_data) > 1:
            start_gdp = country_data.iloc[0]['Value']
            end_gdp = country_data.iloc[-1]['Value']
            years = country_data.iloc[-1]['Year'] - country_data.iloc[0]['Year']
            annual_growth = ((end_gdp / start_gdp) ** (1/years) - 1) * 100 if years > 0 else 0
            avg_gdp = country_data['Value'].mean() / 1e12
            
            growth_data.append({
                'Country': country,
                'Growth': annual_growth,
                'AvgGDP': avg_gdp,
                'StartGDP': start_gdp / 1e12,
                'EndGDP': end_gdp / 1e12
            })
    
    growth_df = pd.DataFrame(growth_data)
    growth_df = growth_df.sort_values('Growth', ascending=True)
    
    # Add color column to dataframe based on growth rate
    growth_df['color'] = ['#d32f2f' if g < 1 else '#ff9800' if g < 2 else '#4caf50' 
                          for g in growth_df['Growth']]
    
    # Create main plot - Bar chart of average annual growth
    p1 = figure(
        y_range=growth_df['Country'].tolist(),
        title=f"Average Annual GDP Growth Rate ({min_year}-{max_year})",
        width=800,
        height=350,
        toolbar_location="above",
        tools="hover,save"
    )
    
    # Create bars using ColumnDataSource
    from bokeh.models import ColumnDataSource
    source = ColumnDataSource(growth_df)
    
    bars = p1.hbar(
        y='Country',
        right='Growth',
        height=0.7,
        source=source,
        color='color',
        alpha=0.8,
        line_color="white",
        line_width=2
    )
    
    # Add value labels
    for i, row in growth_df.iterrows():
        p1.text(row['Growth'] + 0.05, row['Country'], f"{row['Growth']:.2f}%",
               text_align='left', text_baseline='middle', text_font_size='10pt')
    
    # Configure hover
    hover1 = p1.select_one(HoverTool)
    hover1.tooltips = [
        ("Country", "@Country"),
        ("Avg Annual Growth", "@Growth{0.00}%"),
        ("Avg GDP", "@AvgGDP{0.00} Trillion USD"),
        ("Start GDP", "@StartGDP{0.00}T"),
        ("End GDP", "@EndGDP{0.00}T")
    ]
    
    # Styling
    p1.xaxis.axis_label = "Average Annual Growth Rate (%)"
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    
    # Create secondary plot - GDP evolution over selected period
    p2 = figure(
        title=f"GDP Evolution in Selected Period",
        width=800,
        height=200,
        x_axis_label='Year',
        y_axis_label='GDP (Trillion USD)',
        tools="pan,wheel_zoom,reset"
    )
    
    # Plot lines for each country
    from bokeh.palettes import Dark2_7
    for i, country in enumerate(g7_countries):
        country_data = df_filtered[df_filtered['Country Name'] == country].sort_values('Year')
        p2.line(country_data['Year'], country_data['Value']/1e12, 
               line_width=2, color=Dark2_7[i], alpha=0.7, legend_label=country)
    
    p2.legend.location = "top_left"
    p2.legend.label_text_font_size = "8pt"
    p2.legend.click_policy = "hide"
    
    # Create info panel
    from bokeh.models import Div
    info_text = f"""
    <div style="padding: 10px; background: #e3f2fd; border-left: 4px solid #1976d2; margin-bottom: 10px;">
        <strong>📊 GDP Growth Analysis Dashboard</strong><br>
        <b>Period analyzed:</b> {min_year} - {max_year} ({max_year - min_year} years)<br>
        <b>Countries:</b> G7 Major Economies<br>
        <b>Metrics:</b> Average annual growth rate and GDP evolution
    </div>
    """
    info_div = Div(text=info_text, width=800, height=80)
    
    # Add legend info
    legend_text = """
    <div style="padding: 8px; background: #f5f5f5; border-radius: 4px;">
        <b>Growth Rate Colors:</b> 
        <span style="color: #4caf50;">■ >2% (Strong)</span> | 
        <span style="color: #ff9800;">■ 1-2% (Moderate)</span> | 
        <span style="color: #d32f2f;">■ <1% (Weak)</span>
    </div>
    """
    legend_div = Div(text=legend_text, width=800, height=40)
    
    # Combine all elements
    layout = column(info_div, p1, legend_div, p2)
    
    curdoc().add_root(layout)
    
    print("📊 GDP growth analysis dashboard created!")
    print(f"📅 Analyzing period: {min_year}-{max_year}")
    print("🌍 Comparing G7 economies growth rates")
    print("💡 Interactive features: hover for details, click legend to toggle countries")
```

### 6.3. Interactive Year Slider Visualization

```yaml
f_type: "codex_"
height_in_px: 550
inline: |
    from bokeh.plotting import figure, curdoc
    from bokeh.models import Slider, ColumnDataSource, HoverTool
    from bokeh.layouts import column
    from bokeh.palettes import Spectral6
    import pandas as pd
    import numpy as np
    from pyodide.http import open_url
    
    # Load GDP data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))
    
    # Exclude non-country entities
    non_country_entities = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP',
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT',
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC',
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST',
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }
    df_countries = df[~df['Country Code'].isin(non_country_entities)]
    
    # Select year for display (would be controlled by slider in full app)
    selected_year = 2015
    
    # Get top 10 economies for the selected year
    df_year = df_countries[df_countries['Year'] == selected_year]
    top_10 = df_year.nlargest(10, 'Value')
    top_10['GDP_Trillion'] = top_10['Value'] / 1e12
    top_10 = top_10.sort_values('GDP_Trillion', ascending=True)
    
    # Create data source
    source = ColumnDataSource(data=dict(
        countries=top_10['Country Name'].tolist(),
        gdp=top_10['GDP_Trillion'].tolist(),
        gdp_formatted=[f"${g:.2f}T" for g in top_10['GDP_Trillion']]
    ))
    
    # Create figure
    p = figure(
        y_range=top_10['Country Name'].tolist(),
        title=f"Top 10 Economies in {selected_year}",
        width=800,
        height=400,
        toolbar_location="above",
        tools="hover,save"
    )
    
    # Create horizontal bars
    bars = p.hbar(
        y='countries',
        right='gdp',
        height=0.8,
        source=source,
        fill_color='navy',
        fill_alpha=0.7,
        line_color="white",
        line_width=2
    )
    
    # Configure hover
    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Country", "@countries"),
        ("GDP", "@gdp_formatted")
    ]
    
    # Add value labels
    from bokeh.models import Label
    for i, row in top_10.iterrows():
        label = Label(
            x=row['GDP_Trillion'], y=top_10['Country Name'].tolist().index(row['Country Name']),
            text=f"${row['GDP_Trillion']:.1f}T",
            text_font_size='10pt',
            x_offset=5
        )
        p.add_layout(label)
    
    # Styling
    p.xaxis.axis_label = "GDP (Trillion USD)"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.title.text_font_size = "14pt"
    
    # Create slider (demonstration only - in full app would update the plot)
    year_slider = Slider(
        start=2000,
        end=2022,
        value=selected_year,
        step=1,
        title=f"Select Year (Currently showing: {selected_year})"
    )
    
    # Create info panel
    from bokeh.models import Div
    info_text = f"""
    <div style="padding: 10px; background: #fff3cd; border-left: 4px solid #ffc107;">
        <strong>📅 Year Selector Demo</strong><br>
        This demonstrates a Slider widget interface. In a full Bokeh server application,
        moving the slider would dynamically update the bar chart to show the top 10 
        economies for the selected year.<br>
        <em>Currently showing: Year {selected_year}</em>
    </div>
    """
    info_div = Div(text=info_text, width=800, height=80)
    
    # Calculate some statistics for the selected year
    total_gdp = top_10['GDP_Trillion'].sum()
    avg_gdp = top_10['GDP_Trillion'].mean()
    
    stats_text = f"""
    <div style="padding: 10px; background: #e8f4f8; border-radius: 5px;">
        <strong>📊 Statistics for {selected_year}:</strong><br>
        • Total GDP of top 10: ${total_gdp:.1f} Trillion<br>
        • Average GDP: ${avg_gdp:.1f} Trillion<br>
        • Leader: {top_10.iloc[-1]['Country Name']} (${top_10.iloc[-1]['GDP_Trillion']:.1f}T)
    </div>
    """
    stats_div = Div(text=stats_text, width=800, height=80)
    
    # Combine elements
    layout = column(year_slider, info_div, p, stats_div)
    
    curdoc().add_root(layout)
    
    print(f"🎚️ Year slider visualization created for {selected_year}!")
    print("📊 Showing top 10 economies with GDP values")
    print("💡 Slider widget demonstrates UI capability")
    print("📈 In a Bokeh server app, the slider would update the chart dynamically")
```

## Summary and Best Practices

### Key Takeaways

**Bokeh vs Matplotlib Comparison:**

| Feature | Matplotlib | Bokeh |
|---------|------------|-------|
| **Interactivity** | Static by default | Interactive by default |
| **Output** | Images (PNG, SVG) | HTML/JavaScript |
| **Use Case** | Publication figures | Web dashboards |
| **Learning Curve** | Gentler | Steeper initially |
| **Performance** | Good for static | Better for large datasets |

### When to Use Bokeh

✅ **Use Bokeh when you need:**

- Interactive exploration of data
- Web-based visualizations
- Real-time data updates
- Linked plots and dashboards
- Hover tooltips and selection tools

❌ **Consider alternatives when:**

- Creating static publication figures (use Matplotlib)
- Need 3D visualizations (use Plotly)
- Simple quick plots (use Matplotlib)
- Working offline without web output

### Essential Bokeh Patterns

```python
# 1. Always use curdoc() for Pyodide/JupyterLite
from bokeh.plotting import curdoc
curdoc().add_root(plot)

# 2. Configure hover tooltips for better UX
hover = HoverTool(tooltips=[("Label", "@field")])
p.add_tools(hover)

# 3. Enable legend interaction
p.legend.click_policy = "hide"

# 4. Use ColumnDataSource for complex data
from bokeh.models import ColumnDataSource
source = ColumnDataSource(dataframe)
```

### Quick Reference

| Method | Purpose | Example |
|--------|---------|---------|
| `figure()` | Create plot | `p = figure(width=600, height=400)` |
| `p.line()` | Line plot | `p.line(x, y, color='blue')` |
| `p.circle()` | Scatter points | `p.circle(x, y, size=10)` |
| `p.vbar()` | Vertical bars | `p.vbar(x, top=y, width=0.5)` |
| `p.hbar()` | Horizontal bars | `p.hbar(y, right=x, height=0.5)` |
| `column()` | Stack plots vertically | `column(p1, p2, p3)` |
| `row()` | Arrange plots horizontally | `row(p1, p2)` |
| `HoverTool()` | Add hover tooltips | `p.add_tools(HoverTool())` |

**Remember:** Bokeh excels at creating interactive, web-ready visualizations that allow users to explore data dynamically. While it requires more setup than matplotlib for simple plots, it provides unmatched interactivity for data exploration and presentation.
{: .alert .alert-warning .alert-soft}