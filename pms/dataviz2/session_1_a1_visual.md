# 4. Visual  Variables


<span class="font-heading">4. Visual Variables <br>For [Graphic Semiology Fundamentals](session_1_a.md) from Session 1</span>
{: .pm-subtitle}


[TOC]


## Notes

- 1️⃣ Session 1: [Graphic Semiology Fundamentals](session_1_a.md) 
  - <span class="font-heading sm:text-lg">4. Visual Variables</span>


## 4.1. The Eight Visual Variables

> Bertin identifies eight key visual variables used to encode data in 2D graphics.

| Variable     | Description                          | Example Use                        |
| ------------ | ------------------------------------ | ---------------------------------- |
| Position (**Planar**)     | $X$/$Y$ coordinates                  | Maps, scatter plots                |
| Size    (**Retinal**)     | Magnitude (length, area, volume)     | Bubble charts                      |
| Value    (**Retinal**)    | Lightness/darkness                   | Heatmaps, shading                  |
| Texture  (**Retinal**)    | Pattern density                      | Map hatching                       |
| Color (Hue) (**Retinal**) | Color spectrum distinction           | Categorical maps/charts            |
| Orientation (**Retinal**) | Angle/direction                      | Wind maps, texture direction       |
| Shape     (**Retinal**)   | Icon/form                            | Markers, diagram symbols           |
| Grain      (**Retinal**)  | Fineness or coarseness of texture    | (Often non-standard, overlaps above)|

## 4.2. Properties of Visual Variables

- **Selectivity:** Can similar symbols be rapidly and preattentively recognized?
- **Associativity:** Can variables be grouped and compared without interference from others?
- **Order:** Can the variable sensibly convey progression or ranking?
- **Quantification:** Can the variable indicate measurable differences?

Associativity is crucial for design: some variables interfere with others (disassociativity), making layering complex data less clear.


