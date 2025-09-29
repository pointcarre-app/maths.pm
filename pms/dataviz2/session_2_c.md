
# Practical work with `matplotlib` (2/2)




[TOC]


Any issue related to the proper execution of code on your machine must be solved during this session. **Feel free to ask for help.**
{: .alert .alert-error .alert-soft}




We'll use panel data: nominal GDP per year and per country. The dataset and its documentation are available [here](https://github.com/datasets/gdp).

## Objective: applying what you have learned during this session: 


- [**Visual Vocabulary - Financial Times Guide**](session_2_a.md)
- [**`matplotlib` as the Python reference for building graphs**](session_2_b.md)
- [**Practical work with `matplotlib` (2/2)**](session_2_c.md)


Since `matplotlib` enables us to make very flexible graphs, we can make them as elegant as possible. This is a good exercise to learn how to use `matplotlib` to its full potential.
{: .alert .alert-success .alert-soft}

## Dataset Information

The dataset is the same as that used in the first practical work session: [**Practical work with `matplotlib` (1/2)**](session_1_f.md).
{: .alert .alert-info .alert-soft}


- **Source**: World Bank GDP data
- **URL**: `https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv`
- **Key Columns**: `Country Name`, `Country Code`, `Year`, `Value` (GDP in USD)
- **Time Range**: 1960-2020



## Important information

Some entities are not countries but rather regions, income groups, etc. In some cases, you should exclude them; in other cases, they can be very useful. Here is the list of these entities.
{: .alert .alert-info .alert-soft}


```python
non_country_entities = [
    ['Africa Eastern and Southern', 'AFE'],
    ['Africa Western and Central', 'AFW'],
    ['Arab World', 'ARB'],
    ['Caribbean small states', 'CSS'],
    ['Central Europe and the Baltics', 'CEB'],
    ['Channel Islands', 'CHI'],
    ['Early-demographic dividend', 'EAR'],
    ['East Asia & Pacific', 'EAS'],
    ['East Asia & Pacific (IDA & IBRD countries)', 'TEA'],
    ['East Asia & Pacific (excluding high income)', 'EAP'],
    ['Euro area', 'EMU'],
    ['Europe & Central Asia', 'ECS'],
    ['Europe & Central Asia (IDA & IBRD countries)', 'TEC'],
    ['Europe & Central Asia (excluding high income)', 'ECA'],
    ['European Union', 'EUU'],
    ['Fragile and conflict affected situations', 'FCS'],
    ['Heavily indebted poor countries (HIPC)', 'HPC'],
    ['High income', 'HIC'],
    ['IBRD only', 'IBD'],
    ['IDA & IBRD total', 'IBT'],
    ['IDA blend', 'IDB'],
    ['IDA only', 'IDX'],
    ['IDA total', 'IDA'],
    ['Late-demographic dividend', 'LTE'],
    ['Latin America & Caribbean', 'LCN'],
    ['Latin America & Caribbean (excluding high income)', 'LAC'],
    ['Latin America & the Caribbean (IDA & IBRD countries)', 'TLA'],
    ['Least developed countries: UN classification', 'LDC'],
    ['Low & middle income', 'LMY'],
    ['Low income', 'LIC'],
    ['Lower middle income', 'LMC'],
    ['Middle East & North Africa', 'MEA'],
    ['Middle East & North Africa (IDA & IBRD countries)', 'TMN'],
    ['Middle East & North Africa (excluding high income)', 'MNA'],
    ['Middle income', 'MIC'],
    ['North America', 'NAC'],
    ['OECD members', 'OED'],
    ['Other small states', 'OSS'],
    ['Pacific island small states', 'PSS'],
    ['Post-demographic dividend', 'PST'],
    ['Pre-demographic dividend', 'PRE'],
    ['Small states', 'SST'],
    ['South Asia', 'SAS'],
    ['South Asia (IDA & IBRD)', 'TSA'],
    ['Sub-Saharan Africa', 'SSF'],
    ['Sub-Saharan Africa (IDA & IBRD countries)', 'TSS'],
    ['Sub-Saharan Africa (excluding high income)', 'SSA'],
    ['Upper middle income', 'UMC'],
    ['World', 'WLD']
]
```


