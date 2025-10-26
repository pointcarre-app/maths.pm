# Visual Vocabulary - Financial Times Guide


A comprehensive guide to choosing the right chart for your data story using the *FT Data Visualization Guide*
{: .pm-subtitle}

This work is an adaptation from the [*FT Data Visualization Guide*](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) from *the Financial Times*. This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
{: .alert .alert-success .alert-soft}



This resource has been made available by [The official portal for European data](https://data.europa.eu/apps/data-visualisation-guide/visual-vocabulary), i.e. [data.europa.eu](https://data.europa.eu).
{: .alert .alert-info .alert-soft}


[TOC]


## The FT Data Visualization Guide


![Visual Vocabulary - FT Data Visualization Guide](files/bokeh_server_apps/visual-vocabulary-ft.png)

- License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- Link to download the image in high resolution: <a href="/pm/dataviz2/files/bokeh_server_apps/visual-vocabulary-ft.png" download>Download link</a><br>


## Deviation
> Emphasize variations (+/-) from a fixed reference point. Often the reference point is zero but it can also be a target or a long-term average. Can also be used to show sentiment (positive/neutral/negative).

### Example FT uses
Trade surplus/deficit, climate change

### Chart Types

#### **Diverging bar**
- A simple standard bar chart that can handle both negative and positive magnitude values

#### **Diverging stacked bar**
- Perfect for presenting survey results which involve sentiment (eg disagree/neutral/agree)

#### **Spine**
- Splits a single value into 2 contrasting components (eg Male/Female)

#### **Surplus/deficit filled line**
- The shaded area of these charts allows a balance to be shown – either against a baseline or between two series

### Matplotlib implementation examples

```yaml
f_type: "codex_"
height_in_px: 1000
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    
    # Create figure with 2x2 subplots for the 4 deviation chart types
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('DEVIATION CHARTS: Trade Surplus/Deficit Examples', fontsize=16, fontweight='bold', y=1.02)
    
    # Generate sample trade data for a fictitious country "Tradeland"
    np.random.seed(42)
    years = np.arange(2015, 2024)
    
    # 1. DIVERGING BAR - Monthly trade balance for 2023
    ax1 = axes[0, 0]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    trade_balance = np.array([2.3, -1.5, 3.1, -0.8, 1.2, -2.1, 0.5, -1.8, 2.7, 1.1, -0.3, 3.5])
    
    colors = ['#2E7D32' if x > 0 else '#C62828' for x in trade_balance]
    bars = ax1.barh(months, trade_balance, color=colors, alpha=0.8)
    
    # Add zero line
    ax1.axvline(x=0, color='black', linewidth=1, alpha=0.5)
    
    # Styling
    ax1.set_xlabel('Trade Balance (Billion USD)', fontsize=11)
    ax1.set_title('1. DIVERGING BAR\nMonthly Trade Balance 2023', fontsize=12, fontweight='bold', pad=10)
    ax1.grid(axis='x', alpha=0.2)
    ax1.set_xlim(-4, 4)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, trade_balance)):
        if val > 0:
            ax1.text(val + 0.1, i, f'+{val:.1f}', va='center', fontsize=9)
        else:
            ax1.text(val - 0.1, i, f'{val:.1f}', va='center', ha='right', fontsize=9)
    
    # 2. DIVERGING STACKED BAR - Trade sentiment survey
    ax2 = axes[0, 1]
    categories = ['Export Policy', 'Import Tariffs', 'Trade Agreements', 'Currency Policy', 'Market Access']
    
    # Survey results (percentages)
    strongly_negative = np.array([-15, -10, -5, -20, -12])
    negative = np.array([-25, -20, -15, -15, -18])
    neutral = np.array([20, 25, 30, 25, 30])
    positive = np.array([25, 30, 35, 20, 25])
    strongly_positive = np.array([15, 15, 15, 10, 15])
    
    # Plot stacked bars
    y_pos = np.arange(len(categories))
    
    # Negative side
    ax2.barh(y_pos, strongly_negative, color='#D32F2F', alpha=0.9, label='Strongly Negative')
    ax2.barh(y_pos, negative, left=strongly_negative, color='#F57C00', alpha=0.8, label='Negative')
    
    # Neutral (centered)
    neutral_left = strongly_negative + negative
    neutral_right = neutral / 2
    ax2.barh(y_pos, neutral_right, left=neutral_left, color='#9E9E9E', alpha=0.6)
    ax2.barh(y_pos, neutral_right, color='#9E9E9E', alpha=0.6, label='Neutral')
    
    # Positive side
    ax2.barh(y_pos, positive, color='#689F38', alpha=0.8, label='Positive')
    ax2.barh(y_pos, strongly_positive, left=positive, color='#388E3C', alpha=0.9, label='Strongly Positive')
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(categories)
    ax2.set_xlabel('Sentiment (%)', fontsize=11)
    ax2.set_title('2. DIVERGING STACKED BAR\nTrade Policy Sentiment Survey', fontsize=12, fontweight='bold', pad=10)
    ax2.axvline(x=0, color='black', linewidth=1.5, alpha=0.7)
    ax2.set_xlim(-50, 50)
    ax2.legend(loc='lower right', fontsize=8, framealpha=0.9)
    ax2.grid(axis='x', alpha=0.2)
    
    # 3. SPINE CHART - Exports vs Imports composition
    ax3 = axes[1, 0]
    
    # Data for spine chart (percentage of total trade)
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
    exports_pct = np.array([52, 48, 55, 51])  # Percentage of total trade
    imports_pct = 100 - exports_pct
    
    x = np.arange(len(quarters))
    width = 0.6
    
    # Fixed center line at 50%
    center_line = 50
    max_deviation = 50  # Maximum height above or below center
    
    # Create spine chart - bars centered at 50% line
    for i, (exp, imp) in enumerate(zip(exports_pct, imports_pct)):
        # Calculate how much each extends from the center
        export_from_center = (exp / 100) * 100  # Height of export portion
        import_from_center = (imp / 100) * 100  # Height of import portion
        
        # Draw import portion (below center line, red)
        ax3.bar(i, import_from_center, width, bottom=center_line - import_from_center, 
               color='#D32F2F', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Draw export portion (above center line, blue)
        ax3.bar(i, export_from_center, width, bottom=center_line,
               color='#1976D2', alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add percentage labels inside bars
        # Export label (in blue portion above center)
        ax3.text(i, center_line + export_from_center/2, f'{exp}%', 
                ha='center', va='center', fontweight='bold', fontsize=9, color='white')
        
        # Import label (in red portion below center)
        ax3.text(i, center_line - import_from_center/2, f'{imp}%', 
                ha='center', va='center', fontweight='bold', fontsize=9, color='white')
    
    # Add horizontal reference line at 50% (balanced trade)
    ax3.axhline(y=center_line, color='black', linewidth=2.5, 
               linestyle='-', alpha=0.9, zorder=5)
    
    # Add text label for the reference line
    ax3.text(len(quarters) - 0.5, center_line, ' Balance\n (50/50)', 
            fontsize=9, va='center', fontweight='bold')
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#1976D2', alpha=0.8, label='Exports'),
                      Patch(facecolor='#D32F2F', alpha=0.8, label='Imports')]
    ax3.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    ax3.set_ylabel('Percentage of Total Trade', fontsize=11)
    ax3.set_title('3. SPINE CHART\nExports vs Imports Share', fontsize=12, fontweight='bold', pad=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(quarters)
    ax3.set_ylim(0, 100)
    ax3.set_yticks([0, 25, 50, 75, 100])
    ax3.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
    ax3.grid(axis='y', alpha=0.2)
    
    # 4. SURPLUS/DEFICIT FILLED LINE
    ax4 = axes[1, 1]
    
    # Generate monthly data for 2 years
    months_extended = pd.date_range('2022-01', '2024-01', freq='M')
    baseline = 0
    
    # Create fluctuating trade balance
    t = np.linspace(0, 4*np.pi, len(months_extended))
    trade_balance_line = 2 * np.sin(t) + 0.5 * np.sin(3*t) + np.random.normal(0, 0.3, len(t))
    
    # Plot the line
    ax4.plot(months_extended, trade_balance_line, color='black', linewidth=1.5, alpha=0.8)
    
    # Fill areas
    ax4.fill_between(months_extended, baseline, trade_balance_line, 
                     where=(trade_balance_line >= baseline), 
                     color='#2E7D32', alpha=0.6, label='Surplus')
    ax4.fill_between(months_extended, baseline, trade_balance_line, 
                     where=(trade_balance_line < baseline), 
                     color='#C62828', alpha=0.6, label='Deficit')
    
    # Add baseline
    ax4.axhline(y=baseline, color='black', linewidth=1, alpha=0.5)
    
    # Styling
    ax4.set_xlabel('Date', fontsize=11)
    ax4.set_ylabel('Trade Balance (Billion USD)', fontsize=11)
    ax4.set_title('4. SURPLUS/DEFICIT FILLED LINE\nMonthly Trade Balance Over Time', fontsize=12, fontweight='bold', pad=10)
    ax4.grid(True, alpha=0.2)
    ax4.legend(loc='upper right', fontsize=10)
    
    # Format x-axis dates
    import matplotlib.dates as mdates
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "="*60)
    print("DEVIATION CHART TYPES DEMONSTRATED:")
    print("="*60)
    print("1. DIVERGING BAR: Shows positive/negative monthly trade balances")
    print("2. DIVERGING STACKED BAR: Displays sentiment survey with neutral center")
    print("3. SPINE CHART: Compares exports vs imports as percentages")
    print("4. SURPLUS/DEFICIT FILLED LINE: Time series with shaded surplus/deficit areas")
    print("\nData: Fictitious country 'Tradeland' trade statistics")
    print("="*60)
```



## Correlation

> Show the relationship between two or more variables. Be mindful that, unless you tell them otherwise, many readers will assume the relationships you show them to be causal (i.e. one causes the other).

### Example FT uses
Inflation & unemployment, income & life expectancy

### Chart Types

#### Scatterplot
- The standard way to show the relationship between two continuous variables, each of which has its own axis

#### Column + line (dual axis)
- A chart which allows you to look at the relationship between two scaled axes. TAKE CARE: this technique is very easy to manipulate to show nothing or anything

#### Connected scatterplot
- Usually used to show how the relationship between 2 variables has changed over time

#### Bubble
- Like a scatterplot, but adds additional detail by sizing the circles according to a third variable

#### XY heatmap
- A good way of showing the patterns between 2 categories of data, less good at showing fine differences in amounts

### Matplotlib implementation examples

For these correlation examples, we use economic data from 2024:

> Data Sources: World Bank, OECD, UN Statistics, Eurostat, Our World in Data.

```python
import pandas as pd

data = [
    {"Country": "France", "Year": 2024, "Inflation": 4.1, "Unemployment": 7.4, "Income": 42800, "LifeExpectancy": 82.4},
    {"Country": "Germany", "Year": 2024, "Inflation": 2.6, "Unemployment": 3.2, "Income": 51800, "LifeExpectancy": 81.1},
    {"Country": "USA", "Year": 2024, "Inflation": 3.2, "Unemployment": 3.8, "Income": 76650, "LifeExpectancy": 79.2},
    {"Country": "Japan", "Year": 2024, "Inflation": 2.8, "Unemployment": 2.7, "Income": 41400, "LifeExpectancy": 84.7},
    {"Country": "Brazil", "Year": 2024, "Inflation": 3.9, "Unemployment": 8.4, "Income": 11653, "LifeExpectancy": 75.6},
    {"Country": "South Africa", "Year": 2024, "Inflation": 6.0, "Unemployment": 32.0, "Income": 7600, "LifeExpectancy": 65.2},
    {"Country": "India", "Year": 2024, "Inflation": 5.5, "Unemployment": 7.1, "Income": 2600, "LifeExpectancy": 70.8},
]

df = pd.DataFrame(data)
```

The original data values are based on open international datasets and aggregate statistics from sources like the World Bank, OECD, United Nations, Eurostat, and compilations by Our World in Data. For robust research or publication, refer directly to these organizations' portals or download raw datasets from their official sites.
{: .alert .alert-warning .alert-soft}

```yaml
f_type: "codex_"
height_in_px: 1200
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    
    # Create figure with subplots for the 5 correlation chart types
    fig = plt.figure(figsize=(15, 12))
    
    # Economic data for 2024
    data = [
        {"Country": "France", "Year": 2024, "Inflation": 4.1, "Unemployment": 7.4, "Income": 42800, "LifeExpectancy": 82.4},
        {"Country": "Germany", "Year": 2024, "Inflation": 2.6, "Unemployment": 3.2, "Income": 51800, "LifeExpectancy": 81.1},
        {"Country": "USA", "Year": 2024, "Inflation": 3.2, "Unemployment": 3.8, "Income": 76650, "LifeExpectancy": 79.2},
        {"Country": "Japan", "Year": 2024, "Inflation": 2.8, "Unemployment": 2.7, "Income": 41400, "LifeExpectancy": 84.7},
        {"Country": "Brazil", "Year": 2024, "Inflation": 3.9, "Unemployment": 8.4, "Income": 11653, "LifeExpectancy": 75.6},
        {"Country": "South Africa", "Year": 2024, "Inflation": 6.0, "Unemployment": 32.0, "Income": 7600, "LifeExpectancy": 65.2},
        {"Country": "India", "Year": 2024, "Inflation": 5.5, "Unemployment": 7.1, "Income": 2600, "LifeExpectancy": 70.8},
    ]
    df = pd.DataFrame(data)
    
    fig.suptitle('CORRELATION CHARTS: Economic Relationships', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. SCATTERPLOT - Income vs Life Expectancy
    ax1 = plt.subplot(2, 3, 1)
    ax1.scatter(df['Income'], df['LifeExpectancy'], s=100, alpha=0.7, color='#1565C0', edgecolors='black', linewidth=1)
    
    # Add country labels
    for idx, row in df.iterrows():
        ax1.annotate(row['Country'][:3], (row['Income'], row['LifeExpectancy']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=9, alpha=0.8)
    
    # Add trend line
    z = np.polyfit(df['Income'], df['LifeExpectancy'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df['Income'].min(), df['Income'].max(), 100)
    ax1.plot(x_trend, p(x_trend), "r--", alpha=0.5, linewidth=2)
    
    ax1.set_xlabel('GDP per Capita (USD)', fontsize=10)
    ax1.set_ylabel('Life Expectancy (years)', fontsize=10)
    ax1.set_title('1. SCATTERPLOT\nIncome vs Life Expectancy', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Calculate and display correlation
    corr = df['Income'].corr(df['LifeExpectancy'])
    ax1.text(0.05, 0.95, f'r = {corr:.2f}', transform=ax1.transAxes, 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 2. COLUMN + LINE (DUAL AXIS) - Unemployment bars with Inflation line
    ax2 = plt.subplot(2, 3, 2)
    
    # Sort by unemployment for better visualization
    df_sorted = df.sort_values('Unemployment')
    x_pos = np.arange(len(df_sorted))
    
    # Bar chart for unemployment
    color1 = '#FF6B35'
    bars = ax2.bar(x_pos, df_sorted['Unemployment'], alpha=0.7, color=color1, label='Unemployment')
    ax2.set_xlabel('Countries', fontsize=10)
    ax2.set_ylabel('Unemployment Rate (%)', fontsize=10, color=color1)
    ax2.tick_params(axis='y', labelcolor=color1)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([c[:3] for c in df_sorted['Country']], rotation=45)
    
    # Create second y-axis for inflation
    ax2_twin = ax2.twinx()
    color2 = '#004E89'
    ax2_twin.plot(x_pos, df_sorted['Inflation'], color=color2, marker='o', 
                 linewidth=2, markersize=8, label='Inflation')
    ax2_twin.set_ylabel('Inflation Rate (%)', fontsize=10, color=color2)
    ax2_twin.tick_params(axis='y', labelcolor=color2)
    
    ax2.set_title('2. COLUMN + LINE (DUAL AXIS)\nUnemployment vs Inflation', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.2, axis='y')
    
    # 3. CONNECTED SCATTERPLOT - Inflation vs Unemployment trajectory
    ax3 = plt.subplot(2, 3, 3)
    
    # Create a logical order for connection (by unemployment rate)
    df_connected = df.sort_values('Unemployment')
    
    # Plot points
    ax3.scatter(df_connected['Inflation'], df_connected['Unemployment'], 
               s=150, alpha=0.7, color='#2E7D32', edgecolors='black', linewidth=1, zorder=3)
    
    # Connect points with lines
    ax3.plot(df_connected['Inflation'], df_connected['Unemployment'], 
            'k-', alpha=0.3, linewidth=1, zorder=1)
    
    # Add arrows to show direction
    for i in range(len(df_connected) - 1):
        ax3.annotate('', xy=(df_connected.iloc[i+1]['Inflation'], df_connected.iloc[i+1]['Unemployment']),
                    xytext=(df_connected.iloc[i]['Inflation'], df_connected.iloc[i]['Unemployment']),
                    arrowprops=dict(arrowstyle='->', alpha=0.3, lw=0.5))
    
    # Label start and end
    ax3.annotate('Start', (df_connected.iloc[0]['Inflation'], df_connected.iloc[0]['Unemployment']),
                xytext=(-10, 10), textcoords='offset points', fontsize=9, fontweight='bold')
    ax3.annotate('End', (df_connected.iloc[-1]['Inflation'], df_connected.iloc[-1]['Unemployment']),
                xytext=(10, -10), textcoords='offset points', fontsize=9, fontweight='bold')
    
    ax3.set_xlabel('Inflation Rate (%)', fontsize=10)
    ax3.set_ylabel('Unemployment Rate (%)', fontsize=10)
    ax3.set_title('3. CONNECTED SCATTERPLOT\nInflation-Unemployment Path', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # 4. BUBBLE CHART - Income vs Life Expectancy with Unemployment as size
    ax4 = plt.subplot(2, 3, 4)
    
    # Normalize unemployment for bubble sizes (50 to 1000)
    sizes = 50 + (df['Unemployment'] / df['Unemployment'].max()) * 950
    
    # Create bubble chart with color gradient for inflation
    scatter = ax4.scatter(df['Income'], df['LifeExpectancy'], s=sizes, 
                         c=df['Inflation'], cmap='coolwarm', alpha=0.6, 
                         edgecolors='black', linewidth=1)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Inflation Rate (%)', fontsize=9)
    
    # Add country labels
    for idx, row in df.iterrows():
        ax4.annotate(row['Country'][:3], (row['Income'], row['LifeExpectancy']), 
                    ha='center', va='center', fontsize=8, fontweight='bold')
    
    ax4.set_xlabel('GDP per Capita (USD)', fontsize=10)
    ax4.set_ylabel('Life Expectancy (years)', fontsize=10)
    ax4.set_title('4. BUBBLE CHART\n(Size = Unemployment, Color = Inflation)', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. XY HEATMAP - Correlation matrix
    ax5 = plt.subplot(2, 3, 5)
    
    # Select numeric columns for correlation
    numeric_cols = ['Inflation', 'Unemployment', 'Income', 'LifeExpectancy']
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    im = ax5.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    
    # Set ticks and labels
    ax5.set_xticks(np.arange(len(numeric_cols)))
    ax5.set_yticks(np.arange(len(numeric_cols)))
    ax5.set_xticklabels(['Inflation', 'Unemploy.', 'Income', 'Life Exp.'], rotation=45, ha='right')
    ax5.set_yticklabels(['Inflation', 'Unemploy.', 'Income', 'Life Exp.'])
    
    # Add correlation values
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            text = ax5.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                           ha='center', va='center', color='black' if abs(corr_matrix.iloc[i, j]) < 0.5 else 'white',
                           fontweight='bold')
    
    ax5.set_title('5. XY HEATMAP\nCorrelation Matrix', fontsize=11, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax5)
    cbar.set_label('Correlation', fontsize=9)    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "="*60)
    print("CORRELATION CHART TYPES DEMONSTRATED:")
    print("="*60)
    print("1. SCATTERPLOT: Classic visualization of Income vs Life Expectancy")
    print("2. COLUMN + LINE: Dual-axis showing Unemployment bars with Inflation line")
    print("3. CONNECTED SCATTERPLOT: Path showing relationship progression")
    print("4. BUBBLE CHART: Multi-dimensional data (4 variables in one chart)")
    print("5. XY HEATMAP: Correlation matrix showing all variable relationships")
    print("\nData: 2024 Economic indicators for 7 countries")
    print("="*60)
```
 


- Strong positive correlation between: Income and Life Expectancy
- Phillips Curve visible: Higher unemployment with lower inflation 
- South Africa: high unemployment (32%) (could be considered as an outlier depending on the context)
- USA: Highest income but not highest life expectancy
- Japan: Highest life expectancy with moderate income





## Ranking
> Use where an item's position in an ordered list is more important than its absolute or relative value. Don't be afraid to highlight the points of interest.

### Example FT uses
Wealth, deprivation, league tables, constituency election results

### Chart Types

#### Ordered bar
- A standard bar chart which orders the bars (longest, shortest, or other)

#### Ordered column
- A standard column chart which orders the columns (longest, shortest, or other)

#### Ordered proportional symbol
- Use when there are big variations between values and/or seeing fine differences in amounts

#### Slope
- Perfect for showing how ranks have changed over time or vary between categories. Use point labels or a combination of the start and end measurements

#### Lollipop
- Lollipop charts draw attention to the data value by reducing the excess ink of the bar

#### Dot strip plot
- Dot strip plots or dot plot arrays also work well for showing ranking in data where values are more closely grouped

#### Bump
- Effective for showing changing ranks through multiple stages

### Matplotlib implementation examples

> See the examples from *The Financial Times Guide* and [Practical work with `matplotlib` (2/2)](session_2_b.md).

## Distribution
> Show values in a dataset and how often they occur. The shape (or 'skew') of a distribution can be a memorable way of highlighting the lack of uniformity or equality in the data.

### Example FT uses
Income distribution, population (age/sex) distribution

### Chart Types

#### Histogram
- The standard way to show a statistical distribution - keep the gaps between columns small to highlight the 'shape' of the data

#### Dot plot
- A simple way of showing the range (and clustering) of data points

#### Dot strip plot
- Good for showing individual values in a distribution, can be a problem when too many dots are in a line

#### Barcode plot
- Like dot strip plot - but hides the identity of individual values to focus on the collective pattern

#### Beeswarm plot
- A good way of showing all the data points when too many have a single value

#### Population pyramid
- A standard way for showing the age and sex breakdown of a population distribution. Used widely to show a population by age and sex

#### Cumulative curve
- A good way of showing how unequal a distribution is: y axis is always cumulative frequency, x axis is a measure of what the distribution is showing

#### Boxplot
- Summarize multiple distributions by showing the median (center) and the spread of the data

#### Violin plot
- Similar to a box plot but more effective with complex distributions (data with two peaks, or multiple humps)

### Matplotlib implementation examples

For these distribution examples, we use demographic data from France:

> Data Source: INSEE (Institut National de la Statistique et des Études Économiques), France's national statistics bureau.




**Disclaimer:** We use simplified data for the income distribution, some assumptions are made:<br>
1️⃣ €27k average = Fiscal households (tax units) with declared income<br>
2️⃣ ~40M tax-filing units<br>
3️⃣ Couples = 1 unit<br>
4️⃣ Children excluded<br>
5️⃣ Only taxable income counted
{: .alert .alert-success .alert-soft}




```python
import pandas as pd

# France Population Age and Sex Distribution (2025)
data_population = [
    {"AgeGroup": "0-14", "Femmes": 5586, "Hommes": 5861, "Total": 11447},
    {"AgeGroup": "15-19", "Femmes": 2073, "Hommes": 2214, "Total": 4287},
    {"AgeGroup": "20-24", "Femmes": 1939, "Hommes": 2023, "Total": 3962},
    {"AgeGroup": "25-29", "Femmes": 1945, "Hommes": 1943, "Total": 3888},
    {"AgeGroup": "30-34", "Femmes": 2060, "Hommes": 1999, "Total": 4059},
    {"AgeGroup": "35-39", "Femmes": 2205, "Hommes": 2104, "Total": 4309},
    {"AgeGroup": "40-44", "Femmes": 2241, "Hommes": 2130, "Total": 4371},
    {"AgeGroup": "45-49", "Femmes": 2096, "Hommes": 2042, "Total": 4138},
    {"AgeGroup": "50-54", "Femmes": 2283, "Hommes": 2233, "Total": 4516},
    {"AgeGroup": "55-59", "Femmes": 2251, "Hommes": 2157, "Total": 4408},
    {"AgeGroup": "60-64", "Femmes": 2222, "Hommes": 2073, "Total": 4295},
    {"AgeGroup": "65-69", "Femmes": 2093, "Hommes": 1855, "Total": 3948},
    {"AgeGroup": "70-74", "Femmes": 1991, "Hommes": 1679, "Total": 3669},
    {"AgeGroup": "75+", "Femmes": 4342, "Hommes": 2965, "Total": 7307}
]

df_population = pd.DataFrame(data_population)

# Income Distribution in France (Simplified example)
data_income = [
    {"IncomeBracket": "0-10k", "Percentage": 8, "CumulativePercentage": 8},
    {"IncomeBracket": "10-15k", "Percentage": 12, "CumulativePercentage": 20},
    {"IncomeBracket": "15-20k", "Percentage": 15, "CumulativePercentage": 35},
    {"IncomeBracket": "20-25k", "Percentage": 18, "CumulativePercentage": 53},
    {"IncomeBracket": "25-30k", "Percentage": 15, "CumulativePercentage": 68},
    {"IncomeBracket": "30-40k", "Percentage": 17, "CumulativePercentage": 85},
    {"IncomeBracket": "40-50k", "Percentage": 8, "CumulativePercentage": 93},
    {"IncomeBracket": "50-75k", "Percentage": 5, "CumulativePercentage": 98},
    {"IncomeBracket": "75k+", "Percentage": 2, "CumulativePercentage": 100}
]

df_income = pd.DataFrame(data_income)
```

Population data shows France's demographic structure as of January 1, 2025 (in thousands). Income distribution represents household income brackets in euros per year. Source: INSEE, Population par sexe et groupe d'âges (2025).

```yaml
f_type: "codex_"
height_in_px: 1200
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy import stats
    
    # Create figure with subplots for distribution chart types
    fig = plt.figure(figsize=(15, 12))
    
    # France demographic data
    data_population = [
        {"AgeGroup": "0-14", "Femmes": 5586, "Hommes": 5861, "Total": 11447},
        {"AgeGroup": "15-19", "Femmes": 2073, "Hommes": 2214, "Total": 4287},
        {"AgeGroup": "20-24", "Femmes": 1939, "Hommes": 2023, "Total": 3962},
        {"AgeGroup": "25-29", "Femmes": 1945, "Hommes": 1943, "Total": 3888},
        {"AgeGroup": "30-34", "Femmes": 2060, "Hommes": 1999, "Total": 4059},
        {"AgeGroup": "35-39", "Femmes": 2205, "Hommes": 2104, "Total": 4309},
        {"AgeGroup": "40-44", "Femmes": 2241, "Hommes": 2130, "Total": 4371},
        {"AgeGroup": "45-49", "Femmes": 2096, "Hommes": 2042, "Total": 4138},
        {"AgeGroup": "50-54", "Femmes": 2283, "Hommes": 2233, "Total": 4516},
        {"AgeGroup": "55-59", "Femmes": 2251, "Hommes": 2157, "Total": 4408},
        {"AgeGroup": "60-64", "Femmes": 2222, "Hommes": 2073, "Total": 4295},
        {"AgeGroup": "65-69", "Femmes": 2093, "Hommes": 1855, "Total": 3948},
        {"AgeGroup": "70-74", "Femmes": 1991, "Hommes": 1679, "Total": 3669},
        {"AgeGroup": "75+", "Femmes": 4342, "Hommes": 2965, "Total": 7307}
    ]
    
    df_pop = pd.DataFrame(data_population)
    
    # Income distribution data
    income_brackets = np.array([5, 12.5, 17.5, 22.5, 27.5, 35, 45, 62.5, 100])  # Midpoints in thousands
    income_percentages = np.array([8, 12, 15, 18, 15, 17, 8, 5, 2])
    
    # Generate synthetic income data based on distribution
    np.random.seed(42)
    income_samples = []
    for bracket, pct in zip(income_brackets, income_percentages):
        n_samples = int(pct * 10)  # Scale for visualization
        # Add some variance within each bracket
        samples = np.random.normal(bracket, bracket * 0.15, n_samples)
        income_samples.extend(samples)
    income_samples = np.array(income_samples)
    
    fig.suptitle('DISTRIBUTION CHARTS: French Demographics & Income', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. HISTOGRAM - Income Distribution
    ax1 = plt.subplot(2, 3, 1)
    
    n, bins, patches = ax1.hist(income_samples, bins=20, edgecolor='black', alpha=0.7, color='#1565C0')
    
    # Color bars by income level
    for i, patch in enumerate(patches):
        if bins[i] < 20:
            patch.set_facecolor('#D32F2F')  # Low income - red
        elif bins[i] < 40:
            patch.set_facecolor('#FFA726')  # Middle income - orange
        else:
            patch.set_facecolor('#2E7D32')  # High income - green
    
    ax1.set_xlabel('Annual Income (€1000s)', fontsize=10)
    ax1.set_ylabel('Frequency', fontsize=10)
    ax1.set_title('1. HISTOGRAM\nHousehold Income Distribution', fontsize=11, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add statistics
    mean_income = np.mean(income_samples)
    median_income = np.median(income_samples)
    ax1.axvline(mean_income, color='red', linestyle='--', linewidth=2, label=f'Mean: €{mean_income:.1f}k')
    ax1.axvline(median_income, color='green', linestyle='--', linewidth=2, label=f'Median: €{median_income:.1f}k')
    ax1.legend(loc='upper right', fontsize=9)
    
    # 2. DOT PLOT - Age Group Distribution
    ax2 = plt.subplot(2, 3, 2)
    
    # Create dot plot for total population by age
    age_groups = df_pop['AgeGroup'].values
    totals = df_pop['Total'].values / 1000  # Convert to millions
    
    y_positions = np.arange(len(age_groups))
    
    # Plot dots
    ax2.scatter(totals, y_positions, s=100, alpha=0.6, color='#1976D2', edgecolors='black', linewidth=1)
    
    # Add value labels
    for i, (val, y) in enumerate(zip(totals, y_positions)):
        ax2.text(val + 0.1, y, f'{val:.1f}M', va='center', fontsize=9)
    
    # Add reference line for mean
    mean_pop = np.mean(totals)
    ax2.axvline(mean_pop, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax2.text(mean_pop, len(age_groups), f'Mean: {mean_pop:.1f}M', 
            rotation=90, va='bottom', ha='right', fontsize=8)
    
    ax2.set_yticks(y_positions)
    ax2.set_yticklabels(age_groups, fontsize=9)
    ax2.set_xlabel('Population (Millions)', fontsize=10)
    ax2.set_title('2. DOT PLOT\nPopulation by Age Group', fontsize=11, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()  # Youngest at top
    
    # 3. POPULATION PYRAMID
    ax3 = plt.subplot(2, 3, 3)
    
    # Prepare data for pyramid
    age_labels = df_pop['AgeGroup'].values
    men = -df_pop['Hommes'].values / 1000  # Negative for left side, in millions
    women = df_pop['Femmes'].values / 1000  # Positive for right side
    
    y_pos = np.arange(len(age_labels))
    
    # Create horizontal bars
    bars_men = ax3.barh(y_pos, men, height=0.8, color='#1976D2', alpha=0.8, label='Hommes')
    bars_women = ax3.barh(y_pos, women, height=0.8, color='#E91E63', alpha=0.8, label='Femmes')
    
    # Styling
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(age_labels, fontsize=9)
    ax3.set_xlabel('Population (Millions)', fontsize=10)
    ax3.set_title('3. POPULATION PYRAMID\nFrance 2025', fontsize=11, fontweight='bold')
    
    # Format x-axis to show absolute values
    ax3.set_xlim(-7, 7)
    ax3.set_xticks([-6, -4, -2, 0, 2, 4, 6])
    ax3.set_xticklabels(['6M', '4M', '2M', '0', '2M', '4M', '6M'])
    
    # Add vertical line at zero
    ax3.axvline(0, color='black', linewidth=1)
    
    # Legend
    ax3.legend(loc='upper right', fontsize=9)
    ax3.grid(axis='x', alpha=0.3)
    
    # 4. CUMULATIVE CURVE (Lorenz Curve for Income Inequality)
    ax4 = plt.subplot(2, 3, 4)
    
    # Create cumulative distribution
    cumulative_pct_population = np.array([0, 8, 20, 35, 53, 68, 85, 93, 98, 100])
    cumulative_pct_income = np.array([0, 2, 7, 15, 28, 45, 65, 78, 90, 100])  # Example cumulative income
    
    # Plot Lorenz curve
    ax4.plot(cumulative_pct_population, cumulative_pct_income, 
            'b-', linewidth=2.5, label='Income Distribution')
    
    # Plot line of perfect equality
    ax4.plot([0, 100], [0, 100], 'r--', linewidth=2, alpha=0.7, label='Perfect Equality')
    
    # Fill area between curves (Gini coefficient visualization)
    ax4.fill_between(cumulative_pct_population, cumulative_pct_income, 
                     cumulative_pct_population, alpha=0.3, color='yellow', 
                     label='Inequality Area')
    
    # Calculate and display Gini coefficient (simplified)
    gini_area = np.trapz(cumulative_pct_population - cumulative_pct_income, 
                        cumulative_pct_population) / 5000
    ax4.text(20, 70, f'Gini Coefficient ≈ {gini_area:.2f}', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax4.set_xlabel('Cumulative % of Population', fontsize=10)
    ax4.set_ylabel('Cumulative % of Income', fontsize=10)
    ax4.set_title('4. CUMULATIVE CURVE\nIncome Inequality (Lorenz Curve)', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper left', fontsize=9)
    ax4.set_xlim(0, 100)
    ax4.set_ylim(0, 100)
    
    # 5. BOXPLOT - Regional Income Distributions
    ax5 = plt.subplot(2, 3, 5)
    
    # Generate synthetic regional income data
    regions = ['Île-de-France', 'PACA', 'Auvergne-RA', 'Grand Est', 'Bretagne']
    regional_data = []
    
    # Different income distributions for each region
    means = [45, 32, 30, 28, 27]  # Average incomes in thousands
    stds = [15, 10, 8, 9, 7]  # Standard deviations
    
    for mean, std in zip(means, stds):
        # Generate log-normal distribution to simulate income (right-skewed)
        data = np.random.lognormal(np.log(mean), std/mean, 200)
        regional_data.append(data)
    
    # Create boxplot
    bp = ax5.boxplot(regional_data, labels=regions, patch_artist=True,
                     medianprops=dict(color='red', linewidth=2),
                     boxprops=dict(facecolor='#1976D2', alpha=0.7),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))
    
    # Color boxes by median value
    for i, (patch, data) in enumerate(zip(bp['boxes'], regional_data)):
        median_val = np.median(data)
        if median_val > 35:
            patch.set_facecolor('#2E7D32')  # High income - green
        elif median_val > 30:
            patch.set_facecolor('#FFA726')  # Medium income - orange
        else:
            patch.set_facecolor('#D32F2F')  # Lower income - red
    
    ax5.set_ylabel('Annual Income (€1000s)', fontsize=10)
    ax5.set_title('5. BOXPLOT\nRegional Income Distributions', fontsize=11, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)
    plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add mean markers
    means_actual = [np.mean(data) for data in regional_data]
    ax5.scatter(range(1, len(regions) + 1), means_actual, 
               color='black', marker='D', s=50, zorder=3, label='Mean')
    ax5.legend(loc='upper right', fontsize=9)
    
    # 6. VIOLIN PLOT - Age Distribution by Gender
    ax6 = plt.subplot(2, 3, 6)
    
    # Create synthetic age distributions for men and women
    # Based on the population pyramid data, create continuous distributions
    
    # Generate age samples weighted by population
    age_centers = np.array([7, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 80])
    
    # Men's age distribution
    men_weights = df_pop['Hommes'].values / df_pop['Hommes'].sum()
    men_ages = []
    for age, weight in zip(age_centers, men_weights):
        n_samples = int(weight * 5000)
        samples = np.random.normal(age, 3, n_samples)
        men_ages.extend(samples)
    
    # Women's age distribution
    women_weights = df_pop['Femmes'].values / df_pop['Femmes'].sum()
    women_ages = []
    for age, weight in zip(age_centers, women_weights):
        n_samples = int(weight * 5000)
        samples = np.random.normal(age, 3, n_samples)
        women_ages.extend(samples)
    
    # Create violin plot
    parts = ax6.violinplot([men_ages, women_ages], positions=[0, 1], 
                           widths=0.7, showmeans=True, showmedians=True)
    
    # Customize colors
    colors = ['#1976D2', '#E91E63']
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors[i])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
    
    # Customize other elements
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmedians', 'cmeans'):
        if partname in parts:
            vp = parts[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)
    
    # Style the plot
    ax6.set_xticks([0, 1])
    ax6.set_xticklabels(['Hommes', 'Femmes'])
    ax6.set_ylabel('Age (years)', fontsize=10)
    ax6.set_title('6. VIOLIN PLOT\nAge Distribution by Gender', fontsize=11, fontweight='bold')
    ax6.grid(axis='y', alpha=0.3)
    
    # Add statistics annotations
    ax6.text(0, 85, f'Med: {np.median(men_ages):.1f}', ha='center', fontsize=8)
    ax6.text(1, 85, f'Med: {np.median(women_ages):.1f}', ha='center', fontsize=8)
    
    # Add horizontal line at retirement age
    ax6.axhline(y=62, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax6.text(1.2, 62, 'Retirement\nAge', fontsize=8, va='center')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*60)
    print("DISTRIBUTION CHART TYPES DEMONSTRATED:")
    print("="*60)
    print("1. HISTOGRAM: Income distribution with mean/median markers")
    print("2. DOT PLOT: Population by age group showing data spread")
    print("3. POPULATION PYRAMID: Age-sex structure of France 2025")
    print("4. CUMULATIVE CURVE: Lorenz curve showing income inequality")
    print("5. BOXPLOT: Regional income distributions with quartiles")
    print("6. VIOLIN PLOT: Age distribution by gender showing density")
    print("\nData Source: INSEE (French National Statistics Bureau)")
    print("Population data as of January 1, 2025")
    print("="*60)
```



## Change over time
> Give emphasis to changing trends. These can be short (intra-day) or long (decade) periods. As time is a dimension variable this is best shown in most cases by using a horizontal axis.

### Example FT uses
Share price changes, temperature changes, economic time series

### Chart Types

#### Line
- The standard way to show a changing time series. If data are irregular, consider markers to represent data points

#### Column
- Columns work well for showing change over time - but usually best with only one series of data at a time

#### Column + line timeline
- A good way of showing the relationship over time between an amount (columns) and a rate (line)

#### Stock price
- Usually focused on day-to-day activity, these charts show opening/closing and hi/low points of each day

#### Slope
- Good for showing changing data as long as the data can be simply paired

#### Area chart
- Use with care - these are good at showing changes to total, but seeing change in components can be very difficult

#### Fan chart (projections)
- Use to show the uncertainty in future projections - usually this grows the further forward into the future

#### Connected scatterplot
- A good way of showing changing relationship between two variables over time

#### Calendar heatmap
- A great way of showing temporal patterns (daily, weekly, monthly) - at the expense of showing precision in quantity

#### Priestley timeline
- Great when date and duration are key

#### Circle timeline
- Good for showing discrete values of varying size across multiple categories (eg earthquakes by region)

#### Seismogram
- Another alternative to the circle timeline for showing series where there are big variations between values

#### Vertical timeline
- A simple way of showing the order and timing of events

### Matplotlib implementation examples

For these time series examples, we use stock price data for a fictitious technology company "TechCorp":

```yaml
f_type: "codex_"
height_in_px: 1200
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Create figure with subplots for time series chart types
    fig = plt.figure(figsize=(15, 12))
    
    # Generate fake stock data for "TechCorp"
    np.random.seed(42)
    
    # Daily data for 2 years
    start_date = datetime(2022, 1, 1)
    dates = pd.date_range(start_date, periods=730, freq='D')
    
    # Generate realistic stock price with trend and volatility
    trend = np.linspace(100, 140, 730)  # Upward trend from $100 to $140
    seasonal = 10 * np.sin(np.linspace(0, 8*np.pi, 730))  # Seasonal pattern
    noise = np.random.normal(0, 5, 730)  # Daily volatility
    stock_price = trend + seasonal + noise
    
    # Add some events that affect stock price
    stock_price[180:200] *= 0.85  # Q2 2022 dip
    stock_price[400:420] *= 1.15  # Q4 2022 surge
    stock_price[600:610] *= 0.92  # Q3 2023 correction
    
    # Monthly aggregation for some charts
    df_daily = pd.DataFrame({'Date': dates, 'Price': stock_price})
    df_monthly = df_daily.set_index('Date').resample('ME').agg({'Price': 'mean'})
    df_monthly['Volume'] = np.random.uniform(50, 150, len(df_monthly)) * 1e6  # Trading volume
    df_monthly['Volatility'] = df_daily.set_index('Date').resample('ME').agg({'Price': 'std'})['Price']
    
    fig.suptitle('CHANGE OVER TIME CHARTS: TechCorp Stock Analysis', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. LINE CHART - Basic time series
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(dates, stock_price, color='#1565C0', linewidth=1, alpha=0.8)
    
    # Add moving averages
    ma_50 = pd.Series(stock_price).rolling(50).mean()
    ma_200 = pd.Series(stock_price).rolling(200).mean()
    ax1.plot(dates, ma_50, color='#FF6B35', linewidth=1.5, alpha=0.7, label='50-day MA')
    ax1.plot(dates, ma_200, color='#2E7D32', linewidth=1.5, alpha=0.7, label='200-day MA')
    
    ax1.set_xlabel('Date', fontsize=10)
    ax1.set_ylabel('Stock Price ($)', fontsize=10)
    ax1.set_title('1. LINE CHART\nDaily Stock Price with Moving Averages', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left', fontsize=8)
    
    # Format x-axis
    import matplotlib.dates as mdates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    
    # 2. COLUMN CHART - Monthly average price
    ax2 = plt.subplot(3, 3, 2)
    
    # Select quarterly data for cleaner column chart
    df_quarterly = df_daily.set_index('Date').resample('QE').agg({'Price': 'mean'})
    colors = ['#2E7D32' if i > 0 else '#C62828' 
              for i in df_quarterly['Price'].pct_change().fillna(0)]
    
    ax2.bar(df_quarterly.index, df_quarterly['Price'], width=60, 
            color=colors, alpha=0.7, edgecolor='black', linewidth=1)
    
    ax2.set_xlabel('Quarter', fontsize=10)
    ax2.set_ylabel('Average Price ($)', fontsize=10)
    ax2.set_title('2. COLUMN CHART\nQuarterly Average Stock Price', fontsize=11, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    
    # 3. COLUMN + LINE TIMELINE - Price and Volume
    ax3 = plt.subplot(3, 3, 3)
    
    # Bar chart for volume
    color1 = '#FFA726'
    ax3.bar(df_monthly.index, df_monthly['Volume']/1e6, width=20, 
            alpha=0.5, color=color1, label='Volume')
    ax3.set_xlabel('Date', fontsize=10)
    ax3.set_ylabel('Volume (Million shares)', fontsize=10, color=color1)
    ax3.tick_params(axis='y', labelcolor=color1)
    
    # Line chart for price on secondary axis
    ax3_twin = ax3.twinx()
    color2 = '#1565C0'
    ax3_twin.plot(df_monthly.index, df_monthly['Price'], color=color2, 
                  linewidth=2, marker='o', markersize=4, label='Price')
    ax3_twin.set_ylabel('Stock Price ($)', fontsize=10, color=color2)
    ax3_twin.tick_params(axis='y', labelcolor=color2)
    
    ax3.set_title('3. COLUMN + LINE\nMonthly Volume and Price', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.2)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    
    # 4. SLOPE CHART - Year-over-year comparison
    ax4 = plt.subplot(3, 3, 4)
    
    # Compare Q1 and Q4 for each year
    quarters_data = {
        'Q1 2022': df_quarterly.iloc[0]['Price'],
        'Q4 2022': df_quarterly.iloc[3]['Price'],
        'Q1 2023': df_quarterly.iloc[4]['Price'],
        'Q4 2023': df_quarterly.iloc[7]['Price'],
    }
    
    # Plot slopes
    ax4.plot([0, 1], [quarters_data['Q1 2022'], quarters_data['Q4 2022']], 
            'o-', color='#1976D2', linewidth=2, markersize=8, label='2022')
    ax4.plot([0, 1], [quarters_data['Q1 2023'], quarters_data['Q4 2023']], 
            'o-', color='#D32F2F', linewidth=2, markersize=8, label='2023')
    
    # Add value labels
    for i, (period, value) in enumerate(quarters_data.items()):
        x = 0 if 'Q1' in period else 1
        ax4.text(x, value, f'${value:.0f}', ha='center', va='bottom', fontsize=9)
    
    ax4.set_xlim(-0.1, 1.1)
    ax4.set_xticks([0, 1])
    ax4.set_xticklabels(['Q1', 'Q4'])
    ax4.set_ylabel('Stock Price ($)', fontsize=10)
    ax4.set_title('4. SLOPE CHART\nQuarterly Performance Comparison', fontsize=11, fontweight='bold')
    ax4.legend(loc='upper left', fontsize=9)
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. AREA CHART - Price ranges (high/low bands)
    ax5 = plt.subplot(3, 3, 5)
    
    # Calculate monthly high/low
    df_monthly['High'] = df_daily.set_index('Date').resample('ME').agg({'Price': 'max'})['Price']
    df_monthly['Low'] = df_daily.set_index('Date').resample('ME').agg({'Price': 'min'})['Price']
    
    # Fill area between high and low
    ax5.fill_between(df_monthly.index, df_monthly['Low'], df_monthly['High'], 
                     alpha=0.3, color='#1565C0', label='Price Range')
    ax5.plot(df_monthly.index, df_monthly['Price'], color='#D32F2F', 
            linewidth=2, label='Average Price')
    
    ax5.set_xlabel('Date', fontsize=10)
    ax5.set_ylabel('Stock Price ($)', fontsize=10)
    ax5.set_title('5. AREA CHART\nMonthly Price Range (High/Low)', fontsize=11, fontweight='bold')
    ax5.legend(loc='upper left', fontsize=9)
    ax5.grid(True, alpha=0.3)
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax5.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    
    # 6. FAN CHART - Price projections with uncertainty
    ax6 = plt.subplot(3, 3, 6)
    
    # Historical data
    historical_dates = dates[:600]  # First 600 days
    historical_prices = stock_price[:600]
    
    # Future projections (120 days)
    future_dates = pd.date_range(dates[599], periods=121, freq='D')
    base_projection = historical_prices[-1]
    
    # Create fan of projections with increasing uncertainty
    projections = {}
    for confidence in [90, 70, 50, 30, 10]:
        std_dev = (100 - confidence) / 10  # Increasing std dev
        upper = base_projection + np.linspace(0, 30, 121) + np.linspace(0, std_dev*15, 121)
        lower = base_projection + np.linspace(0, 30, 121) - np.linspace(0, std_dev*15, 121)
        projections[confidence] = (upper, lower)
    
    # Plot historical
    ax6.plot(historical_dates, historical_prices, color='black', linewidth=1.5, label='Historical')
    
    # Plot fan
    alphas = {90: 0.2, 70: 0.3, 50: 0.4, 30: 0.5, 10: 0.6}
    for confidence, (upper, lower) in projections.items():
        ax6.fill_between(future_dates, lower, upper, alpha=alphas[confidence], 
                        color='#FF6B35', label=f'{confidence}% confidence' if confidence in [90, 50, 10] else '')
    
    # Central projection
    ax6.plot(future_dates, base_projection + np.linspace(0, 30, 121), 
            'r--', linewidth=2, label='Central projection')
    
    ax6.axvline(x=dates[599], color='gray', linestyle='--', alpha=0.5)
    ax6.set_xlabel('Date', fontsize=10)
    ax6.set_ylabel('Stock Price ($)', fontsize=10)
    ax6.set_title('6. FAN CHART\nPrice Projections with Uncertainty', fontsize=11, fontweight='bold')
    ax6.legend(loc='upper left', fontsize=8)
    ax6.grid(True, alpha=0.3)
    ax6.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    
    # 7. CONNECTED SCATTERPLOT - Price vs Volatility over time
    ax7 = plt.subplot(3, 3, 7)
    
    # Use quarterly data for cleaner visualization
    df_quarterly['Volatility'] = df_daily.set_index('Date').resample('QE').agg({'Price': 'std'})['Price']
    
    # Plot points
    scatter = ax7.scatter(df_quarterly['Volatility'], df_quarterly['Price'], 
                         c=range(len(df_quarterly)), cmap='viridis', 
                         s=100, alpha=0.7, edgecolors='black', linewidth=1)
    
    # Connect points
    ax7.plot(df_quarterly['Volatility'], df_quarterly['Price'], 
            'k-', alpha=0.3, linewidth=1)
    
    # Add start and end labels
    ax7.annotate('Start\n(Q1 2022)', 
                (df_quarterly['Volatility'].iloc[0], df_quarterly['Price'].iloc[0]),
                xytext=(-30, 20), textcoords='offset points', 
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', alpha=0.5))
    ax7.annotate('End\n(Q4 2023)', 
                (df_quarterly['Volatility'].iloc[-1], df_quarterly['Price'].iloc[-1]),
                xytext=(30, -20), textcoords='offset points', 
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', alpha=0.5))
    
    ax7.set_xlabel('Volatility (Std Dev)', fontsize=10)
    ax7.set_ylabel('Average Price ($)', fontsize=10)
    ax7.set_title('7. CONNECTED SCATTERPLOT\nPrice vs Volatility Journey', fontsize=11, fontweight='bold')
    ax7.grid(True, alpha=0.3)
    
    # 8. CALENDAR HEATMAP - Daily returns
    ax8 = plt.subplot(3, 3, 8)
    
    # Calculate daily returns for 2023
    df_2023 = df_daily[(df_daily['Date'] >= '2023-01-01') & (df_daily['Date'] < '2024-01-01')].copy()
    df_2023['Returns'] = df_2023['Price'].pct_change() * 100
    
    # Create calendar grid (simplified - showing months as rows)
    months = df_2023.set_index('Date').resample('ME').agg({'Returns': 'mean'})
    weeks = df_2023.set_index('Date').resample('W').agg({'Returns': 'mean'})
    
    # Create heatmap data (12 months x 4 weeks simplified)
    # Pad or trim to exactly 48 weeks (12 months * 4 weeks)
    weekly_returns = weeks['Returns'].values
    if len(weekly_returns) < 48:
        weekly_returns = np.pad(weekly_returns, (0, 48 - len(weekly_returns)), 'constant', constant_values=0)
    else:
        weekly_returns = weekly_returns[:48]
    heatmap_data = weekly_returns.reshape(12, 4)
    
    im = ax8.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=-5, vmax=5)
    
    ax8.set_xticks(range(4))
    ax8.set_xticklabels(['Week 1', 'Week 2', 'Week 3', 'Week 4'], fontsize=9)
    ax8.set_yticks(range(12))
    ax8.set_yticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=9)
    ax8.set_title('8. CALENDAR HEATMAP\n2023 Weekly Returns (%)', fontsize=11, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax8)
    cbar.set_label('Return (%)', fontsize=9)
    
    # 9. VERTICAL TIMELINE - Key events
    ax9 = plt.subplot(3, 3, 9)
    
    # Define key events
    events = [
        ('2022-01-15', 'IPO Launch', 100),
        ('2022-06-20', 'Q2 Earnings Miss', 85),
        ('2022-11-10', 'New Product Launch', 115),
        ('2023-03-15', 'Partnership Announced', 125),
        ('2023-09-05', 'Market Correction', 115),
        ('2023-12-20', 'Year-End Rally', 140)
    ]
    
    # Create vertical timeline
    ax9.axvline(x=0.5, color='black', linewidth=2, alpha=0.5)
    
    for i, (date_str, event, price) in enumerate(events):
        y_pos = i / (len(events) - 1)
        
        # Add event marker
        ax9.scatter(0.5, y_pos, s=100, c='#1565C0', zorder=3, edgecolors='black', linewidth=1)
        
        # Add event text (alternating sides with more spacing)
        if i % 2 == 0:
            # Left side - moved further left
            ax9.text(0.35, y_pos, f'{event}\n${price}', ha='right', va='center', fontsize=9)
            ax9.plot([0.37, 0.49], [y_pos, y_pos], 'k-', alpha=0.3)
        else:
            # Right side - moved further right
            ax9.text(0.65, y_pos, f'{event}\n${price}', ha='left', va='center', fontsize=9)
            ax9.plot([0.51, 0.63], [y_pos, y_pos], 'k-', alpha=0.3)
        
        # Add date
        date_obj = pd.to_datetime(date_str)
        ax9.text(0.5, y_pos - 0.03, date_obj.strftime('%b %Y'), 
                ha='center', va='top', fontsize=8, style='italic', alpha=0.7)
    
    ax9.set_xlim(0, 1)
    ax9.set_ylim(-0.1, 1.1)
    ax9.set_title('9. VERTICAL TIMELINE\nKey Events', fontsize=11, fontweight='bold')
    ax9.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "="*60)
    print("CHANGE OVER TIME CHART TYPES DEMONSTRATED:")
    print("="*60)
    print("1. LINE CHART: Classic time series with moving averages")
    print("2. COLUMN CHART: Quarterly averages with color coding")
    print("3. COLUMN + LINE: Dual-axis volume and price")
    print("4. SLOPE CHART: Year-over-year quarterly comparison")
    print("5. AREA CHART: Price range visualization")
    print("6. FAN CHART: Future projections with uncertainty bands")
    print("7. CONNECTED SCATTERPLOT: Price-volatility relationship over time")
    print("8. CALENDAR HEATMAP: Weekly returns pattern")
    print("9. VERTICAL TIMELINE: Key events chronology")
    print("\nData: Fictitious 'TechCorp' stock (2022-2023)")
    print("="*60)
```



## Magnitude
> Show size comparisons. These can be relative (just being able to see larger/bigger) or absolute (need to see fine differences). Usually these show a 'counted' number (for example, barrels, dollars or people) rather than a calculated rate or percent.

### Example FT uses
Commodity production, market capitalizations

### Chart Types

#### Column
- The standard way to compare the size of things. Must have a zero baseline!

#### Bar
- See above. Good when the data are not time series and labels have long category names

#### Proportional stacked bar
- A multi-set bar chart which includes a gap between each individual series to allow the reader to clearly see the full extent of each series

#### Paired column
- As per standard column but allows for multiple series. Can become tricky to read with more than 2 series

#### Paired bar
- As per standard bar but allows for multiple series

#### Proportional symbol
- Use when there are big variations between values and/or seeing exact amounts is not so important

#### Isotype (pictogram)
- Excellent solution in some instances - use only with whole numbers (do not slice off an arm to represent a decimal)

#### Lollipop
- Lollipop charts draw attention to the data value by reducing the excess ink of the bar

#### Radar
- A space-efficient way of showing magnitude for several categories - but make sure the scales are consistent!

#### Parallel coordinates
- An alternative to radar charts - again, ensure the scales are consistent. Usually benefits from highlighting values of interest



#### Bullet
- A quick, efficient way of showing actual vs. target values. A good way of showing bars vs. targets without needing too many colors or labels

#### Grouped symbol
- An alternative to bar/column charts when showing data that have big variations. Can work well in small multiple format

### Matplotlib implementation examples

For these magnitude examples, we use economic and demographic data from various countries:

> Data Sources: World Bank, OECD, UN Statistics, Eurostat, Our World in Data.

```python
import pandas as pd

# Economic data for G7 countries (2024)
# (2024, values in trillions USD, population in millions)
data_g7 = [
    {"Country": "USA", "GDP": 29.2, "Population": 332, "GDP_per_capita": 88.0, "Exports": 2.1, "Imports": 3.2},
    {"Country": "Japan", "GDP": 4.2, "Population": 124, "GDP_per_capita": 34.0, "Exports": 0.9, "Imports": 0.9},
    {"Country": "Germany", "GDP": 4.7, "Population": 84, "GDP_per_capita": 56.0, "Exports": 2.0, "Imports": 1.7},
    {"Country": "UK", "GDP": 3.5, "Population": 67, "GDP_per_capita": 52.2, "Exports": 0.8, "Imports": 0.9},
    {"Country": "France", "GDP": 3.0, "Population": 65, "GDP_per_capita": 46.0, "Exports": 0.9, "Imports": 1.0},
    {"Country": "Italy", "GDP": 2.1, "Population": 58, "GDP_per_capita": 36.2, "Exports": 0.6, "Imports": 0.5},
    {"Country": "Canada", "GDP": 2.2, "Population": 39, "GDP_per_capita": 57.0, "Exports": 0.5, "Imports": 0.5},
]

df_g7 = pd.DataFrame(data_g7)
print(df_g7)

```

<!-- # Market capitalizations of top tech companies (2024, in billions USD)
tech_companies = {
    "Apple": 3450, "Microsoft": 3100, "NVIDIA": 2900, "Amazon": 1850, 
    "Google": 2150, "Meta": 1300, "Tesla": 800, "TSMC": 650
} -->

GDP values are in trillions USD, Population in millions, Exports/Imports in trillions USD. Market capitalizations as of Q4 2024.

```yaml
f_type: "codex_"
height_in_px: 1200
inline: |
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
    import matplotlib.patches as mpatches
    
    # Create figure with subplots for magnitude chart types
    fig = plt.figure(figsize=(15, 12))
    
    # Economic data
    data_g7 = [
        {"Country": "USA", "GDP": 29.2, "Population": 332, "GDP_per_capita": 88.0, "Exports": 2.1, "Imports": 3.2},
        {"Country": "Japan", "GDP": 4.2, "Population": 124, "GDP_per_capita": 34.0, "Exports": 0.9, "Imports": 0.9},
        {"Country": "Germany", "GDP": 4.7, "Population": 84, "GDP_per_capita": 56.0, "Exports": 2.0, "Imports": 1.7},
        {"Country": "UK", "GDP": 3.5, "Population": 67, "GDP_per_capita": 52.2, "Exports": 0.8, "Imports": 0.9},
        {"Country": "France", "GDP": 3.0, "Population": 65, "GDP_per_capita": 46.0, "Exports": 0.9, "Imports": 1.0},
        {"Country": "Italy", "GDP": 2.1, "Population": 58, "GDP_per_capita": 36.2, "Exports": 0.6, "Imports": 0.5},
        {"Country": "Canada", "GDP": 2.2, "Population": 39, "GDP_per_capita": 57.0, "Exports": 0.5, "Imports": 0.5},
    ]
        
    df = pd.DataFrame(data_g7)
    
    fig.suptitle('MAGNITUDE CHARTS: Global Economic Comparisons', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. COLUMN CHART - GDP by Country
    ax1 = plt.subplot(2, 3, 1)
    
    countries = df['Country'].values
    gdp_values = df['GDP'].values
    
    # Create gradient colors based on GDP size
    colors = plt.cm.viridis(gdp_values / gdp_values.max())
    
    bars = ax1.bar(countries, gdp_values, color=colors, edgecolor='black', linewidth=1, alpha=0.8)
    
    # Add value labels on bars
    for bar, val in zip(bars, gdp_values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'${val:.1f}T', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.set_ylabel('GDP (Trillion USD)', fontsize=10)
    ax1.set_title('1. COLUMN CHART\nGDP by Country (2024)', fontsize=11, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # MUST have zero baseline for column charts
    ax1.set_ylim(0, max(gdp_values) * 1.1)
    
    # 2. PAIRED BAR - Exports vs Imports
    ax2 = plt.subplot(2, 3, 2)
    
    y_pos = np.arange(len(countries))
    bar_height = 0.35
    
    # Sort by trade volume for better visualization
    df_sorted = df.sort_values('Exports', ascending=True)
    
    bars1 = ax2.barh(y_pos - bar_height/2, df_sorted['Exports'], bar_height, 
                     label='Exports', color='#2E7D32', alpha=0.8)
    bars2 = ax2.barh(y_pos + bar_height/2, df_sorted['Imports'], bar_height,
                     label='Imports', color='#D32F2F', alpha=0.8)
    
    # Add value labels
    for i, (exp, imp) in enumerate(zip(df_sorted['Exports'], df_sorted['Imports'])):
        ax2.text(exp + 0.05, i - bar_height/2, f'${exp:.1f}T', va='center', fontsize=8)
        ax2.text(imp + 0.05, i + bar_height/2, f'${imp:.1f}T', va='center', fontsize=8)
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(df_sorted['Country'])
    ax2.set_xlabel('Trade Volume (Trillion USD)', fontsize=10)
    ax2.set_title('2. PAIRED BAR\nExports vs Imports', fontsize=11, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(axis='x', alpha=0.3)
    
    # 3. PROPORTIONAL SYMBOL - Population and GDP
    ax3 = plt.subplot(2, 3, 3)
    
    # Position countries in a grid (7 countries)
    x_positions = [1, 3, 5, 7, 2, 4, 6]
    y_positions = [3, 3, 3, 3, 1, 1, 1]
    
    # Scale bubble sizes by GDP (area proportional to value)
    max_size = 3000
    sizes = (df['GDP'] / df['GDP'].max()) * max_size
    
    # Color by GDP per capita
    colors_gdppc = df['GDP_per_capita'].values
    
    scatter = ax3.scatter(x_positions[:len(df)], y_positions[:len(df)], 
                         s=sizes, c=colors_gdppc, cmap='coolwarm',
                         alpha=0.6, edgecolors='black', linewidth=2)
    
    # Add country labels
    for i, (x, y, country, gdp) in enumerate(zip(x_positions, y_positions, 
                                                  df['Country'], df['GDP'])):
        ax3.text(x, y, f'{country}\n${gdp:.1f}T', ha='center', va='center',
                fontsize=8, fontweight='bold')
    
    # Add colorbar for GDP per capita
    cbar = plt.colorbar(scatter, ax=ax3, orientation='horizontal', pad=0.1)
    cbar.set_label('GDP per Capita ($1000s)', fontsize=9)
    
    ax3.set_xlim(0, 8)
    ax3.set_ylim(0, 4)
    ax3.set_title('3. PROPORTIONAL SYMBOL\nGDP Size & Per Capita Wealth', fontsize=11, fontweight='bold')
    ax3.axis('off')
    
    # 4. LOLLIPOP CHART - GDP per Capita
    ax4 = plt.subplot(2, 3, 4)
    
    # Sort by GDP per capita
    df_sorted_pc = df.sort_values('GDP_per_capita')
    countries_sorted = df_sorted_pc['Country'].values
    gdp_pc_sorted = df_sorted_pc['GDP_per_capita'].values
    
    y_positions = np.arange(len(countries_sorted))
    
    # Draw lollipops
    ax4.hlines(y_positions, 0, gdp_pc_sorted, colors='gray', alpha=0.4, linewidth=2)
    dots = ax4.scatter(gdp_pc_sorted, y_positions, s=100, 
                      c=gdp_pc_sorted, cmap='plasma', 
                      edgecolors='black', linewidth=1, zorder=3)
    
    # Add value labels
    for i, (val, country) in enumerate(zip(gdp_pc_sorted, countries_sorted)):
        ax4.text(val + 2, i, f'${val:.1f}k', va='center', fontsize=9)
    
    ax4.set_yticks(y_positions)
    ax4.set_yticklabels(countries_sorted)
    ax4.set_xlabel('GDP per Capita ($1000s)', fontsize=10)
    ax4.set_title('4. LOLLIPOP CHART\nGDP per Capita Ranking', fontsize=11, fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    ax4.set_xlim(0, max(gdp_pc_sorted) * 1.15)
    
    # 5. RADAR CHART - Multi-dimensional Country Comparison
    ax5 = plt.subplot(2, 3, 5, projection='polar')
    
    # Select top 4 economies for clarity
    top_countries = ['USA', 'Japan', 'Germany', 'UK']
    df_top = df[df['Country'].isin(top_countries)]
    
    # Categories for radar chart (normalized to 0-100 scale)
    categories = ['GDP', 'Population', 'GDP/Capita', 'Exports', 'Imports']
    
    # Normalize data for radar chart
    radar_data = []
    for _, row in df_top.iterrows():
        values = [
            row['GDP'] / df['GDP'].max() * 100,
            row['Population'] / df['Population'].max() * 100,
            row['GDP_per_capita'] / df['GDP_per_capita'].max() * 100,
            row['Exports'] / df['Exports'].max() * 100,
            row['Imports'] / df['Imports'].max() * 100
        ]
        radar_data.append(values)
    
    # Number of variables
    num_vars = len(categories)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Close the radar chart
    radar_data = [values + [values[0]] for values in radar_data]
    angles += angles[:1]
    
    # Plot data
    colors_radar = ['#1976D2', '#D32F2F', '#FFA726', '#2E7D32']
    for i, (country, values) in enumerate(zip(top_countries, radar_data)):
        ax5.plot(angles, values, 'o-', linewidth=2, label=country, color=colors_radar[i])
        ax5.fill(angles, values, alpha=0.15, color=colors_radar[i])
    
    # Fix axis labels
    ax5.set_xticks(angles[:-1])
    ax5.set_xticklabels(categories, size=9)
    ax5.set_ylim(0, 100)
    ax5.set_yticks([20, 40, 60, 80, 100])
    ax5.set_yticklabels(['20', '40', '60', '80', '100'], size=8)
    ax5.set_title('5. RADAR CHART\nMulti-dimensional Comparison', fontsize=11, fontweight='bold', pad=20)
    ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=9)
    ax5.grid(True)
    
    # 6. BULLET CHART - Actual vs Target Trade Balance
    ax6 = plt.subplot(2, 3, 6)
    
    # Create bullet chart data (actual trade balance and targets)
    countries_bullet = ['USA', 'Germany', 'Japan', 'France', 'UK']
    # IMPORTANT: Reorder the dataframe to match the order in countries_bullet
    df_bullet = df[df['Country'].isin(countries_bullet)]
    df_bullet = df_bullet.set_index('Country').reindex(countries_bullet).reset_index()
    
    # Calculate trade balance (Exports - Imports)
    trade_balance = df_bullet['Exports'] - df_bullet['Imports']
    targets = np.array([0, 0.2, 0, -0.05, -0.1])  # Target balances matching the order
    
    y_pos = np.arange(len(countries_bullet))
    
    # Background ranges (poor, satisfactory, good)
    for i, country in enumerate(countries_bullet):
        # Draw background ranges
        ax6.barh(i, 2, height=0.4, left=-1, color='#ffcccc', alpha=0.5)  # Poor
        ax6.barh(i, 1, height=0.4, left=-1, color='#ffffcc', alpha=0.5)  # Satisfactory  
        ax6.barh(i, 1, height=0.4, left=0, color='#ccffcc', alpha=0.5)   # Good
        
        # Draw actual value bar
        val = trade_balance.iloc[i]
        color = '#2E7D32' if val > 0 else '#D32F2F'
        ax6.barh(i, val, height=0.25, color=color, alpha=0.8)
        
        # Draw target marker
        ax6.plot(targets[i], i, 'k|', markersize=20, markeredgewidth=3)
        
        # Add value label
        ax6.text(val + 0.05 if val > 0 else val - 0.05, i, 
                f'{val:.2f}T', va='center', ha='left' if val > 0 else 'right',
                fontsize=9, fontweight='bold')
    
    ax6.set_yticks(y_pos)
    ax6.set_yticklabels(countries_bullet)
    ax6.set_xlabel('Trade Balance (Trillion USD)', fontsize=10)
    ax6.set_title('6. BULLET CHART\nTrade Balance vs Target', fontsize=11, fontweight='bold')
    ax6.set_xlim(-1.5, 1.5)
    ax6.axvline(x=0, color='black', linewidth=1, alpha=0.5)
    ax6.grid(axis='x', alpha=0.3)
    
    # Add legend for bullet chart
    poor_patch = mpatches.Patch(color='#ffcccc', label='Poor')
    sat_patch = mpatches.Patch(color='#ffffcc', label='Satisfactory')
    good_patch = mpatches.Patch(color='#ccffcc', label='Good')
    target_line = mpatches.Patch(color='black', label='Target')
    ax6.legend(handles=[good_patch, sat_patch, poor_patch, target_line], 
              loc='lower right', fontsize=8)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "="*60)
    print("MAGNITUDE CHART TYPES DEMONSTRATED:")
    print("="*60)
    print("1. COLUMN CHART: GDP comparison with zero baseline")
    print("2. PAIRED BAR: Exports vs Imports side-by-side comparison")
    print("3. PROPORTIONAL SYMBOL: Bubble size shows GDP, color shows per capita")
    print("4. LOLLIPOP CHART: GDP per capita with reduced ink")
    print("5. RADAR CHART: Multi-dimensional comparison of top economies")
    print("6. BULLET CHART: Trade balance actual vs target with ranges")
    print("\nData: 2024 Economic indicators for major economies")
    print("="*60)
```


## Part-to-whole
> Show how a single entity can be broken down into its component elements. If the components are too small to see, consider a grouped bar chart instead.

### Example FT uses
Fiscal budgets, company structures, national household spending

### Chart Types

#### Stacked column
- A simple way to show part-to-whole relationships but can be difficult to read with more than a few components

#### Proportional stacked bar
- A good way of showing the size and proportion of data at the same time - as long as the data are not too complicated

#### Pie
- A common way of showing part-to-whole data - but research shows people find it hard to compare the size of segments

#### Donut
- Similar to a pie chart - but the center can be a good way of making space to include more information about the data (eg. total)

#### Treemap
- Use for hierarchical part-to-whole relationships; can be difficult to read when there are many small segments

#### Voronoi
- A way of turning points in space into polygons while showing part to whole. Irregular division of data might be interpreted as meaningful, when it isn't

#### Arc
- A hemicircle, often used for showing political data, with the seats orientated as they would be in parliament

#### Gridplot
- Good for showing % information, often used when comparing data for two points in time

#### Venn
- Generally only used for illustrating simple set logic. Scale can be (but is not always) related to the size of the population

#### Waterfall
- Can be useful for showing part-to-whole relationships where some of the components are negative


### Matplotlib implementation examples

- [Pie Chart](https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html)
- [Donut Chart](https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html)
- [Arc (polar plots)](https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_demo.html)
- [Gridplot (using `plt.gridspec`)](https://matplotlib.org/3.1.1/tutorials/intermediate/gridspec.html) (this strategy would require a lot of work to implement)

### Examples using other libraries
- [Venn (using `matplotlib-venn`)](https://pypi.org/project/matplotlib-venn/)
- [Treemap (using `plotly`)](https://plotly.com/python/treemaps/)


## Spatial
> Used only when precise locations or geographical patterns in data are more important to the reader than anything else.

### Example FT uses
Locator maps, regional/country maps, office locations, natural resource locations, natural disaster locations

### Chart Types

#### Basic choropleth (rate/ratio)
- The standard approach for putting data on a map - should always be used for rates rather than totals

#### Proportional symbol (count/magnitude)
- Use for totals rather than rates - be wary that small differences in data may be hard to see

#### Flow map
- For showing unambiguous movement across a map

#### Contour map
- For showing areas of equal value on a map. Can use deviation colour schemes for showing +/- values

#### Equalised cartogram
- Converting each unit on a map to a regular and equally-sized shape - good for representing voting regions with equal value

#### Scaled cartogram (value)
- Stretching and shrinking a map so that each area is sized according to a particular value

#### Dot density
- Used to show the location of individual events/locations - make sure to annotate any patterns the reader should see

#### Heat map
- Grid-based data values mapped with an intensity colour scale. As choropleth map - but not snapped to an admin/political unit


### Geopandas implementation examples

`Matplotlib` is the library used by `geopandas` to build its plots. However, `geopandas` provided a high-level API to build maps, with a lot of customization options. In most cases, it is enough to only interact with the `geopandas` API to build maps.
{: .alert .alert-success .alert-soft}

- [`geopandas` User Guide - mapping and plotting tools](https://geopandas.org/en/stable/docs/user_guide/mapping.html)



## Flow
> Show the reader volumes or intensity of movement between two or more states or conditions. These might be logical sequences or geographical locations.

### Example FT uses
Movement of funds, trade, migrants, lawsuits, information, relationships

### Chart Types

#### Sankey
- Shows changes in flows from one condition to at least one other; good for tracing the multiple paths through a complex system

#### Waterfall
- Designed to show the sequencing of data through a flow process, typically budget. Can include +/- components

#### Chord
- A complex but powerful diagram which can illustrate 2-way flows. Needs good labeling

#### Network
- Used for showing the strength and inter-connectedness of relationships of varying types



### Matplotlib implementation examples

- [`matplotlib.sankey`](https://matplotlib.org/stable/api/sankey_api.html)


### Examples using other libraries

- [Network (using `networkx`)](https://networkx.org/documentation/stable/auto_examples/drawing/index.html)
- [Chord (using `mpl_chord_diagram`)](https://github.com/tfardet/mpl_chord_diagram)