*Ticktockmaths* collections such [Bad Graphs](https://ticktockmaths.co.uk/badgraphs/). You will notice in some of those examples that those properties can be instrumentalized to influence our perception.
{: .alert .alert-danger .alert-soft}





## 4.3. Illustration of Bertin's Visual Variables

```yaml
f_type: "codex_"
height_in_px: 630
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches as patches
    
    # Create figure with 3x3 grid
    fig, axes = plt.subplots(3, 3, figsize=(9, 9))
    fig.suptitle("Bertin's Visual Variables", fontsize=16, fontweight='bold', y=1.02)
    
    # Random seed for reproducibility
    np.random.seed(42)
    
    # Helper function to clear axis
    def setup_axis(ax, title):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=11, fontweight='bold', pad=5)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
    
    # 1. POSITION - Top left (following table order)
    ax = axes[0, 0]
    setup_axis(ax, 'POSITION')
    # Different positions showing spatial encoding
    positions = [(2, 8), (7, 7), (3, 3), (8, 2), (5, 5), (1, 6), (6, 1), (9, 9)]
    for pos in positions:
        ax.scatter(pos[0], pos[1], s=50, c='black', alpha=0.8)
    
    # 2. SIZE - Top middle
    ax = axes[0, 1]
    setup_axis(ax, 'SIZE')
    # Different sizes at regular positions
    sizes = [20, 50, 100, 200, 400]
    positions_x = [2, 4, 5, 6, 8]
    positions_y = [5, 7, 3, 8, 5]
    for i, size in enumerate(sizes):
        ax.scatter(positions_x[i], positions_y[i], s=size, c='black', alpha=0.8)
    
    # 3. VALUE (Lightness) - Top right (following table order)
    ax = axes[0, 2]
    setup_axis(ax, 'VALUE')
    # Different grayscale values
    values = np.linspace(0.1, 0.9, 8)
    positions = np.random.uniform(2, 8, (8, 2))
    for i, val in enumerate(values):
        ax.scatter(positions[i, 0], positions[i, 1], s=100, c=str(val), alpha=0.9)
    
    # 4. TEXTURE - Middle left (following table order)
    ax = axes[1, 0]
    setup_axis(ax, 'TEXTURE')
    # Four texture examples in squares
    
    # Add squares to contain each texture
    square_positions = [(2.5, 7.5), (7.5, 7.5), (2.5, 2.5), (7.5, 2.5)]
    for sx, sy in square_positions:
        square = patches.Rectangle((sx-1.8, sy-1.8), 3.6, 3.6, 
                                  linewidth=1, edgecolor='gray', 
                                  facecolor='white', alpha=0.3)
        ax.add_patch(square)
    
    # 1. Dots grid (top-left) - keeping the original dot pattern
    for xi in np.linspace(1.2, 3.8, 4):
        for yi in np.linspace(6.2, 8.8, 4):
            ax.scatter(xi, yi, s=8, c='black', alpha=0.8)
    
    # 2. Fine grid lines (top-right) - very fine line grid
    # Vertical lines
    for x in np.linspace(6.2, 8.8, 8):
        ax.plot([x, x], [6.2, 8.8], 'k-', linewidth=0.3, alpha=0.6)
    # Horizontal lines
    for y in np.linspace(6.2, 8.8, 8):
        ax.plot([6.2, 8.8], [y, y], 'k-', linewidth=0.3, alpha=0.6)
    
    # 3. Hollow circles (bottom-left) - bigger circles, non-filled
    for i in range(3):
        for j in range(3):
            circle = patches.Circle((1.5 + i * 0.8, 1.5 + j * 0.8), 0.25, 
                                   facecolor='none', edgecolor='black', 
                                   linewidth=1.2, alpha=0.8)
            ax.add_patch(circle)
    
    # 4. Heavy grid lines (bottom-right) - perfect grid with thick lines
    # Vertical lines
    for x in np.linspace(6.2, 8.8, 5):
        ax.plot([x, x], [1.2, 3.8], 'k-', linewidth=2.5, alpha=0.8)
    # Horizontal lines
    for y in np.linspace(1.2, 3.8, 5):
        ax.plot([6.2, 8.8], [y, y], 'k-', linewidth=2.5, alpha=0.8)
    
    # 5. COLOR (HUE) - Middle center (following table order)
    ax = axes[1, 1]
    setup_axis(ax, 'COLOR (HUE)')
    # Different colors
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
    positions = np.random.uniform(2, 8, (len(colors), 2))
    for i, color in enumerate(colors):
        ax.scatter(positions[i, 0], positions[i, 1], s=100, c=color, alpha=0.8)
    
    # 6. ORIENTATION - Middle right
    ax = axes[1, 2]
    setup_axis(ax, 'ORIENTATION')
    # Lines at different angles
    angles = [0, 30, 45, 60, 90, 120, 135, 150]
    center_points = np.random.uniform(2, 8, (len(angles), 2))
    for i, angle in enumerate(angles):
        x, y = center_points[i]
        dx = 0.7 * np.cos(np.radians(angle))
        dy = 0.7 * np.sin(np.radians(angle))
        ax.plot([x - dx, x + dx], [y - dy, y + dy], 'k-', linewidth=2, alpha=0.8)
    
    # 7. SHAPE - Bottom left (following table order)
    ax = axes[2, 0]
    setup_axis(ax, 'SHAPE')
    # Different shapes
    shapes = ['o', 's', '^', 'D', 'v', 'p', '*']
    x_positions = np.linspace(2, 8, len(shapes))
    y_positions = np.random.uniform(3, 7, len(shapes))
    for i, (x, y, shape) in enumerate(zip(x_positions, y_positions, shapes)):
        ax.scatter(x, y, s=100, marker=shape, c='black', alpha=0.8)
    
    # 8. GRAIN - Bottom middle (following table order)
    ax = axes[2, 1]
    setup_axis(ax, 'GRAIN')
    # Three clusters with density gradients (epicenter-based opacity)
    
    # Cluster centers
    clusters = [(2.5, 7), (7, 7), (5, 3)]
    
    for cluster_center in clusters:
        xc, yc = cluster_center
        # Generate many points around each center
        n_points = 50
        
        # Generate points with gaussian distribution
        np.random.seed(42 + int(xc * 10))  # Different seed for each cluster
        points_x = np.random.normal(xc, 0.8, n_points)
        points_y = np.random.normal(yc, 0.8, n_points)
        
        # Calculate distance from center for opacity
        for px, py in zip(points_x, points_y):
            # Keep points within bounds
            if 0 < px < 10 and 0 < py < 10:
                distance = np.sqrt((px - xc)**2 + (py - yc)**2)
                # Opacity decreases with distance from epicenter
                opacity = max(0.1, 1.0 - (distance / 2.5))
                ax.scatter(px, py, s=3, c='black', alpha=opacity)
    
    # 9. VISUAL PROPERTIES - Bottom right with nice styling
    ax = axes[2, 2]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('VISUAL PROPERTIES', fontsize=11, fontweight='bold', pad=5)
    
    # Add a light green background
    rect = patches.Rectangle((0, 0), 10, 10, linewidth=1, 
                            edgecolor='darkgreen', facecolor='#90EE90', alpha=0.3)
    ax.add_patch(rect)
    
    # Add prettier text with better styling
    ax.text(5, 8.5, '✓ Selective', ha='center', fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(5, 7.3, '✓ Associative', ha='center', fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(5, 6.1, '✓ Ordered', ha='center', fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(5, 4.9, '✓ Quantitative', ha='center', fontsize=11, fontweight='bold', color='darkgreen')
    
    # Add a divider line
    ax.plot([2, 8], [3.8, 3.8], 'darkgreen', linewidth=1, alpha=0.5)
    
    # Add descriptive text
    ax.text(5, 2.8, 'Visual variables', ha='center', fontsize=10, style='italic', color='darkgreen')
    ax.text(5, 1.8, 'encode data', ha='center', fontsize=10, style='italic', color='darkgreen')
    ax.text(5, 0.8, 'effectively', ha='center', fontsize=10, style='italic', color='darkgreen')
    
    plt.tight_layout()
    plt.show()
```



## 4.4. 💾 Datasets used in the following examples


We'll use some panel data: gdp (nominal) per year and per country. The dataset and its documentation are available [here](https://github.com/datasets/gdp).



## 4.5. Interactive Example with GDP Data



About the graph below: This interactive visualization demonstrates Jacques Bertin's fundamental visual variables using real GDP data. Each subplot shows how the same data can be encoded differently to communicate information.
{: .alert .alert-info .alert-soft}

The visualization below explores **Bertin's six primary visual variables** through practical examples:

1. **POSITION** - The most fundamental variable, using X and Y coordinates to place data points in space. This is how we create traditional scatter plots and line charts.

2. **SIZE** - Varying the area or volume of graphical elements to represent quantitative differences. Larger circles represent larger GDP values, making comparisons intuitive.

3. **VALUE** (Lightness/Darkness) - Using grayscale intensity from light to dark to show magnitude. Darker bars represent higher GDP values, creating a natural ordering.

4. **COLOR (Hue)** - Different colors to categorize or classify data. Here, red represents the highest GDPs, transitioning through orange, yellow, green, to blue for the lowest.

5. **ORIENTATION** - The angle or direction of graphical elements. The GDP evolution curves for European countries show different line orientations (solid, dashed, dotted) to distinguish between countries while showing trends.

6. **SHAPE** - Different symbols to represent categorical distinctions. Each continent gets its own marker shape, making it easy to identify geographic patterns in the data.


```yaml
f_type: "codex_"
height_in_px: 1000
inline: |
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from pyodide.http import open_url

    # Load data
    url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    df = pd.read_csv(open_url(url))

    # Countries/territories to exclude (groups, regions, income classifications)
    exclude_codes = {
        'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
        'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
        'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
        'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
        'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
    }

    # Filter out non-countries and get latest year data
    if 'Country Code' in df.columns:
        df_countries = df[~df['Country Code'].isin(exclude_codes)]
    elif 'country_code' in df.columns:
        df_countries = df[~df['country_code'].isin(exclude_codes)]
    else:
        df_countries = df.copy()

    latest_year = df_countries['Year'].max()
    df_latest = df_countries[df_countries['Year'] == latest_year].copy()

    # Select diverse mix of countries (not just extremes)
    df_sorted = df_latest.sort_values('Value', ascending=False).reset_index(drop=True)

    # Manually pick interesting diverse countries
    interesting_countries = [
        'United States', 'China', 'Germany', 'Japan',  # Large economies
        'Brazil', 'India', 'Mexico', 'South Korea',    # Emerging markets
        'Switzerland', 'Netherlands', 'Sweden', 'Norway',  # Rich smaller countries
        'Nigeria', 'Bangladesh', 'Vietnam', 'Kenya'     # Developing economies
    ]

    # Find these countries in the data, fallback to top/diverse mix if not found
    selected_data = []
    for country in interesting_countries:
        country_data = df_sorted[df_sorted['Country Name'].str.contains(country, case=False, na=False)]
        if not country_data.empty:
            selected_data.append(country_data.iloc[0])

    # If we don't have enough, fill with diverse selection
    if len(selected_data) < 12:
        remaining_needed = 12 - len(selected_data)
        used_countries = [c['Country Name'] for c in selected_data]
        
        # Take every 15th country from sorted list (spread selection)
        step = max(1, len(df_sorted) // remaining_needed)
        for i in range(0, len(df_sorted), step):
            if len(selected_data) >= 12:
                break
            candidate = df_sorted.iloc[i]
            if candidate['Country Name'] not in used_countries:
                selected_data.append(candidate)

    selected_data = pd.DataFrame(selected_data).reset_index(drop=True)

    # Convert to trillions for readability
    selected_data['GDP_Trillions'] = selected_data['Value'] / 1e12

    # Create figure with subplots to demonstrate visual variables (2 cols, 3 rows)
    fig = plt.figure(figsize=(20, 24))

    # 1. POSITION (X,Y coordinates) - Traditional scatter plot
    ax1 = plt.subplot(3, 2, 1)
    x_pos = range(len(selected_data))
    y_pos = selected_data['GDP_Trillions']
    ax1.scatter(x_pos, y_pos, s=150, color='steelblue', alpha=0.7)
    ax1.set_title('1. POSITION\n(X,Y coordinates)', fontweight='bold', fontsize=18)
    ax1.set_xlabel('Country Index', fontsize=14)
    ax1.set_ylabel('GDP (Trillions USD)', fontsize=14)
    ax1.tick_params(axis='both', labelsize=12)
    for i, country in enumerate(selected_data['Country Name']):
        ax1.annotate(country[:3], (i, y_pos.iloc[i]), xytext=(5, 5), 
                    textcoords='offset points', fontsize=11, rotation=45)

    # 2. SIZE - Bubble chart
    ax2 = plt.subplot(3, 2, 2)
    # Normalize sizes (min 50, max 800)
    sizes = 50 + (selected_data['GDP_Trillions'] / selected_data['GDP_Trillions'].max()) * 750
    ax2.scatter(range(len(selected_data)), [1]*len(selected_data), s=sizes, 
            color='steelblue', alpha=0.6, edgecolors='navy')
    ax2.set_title('2. SIZE\n(Circle area)', fontweight='bold', fontsize=18)
    ax2.set_xlabel('Country Index', fontsize=14)
    ax2.set_ylim(0.5, 1.5)
    ax2.set_yticks([])
    ax2.tick_params(axis='x', labelsize=12)
    for i, country in enumerate(selected_data['Country Name']):
        ax2.annotate(country[:3], (i, 1), ha='center', va='center', fontsize=11, fontweight='bold')

    # 3. VALUE (Lightness/Darkness)
    ax3 = plt.subplot(3, 2, 3)
    # Create grayscale values based on GDP (darker = higher GDP)
    values = selected_data['GDP_Trillions'] / selected_data['GDP_Trillions'].max()
    colors = [(1-v, 1-v, 1-v) for v in values]  # Grayscale
    bars = ax3.bar(range(len(selected_data)), selected_data['GDP_Trillions'], color=colors, 
                edgecolor='black', linewidth=1)
    ax3.set_title('3. VALUE\n(Lightness/Darkness)', fontweight='bold', fontsize=18)
    ax3.set_xlabel('Country Index', fontsize=14)
    ax3.set_ylabel('GDP (Trillions USD)', fontsize=14)
    ax3.set_xticks(range(len(selected_data)))
    ax3.set_xticklabels([c[:3] for c in selected_data['Country Name']], rotation=45, fontsize=11)
    ax3.tick_params(axis='y', labelsize=12)

    # 4. COLOR (Hue)
    ax4 = plt.subplot(3, 2, 4)
    # Use distinct colors for different GDP ranges
    colors_hue = []
    for gdp in selected_data['GDP_Trillions']:
        if gdp > 10:
            colors_hue.append('red')      # Highest GDP
        elif gdp > 5:
            colors_hue.append('orange')   # High GDP
        elif gdp > 1:
            colors_hue.append('yellow')   # Medium GDP
        elif gdp > 0.1:
            colors_hue.append('green')    # Low GDP
        else:
            colors_hue.append('blue')     # Lowest GDP

    bars = ax4.bar(range(len(selected_data)), selected_data['GDP_Trillions'], 
                color=colors_hue, alpha=0.8, edgecolor='black', linewidth=1)
    ax4.set_title('4. COLOR (Hue)\n(Different colors for ranges)', fontweight='bold', fontsize=18)
    ax4.set_xlabel('Country Index', fontsize=14)
    ax4.set_ylabel('GDP (Trillions USD)', fontsize=14)
    ax4.set_xticks(range(len(selected_data)))
    ax4.set_xticklabels([c[:3] for c in selected_data['Country Name']], rotation=45, fontsize=11)
    ax4.tick_params(axis='y', labelsize=12)

    # 5. ORIENTATION - GDP curves over time for comparable European countries
    ax5 = plt.subplot(3, 2, 5)
    
    # Get historical data for France, Germany, UK, and Italy
    european_countries = ['France', 'Germany', 'United Kingdom', 'Italy']
    line_styles = ['-', '--', '-.', ':']
    line_colors = ['blue', 'red', 'green', 'orange']
    line_widths = [2.5, 2.5, 2.5, 2.5]
    
    for country_name, style, color, lw in zip(european_countries, line_styles, line_colors, line_widths):
        # Filter for this specific country
        country_data = df_countries[df_countries['Country Name'].str.contains(country_name, case=False, na=False)]
        if not country_data.empty:
            # Get the exact country name from the data
            actual_name = country_data['Country Name'].iloc[0]
            country_data = df_countries[df_countries['Country Name'] == actual_name]
            
            # Sort by year and convert to trillions
            country_data = country_data.sort_values('Year')
            gdp_trillions = country_data['Value'] / 1e12
            
            # Plot the curve
            ax5.plot(country_data['Year'], gdp_trillions, linestyle=style, 
                    color=color, linewidth=lw, label=country_name, alpha=0.85)
    
    ax5.set_title('5. ORIENTATION\n(GDP curves/lines with different orientations)', fontweight='bold', fontsize=18)
    ax5.set_xlabel('Year', fontsize=14)
    ax5.set_ylabel('GDP (Trillions USD)', fontsize=14)
    ax5.tick_params(axis='both', labelsize=12)
    ax5.legend(fontsize=12, loc='upper left')
    ax5.grid(True, alpha=0.3)

    # 6. SHAPE
    ax6 = plt.subplot(3, 2, 6)
    # Use different shapes for different continents
    continent_map = {
        'United States': ('North America', '*', 'red'),
        'China': ('Asia', 's', 'gold'),
        'Germany': ('Europe', '^', 'blue'),
        'Japan': ('Asia', 's', 'gold'),
        'Brazil': ('South America', 'p', 'green'),
        'India': ('Asia', 's', 'gold'),
        'Mexico': ('North America', '*', 'red'),
        'South Korea': ('Asia', 's', 'gold'),
        'Switzerland': ('Europe', '^', 'blue'),
        'Netherlands': ('Europe', '^', 'blue'),
        'Sweden': ('Europe', '^', 'blue'),
        'Norway': ('Europe', '^', 'blue'),
        'Nigeria': ('Africa', 'D', 'purple'),
        'Bangladesh': ('Asia', 's', 'gold'),
        'Vietnam': ('Asia', 's', 'gold'),
        'Kenya': ('Africa', 'D', 'purple')
    }
    
    # Plot each point with its continent-specific marker
    for i, (country, gdp) in enumerate(zip(selected_data['Country Name'], selected_data['GDP_Trillions'])):
        # Find continent and marker for this country
        marker = 'o'  # Default
        color = 'gray'  # Default
        continent = 'Unknown'
        
        for pattern, (cont, mark, col) in continent_map.items():
            if pattern.lower() in country.lower():
                continent = cont
                marker = mark
                color = col
                break
        
        ax6.scatter(i, gdp, marker=marker, s=250, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax6.text(i, gdp + gdp*0.15, country[:3], ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax6.set_title('6. SHAPE\n(Different markers by continent)', fontweight='bold', fontsize=18)
    ax6.set_xlabel('Country Index', fontsize=14)
    ax6.set_ylabel('GDP (Trillions USD)', fontsize=14)
    ax6.set_yscale('log')  # Log scale to better show the range
    ax6.tick_params(axis='both', labelsize=12)

    # Add legend for shapes with better spacing
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=14, 
               label='North America', markeredgecolor='black', markeredgewidth=1.5),
        Line2D([0], [0], marker='p', color='w', markerfacecolor='green', markersize=14, 
               label='South America', markeredgecolor='black', markeredgewidth=1.5),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='blue', markersize=14, 
               label='Europe', markeredgecolor='black', markeredgewidth=1.5),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='gold', markersize=14, 
               label='Asia', markeredgecolor='black', markeredgewidth=1.5),
        Line2D([0], [0], marker='D', color='w', markerfacecolor='purple', markersize=14, 
               label='Africa', markeredgecolor='black', markeredgewidth=1.5)
    ]
    ax6.legend(handles=legend_elements, fontsize=12, loc='upper right', 
              framealpha=0.9, handletextpad=1.5, columnspacing=2.0)

    plt.tight_layout(pad=3.0, h_pad=4.0, w_pad=4.0)
    plt.subplots_adjust(top=0.96, bottom=0.02, left=0.05, right=0.95)
    plt.show()

    # Print summary of visual variables demonstrated
    print("\n" + "="*60)
    print("BERTIN'S VISUAL VARIABLES DEMONSTRATED:")
    print("="*60)
    print("1. POSITION: Country data plotted using X,Y coordinates")
    print("2. SIZE: Circle areas proportional to GDP values")
    print("3. VALUE: Grayscale intensity representing GDP magnitude")
    print("4. COLOR (HUE): Different colors for GDP ranges")
    print("5. ORIENTATION: GDP evolution curves for European countries")
    print("6. SHAPE: Different markers representing continents")
    print("\nExcluded: GRAIN and TEXTURE")
    print("="*60)

```