## Setup Code (Run First)

### Using `pyodide`

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
df_countries = df[~df['Country Code'].isin(non_country_entities)]

df_non_countries = df[df['Country Code'].isin(non_country_entities)]

print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")
```


### Local execution 


```python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("gdp.csv")

# Exclude non-country entities (regions, income groups)
non_country_entities  = {
    'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
    'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
    'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
    'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
    'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
}
df_countries = df[~df['Country Code'].isin(non_country_entities)]

df_non_countries = df[df['Country Code'].isin(non_country_entities)]

print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")
```


## Exercises: Ranking



The exercises illustrate the Ranking section of the [**Visual Vocabulary - Financial Times Guide**](session_2_a.md).
{: .alert .alert-info .alert-soft}


> Ranking visualizations are essential for showing order and hierarchy in data. They help readers quickly identify leaders, laggards, and relative positions. In this exercise, you'll explore different ways to visualize rankings using GDP data.



🏗️ Code for data preprocessing, comments proposing steps to follow, and commented code giving clues have been provided for you in the snippets below.
{: .alert .alert-success .alert-soft}




### Exercise 1.1: Ordered Bar Chart

**Task**: Create a horizontal bar chart showing the top 15 economies by GDP in 2019, ordered from highest to lowest (from bottom to top).

**Requirements**:

- Sort countries by GDP value
- Use a gradient colormap to emphasize ranking
- Format GDP values in trillions
- Add value labels at the end of each bar
- Include gridlines for easier reading

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

  # Exclude non-country entities (regions, income groups)
  non_country_entities  = {
      'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
      'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
      'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
      'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
      'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
  }
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")


  # Filter for 2019 data and get top 15 countries
  df_2019 = df_countries[df_countries['Year'] == 2019].copy()
  df_2019 = df_2019.sort_values('Value', ascending=False).head(15)
  
  # Create figure
  fig, ax = plt.subplots(figsize=(12, 8))
  
  # Create color gradient
  ...
  
  # Create horizontal bar chart
  ...
  
  # Customize axes with rank labels included in country names
  ...

  # Create labels with rank and country name combined
  ...
  
  # Add value labels
  ...
  
  # Style improvements
  ...
  
  # plt.tight_layout()
  # plt.show()
  
  print("💡 Ordered bar charts are ideal for comparing values and showing clear rankings")
```

### Exercise 1.2: Lollipop Chart

**Task**: Create a lollipop chart comparing GDP growth between 2010 and 2019 for the G7 countries.

**Requirements**:

- Show both 2010 and 2019 values on the same chart
- Use different markers for each year
- Sort by 2019 values
- Add a legend and appropriate labels

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

  # Exclude non-country entities (regions, income groups)
  non_country_entities  = {
      'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
      'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
      'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
      'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
      'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
  }
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")


  # G7 countries
  g7_countries = ['United States', 'Japan', 'Germany', 'United Kingdom', 
                  'France', 'Italy', 'Canada']
  
  # Get data for G7 countries in 2010 and 2019
  df_g7_2010 = df_countries[(df_countries['Country Name'].isin(g7_countries)) & 
                            (df_countries['Year'] == 2010)].copy()
  df_g7_2019 = df_countries[(df_countries['Country Name'].isin(g7_countries)) & 
                            (df_countries['Year'] == 2019)].copy()
  
  # Merge and sort by 2019 values
  df_g7 = pd.merge(df_g7_2010[['Country Name', 'Value']], 
                   df_g7_2019[['Country Name', 'Value']], 
                   on='Country Name', suffixes=('_2010', '_2019'))
  df_g7 = df_g7.sort_values('Value_2019', ascending=True)
  
  # Create shorter labels for countries
  country_labels = {
      'United States': 'USA',
      'United Kingdom': 'UK',
      'Japan': 'JPN',
      'Germany': 'GER',
      'France': 'FRA',
      'Italy': 'ITA',
      'Canada': 'CAN'
  }
  df_g7['Short_Name'] = df_g7['Country Name'].map(country_labels)
  
  # Create figure with more horizontal space
  fig, ax = plt.subplots(figsize=(14, 7))
  
  # Plot lollipops
  # y_positions = np.arange(len(df_g7))
  
  # Draw lines
  ...
  
  # Draw circles for 2010 with stronger color
  ...
  
  # Draw circles for 2019 with stronger color
  ...
  
  # Customize axes with short labels
  ...
  
  # Add value labels with stronger colors and smart positioning
  ...
  
  # Style improvements
  ...
  
  # Add growth arrows
  ...
  
  # plt.tight_layout()
  # plt.show()
  
  print("📊 Lollipop charts elegantly show changes between two time points")
