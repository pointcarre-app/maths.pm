# 4. Visual  Variables



[TOC]
<span class="font-heading">4. Visual (Retinal) Variables <br>For [Graphic Semiology Fundamentals](session_1_a.md) from Session 1</span>
{: .pm-subtitle}



## Notes

- 1️⃣ Session 1: [Graphic Semiology Fundamentals](session_1_a.md) 
  - <span class="font-heading sm:text-lg">4. Visual (Retinal) Variables</span>


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

    # World TOTAL GDP per year 1960+ (sum instead of mean)
    world_gdp = df.groupby('Year')['Value'].sum().reset_index()
    world_gdp = world_gdp[world_gdp['Year'] >= 1960].copy()
    world_gdp['GDP (Trillions)'] = world_gdp['Value'] / 1e12
    world_gdp['Trend'] = world_gdp['GDP (Trillions)'].diff().fillna(0)
    world_gdp['Opacity'] = np.where(world_gdp['Trend'] >= 0, 1.0, 0.3)

    # Latest year
    latest_year = df['Year'].max()
    df_latest = df[df['Year'] == latest_year]

    # Select top 10 and bottom 10 countries by GDP in latest year
    top10 = df_latest.nlargest(10, 'Value')['Country Name'].tolist()
    bottom10 = df_latest.nsmallest(10, 'Value')['Country Name'].tolist()
    selected_countries = top10 + bottom10

    # Filter main dataframe for selected countries from 1960
    df_filtered = df[(df['Country Name'].isin(selected_countries)) & (df['Year'] >= 1960)].copy()
    df_filtered['GDP (Trillions)'] = df_filtered['Value'] / 1e12

    fig, ax = plt.subplots(figsize=(16, 9))

    # Plot world GDP bars with opacity per trend
    for idx, row in world_gdp.iterrows():
        ax.bar(row['Year'], row['GDP (Trillions)'], color='grey', alpha=row['Opacity'], width=0.7,
            label='World Total GDP' if idx == 0 else "")

    # Assign distinct colors for countries
    colors = plt.cm.tab20.colors
    country_colors = {}  # Store color mapping for legend

    # Plot country GDP lines with opacity
    for i, country in enumerate(selected_countries):
        country_data = df_filtered[df_filtered['Country Name'] == country]
        if len(country_data) == 0:
            continue
            
        gdp_vals = country_data['GDP (Trillions)'].values
        years = country_data['Year'].values
        
        # Calculate trend for opacity
        trend = np.diff(gdp_vals, prepend=gdp_vals[0])
        if len(trend) > 0:
            max_trend = np.max(np.abs(trend))
            if max_trend > 0:
                alphas = np.clip(0.5 + (trend / max_trend), 0.5, 1.0)
            else:
                alphas = np.full(len(trend), 0.7)
        else:
            alphas = [0.7]
        
        color = colors[i % len(colors)]
        country_colors[country] = color
        
        # Plot line segments
        for j in range(len(country_data) - 1):
            ax.plot(years[j:j + 2], gdp_vals[j:j + 2], color=color,
                    alpha=(alphas[j] + alphas[j + 1]) / 2, linewidth=2)
        
        # Plot markers
        for j, yr in enumerate(years):
            ax.scatter(yr, gdp_vals[j], color=color, alpha=alphas[j], edgecolor='black',
                    s=40, zorder=5)

    # Create custom legend with correct colors
    legend_elements = []
    # Add world GDP first
    legend_elements.append(plt.Rectangle((0,0),1,1, facecolor='grey', alpha=0.7, label='World Total GDP'))

    # Add countries with their colors
    for country in selected_countries:
        if country in country_colors:
            legend_elements.append(plt.Line2D([0], [0], color=country_colors[country], 
                                            linewidth=2, label=country))

    # Title with multiline describing selection
    title_text = ("GDP Trends 1960 - {}\n"
                "Top 10 and Bottom 10 Countries by GDP in {}\n"
                "With World Total GDP Bars (Opacity Indicates Growth/Decline)").format(latest_year, latest_year)

    ax.set_title(title_text, fontsize=18, weight='bold')
    ax.set_xlabel('Year', fontsize=16)
    ax.set_ylabel('GDP (Trillions USD)', fontsize=16)
    ax.legend(handles=legend_elements, fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xlim(1960, latest_year)
    plt.xticks(rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Make room for legend on right
    plt.show()

```



