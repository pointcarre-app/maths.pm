


# Graphic Semiology Fundamentals



[TOC]

## Introduction to Graphic Semiology

*Graphic semiology studies how visual elements act as a language to encode, communicate, and process information. Pioneered by Jacques Bertin, it formalizes the grammar of graphics: how visual variables (symbols, signs, marks) represent data in diagrams, maps, and networks. Bertin’s thesis is that graphics constitute a system with its own syntax and semantics, much as in verbal language.*




![Sémiologie graphique by Jacques Bertin, EHESS 2013 reprint Source: Wikipedia | License: CC BY 4.0](files/bertin-livre-couverture-cc-wikipedia.png)
{: .max-w-[400px] .mx-auto}


<!-- Sémiologie graphique de Jacques Bertin, Réédition EHESS 2013
[Source: Wikipedia - Licence CC 4.0](https://commons.wikimedia.org/wiki/File:Bertin_semiologie-graphique.png) -->


<!-- For more details, see: 

- [1](#source-1)
- [4](#source-4)
- [5](#source-5)
- [6](#source-6) -->

## 1. Theoretical Foundations

### 1.1. Graphics as Language

- Graphics are a visual code, and each constructed image is a message.
- Visual elements (the signifiers) correspond to information components (the signified).
- The goal is to achieve “visual unity,” maximizing both efficiency and global apprehension of a message.



### 1.2. Historical Evolution

- Bertin's laboratory, the Laboratoire de Graphique, crystallized these principles through interdisciplinary collaboration, handling demands across social sciences, geography, and cartography.
- The 1967 *“Sémiologie graphique”* was a paradigm shift, bringing a rational, systematic language for visual analytics.





### 1.3. An example from [a research paper](https://www.science.org/doi/10.1126/sciadv.aaw2594)



> This graph comes from the research paper: *Different languages, similar encoding efficiency: Comparable information rates across the human communicative niche* by Christophe Coupé, Yoon Mi Oh, Dan Dediu, and François Pellegrino.<br>[Source: Science.org](https://www.science.org/doi/10.1126/sciadv.aaw2594)



### 1.4. [Optional] Information Rate (IR) Definition

- In the graph below, "SR" stands for *Speech Rate* and "IR" stands for *Information Rate*.
- Based on Shannon's information theory in the study:
    - Information Density ($ID$): Average bits of information per syllable (conditional entropy, accounting for syllable dependencies).
    - Speech Rate ($SR$): Syllables spoken per second.
- $IR = ID \\times SR$ (bits/second).
- Across $17$ languages, $IR$ averages $\text{\textasciitilde} 39$ bits/s, showing languages encode info at similar rates despite differences in $ID$ or $SR$.




![Different languages, similar encoding efficiency: Comparable information rates across the human communicative niche - by Christophe Coupé, Yoon Mi Oh, Dan Dediu, and François Pellegrino. Source: Science.org](files/language_bits_per_second-original.jpeg)
{: .max-w-[550px] .mx-auto .my-6}


More detailed explanations are available [here: Computing Shannon Entropy for Information Density](session_1_a0_shannon.md).
{: .alert .alert-success .alert-soft}



### 1.4. [An adapation](https://www.economist.com/graphic-detail/2019/09/28/why-are-some-languages-spoken-faster-than-others) from The Economist


> This graph comes from the article: *Why are some languages spoken faster than others?* by The Economist (Sep 28th 2019). [Link](https://www.economist.com/graphic-detail/2019/09/28/why-are-some-languages-spoken-faster-than-others)

![Why are some languages spoken faster than others? by The Economist - Sep 28th 2019](files/language_bits_per_second.webp)
{: .max-w-[550px] .mx-auto .my-6}



### 1.5.  💬 Discussion

**Looking at the two above graphs:**

- What are the signifiers ?
- What are the signified ?
- What can we conclude from those graphs ?
- How to they compare in terms of visual unity ?






## 2. Structure of Information



### 2.1. Theoretical Foundations

- **Invariant (Theme/Essence):** The unifying core of the data (e.g., a common subject or theme linking all data points).
- **Components (Variables/Items):** Distinct fields or characteristics in the dataset (nominal, ordinal, quantitative).
- Components can relate differentially (qualitative categories), ordinally (rank/order), or quantitatively (measured scales).
- Graphic System: Theoretical Framework
    - The cartographic/graphic “plane” is the two-dimensional space in which elements are organized.
    - It translates “plane geometry” into meaningful arrangements: quantities, categories, relationships, or spatial representations.
- **Classes of Representation**
    - **Diagrams:** Abstract data structures (e.g., time series, bar charts).
    - **Networks:** Relationships among entities (e.g., graphs, flow diagrams).
    - **Maps:** Spatial embedding of data (e.g., geographic maps).



### 2.2 Datasets used in the following examples

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Raw data lists - all buildings over 500m
    buildings = ['Burj Khalifa', 'Merdeka 118', 'Shanghai Tower', 'Abraj Al-Bait', 'Ping An']
    heights = [828, 679, 632, 601, 599]  # meters
    cities = ['Dubai', 'Kuala Lumpur', 'Shanghai', 'Mecca', 'Shenzhen']
    completion_years = [2010, 2023, 2015, 2012, 2017]
    
    # Create a DataFrame for better display
    df = pd.DataFrame({
        'Building': buildings,
        'Height (m)': heights,
        'City': cities,
        'Completion Year': completion_years
    })
    
    # Sort by height for better visualization
    df_sorted = df.sort_values('Height (m)', ascending=False).reset_index(drop=True)
    
    # Create a clean table visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=df_sorted.values,
                    colLabels=df_sorted.columns,
                    cellLoc='center',
                    loc='center',
                    bbox=[0, 0.3, 1, 0.6])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    # Style header row
    for i in range(len(df_sorted.columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style data rows with alternating colors
    for i in range(1, len(df_sorted) + 1):
        for j in range(len(df_sorted.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F2F2F2')
            else:
                table[(i, j)].set_facecolor('white')
    
    # Add title and description
    plt.title('DATASET: World\'s Tallest Buildings Over 500m\n' +
              'INVARIANT: Buildings | COMPONENTS: Name, Height, City, Year',
              fontsize=16, fontweight='bold', pad=20)
    
    # Add summary statistics
    plt.figtext(0.05, 0.15, 
               f"Dataset Summary:\n" +
               f"• Total buildings: {len(buildings)}\n" +
               f"• Height range: {min(heights)}m - {max(heights)}m\n" +
               f"• Year range: {min(completion_years)} - {max(completion_years)}\n" +
               f"• Average height: {sum(heights)/len(heights):.0f}m",
               fontsize=11, 
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.3))
    
    plt.figtext(0.35, 0.15,
               f"Data Types:\n" +
               f"• Building names: Nominal (categorical)\n" +
               f"• Heights: Quantitative (continuous)\n" +
               f"• Cities: Nominal (categorical)\n" +
               f"• Years: Quantitative (discrete)",
               fontsize=11,
               bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.3))
    
    plt.tight_layout()
    plt.show()
```

### 2.3. An example with a bar chart


```yaml
f_type: "codex_"
height_in_px: 950
inline: |
    import matplotlib.pyplot as plt

    # Real data: World's tallest buildings over 500m
    # INVARIANT: Buildings (the theme)

    # Raw data lists - all buildings over 500m
    buildings = ['Burj Khalifa', 'Merdeka 118', 'Shanghai Tower', 'Abraj Al-Bait', 'Ping An']
    heights = [828, 679, 632, 601, 599]  # meters
    cities = ['Dubai', 'Kuala Lumpur', 'Shanghai', 'Mecca', 'Shenzhen']
    completion_years = [2010, 2023, 2015, 2012, 2017]

    # Sort by year for proper x-axis
    sorted_data = sorted(zip(completion_years, buildings, heights, cities))
    years_sorted = [item[0] for item in sorted_data]
    buildings_sorted = [item[1] for item in sorted_data]
    heights_sorted = [item[2] for item in sorted_data]
    cities_sorted = [item[3] for item in sorted_data]

    # Create larger figure with high DPI
    plt.figure(figsize=(16, 10), dpi=150)
    colors = ['#2C3E50', '#34495E', '#5D6D7E', '#85929E', '#AEB6BF']  # Different shades of grey
    bars = plt.bar(years_sorted, heights_sorted, width=1, color=colors, alpha=0.9, 
                edgecolor='black', linewidth=2)

    # Add building names and cities above bars with bigger text and more space
    for i, (bar, building, city) in enumerate(zip(bars, buildings_sorted, cities_sorted)):
        # Building name - bigger font and more spacing
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 35, 
                building, ha='center', va='bottom', fontsize=16, fontweight='bold')
        # City name in italics - bigger font and more spacing
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 65, 
                city, ha='center', va='bottom', fontsize=14, style='italic')

    # X-axis with actual years as x values
    all_years = list(range(2010, 2024))
    plt.xticks(all_years, fontsize=16, rotation=45)
    plt.xlabel('Completion Year', fontsize=16, fontweight='bold')
    plt.ylabel('Height (meters)', fontsize=16, fontweight='bold')
    plt.title('STRUCTURE: Invariant + Components\nInvariant: Buildings | Components: Name (nominal), Height (quantitative), City (nominal), Year (quantitative)', 
            fontsize=20, pad=30, fontweight='bold')

    plt.ylim(0, max(heights_sorted) + 120)  # Extra space for larger labels

    # Improve overall appearance
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()

    plt.show()
```



<!-- plt.tight_layout() -->



### 2.4.  💬 Discussion

**Looking at the above graph:**

- What are the signifiers ?
- What are the signified ?
- What can we conclude from those graphs ?
- How to they compare in terms of readability and visual unity ?


## 3. Relationships

### 3.1. Relations and dimensionality

- Key in analysis: how components relate, not necessarily their individual meanings, but their differences and connections.
- For every dataset, determining its dimensionality (number/nature of components) directs the choice of graphic strategy.



### 3.2. 💾 Datasets used in the following examples


```html
<details class="my-2 sm:p-4 sm:bg-base-200" style="border-radius: var(--radius-box);overflow-x: scroll;">
    <summary>100m men world record progression</summary>
    <table class="table p-4 mt-2" style="border-radius: var(--radius-box);">
        <thead>
            <tr>
                <th>Date</th><th>Time (s)</th><th>Athlete Country</th>
            </tr>
        </thead>
      <tbody>
          <tr>
            <td>1912-07-06</td><td>10.6</td><td>🇺🇸</td>
          </tr>   
          <tr>
            <td>1921-04-23</td><td>10.4</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1930-08-09</td><td>10.3</td><td>🇨🇦</td>
          </tr>
          <tr>
            <td>1936-06-20</td><td>10.2</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1956-08-03</td><td>10.1</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1960-06-21</td><td>10.0</td><td>🇩🇪</td>
          </tr>
          <tr>
            <td>1968-06-20</td><td>9.95</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1983-07-03</td><td>9.93</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1988-09-24</td><td>9.92</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1991-06-14</td><td>9.90</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1991-08-25</td><td>9.86</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1994-07-06</td><td>9.85</td><td>🇺🇸</td>
          </tr>
          <tr>
            <td>1996-07-27</td><td>9.84</td><td>🇨🇦</td>
          </tr>
          <tr>
            <td>1999-06-16</td><td>9.79</td><td>🇺🇸</td>
          </tr>
        
          <tr>
            <td>2005-06-14</td><td>9.77</td><td>🇯🇲</td>
          </tr>
          <tr>
            <td>2008-05-31</td><td>9.72</td><td>🇯🇲</td>
          </tr>
          <tr>
            <td>2008-08-16</td><td>9.69</td><td>🇯🇲</td>
          </tr>
          <tr>
            <td>2009-08-16</td><td>9.58</td><td>🇯🇲</td>
          </tr>
      </tbody>
    </table>
    <p class="text-sm text-gray-500">Source: Wikipedia / World Athletics (as of September 2025)</p>
</details>
```


```html
<details class="my-2 sm:p-4 sm:bg-base-200" style="border-radius: var(--radius-box);overflow-x: scroll;">
    <summary>North countries national development profiles</summary>
    <table class="table p-4 mt-2" style="border-radius: var(--radius-box);">
        <thead>
            <tr>
                <th>Country</th><th>GDP per Capita</th><th>Life Expectancy</th><th>Education Index</th><th>Happiness Score</th><th>Innovation Index</th><th>Environmental Score</th>
            </tr>
        </thead>
        <tbody>
            <tr><td style="min-width:180px !important;";>Norway 🇳🇴</td><td>75</td><td>82</td><td>95</td><td>76</td><td>68</td><td>78</td></tr>
            <tr><td style="min-width:180px !important;";>Switzerland 🇨🇭</td><td>81</td><td>84</td><td>88</td><td>75</td><td>67</td><td>81</td></tr>
            <tr><td style="min-width:180px !important;";>Denmark 🇩🇰</td><td>60</td><td>81</td><td>92</td><td>78</td><td>58</td><td>78</td></tr>
            <tr><td style="min-width:180px !important;";>Iceland 🇮🇸</td><td>52</td><td>83</td><td>95</td><td>75</td><td>55</td><td>68</td></tr>
            <tr><td style="min-width:180px !important;";>Netherlands 🇳🇱</td><td>53</td><td>82</td><td>93</td><td>74</td><td>58</td><td>76</td></tr>
            <tr><td style="min-width:180px !important;";>Sweden 🇸🇪</td><td>51</td><td>83</td><td>94</td><td>73</td><td>63</td><td>78</td></tr>
            <tr><td style="min-width:180px !important;";>Germany 🇩🇪</td><td>46</td><td>81</td><td>93</td><td>70</td><td>87</td><td>77</td></tr>
            <tr><td style="min-width:180px !important;";>Canada 🇨🇦</td><td>46</td><td>82</td><td>92</td><td>72</td><td>61</td><td>72</td></tr>
            <tr><td style="min-width:180px !important;";>Australia 🇦🇺</td><td>55</td><td>83</td><td>92</td><td>73</td><td>46</td><td>60</td></tr>
            <tr><td style="min-width:180px !important;";>Japan 🇯🇵</td><td>39</td><td>85</td><td>85</td><td>59</td><td>54</td><td>65</td></tr>
            <tr><td style="min-width:180px !important;";>South Korea 🇰🇷</td><td>31</td><td>83</td><td>85</td><td>58</td><td>64</td><td>63</td></tr>
            <tr><td style="min-width:180px !important;";>United Kingdom 🇬🇧</td><td>42</td><td>81</td><td>90</td><td>70</td><td>59</td><td>58</td></tr>
            <tr><td style="min-width:180px !important;";>France 🇫🇷</td><td>40</td><td>83</td><td>88</td><td>66</td><td>54</td><td>80</td></tr>
            <tr><td style="min-width:180px !important;";>Belgium 🇧🇪</td><td>47</td><td>82</td><td>89</td><td>69</td><td>50</td><td>73</td></tr>
            <tr><td style="min-width:180px !important;";>Austria 🇦🇹</td><td>48</td><td>81</td><td>91</td><td>71</td><td>45</td><td>79</td></tr>
        </tbody>
    </table>
    <p class="text-sm text-gray-500">Source: United Nations Development Programme, World Bank, OECD, WIPO, and World Happiness Report, compiled and normalized (2024–2025)</p>
</details>
```


### 3.3. An example with a scatter plot 


> Here we add a regression line to the scatter plot to show the trend of the data. It show how to combine lines and points in the same plot.


Look carefully at the axis: the $y$ axis is inverted, because the faster times are better. This is a common practice in data visualization, it's not mandatory, but it helps to make the plot more readable.
{: .alert .alert-warning .alert-soft}



```yaml
f_type: "codex_"
height_in_px: 1560
inline: |
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime
    import numpy as np

    # World record data (precise date, time, country)
    records = [
        ("1912-07-06", 10.6, "USA", "🇺🇸"),
        ("1921-04-23", 10.4, "USA", "🇺🇸"),
        ("1930-08-09", 10.3, "CAN", "🇨🇦"),
        ("1936-06-20", 10.2, "USA", "🇺🇸"),
        ("1956-08-03", 10.1, "USA", "🇺🇸"),
        ("1960-06-21", 10.0, "GER", "🇩🇪"),
        ("1968-06-20", 9.95, "USA", "🇺🇸"),
        ("1983-07-03", 9.93, "USA", "🇺🇸"),
        ("1988-09-24", 9.92, "USA", "🇺🇸"),
        ("1991-06-14", 9.90, "USA", "🇺🇸"),
        ("1991-08-25", 9.86, "USA", "🇺🇸"),
        ("1994-07-06", 9.85, "USA", "🇺🇸"),
        ("1996-07-27", 9.84, "CAN", "🇨🇦"),
        ("1999-06-16", 9.79, "USA", "🇺🇸"),
        ("2005-06-14", 9.77, "JAM", "🇯🇲"),
        ("2008-05-31", 9.72, "JAM", "🇯🇲"),
        ("2008-08-16", 9.69, "JAM", "🇯🇲"),
        ("2009-08-16", 9.58, "JAM", "🇯🇲")
    ]

    dates = [datetime.strptime(r[0], "%Y-%m-%d") for r in records]
    times = [r[1] for r in records]
    countries = [r[2] for r in records]
    emojis = [r[3] for r in records]

    colors = {"USA": "#1f77b4", "CAN": "#ff7f0e", "JAM": "#2ca02c", "GER":"#999999"}
    point_colors = [colors[c] for c in countries]

    plt.figure(figsize=(12, 7))
    plt.scatter(dates, times, c=point_colors, s=85, edgecolor='black', label="World Record")

    # Prepare dates for proper regression with zero-based normalization
    x = mdates.date2num(dates)
    x0 = x - x[0]

    # Regression line on normalized x axis
    z = np.polyfit(x0, times, 1)
    p = np.poly1d(z)
    plt.plot(dates, p(x0), "r--", alpha=0.8, linewidth=2, 
            label=f"Trend: {z[0]:.5f} s/day")

    plt.xlabel('Date', fontsize=13)
    plt.ylabel('Time (seconds)', fontsize=13)
    plt.title(
        '100m Men World Record Progression\n'
        'Relationship: Athletic Performance vs Time\n'
        'Source: Wikipedia / World Athletics (as of September 2025)',
        fontsize=15,
        pad=18,
        fontweight='bold'
    )
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3)

    # Custom legend for countries (name + color + emoji)
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["USA"], 
            markeredgecolor='black', markersize=11, label='USA'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["CAN"], 
            markeredgecolor='black', markersize=11, label='Canada'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["JAM"],
            markeredgecolor='black', markersize=11, label='Jamaica'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors["GER"],
            markeredgecolor='black', markersize=11, label='Germany')
    ]
    plt.legend(
        handles=legend_elements,
        loc='lower right',
        fontsize=13,
        title="Country"
    )
    plt.tight_layout()
    plt.show()
```
    
    


Since not only the 100m men world record, but also most of the world records (whatever the sport) have been improved continuously during the last century, what can we conclude about the evolution in the field of athletics?
{: .alert .alert-info .alert-soft}


### 3.4. An example with a heatmap

> This example demonstrates how multiple quantitative components relate across different entities. The heatmap reveals patterns, clusters, and trade-offs that emerge from multi-dimensional data without incorrectly connecting nominal categories.


The y-axis is sorted by GDP per capita, descending.
{: .alert .alert-info .alert-soft}

```yaml
f_type: "codex_"
height_in_px: 800
inline: |
    import matplotlib.pyplot as plt
    import numpy as np

    countries = ['Norway', 'Switzerland', 'Denmark', 'Iceland', 'Netherlands', 
                'Sweden', 'Germany', 'Canada', 'Australia', 'Japan', 'South Korea',
                'United Kingdom', 'France', 'Belgium', 'Austria']

    data = {
        'GDP per Capita': [75, 81, 60, 52, 53, 51, 46, 46, 55, 39, 31, 42, 40, 47, 48],
        'Life Expectancy': [82, 84, 81, 83, 82, 83, 81, 82, 83, 85, 83, 81, 83, 82, 81],
        'Education Index': [95, 88, 92, 95, 93, 94, 93, 92, 92, 85, 85, 90, 88, 89, 91],
        'Happiness Score': [76, 75, 78, 75, 74, 73, 70, 72, 73, 59, 58, 70, 66, 69, 71],
        'Innovation Index': [68, 67, 58, 55, 58, 63, 87, 61, 46, 54, 64, 59, 54, 50, 45],
        'Environmental Score': [78, 81, 78, 68, 76, 78, 77, 72, 60, 65, 63, 58, 80, 73, 79]
    }

    data_matrix = np.array([data[key] for key in data.keys()]).T

    # Sort countries by GDP per capita (descending)
    sorted_indices = np.argsort(data['GDP per Capita'])[::-1]
    countries_sorted = [countries[i] for i in sorted_indices]
    data_matrix_sorted = data_matrix[sorted_indices]

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(data_matrix_sorted, cmap='RdYlBu_r', aspect='auto', vmin=30, vmax=95)

    for i in range(len(countries_sorted)):
        for j in range(len(data.keys())):
            val = int(data_matrix_sorted[i, j])
            color = 'black' if 50 <= val <= 80 else 'white'
            ax.text(j, i, val, ha='center', va='center', color=color, fontweight='bold')

    ax.set_xticks(range(len(data.keys())))
    ax.set_xticklabels(list(data.keys()), rotation=45, ha='right', fontsize=13)
    ax.set_yticks(range(len(countries_sorted)))
    ax.set_yticklabels(countries_sorted)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Score', rotation=270, labelpad=15)

    ax.set_title('DIMENSIONALITY: 6D Data Matrix\nInvariant: National Profiles | Each cell = one relationship', 
                fontsize=16, fontweight='bold', pad=25)
    ax.set_xlabel('Components (Dimensions)', fontsize=14)
    ax.set_ylabel('Countries (Entities)', fontsize=12)

    plt.tight_layout()
    plt.show()

```




### 3.5. Another example with a heatmap


```yaml
f_type: "codex_"
height_in_px: 780
inline: |
    import matplotlib.pyplot as plt
    import numpy as np

    data = {
        'GDP per Capita': [75, 81, 60, 52, 53, 51, 46, 46, 55, 39, 31, 42, 40, 47, 48],
        'Life Expectancy': [82, 84, 81, 83, 82, 83, 81, 82, 83, 85, 83, 81, 83, 82, 81],
        'Education Index': [95, 88, 92, 95, 93, 94, 93, 92, 92, 85, 85, 90, 88, 89, 91],
        'Happiness Score': [76, 75, 78, 75, 74, 73, 70, 72, 73, 59, 58, 70, 66, 69, 71],
        'Innovation Index': [68, 67, 58, 55, 58, 63, 87, 61, 46, 54, 64, 59, 54, 50, 45],
        'Environmental Score': [78, 81, 78, 68, 76, 78, 77, 72, 60, 65, 63, 58, 80, 73, 79]
    }

    data_matrix = np.array([data[key] for key in data.keys()]).T
    corr_matrix = np.corrcoef(data_matrix.T)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    fig, ax = plt.subplots(figsize=(10, 10))
    masked_corr = np.ma.masked_where(mask, corr_matrix)
    im = ax.matshow(masked_corr, cmap='RdBu_r', vmin=-1, vmax=1)

    for i in range(len(data.keys())):
        for j in range(len(data.keys())):
            if i >= j:
                corr_val = corr_matrix[i, j]
                ax.text(j, i, f"{corr_val:.2f}", ha='center', va='center', color='black', fontsize=10, fontweight='bold')

    ax.set_xticks(range(len(data.keys())))
    ax.set_xticklabels([key.replace(' ', '\n') for key in data.keys()], rotation=45, ha='left')
    ax.set_yticks(range(len(data.keys())))
    ax.set_yticklabels([key.replace(' ', '\n') for key in data.keys()])

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Correlation', rotation=270, labelpad=15)

    ax.set_title('COMPONENT RELATIONSHIPS\nHow dimensions correlate with each other', fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
    plt.show()

```

### 3.6. Alternative: Clustered scatter matrix

```yaml
f_type: "codex_"
height_in_px: 1200
inline: |
    import matplotlib.pyplot as plt
    import numpy as np

    # Same data as above
    countries = ['Norway', 'Switzerland', 'Denmark', 'Iceland', 'Netherlands', 
                'Sweden', 'Germany', 'Canada', 'Australia', 'Japan', 'South Korea',
                'United Kingdom', 'France', 'Belgium', 'Austria']
    
    gdp = [75, 81, 60, 52, 53, 51, 46, 46, 55, 39, 31, 42, 40, 47, 48]
    happiness = [76, 75, 78, 75, 74, 73, 70, 72, 73, 59, 58, 70, 66, 69, 71]
    innovation = [68, 67, 58, 55, 58, 63, 87, 61, 46, 54, 64, 59, 54, 50, 45]
    environment = [78, 81, 78, 68, 76, 78, 77, 72, 60, 65, 63, 58, 80, 73, 79]
    
    # Create regions for coloring
    regions = ['Nordic']*6 + ['Western Europe']*5 + ['Asia']*2 + ['Anglo']*2
    region_colors = {'Nordic': '#2E4057', 'Western Europe': '#048A81', 
                    'Asia': '#F18F01', 'Anglo': '#C73E1D'}
    colors = [region_colors[region] for region in regions]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    
    # Four key 2D relationships
    plots_config = [
        (ax1, gdp, happiness, 'GDP per Capita', 'Happiness Score'),
        (ax2, innovation, environment, 'Innovation Index', 'Environmental Score'),
        (ax3, gdp, innovation, 'GDP per Capita', 'Innovation Index'),
        (ax4, happiness, environment, 'Happiness Score', 'Environmental Score')
    ]
    
    for ax, x_data, y_data, x_label, y_label in plots_config:
        scatter = ax.scatter(x_data, y_data, c=colors, s=100, alpha=0.7, 
                           edgecolor='black', linewidth=1)
        
        # Add trend line
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        x_trend = np.linspace(min(x_data), max(x_data), 100)
        ax.plot(x_trend, p(x_trend), "r--", alpha=0.6, linewidth=1.5)
        
        ax.set_xlabel(x_label, fontsize=11)
        ax.set_ylabel(y_label, fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Add correlation coefficient
        corr = np.corrcoef(x_data, y_data)[0,1]
        ax.text(0.05, 0.95, f'r = {corr:.2f}', transform=ax.transAxes, 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Overall title
    fig.suptitle('MULTI-DIMENSIONAL RELATIONSHIPS: 2D Projections of 6D Data\n' +
                'Pattern: Nordic countries cluster consistently across dimensions', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Legend
    handles = [plt.scatter([], [], c=color, s=100, label=region, edgecolor='black') 
              for region, color in region_colors.items()]
    fig.legend(handles=handles, loc='center', bbox_to_anchor=(0.5, 0.02), ncol=4)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.08)
    plt.show()
```


### 3.7.  💬 Discussion

**Looking at the above graph:**

- What are the signifiers ?
- What are the signified ?
- What can we conclude from those graphs ?
- How to they compare in terms of readability and visual unity ?
- **Big findings?** Are we this sure ? (<span class="italic">For some heatmap values from 3.4, once the economical context of those countries is known, the analysis is pretty clear. But for some others, it's not so obvious.</span>)





## 4. Visual  Variables


This part of the lecture is available [here: Visual Variables](session_1_a1_visual_retinal.md).
{: .alert .alert-success .alert-soft}


## 5. Graphic Rules and Grammar

### 5.1. Problem Construction

- Any graphic is a solution to multiple possible ways to encode the same dataset—the “graphic problem” is to choose the most efficient/legible.
- Design must account for perceptual tasks (lookup, comparison, grouping, pattern search).

### 5.2. Grammar of Construction

- **Density:** Avoid excessive clutter, but enough detail for insight.
- **Retinal Legibility:** Variables should combine without creating confusion.
- **Layering/Separation:** Different elements must remain perceptually separable (via color, value, or shape).

***

## 6. Reading Process and Perception

### 6.1. Pre-attentive Perception

- Visual variables support rapid, unconscious discovery of groupings and patterns.[7]
- “Selectivity” relates to perception: some variables (color, size) create instantly distinguishable groups, while others require sequential search.[7]

### 6.2. Cognitive Load

- Bertin aimed for graphics with the “least mental cost”: images readable at a glance, but acknowledged such universality ignores cultural/experiential differences.[5]

***

## 7. Functional Types of Graphics

### 7.1. Graphic Functions

- **Recording:** Visuals act as storage, often exhaustive and detailed.[1]
- **Communication:** Designed to highlight, simplify, persuade (editorial, presentations).[10][1]
- **Processing/Analysis:** Dynamic or interactive graphics for active reasoning, including the “mobile” Bertin Matrix for pattern-finding.[5]

> {{matplotlib_placeholder_functional_types}}

***

## 8. Application Examples

### 8.1. Diagrammatic Uses

- Bar/line charts for temporal or categorical progression.
- Matrices for comparing variables and uncovering structure (e.g., Bertin’s reorderable matrices).[5]

### 8.2. Network Uses

- Force-directed graphs for social/political ties.
- Flow diagrams for process and logistics.

### 8.3. Spatial Use (Maps)

- Thematic maps using hue or texture for data distribution.
- “Image-file” arrangements for sorting and exploring spatial patterns.[5]

> {{matplotlib_placeholder_application_examples}}

***

## 9. Semiotic Theory in Graphics

### 9.1. Signs and Meaning

- **Signifier:** Visual mark/symbol.[11][5]
- **Signified:** The concept/data represented.[11][5]
- Literal (denotation) and cultural/contextual (connotation) meaning may differ.[12][11][5]

### 9.2. Category of Signs

- **Icon:** Resemblance (e.g., shape of a tree for a forest).
- **Index:** Causality/association (e.g., thermometer icon for temperature).
- **Symbol:** Arbitrary or conventional representation (e.g., blue for water).[11]

***

## 10. Critique and Evolution

- Bertin’s work is foundational, yet some properties such as cognitive differences and cultural bias were underexplored.[5]
- Later work in visual analytics, user-centric/cultural semiotics, and digital technology broaden the grammar Bertin established.[3][5]

***

## Placeholders for Matplotlib Visualizations

- {{matplotlib_placeholder_information_structure}}
- {{matplotlib_placeholder_visual_variables}}
- {{matplotlib_placeholder_functional_types}}
- {{matplotlib_placeholder_application_examples}}

***

## References

**Jacques Bertin - Semiology of Graphics: Diagrams, Networks, Maps** (1967/2010)
{: #source-1}
<br>The foundational work that established graphic semiology as a systematic approach to visual information design. Bertin's comprehensive treatise on how visual variables encode data meaning.

**Nicolas Kruchten - Interactive Exploration of Bertin's Semiology of Graphics**
{: #source-2}
<br>Modern interactive interpretation and exploration of Bertin's principles, demonstrating their continued relevance in digital visualization.

**InformationVisuals.com - Jacques Bertin's Semiology of Graphics**
{: #source-3}
<br>Contemporary analysis and explanation of Bertin's theoretical framework, making his concepts accessible to modern designers and data analysts.

**St. Mary's College Archive - Jacques Bertin: Semiology of Graphics**
{: #source-4}
<br>Academic archive containing Bertin's work on graphics as a language system, exploring the linguistic properties of visual communication.

**Hypergeo/EHESS - Jacques Bertin Biography and Theory**
{: #source-5}
<br>Comprehensive biographical and theoretical overview from the École des Hautes Études en Sciences Sociales, detailing Bertin's contributions to geographic and graphic sciences.

**History of Information - Bertin's Visual Variables**
{: #source-6}
<br>Historical documentation of Bertin's eight visual variables and their impact on information design methodology.

**International Cartographic Association - Associativity and Disassociativity of Visual Variables**
{: #source-7}
<br>Reimer's analysis of how visual variables interact, focusing on the crucial concept of associativity in multi-variable graphic design.

**Digital Society School - Bertin Semiology of Graphics Excerpt**
{: #source-8}
<br>Educational excerpt focusing on the practical applications of Bertin's plane geometry concepts in contemporary design.

**Anthony Masure - From Semiology of Graphics to Cultural Analytics**
{: #source-9}
<br>Modern interpretation connecting Bertin's foundational work to contemporary cultural analytics and digital humanities approaches.

**ESRI Press - Semiology of Graphics Sample Pages**
{: #source-10}
<br>Publishing sample demonstrating practical applications of Bertin's principles in geographic information systems and cartographic design.

**Squarespace Archive - Semiotics and Graphic Design**
{: #source-11}
<br>Resource on the broader semiotic foundations underlying graphic design, extending beyond Bertin's specific contributions.

**Aiello, G. - Visual Semiotics: Key Concepts and New Directions (2020)**
{: #source-12}
<br>Contemporary academic analysis published in The SAGE Handbook of Visual Research Methods, updating semiotic theory for modern visual research.

***

All structure, distinctions, and categories directly referenced from leading analyses and primary sources on graphic semiology, ready for highly detailed study or code-linked illustration.