```

### Exercise 1.3: Slope Chart

**Task**: Create a slope chart showing how the ranking of the top 10 economies changed between 2000 and 2019.

**Requirements**:

- Show rankings (not values) on the y-axis
- Connect same countries with lines
- Color code lines by change direction
- Label countries on both sides

```yaml
f_type: "codex_"
height_in_px: 600
inline: |
  import matplotlib.pyplot as plt
  import pandas as pd
  import numpy as np
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
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")

  # Get rankings for all countries in both years
  df_2000 = df_countries[df_countries['Year'] == 2000].copy()
  df_2000 = df_2000.sort_values('Value', ascending=False).reset_index(drop=True)
  df_2000['Rank_2000'] = df_2000.index + 1
  
  df_2019 = df_countries[df_countries['Year'] == 2019].copy()
  df_2019 = df_2019.sort_values('Value', ascending=False).reset_index(drop=True)
  df_2019['Rank_2019'] = df_2019.index + 1
  
  # Get top 10 from each year
  top10_2000 = set(df_2000.head(10)['Country Name'])
  top10_2019 = set(df_2019.head(10)['Country Name'])
  
  # Countries that were in top 10 in either year
  countries_to_show = top10_2000.union(top10_2019)
  
  # Filter and merge data for these countries
  df_2000_filtered = df_2000[df_2000['Country Name'].isin(countries_to_show)]
  df_2019_filtered = df_2019[df_2019['Country Name'].isin(countries_to_show)]
  
  df_merged = pd.merge(df_2000_filtered[['Country Name', 'Rank_2000']], 
                       df_2019_filtered[['Country Name', 'Rank_2019']], 
                       on='Country Name', how='inner')
  
  # Create figure
  fig, ax = plt.subplots(figsize=(14, 10))
  
  # Plot lines
  ...
  
  # Customize axes - adjust y-limits to show all ranks
  ...
  
  # Remove spines
  ...
  
  # Add vertical lines at x positions
  ...
  
  # Add legend
  ...
  
  # Remove y-axis ticks
  ...
  
  # plt.tight_layout()
  # plt.show()
  
  print("📈 Slope charts effectively show ranking changes over time")
```

### Exercise 1.4: Dot Strip Plot

**Task**: Create a dot strip plot showing nominal GDP ranges for different regions in 2019.

**Requirements**:

- Group by regions
- Show individual countries as dots
- Highlight median values

```yaml
f_type: "codex_"
height_in_px: 1000
inline: |

  import matplotlib.pyplot as plt
  import pandas as pd
  import numpy as np
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
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")


  # Comprehensive regional classification for all countries
  regions_map = {
      # North America
      'United States': 'North America',
      'Canada': 'North America',
      'Mexico': 'North America',
      'Bermuda': 'North America',
      'Greenland': 'North America',
      
      # Europe
      'Germany': 'Europe',
      'France': 'Europe',
      'United Kingdom': 'Europe',
      'Italy': 'Europe',
      'Spain': 'Europe',
      'Netherlands': 'Europe',
      'Belgium': 'Europe',
      'Switzerland': 'Europe',
      'Austria': 'Europe',
      'Sweden': 'Europe',
      'Norway': 'Europe',
      'Denmark': 'Europe',
      'Finland': 'Europe',
      'Ireland': 'Europe',
      'Portugal': 'Europe',
      'Greece': 'Europe',
      'Poland': 'Europe',
      'Czechia': 'Europe',
      'Romania': 'Europe',
      'Hungary': 'Europe',
      'Bulgaria': 'Europe',
      'Croatia': 'Europe',
      'Slovak Republic': 'Europe',
      'Slovenia': 'Europe',
      'Lithuania': 'Europe',
      'Latvia': 'Europe',
      'Estonia': 'Europe',
      'Luxembourg': 'Europe',
      'Malta': 'Europe',
      'Cyprus': 'Europe',
      'Iceland': 'Europe',
      'Albania': 'Europe',
      'Serbia': 'Europe',
      'Bosnia and Herzegovina': 'Europe',
      'North Macedonia': 'Europe',
      'Montenegro': 'Europe',
      'Kosovo': 'Europe',
      'Moldova': 'Europe',
      'Belarus': 'Europe',
      'Ukraine': 'Europe',
      'Russian Federation': 'Europe',
      'Andorra': 'Europe',
      'Monaco': 'Europe',
      'Liechtenstein': 'Europe',
      'San Marino': 'Europe',
      'Faroe Islands': 'Europe',
      'Isle of Man': 'Europe',
      'Channel Islands': 'Europe',
      
      # East Asia & Pacific
      'China': 'East Asia & Pacific',
      'Japan': 'East Asia & Pacific',
      'Korea, Rep.': 'East Asia & Pacific',
      'Indonesia': 'East Asia & Pacific',
      'Thailand': 'East Asia & Pacific',
      'Malaysia': 'East Asia & Pacific',
      'Singapore': 'East Asia & Pacific',
      'Philippines': 'East Asia & Pacific',
      'Viet Nam': 'East Asia & Pacific',
      'Myanmar': 'East Asia & Pacific',
      'Cambodia': 'East Asia & Pacific',
      'Lao PDR': 'East Asia & Pacific',
      'Hong Kong SAR, China': 'East Asia & Pacific',
      'Macao SAR, China': 'East Asia & Pacific',
      'Mongolia': 'East Asia & Pacific',
      'Brunei Darussalam': 'East Asia & Pacific',
      'Timor-Leste': 'East Asia & Pacific',
      'Australia': 'East Asia & Pacific',
      'New Zealand': 'East Asia & Pacific',
      'Papua New Guinea': 'East Asia & Pacific',
      'Fiji': 'East Asia & Pacific',
      'Solomon Islands': 'East Asia & Pacific',
      'Vanuatu': 'East Asia & Pacific',
      'Samoa': 'East Asia & Pacific',
      'Tonga': 'East Asia & Pacific',
      'Kiribati': 'East Asia & Pacific',
      'Palau': 'East Asia & Pacific',
      'Marshall Islands': 'East Asia & Pacific',
      'Micronesia, Fed. Sts.': 'East Asia & Pacific',
      'Nauru': 'East Asia & Pacific',
      'Tuvalu': 'East Asia & Pacific',
      'American Samoa': 'East Asia & Pacific',
      'French Polynesia': 'East Asia & Pacific',
      'Guam': 'East Asia & Pacific',
      'New Caledonia': 'East Asia & Pacific',
      'Northern Mariana Islands': 'East Asia & Pacific',
      
      # South Asia
      'India': 'South Asia',
      'Pakistan': 'South Asia',
      'Bangladesh': 'South Asia',
      'Sri Lanka': 'South Asia',
      'Nepal': 'South Asia',
      'Afghanistan': 'South Asia',
      'Bhutan': 'South Asia',
      'Maldives': 'South Asia',
      
      # Middle East & North Africa
      'Saudi Arabia': 'Middle East & North Africa',
      'United Arab Emirates': 'Middle East & North Africa',
      'Egypt, Arab Rep.': 'Middle East & North Africa',
      'Israel': 'Middle East & North Africa',
      'Iran, Islamic Rep.': 'Middle East & North Africa',
      'Iraq': 'Middle East & North Africa',
      'Algeria': 'Middle East & North Africa',
      'Morocco': 'Middle East & North Africa',
      'Kuwait': 'Middle East & North Africa',
      'Qatar': 'Middle East & North Africa',
      'Oman': 'Middle East & North Africa',
      'Lebanon': 'Middle East & North Africa',
      'Jordan': 'Middle East & North Africa',
      'Tunisia': 'Middle East & North Africa',
      'Libya': 'Middle East & North Africa',
      'Bahrain': 'Middle East & North Africa',
      'Yemen, Rep.': 'Middle East & North Africa',
      'Syrian Arab Republic': 'Middle East & North Africa',
      'West Bank and Gaza': 'Middle East & North Africa',
      'Djibouti': 'Middle East & North Africa',
      
      # Sub-Saharan Africa
      'Nigeria': 'Sub-Saharan Africa',
      'South Africa': 'Sub-Saharan Africa',
      'Ethiopia': 'Sub-Saharan Africa',
      'Kenya': 'Sub-Saharan Africa',
      'Ghana': 'Sub-Saharan Africa',
      'Angola': 'Sub-Saharan Africa',
      'Tanzania': 'Sub-Saharan Africa',
      'Uganda': 'Sub-Saharan Africa',
      'Zimbabwe': 'Sub-Saharan Africa',
      'Mozambique': 'Sub-Saharan Africa',
      'Zambia': 'Sub-Saharan Africa',
      'Senegal': 'Sub-Saharan Africa',
      'Mali': 'Sub-Saharan Africa',
      'Burkina Faso': 'Sub-Saharan Africa',
      'Niger': 'Sub-Saharan Africa',
      'Malawi': 'Sub-Saharan Africa',
      'Madagascar': 'Sub-Saharan Africa',
      'Cameroon': 'Sub-Saharan Africa',
      "Cote d'Ivoire": 'Sub-Saharan Africa',
      'Guinea': 'Sub-Saharan Africa',
      'Benin': 'Sub-Saharan Africa',
      'Rwanda': 'Sub-Saharan Africa',
      'Chad': 'Sub-Saharan Africa',
      'Somalia': 'Sub-Saharan Africa',
      'Burundi': 'Sub-Saharan Africa',
      'Togo': 'Sub-Saharan Africa',
      'Sierra Leone': 'Sub-Saharan Africa',
      'Liberia': 'Sub-Saharan Africa',
      'Central African Republic': 'Sub-Saharan Africa',
      'Mauritania': 'Sub-Saharan Africa',
      'Eritrea': 'Sub-Saharan Africa',
      'Gambia, The': 'Sub-Saharan Africa',
      'Botswana': 'Sub-Saharan Africa',
      'Namibia': 'Sub-Saharan Africa',
      'Gabon': 'Sub-Saharan Africa',
      'Lesotho': 'Sub-Saharan Africa',
      'Guinea-Bissau': 'Sub-Saharan Africa',
      'Equatorial Guinea': 'Sub-Saharan Africa',
      'Mauritius': 'Sub-Saharan Africa',
      'Eswatini': 'Sub-Saharan Africa',
      'Congo, Dem. Rep.': 'Sub-Saharan Africa',
      'Congo, Rep.': 'Sub-Saharan Africa',
      'Cabo Verde': 'Sub-Saharan Africa',
      'Comoros': 'Sub-Saharan Africa',
      'Sao Tome and Principe': 'Sub-Saharan Africa',
      'Seychelles': 'Sub-Saharan Africa',
      'Sudan': 'Sub-Saharan Africa',
      'South Sudan': 'Sub-Saharan Africa',
      
      # Latin America & Caribbean
      'Brazil': 'Latin America & Caribbean',
      'Argentina': 'Latin America & Caribbean',
      'Colombia': 'Latin America & Caribbean',
      'Chile': 'Latin America & Caribbean',
      'Peru': 'Latin America & Caribbean',
      'Venezuela, RB': 'Latin America & Caribbean',
      'Ecuador': 'Latin America & Caribbean',
      'Bolivia': 'Latin America & Caribbean',
      'Paraguay': 'Latin America & Caribbean',
      'Uruguay': 'Latin America & Caribbean',
      'Guatemala': 'Latin America & Caribbean',
      'Cuba': 'Latin America & Caribbean',
      'Dominican Republic': 'Latin America & Caribbean',
      'Haiti': 'Latin America & Caribbean',
      'Honduras': 'Latin America & Caribbean',
      'El Salvador': 'Latin America & Caribbean',
      'Nicaragua': 'Latin America & Caribbean',
      'Costa Rica': 'Latin America & Caribbean',
      'Panama': 'Latin America & Caribbean',
      'Jamaica': 'Latin America & Caribbean',
      'Trinidad and Tobago': 'Latin America & Caribbean',
      'Guyana': 'Latin America & Caribbean',
      'Suriname': 'Latin America & Caribbean',
      'Belize': 'Latin America & Caribbean',
      'Barbados': 'Latin America & Caribbean',
      'Bahamas, The': 'Latin America & Caribbean',
      'Puerto Rico': 'Latin America & Caribbean',
      'St. Lucia': 'Latin America & Caribbean',
      'Grenada': 'Latin America & Caribbean',
      'St. Vincent and the Grenadines': 'Latin America & Caribbean',
      'Antigua and Barbuda': 'Latin America & Caribbean',
      'Dominica': 'Latin America & Caribbean',
      'St. Kitts and Nevis': 'Latin America & Caribbean',
      'Cayman Islands': 'Latin America & Caribbean',
      'Aruba': 'Latin America & Caribbean',
      'Virgin Islands (U.S.)': 'Latin America & Caribbean',
      'Curacao': 'Latin America & Caribbean',
      'Sint Maarten (Dutch part)': 'Latin America & Caribbean',
      'Turks and Caicos Islands': 'Latin America & Caribbean',
      'St. Martin (French part)': 'Latin America & Caribbean',
      
      # Central Asia
      'Kazakhstan': 'Central Asia',
      'Uzbekistan': 'Central Asia',
      'Turkmenistan': 'Central Asia',
      'Tajikistan': 'Central Asia',
      'Kyrgyz Republic': 'Central Asia',
      'Azerbaijan': 'Central Asia',
      'Armenia': 'Central Asia',
      'Georgia': 'Central Asia',
      
      # Turkey (Bridge between Europe and Asia)
      'Turkiye': 'Europe'  # Often classified with Europe
  }
  
  # Filter for 2019 and get top 50 countries by GDP
  df_2019 = df_countries[df_countries['Year'] == 2019].copy()
  df_2019 = df_2019.sort_values('Value', ascending=False).head(50)
  
  # Add region column
  df_2019['Region'] = df_2019['Country Name'].map(regions_map)
  
  # Remove countries without region mapping
  df_2019_selected = df_2019.dropna(subset=['Region'])
  
  # Normalize values (as proxy for per capita - simplified)
  # In reality, you'd need population data
  df_2019_selected['Value_normalized'] = df_2019_selected['Value'] / 1e9
  
  # Create figure
  fig, ax = plt.subplots(figsize=(14, 8))
  
  # Get unique regions
  regions = df_2019_selected['Region'].unique()
  region_colors = plt.cm.Set3(np.linspace(0, 1, len(regions)))
  
  # Plot dots for each region
  ...
  
  # Customize axes
  ...
  
  # Style improvements
  ...
  
  # Add legend for median and labeled countries
  # from matplotlib.lines import Line2D
  # from matplotlib.patches import Patch
  # legend_elements = [
  #     Line2D([0], [0], color='black', lw=2, label='Median GDP'),
  #     Patch(facecolor='none', edgecolor='none', label='Labels show largest # economy per region')
  # ]
  # ax.legend(handles=legend_elements, loc='upper right', frameon=True, # # framealpha=0.95, 
  #         fontsize=10)
  
  #plt.tight_layout()
  # plt.show()
  
  print("🔵 Dot strip plots show distributions and individual data points clearly")
```

### Exercise 1.5: Bump Chart

**Task**: Create a bump chart showing ranking evolution of selected economies from 2010 to 2019.

**Requirements**:

- Track ranking changes year by year
- Use smooth lines to connect rankings
- Apply distinct colors for each country
- Show all intermediate years

```yaml
f_type: "codex_"
height_in_px: 600
inline: |


  import matplotlib.pyplot as plt
  import pandas as pd
  import numpy as np
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
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")

  # Select countries to track
  countries_to_track = ['United States', 'China', 'Japan', 'Germany', 
                       'India', 'United Kingdom', 'France', 'Brazil']
  
  # Get data for years 2010-2019
  years = range(2010, 2020)
  rankings_data = {}
  
  for year in years:
      df_year = df_countries[df_countries['Year'] == year].copy()
      df_year = df_year.sort_values('Value', ascending=False)
      df_year['Rank'] = range(1, len(df_year) + 1)
      
      for country in countries_to_track:
          if country not in rankings_data:
              rankings_data[country] = []
          
          country_rank = df_year[df_year['Country Name'] == country]['Rank'].values
          if len(country_rank) > 0:
              rankings_data[country].append(country_rank[0])
          else:
              rankings_data[country].append(None)
  
  # Create figure
  fig, ax = plt.subplots(figsize=(14, 8))
  
  # Color palette
  colors = plt.cm.tab10(np.linspace(0, 1, len(countries_to_track)))
  
  # Plot lines for each country
  ...
  
  # Customize axes
  ...
  
  # Set x-axis ticks
  ...
  
  # Set y-axis ticks
  ...
  
  # Add grid
  ...
  
  # Style improvements
  ...
  
  # plt.tight_layout()
  # plt.show()
  
  print("📊 Bump charts excel at showing ranking changes across multiple time periods")
```

### Exercise 1.6: Ordered Proportional Symbol

**Task**: Create a proportional symbol chart showing GDP sizes with country positions based on GDP growth rate.

**Requirements**:

- Calculate growth rate between 2010 and 2019
- Filter for countries with significant GDP growth rate (top 30 in 2019)
- Size circles by 2019 GDP
- Position on x-axis by growth rate
- Color by GDP size category

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

  # Exclude non-country entities (regions, income groups)
  non_country_entities  = {
      'AFE', 'AFW', 'ARB', 'CSS', 'CEB', 'CHI', 'EAR', 'EAS', 'TEA', 'EAP', 
      'EMU', 'ECS', 'TEC', 'ECA', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 
      'IDB', 'IDX', 'IDA', 'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 
      'LMC', 'MEA', 'TMN', 'MNA', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 
      'PRE', 'SAS', 'TSA', 'SSF', 'TSS', 'SSA', 'SST', 'UMC', 'WLD'
  }
  df_countries = df[~df['Country Code'].isin(non_country_entities)]

  df_non_countries = df[df['Country Code'].isin(non_country_entities)]

  print(f"Dataset loaded: {df_countries.shape[0]} rows, {df_countries['Country Name'].nunique()} countries")



  # Get data for 2010 and 2019
  df_2010 = df_countries[df_countries['Year'] == 2010][['Country Name', 'Value']]
  df_2019 = df_countries[df_countries['Year'] == 2019][['Country Name', 'Value']]
  
  # Merge and calculate growth
  df_growth = pd.merge(df_2010, df_2019, on='Country Name', suffixes=('_2010', '_2019'))
  df_growth['Growth_Rate'] = ((df_growth['Value_2019'] - df_growth['Value_2010']) / 
                              df_growth['Value_2010'] * 100)
  
  # Filter for countries with significant GDP (top 30 in 2019)
  df_growth = df_growth.nlargest(30, 'Value_2019')
  
  # Create figure
  fig, ax = plt.subplots(figsize=(14, 8))
  
  # Normalize bubble sizes
  max_gdp = df_growth['Value_2019'].max()
  sizes = (df_growth['Value_2019'] / max_gdp * 3000) + 100
  
  # Create color categories
  df_growth['Size_Category'] = pd.cut(df_growth['Value_2019'], 
                                       bins=[0, 1e12, 5e12, 10e12, float('inf')],
                                       labels=['< $1T', '$1-5T', '$5-10T', '> $10T'])
  
  # Color map
  color_map = {'< $1T': '#3498DB', '$1-5T': '#2ECC71', 
               '$5-10T': '#F39C12', '> $10T': '#E74C3C'}
  colors = [color_map[cat] for cat in df_growth['Size_Category']]
  
  # Plot bubbles
  ...
  
  # Add country labels
  ...
  
  # Customize axes
  ...
  
  # Remove y-axis labels
  ...
  
  # Add vertical line at 0% growth
  ...
  
  # Add vertical line at 100% growth
  ...
  
  # Grid
  ...
  
  # Style
  ...
  
  # Legend
  ...
  
  # Size legend
  ...
  
  # plt.tight_layout()
  # plt.show()
  
  print("⭕ Proportional symbols effectively show multiple dimensions of ranking data")
```




## Correction


[Accéder à la correction](session_2_c0correction.md)
{: .alert .alert-success .alert-soft}